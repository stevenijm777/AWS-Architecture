"""
evaluar.py — Métricas por video, reutilizando `evaluate_pair` del repo sin cambios.

De `evaluate_pair` salen F1 de servicios, F1 de aristas (protocolo estricto: multiconjunto de
pares de servicios) y exactitud de tipo. Aquí solo se agrega:

  precisión por procedencia  de las aristas generadas con cada procedencia (dibujada, hablada,
                             ambas, regla, critico), qué fracción coincide con el GT. Si un par
                             tiene g aristas generadas y m coinciden, cada una recibe m/g, así
                             que ninguna procedencia se lleva el crédito por orden de llegada.
  llamadas y tokens          de los registros del cliente para ese video.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

from scripts.utils.evaluate_graphs import (
    evaluate_pair, extract_edge_service_pairs_no_type, load_services_catalog,
)

ROOT = Path(__file__).resolve().parent.parent
GT_DIR = ROOT / "data" / "cloudscape_gt"
CATALOGO = load_services_catalog(GT_DIR / "services.csv")
PRECIO = {"entrada": 0.75, "salida": 3.75}       # USD por millón, Flash 3.6/3.8 hasta 2026-12-31


def procedencia(G: nx.MultiDiGraph, grafo: dict, gt: nx.MultiDiGraph) -> dict[str, dict]:
    svc = {str(n): d.get("service", "") for n, d in G.nodes(data=True)}
    gt_c = Counter(extract_edge_service_pairs_no_type(gt))
    por_par = defaultdict(list)
    for e in grafo["edges"]:
        por_par[(svc.get(e["source"], ""), svc.get(e["target"], ""))].append(e.get("procedencia", "?"))
    total, acierto = Counter(), Counter()
    for par, procs in por_par.items():
        credito = min(len(procs), gt_c.get(par, 0)) / len(procs)
        for p in procs:
            total[p] += 1
            acierto[p] += credito
    return {p: {"aristas": total[p], "coinciden": round(acierto[p], 3)} for p in total}


def uso(registros: list[dict]) -> dict:
    ent = sum(r.get("entrada", 0) for r in registros)
    sal = sum(r.get("salida", 0) + r.get("thinking", 0) for r in registros)
    return {"llamadas": len(registros), "nuevas": sum(not r.get("desde_cache") for r in registros),
            "entrada": ent, "salida_y_thinking": sal,
            "usd": round((ent * PRECIO["entrada"] + sal * PRECIO["salida"]) / 1e6, 4),
            "por_agente": dict(Counter(r["agente"] for r in registros))}


def evaluar(vid: str, G: nx.MultiDiGraph, grafo: dict, registros: list[dict]) -> dict:
    gt = nx.MultiDiGraph(nx.read_graphml(GT_DIR / f"{vid}.graphml"))
    ev = evaluate_pair(G, gt, vid, CATALOGO)
    return {
        "video_id": vid, "status": "success",
        **{k: ev[k] for k in ("svc_f1", "edge_f1", "edge_precision", "edge_recall", "edge_type_accuracy",
                              "gen_nodes", "gt_nodes", "gen_edges", "gt_edges", "graph_usable",
                              "services_missing", "services_hallucinated", "edges_only_gen",
                              "edges_only_gt")},
        "procedencia": procedencia(G, grafo, gt),
        "uso": uso(registros),
    }
