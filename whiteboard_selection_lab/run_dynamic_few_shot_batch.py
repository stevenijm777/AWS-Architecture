#!/usr/bin/env python3
"""
run_dynamic_few_shot_batch.py — Dynamic Few-Shot RAG (In-Context Learning) Evaluation Pipeline

This script implements Section 7 of the ablation lab for the 14 Ground Truth videos:
1. Loads world_model.json (Stage 1) for the target video.
2. Extracts detected AWS services.
3. Applies Strict Exclusion Rule: excludes target video_id from candidate pool.
4. Retrieves top 2-3 most similar Ground Truth graphs from data/cloudscape_gt/ using Jaccard similarity.
5. Formats retrieved GT exemplars into JSON in-context learning prompts.
6. Calls Gemini API (Stage 2) with STAGE2_V4_DYNAMIC_FEW_SHOT prompt.
7. Evaluates generated architecture graph against Ground Truth.
8. Compares results vs previous experiment versions (V0, V1, V2, V3, V4).
"""

import base64
import csv
import json
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
from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog
from dynamic_rag_matcher import (
    load_all_ground_truths,
    extract_services_from_world_model,
    find_similar_ground_truths,
    format_few_shot_prompt,
)

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

EXPERIMENT_LABEL = "v4_dynamic_few_shot"
MODEL_NAME = "gemini-3.5-flash"
FORCE_RERUN = False

# Pydantic Schemas for Gemini API
class Entity(BaseModel):
    service: str
    name: str
    type: str
    rationale: str

class VisualConnection(BaseModel):
    source_label: str
    target_label: str
    arrow_direction: str
    description: str

class WorldModelSchema(BaseModel):
    entities: list[Entity]
    visual_connections: list[VisualConnection]

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

# Prompt Definitions
STAGE1_V0_BASELINE = """You are an expert in visual extraction of cloud architectures. Your task is to analyze the provided whiteboard diagram and audio transcript to build a structured "World Model" representing the components and their visual groupings.

Do NOT generate the final graph. Focus strictly on identifying the present entities, how they are visually grouped, and what lines connect them.

## ENTITY IDENTIFICATION AND GROUPING RULES:
1. Identify all active systems, databases, cloud services, and actors VISIBLE on the whiteboard.
2. Identify BOXES or dashed containers. If a service (e.g., SAP) is drawn inside another service or box (e.g., EC2), register both and strictly note this containment in the "rationale".
3. Use valid AWS services from this list: <AWS_SERVICES_PLACEHOLDER>.
4. Identify actors/users from this list: <USER_ACTORS_PLACEHOLDER>. Map on-premises/external systems to "ThirdParty" and actors to "User".
5. Do NOT include transient files, packages, or disk images (like AMIs) as entities.

## VISUAL CONNECTION RULES:
1. Register ALL lines or arrows explicitly drawn between entities on the whiteboard.
2. Note the source, target, and the direction of the arrow.
"""

STAGE2_V4_DYNAMIC_FEW_SHOT = """You are an expert AWS Solutions Architect. Your task is to compile the final logical cloud architecture graph from the provided World Model and audio transcript.

You must generalize your reasoning to deduce the true logical "Ground Truth" architecture based on standard AWS patterns.

## VALID VOCABULARY LISTS (CRITICAL):
You may ONLY use exact values from these lists for the "service" field.

AWS Services:
<AWS_SERVICES_PLACEHOLDER>

User and Client Actors:
<USER_ACTORS_PLACEHOLDER>

## MULTILINGUAL TRANSLATION RULE:
Translate all output text fields (notes, graph name, reasoning, etc.) into ENGLISH.

## WORLD MODEL (BASE INPUT):
Use this as your visual inventory.
<WORLD_MODEL_PLACEHOLDER>

## DYNAMIC FEW-SHOT IN-CONTEXT EXAMPLES (REFERENCE GT PATTERNS):
Study the following reference architecture examples with similar AWS service topologies. Use their edge flow structure and node naming granularity as in-context learning guidance:

<FEW_SHOT_PLACEHOLDER>

## NODE RULES (PRUNING, FUSION, AND AUDIO-DRIVEN EXPANSION):
1. **Strict Normalization (CRITICAL):** The "service" field MUST match exactly with an element from the VALID VOCABULARY LISTS.
2. **Numeric Identifiers:** The "id" field of each node MUST be strictly a sequential integer in string format (e.g., "0", "1", "2").
3. **Audio-Driven Expansion (CRITICAL OVERRIDE):** If the visual World Model shows a generic abstraction (e.g., a single "AWS" cloud icon, or "On-Prem"), but the audio transcript explicitly lists specific services belonging to that group (e.g., S3, SNS, SQS, CloudTrail, GuardDuty), you MUST expand the generic visual node into separate, individual nodes for each explicitly mentioned service. DO NOT create the generic parent node; only create its specific children and route them to their logical destination.
4. **Dynamic Logical Fusion:** Evaluate multiple icons of the same service dynamically. If they act as a single logical unit, FUSE them. If they perform distinct architectural steps at different stages, KEEP THEM SEPARATE.
5. **Pruning:** Remove generic human actors or purely physical concepts. Keep system entry points.
6. **Note Assimilation:** Extract specific constraints and metrics from the transcript and inject them into the "notes".

## EDGE AND FLOW RULES (LOGICAL ROUTING):
1. **Strict Flow Segmentation (`flow_id`):** Group related architectural actions into distinct logical workflows using an integer `flow_id` (starting at 0).
2. **Chronological Sequence (`seq`):** Order events within a flow using string integers ("0", "1"). Use the prime character for parallel actions (e.g., "1" and "1'"). Model bidirectionality as two edges.
3. **Edge Types (`type`):** Use "data" for payload transfers/reads/writes. Use "control" for events, triggers, or asynchronous invocations.
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

def call_gemini_api(full_prompt, mime, image_b64, model_name, response_schema=None):
    client = get_gemini_client()
    max_retries = 30
    retry_delay = 20

    if response_schema is not None:
        config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=response_schema)
    else:
        config = types.GenerateContentConfig(response_mime_type="application/json")
    
    for attempt in range(max_retries):
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=[{
                    "parts": [
                        {"text": full_prompt},
                        {"inline_data": {"mime_type": mime, "data": image_b64}}
                    ]
                }],
                config=config,
            )
            return json.loads(res.text)
        except Exception as e:
            err_msg = str(e).upper()
            if attempt < max_retries - 1 and any(k in err_msg for k in ["503", "429", "RESOURCE_EXHAUSTED", "LIMIT"]):
                delay = 35 if ("429" in err_msg or "RESOURCE" in err_msg) else retry_delay
                print(f"  ⏳ Límite de cuota / Servidor ocupado en modelo estricto '{model_name}'. Esperando {delay}s antes de reintentar en '{model_name}' (intento {attempt+1}/{max_retries})...")
                time.sleep(delay)
                retry_delay = min(retry_delay * 2, 60)
            else:
                print(f"  ❌ Error fatal en modelo estricto '{model_name}': {e}")
                raise e

def run_dynamic_few_shot_experiment(video_ids=ALL_14_VIDEOS, force=FORCE_RERUN):
    print("=" * 80)
    print(f"🚀 INICIANDO EXPERIMENTO: '{EXPERIMENT_LABEL}' (Dynamic Few-Shot RAG)")
    print(f"   • Modelo: {MODEL_NAME}")
    print(f"   • Total Videos: {len(video_ids)}")
    print(f"   • Rule: Dynamic Jaccard Matcher + Target Video Exclusion")
    print("=" * 80)

    # 1. Load Ground Truth database for RAG matching
    print("\n🔍 Cargando base de datos de 165 Ground Truths...")
    gt_db = load_all_ground_truths(GT_DIR)
    print(f"✅ Cargados {len(gt_db)} grafos Ground Truth para recuperación RAG.\n")

    results = []

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
        wm_base = workspace / "world_model.json"
        an_path = workspace / f"test_analysis{suffix}.json"
        gml_path = workspace / f"test_graph{suffix}.graphml"
        eval_path = workspace / f"evaluation{suffix}.json"

        # Stage 1: Load or Generate World Model
        if wm_base.exists() and not force:
            with open(wm_base, "r", encoding="utf-8") as f:
                world_model = json.load(f)
        else:
            p1 = STAGE1_V0_BASELINE.replace("<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR).replace("<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR)
            parts1 = [p1, f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={video_id}"]
            if transcript_text: parts1.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")
            world_model = call_gemini_api("\n".join(parts1), "image/jpeg", img_b64, MODEL_NAME, response_schema=WorldModelSchema)
            with open(wm_base, "w", encoding="utf-8") as f:
                json.dump(world_model, f, indent=2, ensure_ascii=False)

        # Stage 2: Dynamic Few-Shot RAG Retrieval
        target_services = extract_services_from_world_model(world_model)
        matches = find_similar_ground_truths(video_id, target_services, gt_db, top_k=2)
        few_shot_str = format_few_shot_prompt(matches)

        match_vids = [m["video_id"] for m in matches]
        print(f"  🎯 RAG Matcher (Excluyendo '{video_id}'): Ejemplos seleccionados -> {match_vids}")

        # Stage 2 Execution
        if an_path.exists() and not force:
            print(f"  ✓ Cargando análisis local en caché ({an_path.name})...")
            with open(an_path, "r", encoding="utf-8") as f:
                analysis_res = json.load(f)
        else:
            print(f"  🤖 Ejecutando Gemini API (Stage 2) con Dynamic Few-Shot Prompt...")
            p2 = STAGE2_V4_DYNAMIC_FEW_SHOT.replace("<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False)) \
                                           .replace("<FEW_SHOT_PLACEHOLDER>", few_shot_str) \
                                           .replace("<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR) \
                                           .replace("<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR)
            parts2 = [p2, f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={video_id}"]
            if transcript_text: parts2.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")
            analysis_res = call_gemini_api("\n".join(parts2), "image/jpeg", img_b64, MODEL_NAME, response_schema=FinalArchitectureSchema)
            with open(an_path, "w", encoding="utf-8") as f:
                json.dump(analysis_res, f, indent=2, ensure_ascii=False)

        # Build Graph and Evaluate
        G = create_graph_from_cloudscape_json(analysis_res, video_id=video_id)
        nx.write_graphml(G, str(gml_path))

        gt_path = GT_DIR / f"{video_id}.graphml"
        eval_res = {}
        if gt_path.exists():
            gt_g = nx.read_graphml(str(gt_path))
            eval_res = evaluate_pair(G, gt_g, video_id, CATALOG_DICT)
            with open(eval_path, "w", encoding="utf-8") as f:
                json.dump(eval_res, f, indent=2, ensure_ascii=False, default=str)

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
            "rag_matches": match_vids,
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
        print(df[["video_id", "svc_f1", "edge_f1", "gen_nodes", "gen_edges", "rag_matches"]].to_string(index=False))

    return results

if __name__ == "__main__":
    run_dynamic_few_shot_experiment()
