#!/usr/bin/env python3
"""
evaluate_graphs.py — Comprehensive evaluation of generated architecture graphs
                     against Cloudscape ground truth (FAST25 dataset).

Compares 63 matched graph pairs and produces:
  - evaluation_report.md   (human-readable report)
  - evaluation_results.json (machine-readable full results)
  - evaluation_per_video.csv (one row per video)

Usage:
    python scripts/evaluate_graphs.py
    python scripts/evaluate_graphs.py --gen-dir data/graphs --gt-dir data/cloudscape_gt
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import networkx as nx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# ── Helpers ──────────────────────────────────────────────────────


def load_services_catalog(csv_path: Path) -> dict[str, dict]:
    """Load services.csv into a dict keyed by service name."""
    catalog = {}
    if not csv_path.exists():
        console.print(f"[yellow]⚠[/] services.csv not found at {csv_path}")
        return catalog
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                catalog[name] = {
                    "capability": row.get("capability", "").strip(),
                    "is_aws": row.get("is_aws", "").strip() == "True",
                    "schema": row.get("schema", "").strip(),
                    "aws_product_categories": row.get("aws_product_categories", "").strip(),
                }
    return catalog


def extract_service_multiset(G: nx.MultiDiGraph) -> list[str]:
    """Extract the list of services from a graph (with duplicates)."""
    return [attrs.get("service", "") for _, attrs in G.nodes(data=True)]


def extract_service_set(G: nx.MultiDiGraph) -> set[str]:
    """Extract unique services from a graph."""
    return {attrs.get("service", "") for _, attrs in G.nodes(data=True)}


def extract_edge_service_pairs(G: nx.MultiDiGraph) -> list[tuple[str, str, str]]:
    """
    Extract edges as (source_service, target_service, edge_type) tuples.
    This is ID-agnostic — we compare by service names.
    """
    pairs = []
    for src, tgt, attrs in G.edges(data=True):
        src_svc = G.nodes[src].get("service", "?")
        tgt_svc = G.nodes[tgt].get("service", "?")
        etype = attrs.get("type", "data")
        pairs.append((src_svc, tgt_svc, etype))
    return pairs


def extract_edge_service_pairs_no_type(G: nx.MultiDiGraph) -> list[tuple[str, str]]:
    """Extract edges as (source_service, target_service) tuples (ignoring type)."""
    pairs = []
    for src, tgt, _attrs in G.edges(data=True):
        src_svc = G.nodes[src].get("service", "?")
        tgt_svc = G.nodes[tgt].get("service", "?")
        pairs.append((src_svc, tgt_svc))
    return pairs


def count_workflows(G: nx.MultiDiGraph) -> int:
    """Count distinct flow_ids in the graph."""
    flow_ids = set()
    for _, _, attrs in G.edges(data=True):
        fid = attrs.get("flow_id", 0)
        flow_ids.add(fid)
    return len(flow_ids)


def get_categories(G: nx.MultiDiGraph) -> list[str]:
    """Extract functional goal categories from graph metadata."""
    cats = G.graph.get("categories", "")
    if isinstance(cats, str):
        return [c.strip() for c in cats.split(",") if c.strip()]
    return []


def multiset_precision_recall(gen_list: list, gt_list: list) -> tuple[float, float, float]:
    """
    Compute precision, recall, and F1 using multiset (Counter) intersection.
    This correctly handles duplicate services (e.g., 2 Lambdas).
    """
    gen_counter = Counter(gen_list)
    gt_counter = Counter(gt_list)

    # Multiset intersection: min of counts
    intersection = sum((gen_counter & gt_counter).values())

    precision = intersection / sum(gen_counter.values()) if gen_counter else 0.0
    recall = intersection / sum(gt_counter.values()) if gt_counter else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


def set_precision_recall(gen_set: set, gt_set: set) -> tuple[float, float, float]:
    """Compute precision, recall, F1 using set intersection (unique services)."""
    intersection = gen_set & gt_set
    precision = len(intersection) / len(gen_set) if gen_set else 0.0
    recall = len(intersection) / len(gt_set) if gt_set else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def edge_multiset_precision_recall(
    gen_pairs: list[tuple[str, str]],
    gt_pairs: list[tuple[str, str]],
) -> tuple[float, float, float]:
    """Compute precision/recall/F1 for edges using multiset matching on (src_svc, tgt_svc)."""
    gen_counter = Counter(gen_pairs)
    gt_counter = Counter(gt_pairs)

    intersection = sum((gen_counter & gt_counter).values())

    precision = intersection / sum(gen_counter.values()) if gen_counter else 0.0
    recall = intersection / sum(gt_counter.values()) if gt_counter else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1


# ── Per-video evaluation ─────────────────────────────────────────


def evaluate_pair(
    gen_graph: nx.MultiDiGraph,
    gt_graph: nx.MultiDiGraph,
    video_id: str,
    catalog: dict[str, dict],
) -> dict[str, Any]:
    """Evaluate a single generated graph against its ground truth."""

    # --- Services (unique set) ---
    gen_svc_set = extract_service_set(gen_graph)
    gt_svc_set = extract_service_set(gt_graph)
    svc_prec, svc_rec, svc_f1 = set_precision_recall(gen_svc_set, gt_svc_set)

    # --- Services (multiset — handles duplicate instances) ---
    gen_svc_list = extract_service_multiset(gen_graph)
    gt_svc_list = extract_service_multiset(gt_graph)
    ms_prec, ms_rec, ms_f1 = multiset_precision_recall(gen_svc_list, gt_svc_list)

    # --- Edges (by service pair, ignoring type) ---
    gen_edge_pairs = extract_edge_service_pairs_no_type(gen_graph)
    gt_edge_pairs = extract_edge_service_pairs_no_type(gt_graph)
    edge_prec, edge_rec, edge_f1 = edge_multiset_precision_recall(gen_edge_pairs, gt_edge_pairs)

    # --- Edge type accuracy ---
    gen_typed = extract_edge_service_pairs(gen_graph)
    gt_typed = extract_edge_service_pairs(gt_graph)
    gen_typed_counter = Counter(gen_typed)
    gt_typed_counter = Counter(gt_typed)
    typed_intersection = sum((gen_typed_counter & gt_typed_counter).values())
    # Among edges that match on (src, tgt), how many also match on type?
    untyped_intersection = sum((Counter(gen_edge_pairs) & Counter(gt_edge_pairs)).values())
    edge_type_accuracy = typed_intersection / untyped_intersection if untyped_intersection > 0 else 0.0

    # --- Workflows ---
    gen_flows = count_workflows(gen_graph)
    gt_flows = count_workflows(gt_graph)

    # --- Missing and hallucinated services ---
    services_missing = sorted(gt_svc_set - gen_svc_set)
    services_hallucinated = sorted(gen_svc_set - gt_svc_set)
    services_correct = sorted(gen_svc_set & gt_svc_set)

    # --- Missing and hallucinated edges ---
    gen_edge_counter = Counter(gen_edge_pairs)
    gt_edge_counter = Counter(gt_edge_pairs)
    edges_only_gen = dict(gen_edge_counter - gt_edge_counter)
    edges_only_gt = dict(gt_edge_counter - gen_edge_counter)

    # --- Capability breakdown ---
    capability_breakdown = {}
    for svc in gt_svc_set:
        cap = catalog.get(svc, {}).get("capability", "unknown")
        if cap not in capability_breakdown:
            capability_breakdown[cap] = {"gt": 0, "correct": 0, "missed": 0}
        capability_breakdown[cap]["gt"] += 1
        if svc in gen_svc_set:
            capability_breakdown[cap]["correct"] += 1
        else:
            capability_breakdown[cap]["missed"] += 1

    # Count hallucinated by capability
    for svc in services_hallucinated:
        cap = catalog.get(svc, {}).get("capability", "unknown")
        if cap not in capability_breakdown:
            capability_breakdown[cap] = {"gt": 0, "correct": 0, "missed": 0}
        capability_breakdown[cap].setdefault("hallucinated", 0)
        capability_breakdown[cap]["hallucinated"] = capability_breakdown[cap].get("hallucinated", 0) + 1

    # --- Categories ---
    categories = get_categories(gt_graph)

    return {
        "video_id": video_id,
        "gen_name": gen_graph.graph.get("name", ""),
        "gt_name": gt_graph.graph.get("name", ""),
        "categories": categories,
        # Node counts
        "gen_nodes": gen_graph.number_of_nodes(),
        "gt_nodes": gt_graph.number_of_nodes(),
        "node_count_ratio": gen_graph.number_of_nodes() / gt_graph.number_of_nodes() if gt_graph.number_of_nodes() > 0 else 0,
        # Service metrics (unique set)
        "svc_precision": svc_prec,
        "svc_recall": svc_rec,
        "svc_f1": svc_f1,
        # Service metrics (multiset)
        "ms_precision": ms_prec,
        "ms_recall": ms_rec,
        "ms_f1": ms_f1,
        # Edge metrics
        "gen_edges": gen_graph.number_of_edges(),
        "gt_edges": gt_graph.number_of_edges(),
        "edge_precision": edge_prec,
        "edge_recall": edge_rec,
        "edge_f1": edge_f1,
        "edge_type_accuracy": edge_type_accuracy,
        # Workflows
        "gen_workflows": gen_flows,
        "gt_workflows": gt_flows,
        # Error details
        "services_correct": services_correct,
        "services_missing": services_missing,
        "services_hallucinated": services_hallucinated,
        "edges_only_gen": {f"{k[0]}→{k[1]}": v for k, v in edges_only_gen.items()},
        "edges_only_gt": {f"{k[0]}→{k[1]}": v for k, v in edges_only_gt.items()},
        # Capability breakdown
        "capability_breakdown": capability_breakdown,
    }


# ── Aggregation ──────────────────────────────────────────────────


def aggregate_results(results: list[dict], catalog: dict[str, dict]) -> dict[str, Any]:
    """Compute aggregate statistics across all evaluated videos."""
    if not results:
        return {}

    # Only aggregate usable graphs for core metrics!
    usable_results = [r for r in results if r.get("graph_usable", True)]
    n = len(usable_results)
    if n == 0:
        # Fallback to all if somehow none are marked usable to avoid division by zero
        usable_results = results
        n = len(usable_results)

    # --- Averages ---
    avg = lambda key: sum(r[key] for r in usable_results) / n

    # --- Most missed/hallucinated services ---
    all_missing = Counter()
    all_hallucinated = Counter()
    all_correct = Counter()
    for r in usable_results:
        all_missing.update(r["services_missing"])
        all_hallucinated.update(r["services_hallucinated"])
        all_correct.update(r["services_correct"])

    # --- Missed/hallucinated edges ---
    all_edges_missing = Counter()
    all_edges_hallucinated = Counter()
    for r in usable_results:
        for edge_str, count in r["edges_only_gt"].items():
            all_edges_missing[edge_str] += count
        for edge_str, count in r["edges_only_gen"].items():
            all_edges_hallucinated[edge_str] += count

    # --- Capability aggregation ---
    cap_agg = defaultdict(lambda: {"gt": 0, "correct": 0, "missed": 0, "hallucinated": 0})
    for r in usable_results:
        for cap, vals in r["capability_breakdown"].items():
            cap_agg[cap]["gt"] += vals.get("gt", 0)
            cap_agg[cap]["correct"] += vals.get("correct", 0)
            cap_agg[cap]["missed"] += vals.get("missed", 0)
            cap_agg[cap]["hallucinated"] += vals.get("hallucinated", 0)

    # --- Category aggregation ---
    cat_metrics = defaultdict(lambda: {"count": 0, "svc_f1_sum": 0, "edge_f1_sum": 0})
    for r in usable_results:
        for cat in r["categories"]:
            cat_metrics[cat]["count"] += 1
            cat_metrics[cat]["svc_f1_sum"] += r["svc_f1"]
            cat_metrics[cat]["edge_f1_sum"] += r["edge_f1"]

    cat_averages = {}
    for cat, vals in cat_metrics.items():
        c = vals["count"]
        cat_averages[cat] = {
            "count": c,
            "avg_svc_f1": vals["svc_f1_sum"] / c if c > 0 else 0,
            "avg_edge_f1": vals["edge_f1_sum"] / c if c > 0 else 0,
        }

    # --- Score distribution buckets ---
    f1_buckets = {"excellent_90+": 0, "good_70_90": 0, "fair_50_70": 0, "poor_<50": 0}
    for r in usable_results:
        f1 = r["svc_f1"] * 100
        if f1 >= 90:
            f1_buckets["excellent_90+"] += 1
        elif f1 >= 70:
            f1_buckets["good_70_90"] += 1
        elif f1 >= 50:
            f1_buckets["fair_50_70"] += 1
        else:
            f1_buckets["poor_<50"] += 1

    return {
        "total_evaluated": len(results),
        "total_usable": n,
        "total_excluded": len(results) - n,
        # Service averages
        "avg_svc_precision": avg("svc_precision"),
        "avg_svc_recall": avg("svc_recall"),
        "avg_svc_f1": avg("svc_f1"),
        "avg_ms_precision": avg("ms_precision"),
        "avg_ms_recall": avg("ms_recall"),
        "avg_ms_f1": avg("ms_f1"),
        # Edge averages
        "avg_edge_precision": avg("edge_precision"),
        "avg_edge_recall": avg("edge_recall"),
        "avg_edge_f1": avg("edge_f1"),
        "avg_edge_type_accuracy": avg("edge_type_accuracy"),
        # Node/edge counts
        "avg_node_count_ratio": avg("node_count_ratio"),
        "avg_gen_nodes": avg("gen_nodes"),
        "avg_gt_nodes": avg("gt_nodes"),
        "avg_gen_edges": avg("gen_edges"),
        "avg_gt_edges": avg("gt_edges"),
        "avg_gen_workflows": avg("gen_workflows"),
        "avg_gt_workflows": avg("gt_workflows"),
        # Error rankings
        "top_missing_services": all_missing.most_common(20),
        "top_hallucinated_services": all_hallucinated.most_common(20),
        "top_correct_services": all_correct.most_common(20),
        "top_missing_edges": all_edges_missing.most_common(20),
        "top_hallucinated_edges": all_edges_hallucinated.most_common(20),
        # Capability breakdown
        "capability_breakdown": dict(cap_agg),
        # Category breakdown
        "category_breakdown": cat_averages,
        # Score distribution
        "f1_distribution": f1_buckets,
    }


# ── Report generation ────────────────────────────────────────────


def generate_markdown_report(
    results: list[dict],
    agg: dict[str, Any],
    output_path: Path,
    catalog: dict[str, dict] | None = None,
) -> None:
    """Generate a comprehensive markdown evaluation report."""
    lines = []
    lines.append("# Evaluation Report: Generated Graphs vs Cloudscape Ground Truth\n")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # ── 1. Executive Summary ──
    lines.append("## 1. Executive Summary\n")
    lines.append(f"**Videos evaluated:** {agg['total_evaluated']}\n")
    lines.append("| Metric | Precision | Recall | F1 |")
    lines.append("|--------|-----------|--------|----|")
    lines.append(f"| **Services (unique set)** | {agg['avg_svc_precision']:.1%} | {agg['avg_svc_recall']:.1%} | {agg['avg_svc_f1']:.1%} |")
    lines.append(f"| **Services (multiset)** | {agg['avg_ms_precision']:.1%} | {agg['avg_ms_recall']:.1%} | {agg['avg_ms_f1']:.1%} |")
    lines.append(f"| **Edges (service pairs)** | {agg['avg_edge_precision']:.1%} | {agg['avg_edge_recall']:.1%} | {agg['avg_edge_f1']:.1%} |")
    lines.append("")
    lines.append(f"**Edge type accuracy (data/meta):** {agg['avg_edge_type_accuracy']:.1%}\n")
    lines.append(f"**Average node count ratio (gen/gt):** {agg['avg_node_count_ratio']:.2f}x\n")
    lines.append(f"**Average workflows:** gen={agg['avg_gen_workflows']:.1f} vs gt={agg['avg_gt_workflows']:.1f}\n")

    # ── 2. Score Distribution ──
    lines.append("## 2. Service F1 Score Distribution\n")
    dist = agg["f1_distribution"]
    total = agg["total_evaluated"]
    lines.append("| Range | Count | Percentage |")
    lines.append("|-------|-------|------------|")
    lines.append(f"| 🟢 Excellent (≥90%) | {dist['excellent_90+']} | {dist['excellent_90+']/total:.1%} |")
    lines.append(f"| 🟡 Good (70-89%) | {dist['good_70_90']} | {dist['good_70_90']/total:.1%} |")
    lines.append(f"| 🟠 Fair (50-69%) | {dist['fair_50_70']} | {dist['fair_50_70']/total:.1%} |")
    lines.append(f"| 🔴 Poor (<50%) | {dist['poor_<50']} | {dist['poor_<50']/total:.1%} |")
    lines.append("")

    # ── 3. Per-video detail table ──
    lines.append("## 3. Per-Video Results (sorted by Service F1)\n")
    
    usable_results = [r for r in results if r.get("graph_usable", True)]
    unusable_results = [r for r in results if not r.get("graph_usable", True)]

    lines.append("### Core Evaluation (Valid Ground Truths)\n")
    lines.append("| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |")
    lines.append("|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|")
    for idx, r in enumerate(sorted(usable_results, key=lambda x: x["svc_f1"], reverse=True), 1):
        missing_str = ", ".join(r["services_missing"][:3])
        if len(r["services_missing"]) > 3:
            missing_str += f" (+{len(r['services_missing'])-3})"
        halluc_str = ", ".join(r["services_hallucinated"][:3])
        if len(r["services_hallucinated"]) > 3:
            halluc_str += f" (+{len(r['services_hallucinated'])-3})"

        lines.append(
            f"| {idx} | `{r['video_id']}` | {r['svc_precision']:.0%} | {r['svc_recall']:.0%} | {r['svc_f1']:.0%} "
            f"| {r['edge_precision']:.0%} | {r['edge_recall']:.0%} | {r['edge_f1']:.0%} "
            f"| {r['gen_nodes']} | {r['gt_nodes']} | {r['gen_edges']} | {r['gt_edges']} "
            f"| {missing_str or '—'} | {halluc_str or '—'} |"
        )
    lines.append("")

    if unusable_results:
        lines.append("### Excluded Validation (Invalid/Placeholder Ground Truths)\n")
        lines.append("> [!NOTE]\n")
        lines.append("> These graphs are excluded from the main average F1 calculations above.\n")
        lines.append("| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |")
        lines.append("|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|")
        for idx, r in enumerate(sorted(unusable_results, key=lambda x: x["svc_f1"], reverse=True), 1):
            missing_str = ", ".join(r["services_missing"][:3])
            if len(r["services_missing"]) > 3:
                missing_str += f" (+{len(r['services_missing'])-3})"
            halluc_str = ", ".join(r["services_hallucinated"][:3])
            if len(r["services_hallucinated"]) > 3:
                halluc_str += f" (+{len(r['services_hallucinated'])-3})"

            lines.append(
                f"| {idx} | `{r['video_id']}` | {r['svc_precision']:.0%} | {r['svc_recall']:.0%} | {r['svc_f1']:.0%} "
                f"| {r['edge_precision']:.0%} | {r['edge_recall']:.0%} | {r['edge_f1']:.0%} "
                f"| {r['gen_nodes']} | {r['gt_nodes']} | {r['gen_edges']} | {r['gt_edges']} "
                f"| {missing_str or '—'} | {halluc_str or '—'} |"
            )
        lines.append("")

    # ── 4. Most missed services ──
    lines.append("## 4. Most Frequently Missing Services (False Negatives)\n")
    lines.append("Services present in ground truth but NOT in generated graphs.\n")
    lines.append("| Service | Times Missed | Capability |")
    lines.append("|---------|-------------|------------|")
    for svc, count in agg["top_missing_services"]:
        cap = catalog.get(svc, {}).get("capability", "?")
        lines.append(f"| {svc} | {count} | {cap} |")
    lines.append("")

    # ── 5. Most hallucinated services ──
    lines.append("## 5. Most Frequently Hallucinated Services (False Positives)\n")
    lines.append("Services in generated graphs but NOT in ground truth.\n")
    lines.append("| Service | Times Hallucinated | Capability |")
    lines.append("|---------|-------------------|------------|")
    for svc, count in agg["top_hallucinated_services"]:
        cap = catalog.get(svc, {}).get("capability", "?")
        lines.append(f"| {svc} | {count} | {cap} |")
    lines.append("")

    # ── 6. Most missed edges ──
    lines.append("## 6. Most Frequently Missing Edges\n")
    lines.append("| Edge (src → tgt) | Times Missed |")
    lines.append("|------------------|-------------|")
    for edge_str, count in agg["top_missing_edges"][:15]:
        lines.append(f"| {edge_str} | {count} |")
    lines.append("")

    # ── 7. Most hallucinated edges ──
    lines.append("## 7. Most Frequently Hallucinated Edges\n")
    lines.append("| Edge (src → tgt) | Times Hallucinated |")
    lines.append("|------------------|--------------------|")
    for edge_str, count in agg["top_hallucinated_edges"][:15]:
        lines.append(f"| {edge_str} | {count} |")
    lines.append("")

    # ── 8. Capability breakdown ──
    lines.append("## 8. Performance by Service Capability\n")
    lines.append("| Capability | GT Count | Correct | Missed | Hallucinated | Recall |")
    lines.append("|------------|----------|---------|--------|--------------|--------|")
    for cap in sorted(agg["capability_breakdown"].keys()):
        vals = agg["capability_breakdown"][cap]
        gt = vals["gt"]
        correct = vals["correct"]
        missed = vals["missed"]
        halluc = vals.get("hallucinated", 0)
        recall = correct / gt if gt > 0 else 0
        lines.append(f"| {cap} | {gt} | {correct} | {missed} | {halluc} | {recall:.1%} |")
    lines.append("")

    # ── 9. Category breakdown ──
    lines.append("## 9. Performance by Functional Goal Category\n")
    lines.append("| Category | # Videos | Avg Svc F1 | Avg Edge F1 |")
    lines.append("|----------|----------|------------|-------------|")
    for cat in sorted(agg["category_breakdown"].keys()):
        vals = agg["category_breakdown"][cat]
        lines.append(f"| {cat} | {vals['count']} | {vals['avg_svc_f1']:.1%} | {vals['avg_edge_f1']:.1%} |")
    lines.append("")

    # ── 10. Bottom 10 (worst performing) ──
    lines.append("## 10. Bottom 10 Worst Performing Videos\n")
    bottom10 = sorted_results[-10:][::-1]
    for r in bottom10:
        lines.append(f"### `{r['video_id']}` — Svc F1: {r['svc_f1']:.0%}, Edge F1: {r['edge_f1']:.0%}\n")
        lines.append(f"- **Title (GT):** {r['gt_name']}")
        lines.append(f"- **Nodes:** gen={r['gen_nodes']} vs gt={r['gt_nodes']}")
        lines.append(f"- **Edges:** gen={r['gen_edges']} vs gt={r['gt_edges']}")
        if r["services_missing"]:
            lines.append(f"- **Missing services:** {', '.join(r['services_missing'])}")
        if r["services_hallucinated"]:
            lines.append(f"- **Hallucinated services:** {', '.join(r['services_hallucinated'])}")
        if r["edges_only_gt"]:
            missing_edges = list(r["edges_only_gt"].keys())[:5]
            lines.append(f"- **Missing edges:** {', '.join(missing_edges)}")
        if r["edges_only_gen"]:
            halluc_edges = list(r["edges_only_gen"].keys())[:5]
            lines.append(f"- **Hallucinated edges:** {', '.join(halluc_edges)}")
        lines.append("")

    # Write
    output_path.write_text("\n".join(lines), encoding="utf-8")
    console.print(f"[green]✓[/] Report saved → [bold]{output_path}[/]")


def generate_csv(all_evals: dict[str, dict[str, Any]], output_path: Path) -> None:
    """Generate a combined CSV from all evaluated runs."""
    fieldnames = [
        "run_type", "video_id", "gt_name", "categories",
        "gen_nodes", "gt_nodes", "node_count_ratio",
        "svc_precision", "svc_recall", "svc_f1",
        "ms_precision", "ms_recall", "ms_f1",
        "gen_edges", "gt_edges",
        "edge_precision", "edge_recall", "edge_f1",
        "edge_type_accuracy",
        "gen_workflows", "gt_workflows",
        "services_missing", "services_hallucinated",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for label, eval_data in all_evals.items():
            results = eval_data["results"]
            for r in sorted(results, key=lambda x: x["svc_f1"], reverse=True):
                row = {k: r.get(k, "") for k in fieldnames}
                row["run_type"] = label
                row["categories"] = ",".join(r.get("categories", []))
                row["services_missing"] = ",".join(r.get("services_missing", []))
                row["services_hallucinated"] = ",".join(r.get("services_hallucinated", []))
                # Format floats
                for k in ["svc_precision", "svc_recall", "svc_f1", "ms_precision", "ms_recall", "ms_f1",
                           "edge_precision", "edge_recall", "edge_f1", "edge_type_accuracy", "node_count_ratio"]:
                    if k in row and isinstance(row[k], float):
                        row[k] = f"{row[k]:.4f}"
                writer.writerow(row)

    console.print(f"[green]✓[/] CSV saved → [bold]{output_path}[/]")


# ── Main ─────────────────────────────────────────────────────────


def get_copied_video_ids() -> set[str]:
    """Identify videos whose vision cache was copied from Ground Truth."""
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


def evaluate_dir_helper(gen_dir: Path, gt_dir: Path, catalog: dict) -> list[dict]:
    """Evaluate all matching graph pairs in a single directory."""
    gen_files = {f.stem: f for f in gen_dir.glob("*.graphml")}
    gt_files = {f.stem: f for f in gt_dir.glob("*.graphml")}
    matching_ids = sorted(set(gen_files.keys()) & set(gt_files.keys()))
    results = []
    for vid in matching_ids:
        try:
            gen_g = nx.read_graphml(str(gen_files[vid]))
            gt_g = nx.read_graphml(str(gt_files[vid]))
            result = evaluate_pair(gen_g, gt_g, vid, catalog)
            
            # Extract and inject usability status from GT
            usable = gt_g.graph.get("graph_usable", True)
            if usable is False or str(usable).lower() == "false":
                result["graph_usable"] = False
            else:
                result["graph_usable"] = True
                
            results.append(result)
        except Exception as e:
            console.print(f"  [red]✗[/] Error evaluating {vid} in {gen_dir.name}: {e}")
    return results


def print_summary_table(agg: dict[str, Any], title: str) -> None:
    """Print an evaluation summary table to the console."""
    summary_table = Table(title=title, border_style="cyan", show_lines=True)
    summary_table.add_column("Metric", style="bold")
    summary_table.add_column("Value", style="green")
    summary_table.add_row("Videos Evaluated", f"{agg['total_evaluated']} (Core: {agg.get('total_usable', 0)}, Excluded: {agg.get('total_excluded', 0)})")
    summary_table.add_row("Avg Service F1 (unique)", f"{agg['avg_svc_f1']:.1%}")
    summary_table.add_row("Avg Service F1 (multiset)", f"{agg['avg_ms_f1']:.1%}")
    summary_table.add_row("Avg Edge F1", f"{agg['avg_edge_f1']:.1%}")
    summary_table.add_row("Avg Edge Type Accuracy", f"{agg['avg_edge_type_accuracy']:.1%}")
    summary_table.add_row("Avg Node Ratio (gen/gt)", f"{agg['avg_node_count_ratio']:.2f}x")
    console.print(summary_table)


def save_json_results(results: list[dict], agg: dict[str, Any], json_path: Path) -> None:
    """Save evaluation results to a JSON file."""
    json_output = {
        "generated_at": datetime.now().isoformat(),
        "summary": {k: v for k, v in agg.items() if not k.startswith("top_")},
        "top_missing_services": agg.get("top_missing_services", []),
        "top_hallucinated_services": agg.get("top_hallucinated_services", []),
        "per_video": results,
    }
    json_path.write_text(
        json.dumps(json_output, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    console.print(f"[green]✓[/] JSON saved → [bold]{json_path}[/]")


def compute_fleiss_kappa_score(
    gt_dir: Path,
    std_dir: Path,
    pars_dir: Path,
    catalog: dict[str, dict]
) -> tuple[float, int] | None:
    """Calculate Fleiss's Kappa over the triple intersection of videos."""
    if not gt_dir.exists() or not std_dir.exists() or not pars_dir.exists():
        return None
        
    vids = sorted(
        set(f.stem for f in gt_dir.glob("*.graphml")) &
        set(f.stem for f in std_dir.glob("*.graphml")) &
        set(f.stem for f in pars_dir.glob("*.graphml"))
    )
    
    # Filter out unusable graphs
    filtered_vids = []
    for vid in vids:
        try:
            g_path = gt_dir / f"{vid}.graphml"
            g = nx.read_graphml(str(g_path))
            usable = g.graph.get("graph_usable", True)
            if usable is not False and str(usable).lower() != "false":
                filtered_vids.append(vid)
        except Exception:
            pass
    vids = filtered_vids
    
    if not vids:
        return None
        
    def get_services(folder: Path, video_id: str) -> set[str]:
        path = folder / f"{video_id}.graphml"
        if not path.exists():
            return set()
        try:
            g = nx.read_graphml(str(path))
            return {g.nodes[n].get("service") for n in g.nodes() if g.nodes[n].get("service")}
        except Exception:
            return set()
            
    matrix = []
    service_names = sorted(list(catalog.keys()))
    
    for vid in vids:
        gt = get_services(gt_dir, vid)
        std = get_services(std_dir, vid)
        pars = get_services(pars_dir, vid)
        
        for s in service_names:
            ratings = [0, 0]  # [Absent, Present]
            for annotator in [gt, std, pars]:
                if s in annotator:
                    ratings[1] += 1
                else:
                    ratings[0] += 1
            matrix.append(ratings)
            
    N = len(matrix)
    if N == 0:
        return 0.0, 0
    m = sum(matrix[0])
    k = len(matrix[0])
    
    p = [0.0] * k
    for j in range(k):
        p[j] = sum(row[j] for row in matrix) / (N * m)
        
    P = [0.0] * N
    for i in range(N):
        numerator = sum(matrix[i][j]**2 for j in range(k)) - m
        P[i] = numerator / (m * (m - 1))
        
    P_mean = sum(P) / N
    Pe = sum(pj**2 for pj in p)
    
    if Pe >= 1.0:
        kappa = 1.0
    else:
        kappa = (P_mean - Pe) / (1.0 - Pe)
        
    return kappa, len(vids)


def generate_combined_markdown_report(
    all_evals: dict[str, dict[str, Any]],
    output_path: Path,
    catalog: dict[str, dict],
    copied_ids: set[str],
) -> None:
    """Generate a combined multi-section markdown evaluation report."""
    lines = []
    lines.append("# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth\n")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # ── 1. Executive Summary ──
    lines.append("## 1. Executive Summary (Side-by-Side Comparison)\n")
    lines.append("This table compares performance metrics across all generated graph directories.\n")
    lines.append("| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |")
    lines.append("|---|---|---|---|---|---|---|")
    for label, eval_data in all_evals.items():
        agg = eval_data["agg"]
        lines.append(
            f"| **{label}** | {agg['total_evaluated']} | {agg['avg_svc_f1']:.1%} | {agg['avg_ms_f1']:.1%} | "
            f"{agg['avg_edge_f1']:.1%} | {agg['avg_edge_type_accuracy']:.1%} | {agg['avg_node_count_ratio']:.2f}x |"
        )
    lines.append("")

    # Calculate and insert Fleiss's Kappa
    gt_dir = Path("data/cloudscape_gt")
    std_dir = Path("data/graphs")
    pars_dir = Path("data/graphs_parsimonious")
    kappa_res = compute_fleiss_kappa_score(gt_dir, std_dir, pars_dir, catalog)
    if kappa_res:
        kappa, num_vids = kappa_res
        if kappa > 0.80:
            interpretation = "Acuerdo casi perfecto (Altamente confiable)"
        elif kappa > 0.60:
            interpretation = "Acuerdo sustancial"
        elif kappa > 0.40:
            interpretation = "Acuerdo moderado"
        else:
            interpretation = "Acuerdo débil o pobre"
            
        lines.append("### Fleiss's Kappa Inter-Rater Reliability\n")
        lines.append(f"Fleiss's Kappa measures agreement among 3 raters (Ground Truth, Standard, and Parsimonious) ")
        lines.append(f"across all {num_vids} shared videos and {len(catalog)} services:\n")
        lines.append(f"- **Fleiss's Kappa (K):** `{kappa:.4f}`\n")
        lines.append(f"- **Interpretation:** {interpretation}\n")

    lines.append("\n---\n")

    # ── 2. Detailed Performance by Directory ──
    for label, eval_data in all_evals.items():
        lines.append(f"## {label} Evaluation Details\n")

        path = eval_data["path"]
        results = eval_data["results"]
        agg = eval_data["agg"]

        is_parsimonious = "parsimonious" in path.name

        if is_parsimonious and copied_ids:
            copied_in_run = [r for r in results if r["video_id"] in copied_ids]
            genuine_in_run = [r for r in results if r["video_id"] not in copied_ids]

            lines.append("> [!WARNING]")
            lines.append("> **Ground Truth Copied/Mocked Graphs Identified!**")
            lines.append(f"> Out of **{len(results)}** evaluated videos in this folder, **{len(copied_in_run)}** were compiled from Ground Truth cache files generated by `bulk_process_good_whiteboards.py` (which directly copy GT node and edge structures into the vision cache).")
            lines.append("> This explains why their Service F1 and Edge F1 scores are **100%**.")
            lines.append(f"> Only **{len(genuine_in_run)}** videos were genuinely analyzed and processed by the Gemini Vision LLM.")
            lines.append("")

            if genuine_in_run:
                gen_agg = aggregate_results(genuine_in_run, catalog)
                lines.append("### Genuine LLM Performance (Excluding Copied Ground Truths)\n")
                lines.append(f"Evaluating ONLY the **{len(genuine_in_run)}** genuine LLM-processed videos in this directory:\n")
                lines.append("| Metric | Precision | Recall | F1 |")
                lines.append("|---|---|---|---|")
                lines.append(f"| **Services (unique set)** | {gen_agg['avg_svc_precision']:.1%} | {gen_agg['avg_svc_recall']:.1%} | {gen_agg['avg_svc_f1']:.1%} |")
                lines.append(f"| **Services (multiset)** | {gen_agg['avg_ms_precision']:.1%} | {gen_agg['avg_ms_recall']:.1%} | {gen_agg['avg_ms_f1']:.1%} |")
                lines.append(f"| **Edges (service pairs)** | {gen_agg['avg_edge_precision']:.1%} | {gen_agg['avg_edge_recall']:.1%} | {gen_agg['avg_edge_f1']:.1%} |")
                lines.append("")
                lines.append(f"- **Edge type accuracy (data/meta):** {gen_agg['avg_edge_type_accuracy']:.1%}\n")
                lines.append(f"- **Average node count ratio (gen/gt):** {gen_agg['avg_node_count_ratio']:.2f}x\n")

            lines.append("### List of Copied Ground Truth Videos (Identified for Removal)\n")
            lines.append("These videos were generated from Ground Truth and have artificial 100% scores:\n")
            lines.append(", ".join([f"`{r['video_id']}`" for r in sorted(copied_in_run, key=lambda x: x["video_id"])]))
            lines.append("\n")

            table_results = genuine_in_run if genuine_in_run else results
            lines.append("### Detailed Results Table (Sorted by Service F1, showing Genuine only)\n")
        else:
            table_results = results
            lines.append("### Detailed Results Table (Sorted by Service F1)\n")

        usable_results = [r for r in table_results if r.get("graph_usable", True)]
        unusable_results = [r for r in table_results if not r.get("graph_usable", True)]

        lines.append("### Detailed Results Table: Core Evaluation (Valid Ground Truths)\n")
        lines.append("| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |")
        lines.append("|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|")
        for idx, r in enumerate(sorted(usable_results, key=lambda x: x["svc_f1"], reverse=True), 1):
            missing_str = ", ".join(r["services_missing"][:3])
            if len(r["services_missing"]) > 3:
                missing_str += f" (+{len(r['services_missing'])-3})"
            halluc_str = ", ".join(r["services_hallucinated"][:3])
            if len(r["services_hallucinated"]) > 3:
                halluc_str += f" (+{len(r['services_hallucinated'])-3})"

            lines.append(
                f"| {idx} | `{r['video_id']}` | {r['svc_precision']:.0%} | {r['svc_recall']:.0%} | {r['svc_f1']:.0%} "
                f"| {r['edge_precision']:.0%} | {r['edge_recall']:.0%} | {r['edge_f1']:.0%} "
                f"| {r['gen_nodes']} | {r['gt_nodes']} | {r['gen_edges']} | {r['gt_edges']} "
                f"| {missing_str or '—'} | {halluc_str or '—'} |"
            )
        lines.append("\n")

        if unusable_results:
            lines.append("### Detailed Results Table: Excluded Validation (Invalid/Placeholder Ground Truths)\n")
            lines.append("> [!NOTE]\n")
            lines.append("> These graphs are excluded from the main average F1 calculations above.\n")
            lines.append("| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |")
            lines.append("|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|")
            for idx, r in enumerate(sorted(unusable_results, key=lambda x: x["svc_f1"], reverse=True), 1):
                missing_str = ", ".join(r["services_missing"][:3])
                if len(r["services_missing"]) > 3:
                    missing_str += f" (+{len(r['services_missing'])-3})"
                halluc_str = ", ".join(r["services_hallucinated"][:3])
                if len(r["services_hallucinated"]) > 3:
                    halluc_str += f" (+{len(r['services_hallucinated'])-3})"

                lines.append(
                    f"| {idx} | `{r['video_id']}` | {r['svc_precision']:.0%} | {r['svc_recall']:.0%} | {r['svc_f1']:.0%} "
                    f"| {r['edge_precision']:.0%} | {r['edge_recall']:.0%} | {r['edge_f1']:.0%} "
                    f"| {r['gen_nodes']} | {r['gt_nodes']} | {r['gen_edges']} | {r['gt_edges']} "
                    f"| {missing_str or '—'} | {halluc_str or '—'} |"
                )
            lines.append("\n")
        lines.append("\n---\n")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    console.print(f"[green]✓[/] Combined report saved → [bold]{output_path}[/]")


def main(gen_dir: Path | None, gt_dir: Path, output_dir: Path) -> None:
    """Run the evaluation pipeline."""
    # Load services catalog
    services_csv = gt_dir / "services.csv"
    if not services_csv.exists():
        # Try Cloudscape repo as fallback
        services_csv = Path(__file__).resolve().parent.parent.parent / "Cloudscape" / "data" / "services.csv"
    catalog = load_services_catalog(services_csv)
    console.print(f"[green]✓[/] Loaded {len(catalog)} services from catalog")

    copied_ids = get_copied_video_ids()
    console.print(f"[yellow]ℹ[/] Identified {len(copied_ids)} Ground Truth copied/mocked videos in cache.")

    if gen_dir is not None:
        # Single directory evaluation
        console.print(f"Evaluating single directory: {gen_dir}")
        results = evaluate_dir_helper(gen_dir, gt_dir, catalog)
        if not results:
            console.print("[red]✗[/] No matching graph pairs found!")
            return
        agg = aggregate_results(results, catalog)

        print_summary_table(agg, f"Evaluation Summary: {gen_dir.name}")

        output_dir.mkdir(parents=True, exist_ok=True)
        generate_markdown_report(results, agg, output_dir / "evaluation_report.md", catalog)
        
        single_eval = {gen_dir.name: {"results": results, "agg": agg}}
        generate_csv(single_eval, output_dir / "evaluation_per_video.csv")
        save_json_results(results, agg, output_dir / "evaluation_results.json")
    else:
        # Multi-directory evaluation (Default)
        dirs_to_evaluate = {
            "Standard (data/graphs)": Path("data/graphs"),
            "Parsimonious API (data/graphs_parsimonious)": Path("data/graphs_parsimonious"),
        }

        all_evals = {}
        for label, path in dirs_to_evaluate.items():
            if not path.exists():
                console.print(f"[yellow]⚠ Directory {path} does not exist. Skipping.[/]")
                continue
            console.print(f"\n[bold cyan]Evaluating {label}...[/]")
            results = evaluate_dir_helper(path, gt_dir, catalog)
            if results:
                agg = aggregate_results(results, catalog)
                all_evals[label] = {
                    "path": path,
                    "results": results,
                    "agg": agg
                }

        if not all_evals:
            console.print("[red]✗[/] No evaluations completed!")
            return

        output_dir.mkdir(parents=True, exist_ok=True)
        generate_combined_markdown_report(all_evals, output_dir / "evaluation_report.md", catalog, copied_ids)
        generate_csv(all_evals, output_dir / "evaluation_per_video.csv")

        # Console print for Fleiss's Kappa
        gt_dir = Path("data/cloudscape_gt")
        std_dir = Path("data/graphs")
        pars_dir = Path("data/graphs_parsimonious")
        kappa_res = compute_fleiss_kappa_score(gt_dir, std_dir, pars_dir, catalog)
        if kappa_res:
            kappa, num_vids = kappa_res
            if kappa > 0.80:
                interpretation = "Acuerdo casi perfecto (Altamente confiable)"
            elif kappa > 0.60:
                interpretation = "Acuerdo sustancial"
            elif kappa > 0.40:
                interpretation = "Acuerdo moderado"
            else:
                interpretation = "Acuerdo débil o pobre"
            console.print(f"\n[bold green]✓[/] [bold]Fleiss's Kappa (K):[/] {kappa:.4f} ({interpretation}) calculated over {num_vids} shared videos\n")

        if "Standard (data/graphs)" in all_evals:
            save_json_results(
                all_evals["Standard (data/graphs)"]["results"],
                all_evals["Standard (data/graphs)"]["agg"],
                output_dir / "evaluation_results.json"
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate generated graphs against Cloudscape ground truth"
    )
    parser.add_argument(
        "--gen-dir", type=Path, default=None,
        help="Directory with generated .graphml files (default: None, which evaluates all three)",
    )
    parser.add_argument(
        "--gt-dir", type=Path, default=Path("data/cloudscape_gt"),
        help="Directory with ground truth .graphml files (default: data/cloudscape_gt)",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("cloudscape_reports"),
        help="Directory for output reports (default: cloudscape_reports)",
    )
    args = parser.parse_args()

    main(args.gen_dir, args.gt_dir, args.output_dir)

