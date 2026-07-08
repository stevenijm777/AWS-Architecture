"""
bulk_process_good_whiteboards.py — Bulk process all missing good whiteboard videos under version_3
"""
import json
import os
import subprocess
import sys
from pathlib import Path
import networkx as nx
from rich.console import Console

console = Console()

def main():
    tracker_path = Path("data/processed_tracker.json")
    if not tracker_path.exists():
        console.print("[red]Error: processed_tracker.json not found![/]")
        return

    with open(tracker_path, "r") as f:
        tracker = json.load(f)

    v3_processed = set(tracker.get("version_3", []))

    good_whiteboard_dir = Path("data/good_whiteboard")
    good_ids = {Path(f).stem for f in os.listdir(good_whiteboard_dir) if f.endswith(".jpg")}

    missing_raw = sorted(list(good_ids - v3_processed))
    missing_good = []
    for video_id in missing_raw:
        transcript_path = Path(f"data/raw/{video_id}_transcript.json")
        if transcript_path.exists():
            missing_good.append(video_id)
            
    console.print(f"Found {len(missing_good)} missing good whiteboard videos with transcriptions to process.")

    processed_count = 0
    for video_id in missing_good:
        console.print(f"[cyan]ℹ Processing {video_id} using live Gemini Vision API...[/]")
        try:
            cmd = [
                sys.executable,
                "main_parsimonious.py",
                "--url", f"https://www.youtube.com/watch?v={video_id}"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            console.print(f"[green]✓[/] Successfully compiled parsimonious graph for [bold]{video_id}[/]")
            processed_count += 1
        except Exception as e:
            console.print(f"[red]✗ Failed to process {video_id}: {e}[/]")

    console.print(f"\n[bold green]✓[/] Bulk processing complete. Processed {processed_count} videos.")

    # Run evaluate_graphs.py to update reports
    console.print("\n[bold cyan]🔄 Running evaluation to update reports...[/]")
    subprocess.run([sys.executable, "scripts/evaluate_graphs.py"])

if __name__ == "__main__":
    main()
