#!/usr/bin/env python3
"""
batch_prompt_test.py — Script de prueba batch para el whiteboard_selection_lab.

Permite recibir una lista de video IDs, ejecutar el algoritmo adaptativo de
detección de pizarra sobre el best_whiteboard aprobado, inyectar los resultados
en el prompt de Gemini (Stage 1 + Stage 2), generar grafos, y evaluar contra
Ground Truth.

Todos los resultados se guardan localmente en lab_workspace/{VIDEO_ID}/ siguiendo
la estructura del lab (nunca escribe en data/graphs/).

Usage:
    # Procesar videos específicos
    python batch_prompt_test.py VIDEO_ID1 VIDEO_ID2 VIDEO_ID3

    # Procesar todos los videos de cloudscape_reports
    python batch_prompt_test.py --from-reports

    # Procesar una lista de un archivo de texto (un ID por línea)
    python batch_prompt_test.py --from-file video_ids.txt

    # Forzar re-ejecución (ignorar cache)
    python batch_prompt_test.py --force VIDEO_ID1 VIDEO_ID2

    # Usar un label de experimento para versionado
    python batch_prompt_test.py --experiment-label "v2_delta40" VIDEO_ID1
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import shutil
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

import cv2
import networkx as nx
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table

# ── Project paths ────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = Path(__file__).resolve().parent

sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(LAB_DIR / "algorithms"))

from config.settings import GEMINI_API_KEY, GEMINI_MODEL
from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

from algorithms.adaptive_whiteboard_detector import (
    procesar_y_resaltar_conclusiones_pizarra,
    format_symbols_for_prompt,
)

console = Console()

# ── Paths ────────────────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
GOOD_WHITEBOARD_DIR = DATA_DIR / "good_whiteboard"
GT_DIR = DATA_DIR / "cloudscape_gt"
SERVICES_CSV = DATA_DIR / "services.csv"
if not SERVICES_CSV.exists():
    SERVICES_CSV = DATA_DIR / "cloudscape_gt" / "services.csv"
REPORTS_DIR = PROJECT_ROOT / "cloudscape_reports"
LAB_WORKSPACE = LAB_DIR / "lab_workspace"
TRANSCRIPTIONS_DIR = LAB_DIR / "transcriptions"


# ── Services Catalog ─────────────────────────────────────────────
def load_services_list() -> tuple[str, str]:
    """Load AWS services and user actors from services.csv for prompt injection."""
    csv_path = SERVICES_CSV
    if not csv_path.exists():
        csv_path = PROJECT_ROOT / "graph_renderer" / "services.csv"
    if not csv_path.exists():
        return "", ""

    aws_services = set()
    user_actors = set()
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                capability = row.get("capability", "").strip().lower()
                if not name:
                    continue
                if capability == "user" or name.startswith("User"):
                    user_actors.add(name)
                else:
                    aws_services.add(name)
    except Exception as e:
        console.print(f"[yellow]⚠ Failed to load services catalog: {e}[/]")
    return ", ".join(sorted(aws_services)), ", ".join(sorted(user_actors))


AWS_SERVICES_STR, USER_ACTORS_STR = load_services_list()


# ══════════════════════════════════════════════════════════════════
# PROMPTS (Identical to vision_analyzer.py — self-contained for lab)
# ══════════════════════════════════════════════════════════════════

MFR_STAGE_1_PROMPT_TEMPLATE = """You are an expert in visual extraction of cloud architectures. Your task is to analyze the provided whiteboard diagram and audio transcript to build a structured "World Model" representing the components and their visual groupings.

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

MFR_STAGE_2_PROMPT_TEMPLATE = """
You are an expert AWS Solutions Architect. Your task is to compile the final logical cloud architecture graph from the provided World Model and audio transcript.

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


# ── Pydantic Schemas (for structured output) ─────────────────────
try:
    from pydantic import BaseModel

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

    HAS_PYDANTIC = True
except ImportError:
    HAS_PYDANTIC = False
    WorldModelSchema = None
    FinalArchitectureSchema = None


# ── Gemini Client ────────────────────────────────────────────────
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set. Add it to your .env file.")
        _client = genai.Client(api_key=GEMINI_API_KEY)
        console.print(f"[green]✓[/] Gemini client initialized (model: {GEMINI_MODEL})")
    return _client


def _call_gemini_with_retry(client, full_prompt, mime, image_b64, response_schema=None):
    """Call Gemini with retry logic for transient API errors using Pydantic structured output."""
    from google.genai import types
    max_retries = 5
    retry_delay = 10
    response = None

    if response_schema is not None:
        config = types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
            response_schema=response_schema,
        )
    else:
        config = types.GenerateContentConfig(
            temperature=0.0,
            response_mime_type="application/json",
        )

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[
                    {
                        "parts": [
                            {"text": full_prompt},
                            {
                                "inline_data": {
                                    "mime_type": mime,
                                    "data": image_b64,
                                }
                            },
                        ]
                    }
                ],
                config=config,
            )
            return response
        except Exception as e:
            err_msg = str(e)
            err_upper = err_msg.upper()
            is_transient = any(k in err_upper for k in ["503", "429", "UNAVAILABLE", "LIMIT", "QUOTA", "RESOURCE_EXHAUSTED", "DEMAND"])
            if attempt < max_retries - 1 and is_transient:
                delay = 35 if ("429" in err_upper or "RESOURCE_EXHAUSTED" in err_upper or "QUOTA" in err_upper) else retry_delay
                console.print(f"  [yellow]⚠ Gemini API error: {err_msg[:120]}... Retrying in {delay}s ({attempt+1}/{max_retries})[/]")
                time.sleep(delay)
                retry_delay *= 2
            else:
                raise e


# ══════════════════════════════════════════════════════════════════
# CORE: Analyze a single video
# ══════════════════════════════════════════════════════════════════

def process_single_video(
    video_id: str,
    force: bool = False,
    experiment_label: str = "",
) -> dict[str, Any]:
    """
    Process a single video through the full lab pipeline:
    1. Locate best_whiteboard from good_whiteboard/
    2. Copy transcript to lab transcriptions/
    3. Run adaptive whiteboard detection
    4. Inject symbol positions into prompt1
    5. Call Gemini Stage 1 (World Model) + Stage 2 (Final Graph)
    6. Build GraphML and evaluate against Ground Truth

    All outputs go to lab_workspace/{video_id}/ following the lab structure.
    """
    console.rule(f"[bold cyan]Processing {video_id}")

    workspace = LAB_WORKSPACE / video_id
    workspace.mkdir(parents=True, exist_ok=True)

    # ── 1. Locate whiteboard image ───────────────────────────────
    whiteboard_path = GOOD_WHITEBOARD_DIR / f"{video_id}.jpg"
    if not whiteboard_path.exists():
        console.print(f"  [red]✗ No approved whiteboard found at {whiteboard_path}[/]")
        return {"video_id": video_id, "status": "error", "error": "No whiteboard in good_whiteboard/"}

    # Copy to workspace
    local_wb = workspace / "best_whiteboard.jpg"
    if not local_wb.exists() or force:
        shutil.copy2(whiteboard_path, local_wb)
    console.print(f"  [green]✓[/] Whiteboard: {local_wb.name}")

    # ── 2. Locate and copy transcript ────────────────────────────
    transcript_text = ""
    transcript_src = RAW_DIR / f"{video_id}_transcript.json"
    transcript_lab = TRANSCRIPTIONS_DIR / f"{video_id}_transcript.json"

    if transcript_src.exists():
        if not transcript_lab.exists() or force:
            TRANSCRIPTIONS_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(transcript_src, transcript_lab)
        with open(transcript_lab, "r", encoding="utf-8") as f:
            segments = json.load(f)
        if isinstance(segments, list):
            transcript_text = " ".join(s.get("text", "").strip() for s in segments)
        elif isinstance(segments, dict) and "text" in segments:
            transcript_text = segments["text"]
        console.print(f"  [green]✓[/] Transcript: {len(transcript_text)} chars")
    elif transcript_lab.exists():
        with open(transcript_lab, "r", encoding="utf-8") as f:
            segments = json.load(f)
        if isinstance(segments, list):
            transcript_text = " ".join(s.get("text", "").strip() for s in segments)
        elif isinstance(segments, dict) and "text" in segments:
            transcript_text = segments["text"]
        console.print(f"  [green]✓[/] Transcript (lab cache): {len(transcript_text)} chars")
    else:
        console.print(f"  [yellow]⚠ No transcript found for {video_id}[/]")

    # ── 3. Run adaptive whiteboard detection ─────────────────────
    console.print(f"  [dim]→ Running adaptive whiteboard detection...[/]")
    try:
        symbols_list, processed_img_path = procesar_y_resaltar_conclusiones_pizarra(
            local_wb, workspace, delta_contraste_min=40.0
        )
    except Exception as e:
        console.print(f"  [yellow]⚠ Adaptive detection failed: {e}[/]")
        symbols_list = []
        processed_img_path = None

    symbols_prompt_section = format_symbols_for_prompt(symbols_list)

    # ── 4. Check cache for world_model and test_analysis ─────────
    suffix = f"_{experiment_label}" if experiment_label else ""
    world_model_path = workspace / f"world_model{suffix}.json"
    analysis_path = workspace / f"test_analysis{suffix}.json"
    graphml_path = workspace / f"test_graph{suffix}.graphml"

    # ── 5. Stage 1: World Model ──────────────────────────────────
    if world_model_path.exists() and not force:
        console.print(f"  [yellow]⚠ World model cache found: {world_model_path.name}. Skipping Stage 1.[/]")
        with open(world_model_path, "r", encoding="utf-8") as f:
            world_model = json.load(f)
    else:
        client = _get_client()

        # Read and encode image
        image_bytes = local_wb.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        suffix_ext = local_wb.suffix.lower()
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(
            suffix_ext.lstrip("."), "image/jpeg"
        )

        # Build prompt 1 with symbol injection
        formatted_prompt_1 = MFR_STAGE_1_PROMPT_TEMPLATE.replace(
            "<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR
        ).replace(
            "<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR
        )

        prompt_parts_1 = [formatted_prompt_1]

        # Inject adaptive detection results into prompt1
        if symbols_prompt_section:
            prompt_parts_1.append(symbols_prompt_section)

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        prompt_parts_1.append(f"\n## VIDEO URL:\n{video_url}")
        if transcript_text:
            prompt_parts_1.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")

        full_prompt_1 = "\n".join(prompt_parts_1)

        console.print(f"  [dim]→ [Stage 1] Building World Model with Gemini ({GEMINI_MODEL})...[/]")
        response_1 = _call_gemini_with_retry(
            client, full_prompt_1, mime, image_b64,
            response_schema=WorldModelSchema if HAS_PYDANTIC else None,
        )

        world_model = json.loads(response_1.text)
        with open(world_model_path, "w", encoding="utf-8") as f:
            json.dump(world_model, f, indent=2, ensure_ascii=False)
        console.print(f"  [green]✓[/] World Model: {len(world_model.get('entities', []))} entities, {len(world_model.get('visual_connections', []))} connections → {world_model_path.name}")

    # ── 6. Stage 2: Final Architecture Graph ─────────────────────
    if analysis_path.exists() and not force:
        console.print(f"  [yellow]⚠ Analysis cache found: {analysis_path.name}. Skipping Stage 2.[/]")
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis_result = json.load(f)
    else:
        client = _get_client()

        image_bytes = local_wb.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        suffix_ext = local_wb.suffix.lower()
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(
            suffix_ext.lstrip("."), "image/jpeg"
        )

        formatted_prompt_2 = MFR_STAGE_2_PROMPT_TEMPLATE.replace(
            "<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False)
        ).replace(
            "<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR
        ).replace(
            "<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR
        )

        prompt_parts_2 = [formatted_prompt_2]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        prompt_parts_2.append(f"\n## VIDEO URL:\n{video_url}")
        if transcript_text:
            prompt_parts_2.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")

        full_prompt_2 = "\n".join(prompt_parts_2)

        console.print(f"  [dim]→ [Stage 2] Compiling final architecture with Gemini ({GEMINI_MODEL})...[/]")
        response_2 = _call_gemini_with_retry(
            client, full_prompt_2, mime, image_b64,
            response_schema=FinalArchitectureSchema if HAS_PYDANTIC else None,
        )

        analysis_result = json.loads(response_2.text)
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)
        console.print(f"  [green]✓[/] Analysis: {len(analysis_result.get('nodes', []))} nodes, {len(analysis_result.get('edges', []))} edges → {analysis_path.name}")

    # ── 7. Build GraphML ─────────────────────────────────────────
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    G = create_graph_from_cloudscape_json(analysis_result, video_id=video_id, video_url=video_url)
    nx.write_graphml(G, str(graphml_path))
    console.print(f"  [green]✓[/] GraphML: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges → {graphml_path.name}")

    # ── 8. Evaluate against Ground Truth ─────────────────────────
    gt_path = GT_DIR / f"{video_id}.graphml"
    eval_result = None

    if gt_path.exists():
        try:
            gt_graph = nx.read_graphml(str(gt_path))
            catalog = load_services_catalog(SERVICES_CSV)
            eval_result = evaluate_pair(G, gt_graph, video_id, catalog)

            # Check GT usability
            usable = gt_graph.graph.get("graph_usable", True)
            eval_result["graph_usable"] = usable is not False and str(usable).lower() != "false"

            svc_f1 = eval_result["svc_f1"]
            edge_f1 = eval_result["edge_f1"]
            missing = eval_result["services_missing"]
            halluc = eval_result["services_hallucinated"]

            emoji = "🟢" if svc_f1 >= 0.9 else "🟡" if svc_f1 >= 0.7 else "🟠" if svc_f1 >= 0.5 else "🔴"
            console.print(f"  {emoji} Evaluation: Svc F1={svc_f1:.0%}, Edge F1={edge_f1:.0%}")
            if missing:
                console.print(f"     Missing: {', '.join(missing)}")
            if halluc:
                console.print(f"     Hallucinated: {', '.join(halluc)}")

            # Save evaluation
            eval_path = workspace / f"evaluation{suffix}.json"
            with open(eval_path, "w", encoding="utf-8") as f:
                json.dump(eval_result, f, indent=2, ensure_ascii=False, default=str)

        except Exception as e:
            console.print(f"  [yellow]⚠ Evaluation failed: {e}[/]")
    else:
        console.print(f"  [dim]No Ground Truth found for {video_id}[/]")

    return {
        "video_id": video_id,
        "status": "success",
        "symbols_detected": len(symbols_list),
        "gen_nodes": G.number_of_nodes(),
        "gen_edges": G.number_of_edges(),
        "svc_f1": eval_result["svc_f1"] if eval_result else None,
        "edge_f1": eval_result["edge_f1"] if eval_result else None,
        "services_missing": eval_result["services_missing"] if eval_result else [],
        "services_hallucinated": eval_result["services_hallucinated"] if eval_result else [],
        "workspace": str(workspace),
    }


# ══════════════════════════════════════════════════════════════════
# BATCH PROCESSING
# ══════════════════════════════════════════════════════════════════

def get_video_ids_from_reports() -> list[str]:
    """Get video IDs from cloudscape_reports directory."""
    if not REPORTS_DIR.exists():
        console.print(f"[yellow]⚠ cloudscape_reports/ not found[/]")
        return []
    return sorted([
        d.name for d in REPORTS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    ])


def run_batch(
    video_ids: list[str],
    force: bool = False,
    experiment_label: str = "",
) -> list[dict[str, Any]]:
    """Process a batch of videos and generate a summary report."""

    console.print(Panel.fit(
        f"[bold white]🧪 Batch Prompt Test — Whiteboard Selection Lab[/]\n"
        f"[dim]Videos: {len(video_ids)} | Model: {GEMINI_MODEL} | Force: {force}[/]\n"
        f"[dim]Experiment: {experiment_label or '(default)'}[/]",
        border_style="cyan",
    ))

    results = []
    for i, vid in enumerate(video_ids, 1):
        console.print(f"\n[bold cyan][{i}/{len(video_ids)}][/]")
        try:
            res = process_single_video(vid, force=force, experiment_label=experiment_label)
            results.append(res)
        except Exception as e:
            console.print(f"  [bold red]✗ Error: {e}[/]")
            import traceback
            traceback.print_exc()
            results.append({
                "video_id": vid,
                "status": "error",
                "error": str(e),
            })

    # ── Summary Table ────────────────────────────────────────────
    console.print()
    table = Table(
        title=f"Batch Results Summary ({experiment_label or 'default'})",
        border_style="cyan",
        show_lines=True,
    )
    table.add_column("#", style="bold", width=3)
    table.add_column("Video ID", style="bold")
    table.add_column("Status")
    table.add_column("Symbols", style="magenta", justify="right")
    table.add_column("Nodes", style="green", justify="right")
    table.add_column("Edges", style="green", justify="right")
    table.add_column("Svc F1", style="cyan", justify="right")
    table.add_column("Edge F1", style="cyan", justify="right")
    table.add_column("Missing", style="yellow")
    table.add_column("Hallucinated", style="red")

    for idx, r in enumerate(results, 1):
        if r["status"] == "error":
            table.add_row(
                str(idx), r["video_id"],
                "[red]Error[/]",
                "—", "—", "—", "—", "—",
                r.get("error", "")[:30], ""
            )
            continue

        svc_f1_str = f"{r['svc_f1']:.0%}" if r.get("svc_f1") is not None else "—"
        edge_f1_str = f"{r['edge_f1']:.0%}" if r.get("edge_f1") is not None else "—"
        missing_str = ", ".join(r.get("services_missing", [])[:3])
        if len(r.get("services_missing", [])) > 3:
            missing_str += f" (+{len(r['services_missing'])-3})"
        halluc_str = ", ".join(r.get("services_hallucinated", [])[:3])
        if len(r.get("services_hallucinated", [])) > 3:
            halluc_str += f" (+{len(r['services_hallucinated'])-3})"

        table.add_row(
            str(idx), r["video_id"],
            "[green]OK[/]",
            str(r.get("symbols_detected", 0)),
            str(r.get("gen_nodes", 0)),
            str(r.get("gen_edges", 0)),
            svc_f1_str,
            edge_f1_str,
            missing_str or "—",
            halluc_str or "—",
        )

    console.print(table)

    # ── Aggregate metrics ────────────────────────────────────────
    evaluated = [r for r in results if r.get("svc_f1") is not None]
    if evaluated:
        avg_svc_f1 = sum(r["svc_f1"] for r in evaluated) / len(evaluated)
        avg_edge_f1 = sum(r["edge_f1"] for r in evaluated) / len(evaluated)
        console.print(f"\n[bold]📊 Aggregate ({len(evaluated)} videos with GT):[/]")
        console.print(f"   Avg Service F1: [bold cyan]{avg_svc_f1:.1%}[/]")
        console.print(f"   Avg Edge F1:    [bold cyan]{avg_edge_f1:.1%}[/]")

    # ── Save batch summary ───────────────────────────────────────
    suffix = f"_{experiment_label}" if experiment_label else ""
    summary_path = LAB_DIR / f"batch_results{suffix}.json"
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "experiment_label": experiment_label,
        "gemini_model": GEMINI_MODEL,
        "total_videos": len(video_ids),
        "successful": len([r for r in results if r["status"] == "success"]),
        "errors": len([r for r in results if r["status"] == "error"]),
        "avg_svc_f1": avg_svc_f1 if evaluated else None,
        "avg_edge_f1": avg_edge_f1 if evaluated else None,
        "results": results,
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False, default=str)
    console.print(f"\n[green]✓[/] Batch summary saved → {summary_path}")

    return results


# ══════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch prompt test runner for whiteboard_selection_lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process specific videos
  python batch_prompt_test.py 6CgqEzyWpeA 1aYoIZvabbk

  # Process all cloudscape_reports videos
  python batch_prompt_test.py --from-reports

  # Process video IDs from a text file
  python batch_prompt_test.py --from-file my_batch.txt

  # Force re-run (ignore cache) with experiment label
  python batch_prompt_test.py --force --experiment-label "v2_symbols" 6CgqEzyWpeA
        """,
    )
    parser.add_argument(
        "video_ids", nargs="*", default=[],
        help="Video IDs to process",
    )
    parser.add_argument(
        "--from-reports", action="store_true",
        help="Process all videos from cloudscape_reports/",
    )
    parser.add_argument(
        "--from-file", type=Path, default=None,
        help="Read video IDs from a text file (one ID per line)",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Force re-execution, ignore cached results",
    )
    parser.add_argument(
        "--experiment-label", default="",
        help="Label for this experiment run (used for file naming)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    video_ids = list(args.video_ids)

    if args.from_reports:
        report_ids = get_video_ids_from_reports()
        console.print(f"[cyan]📂 Found {len(report_ids)} videos in cloudscape_reports/[/]")
        video_ids.extend(report_ids)

    if args.from_file and args.from_file.exists():
        with open(args.from_file, "r") as f:
            file_ids = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        console.print(f"[cyan]📄 Read {len(file_ids)} video IDs from {args.from_file}[/]")
        video_ids.extend(file_ids)

    # Deduplicate preserving order
    seen = set()
    unique_ids = []
    for vid in video_ids:
        if vid not in seen:
            seen.add(vid)
            unique_ids.append(vid)
    video_ids = unique_ids

    if not video_ids:
        console.print("[bold red]✗ No video IDs provided. Use positional args, --from-reports, or --from-file.[/]")
        sys.exit(1)

    try:
        run_batch(
            video_ids,
            force=args.force,
            experiment_label=args.experiment_label,
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user.[/]")
        sys.exit(130)
