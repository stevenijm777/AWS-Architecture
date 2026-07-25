"""
process_non_analyzed_whiteboards.py — Process non-analyzed GT videos using frame_selector,
                                    save top 1 best whiteboard, top10 folder, and copy
                                    to bad_whiteboard for manual review.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.core.frame_selector import select_best_frame

console = Console()


def process_non_analyzed_videos():
    gt_dir = PROJECT_ROOT / "data" / "cloudscape_gt"
    std_dir = PROJECT_ROOT / "data" / "graphs"
    pars_dir = PROJECT_ROOT / "data" / "graphs_parsimonious"
    frames_dir = PROJECT_ROOT / "data" / "frames"
    bad_wb_dir = PROJECT_ROOT / "data" / "bad_whiteboard"
    lab_bad_wb_dir = PROJECT_ROOT / "whiteboard_selection_lab" / "bad_whiteboard"

    bad_wb_dir.mkdir(parents=True, exist_ok=True)
    lab_bad_wb_dir.mkdir(parents=True, exist_ok=True)

    gt_ids = {f.stem for f in gt_dir.glob("*.graphml")}
    std_ids = {f.stem for f in std_dir.glob("*.graphml")} if std_dir.exists() else set()
    pars_ids = {f.stem for f in pars_dir.glob("*.graphml")} if pars_dir.exists() else set()
    analyzed_ids = std_ids | pars_ids

    non_analyzed = sorted(gt_ids - analyzed_ids)
    console.print(f"\n[bold cyan]🔍 Non-analyzed Ground Truth Videos Count:[/] {len(non_analyzed)}")

    processable = []
    skipped = []

    for vid in non_analyzed:
        f_dir = frames_dir / vid
        if f_dir.exists() and list(f_dir.glob("*.jpg")):
            processable.append(vid)
        else:
            skipped.append(vid)

    console.print(f"[green]✓ {len(processable)} videos have extracted frame folders ready.[/]")
    if skipped:
        console.print(f"[yellow]⚠ {len(skipped)} videos do not have frame folders yet: {skipped}[/]")

    results = []
    
    for i, vid in enumerate(processable, 1):
        console.print(f"\n[bold]------------------------------------------------------------[/]")
        console.print(f"[bold cyan][{i}/{len(processable)}] Processing non-analyzed video {vid}...[/]")
        
        try:
            res = select_best_frame(vid, frames_dir=frames_dir, debug=True)
            
            best_frame_path = Path(res["best_frame"])
            
            # Copy to data/bad_whiteboard/
            dest_bad_wb = bad_wb_dir / f"{vid}.jpg"
            shutil.copy2(best_frame_path, dest_bad_wb)
            
            # Copy to whiteboard_selection_lab/bad_whiteboard/
            dest_lab_bad_wb = lab_bad_wb_dir / f"{vid}.jpg"
            shutil.copy2(best_frame_path, dest_lab_bad_wb)

            results.append({
                "video_id": vid,
                "status": "Success",
                "selected_frame": res["source_frame"].name if hasattr(res["source_frame"], "name") else str(res["source_frame"]),
                "best_wb_path": str(dest_bad_wb),
                "score": f"{res['final_score']:.3f}",
                "occlusion": f"{res['occlusion_pct']:.1f}%",
                "error": ""
            })
            console.print(f"  [bold green]✓ Copied to bad_whiteboard:[/] {dest_bad_wb}")
        except Exception as e:
            console.print(f"  [bold red]✗ Error processing {vid}:[/] {e}")
            results.append({
                "video_id": vid,
                "status": "Error",
                "selected_frame": "",
                "best_wb_path": "",
                "score": "",
                "occlusion": "",
                "error": str(e)
            })

    # Summary Table
    table = Table(title="Non-Analyzed Videos Frame Selection Summary", border_style="cyan", show_lines=True)
    table.add_column("#", style="bold")
    table.add_column("Video ID", style="bold")
    table.add_column("Status")
    table.add_column("Selected Frame", style="green")
    table.add_column("Score", style="magenta")
    table.add_column("Occlusion", style="yellow")
    table.add_column("Saved in bad_whiteboard", style="cyan")

    for idx, r in enumerate(results, 1):
        status_style = "green" if r["status"] == "Success" else "red"
        table.add_row(
            str(idx),
            r["video_id"],
            f"[{status_style}]{r['status']}[/]",
            r["selected_frame"],
            r["score"],
            r["occlusion"],
            Path(r["best_wb_path"]).name if r["best_wb_path"] else "Failed"
        )

    console.print()
    console.print(table)
    
    # Export summary JSON
    summary_file = PROJECT_ROOT / "whiteboard_selection_lab" / "non_analyzed_selection_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    console.print(f"\n[green]✓ Summary report saved to:[/] {summary_file}")

    return results


if __name__ == "__main__":
    process_non_analyzed_videos()
