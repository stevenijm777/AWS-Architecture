#!/usr/bin/env python3
"""
fase1a_huella_y_reglas.py — Fase 1a del experimento de reglas de convención (sin API).

1. Huella de anotación. Rasgos del GT que delatan cómo se anotó (primas en `seq`, notas en
   aristas, nombres de nodos, notas del grafo) frente a la fracción de pares con ida y vuelta.
   Si el estilo de retornos va con la huella, es una convención de quien anotó, no del video.
2. Señales disponibles al inferir (el grafo de producción y la transcripción) frente a ese estilo.
3. Reglas firmes por par, estimadas en inducción y aplicadas a la producción:
     invertir   — una arista de un solo sentido va al revés de lo que el GT hace casi siempre
     ambas      — el par lleva ida y vuelta en casi todos los grafos del GT
     solo_ida   — el par nunca lleva vuelta en el GT (solo se cuenta: los retornos extra
                  valen +0,25 como máximo, no compensa aplicarla)
     actor     — el subtipo de actor generado se cambia por el que el GT usa en su lugar
   Se miden en inducción (donde se estimaron) y en validación (estimación honesta).
   El panel de 30 no se abre.

    .venv/Scripts/python scripts/reglas/fase1a_huella_y_reglas.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from fase0_diagnostico import (  # noqa: E402
    GEN_DIR, GT_DIR, OUT, es_actor, estilo, f1, leer, spearman,
)
from scripts.utils.evaluate_graphs import extract_edge_service_pairs_no_type, extract_service_set  # noqa: E402

SOPORTE, UMBRAL = 5, 0.8      # grafos mínimos con el par y proporción mínima para fijar una regla
ALMACENES = {"S3", "DynamoDB", "RDS", "Aurora", "ElastiCache", "RedShift", "DocumentDB", "Neptune",
             "OpenSearch", "ElasticSearch", "Timestream", "Keyspaces", "MemoryDB", "EFS", "EBS"}


def pares(G) -> Counter:
    return Counter(extract_edge_service_pairs_no_type(G))


# ── 1. Huella ────────────────────────────────────────────────────────
def huella(G) -> dict:
    seqs = [str(d.get("seq", "")) for *_, d in G.edges(data=True)]
    notas = str(G.graph.get("notes", "") or "")
    n_e, n_n = max(G.number_of_edges(), 1), max(G.number_of_nodes(), 1)
    return {
        "seq_con_prima": any("'" in s for s in seqs),
        "seq_con_NA": any(s.startswith("NA") for s in seqs),
        "notas_en_aristas": sum(bool(d.get("notes")) for *_, d in G.edges(data=True)) / n_e > 0,
        "nombres_de_nodo": sum(bool(d.get("name")) for _, d in G.nodes(data=True)) / n_n,
        "notas_del_grafo": len(notas.strip()) > 0,
        "notas_en_viñetas": notas.lstrip().startswith("-"),
        "frac_meta": sum(d.get("type") == "meta" for *_, d in G.edges(data=True)) / n_e,
    }


def primas_son_retornos(ids: list[str]) -> dict:
    """¿Una arista con seq primado (2') es la vuelta de otra arista del mismo grafo?"""
    con_vuelta = total = 0
    for vid in ids:
        G = leer(GT_DIR / f"{vid}.graphml")
        dirigidos = set(extract_edge_service_pairs_no_type(G))
        for u, v, d in G.edges(data=True):
            if "'" in str(d.get("seq", "")):
                a, b = G.nodes[u].get("service"), G.nodes[v].get("service")
                total += 1
                con_vuelta += (b, a) in dirigidos
    return {"aristas_primadas": total, "con_la_arista_inversa_pct": round(100 * con_vuelta / max(total, 1), 1)}


def comparar_grupos(ids: list[str], rasgo) -> dict:
    si, no = [], []
    for vid in ids:
        G = leer(GT_DIR / f"{vid}.graphml")
        (si if rasgo(vid, G) else no).append(estilo(G)["frac_bidireccional"])
    return {"n_si": len(si), "bidir_si": round(mean(si), 3) if si else None,
            "n_no": len(no), "bidir_no": round(mean(no), 3) if no else None}


# ── 2. Señales al inferir ────────────────────────────────────────────
def transcripcion(vid: str) -> str:
    t = ROOT / "data" / "raw" / f"{vid}_transcript.json"
    if not t.exists():
        return ""
    d = json.loads(t.read_text(encoding="utf-8"))
    return " ".join(s.get("text", "") for s in d) if isinstance(d, list) else d.get("text", "")


def señales(ids: list[str]) -> dict:
    y, X = [], defaultdict(list)
    for vid in ids:
        gen, gt = leer(GEN_DIR / f"{vid}.graphml"), leer(GT_DIR / f"{vid}.graphml")
        y.append(estilo(gt)["frac_bidireccional"])
        s = extract_service_set(gen)
        X["palabras_transcripcion"].append(len(transcripcion(vid).split()))
        X["nodos_generados"].append(gen.number_of_nodes())
        X["aristas_generadas"].append(gen.number_of_edges())
        X["almacenes_generados"].append(len(s & ALMACENES))
        X["actor_generado"].append(float(any(es_actor(x) for x in s)))
        X["bidir_generada"].append(estilo(gen)["frac_bidireccional"])
    return {k: round(spearman(v, y), 3) for k, v in X.items()}


# ── 3. Reglas firmes ─────────────────────────────────────────────────
def estimar(ids: list[str]) -> dict:
    dire, unico, actor = defaultdict(Counter), defaultdict(Counter), defaultdict(Counter)
    for vid in ids:
        gt, gen = leer(GT_DIR / f"{vid}.graphml"), leer(GEN_DIR / f"{vid}.graphml")
        d = set(pares(gt))
        for a, b in {tuple(sorted(p)) for p in d if p[0] != p[1]}:
            ida, vuelta = (a, b) in d, (b, a) in d
            dire[(a, b)]["ambas" if ida and vuelta else "uno"] += 1
            if ida != vuelta:
                unico[(a, b)][(a, b) if ida else (b, a)] += 1
        # Subtipo de actor: si hay un solo actor de cada lado, el generado "debió ser" el del GT
        ag = sorted(x for x in extract_service_set(gen) if es_actor(x))
        at = sorted(x for x in extract_service_set(gt) if es_actor(x))
        if len(ag) == 1 and len(at) == 1:
            actor[ag[0]][at[0]] += 1
    reglas = {"invertir": {}, "ambas": set(), "solo_ida": set(), "actor": {}}
    for par, c in unico.items():
        n = sum(c.values())
        sentido, k = c.most_common(1)[0]
        if n >= SOPORTE and k / n >= UMBRAL:
            reglas["invertir"][sentido[::-1]] = sentido      # la dirección contraria se corrige
    for par, c in dire.items():
        n = sum(c.values())
        if n >= SOPORTE and c["ambas"] / n >= UMBRAL:
            reglas["ambas"].add(par)
        if n >= SOPORTE and c["ambas"] == 0:
            reglas["solo_ida"].add(par)
    for x, c in actor.items():
        y, k = c.most_common(1)[0]
        if y != x and sum(c.values()) >= SOPORTE and k > c[x]:
            reglas["actor"][x] = y
    return reglas


def aplicar(gen_c: Counter, reglas: dict, cuales: set[str]) -> Counter:
    g = Counter(gen_c)
    if "actor" in cuales:
        g = Counter({(reglas["actor"].get(a, a), reglas["actor"].get(b, b)): n for (a, b), n in g.items()})
    if "invertir" in cuales:
        nuevo = Counter()
        for (a, b), n in g.items():
            ok = reglas["invertir"].get((a, b))
            nuevo[ok if ok and (b, a) not in g else (a, b)] += n
        g = nuevo
    if "ambas" in cuales:
        for a, b in list(g):
            if tuple(sorted((a, b))) in reglas["ambas"] and a != b and (b, a) not in g:
                g[(b, a)] += 1
    return g


def medir(ids: list[str], reglas: dict) -> dict:
    combos = {"ninguna": set(), "actor": {"actor"}, "invertir": {"invertir"}, "ambas": {"ambas"},
              "todas": {"actor", "invertir", "ambas"}}
    res = {}
    for nombre, cuales in combos.items():
        res[nombre] = round(mean(f1(aplicar(pares(leer(GEN_DIR / f"{v}.graphml")), reglas, cuales),
                                   pares(leer(GT_DIR / f"{v}.graphml"))) for v in ids), 2)
    return res


def main() -> None:
    p = json.loads((OUT / "particion.json").read_text(encoding="utf-8"))
    ind, val = p["induccion"], p["validacion"]

    huellas = {v: huella(leer(GT_DIR / f"{v}.graphml")) for v in ind}
    grupos = {k: comparar_grupos(ind, lambda v, G, k=k: bool(huellas[v][k]) if not isinstance(huellas[v][k], float)
                                 else huellas[v][k] > 0.5)
              for k in huellas[ind[0]]}
    reglas = estimar(ind)
    res = {
        "huella": {"primas": primas_son_retornos(ind), "bidir_por_rasgo": grupos},
        "señales_al_inferir_spearman": señales(ind),
        "reglas": {"invertir": len(reglas["invertir"]), "ambas": sorted(" — ".join(x) for x in reglas["ambas"]),
                   "solo_ida": len(reglas["solo_ida"]), "actor": reglas["actor"],
                   "soporte_minimo": SOPORTE, "umbral": UMBRAL},
        "edge_f1_induccion": medir(ind, reglas),
        "edge_f1_validacion": medir(val, reglas),
    }
    (OUT / "fase1a_resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
