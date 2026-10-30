#!/usr/bin/env python3
"""
permisivo.py — Evaluación permisiva con las tres reglas por separado, sin llamadas a la API.

El permisivo del paper (`build_evidence_tables.eval_permissive`) relaja tres cosas a la vez:
  A  actores: todo User* cuenta como User y todo ThirdParty* como ThirdParty;
  C  conjunto: las aristas repetidas entre el mismo par de servicios cuentan una sola vez;
  N  no dirigida: A→B y B→A son la misma arista.
Aquí se prueban las 8 combinaciones sobre los mismos grafos, para ver qué regla explica la
diferencia entre dos corridas. Con ninguna regla se reproduce el edge F1 de `evaluate_pair` (multiconjunto
dirigido) y con las tres se reproduce el permisivo del paper.

Los grafos salen del `analysis` de cada fila (corridas de rerun_panel o linea_base) o del
.graphml que exporta el orquestador.

    .venv/Scripts/python -m multiagent.permisivo --a <línea base> --b <corrida> [--b ...]
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import product
from pathlib import Path

import networkx as nx

from multiagent.estadistica import MDE, comparar
from scripts.ablation.build_evidence_tables import norm_permissive
from scripts.core.graph_builder import create_graph_from_cloudscape_json

GT_DIR = Path("data/cloudscape_gt")
COMBOS = [dict(zip("ACN", bits)) for bits in product([False, True], repeat=3)]


def nombre(combo: dict) -> str:
    return "+".join(k for k in "ACN" if combo[k]) or "estricto"


def f1(gen: Counter, gt: Counter) -> float:
    hit = sum((gen & gt).values())
    p = hit / sum(gen.values()) if gen else 0.0
    r = hit / sum(gt.values()) if gt else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def servicios(G, actores: bool) -> Counter:
    norm = norm_permissive if actores else str
    return Counter({norm(G.nodes[n].get("service", "?")) for n in G})


def aristas(G, A: bool, C: bool, N: bool) -> Counter:
    norm = norm_permissive if A else str
    pares = []
    for u, v in G.edges():
        a, b = norm(G.nodes[u].get("service", "?")), norm(G.nodes[v].get("service", "?"))
        if A and "Unknown" in (a, b):           # mismo filtro que el permisivo del paper
            continue
        pares.append(tuple(sorted((a, b))) if N else (a, b))
    return Counter(set(pares)) if C else Counter(pares)


def cargar(ruta: str, gts: dict) -> dict:
    """{vid: {métrica: valor}} con las 8 combinaciones; comprueba que el estricto reproduce run.json."""
    carpeta = Path(ruta)
    run = json.loads((carpeta / "run.json").read_text(encoding="utf-8"))
    por_video = {}
    for r in run["results"]:
        if r.get("status") != "success":
            continue
        vid = r["video_id"]
        if vid not in gts:
            gts[vid] = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
        gt = gts[vid]
        if r.get("analysis"):
            G = create_graph_from_cloudscape_json(r["analysis"], video_id=vid)
        else:
            G = nx.read_graphml(str(carpeta / vid / f"{vid}.graphml"))
        fila = {"svc_f1": f1(servicios(G, False), servicios(gt, False)),
                "svc_f1_A": f1(servicios(G, True), servicios(gt, True))}
        for c in COMBOS:
            fila[f"edge_f1_{nombre(c)}"] = f1(aristas(G, **c), aristas(gt, **c))
        estricto = r["edge_f1"]
        if abs(fila["edge_f1_estricto"] - estricto) > 1e-9:
            raise SystemExit(f"{ruta} · {vid}: el estricto no reproduce run.json "
                             f"({fila['edge_f1_estricto']:.4f} vs {estricto:.4f})")
        por_video[vid] = fila
    return {"_by_id": por_video, "ruta": ruta}


def main() -> None:
    ap = argparse.ArgumentParser(description="Permisivo con las tres reglas por separado")
    ap.add_argument("--a", required=True, help="línea base (carpeta con run.json)")
    ap.add_argument("--b", required=True, nargs="+")
    ap.add_argument("--out", default="reports/multiagente/permisivo_por_regla.json")
    args = ap.parse_args()

    gts: dict = {}
    base = cargar(args.a, gts)
    otras = [cargar(b, gts) for b in args.b]
    metricas = [f"edge_f1_{nombre(c)}" for c in COMBOS] + ["svc_f1", "svc_f1_A"]

    salida = {"base": args.a, "medias": {}, "comparaciones": {}}
    for run in [base] + otras:
        filas = run["_by_id"].values()
        salida["medias"][run["ruta"]] = {m: round(100 * sum(f[m] for f in filas) / len(filas), 2) for m in metricas}

    print(f"Medias (edge F1 salvo svc_*), n por corrida = {[len(r['_by_id']) for r in [base] + otras]}")
    print(f"{'regla':14s}" + "".join(f"{Path(r['ruta']).name[:26]:>28s}" for r in [base] + otras))
    for m in metricas:
        print(f"{m.replace('edge_f1_', ''):14s}" + "".join(f"{salida['medias'][r['ruta']][m]:28.2f}" for r in [base] + otras))

    for run in otras:
        print(f"\n{Path(run['ruta']).name} − {Path(args.a).name}")
        salida["comparaciones"][run["ruta"]] = {}
        for m in metricas:
            r = comparar(base, run, m)
            salida["comparaciones"][run["ruta"]][m] = r
            print(f"  {m.replace('edge_f1_', ''):12s} Δ {r['delta']:+6.2f}  IC95 [{r['ic95'][0]:+6.2f}, {r['ic95'][1]:+6.2f}]"
                  f"  signos {r['signos']['mejora']:2d}/{r['signos']['empeora']:2d}/{r['signos']['empates']:2d}"
                  f"  Wilcoxon p={r['wilcoxon']['p']:.3f}  Â12={r['a12']:.2f}  {'≥' if r['supera_mde'] else '<'} MDE {MDE}")
    Path(args.out).write_text(json.dumps(salida, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
