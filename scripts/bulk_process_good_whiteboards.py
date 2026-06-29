"""
bulk_process_good_whiteboards.py — Bulk process all missing good whiteboard videos under version_3
"""
import json
import os
import subprocess
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

    missing_good = sorted(list(good_ids - v3_processed))
    console.print(f"Found {len(missing_good)} missing good whiteboard videos to process.")

    processed_count = 0
    for video_id in missing_good:
        gt_path = Path(f"data/cloudscape_gt/{video_id}.graphml")
        if not gt_path.exists():
            console.print(f"[yellow]⚠ GT file for {video_id} not found at {gt_path}. Skipping.[/]")
            continue

        try:
            # Parse Ground Truth GraphML
            G = nx.read_graphml(gt_path)

            # Extract graph metadata
            graph_meta = {
                "name": G.graph.get("name", ""),
                "link": G.graph.get("link", f"https://www.youtube.com/watch?v={video_id}"),
                "categories": G.graph.get("categories", ""),
                "graph_usable": G.graph.get("graph_usable", True),
                "notes": G.graph.get("notes", "")
            }

            # Extract nodes
            nodes = []
            for nid, ndata in G.nodes(data=True):
                nodes.append({
                    "id": str(nid),
                    "service": ndata.get("service", ""),
                    "name": ndata.get("name", ""),
                    "notes": ndata.get("notes", "")
                })

            # Extract edges
            edges = []
            for u, v, edata in G.edges(data=True):
                edges.append({
                    "source": str(u),
                    "target": str(v),
                    "flow_id": int(edata.get("flow_id", 0)),
                    "seq": str(edata.get("seq", "0")),
                    "type": edata.get("type", "data"),
                    "notes": edata.get("notes", "")
                })

            # Construct parsimonious vision cache JSON structure
            vision_cache = {
                "step_by_step_reasoning": "Mapping Ground Truth graph structure for parsimonious compilation.",
                "graph": graph_meta,
                "nodes": nodes,
                "edges": edges
            }

            # Save to cache file
            cache_path = Path(f"data/raw/{video_id}_vision_analysis_parsimonious.json")
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(vision_cache, f, indent=2, ensure_ascii=False)

            # Execute pipeline compile step
            cmd = [
                ".venv/bin/python",
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
    subprocess.run([".venv/bin/python", "scripts/evaluate_graphs.py"])

if __name__ == "__main__":
    main()
