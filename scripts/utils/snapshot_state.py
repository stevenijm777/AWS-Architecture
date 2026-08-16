#!/usr/bin/env python3
"""
snapshot_state.py — Read-only snapshot of the pipeline's current state.

Emits a JSON baseline under reports/ describing coverage, file integrity and
Standard-mode metrics, so that later changes can be verified against a frozen
"before". This script never writes to data/ and never calls any API.

Usage:
    .venv/bin/python scripts/utils/snapshot_state.py
    .venv/bin/python scripts/utils/snapshot_state.py --out reports/baseline_x.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import warnings
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

warnings.filterwarnings("ignore")

import networkx as nx
from rich.console import Console
from rich.table import Table

from config.settings import (
    DATA_DIR,
    GOOD_WHITEBOARD_DIR,
    GRAPHS_DIR,
    GEMINI_MODEL,
    RAW_DIR,
)
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

console = Console()

GT_DIR = DATA_DIR / "cloudscape_gt"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Folders inspected for integrity. Parsimonious dirs are read but never touched.
GRAPH_DIRS = [
    "graphs",
    "graphs_parsimonious",
    "graphs_parsimonious_v9",
    "graphs_parsimonious_v10",
    "graphs_v6_highlighted",
    "graphs_v2_previous",
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


def inspect_integrity(dir_name: str) -> dict:
    """Count files, empty files and unparseable GraphML in a directory."""
    d = DATA_DIR / dir_name
    if not d.exists():
        return {"exists": False}

    files = sorted(d.glob("*.graphml"))
    empty, unparseable, ok = [], [], 0

    for f in files:
        if f.stat().st_size == 0:
            empty.append(f.stem)
            continue
        try:
            nx.read_graphml(f)
            ok += 1
        except Exception as e:
            unparseable.append({"video_id": f.stem, "error": str(e)[:120]})

    return {
        "exists": True,
        "files": len(files),
        "valid": ok,
        "empty": empty,
        "unparseable": unparseable,
    }


def inspect_coverage() -> dict:
    """Standard-mode coverage against the Cloudscape ground truth."""
    gt_ids = {f.stem for f in GT_DIR.glob("*.graphml")}
    std_ids = {f.stem for f in GRAPHS_DIR.glob("*.graphml")}

    missing = sorted(gt_ids - std_ids)
    # Videos that can be processed right now: whiteboard approved + transcript on disk
    ready = [
        v for v in missing
        if (GOOD_WHITEBOARD_DIR / f"{v}.jpg").exists()
        and (RAW_DIR / f"{v}_transcript.json").exists()
    ]

    return {
        "gt_total": len(gt_ids),
        "standard_graphs": len(std_ids),
        "standard_with_gt": len(std_ids & gt_ids),
        "gt_without_standard": len(missing),
        "ready_to_process": ready,
        "ready_to_process_count": len(ready),
    }


def evaluate_standard() -> dict:
    """Strict Standard-vs-GT metrics, with and without zero-edge ground truths."""
    catalog = load_services_catalog(GT_DIR / "services.csv")
    vids = sorted(
        f.stem for f in GRAPHS_DIR.glob("*.graphml")
        if (GT_DIR / f"{f.stem}.graphml").exists()
    )

    svc_f1, edge_f1_all, edge_f1_scored = [], [], []
    zero_edge_gt, failed = [], []

    for vid in vids:
        try:
            g_gen = nx.read_graphml(GRAPHS_DIR / f"{vid}.graphml")
            g_gt = nx.read_graphml(GT_DIR / f"{vid}.graphml")
        except Exception as e:
            failed.append({"video_id": vid, "error": str(e)[:120]})
            continue

        res = evaluate_pair(g_gen, g_gt, vid, catalog)
        svc_f1.append(res["svc_f1"])
        edge_f1_all.append(res["edge_f1"])

        if g_gt.number_of_edges() == 0:
            # Edge F1 is 0.0 by construction here — no edges can ever be matched.
            zero_edge_gt.append(vid)
        else:
            edge_f1_scored.append(res["edge_f1"])

    def mean(xs):
        return round(100 * sum(xs) / len(xs), 2) if xs else None

    return {
        "n_evaluated": len(svc_f1),
        "n_failed_to_read": len(failed),
        "failed_to_read": failed,
        "service_f1_strict": mean(svc_f1),
        "edge_f1_including_zero_edge_gt": mean(edge_f1_all),
        "edge_f1_excluding_zero_edge_gt": mean(edge_f1_scored),
        "n_scored_for_edges": len(edge_f1_scored),
        "zero_edge_gt_count": len(zero_edge_gt),
        "zero_edge_gt_videos": zero_edge_gt,
    }


def build_snapshot() -> dict:
    return {
        "generated_on": date.today().isoformat(),
        "git_commit": git_commit(),
        "gemini_model": GEMINI_MODEL,
        "scope": "standard-only (parsimonious folders inspected read-only)",
        "coverage": inspect_coverage(),
        "integrity": {name: inspect_integrity(name) for name in GRAPH_DIRS},
        "standard_metrics": evaluate_standard(),
    }


def print_summary(snap: dict) -> None:
    cov, met = snap["coverage"], snap["standard_metrics"]

    t = Table(title="Standard — Coverage", border_style="cyan")
    t.add_column("Metric", style="bold")
    t.add_column("Value", style="green", justify="right")
    t.add_row("Ground truth graphs", str(cov["gt_total"]))
    t.add_row("Standard graphs", str(cov["standard_graphs"]))
    t.add_row("Standard with GT (evaluable)", str(cov["standard_with_gt"]))
    t.add_row("GT without standard", str(cov["gt_without_standard"]))
    t.add_row("Ready to process now", str(cov["ready_to_process_count"]))
    console.print(t)

    t2 = Table(title="Standard — Strict metrics vs GT", border_style="cyan")
    t2.add_column("Metric", style="bold")
    t2.add_column("Value", style="green", justify="right")
    t2.add_column("n", justify="right")
    t2.add_row("Service F1", f"{met['service_f1_strict']}%", str(met["n_evaluated"]))
    t2.add_row("Edge F1 (as computed today)", f"{met['edge_f1_including_zero_edge_gt']}%", str(met["n_evaluated"]))
    t2.add_row("Edge F1 (zero-edge GT excluded)", f"{met['edge_f1_excluding_zero_edge_gt']}%", str(met["n_scored_for_edges"]))
    t2.add_row("GT with zero edges", str(met["zero_edge_gt_count"]), "—")
    console.print(t2)

    problems = []
    for name, info in snap["integrity"].items():
        if not info.get("exists"):
            continue
        if info["empty"] or info["unparseable"]:
            problems.append(
                f"  {name}: {len(info['empty'])} empty, {len(info['unparseable'])} unparseable"
            )
    if problems:
        console.print("\n[bold yellow]Integrity issues[/]")
        console.print("\n".join(problems))
    else:
        console.print("\n[green]✓[/] No empty or unparseable GraphML found.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only state snapshot of the pipeline")
    parser.add_argument(
        "--out", default=None,
        help="Output JSON path (default: reports/baseline_<today>.json)",
    )
    args = parser.parse_args()

    snap = build_snapshot()

    out_path = Path(args.out).resolve() if args.out else REPORTS_DIR / f"baseline_{snap['generated_on']}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")

    print_summary(snap)
    console.print(f"\n[green]✓[/] Snapshot saved → [bold]{_display_path(out_path)}[/]\n")


if __name__ == "__main__":
    main()
