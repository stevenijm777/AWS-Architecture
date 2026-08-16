#!/usr/bin/env python3
"""
build_manifest.py — Regenerate reports/MANIFEST.md from the run directories.

The index is derived entirely from each run's run.json, so it cannot drift out
of sync with the runs it describes. Re-run it after every evaluation.

Usage:
    .venv/bin/python scripts/utils/build_manifest.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
RUNS_DIR = REPORTS_DIR / "runs"

HEADER = """# Reports index

Every row is generated from a run's `run.json`. Do not edit by hand — run
`.venv/bin/python scripts/utils/build_manifest.py` instead.

Each run directory holds `results.csv` (one row per video, unaggregated),
`run.json` (aggregates + provenance) and `report.html` (rendered from the CSV).
"""


def collect_runs() -> list[dict]:
    if not RUNS_DIR.exists():
        return []
    runs = []
    for run_dir in sorted(RUNS_DIR.iterdir(), reverse=True):
        meta_path = run_dir / "run.json"
        if not meta_path.exists():
            continue
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        meta["_dir"] = run_dir.name
        runs.append(meta)
    return runs


def render(runs: list[dict]) -> str:
    lines = [HEADER, "## Runs\n"]

    if not runs:
        lines.append("_No runs yet._\n")
        return "\n".join(lines)

    lines.append("| Date | Mode | Label | n | Service F1 | Edge F1 | Model | Commit |")
    lines.append("| :--- | :--- | :--- | ---: | ---: | ---: | :--- | :--- |")
    for m in runs:
        met, cnt = m.get("metrics", {}), m.get("counts", {})
        svc = met.get("service_f1") or {}
        edge = met.get("edge_f1") or {}
        lines.append(
            f"| [{m.get('generated_on', '?')}](runs/{m['_dir']}/report.html) "
            f"| {m.get('mode', '?')} | `{m.get('label', '?')}` "
            f"| {cnt.get('evaluated', '?')} "
            f"| {svc.get('mean', '?')}% "
            f"| {edge.get('mean', '?')}% (n={cnt.get('scored_for_edges', '?')}) "
            f"| `{m.get('gemini_model', '?')}` | `{m.get('git_commit', '?')}` |"
        )

    lines.append("\n## Notes per run\n")
    for m in runs:
        cnt = m.get("counts", {})
        excl = m.get("exclusions", {}).get("gt_has_zero_edges", [])
        legacy = (m.get("metrics", {}).get("edge_f1_legacy_including_zero_edge_gt") or {}).get("mean")
        lines.append(f"### `{m['_dir']}`\n")
        lines.append(f"- Pipeline: {m.get('pipeline', 'n/a')}")
        lines.append(f"- Input: `{m.get('inputs', {}).get('graphs_dir', '?')}` vs `{m.get('inputs', {}).get('gt_dir', '?')}`")
        lines.append(
            f"- Evaluated {cnt.get('evaluated')} · edges scored on {cnt.get('scored_for_edges')} · "
            f"excluded from edge averages {cnt.get('excluded_from_edges')} (ground truth has zero edges)"
        )
        if legacy is not None:
            lines.append(f"- Edge F1 averaged the old way (zero-edge GT included): {legacy}%")
        if excl:
            lines.append(f"- Excluded: {', '.join(f'`{v}`' for v in excl)}")
        if cnt.get("unreadable"):
            lines.append(f"- **{cnt['unreadable']} unreadable graph(s)** — see `run.json`")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    runs = collect_runs()
    out = REPORTS_DIR / "MANIFEST.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(runs), encoding="utf-8")
    print(f"✓ Manifest written → {out.relative_to(PROJECT_ROOT)} ({len(runs)} run(s))")


if __name__ == "__main__":
    main()
