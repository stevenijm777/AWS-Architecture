#!/usr/bin/env python3
"""
audit_dataset_coverage.py — Which ground-truth videos are in the study, and why.

Read-only. Cross-references every Cloudscape ground-truth graph against four
things that decide whether it belongs in a published comparison:

  1. graph_usable — Cloudscape's own flag. 56 of its 396 graphs are marked
     False by the dataset authors, and nothing in this repo honours it: the
     filter in evaluate_graphs.py reads r.get("graph_usable", True) but
     evaluate_pair never sets that key, so it always passes.
  2. Zero-edge ground truths, where Edge F1 is 0 by construction.
  3. Non-English videos, detected from the "(Language)" marker AWS puts in
     the title.
  4. Pairing — a video with no parsimonious counterpart cannot appear in a
     like-for-like comparison.

Emits a markdown report plus a CSV of per-video flags.

Usage:
    .venv/bin/python scripts/utils/audit_dataset_coverage.py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import warnings
from datetime import date
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

warnings.filterwarnings("ignore")

import networkx as nx
from rich.console import Console

from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

console = Console()

DATA = PROJECT_ROOT / "data"
GT_DIR = DATA / "cloudscape_gt"
STD_DIR = DATA / "graphs"
PARS_DIR = DATA / "graphs_parsimonious"
REPORTS = PROJECT_ROOT / "reports"

LANGUAGES = [
    "Japanese", "Spanish", "French", "Italian", "German", "Portuguese",
    "Korean", "Mandarin", "Chinese", "Arabic", "Hebrew", "Dutch", "Russian",
    "Turkish", "Polish", "Hindi",
]

# Compilation / special episodes: they aggregate several architectures, so a
# single whiteboard frame cannot represent them.
SPECIAL_KEYWORDS = [
    "spotlight", "greatest hits", "bloopers", "reprise",
    "special episode", "(special)",
]


def detect_language(title: str) -> str:
    for lang in LANGUAGES:
        if re.search(rf"\b{lang}\b", title, re.I):
            return lang
    return "English"


def is_special(title: str) -> bool:
    low = title.lower()
    return any(k in low for k in SPECIAL_KEYWORDS)


def collect() -> list[dict]:
    catalog = load_services_catalog(GT_DIR / "services.csv")
    rows: list[dict] = []

    for gt_path in sorted(GT_DIR.glob("*.graphml")):
        vid = gt_path.stem
        try:
            g_gt = nx.read_graphml(gt_path)
        except Exception as e:
            rows.append({"video_id": vid, "error": str(e)[:80]})
            continue

        title = str(g_gt.graph.get("name", ""))
        usable = str(g_gt.graph.get("graph_usable", True)).lower() != "false"

        row = {
            "video_id": vid,
            "title": title,
            "categories": str(g_gt.graph.get("categories", "")),
            "gt_usable": usable,
            "gt_nodes": g_gt.number_of_nodes(),
            "gt_edges": g_gt.number_of_edges(),
            "zero_edge_gt": g_gt.number_of_edges() == 0,
            "language": detect_language(title),
            "is_special": is_special(title),
            "has_standard": (STD_DIR / f"{vid}.graphml").exists(),
            "has_parsimonious": (PARS_DIR / f"{vid}.graphml").exists(),
        }

        for label, folder in (("std", STD_DIR), ("pars", PARS_DIR)):
            p = folder / f"{vid}.graphml"
            if not p.exists():
                row[f"{label}_svc_f1"] = None
                row[f"{label}_edge_f1"] = None
                continue
            try:
                res = evaluate_pair(nx.read_graphml(p), g_gt, vid, catalog)
                row[f"{label}_svc_f1"] = round(100 * res["svc_f1"], 2)
                row[f"{label}_edge_f1"] = round(100 * res["edge_f1"], 2)
            except Exception:
                row[f"{label}_svc_f1"] = None
                row[f"{label}_edge_f1"] = None

        row["in_paired_comparison"] = row["has_standard"] and row["has_parsimonious"]
        # What a published comparison should arguably rest on.
        row["study_eligible"] = (
            row["in_paired_comparison"]
            and row["gt_usable"]
            and not row["is_special"]
        )
        rows.append(row)

    return rows


def fmt(v) -> str:
    return "—" if v is None else f"{v:.1f}%"


def build_report(rows: list[dict]) -> str:
    ok = [r for r in rows if "error" not in r]
    L: list[str] = []
    A = L.append

    A(f"# Auditoría de cobertura del dataset — {date.today().isoformat()}\n")
    A("Generado por `scripts/utils/audit_dataset_coverage.py` (solo lectura).\n")

    total = len(ok)
    std = [r for r in ok if r["has_standard"]]
    pars = [r for r in ok if r["has_parsimonious"]]
    paired = [r for r in ok if r["in_paired_comparison"]]
    eligible = [r for r in ok if r["study_eligible"]]

    A("## 1. Resumen\n")
    A("| | n |")
    A("|---|---:|")
    A(f"| Grafos en el ground truth | {total} |")
    A(f"| Con grafo Standard | {len(std)} |")
    A(f"| Con grafo Parsimonious | {len(pars)} |")
    A(f"| **Pareados** (ambos, comparables) | **{len(paired)}** |")
    A(f"| Marcados `graph_usable=False` por Cloudscape | {sum(1 for r in ok if not r['gt_usable'])} |")
    A(f"| Ground truth sin aristas | {sum(1 for r in ok if r['zero_edge_gt'])} |")
    A(f"| No-inglés | {sum(1 for r in ok if r['language'] != 'English')} |")
    A(f"| Episodios especiales | {sum(1 for r in ok if r['is_special'])} |")
    A(f"| **Elegibles para el artículo** | **{len(eligible)}** |")
    A("")

    def avg(subset, key):
        vals = [r[key] for r in subset if r.get(key) is not None]
        return mean(vals) if vals else None

    A("## 2. Impacto de aplicar cada filtro\n")
    A("Service F1 medio sobre los videos pareados, retirando cada grupo:\n")
    A("| Conjunto | n | Standard | Parsimonious |")
    A("|---|---:|---:|---:|")
    variants = [
        ("Todos los pareados (como se reporta hoy)", paired),
        ("Sin los `graph_usable=False`", [r for r in paired if r["gt_usable"]]),
        ("Sin especiales", [r for r in paired if not r["is_special"]]),
        ("Sin no-inglés", [r for r in paired if r["language"] == "English"]),
        ("**Elegibles** (sin unusable ni especiales)", eligible),
        ("Elegibles y solo inglés", [r for r in eligible if r["language"] == "English"]),
    ]
    for label, subset in variants:
        A(f"| {label} | {len(subset)} | {fmt(avg(subset,'std_svc_f1'))} | {fmt(avg(subset,'pars_svc_f1'))} |")
    A("")

    A("## 3. Marcados `graph_usable=False` por Cloudscape\n")
    A("Etiqueta del propio dataset. **Actualmente se incluyen en todas las métricas.**\n")
    unus = sorted([r for r in ok if not r["gt_usable"]], key=lambda r: (r["std_svc_f1"] is None, r["std_svc_f1"] or 0))
    A("| Video | Título | Std F1 | Pars F1 | ¿en comparación? |")
    A("|---|---|---:|---:|---|")
    for r in unus:
        inc = "**sí**" if r["in_paired_comparison"] else "no"
        A(f"| `{r['video_id']}` | {r['title'][:52]} | {fmt(r['std_svc_f1'])} | {fmt(r['pars_svc_f1'])} | {inc} |")
    A("")

    A("## 4. Peor rendimiento — revisar a mano\n")
    A("Videos elegibles (pareados, usables, no especiales) ordenados por Service F1 de Standard.\n")
    worst = sorted([r for r in eligible if r["std_svc_f1"] is not None], key=lambda r: r["std_svc_f1"])[:30]
    A("| # | Video | Título | Std F1 | Pars F1 | Nodos GT | Aristas GT | Idioma |")
    A("|---:|---|---|---:|---:|---:|---:|---|")
    for i, r in enumerate(worst, 1):
        A(f"| {i} | `{r['video_id']}` | {r['title'][:44]} | {fmt(r['std_svc_f1'])} | "
          f"{fmt(r['pars_svc_f1'])} | {r['gt_nodes']} | {r['gt_edges']} | {r['language']} |")
    A("")

    A("### Peor Edge F1 (con ground truth que sí tiene aristas)\n")
    worst_e = sorted(
        [r for r in eligible if r["std_edge_f1"] is not None and not r["zero_edge_gt"]],
        key=lambda r: r["std_edge_f1"],
    )[:20]
    A("| # | Video | Título | Edge F1 | Aristas GT |")
    A("|---:|---|---|---:|---:|")
    for i, r in enumerate(worst_e, 1):
        A(f"| {i} | `{r['video_id']}` | {r['title'][:48]} | {fmt(r['std_edge_f1'])} | {r['gt_edges']} |")
    A("")

    A("## 5. Videos no-inglés\n")
    by_lang: dict[str, list[dict]] = {}
    for r in ok:
        if r["language"] != "English":
            by_lang.setdefault(r["language"], []).append(r)
    for lang in sorted(by_lang, key=lambda x: -len(by_lang[x])):
        grp = by_lang[lang]
        inc = sum(1 for r in grp if r["in_paired_comparison"])
        A(f"**{lang}** — {len(grp)} videos, {inc} dentro de la comparación\n")
        A("| Video | Título | Std F1 | ¿en comparación? |")
        A("|---|---|---:|---|")
        for r in sorted(grp, key=lambda r: r["video_id"]):
            A(f"| `{r['video_id']}` | {r['title'][:50]} | {fmt(r['std_svc_f1'])} | "
              f"{'**sí**' if r['in_paired_comparison'] else 'no'} |")
        A("")

    A("## 6. Episodios especiales\n")
    sp = [r for r in ok if r["is_special"]]
    if sp:
        A("| Video | Título | ¿en comparación? |")
        A("|---|---|---|")
        for r in sorted(sp, key=lambda r: r["video_id"]):
            A(f"| `{r['video_id']}` | {r['title'][:60]} | "
              f"{'**sí**' if r['in_paired_comparison'] else 'no'} |")
    else:
        A("_Ninguno en el ground truth._")
    A("")

    A("## 7. Sin par — quedan fuera de cualquier comparación\n")
    only_std = [r for r in ok if r["has_standard"] and not r["has_parsimonious"]]
    only_pars = [r for r in ok if r["has_parsimonious"] and not r["has_standard"]]
    neither = [r for r in ok if not r["has_standard"] and not r["has_parsimonious"]]
    A(f"- Solo Standard: **{len(only_std)}** — {', '.join('`%s`' % r['video_id'] for r in only_std[:40])}")
    A(f"- Solo Parsimonious: **{len(only_pars)}**")
    A(f"- Sin ninguno de los dos: **{len(neither)}**")
    A("")

    return "\n".join(L)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit which GT videos enter the study")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    rows = collect()
    REPORTS.mkdir(parents=True, exist_ok=True)

    md = Path(args.out) if args.out else REPORTS / f"dataset_audit_{date.today().isoformat()}.md"
    md.write_text(build_report(rows), encoding="utf-8")

    csv_path = md.with_suffix(".csv")
    cols = ["video_id", "title", "language", "categories", "gt_usable", "is_special",
            "zero_edge_gt", "gt_nodes", "gt_edges", "has_standard", "has_parsimonious",
            "in_paired_comparison", "study_eligible", "std_svc_f1", "std_edge_f1",
            "pars_svc_f1", "pars_edge_f1"]
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            if "error" not in r:
                w.writerow(r)

    ok = [r for r in rows if "error" not in r]
    console.print(f"[green]✓[/] {len(ok)} videos auditados")
    console.print(f"[green]✓[/] {md.relative_to(PROJECT_ROOT)}")
    console.print(f"[green]✓[/] {csv_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
