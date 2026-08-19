#!/usr/bin/env python3
"""
evaluate_parsimonious.py — Dedicated evaluator for Parsimonious mode graphs.

Evaluates parsimonious graphs against Cloudscape Ground Truth and produces:
  - whiteboard_selection_lab/results_parsimonious.csv (one row per video)
  - whiteboard_selection_lab/info_parsimonious.json (aggregated metrics summary)

Usage:
    python scripts/evaluation/evaluate_parsimonious.py
    python scripts/evaluation/evaluate_parsimonious.py --graphs-dir data/graphs_parsimonious_v9
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog


def evaluate_parsimonious(
    graphs_dir: Path,
    gt_dir: Path,
    output_dir: Path
) -> dict:
    catalog_path = gt_dir / "services.csv"
    catalog = load_services_catalog(catalog_path)
    
    if not graphs_dir.exists():
        print(f"❌ Directoy not found: {graphs_dir}")
        return {}
        
    all_gen_files = sorted(graphs_dir.glob("*.graphml"))
    
    results = []
    svc_f1_list = []
    edge_f1_all_list = []
    edge_f1_scored_list = []
    zero_edge_gt_list = []
    failed_list = []
    
    for g_file in all_gen_files:
        vid = g_file.stem
        gt_file = gt_dir / f"{vid}.graphml"
        
        if not gt_file.exists():
            continue
            
        try:
            g_gen = nx.read_graphml(g_file)
            g_gt = nx.read_graphml(gt_file)
        except Exception as e:
            failed_list.append({"video_id": vid, "error": str(e)[:120]})
            continue
            
        pair_res = evaluate_pair(g_gen, g_gt, vid, catalog)
        
        is_zero_edge_gt = (g_gt.number_of_edges() == 0)
        if is_zero_edge_gt:
            zero_edge_gt_list.append(vid)
        else:
            edge_f1_scored_list.append(pair_res["edge_f1"])
            
        svc_f1_list.append(pair_res["svc_f1"])
        edge_f1_all_list.append(pair_res["edge_f1"])
        
        results.append({
            "video_id": vid,
            "title": pair_res.get("title", f"Video {vid}"),
            "category": pair_res.get("category", "Uncategorized"),
            "gen_nodes": g_gen.number_of_nodes(),
            "gt_nodes": g_gt.number_of_nodes(),
            "svc_precision": pair_res.get("svc_precision", 0.0),
            "svc_recall": pair_res.get("svc_recall", 0.0),
            "svc_f1": pair_res.get("svc_f1", 0.0),
            "gen_edges": g_gen.number_of_edges(),
            "gt_edges": g_gt.number_of_edges(),
            "edge_precision": pair_res.get("edge_precision", 0.0),
            "edge_recall": pair_res.get("edge_recall", 0.0),
            "edge_f1": pair_res.get("edge_f1", 0.0),
            "is_zero_edge_gt": is_zero_edge_gt
        })
        
    def mean(xs):
        return round(sum(xs) / len(xs), 4) if xs else 0.0
        
    mean_svc_f1 = mean(svc_f1_list)
    mean_edge_f1_all = mean(edge_f1_all_list)
    mean_edge_f1_scored = mean(edge_f1_scored_list)
    
    summary = {
        "mode": "parsimonious",
        "graphs_directory": str(graphs_dir),
        "total_evaluated": len(results),
        "failed_reads": len(failed_list),
        "mean_service_f1": mean_svc_f1,
        "mean_edge_f1_all": mean_edge_f1_all,
        "mean_edge_f1_excluding_zero_edge_gt": mean_edge_f1_scored,
        "zero_edge_gt_count": len(zero_edge_gt_list),
        "zero_edge_gt_videos": zero_edge_gt_list
    }
    
    # Save CSV
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "results_parsimonious.csv"
    fieldnames = [
        "video_id", "title", "category",
        "gen_nodes", "gt_nodes", "svc_precision", "svc_recall", "svc_f1",
        "gen_edges", "gt_edges", "edge_precision", "edge_recall", "edge_f1",
        "is_zero_edge_gt"
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    # Save JSON
    json_path = output_dir / "info_parsimonious.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print("======================================================================")
    print(" EVALUACIÓN DE MODO PARSIMONIOSO COMPLETADA EX ITOSAMENTE")
    print("======================================================================")
    print(f"Directorio de Grafos: {graphs_dir}")
    print(f"Total Evaluados: {len(results)}")
    print(f"Service F1 Medio: {mean_svc_f1 * 100:.2f}%")
    print(f"Edge F1 Medio (General): {mean_edge_f1_all * 100:.2f}%")
    print(f"Edge F1 Medio (Sin GT 0-Aristas): {mean_edge_f1_scored * 100:.2f}%")
    print(f"Archivos Generados:")
    print(f"  • CSV:  {csv_path}")
    print(f"  • JSON: {json_path}")
    print("======================================================================")
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="Evaluate parsimonious graphs against Ground Truth")
    parser.add_argument(
        "--graphs-dir", type=Path, default=PROJECT_ROOT / "data" / "graphs_parsimonious",
        help="Directory containing parsimonious .graphml files"
    )
    parser.add_argument(
        "--gt-dir", type=Path, default=PROJECT_ROOT / "data" / "cloudscape_gt",
        help="Directory containing ground truth .graphml files"
    )
    parser.add_argument(
        "--output-dir", type=Path, default=PROJECT_ROOT / "whiteboard_selection_lab",
        help="Directory to save results_parsimonious.csv and info_parsimonious.json"
    )
    args = parser.parse_args()
    evaluate_parsimonious(args.graphs_dir, args.gt_dir, args.output_dir)


if __name__ == "__main__":
    main()
