#!/usr/bin/env python3
"""
fase0_diagnostico.py — Fase 0 del experimento de reglas de convención (sin API).

1. Partición. Los grafos puntuables del paper (321) que no están en el panel de 30 se
   dividen con semilla 42 en inducción (75 %) y validación (25 %). El panel es la prueba.
   Esta fase solo mira inducción; validación y panel no se abren.
2. Errores de producción en inducción. Cada arista del GT que la producción no tiene (FN) y
   cada arista generada que el GT no tiene (FP) cae en una sola clase. Para cada clase se
   calcula el F1 de aristas si se corrigiera entera: el techo de una regla dirigida a ella.
3. Consistencia del GT en inducción. Estilo de cada grafo (retornos, repeticiones, actores,
   tipos) y qué tan predecible es una arista a partir de los demás grafos (dejando uno fuera).
   Lo que no se predice desde los demás grafos no es convención: depende del video o es ruido.

    .venv/Scripts/python scripts/reglas/fase0_diagnostico.py
"""
from __future__ import annotations

import csv
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

import networkx as nx  # noqa: E402

from scripts.ablation.rerun_panel import PANEL_30  # noqa: E402
from scripts.utils.evaluate_graphs import (  # noqa: E402
    edge_multiset_precision_recall,
    extract_edge_service_pairs,
    extract_edge_service_pairs_no_type,
    extract_service_set,
)

RUN = ROOT / "reports" / "runs" / "2026-08-20_standard_v6corrected_370v" / "results.csv"
GEN_DIR = ROOT / "data" / "graphs"
GT_DIR = ROOT / "data" / "cloudscape_gt"
OUT = ROOT / "reports" / "reglas_convencion"
SEMILLA, FRAC_INDUCCION = 42, 0.75
MIN_SOPORTE = 3          # grafos "vecinos" mínimos para predecir algo por convención

FN_CLASES = ["nodo_faltante", "actor_subtipo", "repeticion_omitida", "direccion_invertida",
             "retorno_omitido", "conexion_omitida"]
FP_CLASES = ["nodo_alucinado", "actor_subtipo", "repeticion_extra", "direccion_invertida",
             "retorno_extra", "conexion_extra"]


def es_actor(s: str) -> bool:
    return s.startswith(("User", "ThirdParty"))


# ── 1. Partición ─────────────────────────────────────────────────────
def particion() -> dict:
    filas = [r for r in csv.DictReader(open(RUN, encoding="utf-8"))
             if r["scored_for_edges"] == "True" and r["graph_usable"] == "True"
             and not r["exclusion_reason"]]
    puntuables = sorted(r["video_id"] for r in filas)
    panel = set(PANEL_30)
    fuera = [v for v in puntuables if v not in panel]
    random.Random(SEMILLA).shuffle(fuera)
    k = round(FRAC_INDUCCION * len(fuera))
    p = {"semilla": SEMILLA, "fuente": str(RUN.relative_to(ROOT)),
         "n_puntuables": len(puntuables), "n_panel_en_puntuables": len(panel & set(puntuables)),
         "induccion": sorted(fuera[:k]), "validacion": sorted(fuera[k:]), "prueba": sorted(PANEL_30)}
    assert not (set(p["induccion"]) | set(p["validacion"])) & panel, "el panel se filtró"
    assert not set(p["induccion"]) & set(p["validacion"])
    return p


def leer(path: Path) -> nx.MultiDiGraph:
    return nx.MultiDiGraph(nx.read_graphml(str(path)))


# ── 2. Errores de producción ─────────────────────────────────────────
def clasificar(gen: nx.MultiDiGraph, gt: nx.MultiDiGraph) -> tuple[list, list]:
    """Devuelve [(par, clase)] para FN y para FP, con clases excluyentes."""
    gen_p, gt_p = extract_edge_service_pairs_no_type(gen), extract_edge_service_pairs_no_type(gt)
    gen_c, gt_c = Counter(gen_p), Counter(gt_p)
    gen_s, gt_s = extract_service_set(gen), extract_service_set(gt)
    fp_rest = gen_c - gt_c
    fns, fps = [], []
    for a, b in sorted((gt_c - gen_c).elements()):
        if es_actor(a) or es_actor(b):
            # Mismo par salvo el subtipo de actor (UserConsumerWeb vs UserCompanyAgent…)
            par = next((q for q in sorted(fp_rest) if fp_rest[q] > 0
                        and (es_actor(q[0]) if es_actor(a) else q[0] == a)
                        and (es_actor(q[1]) if es_actor(b) else q[1] == b)), None)
            if par:
                fp_rest[par] -= 1
                fns.append(((a, b), "actor_subtipo")); fps.append((par, "actor_subtipo"))
                continue
        if a not in gen_s or b not in gen_s:
            c = "nodo_faltante"
        elif gen_c[(a, b)] > 0:
            c = "repeticion_omitida"
        elif fp_rest[(b, a)] > 0:
            fp_rest[(b, a)] -= 1
            fps.append(((b, a), "direccion_invertida"))
            c = "direccion_invertida"
        elif gen_c[(b, a)] > 0:
            c = "retorno_omitido"           # la vuelta está y coincide: falta la ida
        else:
            c = "conexion_omitida"
        fns.append(((a, b), c))
    for a, b in sorted(fp_rest.elements()):
        if a not in gt_s or b not in gt_s:
            c = "nodo_alucinado"
        elif gt_c[(a, b)] > 0:
            c = "repeticion_extra"
        elif gt_c[(b, a)] > 0:
            c = "retorno_extra"
        else:
            c = "conexion_extra"
        fps.append(((a, b), c))
    return fns, fps


def f1(gen_c: Counter, gt_c: Counter) -> float:
    return 100 * edge_multiset_precision_recall(list(gen_c.elements()), list(gt_c.elements()))[2]


def errores(ids: list[str], referencia: dict[str, float]) -> dict:
    por_clase_fn, por_clase_fp = Counter(), Counter()
    videos_fn, videos_fp = defaultdict(set), defaultdict(set)
    base, corregido = [], defaultdict(list)
    desajustes, filas = [], []
    clases = sorted(set(FN_CLASES) | set(FP_CLASES))
    for vid in ids:
        gen, gt = leer(GEN_DIR / f"{vid}.graphml"), leer(GT_DIR / f"{vid}.graphml")
        gen_c = Counter(extract_edge_service_pairs_no_type(gen))
        gt_c = Counter(extract_edge_service_pairs_no_type(gt))
        b = f1(gen_c, gt_c)
        if abs(b - referencia[vid]) > 0.01:
            desajustes.append((vid, round(b, 2), referencia[vid]))
        base.append(b)
        fns, fps = clasificar(gen, gt)
        assert len(fns) == sum((gt_c - gen_c).values()) and len(fps) == sum((gen_c - gt_c).values())
        for par, c in fns:
            por_clase_fn[c] += 1; videos_fn[c].add(vid)
        for par, c in fps:
            por_clase_fp[c] += 1; videos_fp[c].add(vid)
        for c in clases:   # techo: corregir solo esta clase
            g = gen_c + Counter(p for p, k in fns if k == c)
            g = g - Counter(p for p, k in fps if k == c)
            corregido[c].append(f1(g, gt_c))
        filas.append({"video_id": vid, "edge_f1": round(b, 2), "gt_edges": sum(gt_c.values()),
                      "gen_edges": sum(gen_c.values()),
                      **{f"fn_{c}": sum(k == c for _, k in fns) for c in FN_CLASES},
                      **{f"fp_{c}": sum(k == c for _, k in fps) for c in FP_CLASES}})
    tot_fn, tot_fp = sum(por_clase_fn.values()), sum(por_clase_fp.values())
    mb = mean(base)
    return {
        "n_videos": len(ids), "edge_f1_base": round(mb, 2),
        "desajustes_con_results_csv": desajustes,
        "fn_total": tot_fn, "fp_total": tot_fp,
        "gt_aristas": sum(f["gt_edges"] for f in filas), "gen_aristas": sum(f["gen_edges"] for f in filas),
        "clases": {c: {"fn": por_clase_fn[c], "fp": por_clase_fp[c],
                       "fn_pct": round(100 * por_clase_fn[c] / tot_fn, 1),
                       "fp_pct": round(100 * por_clase_fp[c] / tot_fp, 1),
                       "videos": len(videos_fn[c] | videos_fp[c]),
                       "edge_f1_si_se_corrige": round(mean(corregido[c]), 2),
                       "ganancia": round(mean(corregido[c]) - mb, 2)} for c in clases},
        "_filas": filas,
    }


# ── 3. Consistencia del GT ───────────────────────────────────────────
def estilo(gt: nx.MultiDiGraph) -> dict:
    pares = extract_edge_service_pairs_no_type(gt)
    dirigidos = set(pares)
    no_dir = {frozenset(p) for p in dirigidos if p[0] != p[1]}
    bidir = sum(1 for u in no_dir if len(u) == 2 and tuple(u) in dirigidos and tuple(u)[::-1] in dirigidos)
    tipos = Counter(t for _, _, t in extract_edge_service_pairs(gt))
    flujos = {d.get("flow_id") for _, _, d in gt.edges(data=True)}
    svc = extract_service_set(gt)
    return {"aristas": len(pares), "pares": len(no_dir),
            "frac_bidireccional": bidir / len(no_dir) if no_dir else 0.0,
            "frac_repetidas": (len(pares) - len(dirigidos)) / len(pares) if pares else 0.0,
            "lazos": sum(1 for a, b in pares if a == b),
            "actores": sorted(s for s in svc if es_actor(s)), "tipos": dict(tipos), "flujos": len(flujos)}


def etiqueta_direccion(dirigidos: set, a: str, b: str) -> str:
    ida, vuelta = (a, b) in dirigidos, (b, a) in dirigidos
    return "ambas" if ida and vuelta else ("a->b" if ida else "b->a")


def predictibilidad(ids: list[str]) -> dict:
    """Dejando un grafo fuera, ¿los demás predicen sus aristas?"""
    info = {}
    for vid in ids:
        gt = leer(GT_DIR / f"{vid}.graphml")
        dirigidos = set(extract_edge_service_pairs_no_type(gt))
        svc = sorted(extract_service_set(gt))
        conectados = {tuple(sorted(p)) for p in dirigidos if p[0] != p[1]}
        info[vid] = {"svc": svc, "dir": dirigidos, "con": conectados}
    # Tablas globales; al predecir un grafo se le resta su propia contribución.
    co, con, dire = Counter(), Counter(), defaultdict(Counter)
    for v in info.values():
        s = v["svc"]
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                co[(s[i], s[j])] += 1
        for a, b in v["con"]:
            con[(a, b)] += 1
            dire[(a, b)][etiqueta_direccion(v["dir"], a, b)] += 1

    pres = {"aciertos": 0, "total": 0, "cubiertos": 0, "tp": 0, "fp": 0}
    dir_ok = dir_tot = dir_cub = 0
    dir_maj_ambas = 0
    mayorias = []
    for vid, v in info.items():
        s = v["svc"]
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                par = (s[i], s[j])
                real = par in v["con"]
                n_co, n_con = co[par] - 1, con[par] - real
                pres["total"] += 1
                if n_co >= MIN_SOPORTE:
                    pres["cubiertos"] += 1
                    pred = n_con / n_co > 0.5
                    pres["aciertos"] += pred == real
                    pres["tp"] += pred and real; pres["fp"] += pred and not real
        for a, b in v["con"]:
            dir_tot += 1
            propia = etiqueta_direccion(v["dir"], a, b)
            otros = dire[(a, b)].copy(); otros[propia] -= 1
            n = sum(otros.values())
            if n >= MIN_SOPORTE:
                dir_cub += 1
                maj, k = otros.most_common(1)[0]
                dir_ok += maj == propia
                dir_maj_ambas += maj == "ambas"
    for par, c in dire.items():
        n = sum(c.values())
        if n >= 5:
            mayorias.append({"par": f"{par[0]} — {par[1]}", "grafos": n,
                             **{k: c[k] for k in ("a->b", "b->a", "ambas")},
                             "mayoria": round(c.most_common(1)[0][1] / n, 2)})
    mayorias.sort(key=lambda r: -r["grafos"])
    total_real = sum(len(v["con"]) for v in info.values())
    return {
        "presencia": {"pares_con_ambos_servicios": pres["total"],
                      "cubiertos_pct": round(100 * pres["cubiertos"] / pres["total"], 1),
                      "exactitud_en_cubiertos": round(100 * pres["aciertos"] / max(pres["cubiertos"], 1), 1),
                      "pares_conectados_reales": total_real,
                      "recall_aristas_por_convencion": round(100 * pres["tp"] / total_real, 1),
                      "precision_aristas_por_convencion": round(100 * pres["tp"] / max(pres["tp"] + pres["fp"], 1), 1)},
        "direccion": {"pares_conectados": dir_tot, "cubiertos_pct": round(100 * dir_cub / dir_tot, 1),
                      "exactitud_en_cubiertos": round(100 * dir_ok / max(dir_cub, 1), 1),
                      "mayoria_es_ambas_pct": round(100 * dir_maj_ambas / max(dir_cub, 1), 1)},
        "pares_frecuentes": mayorias[:40],
    }


RE_RESPUESTA = re.compile(r"\b(return(s|ed|ing)?|respon(d|ds|ded|se|ses)|repl(y|ies|ied)|back to|"
                          r"send(s)? (it|them|that|this|the \w+) back|acknowledg\w*)\b")
RE_LECTURA = re.compile(r"\b(read(s|ing)?|fetch(es|ed|ing)?|retriev\w*|quer(y|ies|ied)|look(s|ed)? up|pull(s|ed)?)\b")


def retornos(ids: list[str]) -> dict:
    """¿Anotar ida y vuelta es un estilo del grafo, una propiedad del par o algo que se dice?"""
    pares = []          # (vid, par, bidireccional)
    for vid in ids:
        dirigidos = set(extract_edge_service_pairs_no_type(leer(GT_DIR / f"{vid}.graphml")))
        for a, b in sorted({tuple(sorted(p)) for p in dirigidos if p[0] != p[1]}):
            pares.append((vid, (a, b), (a, b) in dirigidos and (b, a) in dirigidos))
    por_par, por_grafo = defaultdict(list), defaultdict(list)
    for vid, par, bi in pares:
        por_par[par].append(bi); por_grafo[vid].append(bi)
    tasa = mean(bi for _, _, bi in pares)
    ok = Counter(); n = 0
    for vid, par, bi in pares:
        otros_par = list(por_par[par]); otros_par.remove(bi)
        otros_graf = list(por_grafo[vid]); otros_graf.remove(bi)
        if len(otros_par) < MIN_SOPORTE or len(otros_graf) < MIN_SOPORTE:
            continue                       # comparación justa: los tres predictores definidos
        n += 1
        ok["base"] += (tasa > 0.5) == bi
        ok["par"] += (mean(otros_par) > 0.5) == bi
        ok["grafo"] += (mean(otros_graf) > 0.5) == bi
    # Dirección cuando la arista va en un solo sentido: ¿todos los grafos coinciden?
    unico = defaultdict(Counter)
    for vid in ids:
        dirigidos = set(extract_edge_service_pairs_no_type(leer(GT_DIR / f"{vid}.graphml")))
        for a, b in dirigidos:
            if a != b and (b, a) not in dirigidos:
                unico[tuple(sorted((a, b)))][(a, b)] += 1
    con_mayoria = sum(c.most_common(1)[0][1] for c in unico.values() if sum(c.values()) >= 3)
    total_unico = sum(sum(c.values()) for c in unico.values() if sum(c.values()) >= 3)
    # Señal hablada: frecuencia de verbos de respuesta y de lectura frente a la fracción bidireccional
    xs, r_resp, r_lect = [], [], []
    for vid in ids:
        t = ROOT / "data" / "raw" / f"{vid}_transcript.json"
        if not t.exists():
            continue
        d = json.loads(t.read_text(encoding="utf-8"))
        texto = (" ".join(s.get("text", "") for s in d) if isinstance(d, list) else d.get("text", "")).lower()
        palabras = max(len(texto.split()), 1)
        xs.append(mean(por_grafo[vid]) if por_grafo[vid] else 0.0)
        r_resp.append(1000 * len(RE_RESPUESTA.findall(texto)) / palabras)
        r_lect.append(1000 * len(RE_LECTURA.findall(texto)) / palabras)
    return {
        "pares": len(pares), "tasa_bidireccional": round(100 * tasa, 1),
        "prediccion_bidireccional": {"n_comparables": n,
                                     **{f"exactitud_{k}": round(100 * v / n, 1) for k, v in ok.items()}},
        "direccion_si_va_en_un_sentido": {"aristas": total_unico,
                                          "en_la_direccion_mayoritaria_pct": round(100 * con_mayoria / max(total_unico, 1), 1)},
        "señal_hablada_spearman": {"n_grafos": len(xs), "verbos_respuesta": round(spearman(r_resp, xs), 3),
                                   "verbos_lectura": round(spearman(r_lect, xs), 3)},
    }


def politicas_retorno(ids: list[str]) -> dict:
    """F1 de producción si se agrega la vuelta de cada arista de un solo sentido:
    nunca, siempre, o solo en los grafos cuyo GT es mayormente bidireccional (oráculo de estilo)."""
    f = defaultdict(list)
    for vid in ids:
        gen, gt = leer(GEN_DIR / f"{vid}.graphml"), leer(GT_DIR / f"{vid}.graphml")
        gen_c = Counter(extract_edge_service_pairs_no_type(gen))
        gt_c = Counter(extract_edge_service_pairs_no_type(gt))
        vueltas = Counter({(b, a): 1 for a, b in gen_c if a != b and (b, a) not in gen_c})
        e = estilo(gt)
        f["nunca"].append(f1(gen_c, gt_c))
        f["siempre"].append(f1(gen_c + vueltas, gt_c))
        f["oraculo_estilo"].append(f1(gen_c + vueltas, gt_c) if e["frac_bidireccional"] >= 0.5 else f1(gen_c, gt_c))
    return {k: round(mean(v), 2) for k, v in f.items()}


def spearman(x: list[float], y: list[float]) -> float:
    def rangos(v):
        orden = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
        while i < len(v):
            j = i
            while j + 1 < len(v) and v[orden[j + 1]] == v[orden[i]]:
                j += 1
            for k in range(i, j + 1):
                r[orden[k]] = (i + j) / 2
            i = j + 1
        return r
    rx, ry = rangos(x), rangos(y)
    mx, my = mean(rx), mean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = (sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)) ** 0.5
    return num / den if den else 0.0


def histograma(xs: list[float], cortes=(0.0, 0.25, 0.5, 1.0)) -> dict:
    h = {"0": sum(x == 0 for x in xs)}
    for lo, hi in zip(cortes, cortes[1:]):
        h[f"({lo},{hi}]"] = sum(lo < x <= hi for x in xs)
    return h


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    p = particion()
    (OUT / "particion.json").write_text(json.dumps(p, indent=2), encoding="utf-8")
    ind = p["induccion"]
    print(f"partición: {len(ind)} inducción · {len(p['validacion'])} validación · {len(p['prueba'])} prueba "
          f"(de {p['n_puntuables']} puntuables; {p['n_panel_en_puntuables']} del panel estaban entre ellos)")

    ref = {r["video_id"]: float(r["edge_f1"]) for r in csv.DictReader(open(RUN, encoding="utf-8"))}
    err = errores(ind, ref)
    filas = err.pop("_filas")
    with open(OUT / "fase0_errores_por_video.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0])); w.writeheader(); w.writerows(filas)

    estilos = {vid: estilo(leer(GT_DIR / f"{vid}.graphml")) for vid in ind}
    E = list(estilos.values())
    tipos = Counter(); [tipos.update(e["tipos"]) for e in E]
    actores = Counter(a for e in E for a in e["actores"])
    cons = {
        "n_grafos": len(E),
        "aristas_por_grafo_mediana": median(e["aristas"] for e in E),
        "frac_bidireccional": {"media": round(mean(e["frac_bidireccional"] for e in E), 3),
                               "histograma": histograma([e["frac_bidireccional"] for e in E])},
        "frac_repetidas": {"media": round(mean(e["frac_repetidas"] for e in E), 3),
                           "histograma": histograma([e["frac_repetidas"] for e in E])},
        "grafos_con_lazos": sum(e["lazos"] > 0 for e in E),
        "grafos_con_actor": sum(bool(e["actores"]) for e in E),
        "actores": dict(actores.most_common()),
        "tipos_de_arista": dict(tipos.most_common()),
        "flujos_por_grafo_mediana": median(e["flujos"] for e in E),
        **predictibilidad(ind),
        "retornos": {**retornos(ind), "edge_f1_segun_politica": politicas_retorno(ind)},
    }
    res = {"particion": {k: (len(v) if isinstance(v, list) else v) for k, v in p.items()},
           "errores_produccion": err, "consistencia_gt": cons}
    (OUT / "fase0_resumen.json").write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in res.items()}, indent=1, ensure_ascii=False)[:9000])


if __name__ == "__main__":
    main()
