#!/usr/bin/env python3
"""
evaluate_parsimonious.py — Dedicated evaluator for Parsimonious mode graphs.

Evaluates parsimonious graphs against Cloudscape Ground Truth and produces:
  - whiteboard_selection_lab/results_parsimonious.csv (one row per video)
  - whiteboard_selection_lab/info_parsimonious.json (aggregated metrics summary)
  - reports/runs/<fecha>_parsimonious_v9/results.csv (run result copy)
  - reports/runs/<fecha>_parsimonious_v9/run.json (provenance, sha256 and metrics)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import hashlib
import subprocess
from datetime import date
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Fix Windows console encoding issues for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def get_prompt_v9_sha256() -> str:
    try:
        from scripts.core.vision_analyzer_parsimonious import CLOUDSCAPE_PROMPT_TEMPLATE
        return hashlib.sha256(CLOUDSCAPE_PROMPT_TEMPLATE.encode("utf-8")).hexdigest()
    except Exception:
        return "unknown"


def evaluate_parsimonious(
    graphs_dir: Path,
    gt_dir: Path,
    output_dir: Path
) -> dict:
    catalog_path = gt_dir / "services.csv"
    catalog = load_services_catalog(catalog_path)
    
    if not graphs_dir.exists():
        print(f"❌ Directory not found: {graphs_dir}")
        return {}
        
    all_gen_files = sorted(graphs_dir.glob("*.graphml"))
    
    results = []
    skipped_no_gt = []
    svc_f1_list = []
    edge_f1_all_list = []
    edge_f1_scored_list = []
    zero_edge_gt_list = []
    failed_list = []
    
    for g_file in all_gen_files:
        vid = g_file.stem
        gt_file = gt_dir / f"{vid}.graphml"
        
        if not gt_file.exists():
            skipped_no_gt.append(vid)
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
        
        # Format metrics as percentages (0.0 to 100.0)
        results.append({
            "video_id": vid,
            "title": g_gt.graph.get("name") or f"Video {vid}",
            "category": g_gt.graph.get("categories") or "Uncategorized",
            "gen_nodes": g_gen.number_of_nodes(),
            "gt_nodes": g_gt.number_of_nodes(),
            "svc_precision": round(100 * pair_res.get("svc_precision", 0.0), 2),
            "svc_recall": round(100 * pair_res.get("svc_recall", 0.0), 2),
            "svc_f1": round(100 * pair_res.get("svc_f1", 0.0), 2),
            "gen_edges": g_gen.number_of_edges(),
            "gt_edges": g_gt.number_of_edges(),
            "edge_precision": round(100 * pair_res.get("edge_precision", 0.0), 2),
            "edge_recall": round(100 * pair_res.get("edge_recall", 0.0), 2),
            "edge_f1": round(100 * pair_res.get("edge_f1", 0.0), 2),
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
        "skipped_no_gt_count": len(skipped_no_gt),
        "mean_service_f1": round(100 * mean_svc_f1, 2),
        "mean_edge_f1_all": round(100 * mean_edge_f1_all, 2),
        "mean_edge_f1_excluding_zero_edge_gt": round(100 * mean_edge_f1_scored, 2),
        "zero_edge_gt_count": len(zero_edge_gt_list),
        "zero_edge_gt_videos": zero_edge_gt_list,
        "skipped_no_gt_videos": skipped_no_gt
    }
    
    # Save CSV to legacy directory
    output_dir.mkdir(parents=True, exist_ok=True)
    legacy_csv_path = output_dir / "results_parsimonious.csv"
    fieldnames = [
        "video_id", "title", "category",
        "gen_nodes", "gt_nodes", "svc_precision", "svc_recall", "svc_f1",
        "gen_edges", "gt_edges", "edge_precision", "edge_recall", "edge_f1",
        "is_zero_edge_gt"
    ]
    with open(legacy_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
        
    # Save JSON to legacy directory
    legacy_json_path = output_dir / "info_parsimonious.json"
    with open(legacy_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    # Save run to reports directory
    today_str = date.today().isoformat()
    run_dir = PROJECT_ROOT / "reports" / "runs" / f"{today_str}_parsimonious_v9"
    run_dir.mkdir(parents=True, exist_ok=True)
    
    # Write results.csv run copy
    write_csv_path = run_dir / "results.csv"
    shutil_copy = True
    try:
        import shutil
        shutil.copy2(legacy_csv_path, write_csv_path)
    except Exception:
        with open(write_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
            
    # Write run.json meta file
    run_json_path = run_dir / "run.json"
    run_meta = {
        "generated_on": today_str,
        "mode": "parsimonious",
        "label": "v9",
        "pipeline": "1-stage parsimonious v9",
        "gemini_model": "gemini-3.6-flash",
        "git_commit": git_commit(),
        "inputs": {
            "graphs_dir": "data/graphs_parsimonious",
            "gt_dir": "data/cloudscape_gt"
        },
        "counts": {
            "evaluated": len(results),
            "scored_for_edges": len(results) - len(zero_edge_gt_list),
            "excluded_from_edges": len(zero_edge_gt_list),
            "unreadable": len(failed_list)
        },
        "exclusions": {
            "gt_has_zero_edges": zero_edge_gt_list,
            "skipped_no_gt": skipped_no_gt,
            "unreadable": failed_list
        },
        "prompt_v9_sha256": get_prompt_v9_sha256(),
        "metrics": {
            "service_f1": {
                "mean": round(100 * mean_svc_f1, 2)
            },
            "edge_f1": {
                "mean": round(100 * mean_edge_f1_scored, 2)
            },
            "edge_f1_legacy_including_zero_edge_gt": {
                "mean": round(100 * mean_edge_f1_all, 2)
            },
            # Parsimonious legacy compatibility
            "service_f1_mean": round(100 * mean_svc_f1, 2),
            "edge_f1_mean_all": round(100 * mean_edge_f1_all, 2),
            "edge_f1_mean_excluding_zero_edge_gt": round(100 * mean_edge_f1_scored, 2)
        }
    }
    with open(run_json_path, "w", encoding="utf-8") as f:
        json.dump(run_meta, f, indent=2, ensure_ascii=False)
        
    print("======================================================================")
    print(" EVALUACIÓN DE MODO PARSIMONIOSO COMPLETADA EXITOSAMENTE")
    print("======================================================================")
    print(f"Directorio de Grafos:                  {graphs_dir}")
    print(f"Total Evaluados:                       {len(results)}")
    print(f"Saltados por falta de Ground Truth:    {len(skipped_no_gt)}")
    print(f"Service F1 Medio:                      {mean_svc_f1 * 100:.2f}%")
    print(f"Edge F1 Medio (General):               {mean_edge_f1_all * 100:.2f}%")
    print(f"Edge F1 Medio (Sin GT 0-Aristas):      {mean_edge_f1_scored * 100:.2f}%")
    print(f"Archivos Generados:")
    print(f"  • Legacy CSV:   {legacy_csv_path}")
    print(f"  • Legacy JSON:  {legacy_json_path}")
    print(f"  • Run CSV:      {write_csv_path}")
    print(f"  • Run JSON:     {run_json_path}")
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
