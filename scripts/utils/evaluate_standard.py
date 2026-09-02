#!/usr/bin/env python3
"""
evaluate_standard.py — Single source of truth for Standard-mode evaluation.

Evaluates a folder of generated graphs against the Cloudscape ground truth and
writes two files into a run directory:

    results.csv   one row per video, no aggregation, no filtering
    run.json      aggregates + provenance (inputs, exclusions, model, commit)

Ground-truth graphs with zero edges are counted in the service metrics but
excluded from the edge averages: with no edges to match, Edge F1 is 0.0 by
construction and would silently depress the mean. They are reported separately
rather than dropped.

Usage:
    .venv/bin/python scripts/utils/evaluate_standard.py
    .venv/bin/python scripts/utils/evaluate_standard.py --graphs data/graphs --label v6corrected
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import warnings
from datetime import date
from pathlib import Path
from statistics import mean, median

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

warnings.filterwarnings("ignore")

import networkx as nx
from rich.console import Console
from rich.table import Table

from config.settings import DATA_DIR, GEMINI_MODEL
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

console = Console()

GT_DIR = DATA_DIR / "cloudscape_gt"
REPORTS_DIR = PROJECT_ROOT / "reports"

CSV_COLUMNS = [
    "video_id", "gt_name",
    "gen_nodes", "gt_nodes", "gen_edges", "gt_edges",
    "svc_precision", "svc_recall", "svc_f1",
    # `svc_f1` compara CONJUNTOS de servicios: duplicar o colapsar instancias de un tipo
    # que el GT ya tiene sale gratis. `ms_f1` usa MULTICONJUNTOS y por lo tanto exige
    # acertar tambien la multiplicidad. `evaluate_pair` calculaba las dos desde siempre,
    # pero solo la primera llegaba al CSV — y el 15.3 % de los nodos del GT son instancias
    # repetidas, asi que la diferencia no es marginal (~2.4 pts sobre el corpus).
    "ms_precision", "ms_recall", "ms_f1",
    "edge_precision", "edge_recall", "edge_f1",
    "edge_type_accuracy",
    "graph_usable", "scored_for_edges", "exclusion_reason",
    "categories",
]


def _display_path(path: Path) -> str:
    """Path relative to the project root when possible, absolute otherwise."""
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        return str(path)


def git_commit() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10,
        )
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def evaluate_folder(graphs_dir: Path, gt_dir: Path) -> tuple[list[dict], list[dict]]:
    """Evaluate every graph that has a ground truth. Returns (rows, unreadable)."""
    catalog = load_services_catalog(gt_dir / "services.csv")
    vids = sorted(
        f.stem for f in graphs_dir.glob("*.graphml")
        if (gt_dir / f"{f.stem}.graphml").exists()
    )

    rows: list[dict] = []
    unreadable: list[dict] = []

    for vid in vids:
        try:
            g_gen = nx.read_graphml(graphs_dir / f"{vid}.graphml")
            g_gt = nx.read_graphml(gt_dir / f"{vid}.graphml")
        except Exception as e:
            unreadable.append({"video_id": vid, "error": str(e)[:150]})
            continue

        res = evaluate_pair(g_gen, g_gt, vid, catalog)

        # Edge F1 is only meaningful when the ground truth actually has edges.
        has_gt_edges = g_gt.number_of_edges() > 0
        res["scored_for_edges"] = has_gt_edges

        reasons = []
        if not res["graph_usable"]:
            reasons.append("gt_marked_unusable")
        if not has_gt_edges:
            reasons.append("gt_has_zero_edges")
        res["exclusion_reason"] = ",".join(reasons)
        rows.append(res)

    return rows, unreadable


def summarize(rows: list[dict]) -> dict:
    """Aggregate metrics over GT-usable rows; edge metrics further limited to rows with GT edges.

    Cloudscape marks 56/396 of its own ground-truth graphs graph_usable=False.
    Those rows stay in results.csv (raw, unfiltered) but are dropped from every
    published mean/median here — same treatment as the zero-edge-GT exclusion
    already applied to edge metrics.
    """
    usable = [r for r in rows if r["graph_usable"]]
    scored = [r for r in usable if r["scored_for_edges"]]

    def stats(values: list[float]) -> dict | None:
        if not values:
            return None
        return {
            "mean": round(100 * mean(values), 2),
            "median": round(100 * median(values), 2),
            "min": round(100 * min(values), 2),
            "max": round(100 * max(values), 2),
        }

    return {
        "n_evaluated": len(rows),
        "n_excluded_unusable": len(rows) - len(usable),
        "n_scored_for_edges": len(scored),
        "n_excluded_from_edges": len(usable) - len(scored),
        "service_precision": stats([r["svc_precision"] for r in usable]),
        "service_recall": stats([r["svc_recall"] for r in usable]),
        "service_f1": stats([r["svc_f1"] for r in usable]),
        # Variante de multiconjunto: misma poblacion, pero exigiendo la multiplicidad.
        "service_f1_multiset": stats([r["ms_f1"] for r in usable]),
        "edge_precision": stats([r["edge_precision"] for r in scored]),
        "edge_recall": stats([r["edge_recall"] for r in scored]),
        "edge_f1": stats([r["edge_f1"] for r in scored]),
        # Kept for continuity with older reports, which averaged over everything.
        "edge_f1_legacy_including_zero_edge_gt": stats([r["edge_f1"] for r in usable]),
        "service_f1_legacy_including_unusable": stats([r["svc_f1"] for r in rows]),
    }


def write_csv(rows: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for r in sorted(rows, key=lambda x: x["video_id"]):
            row = dict(r)
            for k in ("svc_precision", "svc_recall", "svc_f1",
                      "ms_precision", "ms_recall", "ms_f1",
                      "edge_precision", "edge_recall", "edge_f1", "edge_type_accuracy"):
                row[k] = round(100 * row[k], 2)
            row["categories"] = ", ".join(row["categories"]) if isinstance(row["categories"], (list, tuple)) else row["categories"]
            writer.writerow(row)


def print_summary(agg: dict, excluded_edges: list[str], excluded_unusable: list[str]) -> None:
    n_usable = agg["n_evaluated"] - agg["n_excluded_unusable"]
    t = Table(title="Standard vs Cloudscape GT — strict", border_style="cyan")
    t.add_column("Metric", style="bold")
    t.add_column("Mean", justify="right", style="green")
    t.add_column("Median", justify="right")
    t.add_column("n", justify="right")

    for label, key, n in [
        ("Service Precision", "service_precision", n_usable),
        ("Service Recall", "service_recall", n_usable),
        ("Service F1", "service_f1", n_usable),
        ("Service F1 (multiconjunto)", "service_f1_multiset", n_usable),
        ("Edge Precision", "edge_precision", agg["n_scored_for_edges"]),
        ("Edge Recall", "edge_recall", agg["n_scored_for_edges"]),
        ("Edge F1", "edge_f1", agg["n_scored_for_edges"]),
    ]:
        s = agg[key]
        if s:
            t.add_row(label, f"{s['mean']}%", f"{s['median']}%", str(n))
    console.print(t)

    if agg["n_excluded_unusable"]:
        console.print(
            f"[dim]{agg['n_excluded_unusable']} graph(s) marked graph_usable=False by "
            f"Cloudscape excluded from all published means (kept raw in results.csv): "
            f"{', '.join(excluded_unusable)}[/]"
        )

    legacy = agg["edge_f1_legacy_including_zero_edge_gt"]
    if legacy and agg["n_excluded_from_edges"]:
        console.print(
            f"[dim]Edge F1 as older reports computed it (zero-edge GT included): "
            f"{legacy['mean']}% over {n_usable} usable videos — "
            f"{agg['n_excluded_from_edges']} of them can never score above 0.[/]"
        )
        console.print(f"[dim]Excluded from edge averages: {', '.join(excluded_edges)}[/]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Standard-mode graphs against Cloudscape GT")
    parser.add_argument("--graphs", default=str(DATA_DIR / "graphs"), help="Folder of generated graphs")
    parser.add_argument("--gt", default=str(GT_DIR), help="Ground truth folder")
    parser.add_argument("--label", default="v6corrected", help="Prompt/model label recorded in run.json")
    parser.add_argument("--out", default=None, help="Run directory (default: reports/runs/<date>_standard_<label>_<n>v)")
    args = parser.parse_args()

    graphs_dir, gt_dir = Path(args.graphs), Path(args.gt)
    if not graphs_dir.exists():
        console.print(f"[bold red]✗ Graphs folder not found: {graphs_dir}[/]")
        sys.exit(1)

    console.print(f"[dim]Evaluating {graphs_dir} against {gt_dir}…[/]")
    rows, unreadable = evaluate_folder(graphs_dir, gt_dir)
    if not rows:
        console.print("[bold red]✗ Nothing to evaluate.[/]")
        sys.exit(1)

    agg = summarize(rows)
    excluded_unusable = sorted(r["video_id"] for r in rows if not r["graph_usable"])
    excluded_edges = sorted(
        r["video_id"] for r in rows if r["graph_usable"] and not r["scored_for_edges"]
    )

    out_dir = Path(args.out).resolve() if args.out else (
        REPORTS_DIR / "runs" / f"{date.today().isoformat()}_standard_{args.label}_{len(rows)}v"
    )
    out_dir.mkdir(parents=True, exist_ok=True)

    write_csv(rows, out_dir / "results.csv")

    run_meta = {
        "generated_on": date.today().isoformat(),
        "mode": "standard",
        "label": args.label,
        "pipeline": "2-stage (Stage 1 Modeler → Stage 2 Planner), Pydantic response_schema, temperature 0.0",
        "gemini_model": GEMINI_MODEL,
        "git_commit": git_commit(),
        "inputs": {
            "graphs_dir": _display_path(graphs_dir),
            "gt_dir": _display_path(gt_dir),
        },
        "counts": {
            "evaluated": agg["n_evaluated"],
            "excluded_unusable": agg["n_excluded_unusable"],
            "scored_for_edges": agg["n_scored_for_edges"],
            "excluded_from_edges": agg["n_excluded_from_edges"],
            "unreadable": len(unreadable),
        },
        "exclusions": {
            "gt_marked_unusable": excluded_unusable,
            "gt_has_zero_edges": excluded_edges,
            "unreadable": unreadable,
        },
        "metrics": agg,
    }
    (out_dir / "run.json").write_text(
        json.dumps(run_meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print_summary(agg, excluded_edges, excluded_unusable)
    if unreadable:
        console.print(f"[yellow]⚠ {len(unreadable)} unreadable graph(s) skipped — see run.json[/]")
    console.print(f"\n[green]✓[/] Run written → [bold]{_display_path(out_dir)}[/]\n")


if __name__ == "__main__":
    main()
