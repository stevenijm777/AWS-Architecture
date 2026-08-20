#!/usr/bin/env python3
"""
audit_parsimonious_provenance.py — Audit script to check and classify parsimonious cache files.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load valid services catalog
def load_valid_services() -> set[str]:
    csv_paths = [
        PROJECT_ROOT / "data" / "services.csv",
        PROJECT_ROOT / "graph_renderer" / "services.csv",
        PROJECT_ROOT / "data" / "cloudscape_gt" / "services.csv"
    ]
    for p in csv_paths:
        if p.exists():
            valid = set()
            with open(p, mode="r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    name = row.get("name", "").strip()
                    if name:
                        valid.add(name)
            return valid
    return set()

def compare_json_contents(path1: Path, path2: Path) -> bool:
    if not path1.exists() or not path2.exists():
        return False
    try:
        with open(path1, "r", encoding="utf-8") as f1, open(path2, "r", encoding="utf-8") as f2:
            d1 = json.load(f1)
            d2 = json.load(f2)
            return d1 == d2
    except Exception:
        return False

def main():
    raw_dir = PROJECT_ROOT / "data" / "raw"
    graphs_dir = PROJECT_ROOT / "data" / "graphs_parsimonious"
    lab_dir = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    valid_services = load_valid_services()

    # Find all cache files
    cache_files = sorted(raw_dir.glob("*_vision_analysis_parsimonious.json"))
    
    audit_rows = []
    
    counts = {
        "v9_confirmado": 0,
        "v9_probable": 0,
        "v10_o_desconocido": 0
    }
    
    schemas = {
        "A": 0,
        "B": 0,
        "otro": 0
    }

    for f in cache_files:
        # Extract video_id from filename: {vid}_vision_analysis_parsimonious.json
        vid = f.name.replace("_vision_analysis_parsimonious.json", "")
        
        # Load raw json
        schema = "otro"
        prompt_version = ""
        try:
            with open(f, "r", encoding="utf-8") as jf:
                data = json.load(jf)
            if isinstance(data, dict):
                if "extracted_graph" in data:
                    schema = "B"
                elif all(k in data for k in ("step_by_step_reasoning", "graph", "nodes", "edges")):
                    schema = "A"
                prompt_version = data.get("prompt_version", "")
        except Exception:
            pass
            
        schemas[schema] += 1
        
        # Check lab workspace test_analysis.json
        lab_workspace_json = lab_dir / vid / "test_analysis.json"
        lab_json_exists = lab_workspace_json.exists()
        lab_json_matches = compare_json_contents(f, lab_workspace_json)
        
        # Check if v10 cache file exists
        v10_cache_exists = (raw_dir / f"{vid}_vision_analysis_parsimonious_v10.json").exists()
        
        # Check if graphml exists in data/graphs_parsimonious
        graphml_path = graphs_dir / f"{vid}.graphml"
        graphml_exists = graphml_path.exists()
        graphml_size = graphml_path.stat().st_size if graphml_exists else 0
        
        parse_success = False
        nodes_count = 0
        edges_count = 0
        unknown_services_count = 0
        unknown_services_list = []
        
        if graphml_exists:
            try:
                G = nx.read_graphml(str(graphml_path))
                parse_success = True
                nodes_count = G.number_of_nodes()
                edges_count = G.number_of_edges()
                
                for _, attrs in G.nodes(data=True):
                    svc = attrs.get("service", "")
                    if svc and svc not in valid_services:
                        unknown_services_count += 1
                        unknown_services_list.append(svc)
            except Exception:
                parse_success = False
                nodes_count = -1
                edges_count = -1
                
        # Determine verdict
        if schema == "B" and prompt_version == "v9":
            verdict = "v9_confirmado"
        elif schema == "A" and lab_json_matches:
            verdict = "v9_confirmado"
        elif schema == "A" and not v10_cache_exists:
            verdict = "v9_probable"
        else:
            verdict = "v10_o_desconocido"
            
        counts[verdict] += 1
        
        audit_rows.append({
            "video_id": vid,
            "schema": schema,
            "prompt_version": prompt_version,
            "lab_json_exists": int(lab_json_exists),
            "lab_json_matches": int(lab_json_matches),
            "v10_cache_exists": int(v10_cache_exists),
            "graphml_exists": int(graphml_exists),
            "graphml_size_bytes": graphml_size,
            "graphml_parses": int(parse_success),
            "graphml_nodes": nodes_count,
            "graphml_edges": edges_count,
            "unknown_services_count": unknown_services_count,
            "unknown_services_list": ", ".join(unknown_services_list),
            "verdict": verdict
        })
        
    # Write to CSV
    csv_out = reports_dir / "parsimonious_provenance.csv"
    with open(csv_out, "w", newline="", encoding="utf-8") as outf:
        fieldnames = [
            "video_id", "schema", "prompt_version", "lab_json_exists",
            "lab_json_matches", "v10_cache_exists", "graphml_exists",
            "graphml_size_bytes", "graphml_parses", "graphml_nodes",
            "graphml_edges", "unknown_services_count", "unknown_services_list",
            "verdict"
        ]
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(audit_rows)
        
    # Print Console Summary
    print("======================================================================")
    print(" AUDIT OF PARSIMONIOUS PROVENANCE SUMMARY")
    print("======================================================================")
    print(f"Total cache files scanned: {len(cache_files)}")
    print(f"Schemas: A={schemas['A']}, B={schemas['B']}, Other/Invalid={schemas['otro']}")
    print(f"Verdict counts:")
    print(f"  • v9_confirmado:     {counts['v9_confirmado']}")
    print(f"  • v9_probable:       {counts['v9_probable']}")
    print(f"  • v10_o_desconocido: {counts['v10_o_desconocido']}")
    print(f"Report written to: {csv_out}")
    print("======================================================================")

if __name__ == "__main__":
    main()
