#!/usr/bin/env python3
"""
run_unified_analyzer_batch.py — Pipeline Analyzer + Evaluator (Unified Model 1 + Ground Truth Evaluator Model 2)

This script implements Section 7b of spanish_videos_lab in a batch runner for the 14 Ground Truth videos:
- Model 1 (Analyzer): Single-pass unified prompt that extracts visual components and compiles the final logical graph.
- Model 2 (Evaluator): Compares Model 1 output with CloudScape Ground Truth, generating a structured discrepancy report.
- Saves results to `batch_results_v5_unified_analyzer.json` compatible with `prompt_batch_ablation_lab.ipynb`.
"""

import base64
import csv
import json

from datetime import datetime
from pathlib import Path
import shutil
import sys
import time

import networkx as nx
import pandas as pd

# Paths setup
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
LAB_DIR = CURRENT_DIR if CURRENT_DIR.name == "whiteboard_selection_lab" else PROJECT_ROOT / "whiteboard_selection_lab"

sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(LAB_DIR / "algorithms"))

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from scripts.core.graph_builder import create_graph_from_cloudscape_json
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

# Gemini API Client
from google import genai
from google.genai import types
from pydantic import BaseModel

# Data Directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
GOOD_WHITEBOARD_DIR = DATA_DIR / "good_whiteboard"
GT_DIR = DATA_DIR / "cloudscape_gt"
SERVICES_CSV = GT_DIR / "services.csv" if (GT_DIR / "services.csv").exists() else DATA_DIR / "services.csv"
LAB_WORKSPACE = LAB_DIR / "lab_workspace"
TRANSCRIPTIONS_DIR = LAB_DIR / "transcriptions"

ALL_14_VIDEOS = [
    "-3lnf5lzsH0", "-kA0ahrhX3I", "-wLEkq21cvA", "07lfvavMdfU", "1aYoIZvabbk",
    "2L0m28ZLmtE", "2e3vOxsHekE", "6CgqEzyWpeA", "6EUknQqaV1w", "6YkguepAQuQ",
    "BZ32w0SSAoY", "Cgv0kfp_6xQ", "wjtSHyENv0I", "ww5fiygF6eg"
]

EXPERIMENT_LABEL = "v5_unified_analyzer"
MODEL_NAME = "gemini-2.5-flash"
FORCE_RERUN = False

# ══════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — MODEL 1 (Analyzer)
# ══════════════════════════════════════════════════════════════
class GraphMetadata(BaseModel):
    name: str
    link: str
    categories: str
    graph_usable: bool
    notes: str

class Node(BaseModel):
    id: str
    service: str
    name: str
    notes: str

class Edge(BaseModel):
    source: str
    target: str
    flow_id: int
    seq: str
    type: str
    notes: str

class FinalArchitectureSchema(BaseModel):
    step_by_step_reasoning: str
    graph: GraphMetadata
    nodes: list[Node]
    edges: list[Edge]

# ══════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — MODEL 2 (Evaluator)
# ══════════════════════════════════════════════════════════════
class NodeDiscrepancy(BaseModel):
    node_id_gt: str
    node_id_gen: str
    service_gt: str
    service_gen: str
    issue_type: str   # "missing" | "hallucinated" | "wrong_service" | "wrong_name"
    severity: str     # "critical" | "minor"
    explanation: str

class EdgeDiscrepancy(BaseModel):
    source_gt: str
    target_gt: str
    source_gen: str
    target_gen: str
    issue_type: str   # "missing" | "hallucinated" | "wrong_type" | "wrong_flow"
    severity: str
    explanation: str

class PromptImprovementSuggestion(BaseModel):
    category: str     # "node_rules" | "edge_rules" | "vocabulary" | "prompt_structure"
    suggestion: str
    priority: str     # "high" | "medium" | "low"

class EvaluationSchema(BaseModel):
    overall_score: float
    node_precision: float
    node_recall: float
    edge_precision: float
    edge_recall: float
    summary: str
    node_discrepancies: list[NodeDiscrepancy]
    edge_discrepancies: list[EdgeDiscrepancy]
    prompt_improvement_suggestions: list[PromptImprovementSuggestion]

# ══════════════════════════════════════════════════════════════
# PROMPT UNIFICADO — MODELO 1 (Analyzer)
# ══════════════════════════════════════════════════════════════
UNIFIED_ANALYZER_PROMPT = """You are an expert AWS Solutions Architect analyzing a whiteboard diagram from an AWS "This is My Architecture" video.

Your task is to extract the complete cloud architecture from the provided whiteboard image and audio transcript, producing a final logical architecture graph in a single pass.

## STEP 1 — VISUAL EXTRACTION:
1. Identify all active systems, databases, cloud services, and actors VISIBLE on the whiteboard.
2. Identify BOXES or dashed containers. If a service (e.g., SAP) is drawn inside another box (e.g., EC2), note this containment.
3. Register ALL lines or arrows explicitly drawn between entities on the whiteboard, noting source, target, and direction.
4. Do NOT include transient files, packages, or disk images (like AMIs) as entities.

## STEP 2 — GRAPH COMPILATION:
Using your visual extraction and the audio transcript, compile the final logical architecture graph.

## VALID VOCABULARY LISTS (CRITICAL):
You may ONLY use exact values from these lists for the "service" field.

AWS Services:
<AWS_SERVICES_PLACEHOLDER>

User and Client Actors:
<USER_ACTORS_PLACEHOLDER>

## NODE RULES:
1. **Strict Normalization (CRITICAL):** The "service" field MUST match exactly with an element from the VALID VOCABULARY LISTS.
2. **Numeric Identifiers:** The "id" field MUST be a sequential integer in string format ("0", "1", "2").
3. **Audio-Driven Expansion:** If the whiteboard shows a generic abstraction (e.g., "AWS" cloud icon) but the transcript lists specific services (e.g., S3, SNS, SQS), expand into separate nodes for each mentioned service.
4. **Dynamic Logical Fusion:** If multiple icons of the same service act as a single logical unit, FUSE them. If they perform distinct steps, KEEP SEPARATE.
5. **Pruning:** Remove generic human actors or purely physical concepts. Keep system entry points.
6. **Note Assimilation:** Extract specific constraints and metrics from the transcript into the "notes".
7. Map on-premises/external systems to "ThirdParty" and actors to the appropriate User type.

## EDGE AND FLOW RULES:
1. **Flow Segmentation (`flow_id`):** Group related actions into distinct workflows using an integer `flow_id` (starting at 0).
2. **Chronological Sequence (`seq`):** Order events within a flow using string integers ("0", "1"). Use prime for parallel actions ("1" and "1'").
3. **Edge Types (`type`):** Use "data" for payload transfers/reads/writes. Use "control" for events, triggers, or asynchronous invocations.

## MULTILINGUAL TRANSLATION RULE:
Translate all output text fields (notes, graph name, reasoning, etc.) into ENGLISH.
"""

# ══════════════════════════════════════════════════════════════
# PROMPT — MODELO 2 (Evaluator)
# ══════════════════════════════════════════════════════════════
EVALUATOR_PROMPT_TEMPLATE = """You are an expert evaluator of cloud architecture graph extraction models. Your task is to compare a GENERATED architecture graph against the GROUND TRUTH graph and produce a detailed discrepancy analysis.

## GROUND TRUTH GRAPH (Reference — this is the correct answer):
<GROUND_TRUTH_PLACEHOLDER>

## GENERATED GRAPH (Model output — this is what needs to be evaluated):
<GENERATED_GRAPH_PLACEHOLDER>

## EVALUATION INSTRUCTIONS:

### Node Analysis:
1. Compare the set of services in the generated graph vs ground truth.
2. Identify MISSING nodes: services present in GT but absent in generated.
3. Identify HALLUCINATED nodes: services present in generated but absent in GT.
4. Identify WRONG SERVICE mappings: nodes where the service name was misidentified.
5. For each discrepancy, classify severity as "critical" (affects architecture understanding) or "minor" (cosmetic/naming).

### Edge Analysis:
1. Compare edges by (source_service → target_service) pairs.
2. Identify MISSING edges: connections in GT but not in generated.
3. Identify HALLUCINATED edges: connections in generated but not in GT.
4. Identify WRONG TYPE edges: correct connection but wrong edge type (data vs control).
5. Identify WRONG FLOW edges: correct connection but assigned to wrong flow_id.

### Metrics:
- Calculate node_precision, node_recall based on service set overlap.
- Calculate edge_precision, edge_recall based on (src_service, tgt_service) pair overlap.
- Calculate overall_score as the harmonic mean of all four metrics.

### Prompt Improvement Suggestions:
Based on the patterns of errors you observe, provide SPECIFIC, ACTIONABLE suggestions for improving the prompt that was used to generate the architecture. Categorize each suggestion as:
- "node_rules": Rules about which nodes to include/exclude
- "edge_rules": Rules about how to connect nodes
- "vocabulary": Rules about service name normalization
- "prompt_structure": General prompt engineering improvements

Prioritize suggestions as "high" (would fix critical errors), "medium" (would fix minor errors), or "low" (nice-to-have improvements).
"""

_client = None

def get_gemini_client():
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no encontrada en .env")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client

def load_services_catalogs():
    aws_services, user_actors = set(), set()
    catalog_dict = {}
    if SERVICES_CSV.exists():
        with open(SERVICES_CSV, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                capability = row.get("capability", "").strip().lower()
                if not name:
                    continue
                catalog_dict[name] = {"capability": capability}
                if capability == "user" or name.startswith("User"):
                    user_actors.add(name)
                else:
                    aws_services.add(name)
    return ", ".join(sorted(aws_services)), ", ".join(sorted(user_actors)), catalog_dict

AWS_SERVICES_STR, USER_ACTORS_STR, CATALOG_DICT = load_services_catalogs()

def call_gemini_api(full_prompt, mime=None, image_b64=None, model_name=MODEL_NAME, response_schema=None):
    client = get_gemini_client()
    max_retries = 30
    retry_delay = 20

    config_args = {"response_mime_type": "application/json"}
    if response_schema is not None:
        config_args["response_schema"] = response_schema
    config = types.GenerateContentConfig(**config_args)

    contents = []
    parts = [{"text": full_prompt}]
    if mime and image_b64:
        parts.append({"inline_data": {"mime_type": mime, "data": image_b64}})
    contents.append({"parts": parts})

    for attempt in range(max_retries):
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            return json.loads(res.text)
        except Exception as e:
            err_msg = str(e).upper()
            if attempt < max_retries - 1 and any(k in err_msg for k in ["503", "429", "RESOURCE_EXHAUSTED", "LIMIT"]):
                delay = 40 if ("429" in err_msg or "RESOURCE" in err_msg) else retry_delay
                print(f"  ⏳ Límite de cuota / Servidor ocupado en '{model_name}'. Esperando {delay}s antes de reintentar (intento {attempt+1}/{max_retries})...")
                time.sleep(delay)
                retry_delay = min(retry_delay * 2, 60)
            else:
                print(f"  ❌ Error en modelo estricto '{model_name}': {e}")
                raise e

def serialize_graph_for_prompt(G):
    lines = [
        f"Graph Name: {G.graph.get('name', 'N/A')}",
        f"Categories: {G.graph.get('categories', 'N/A')}",
        f"Notes: {G.graph.get('notes', '')}",
        f"\nNodes ({G.number_of_nodes()}):"
    ]
    for nid, attrs in G.nodes(data=True):
        svc = attrs.get('service', '?')
        name = attrs.get('name', '')
        notes = attrs.get('notes', '')
        line = f"  [{nid}] service={svc}"
        if name: line += f", name={name}"
        if notes: line += f", notes={notes[:100]}"
        lines.append(line)
    lines.append(f"\nEdges ({G.number_of_edges()}):")
    for src, tgt, attrs in G.edges(data=True):
        src_svc = G.nodes[src].get('service', '?') if src in G.nodes else '?'
        tgt_svc = G.nodes[tgt].get('service', '?') if tgt in G.nodes else '?'
        flow = attrs.get('flow_id', '?')
        seq = attrs.get('seq', '?')
        etype = attrs.get('type', 'data')
        lines.append(f"  {src_svc} -> {tgt_svc} (flow={flow}, seq={seq}, type={etype})")
    return "\n".join(lines)

def serialize_json_graph_for_prompt(analysis_res):
    lines = []
    g_meta = analysis_res.get("graph", {})
    lines.append(f"Graph Name: {g_meta.get('name', 'N/A')}")
    lines.append(f"Reasoning: {analysis_res.get('step_by_step_reasoning', '')[:200]}")
    
    nodes = analysis_res.get("nodes", [])
    lines.append(f"\nNodes ({len(nodes)}):")
    node_svc_map = {}
    for n in nodes:
        node_svc_map[str(n.get('id'))] = n.get('service', '?')
        lines.append(f"  [{n.get('id')}] service={n.get('service')}, name={n.get('name')}")
        
    edges = analysis_res.get("edges", [])
    lines.append(f"\nEdges ({len(edges)}):")
    for e in edges:
        src_svc = node_svc_map.get(str(e.get('source')), e.get('source'))
        tgt_svc = node_svc_map.get(str(e.get('target')), e.get('target'))
        lines.append(f"  {src_svc} -> {tgt_svc} (flow={e.get('flow_id')}, seq={e.get('seq')}, type={e.get('type')})")
    return "\n".join(lines)

def run_unified_analyzer_experiment(video_ids=ALL_14_VIDEOS, force=FORCE_RERUN):
    print("=" * 80)
    print(f"🚀 INICIANDO EXPERIMENTO: '{EXPERIMENT_LABEL}' (Unified Analyzer + Evaluator)")
    print(f"   • Modelo: {MODEL_NAME}")
    print(f"   • Total Videos: {len(video_ids)}")
    print("=" * 80)

    results = []
    discrepancies_log = LAB_WORKSPACE / "discrepancies_log.jsonl"

    for idx, video_id in enumerate(video_ids, 1):
        print(f"[{idx}/{len(video_ids)}] Procesando video: {video_id}...")
        workspace = LAB_WORKSPACE / video_id
        workspace.mkdir(parents=True, exist_ok=True)

        local_wb = workspace / "best_whiteboard.jpg"
        wb_src = GOOD_WHITEBOARD_DIR / f"{video_id}.jpg"
        if not wb_src.exists():
            print(f"  ❌ No existe pizarra para {video_id}")
            continue
        if not local_wb.exists() or force:
            shutil.copy2(wb_src, local_wb)

        t_src = RAW_DIR / f"{video_id}_transcript.json"
        t_lab = TRANSCRIPTIONS_DIR / f"{video_id}_transcript.json"
        if t_src.exists() and (not t_lab.exists() or force):
            TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(t_src, t_lab)

        transcript_text = ""
        target_t = t_lab if t_lab.exists() else t_src
        if target_t.exists():
            with open(target_t, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    transcript_text = " ".join(s.get("text", "").strip() for s in data)
                elif isinstance(data, dict):
                    transcript_text = data.get("text", "")

        img_b64 = base64.b64encode(local_wb.read_bytes()).decode("utf-8")

        suffix = f"_{EXPERIMENT_LABEL}"
        an_path = workspace / f"test_analysis{suffix}.json"
        gml_path = workspace / f"test_graph{suffix}.graphml"
        eval_path = workspace / f"evaluation{suffix}.json"

        # Model 1: Unified Analyzer
        if an_path.exists() and not force:
            print(f"  ✓ Cargando análisis unificado en caché ({an_path.name})...")
            with open(an_path, "r", encoding="utf-8") as f:
                analyzer_res = json.load(f)
        else:
            print(f"  🔍 Model 1 (Unified Analyzer): Extrayendo componentes y grafos...")
            p1 = UNIFIED_ANALYZER_PROMPT.replace("<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR).replace("<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR)
            full_prompt_1 = f"{p1}\n\n## FULL TRANSCRIPT:\n{transcript_text}"
            analyzer_res = call_gemini_api(full_prompt_1, "image/jpeg", img_b64, MODEL_NAME, response_schema=FinalArchitectureSchema)
            with open(an_path, "w", encoding="utf-8") as f:
                json.dump(analyzer_res, f, indent=2, ensure_ascii=False)

        # Build GraphML
        G = create_graph_from_cloudscape_json(analyzer_res, video_id=video_id)
        nx.write_graphml(G, str(gml_path))

        # Model 2: Evaluator vs Ground Truth
        gt_path = GT_DIR / f"{video_id}.graphml"
        eval_res = {}
        evaluator_eval = {}

        if gt_path.exists():
            gt_g = nx.read_graphml(str(gt_path))
            eval_res = evaluate_pair(G, gt_g, video_id, CATALOG_DICT)

            if eval_path.exists() and not force:
                with open(eval_path, "r", encoding="utf-8") as f:
                    evaluator_eval = json.load(f)
            else:
                print(f"  🤖 Model 2 (Evaluator): Analizando discrepancias contra Ground Truth...")
                gt_text = serialize_graph_for_prompt(gt_g)
                gen_text = serialize_json_graph_for_prompt(analyzer_res)
                eval_prompt = EVALUATOR_PROMPT_TEMPLATE.replace("<GROUND_TRUTH_PLACEHOLDER>", gt_text).replace("<GENERATED_GRAPH_PLACEHOLDER>", gen_text)
                evaluator_eval = call_gemini_api(eval_prompt, response_schema=EvaluationSchema)
                with open(eval_path, "w", encoding="utf-8") as f:
                    json.dump(evaluator_eval, f, indent=2, ensure_ascii=False)

                # Append to discrepancies log (jsonl)
                log_entry = {
                    "video_id": video_id,
                    "timestamp": datetime.now().isoformat(),
                    "model": MODEL_NAME,
                    "overall_score": evaluator_eval.get("overall_score", 0.0),
                    "node_precision": evaluator_eval.get("node_precision", 0.0),
                    "node_recall": evaluator_eval.get("node_recall", 0.0),
                    "edge_precision": evaluator_eval.get("edge_precision", 0.0),
                    "edge_recall": evaluator_eval.get("edge_recall", 0.0),
                    "num_node_discrepancies": len(evaluator_eval.get("node_discrepancies", [])),
                    "num_edge_discrepancies": len(evaluator_eval.get("edge_discrepancies", [])),
                    "num_suggestions": len(evaluator_eval.get("prompt_improvement_suggestions", [])),
                    "node_discrepancies": evaluator_eval.get("node_discrepancies", []),
                    "edge_discrepancies": evaluator_eval.get("edge_discrepancies", []),
                    "prompt_improvement_suggestions": evaluator_eval.get("prompt_improvement_suggestions", [])
                }
                with open(discrepancies_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

        svc_f1 = eval_res.get("svc_f1", 0.0)
        edge_f1 = eval_res.get("edge_f1", 0.0)
        print(f"  ✅ Video {video_id} finalizado -> Service F1: {svc_f1:.1%} | Edge F1: {edge_f1:.1%}\n")

        results.append({
            "video_id": video_id,
            "status": "success",
            "svc_f1": svc_f1,
            "edge_f1": edge_f1,
            "gen_nodes": G.number_of_nodes(),
            "gen_edges": G.number_of_edges(),
            "overall_score": evaluator_eval.get("overall_score", 0.0),
            "services_missing": list(eval_res.get("missing_services", [])) if eval_res else [],
            "services_hallucinated": list(eval_res.get("hallucinated_services", [])) if eval_res else []
        })

    # Save summary json
    summary_file = LAB_DIR / f"batch_results_{EXPERIMENT_LABEL}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print(f"✅ EXPERIMENTO COMPLETADO. Resumen guardado en: {summary_file}")
    print("=" * 80)

    # Print summary table
    df = pd.DataFrame(results)
    if "svc_f1" in df.columns:
        avg_svc = df["svc_f1"].mean()
        avg_edge = df["edge_f1"].mean()
        print(f"\n📊 PROMEDIOS GLOBALES ({EXPERIMENT_LABEL}):")
        print(f"   • Service F1 Promedio: {avg_svc:.1%}")
        print(f"   • Edge F1 Promedio:    {avg_edge:.1%}\n")
        print(df[["video_id", "svc_f1", "edge_f1", "gen_nodes", "gen_edges", "overall_score"]].to_string(index=False))

    return results

if __name__ == "__main__":
    run_unified_analyzer_experiment()
