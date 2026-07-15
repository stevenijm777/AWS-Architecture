#!/usr/bin/env python3
"""
delete_copied_graphs.py — Deletes all graphml files and raw cache files
                            that were copied directly from the Ground Truth,
                            and updates the processed tracker version_3 list.
"""
import json
import os
from pathlib import Path
from rich.console import Console

console = Console()

def get_copied_video_ids() -> set[str]:
    copied = set()
    raw_dir = Path("data/raw")
    if raw_dir.exists():
        for f in raw_dir.glob("*_vision_analysis_parsimonious.json"):
            try:
                with open(f, "r", encoding="utf-8") as file:
                    data = json.load(file)
                reasoning = data.get("step_by_step_reasoning", "")
                if "Mapping Ground Truth" in reasoning:
                    copied.add(f.name.replace("_vision_analysis_parsimonious.json", ""))
            except Exception:
                pass
    return copied

def main():
    copied_ids = get_copied_video_ids()
    if not copied_ids:
        console.print("[yellow]No ground-truth copied videos found in the cache.[/]")
        return

    console.print(f"[bold red]Found {len(copied_ids)} ground-truth copied videos to remove.[/]")

    # 1. Update processed_tracker.json
    tracker_path = Path("data/processed_tracker.json")
    if tracker_path.exists():
        try:
            with open(tracker_path, "r", encoding="utf-8") as f:
                tracker = json.load(f)
            
            v3_list = tracker.get("version_3", [])
            original_v3_len = len(v3_list)
            updated_v3 = [vid for vid in v3_list if vid not in copied_ids]
            
            tracker["version_3"] = updated_v3
            with open(tracker_path, "w", encoding="utf-8") as f:
                json.dump(tracker, f, indent=2, ensure_ascii=False)
            
            console.print(f"[green]✓[/] Updated {tracker_path}. version_3 size: {original_v3_len} → {len(updated_v3)}")
        except Exception as e:
            console.print(f"[red]✗ Failed to update tracker: {e}[/]")

    # 2. Delete files
    deleted_files_count = 0
    dirs_to_clean = [
        Path("data/graphs_parsimonious"),
        Path("data/graphs_agent_parsimonious"),
        Path("data/raw")
    ]

    for vid in sorted(copied_ids):
        files_to_delete = [
            Path(f"data/graphs_parsimonious/{vid}.graphml"),
            Path(f"data/graphs_agent_parsimonious/{vid}.graphml"),
            Path(f"data/raw/{vid}_vision_analysis_parsimonious.json"),
            Path(f"data/raw/{vid}_agent_parsimonious.json")
        ]
        
        for fpath in files_to_delete:
            if fpath.exists():
                try:
                    fpath.unlink()
                    deleted_files_count += 1
                except Exception as e:
                    console.print(f"[red]✗ Failed to delete {fpath}: {e}[/]")

    console.print(f"[green]✓[/] Successfully deleted {deleted_files_count} files associated with ground-truth copied runs.")

if __name__ == "__main__":
    main()
