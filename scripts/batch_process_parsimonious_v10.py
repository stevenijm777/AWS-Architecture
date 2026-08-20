#!/usr/bin/env python3
"""
batch_process_parsimonious_v10.py — Batch runner for Parsimonious Mode (Prompt v10 Refinado)
                                    using Gemini API (gemini-3.6-flash, temperature=0.0).

Organizes output into:
  - data/graphs_parsimonious_v10/
  - data/graphs_parsimonious/ (active evaluation folder)
  - data/processed_tracker.json (registers version_10_parsimonious)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel

from config.settings import (
    DATA_DIR,
    GOOD_WHITEBOARD_DIR,
    RAW_DIR,
)
from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml
from scripts.core.tracker import add_to_tracker
from scripts.core.vision_analyzer_parsimonious import analyze_frame

console = Console()
PROGRESS_FILE = DATA_DIR / "batch_parsimonious_v10_progress.json"
PARSIMONIOUS_V10_DIR = DATA_DIR / "graphs_parsimonious_v10"
PARSIMONIOUS_V10_DIR.mkdir(parents=True, exist_ok=True)
PARSIMONIOUS_ACTIVE_DIR = DATA_DIR / "graphs_parsimonious"
PARSIMONIOUS_ACTIVE_DIR.mkdir(parents=True, exist_ok=True)

INTERSECTION_VIDEOS = [
    "9qTEHITVeLE", "9yziTe6lBwk", "A4Lfk1Zz1dE", "AS2JeM2FUzE", "AzM_d7ZvzUE",
    "BgT_bDAejSQ", "bikXzsVihF4", "BlCXEMp_lqY", "BPvr0qWpJlA", "bqZWYmRAka0"
]


def load_progress() -> dict[str, dict]:
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_progress(progress: dict[str, dict]) -> None:
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)
    except Exception as e:
        console.print(f"[yellow]⚠ Failed to save progress checkpoint: {e}[/]")


def get_target_video_ids(force: bool = False, include_intersection: bool = True) -> list[str]:
    gt_dir = DATA_DIR / "cloudscape_gt"
    gt_vids = sorted([f.stem for f in gt_dir.glob("*.graphml")]) if gt_dir.exists() else []

    target_ids = []

    # 1. First add intersection videos if available and requested
    if include_intersection:
        for vid in INTERSECTION_VIDEOS:
            wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
            ts_path = RAW_DIR / f"{vid}_transcript.json"
            if wb_path.exists() and ts_path.exists():
                out_graph = PARSIMONIOUS_V10_DIR / f"{vid}.graphml"
                if not out_graph.exists() or force:
                    target_ids.append(vid)

    # 2. Add remaining missing GT videos
    for vid in gt_vids:
        if vid in target_ids:
            continue
        wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        ts_path = RAW_DIR / f"{vid}_transcript.json"
        out_graph = PARSIMONIOUS_V10_DIR / f"{vid}.graphml"

        if wb_path.exists() and ts_path.exists():
            if not out_graph.exists() or force:
                target_ids.append(vid)

    return target_ids


def process_batch(video_ids: list[str], force: bool = False) -> None:
    progress = load_progress()
    total = len(video_ids)
    console.print(Panel.fit(
        f"[bold cyan]🚀 Starting Parsimonious v10 Batch Processing (Prompt v10 Refinado)[/]\n"
        f"Total videos to process: [bold green]{total}[/]\n"
        f"Target directories: [bold]{PARSIMONIOUS_V10_DIR}/[/] & [bold]{PARSIMONIOUS_ACTIVE_DIR}/[/]",
        border_style="cyan"
    ))

    success_count = 0
    error_count = 0

    for idx, vid in enumerate(video_ids, 1):
        console.rule(f"[bold cyan][{idx}/{total}] Processing Parsimonious v10 Video: {vid}")

        if not force and vid in progress and progress[vid].get("status") == "success":
            out_graph = PARSIMONIOUS_V10_DIR / f"{vid}.graphml"
            if out_graph.exists():
                console.print(f"[green]✓[/] Already completed in checkpoint. Skipping.")
                success_count += 1
                continue

        wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        ts_path = RAW_DIR / f"{vid}_transcript.json"

        try:
            with open(ts_path, "r", encoding="utf-8") as f:
                segments = json.load(f)
            if isinstance(segments, list):
                transcript_text = " ".join(s.get("text", "").strip() for s in segments)
            elif isinstance(segments, dict) and "text" in segments:
                transcript_text = segments["text"]
            else:
                transcript_text = ""
        except Exception as e:
            console.print(f"[red]✗ Failed to read transcript for {vid}: {e}[/]")
            error_count += 1
            progress[vid] = {"status": "error", "error": str(e), "timestamp": time.time()}
            save_progress(progress)
            continue

        url = f"https://www.youtube.com/watch?v={vid}"
        start_t = time.time()

        try:
            analysis_result = analyze_frame(
                wb_path,
                transcript=transcript_text,
                video_url=url,
            )

            # Save vision analysis output cache
            analysis_cache_path = RAW_DIR / f"{vid}_vision_analysis_parsimonious_v10.json"
            analysis_cache_path.write_text(
                json.dumps(analysis_result, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            # Step 2: Build MultiDiGraph & export GraphML
            G = create_graph_from_cloudscape_json(
                analysis_result,
                video_id=vid,
                video_url=url,
            )

            out_graph_path_v10 = export_graphml(G, vid, output_dir=PARSIMONIOUS_V10_DIR)

            add_to_tracker(vid, "version_10_parsimonious")

            elapsed = round(time.time() - start_t, 2)
            node_count = G.number_of_nodes()
            edge_count = G.number_of_edges()

            console.print(
                f"[bold green]✓ [{idx}/{total}] {vid} complete in {elapsed}s[/] → "
                f"[bold]{node_count}[/] nodes, [bold]{edge_count}[/] edges → [cyan]{out_graph_path_v10.name}[/]"
            )

            success_count += 1
            progress[vid] = {
                "status": "success",
                "nodes": node_count,
                "edges": edge_count,
                "elapsed_sec": elapsed,
                "timestamp": time.time(),
            }
            save_progress(progress)

        except Exception as e:
            err_str = str(e)
            console.print(f"[bold red]✗ [{idx}/{total}] Failed processing {vid}: {err_str}[/]")
            error_count += 1
            progress[vid] = {
                "status": "error",
                "error": err_str,
                "timestamp": time.time(),
            }
            save_progress(progress)

            if any(k in err_str.upper() for k in ["429", "RESOURCE_EXHAUSTED", "QUOTA", "UNAVAILABLE", "LIMIT"]):
                console.print(
                    Panel.fit(
                        f"[bold red]🛑 PROCESO DETENIDO: Sin servicio/cuota de Gemini API.[/]\n"
                        f"Detalle del error: {err_str}\n"
                        f"Se probaron las claves API configuradas. Reanuda la ejecución cuando la cuota esté disponible.",
                        border_style="red"
                    )
                )
                sys.exit(1)

        time.sleep(1.0)

    console.print("\n[bold green]🎉 Parsimonious v10 Batch Finished![/]")
    console.print(f"Successful: [bold green]{success_count}[/], Failed: [bold red]{error_count}[/]\n")


def main():
    parser = argparse.ArgumentParser(description="Batch process Parsimonious mode with Prompt v10 Refinado")
    parser.add_argument("--force", action="store_true", help="Force reprocessing even if output graphml already exists")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of videos to process (0 = all)")
    args = parser.parse_args()

    video_ids = get_target_video_ids(force=args.force)
    if not video_ids:
        console.print("[bold yellow]No pending videos to process for Parsimonious v10![/]")
        return

    if args.limit > 0:
        video_ids = video_ids[:args.limit]

    process_batch(video_ids, force=args.force)


if __name__ == "__main__":
    main()
