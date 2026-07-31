#!/usr/bin/env python3
"""
process_batch_vision.py — Batch runner for Gemini Vision API architecture extraction.

Features:
  - Supports both 'standard' (data/graphs) and 'parsimonious' (data/graphs_parsimonious) modes.
  - Processes missing videos (videos with good whiteboard + transcript that lack a GraphML output).
  - Default: processes 10 missing videos (--limit 10).
  - Quota mode (--until-quota / --until-quota-exhausted): processes missing videos continuously
    until all are completed OR until the Gemini API quota/rate limit is reached.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

console = Console()

def get_missing_videos(mode: str = "standard", force: bool = False) -> list[str]:
    """Find video IDs that have good_whiteboard + transcript but lack a graphml output."""
    good_wb_dir = PROJECT_ROOT / "data" / "good_whiteboard"
    raw_dir = PROJECT_ROOT / "data" / "raw"
    
    if mode == "parsimonious":
        target_dir = PROJECT_ROOT / "data" / "graphs_parsimonious"
    else:
        target_dir = PROJECT_ROOT / "data" / "graphs"

    if not good_wb_dir.exists() or not raw_dir.exists():
        return []

    good_ids = {f.stem for f in good_wb_dir.glob("*.jpg")}
    transcript_ids = {f.name.replace("_transcript.json", "") for f in raw_dir.glob("*_transcript.json")}

    candidates = sorted(list(good_ids & transcript_ids))

    if force:
        return candidates

    existing_graphs = {f.stem for f in target_dir.glob("*.graphml")} if target_dir.exists() else set()

    missing = [vid for vid in candidates if vid not in existing_graphs]
    return missing


def is_quota_error(err_str: str) -> bool:
    """Check if an error string indicates Gemini API quota or rate limit exhaustion."""
    err_upper = err_str.upper()
    err_lower = err_str.lower()
    quota_indicators = [
        "429",
        "RESOURCE_EXHAUSTED",
        "QUOTA EXCEEDED",
        "QUOTA",
        "RATE_LIMIT_EXCEEDED",
        "EXCEEDED YOUR CURRENT QUOTA",
    ]
    return any(indicator in err_upper or indicator.lower() in err_lower for indicator in quota_indicators)


def run_batch(
    mode: str = "standard",
    limit: int | None = 10,
    until_quota: bool = False,
    force: bool = False,
):
    """Execute vision analysis batch processing."""
    console.print(
        f"\n[bold cyan]🚀 Starting Vision Batch Runner[/] Mode: [bold yellow]{mode.upper()}[/]"
    )

    missing = get_missing_videos(mode=mode, force=force)
    total_missing = len(missing)

    console.print(f"📊 Found [bold cyan]{total_missing}[/] videos pending processing in {mode.upper()} mode.")

    if not missing:
        console.print("[bold green]✓ No missing videos to process! All candidate graphs are up-to-date.[/]")
        return

    # Determine execution limit
    if until_quota:
        max_videos = total_missing
        console.print("[bold green]🔄 Execution mode: CONTINUOUS until quota exhausted or all videos complete.[/]")
    else:
        max_videos = min(limit or 10, total_missing)
        console.print(f"[bold green]🎯 Execution mode: Processing up to {max_videos} videos.[/]")

    queue = missing[:max_videos]

    processed_success = []
    processed_failed = []
    quota_exhausted = False

    env = dict(os.environ)
    if "GEMINI_MODEL" not in env:
        env["GEMINI_MODEL"] = "gemini-3-flash-preview"

    start_time = time.time()

    for idx, vid in enumerate(queue, 1):
        console.print("\n" + "─" * 60)
        console.print(f"[bold cyan][{idx}/{len(queue)}] Processing Video ID: {vid}[/]")
        console.print("─" * 60)

        cmd = [
            sys.executable,
            str(PROJECT_ROOT / "main.py"),
            "--url", f"https://www.youtube.com/watch?v={vid}",
            "--mode", mode,
        ]
        if force:
            cmd.append("--force-vision")

        try:
            res = subprocess.run(cmd, env=env, text=True, capture_output=True)
            
            if res.returncode == 0:
                console.print(f"[bold green]✓ Successfully processed {vid}[/]")
                processed_success.append(vid)
            else:
                err_output = res.stderr + "\n" + res.stdout
                console.print(f"[bold red]✗ Failed to process {vid}[/]")
                
                if is_quota_error(err_output):
                    console.print(f"\n[bold red]🛑 Gemini API Quota Exhausted / Rate Limit Reached![/]")
                    console.print(f"[yellow]Details: {err_output[-300:].strip()}[/]")
                    quota_exhausted = True
                    processed_failed.append({"video_id": vid, "reason": "Quota Exhausted"})
                    break
                else:
                    console.print(f"[dim]Error: {err_output[-250:].strip()}[/]")
                    processed_failed.append({"video_id": vid, "reason": "Execution Error"})

        except Exception as e:
            console.print(f"[bold red]✗ Unexpected error processing {vid}: {e}[/]")
            processed_failed.append({"video_id": vid, "reason": str(e)})

    total_duration = time.time() - start_time

    # ── Summary Table ──
    table = Table(title=f"Batch Vision Execution Summary ({mode.upper()} Mode)", border_style="cyan", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Mode", mode.capitalize())
    table.add_row("Successful Videos", str(len(processed_success)))
    table.add_row("Failed / Stopped Videos", str(len(processed_failed)))
    table.add_row("Total Time", f"{total_duration:.1f}s ({total_duration/60:.2f} m)")
    table.add_row("Status", "Stopped by Quota Limit" if quota_exhausted else "Batch Complete")

    console.print("\n")
    console.print(table)

    rem_after = len(get_missing_videos(mode=mode, force=False))
    console.print(f"\n[bold yellow]📌 Remaining missing videos in {mode.upper()} mode: {rem_after}[/]\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch process missing AWS Architecture videos with Gemini Vision API."
    )
    parser.add_argument(
        "--mode", choices=["standard", "parsimonious"], default="standard",
        help="Processing mode: 'standard' (data/graphs) or 'parsimonious' (data/graphs_parsimonious). Default: standard",
    )
    parser.add_argument(
        "--limit", type=int, default=10,
        help="Number of missing videos to process (default: 10)",
    )
    parser.add_argument(
        "--until-quota", "--until-quota-exhausted", "--all", dest="until_quota", action="store_true",
        help="Process missing videos continuously until API quota is exhausted or all are done",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Force reprocessing even if GraphML output already exists",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_batch(
        mode=args.mode,
        limit=args.limit,
        until_quota=args.until_quota,
        force=args.force,
    )
