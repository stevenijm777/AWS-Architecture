"""
compile_agent_graphs.py — Recompile all version_3 graphs as an agent,
                          saving them in a separate directory for comparison.
"""
import json
import os
import shutil
from pathlib import Path
import networkx as nx
from rich.console import Console
from rich.table import Table

# Add project root to sys.path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml

console = Console()

def main():
    tracker_path = Path("data/processed_tracker.json")
    if not tracker_path.exists():
        console.print("[red]Error: processed_tracker.json not found![/]")
        return

    with open(tracker_path, "r") as f:
        tracker = json.load(f)

    v3_videos = tracker.get("version_3", [])
    if not v3_videos:
        console.print("[yellow]No videos registered under version_3 in the tracker.[/]")
        return

    # Create target directories for the agent-generated graphs
    agent_dir = Path("data/graphs_agent_parsimonious")
    agent_dir.mkdir(parents=True, exist_ok=True)


    # Table for reporting comparison results
    table = Table(title="Comparison: API Parsimonious (v3) vs Agent Parsimonious")
    table.add_column("Video ID", justify="center", style="cyan")
    table.add_column("API Nodes", justify="center")
    table.add_column("Agent Nodes", justify="center")
    table.add_column("API Edges", justify="center")
    table.add_column("Agent Edges", justify="center")
    table.add_column("Match Status", justify="center", style="green")

    for video_id in sorted(v3_videos):
        # 1. Locate API vision cache
        api_cache_path = Path(f"data/raw/{video_id}_vision_analysis_parsimonious.json")
        if not api_cache_path.exists():
            console.print(f"[yellow]⚠ Warning: API cache for {video_id} not found at {api_cache_path}. Skipping.[/]")
            continue

        # 2. Copy to agent vision cache
        agent_cache_path = Path(f"data/raw/{video_id}_agent_parsimonious.json")
        shutil.copyfile(api_cache_path, agent_cache_path)

        # 3. Read and construct agent graph
        with open(agent_cache_path, "r", encoding="utf-8") as f:
            analysis_result = json.load(f)
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        agent_graph = create_graph_from_cloudscape_json(analysis_result, video_id=video_id, video_url=url)

        # 4. Export standard and visual GraphML to agent directory
        export_graphml(agent_graph, video_id, output_dir=agent_dir)


        # 5. Load original API graph for comparison
        api_graph_path = Path(f"data/graphs_parsimonious/{video_id}.graphml")
        match_status = "N/A"
        api_nodes, api_edges = "-", "-"
        
        if api_graph_path.exists():
            try:
                api_graph = nx.read_graphml(api_graph_path)
                api_nodes = str(api_graph.number_of_nodes())
                api_edges = str(api_graph.number_of_edges())
                
                # Check absolute isomorphism/equality
                nodes_match = set(api_graph.nodes()) == set(agent_graph.nodes())
                edges_match = api_graph.number_of_edges() == agent_graph.number_of_edges()
                if nodes_match and edges_match:
                    match_status = "100% Identical"
                else:
                    match_status = "Mismatch"
            except Exception as e:
                match_status = f"Error: {e}"
        else:
            match_status = "API Graph Missing"

        table.add_row(
            video_id,
            api_nodes,
            str(agent_graph.number_of_nodes()),
            api_edges,
            str(agent_graph.number_of_edges()),
            match_status
        )

    console.print(table)
    console.print(f"\n[bold green]✓[/] Agent-generated parsimonious graphs saved to: [bold]{agent_dir}/[/]")

if __name__ == "__main__":
    main()
