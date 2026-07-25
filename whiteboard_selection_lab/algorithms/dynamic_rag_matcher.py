"""
dynamic_rag_matcher.py — Dynamic Few-Shot RAG Retriever & Matcher for AWS Architecture Graphs

Provides utilities to:
1. Parse all Ground Truth (.graphml) files from data/cloudscape_gt/.
2. Extract service sets from target world_model.json.
3. Compute Jaccard / Overlap similarity to find Top-K similar Ground Truth graphs (with target video exclusion).
4. Visualize matched graphs side-by-side using NetworkX / Matplotlib.
5. Format retrieved GT graphs into JSON Few-Shot exemplars for Gemini prompts.
"""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


class GroundTruthGraph:
    """Represents a parsed Ground Truth architecture graph."""
    def __init__(self, video_id: str, name: str, link: str, categories: List[str],
                 usable: bool, notes: str, nodes: List[Dict[str, Any]],
                 edges: List[Dict[str, Any]], service_set: Set[str]):
        self.video_id = video_id
        self.name = name
        self.link = link
        self.categories = categories
        self.usable = usable
        self.notes = notes
        self.nodes = nodes
        self.edges = edges
        self.service_set = service_set

    def to_json(self) -> Dict[str, Any]:
        """Convert to standard schema dict."""
        return {
            "graph": {
                "name": self.name,
                "link": self.link,
                "categories": ", ".join(self.categories) if isinstance(self.categories, list) else str(self.categories),
                "graph_usable": self.usable,
                "notes": self.notes
            },
            "nodes": self.nodes,
            "edges": self.edges
        }

    def to_networkx(self) -> nx.DiGraph:
        """Convert to NetworkX DiGraph for plotting/analysis."""
        G = nx.DiGraph(name=self.name, video_id=self.video_id)
        for n in self.nodes:
            G.add_node(n["id"], service=n.get("service", ""), name=n.get("name", ""), notes=n.get("notes", ""))
        for e in self.edges:
            G.add_edge(e["source"], e["target"], flow_id=e.get("flow_id", 0), seq=e.get("seq", "0"), type=e.get("type", "data"))
        return G


def parse_graphml_file(graphml_path: Path) -> GroundTruthGraph:
    """Parse a GraphML XML file into GroundTruthGraph object."""
    tree = ET.parse(graphml_path)
    root = tree.getroot()
    
    # GraphML namespaces
    ns = {'g': 'http://graphml.graphdrawing.org/xmlns'}
    
    # Map key IDs
    key_map = {}
    for key in root.findall('g:key', ns):
        k_id = key.attrib.get('id')
        for_type = key.attrib.get('for')
        name = key.attrib.get('attr.name')
        key_map[k_id] = (for_type, name)

    video_id = graphml_path.stem
    graph_elem = root.find('g:graph', ns)
    
    # Graph metadata
    graph_data = {}
    for data in graph_elem.findall('g:data', ns):
        k_id = data.attrib.get('key')
        if k_id in key_map:
            _, attr_name = key_map[k_id]
            graph_data[attr_name] = data.text or ""
            
    name = graph_data.get('name', f"Video {video_id}")
    link = graph_data.get('link', f"https://www.youtube.com/watch?v={video_id}")
    categories_str = graph_data.get('categories', '')
    categories = [c.strip() for c in categories_str.split(',') if c.strip()]
    usable_val = graph_data.get('graph_usable', 'True')
    usable = usable_val.lower() == 'true' if isinstance(usable_val, str) else bool(usable_val)
    notes = graph_data.get('notes', '')

    # Nodes
    nodes = []
    service_set = set()
    for node_elem in graph_elem.findall('g:node', ns):
        n_id = node_elem.attrib.get('id')
        n_data = {}
        for data in node_elem.findall('g:data', ns):
            k_id = data.attrib.get('key')
            if k_id in key_map:
                _, attr_name = key_map[k_id]
                n_data[attr_name] = data.text or ""
        
        svc = n_data.get('service', '').strip()
        n_name = n_data.get('name', '').strip()
        n_notes = n_data.get('notes', '').strip()
        
        if svc:
            service_set.add(svc)
            
        nodes.append({
            "id": str(n_id),
            "service": svc,
            "name": n_name or svc,
            "notes": n_notes
        })

    # Edges
    edges = []
    for edge_elem in graph_elem.findall('g:edge', ns):
        src = str(edge_elem.attrib.get('source'))
        tgt = str(edge_elem.attrib.get('target'))
        e_data = {}
        for data in edge_elem.findall('g:data', ns):
            k_id = data.attrib.get('key')
            if k_id in key_map:
                _, attr_name = key_map[k_id]
                e_data[attr_name] = data.text or ""
                
        fid_raw = e_data.get('flow_id', '0')
        try:
            flow_id = int(fid_raw)
        except ValueError:
            flow_id = 0
            
        edges.append({
            "source": src,
            "target": tgt,
            "flow_id": flow_id,
            "seq": str(e_data.get('seq', '0')),
            "type": e_data.get('type', 'data'),
            "notes": e_data.get('notes', '')
        })

    return GroundTruthGraph(
        video_id=video_id,
        name=name,
        link=link,
        categories=categories,
        usable=usable,
        notes=notes,
        nodes=nodes,
        edges=edges,
        service_set=service_set
    )


def parse_gt_json_file(json_path: Path) -> GroundTruthGraph:
    """Parse a Ground Truth JSON file into GroundTruthGraph object."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    video_id = json_path.stem
    graph_info = data.get("graph", {})
    name = graph_info.get("name", f"Video {video_id}")
    link = graph_info.get("link", f"https://www.youtube.com/watch?v={video_id}")
    cats_val = graph_info.get("categories", "")
    categories = [c.strip() for c in cats_val.split(",") if c.strip()] if isinstance(cats_val, str) else list(cats_val)
    usable = graph_info.get("graph_usable", True)
    notes = graph_info.get("notes", "")

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])
    
    service_set = set()
    for n in nodes:
        svc = n.get("service", "").strip()
        if svc:
            service_set.add(svc)

    return GroundTruthGraph(
        video_id=video_id,
        name=name,
        link=link,
        categories=categories,
        usable=usable,
        notes=notes,
        nodes=nodes,
        edges=edges,
        service_set=service_set
    )


def load_all_ground_truths(gt_dir: Path) -> Dict[str, GroundTruthGraph]:
    """Load and parse all Ground Truth files (.json or .graphml) from gt_dir or corresponding gt_json dir."""
    gt_db = {}
    
    # Check if gt_dir itself contains .json or if there is a cloudscape_gt_json directory
    json_dir = gt_dir.parent / "cloudscape_gt_json" if gt_dir.name == "cloudscape_gt" else gt_dir
    
    if json_dir.exists() and list(json_dir.glob("*.json")):
        # Fast load from JSON
        for p in json_dir.glob("*.json"):
            try:
                gt_obj = parse_gt_json_file(p)
                gt_db[p.stem] = gt_obj
            except Exception as e:
                print(f"⚠ Warning: Error parsing {p.name}: {e}")
    else:
        # Fallback to GraphML XML parsing
        for p in gt_dir.glob("*.graphml"):
            try:
                gt_obj = parse_graphml_file(p)
                gt_db[p.stem] = gt_obj
            except Exception as e:
                print(f"⚠ Warning: Error parsing {p.name}: {e}")
                
    return gt_db


def extract_services_from_world_model(world_model_data: Dict[str, Any]) -> Set[str]:
    """Extract unique AWS services from world_model.json entities."""
    services = set()
    entities = world_model_data.get("entities", [])
    for ent in entities:
        svc = ent.get("service", "").strip()
        if svc and svc.lower() != "user":
            services.add(svc)
    return services


def find_similar_ground_truths(
    target_video_id: str,
    target_services: Set[str],
    gt_db: Dict[str, GroundTruthGraph],
    top_k: int = 3
) -> List[Dict[str, Any]]:
    """
    Search for top_k Ground Truth graphs most similar to target_services.
    
    EXCLUSION RULE: Excludes target_video_id from candidate pool to prevent data leakage.
    """
    results = []
    
    for vid, gt_obj in gt_db.items():
        # 1. EXCLUSION RULE: Skip candidate if it is the target video itself!
        if vid == target_video_id:
            continue
            
        cand_services = gt_obj.service_set
        if not cand_services:
            continue
            
        intersection = target_services & cand_services
        union = target_services | cand_services
        
        jaccard = len(intersection) / len(union) if union else 0.0
        overlap = len(intersection) / min(len(target_services), len(cand_services)) if target_services and cand_services else 0.0
        
        # Combined score prioritizing Jaccard & absolute count of shared services
        score = jaccard * 0.7 + overlap * 0.3
        
        results.append({
            "video_id": vid,
            "gt_name": gt_obj.name,
            "score": round(score, 4),
            "jaccard": round(jaccard, 4),
            "overlap": round(overlap, 4),
            "shared_services": sorted(list(intersection)),
            "shared_count": len(intersection),
            "target_services": sorted(list(target_services)),
            "gt_services": sorted(list(cand_services)),
            "missing_in_gt": sorted(list(target_services - cand_services)),
            "extra_in_gt": sorted(list(cand_services - target_services)),
            "gt_object": gt_obj
        })

    # Sort descending by score, then shared_count
    results.sort(key=lambda x: (x["score"], x["shared_count"]), reverse=True)
    return results[:top_k]


def build_world_model_networkx(world_model_data: Dict[str, Any]) -> nx.DiGraph:
    """Convert world_model.json to a NetworkX DiGraph for comparison visualization."""
    G = nx.DiGraph(name="World Model (Target)")
    
    # Add nodes
    for idx, ent in enumerate(world_model_data.get("entities", [])):
        svc = ent.get("service", f"Entity_{idx}")
        lbl = ent.get("name", svc)
        G.add_node(lbl, service=svc, type=ent.get("type", ""))
        
    # Add edges
    for conn in world_model_data.get("visual_connections", []):
        src = conn.get("source_label", "")
        tgt = conn.get("target_label", "")
        if src and tgt:
            G.add_edge(src, tgt, description=conn.get("description", ""))
            
    return G


def visualize_target_and_similar_graphs(
    target_video_id: str,
    world_model_data: Dict[str, Any],
    matched_results: List[Dict[str, Any]],
    output_path: Path | None = None
):
    """Plot target world model alongside the top matched Ground Truth graphs."""
    num_plots = 1 + len(matched_results)
    fig, axes = plt.subplots(1, num_plots, figsize=(6 * num_plots, 6))
    if num_plots == 1:
        axes = [axes]
        
    # 1. Plot Target World Model
    G_target = build_world_model_networkx(world_model_data)
    pos_target = nx.spring_layout(G_target, seed=42)
    ax0 = axes[0]
    nx.draw_networkx_nodes(G_target, pos_target, ax=ax0, node_color='lightcyan', node_size=1200, edgecolors='teal')
    nx.draw_networkx_edges(G_target, pos_target, ax=ax0, edge_color='teal', arrows=True, arrowsize=15)
    labels0 = {n: f"{n}\n({d.get('service','')})" for n, d in G_target.nodes(data=True)}
    nx.draw_networkx_labels(G_target, pos_target, labels=labels0, ax=ax0, font_size=8, font_weight='bold')
    ax0.set_title(f"Target: {target_video_id}\n(World Model)", fontsize=10, fontweight='bold', color='navy')
    ax0.axis('off')

    # 2. Plot Matched GT Graphs
    for idx, match in enumerate(matched_results, 1):
        gt_obj: GroundTruthGraph = match["gt_object"]
        G_match = gt_obj.to_networkx()
        pos_m = nx.spring_layout(G_match, seed=42)
        ax = axes[idx]
        
        # Color nodes: Highlight shared services vs GT-only services
        shared_svcs = set(match["shared_services"])
        node_colors = []
        for n, d in G_match.nodes(data=True):
            if d.get("service") in shared_svcs:
                node_colors.append('lightgreen')  # Match
            else:
                node_colors.append('mistyrose')   # Difference
                
        nx.draw_networkx_nodes(G_match, pos_m, ax=ax, node_color=node_colors, node_size=1200, edgecolors='darkgreen')
        nx.draw_networkx_edges(G_match, pos_m, ax=ax, edge_color='gray', arrows=True, arrowsize=15)
        labels_m = {n: f"[{n}] {d.get('service','')}" for n, d in G_match.nodes(data=True)}
        nx.draw_networkx_labels(G_match, pos_m, labels=labels_m, ax=ax, font_size=8)
        
        title_str = (
            f"Rank #{idx}: {match['video_id']}\n"
            f"Score: {match['score']:.2f} (Jaccard: {match['jaccard']:.2f})\n"
            f"Shared: {', '.join(match['shared_services'][:4])}"
        )
        ax.set_title(title_str, fontsize=9, fontweight='bold', color='darkgreen')
        ax.axis('off')

    plt.tight_layout()
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=200, bbox_inches='tight')
        print(f"📊 Visualization saved to: {output_path}")
    plt.show()


def format_few_shot_prompt(matched_results: List[Dict[str, Any]]) -> str:
    """
    Build clean JSON text representation of retrieved GT graphs for prompt injection.
    """
    exemplars = []
    for idx, match in enumerate(matched_results, 1):
        gt_obj: GroundTruthGraph = match["gt_object"]
        json_data = gt_obj.to_json()
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
        
        exemplar_text = (
            f"--- REFERENCE EXAMPLE {idx} (Video ID: {gt_obj.video_id}) ---\n"
            f"Architecture Name: {gt_obj.name}\n"
            f"Shared AWS Services: {', '.join(match['shared_services'])}\n"
            f"Ground Truth JSON Graph:\n{json_str}\n"
        )
        exemplars.append(exemplar_text)
        
    return "\n".join(exemplars)
