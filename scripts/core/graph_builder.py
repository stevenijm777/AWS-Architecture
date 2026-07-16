"""
graph_builder.py — Build a NetworkX MultiDiGraph from Cloudscape-schema data
                   and export to standard GraphML (compatible with Cloudscape
                   dataset from FAST25).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

import networkx as nx
from rich.console import Console

from config.settings import GRAPHS_DIR

console = Console()


def load_valid_services() -> dict[str, str]:
    csv_path = Path(__file__).resolve().parent.parent.parent / "graph_renderer" / "services.csv"
    if not csv_path.exists():
        return {}

    valid_services = {}
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                valid_services[name.lower()] = name
    return valid_services


def create_graph_from_cloudscape_json(
    analysis_result: dict[str, Any],
    video_id: str = "",
    video_url: str = "",
) -> nx.MultiDiGraph:
    """
    Create a MultiDiGraph from Cloudscape-schema JSON output.

    The JSON should have ``graph``, ``nodes``, and ``edges`` keys
    matching the Cloudscape dataset schema.

    Parameters
    ----------
    analysis_result : dict
        Output from ``vision_analyzer.analyze_frame()`` with Cloudscape schema.
    video_id : str
        YouTube video ID.
    video_url : str
        Full YouTube URL.

    Returns
    -------
    nx.MultiDiGraph
        Graph compatible with Cloudscape dataset.
    """
    graph_meta = analysis_result.get("graph", {})
    nodes_data = analysis_result.get("nodes", [])
    edges_data = analysis_result.get("edges", [])

    # Create graph with Cloudscape-standard attributes
    G = nx.MultiDiGraph()
    G.graph["name"] = graph_meta.get("name", "")
    G.graph["link"] = graph_meta.get("link", video_url or "")
    G.graph["notes"] = graph_meta.get("notes", "")
    G.graph["categories"] = graph_meta.get("categories", "")
    G.graph["graph_usable"] = graph_meta.get("graph_usable", True)

    valid_services = load_valid_services()

    # ── Add Nodes ────────────────────────────────────────────
    for node in nodes_data:
        node_id = str(node.get("id", ""))
        service = str(node.get("service", "")).strip()
        name = str(node.get("name", "")).strip()
        notes = str(node.get("notes", "")).strip()

        # Normalize service name casing and resolve generic services
        service_lower = service.lower()
        service_clean = service_lower.replace(" ", "").replace("-", "").replace("_", "")
        
        if "cloudwatch" in service_clean:
            service = "CloudWatch"
        elif "stepfunction" in service_clean:
            service = "StepFunctions"
        elif "apigateway" in service_clean:
            service = "ApiGateway"
        elif "renderingengine" in service_clean or "spotinstance" in service_clean:
            service = "EC2"
        elif service_clean in valid_services:
            service = valid_services[service_clean]
        elif service_lower == "database":
            # Map generic Database to ThirdParty (or RDS/DynamoDB if specified in name/notes)
            if "dynamodb" in name.lower() or "dynamodb" in notes.lower():
                service = "DynamoDB"
            elif "rds" in name.lower() or "rds" in notes.lower() or "sql" in name.lower():
                service = "RDS"
            else:
                service = "ThirdParty"
                if not name:
                    name = "unspecified AWS database services"
        
        # Final validation against valid_services
        if service.lower() not in valid_services and service:
            console.print(f"[yellow]⚠[/] Unknown service '{service}' normalized to 'ThirdParty'")
            if not name:
                name = service
            service = "ThirdParty"

        G.add_node(
            node_id,
            name=name,
            service=service,
            notes=notes,
        )

    # ── Add Edges ────────────────────────────────────────────
    for edge in edges_data:
        src = str(edge.get("source", ""))
        tgt = str(edge.get("target", ""))
        if not src or not tgt:
            continue

        # Ensure source/target nodes exist
        for nid in (src, tgt):
            if not G.has_node(nid):
                G.add_node(nid, name="", service="unknown", notes="")

        G.add_edge(
            src,
            tgt,
            flow_id=int(edge.get("flow_id", 0)),
            notes=edge.get("notes", ""),
            seq=str(edge.get("seq", "0")),
            type=edge.get("type", "data"),
        )

    console.print(
        f"[green]✓[/] Graph created: "
        f"[bold]{G.number_of_nodes()}[/] nodes, "
        f"[bold]{G.number_of_edges()}[/] edges"
    )
    return G


def export_graphml(
    G: nx.MultiDiGraph,
    video_id: str,
    output_dir: Path | None = None,
) -> Path:
    """
    Export the graph as a standard ``.graphml`` file (Cloudscape-compatible).

    Returns
    -------
    Path
        Path to the saved GraphML file.
    """
    output_dir = output_dir or GRAPHS_DIR
    output_path = output_dir / f"{video_id}.graphml"

    nx.write_graphml(G, str(output_path))

    console.print(f"[green]✓[/] Graph exported → [bold]{output_path}[/]")
    return output_path



def print_graph_summary(G: nx.MultiDiGraph) -> None:
    """Pretty-print a summary of the graph contents."""
    console.print("\n[bold]═══ Graph Summary (Cloudscape Schema) ═══[/]")

    # Graph-level attributes
    console.print(f"  Name: {G.graph.get('name', 'N/A')}")
    console.print(f"  Link: {G.graph.get('link', 'N/A')}")
    console.print(f"  Categories: {G.graph.get('categories', 'N/A')}")
    console.print(f"  Usable: {G.graph.get('graph_usable', 'N/A')}")
    notes = G.graph.get("notes", "")
    if notes:
        console.print(f"  Notes: {notes[:120]}{'…' if len(notes) > 120 else ''}")

    console.print(f"\n  Nodes: {G.number_of_nodes()}")
    console.print(f"  Edges: {G.number_of_edges()}")

    # Identify workflows
    flow_ids = set()
    for _, _, attrs in G.edges(data=True):
        flow_ids.add(attrs.get("flow_id", 0))
    console.print(f"  Workflows: {len(flow_ids)}")

    if G.number_of_nodes() > 0:
        console.print("\n  [bold]Nodes:[/]")
        for node_id, attrs in G.nodes(data=True):
            service = attrs.get("service", "?")
            name = attrs.get("name", "")
            notes = attrs.get("notes", "")
            label = f"{service}"
            if name:
                label += f" ({name})"
            if notes:
                label += f" — {notes[:60]}"
            console.print(f"    [{node_id}] {label}")

    if G.number_of_edges() > 0:
        console.print("\n  [bold]Edges:[/]")
        for src, tgt, attrs in G.edges(data=True):
            flow = attrs.get("flow_id", "?")
            seq = attrs.get("seq", "?")
            etype = attrs.get("type", "?")
            notes = attrs.get("notes", "")
            line = f"    F{flow}.{seq} [{etype}] {src} → {tgt}"
            if notes:
                line += f" ({notes})"
            console.print(line)

    console.print("")


def compare_with_ground_truth(
    generated: nx.MultiDiGraph,
    ground_truth_path: Path,
) -> dict[str, Any]:
    """
    Compare a generated graph against Cloudscape ground truth.

    Returns
    -------
    dict
        Comparison metrics.
    """
    gt = nx.read_graphml(str(ground_truth_path))

    # Extract service sets
    gen_services = {attrs.get("service", "") for _, attrs in generated.nodes(data=True)}
    gt_services = {attrs.get("service", "") for _, attrs in gt.nodes(data=True)}

    # Edge counts
    gen_edges = generated.number_of_edges()
    gt_edges = gt.number_of_edges()

    # Workflow counts
    gen_flows = {attrs.get("flow_id", 0) for _, _, attrs in generated.edges(data=True)}
    gt_flows = {attrs.get("flow_id", 0) for _, _, attrs in gt.edges(data=True)}

    metrics = {
        "gen_nodes": generated.number_of_nodes(),
        "gt_nodes": gt.number_of_nodes(),
        "gen_edges": gen_edges,
        "gt_edges": gt_edges,
        "gen_services": sorted(gen_services),
        "gt_services": sorted(gt_services),
        "services_intersection": sorted(gen_services & gt_services),
        "services_only_in_gen": sorted(gen_services - gt_services),
        "services_only_in_gt": sorted(gt_services - gen_services),
        "service_precision": len(gen_services & gt_services) / len(gen_services) if gen_services else 0,
        "service_recall": len(gen_services & gt_services) / len(gt_services) if gt_services else 0,
        "gen_workflows": len(gen_flows),
        "gt_workflows": len(gt_flows),
    }

    console.print("\n[bold]═══ Comparison with Ground Truth ═══[/]")
    console.print(f"  Nodes:     gen={metrics['gen_nodes']}, gt={metrics['gt_nodes']}")
    console.print(f"  Edges:     gen={metrics['gen_edges']}, gt={metrics['gt_edges']}")
    console.print(f"  Workflows: gen={metrics['gen_workflows']}, gt={metrics['gt_workflows']}")
    console.print(f"  Services in both: {metrics['services_intersection']}")
    console.print(f"  Only in generated: {metrics['services_only_in_gen']}")
    console.print(f"  Only in GT:        {metrics['services_only_in_gt']}")
    console.print(
        f"  Service Precision: {metrics['service_precision']:.1%}"
        f"  Recall: {metrics['service_recall']:.1%}"
    )

    return metrics
