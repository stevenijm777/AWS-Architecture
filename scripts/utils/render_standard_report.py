#!/usr/bin/env python3
"""
render_standard_report.py — Render an HTML report from an evaluation run.

Reads a run directory produced by evaluate_standard.py (results.csv + run.json)
and writes report.html next to them. The report is generated only from those two
files, never from the graphs themselves, so what it shows is always exactly what
was measured — and its header states the real sample size and every exclusion.

Usage:
    .venv/bin/python scripts/utils/render_standard_report.py reports/runs/<run-dir>
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def load_run(run_dir: Path) -> tuple[dict, list[dict]]:
    meta = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
    with open(run_dir / "results.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return meta, rows


def stat_card(label: str, value: str, sub: str) -> str:
    return (
        f'<div class="card"><div class="card-label">{html.escape(label)}</div>'
        f'<div class="card-value">{html.escape(value)}</div>'
        f'<div class="card-sub">{html.escape(sub)}</div></div>'
    )


def build_html(meta: dict, rows: list[dict]) -> str:
    m = meta["metrics"]
    c = meta["counts"]
    excluded = set(meta["exclusions"]["gt_has_zero_edges"])

    cards = "".join([
        stat_card("Service F1", f"{m['service_f1']['mean']}%", f"median {m['service_f1']['median']}% · n={c['evaluated']}"),
        stat_card("Service Recall", f"{m['service_recall']['mean']}%", f"n={c['evaluated']}"),
        stat_card("Edge F1", f"{m['edge_f1']['mean']}%", f"median {m['edge_f1']['median']}% · n={c['scored_for_edges']}"),
        stat_card("Edge Recall", f"{m['edge_recall']['mean']}%", f"n={c['scored_for_edges']}"),
    ])

    body_rows = []
    for r in sorted(rows, key=lambda x: float(x["svc_f1"]), reverse=True):
        excl = r["video_id"] in excluded
        edge_cells = (
            '<td class="muted" colspan="2">GT sin aristas — no puntuable</td>'
            if excl else
            f'<td>{r["edge_f1"]}%</td><td>{r["edge_type_accuracy"]}%</td>'
        )
        body_rows.append(
            f'<tr class="{"excluded" if excl else ""}">'
            f'<td class="mono">{html.escape(r["video_id"])}</td>'
            f'<td class="name">{html.escape(r["gt_name"][:70])}</td>'
            f'<td>{r["gen_nodes"]}/{r["gt_nodes"]}</td>'
            f'<td>{r["gen_edges"]}/{r["gt_edges"]}</td>'
            f'<td><b>{r["svc_f1"]}%</b></td>'
            f'{edge_cells}</tr>'
        )

    legacy = m["edge_f1_legacy_including_zero_edge_gt"]
    caveat = ""
    if c["excluded_from_edges"]:
        caveat = (
            f'<p class="caveat"><b>{c["excluded_from_edges"]}</b> de los {c["evaluated"]} vídeos tienen un '
            f'ground truth <b>sin aristas</b>: su Edge F1 es 0 por construcción, así que quedan fuera del promedio '
            f'de aristas (siguen contando en servicios). Promediando sobre todos, como hacían los reportes '
            f'anteriores, el Edge F1 sería <b>{legacy["mean"]}%</b> en vez de <b>{m["edge_f1"]["mean"]}%</b>.</p>'
        )

    return f"""<meta charset="utf-8">
<title>Standard {meta['label']} — {c['evaluated']} vídeos</title>
<style>
  :root {{ --bg:#fff; --fg:#1a1a1a; --muted:#6b7280; --line:#e5e7eb; --accent:#0f766e; --card:#f9fafb; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#0f1115; --fg:#e5e7eb; --muted:#9ca3af; --line:#272b33; --accent:#2dd4bf; --card:#161a21; }}
  }}
  body {{ background:var(--bg); color:var(--fg); font:15px/1.55 system-ui,-apple-system,Segoe UI,sans-serif;
         margin:0; padding:32px 20px; }}
  .wrap {{ max-width:1120px; margin:0 auto; }}
  h1 {{ font-size:24px; margin:0 0 4px; }}
  .sub {{ color:var(--muted); margin:0 0 6px; }}
  .prov {{ color:var(--muted); font-size:13px; margin:0 0 24px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:14px; margin-bottom:22px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:16px; }}
  .card-label {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.05em; }}
  .card-value {{ font-size:28px; font-weight:650; color:var(--accent); margin:4px 0 2px; }}
  .card-sub {{ color:var(--muted); font-size:12px; }}
  .caveat {{ background:var(--card); border-left:3px solid var(--accent); border-radius:6px;
             padding:12px 16px; font-size:14px; margin:0 0 24px; }}
  .scroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:10px; }}
  table {{ border-collapse:collapse; width:100%; font-size:14px; }}
  th,td {{ padding:9px 12px; text-align:right; border-bottom:1px solid var(--line); white-space:nowrap; }}
  th {{ background:var(--card); position:sticky; top:0; font-size:12px; text-transform:uppercase;
        letter-spacing:.04em; color:var(--muted); }}
  td.mono {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; text-align:left; }}
  td.name {{ text-align:left; max-width:380px; overflow:hidden; text-overflow:ellipsis; }}
  tr.excluded {{ opacity:.55; }}
  .muted {{ color:var(--muted); font-style:italic; text-align:center; }}
  tbody tr:hover {{ background:var(--card); }}
</style>
<div class="wrap">
  <h1>Standard <code>{html.escape(meta['label'])}</code> vs Cloudscape GT</h1>
  <p class="sub">Evaluación estricta sobre <b>{c['evaluated']} vídeos</b> ·
     aristas puntuadas sobre <b>{c['scored_for_edges']}</b></p>
  <p class="prov">{html.escape(meta['pipeline'])}<br>
     modelo <code>{html.escape(meta['gemini_model'])}</code> ·
     commit <code>{html.escape(meta['git_commit'])}</code> ·
     entrada <code>{html.escape(meta['inputs']['graphs_dir'])}</code> ·
     generado {html.escape(meta['generated_on'])}</p>
  <div class="cards">{cards}</div>
  {caveat}
  <div class="scroll"><table>
    <thead><tr>
      <th style="text-align:left">Video ID</th><th style="text-align:left">Título (GT)</th>
      <th>Nodos gen/GT</th><th>Aristas gen/GT</th>
      <th>Service F1</th><th>Edge F1</th><th>Tipo arista</th>
    </tr></thead>
    <tbody>{''.join(body_rows)}</tbody>
  </table></div>
</div>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render HTML from an evaluation run directory")
    parser.add_argument("run_dir", help="Run directory containing results.csv and run.json")
    args = parser.parse_args()

    run_dir = Path(args.run_dir)
    for required in ("results.csv", "run.json"):
        if not (run_dir / required).exists():
            print(f"✗ Missing {required} in {run_dir}", file=sys.stderr)
            sys.exit(1)

    meta, rows = load_run(run_dir)
    out = run_dir / "report.html"
    out.write_text(build_html(meta, rows), encoding="utf-8")
    print(f"✓ Report written → {out}")


if __name__ == "__main__":
    main()
