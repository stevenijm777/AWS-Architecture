#!/usr/bin/env python3
"""
select_all_best_whiteboards.py — Run frame selector on all video frame folders.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import FRAMES_DIR
from scripts.frame_selector import select_best_frame

console = Console()

TEST_VIDEOS = ["7dtomip_VXc", "1xLjtJnfZes", "BgT_bDAejSQ"]

def main():
    parser = argparse.ArgumentParser(description="Process keyframes to select the best whiteboard frame.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test", action="store_true", help=f"Only process the 3 test videos: {TEST_VIDEOS}")
    group.add_argument("--all", action="store_true", help="Process all video frame directories in data/frames/")
    parser.add_argument("--debug", action="store_true", default=True, help="Save debug occlusion images and metadata")
    
    args = parser.parse_args()
    
    if not FRAMES_DIR.exists():
        console.print(f"[bold red]Error: Frames directory not found at {FRAMES_DIR}[/]")
        sys.exit(1)
        
    # Get all subdirectories in FRAMES_DIR
    subdirs = sorted([d for d in FRAMES_DIR.iterdir() if d.is_dir()])
    
    # Filter only those that look like YouTube video ID folders (length 11 and not ending with _pizarra)
    video_ids = []
    for d in subdirs:
        name = d.name
        if len(name) == 11 and not name.endswith("_pizarra"):
            video_ids.append(name)
            
    if args.test:
        # Check if test folders exist
        targets = []
        for vid in TEST_VIDEOS:
            if vid in video_ids:
                targets.append(vid)
            else:
                console.print(f"[yellow]Warning: Test video {vid} directory not found under data/frames/[/]")
        if not targets:
            console.print("[bold red]Error: None of the test video directories were found![/]")
            sys.exit(1)
    else:
        targets = video_ids
        
    console.print(f"\n[bold cyan]🚀 Starting Batch Frame Selection[/] ({len(targets)} videos to process)")
    
    results = []
    success_count = 0
    error_count = 0
    
    for i, vid in enumerate(targets):
        console.print(f"\n[bold]------------------------------------------------------------[/]")
        console.print(f"[bold cyan][{i+1}/{len(targets)}] Processing {vid}...[/]")
        try:
            res = select_best_frame(vid, debug=args.debug)
            results.append({
                "video_id": vid,
                "status": "Success",
                "best_frame": res["best_frame"].name if hasattr(res["best_frame"], "name") else str(res["best_frame"]),
                "source_frame": res["source_frame"].name if hasattr(res["source_frame"], "name") else str(res["source_frame"]),
                "final_score": f"{res['final_score']:.3f}",
                "occlusion_pct": f"{res['occlusion_pct']:.1f}%",
                "error": ""
            })
            success_count += 1
        except Exception as e:
            console.print(f"[bold red]✗ Failed to process {vid}:[/] {e}")
            results.append({
                "video_id": vid,
                "status": "Error",
                "best_frame": "",
                "source_frame": "",
                "final_score": "",
                "occlusion_pct": "",
                "error": str(e)
            })
            error_count += 1
            
    # Print Summary Table
    table = Table(title="Batch Frame Selection Summary", border_style="cyan", show_lines=True)
    table.add_column("Video ID", style="bold")
    table.add_column("Status")
    table.add_column("Selected Frame", style="green")
    table.add_column("Score", style="magenta")
    table.add_column("Occlusion", style="yellow")
    table.add_column("Details / Error", style="red")
    
    for r in results:
        status_style = "green" if r["status"] == "Success" else "red"
        table.add_row(
            r["video_id"],
            f"[{status_style}]{r['status']}[/]",
            r["source_frame"],
            r["final_score"],
            r["occlusion_pct"],
            r["error"]
        )
        
    console.print()
    console.print(table)
    console.print(f"\n[bold green]✓ Done![/] Success: {success_count}, Errors: {error_count}\n")

if __name__ == "__main__":
    main()
