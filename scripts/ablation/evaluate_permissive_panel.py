#!/usr/bin/env python3
"""
evaluate_permissive_panel.py — Re-score every ablation run under permissive rules.

Under the strict evaluator no pair of prompt variants differs significantly on the
30-video panel. One explanation is that the strict metric is dominated by noise the
variants have no control over — which actor subtype was named, whether a duplicated
service was fused, which way an arrow points. The permissive evaluator removes
exactly those three sources, so if real differences exist underneath, this is where
they surface.

**Permissive relaxes three things at once** (mirrors `generate_comparison_plots.py`,
`norm_permissive` / `eval_permissive`) — worth stating, because it is often described
as if it only merged actors:

  1. every `User*` collapses to `User`, every `ThirdParty*` to `ThirdParty`;
  2. services become a *set*, so duplicate instances stop counting;
  3. edges become *undirected* pairs, so direction errors stop counting.

Costs no API calls: every run's full `analysis` payload is stored in its `run.json`.

Usage
-----
    .venv/bin/python scripts/ablation/evaluate_permissive_panel.py
"""
from __future__ import annotations

import glob
import json
import sys
from itertools import combinations
from math import comb
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402
from scripts.utils.evaluate_graphs import load_services_catalog  # noqa: E402

console = Console()
GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
OUT = PROJECT_ROOT / "reports" / "permissive_panel.json"

CATALOG = load_services_catalog(GT_DIR / "services.csv")


def norm_permissive(svc: str) -> str:
    if not svc or svc == "?":
        return "Unknown"
    s = str(svc).strip()
    cap = CATALOG.get(s, {}).get("capability", "")
    if s.startswith("User") or cap == "User":
        return "User"
    if s.startswith("ThirdParty") or cap == "ThirdParty":
        return "ThirdParty"
    return s


def prf1(inter: int, gen: int, gt: int) -> float:
    p = inter / gen if gen else 0.0
    r = inter / gt if gt else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def eval_permissive(g_gen, g_gt) -> tuple[float, float]:
    gen_set = {norm_permissive(g_gen.nodes[n].get("service", "")) for n in g_gen}
    gt_set = {norm_permissive(g_gt.nodes[n].get("service", "")) for n in g_gt}
    node_f1 = prf1(len(gen_set & gt_set), len(gen_set), len(gt_set))

    def edges(G):
        out = set()
        for u, v in G.edges():
            a, b = (norm_permissive(G.nodes[u].get("service", "")),
                    norm_permissive(G.nodes[v].get("service", "")))
            if a and b and a != "Unknown" and b != "Unknown":
                out.add(tuple(sorted([a, b])))
        return out

    ge, te = edges(g_gen), edges(g_gt)
    return node_f1, prf1(len(ge & te), len(ge), len(te))


def sign_test(w: int, l: int) -> float:
    n = w + l
    if n == 0:
        return 1.0
    k = min(w, l)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main() -> None:
    gt_cache: dict[str, nx.MultiDiGraph] = {}
    variants = []

    for rj in sorted(glob.glob(str(PROJECT_ROOT / "reports/ablation/*_p30*/run.json"))):
        d = json.load(open(rj))
        # Las corridas con oráculo llevan el mismo prompt de Stage 2 pero reciben otro
        # world model —el ground truth, o una transcripción a mano—. Contarlas como
        # una variante más mezcla el efecto de cambiar la entrada con el de cambiar el
        # prompt, que es justo lo que este panel intenta separar.
        if d.get("oracle") or d.get("world_model_file"):
            continue
        sp, m = d["stage2_prompt"], d["metrics"]
        per_video = {}
        for r in d["results"]:
            if r["status"] != "success":
                continue
            vid = r["video_id"]
            if vid not in gt_cache:
                gt_cache[vid] = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
            G = create_graph_from_cloudscape_json(r["analysis"], video_id=vid)
            n_f1, e_f1 = eval_permissive(G, gt_cache[vid])
            per_video[vid] = {"node_f1": n_f1, "edge_f1": e_f1,
                              "strict_svc_f1": r["svc_f1"], "strict_edge_f1": r["edge_f1"]}
        name = sp["name"].replace("STAGE2_", "")
        if d.get("connection_evidence_enabled"):
            name += " +evidencia"
        variants.append({
            "name": name, "cell": sp.get("source_cell"), "sha": sp["sha256"][:12],
            "is_production": bool(sp.get("matches_production"))
                             and not d.get("connection_evidence_enabled"),
            "strict_svc_f1": m["service_f1_mean"], "strict_edge_f1": m["edge_f1_mean"],
            "perm_node_f1": round(100 * sum(v["node_f1"] for v in per_video.values()) / len(per_video), 2),
            "perm_edge_f1": round(100 * sum(v["edge_f1"] for v in per_video.values()) / len(per_video), 2),
            "videos": per_video,
        })

    variants.sort(key=lambda v: -v["perm_edge_f1"])

    t = Table(title="Evaluación permisiva vs estricta — panel de 30", border_style="cyan")
    t.add_column("variante", style="bold"); t.add_column("celda", justify="right")
    for c in ("Svc estricto", "Node permisivo", "Edge estricto", "Edge permisivo", "ganancia"):
        t.add_column(c, justify="right")
    for v in variants:
        t.add_row(v["name"] + (" ←prod" if v["is_production"] else ""),
                  str(v["cell"]), f"{v['strict_svc_f1']:.2f}", f"{v['perm_node_f1']:.2f}",
                  f"{v['strict_edge_f1']:.2f}", f"{v['perm_edge_f1']:.2f}",
                  f"+{v['perm_edge_f1'] - v['strict_edge_f1']:.2f}")
    console.print(t)

    # ¿discrimina mejor la permisiva? empates y significancia, misma prueba pareada
    console.print("\n[bold]Comparaciones pareadas — ¿aparece alguna diferencia?[/]")
    t2 = Table(border_style="cyan")
    for c in ("par", "estricto (G-P-E)", "p", "permisivo (G-P-E)", "p"):
        t2.add_column(c, justify="right" if c != "par" else "left")

    rows = []
    for a, b in combinations(variants, 2):
        vids = sorted(set(a["videos"]) & set(b["videos"]))
        res = {}
        for key, mode in (("strict_edge_f1", "estricto"), ("edge_f1", "permisivo")):
            w = l = t_ = 0
            for v in vids:
                x, y = a["videos"][v][key], b["videos"][v][key]
                if abs(x - y) < 1e-9:
                    t_ += 1
                elif x > y:
                    w += 1
                else:
                    l += 1
            res[mode] = (w, l, t_, sign_test(w, l))
        rows.append((f"{a['name']} c{a['cell']} vs {b['name']} c{b['cell']}", res))

    rows.sort(key=lambda r: r[1]["permisivo"][3])
    for label, res in rows[:12]:
        s, p = res["estricto"], res["permisivo"]
        t2.add_row(label[:52], f"{s[0]}-{s[1]}-{s[2]}", f"{s[3]:.3f}",
                   f"{p[0]}-{p[1]}-{p[2]}",
                   f"[bold red]{p[3]:.3f}[/]" if p[3] < 0.05 else f"{p[3]:.3f}")
    console.print(t2)
    console.print("[dim]G-P-E = gana-pierde-empata. Se muestran los 12 pares con menor p permisivo.[/]")

    n_sig_s = sum(1 for _, r in rows if r["estricto"][3] < 0.05)
    n_sig_p = sum(1 for _, r in rows if r["permisivo"][3] < 0.05)
    ties_s = sum(r["estricto"][2] for _, r in rows) / len(rows)
    ties_p = sum(r["permisivo"][2] for _, r in rows) / len(rows)
    console.print(f"\n[bold]De {len(rows)} comparaciones:[/] significativas con estricto "
                  f"[bold]{n_sig_s}[/], con permisivo [bold]{n_sig_p}[/]")
    console.print(f"Empates promedio por comparación: estricto {ties_s:.1f}/30 · "
                  f"permisivo {ties_p:.1f}/30")

    OUT.write_text(json.dumps({
        "note": "Permisivo = colapsa User*/ThirdParty*, usa conjuntos (ignora duplicados) "
                "y aristas no dirigidas. Ver generate_comparison_plots.py:norm_permissive.",
        "variants": variants,
        "pairwise": [{"pair": lbl, **{k: {"win": v[0], "loss": v[1], "tie": v[2], "p": round(v[3], 4)}
                                      for k, v in res.items()}} for lbl, res in rows],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
