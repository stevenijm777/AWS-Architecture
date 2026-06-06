#!/usr/bin/env python3
"""
visualize_gt.py — Generate simplified yEd visual GraphML files for all standard Ground Truth
                  GraphML files in the simplified cloudscape_gt directory.
"""
from __future__ import annotations

import sys
from pathlib import Path
import networkx as nx
from rich.console import Console

# Add project root and simplified root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.graph_builder import export_yed_graphml

console = Console()

def visualize_all_gt():
    gt_dir = Path(__file__).resolve().parent.parent / "data" / "cloudscape_gt"
    
    if not gt_dir.exists():
        console.print(f"[bold red]Error:[/] GT directory {gt_dir} does not exist.")
        sys.exit(1)

    # Find all .graphml files in the GT directory (excluding the visual/ subdirectory)
    gt_files = sorted(gt_dir.glob("*.graphml"))
    
    if not gt_files:
        console.print(f"[yellow]No .graphml files found in {gt_dir}[/]")
        return

    console.print(f"[bold cyan]Generating visual Ground Truth graphs from {gt_dir}...[/]")
    for gt_file in gt_files:
        video_id = gt_file.stem
        console.print(f"Processing [bold green]{video_id}[/]...")
        
        try:
            # Read standard graphml and convert to MultiDiGraph to support any parallel edges
            G_raw = nx.read_graphml(str(gt_file))
            G = nx.MultiDiGraph(G_raw)
            
            # Export to yEd visual GraphML in the cloudscape_gt directory
            export_yed_graphml(G, video_id, output_dir=gt_dir)
        except Exception as e:
            console.print(f"[bold red]Failed to process {gt_file.name}:[/] {e}")

if __name__ == "__main__":
    visualize_all_gt()
