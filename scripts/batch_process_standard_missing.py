#!/usr/bin/env python3
"""
batch_process_standard_missing.py — Batch runner to process missing Standard graphs (v6corrected prompt)
                                    so that Standard matches Parsimonious GT coverage (132+ videos side-by-side).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx
from rich.console import Console
from rich.panel import Panel

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
PROGRESS_FILE = DATA_DIR / "batch_standard_missing_progress.json"


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


def is_valid_graphml(path: Path) -> bool:
    """A graph counts as done only if it exists, is non-empty and actually parses.

    A failed export used to leave a zero-byte file behind, which made this
    script treat the video as completed and never retry it.
    """
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        nx.read_graphml(path)
        return True
    except Exception:
        return False


def get_missing_standard_ids(force: bool = False) -> list[str]:
    gt_dir = DATA_DIR / "cloudscape_gt"
    gt_vids = sorted([f.stem for f in gt_dir.glob("*.graphml")]) if gt_dir.exists() else []
    std_vids = (
        {f.stem for f in GRAPHS_DIR.glob("*.graphml") if is_valid_graphml(f)}
        if GRAPHS_DIR.exists() else set()
    )

    target_ids = []
    for vid in gt_vids:
        if vid in std_vids and not force:
            continue
        wb_path = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        ts_path = RAW_DIR / f"{vid}_transcript.json"

        if wb_path.exists() and ts_path.exists():
            target_ids.append(vid)

    return target_ids



def process_batch(video_ids: list[str], force: bool = False) -> None:
    progress = load_progress()
    total = len(video_ids)
    console.print(Panel.fit(
        f"[bold cyan]🚀 Starting Standard Mode Batch Processing (v6corrected Prompt)[/]\n"
        f"Total videos to process: [bold green]{total}[/]\n"
        f"Target directory: [bold]{GRAPHS_DIR}/[/]",
        border_style="cyan"
    ))

    success_count = 0
    error_count = 0

    for idx, vid in enumerate(video_ids, 1):
        console.rule(f"[bold cyan][{idx}/{total}] Processing Standard Video: {vid}")

        if not force and vid in progress and progress[vid].get("status") == "success":
            out_graph = GRAPHS_DIR / f"{vid}.graphml"
            if is_valid_graphml(out_graph):
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

            out_graph_path = export_graphml(G, vid, output_dir=GRAPHS_DIR)
            add_to_tracker(vid, "version_2")

            elapsed = round(time.time() - start_t, 2)
            node_count = G.number_of_nodes()
            edge_count = G.number_of_edges()

            console.print(
                f"[bold green]✓ [{idx}/{total}] {vid} complete in {elapsed}s[/] → "
                f"[bold]{node_count}[/] nodes, [bold]{edge_count}[/] edges → [cyan]{out_graph_path.name}[/]"
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
                        f"Se probaron las claves API configuradas.",
                        border_style="red"
                    )
                )
                sys.exit(1)

        time.sleep(1.0)

    console.print("\n[bold green]🎉 Standard Missing Batch Finished![/]")
    console.print(f"Successful: [bold green]{success_count}[/], Failed: [bold red]{error_count}[/]\n")


def main():
    parser = argparse.ArgumentParser(description="Batch process missing Standard mode graphs")
    parser.add_argument("--force", action="store_true", help="Force reprocessing even if output graphml already exists")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of videos to process (0 = all)")
    args = parser.parse_args()

    video_ids = get_missing_standard_ids(force=args.force)
    if not video_ids:
        console.print("[bold yellow]No pending missing videos to process for Standard Mode![/]")
        return

    if args.limit > 0:
        video_ids = video_ids[:args.limit]

    process_batch(video_ids, force=args.force)


if __name__ == "__main__":
    main()
