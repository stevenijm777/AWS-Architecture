"""
agentes.py — Insumos y armado de prompts de los agentes LLM (A1, A2, A3, A4, llamada única).

Cada agente ve una sola fuente:
  A1      los k fotogramas de pizarra, sin transcripción
  A2      la transcripción con marca de tiempo por segmento, sin imágenes
  A3      las salidas de A1 y A2 ya normalizadas por C1, sin_resolver y el catálogo
  A4      el grafo, los problemas de C3/C2 y las mismas salidas normalizadas
  única   pizarra + transcripción + catálogo en una sola llamada (configuración 2)
"""
from __future__ import annotations

import base64
import json
from functools import lru_cache
from pathlib import Path

import networkx as nx

from multiagent import esquemas
from multiagent.llm import CONFIG, Cliente, prompt, ruta
from scripts.ablation.rerun_panel import load_catalogs

ROOT = Path(__file__).resolve().parent.parent


@lru_cache(maxsize=1)
def catalogos() -> tuple[str, str]:
    aws, actores, _ = load_catalogs()
    return aws, actores


# ── Insumos ──────────────────────────────────────────────────────────
def fotogramas(vid: str, k: int) -> list[str]:
    if k == 1:
        rutas = [ruta("pizarras") / f"{vid}.jpg"]
    else:
        rutas = sorted((ruta("top_k") / vid / "top10").glob("rank_*.jpg"))[:k]
        if len(rutas) < k:
            raise FileNotFoundError(f"{vid}: hay {len(rutas)} fotogramas en top10/, se pidieron {k}")
    for r in rutas:
        if not r.exists():
            raise FileNotFoundError(f"{vid}: falta {r}")
    return [base64.b64encode(r.read_bytes()).decode("utf-8") for r in rutas]


def transcripcion(vid: str) -> str:
    p = ruta("transcripciones") / f"{vid}_transcript.json"
    segmentos = json.loads(p.read_text(encoding="utf-8"))
    return "\n".join(f"[{s['start']:.1f}] {s['text'].strip()}" for s in segmentos)


def lectura_desde_gt(vid: str) -> dict:
    """Brazo B: el GT en el formato de A1, como si la pizarra fuera la referencia."""
    G = nx.read_graphml(ruta("ground_truth") / f"{vid}.graphml")
    ids = {n: f"b{i}" for i, n in enumerate(G.nodes)}
    cajas = [{"id": ids[n], "texto_literal": d.get("name") or d.get("service", ""), "fotograma": 0}
             for n, d in G.nodes(data=True)]
    for c, (n, d) in zip(cajas, G.nodes(data=True)):
        if d.get("service") == "ThirdParty" and d.get("name"):
            c["texto_literal"] = f"{d['name']} (third-party)"
        elif d.get("service", "").startswith("User"):
            c["texto_literal"] = d["service"]
    lineas = [{"origen": ids[a], "destino": ids[b], "punta": "una", "etiqueta_literal": ""}
              for a, b in G.edges()]
    return {"cajas": cajas, "lineas": lineas, "contenedores": []}


def _json(x) -> str:
    return json.dumps(x, indent=1, ensure_ascii=False)


# ── Agentes ──────────────────────────────────────────────────────────
def a1(cli: Cliente, vid: str, k: int) -> tuple[dict, str]:
    plantilla, version = prompt("a1_lector_visual_v1.txt")
    texto = plantilla.replace("<K>", str(k))
    return cli.llamar(vid, "a1", texto, version, esquemas.LecturaVisual, fotogramas(vid, k)), version


def a2(cli: Cliente, vid: str) -> tuple[dict, str]:
    plantilla, version = prompt("a2_narracion_v1.txt")
    texto = plantilla.replace("<TRANSCRIPCION>", transcripcion(vid))
    return cli.llamar(vid, "a2", texto, version, esquemas.Narracion), version


def a3(cli: Cliente, vid: str, norm: dict) -> tuple[dict, str]:
    plantilla, version = prompt("a3_reconciliador_v1.txt")
    aws, actores = catalogos()
    narracion = _json(norm["a2"]) if norm["a2"] is not None else \
        "Not available in this configuration: use the visual reading only (no 'hablada' evidence)."
    texto = (plantilla.replace("<CATALOGO_AWS>", aws).replace("<CATALOGO_ACTORES>", actores)
             .replace("<LECTURA_VISUAL>", _json(norm["a1"]))
             .replace("<NARRACION>", narracion)
             .replace("<SIN_RESOLVER>", _json(norm["sin_resolver"])))
    return cli.llamar(vid, "a3", texto, version, esquemas.GrafoReconciliado), version


def a4(cli: Cliente, vid: str, grafo: dict, problemas: list[dict], norm: dict) -> tuple[dict, str]:
    plantilla, version = prompt("a4_critico_v1.txt")
    vista = {"nodes": [{k: n[k] for k in ("id", "service", "name")} for n in grafo["nodes"]],
             "edges": [{k: e.get(k) for k in ("source", "target", "type", "procedencia", "respaldo")}
                       for e in grafo["edges"]]}
    narracion = _json(norm["a2"]) if norm["a2"] is not None else "Not available in this configuration."
    texto = (plantilla.replace("<GRAFO>", _json(vista)).replace("<PROBLEMAS>", _json(problemas))
             .replace("<LECTURA_VISUAL>", _json(norm["a1"])).replace("<NARRACION>", narracion))
    return cli.llamar(vid, "a4", texto, version, esquemas.Critica), version


def unica(cli: Cliente, vid: str, k: int) -> tuple[dict, str]:
    plantilla, version = prompt("unica_llamada_v1.txt")
    aws, actores = catalogos()
    texto = (plantilla.replace("<K>", str(k)).replace("<CATALOGO_AWS>", aws)
             .replace("<CATALOGO_ACTORES>", actores).replace("<TRANSCRIPCION>", transcripcion(vid)))
    return cli.llamar(vid, "unica", texto, version, esquemas.GrafoReconciliado, fotogramas(vid, k)), version


def aplicar_correcciones(grafo: dict, critica: dict) -> tuple[dict, list[dict]]:
    """Aplica las correcciones de A4 que apuntan a nodos existentes; registra las demás."""
    g = json.loads(json.dumps(grafo))
    ids = {n["id"] for n in g["nodes"]}
    hechas = []
    for c in critica.get("correcciones", []):
        s, t, accion = c["source"], c["target"], c["accion"]
        if s not in ids or t not in ids:
            hechas.append({**c, "aplicada": False, "por_que": "nodo inexistente"})
            continue
        existente = next((e for e in g["edges"] if e["source"] == s and e["target"] == t), None)
        if accion == "agregar":
            vecina = next((e for e in g["edges"] if t in (e["source"], e["target"])
                           or s in (e["source"], e["target"])), None)
            g["edges"].append({"source": s, "target": t, "flow_id": vecina["flow_id"] if vecina else 0,
                               "seq": "0", "type": c["type"], "notes": "", "procedencia": "critico",
                               "critico": "agregada", "respaldo": c["motivo"]})
        elif existente is None:
            hechas.append({**c, "aplicada": False, "por_que": "la arista no existe"})
            continue
        elif accion == "quitar":
            g["edges"].remove(existente)
        else:
            existente["source"], existente["target"] = t, s
            existente["critico"] = "invertida"
        hechas.append({**c, "aplicada": True})
    return g, hechas
