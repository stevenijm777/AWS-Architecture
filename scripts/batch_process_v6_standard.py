#!/usr/bin/env python3
"""
batch_process_v6_standard.py — Batch process standard mode cloud architecture extraction
                               for all videos that have a parsimonious graph using the
                               v6corrected prompt.
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
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn

from config.settings import (
    DATA_DIR,
    GOOD_WHITEBOARD_DIR,
    GRAPHS_DIR,
    RAW_DIR,
)
from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml
from scripts.core.tracker import add_to_tracker
from scripts.core.vision_analyzer import analyze_frame

console = Console()
PROGRESS_FILE = DATA_DIR / "batch_v6_progress.json"


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


def get_target_video_ids(force: bool = False) -> list[str]:
    parsimonious_dir = DATA_DIR / "graphs_parsimonious"
    if not parsimonious_dir.exists():
        console.print("[red]✗ Directory data/graphs_parsimonious does not exist![/]")
        return []

    video_ids = sorted([f.stem for f in parsimonious_dir.glob("*.graphml")])
    valid_ids = []

    for vid in video_ids:
        wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        ts_path = RAW_DIR / f"{vid}_transcript.json"
        out_graph = GRAPHS_DIR / f"{vid}.graphml"

        if not wb_path.exists():
            console.print(f"[dim]Skipping {vid}: missing data/good_whiteboard/{vid}.jpg[/]")
            continue
        if not ts_path.exists():
            console.print(f"[dim]Skipping {vid}: missing data/raw/{vid}_transcript.json[/]")
            continue

        if out_graph.exists() and not force:
            continue

        valid_ids.append(vid)

    return valid_ids


def process_batch(video_ids: list[str], force: bool = False) -> None:
    progress = load_progress()
    total = len(video_ids)
    console.print(Panel.fit(
        f"[bold cyan]🚀 Starting Batch Standard Processing (v6corrected Prompt)[/]\n"
        f"Total videos to process: [bold green]{total}[/]\n"
        f"Target directory: [bold]{GRAPHS_DIR}/[/]",
        border_style="cyan"
    ))

    success_count = 0
    error_count = 0
    consecutive_errors = 0

    for idx, vid in enumerate(video_ids, 1):
        console.rule(f"[bold cyan][{idx}/{total}] Processing Video: {vid}")
        
        # Check checkpoint
        if not force and vid in progress and progress[vid].get("status") == "success":
            out_graph = GRAPHS_DIR / f"{vid}.graphml"
            if out_graph.exists():
                console.print(f"[green]✓[/] Already completed in checkpoint. Skipping.")
                success_count += 1
                continue

        wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        ts_path = RAW_DIR / f"{vid}_transcript.json"

        # Load transcript text
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
            # Step 1: Vision analysis via Gemini (v6corrected)
            analysis_result = analyze_frame(
                wb_path,
                transcript=transcript_text,
                video_url=url,
            )

            # Save vision analysis output cache
            analysis_cache_path = RAW_DIR / f"{vid}_vision_analysis.json"
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
            out_graph_path = export_graphml(G, vid)

            # Register in tracker
            add_to_tracker(vid, "version_2")

            elapsed = round(time.time() - start_t, 2)
            node_count = G.number_of_nodes()
            edge_count = G.number_of_edges()

            console.print(
                f"[bold green]✓ [{idx}/{total}] {vid} complete in {elapsed}s[/] → "
                f"[bold]{node_count}[/] nodes, [bold]{edge_count}[/] edges → [cyan]{out_graph_path.name}[/]"
            )

            success_count += 1
            consecutive_errors = 0
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
            consecutive_errors += 1
            progress[vid] = {
                "status": "error",
                "error": err_str,
                "timestamp": time.time(),
            }
            save_progress(progress)

            # Halt if quota or service is exhausted across retries
            if any(k in err_str.upper() for k in ["429", "RESOURCE_EXHAUSTED", "QUOTA", "UNAVAILABLE", "LIMIT"]) or consecutive_errors >= 3:
                console.print(
                    Panel.fit(
                        f"[bold red]🛑 PROCESO DETENIDO: Sin servicio/cuota de Gemini API.[/]\n"
                        f"Detalle del error: {err_str}\n"
                        f"Se probaron las claves API configuradas. Reanuda la ejecución cuando la cuota esté disponible.",
                        border_style="red"
                    )
                )
                sys.exit(1)

        # Brief pause between calls
        time.sleep(1.0)


    console.print("\n[bold green]🎉 Batch Processing Finished![/]")
    console.print(f"Successful: [bold green]{success_count}[/], Failed: [bold red]{error_count}[/]\n")


def main():
    parser = argparse.ArgumentParser(description="Batch process standard mode cloud extraction with v6corrected prompt")
    parser.add_argument("--force", action="store_true", help="Force reprocessing even if output graphml already exists")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of videos to process (0 = all)")
    args = parser.parse_args()

    video_ids = get_target_video_ids(force=args.force)
    if not video_ids:
        console.print("[bold yellow]No pending videos to process![/]")
        return

    if args.limit > 0:
        video_ids = video_ids[:args.limit]

    process_batch(video_ids, force=args.force)


if __name__ == "__main__":
    main()
