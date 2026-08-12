#!/usr/bin/env python3
"""
run_image_routing_experiment.py — Experimento de enrutamiento de imágenes (Limpia vs Resaltada)
para el laboratorio whiteboard_selection_lab.

Compara 3 estrategias de paso de imágenes en el pipeline de 2 etapas (Stage 1 Modeler, Stage 2 Planner):
  1. 'baseline_clean': Limpia en Stage 1, Limpia en Stage 2.
  2. 'user_proposal': Resaltada (conexiones/cajas) en Stage 1, Limpia en Stage 2.
  3. 'dual_stage1': [Limpia + Resaltada] en Stage 1, Limpia en Stage 2.

Usa los 14 videos benchmark estándar con Ground Truth para evaluar Service F1 y Edge F1.
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import networkx as nx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(LAB_DIR / "algorithms"))

from config.settings import GEMINI_API_KEY, GEMINI_API_KEYS, GEMINI_MODEL
from scripts.core.graph_builder import create_graph_from_cloudscape_json
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

from batch_prompt_test import (
    MFR_STAGE_1_PROMPT_TEMPLATE,
    MFR_STAGE_2_PROMPT_TEMPLATE,
    AWS_SERVICES_STR,
    USER_ACTORS_STR,
    WorldModelSchema,
    FinalArchitectureSchema,
    HAS_PYDANTIC,
    GOOD_WHITEBOARD_DIR,
    RAW_DIR,
    GT_DIR,
    SERVICES_CSV,
    LAB_WORKSPACE,
    TRANSCRIPTIONS_DIR,
)

from algorithms.adaptive_whiteboard_detector import (
    procesar_y_resaltar_conclusiones_pizarra,
    format_symbols_for_prompt,
)

console = Console()

# ── Gemini Client Management with Key Rotation ──────────────────
_client = None
_current_key_idx: int = 0


def _get_client():
    global _client, _current_key_idx
    if _client is None:
        from google import genai
        keys = GEMINI_API_KEYS if GEMINI_API_KEYS else ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
        if not keys:
            raise ValueError("GEMINI_API_KEY not set. Add it to your .env file.")
        _current_key_idx = _current_key_idx % len(keys)
        active_key = keys[_current_key_idx]
        _client = genai.Client(api_key=active_key)
        masked_key = active_key[:8] + "..." + active_key[-4:] if len(active_key) > 12 else "active_key"
        console.print(f"[green]✓[/] Gemini client initialized (Key {_current_key_idx + 1}/{len(keys)}: {masked_key})")
    return _client


def _rotate_client():
    global _client, _current_key_idx
    from google import genai
    keys = GEMINI_API_KEYS if GEMINI_API_KEYS else ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    if len(keys) > 1:
        _current_key_idx = (_current_key_idx + 1) % len(keys)
        active_key = keys[_current_key_idx]
        _client = genai.Client(api_key=active_key)
        masked_key = active_key[:8] + "..." + active_key[-4:] if len(active_key) > 12 else "rotated_key"
        console.print(f"[bold yellow]🔄 Rotated Gemini API Key → Key {_current_key_idx + 1}/{len(keys)} ({masked_key})[/]")
    return _get_client()


# 14 Benchmark Videos
BENCHMARK_VIDEOS = [
    "-3lnf5lzsH0",
    "-kA0ahrhX3I",
    "-wLEkq21cvA",
    "07lfvavMdfU",
    "1aYoIZvabbk",
    "2L0m28ZLmtE",
    "2e3vOxsHekE",
    "6CgqEzyWpeA",
    "6EUknQqaV1w",
    "6YkguepAQuQ",
    "BZ32w0SSAoY",
    "Cgv0kfp_6xQ",
    "wjtSHyENv0I",
    "ww5fiygF6eg",
]


def _call_gemini_multi_image(client, full_prompt: str, images: list[Path], response_schema=None):
    """Llama a Gemini permitiendo enviar una o múltiples imágenes en la lista de contenidos, rotando API keys automáticamente en caso de cuota/límite."""
    from google.genai import types

    parts = [{"text": full_prompt}]
    for img_path in images:
        img_bytes = img_path.read_bytes()
        img_b64 = base64.b64encode(img_bytes).decode("utf-8")
        suffix_ext = img_path.suffix.lower()
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(
            suffix_ext.lstrip("."), "image/jpeg"
        )
        parts.append({
            "inline_data": {
                "mime_type": mime,
                "data": img_b64,
            }
        })

    config = types.GenerateContentConfig(
        temperature=0.0,
        response_mime_type="application/json",
        response_schema=response_schema if HAS_PYDANTIC else None,
    )

    max_retries = 10
    retry_delay = 5
    for attempt in range(max_retries):
        try:
            active_client = client or _get_client()
            response = active_client.models.generate_content(
                model=GEMINI_MODEL,
                contents=[{"parts": parts}],
                config=config,
            )
            return response
        except Exception as e:
            err_msg = str(e)
            err_upper = err_msg.upper()
            is_transient = any(k in err_upper for k in ["503", "429", "UNAVAILABLE", "LIMIT", "QUOTA", "RESOURCE_EXHAUSTED", "DEMAND"])
            if attempt < max_retries - 1 and is_transient:
                keys_count = len(GEMINI_API_KEYS) if GEMINI_API_KEYS else 1
                if keys_count > 1:
                    console.print(f"  [yellow]⚠ Gemini API Límite/Cuota ({err_msg[:80]}...). Rotando a la siguiente clave API...[/]")
                    client = _rotate_client()
                    time.sleep(2)
                else:
                    delay = 35 if ("429" in err_upper or "QUOTA" in err_upper or "RESOURCE_EXHAUSTED" in err_upper) else retry_delay
                    console.print(f"  [yellow]⚠ Gemini API Error: {err_msg[:100]}... Reintentando en {delay}s ({attempt+1}/{max_retries})[/]")
                    time.sleep(delay)
                    retry_delay *= 2
            else:
                raise e


def process_video_image_routing(
    video_id: str,
    routing_mode: str = "user_proposal",
    force: bool = False,
) -> dict[str, Any]:
    """
    routing_mode options:
      - 'baseline_clean': Clean img in Stage 1, Clean img in Stage 2
      - 'user_proposal': Highlighted img in Stage 1, Clean img in Stage 2
      - 'dual_stage1': [Clean + Highlighted] imgs in Stage 1, Clean img in Stage 2
    """
    workspace = LAB_WORKSPACE / video_id
    workspace.mkdir(parents=True, exist_ok=True)

    whiteboard_path = GOOD_WHITEBOARD_DIR / f"{video_id}.jpg"
    if not whiteboard_path.exists():
        return {"video_id": video_id, "status": "error", "error": "No whiteboard found"}

    local_clean_wb = workspace / "best_whiteboard.jpg"
    if not local_clean_wb.exists() or force:
        shutil.copy2(whiteboard_path, local_clean_wb)

    # Transcript
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

    # Detection & Highlighted Image
    try:
        symbols_list, processed_img_path = procesar_y_resaltar_conclusiones_pizarra(
            local_clean_wb, workspace, delta_contraste_min=40.0
        )
    except Exception as e:
        symbols_list = []
        processed_img_path = local_clean_wb

    symbols_prompt_section = format_symbols_for_prompt(symbols_list)

    exp_label = f"img_mode_{routing_mode}"
    world_model_path = workspace / f"world_model_{exp_label}.json"
    analysis_path = workspace / f"test_analysis_{exp_label}.json"
    graphml_path = workspace / f"test_graph_{exp_label}.graphml"

    client = _get_client()

    # ── STAGE 1: Modeler ──
    if world_model_path.exists() and not force:
        with open(world_model_path, "r", encoding="utf-8") as f:
            world_model = json.load(f)
    else:
        formatted_prompt_1 = MFR_STAGE_1_PROMPT_TEMPLATE.replace(
            "<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR
        ).replace(
            "<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR
        )
        prompt_parts_1 = [formatted_prompt_1]
        if symbols_prompt_section:
            prompt_parts_1.append(symbols_prompt_section)
        prompt_parts_1.append(f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={video_id}")
        if transcript_text:
            prompt_parts_1.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")

        full_prompt_1 = "\n".join(prompt_parts_1)

        # Image selection for Stage 1
        if routing_mode == "user_proposal":
            stage1_images = [processed_img_path if processed_img_path and processed_img_path.exists() else local_clean_wb]
        elif routing_mode == "dual_stage1":
            stage1_images = [local_clean_wb]
            if processed_img_path and processed_img_path.exists():
                stage1_images.append(processed_img_path)
        else: # baseline_clean
            stage1_images = [local_clean_wb]

        res1 = _call_gemini_multi_image(client, full_prompt_1, stage1_images, response_schema=WorldModelSchema)
        world_model = json.loads(res1.text)
        with open(world_model_path, "w", encoding="utf-8") as f:
            json.dump(world_model, f, indent=2, ensure_ascii=False)

    # ── STAGE 2: Planner (SIEMPRE IMAGEN LIMPIA) ──
    if analysis_path.exists() and not force:
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis_result = json.load(f)
    else:
        formatted_prompt_2 = MFR_STAGE_2_PROMPT_TEMPLATE.replace(
            "<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False)
        ).replace(
            "<AWS_SERVICES_PLACEHOLDER>", AWS_SERVICES_STR
        ).replace(
            "<USER_ACTORS_PLACEHOLDER>", USER_ACTORS_STR
        )
        prompt_parts_2 = [formatted_prompt_2]
        prompt_parts_2.append(f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={video_id}")
        if transcript_text:
            prompt_parts_2.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")

        full_prompt_2 = "\n".join(prompt_parts_2)

        # Stage 2 usa SIEMPRE la imagen limpia local_clean_wb para evitar oclusión de texto
        stage2_images = [local_clean_wb]

        res2 = _call_gemini_multi_image(client, full_prompt_2, stage2_images, response_schema=FinalArchitectureSchema)
        analysis_result = json.loads(res2.text)
        with open(analysis_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=2, ensure_ascii=False)

    # GraphML
    url = f"https://www.youtube.com/watch?v={video_id}"
    G = create_graph_from_cloudscape_json(analysis_result, video_id=video_id, video_url=url)
    nx.write_graphml(G, str(graphml_path))

    # Evaluate
    gt_path = GT_DIR / f"{video_id}.graphml"
    eval_res = None
    if gt_path.exists():
        gt_graph = nx.read_graphml(str(gt_path))
        catalog = load_services_catalog(SERVICES_CSV)
        eval_res = evaluate_pair(G, gt_graph, video_id, catalog)

    return {
        "video_id": video_id,
        "status": "success",
        "routing_mode": routing_mode,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "svc_f1": eval_res["svc_f1"] if eval_res else None,
        "edge_f1": eval_res["edge_f1"] if eval_res else None,
        "missing": eval_res["services_missing"] if eval_res else [],
        "hallucinated": eval_res["services_hallucinated"] if eval_res else [],
    }


def main():
    parser = argparse.ArgumentParser(description="Image Routing Experiment Runner")
    parser.add_argument(
        "--mode",
        choices=["baseline_clean", "user_proposal", "dual_stage1", "all"],
        default="user_proposal",
        help="Image routing mode to evaluate",
    )
    parser.add_argument("--force", action="store_true", help="Force re-execution")
    parser.add_argument("--videos", nargs="*", default=BENCHMARK_VIDEOS, help="Video IDs to test")
    args = parser.parse_args()

    modes_to_test = [args.mode] if args.mode != "all" else ["baseline_clean", "user_proposal", "dual_stage1"]

    for m in modes_to_test:
        console.print(Panel.fit(
            f"[bold cyan]🧪 Testing Image Routing Strategy: '{m}'[/]\n"
            f"Videos count: {len(args.videos)} | Model: {GEMINI_MODEL}",
            border_style="cyan"
        ))

        results = []
        for vid in args.videos:
            console.print(f"[dim]Processing {vid} ({m})...[/]")
            res = process_video_image_routing(vid, routing_mode=m, force=args.force)
            results.append(res)
            if res.get("svc_f1") is not None:
                console.print(f"  ✓ {vid}: Svc F1={res['svc_f1']:.1%}, Edge F1={res['edge_f1']:.1%}")

        valid = [r for r in results if r.get("svc_f1") is not None]
        if valid:
            avg_s = sum(r["svc_f1"] for r in valid) / len(valid)
            avg_e = sum(r["edge_f1"] for r in valid) / len(valid)
            console.print(f"\n[bold green]📊 RESULTS FOR '{m}':[/]")
            console.print(f"   Avg Service F1: [bold cyan]{avg_s:.2%}[/]")
            console.print(f"   Avg Edge F1:    [bold cyan]{avg_e:.2%}[/]")

            out_file = LAB_DIR / f"image_routing_results_{m}.json"
            out_file.write_text(json.dumps({
                "mode": m,
                "avg_svc_f1": avg_s,
                "avg_edge_f1": avg_e,
                "results": results
            }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
