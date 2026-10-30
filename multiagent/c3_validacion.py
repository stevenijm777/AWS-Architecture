"""
c3_validacion.py — C3: valida el grafo contra el esquema de Cloudscape y lo exporta.

Revisa, y corrige lo que es determinista:
  servicio_fuera_de_catalogo  → ThirdParty con el texto original como nombre
  id_de_nodo_repetido         → se queda el primero
  arista_colgante             → se quita (apunta a un nodo inexistente)
  arista_duplicada            → se quita (mismo origen, destino, flow_id y seq)
Y solo reporta:
  nodo_huerfano               → nodo sin aristas
  lazo                        → arista de un nodo a sí mismo (el GT tiene algunos)

`necesita_critico` es verdadero si hubo huérfanos o aristas colgantes: son los problemas
que una corrección puntual de A4 puede arreglar.

Exporta con `create_graph_from_cloudscape_json` + `export_graphml` (el mismo camino que
producción) y escribe aparte un JSON con la procedencia de cada arista.
"""
from __future__ import annotations

import copy
import csv
import json
from pathlib import Path

import networkx as nx

from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml

ROOT = Path(__file__).resolve().parent.parent
SERVICES_CSV = ROOT / "data" / "cloudscape_gt" / "services.csv"
DISPARAN_A4 = {"nodo_huerfano", "arista_colgante"}


def catalogo() -> dict[str, str]:
    with open(SERVICES_CSV, encoding="utf-8") as fh:
        return {r["name"].strip().lower(): r["name"].strip() for r in csv.DictReader(fh) if r["name"].strip()}


def validar(grafo: dict) -> tuple[dict, list[dict]]:
    g = copy.deepcopy(grafo)
    cat = catalogo()
    problemas: list[dict] = []

    vistos, nodos = set(), []
    for n in g["nodes"]:
        if n["id"] in vistos:
            problemas.append({"tipo": "id_de_nodo_repetido", "nodo": n["id"]})
            continue
        vistos.add(n["id"])
        canon = cat.get(str(n["service"]).strip().lower())
        if canon is None:
            problemas.append({"tipo": "servicio_fuera_de_catalogo", "nodo": n["id"], "servicio": n["service"]})
            n["name"] = n.get("name") or n["service"]
            canon = "ThirdParty"
        n["service"] = canon
        nodos.append(n)
    g["nodes"] = nodos

    claves, aristas = set(), []
    for e in g["edges"]:
        if e["source"] not in vistos or e["target"] not in vistos:
            problemas.append({"tipo": "arista_colgante", "arista": f"{e['source']}->{e['target']}"})
            continue
        k = (e["source"], e["target"], e["flow_id"], e["seq"])
        if k in claves:
            problemas.append({"tipo": "arista_duplicada", "arista": f"{e['source']}->{e['target']}",
                              "flow_id": e["flow_id"], "seq": e["seq"]})
            continue
        claves.add(k)
        if e["source"] == e["target"]:
            problemas.append({"tipo": "lazo", "arista": f"{e['source']}->{e['target']}"})
        aristas.append(e)
    g["edges"] = aristas

    con_arista = {e["source"] for e in aristas} | {e["target"] for e in aristas}
    for n in nodos:
        if n["id"] not in con_arista:
            problemas.append({"tipo": "nodo_huerfano", "nodo": n["id"], "servicio": n["service"]})
    return g, problemas


def necesita_critico(problemas: list[dict]) -> bool:
    return any(p["tipo"] in DISPARAN_A4 for p in problemas)


def a_cloudscape(grafo: dict, vid: str) -> dict:
    return {
        "graph": {"name": grafo.get("nombre", ""), "link": f"https://www.youtube.com/watch?v={vid}",
                  "categories": "", "graph_usable": True, "notes": ""},
        "nodes": [{k: n.get(k, "") for k in ("id", "service", "name", "notes")} for n in grafo["nodes"]],
        "edges": [{k: e.get(k, "") for k in ("source", "target", "flow_id", "seq", "type", "notes")}
                  for e in grafo["edges"]],
    }


def exportar(grafo: dict, vid: str, carpeta: Path) -> tuple[nx.MultiDiGraph, Path]:
    G = create_graph_from_cloudscape_json(a_cloudscape(grafo, vid), video_id=vid)
    ruta = export_graphml(G, vid, carpeta)
    svc = {n["id"]: n["service"] for n in grafo["nodes"]}
    procedencia = [{"source": e["source"], "target": e["target"],
                    "par": f"{svc.get(e['source'])}->{svc.get(e['target'])}",
                    "procedencia": e.get("procedencia", "?"), "regla": e.get("regla"),
                    "critico": e.get("critico"), "respaldo": e.get("respaldo", "")}
                   for e in grafo["edges"]]
    (carpeta / f"{vid}_procedencia.json").write_text(
        json.dumps(procedencia, indent=1, ensure_ascii=False), encoding="utf-8")
    return G, ruta
