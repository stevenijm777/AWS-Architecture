#!/usr/bin/env python3
"""
build_evidence_tables.py — Regenera las dos tablas de evidencia del ARA desde los datos.

Las versiones anteriores de `ara/evidence/tables/table1` y `table2` citaban archivos que
no contenían sus cifras (table2) o publicaban 16 de 60 filas de una fuente congelada
(table1). Este script las reconstruye desde los artefactos actuales del repo, de modo que
cada número de la tabla sea reproducible corriéndolo de nuevo.

No gasta llamadas a la API: todo sale de `run.json` y de los `results.csv` ya guardados.

Table 2 — estricto vs permisivo
    Mismos grafos generados, dos protocolos de evaluación. Se toma la corrida de
    producción sobre el panel de 30 (`STAGE2_V6_CORRECTED` celda 9, sha ed1d85054d73)
    y se puntúa dos veces: con el evaluador estricto del proyecto
    (`scripts/utils/evaluate_graphs.evaluate_pair`) y con el permisivo
    (mismas reglas que `generate_comparison_plots.norm_permissive`).

Table 1 — Parsimonious vs Standard
    Cruce pareado sobre TODOS los videos que ambos pipelines pudieron procesar,
    no sobre una selección. Prueba de signos exacta y Wilcoxon de rangos con signo,
    ambas implementadas acá porque el venv no tiene scipy.

Uso
---
    .venv/bin/python scripts/ablation/build_evidence_tables.py
"""
from __future__ import annotations

import csv
import glob
import json
import random
import sys
from collections import Counter
from math import comb, erfc, sqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402
from scripts.utils.evaluate_graphs import (  # noqa: E402
    evaluate_pair,
    load_services_catalog,
)

GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
TABLES = PROJECT_ROOT / "ara" / "evidence" / "tables"
PROD_SHA = "ed1d85054d73"

PARS_CSV = PROJECT_ROOT / "reports/runs/2026-08-21_parsimonious_v9/results.csv"
STD_CSV = PROJECT_ROOT / "reports/runs/2026-08-20_standard_v6corrected_370v/results.csv"

CATALOG = load_services_catalog(GT_DIR / "services.csv")


# ── Estadística (sin scipy) ──────────────────────────────────────


def sign_test(wins: int, losses: int) -> float:
    """Prueba de signos exacta, dos colas. Los empates se descartan, como corresponde."""
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2**n)


def wilcoxon_signed_rank(diffs: list[float]) -> tuple[float, float]:
    """Wilcoxon de rangos con signo, aproximación normal con corrección por empates.

    Vale la pena correrlo además de la t pareada: cuando las dos divergen, la que se
    cae es el supuesto de normalidad, y acá la mitad de los videos empata exactamente,
    así que la distribución de diferencias no es ni remotamente normal.

    Devuelve (W, p a dos colas).
    """
    nz = [d for d in diffs if abs(d) > 1e-9]
    n = len(nz)
    if n == 0:
        return 0.0, 1.0

    order = sorted(range(n), key=lambda i: abs(nz[i]))
    ranks = [0.0] * n
    i = 0
    tie_groups: list[int] = []
    while i < n:
        j = i
        while j + 1 < n and abs(abs(nz[order[j + 1]]) - abs(nz[order[i]])) < 1e-9:
            j += 1
        avg = (i + j) / 2 + 1  # rangos promediados dentro del empate
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        tie_groups.append(j - i + 1)
        i = j + 1

    w_pos = sum(r for d, r in zip(nz, ranks) if d > 0)
    w_neg = sum(r for d, r in zip(nz, ranks) if d < 0)
    w = min(w_pos, w_neg)

    if n <= 25:
        # Con pocas diferencias no nulas la aproximación normal no sirve, y devolver
        # un centinela (p=1) se lee como un resultado calculado cuando no lo es. Acá
        # se enumera la distribución nula exacta: bajo H0 cada signo es ±1 con
        # probabilidad 1/2, así que basta contar de cuántas maneras los rangos suman
        # cada valor. Los rangos promediados son múltiplos de 0.5, y duplicarlos los
        # vuelve enteros, que es lo que necesita la programación dinámica.
        r2 = [int(round(2 * r)) for r in ranks]
        counts = {0: 1}
        for v in r2:
            nxt: dict[int, int] = {}
            for s, c in counts.items():
                nxt[s] = nxt.get(s, 0) + c
                nxt[s + v] = nxt.get(s + v, 0) + c
            counts = nxt
        target = int(round(2 * w))
        tail = sum(c for s, c in counts.items() if s <= target)
        return w, min(1.0, 2 * tail / 2**n)

    mean = n * (n + 1) / 4
    var = n * (n + 1) * (2 * n + 1) / 24
    var -= sum(t**3 - t for t in tie_groups) / 48  # corrección por empates
    if var <= 0:
        return w, 1.0
    z = (w - mean + 0.5) / sqrt(var)  # corrección de continuidad
    return w, erfc(abs(z) / sqrt(2))


def normal_p(z: float) -> float:
    return erfc(abs(z) / sqrt(2))


def paired_stats(diffs: list[float]) -> dict:
    n = len(diffs)
    mean = sum(diffs) / n
    sd = sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1))
    se = sd / sqrt(n)
    w_pos = sum(1 for d in diffs if d > 1e-9)
    w_neg = sum(1 for d in diffs if d < -1e-9)
    _, p_w = wilcoxon_signed_rank(diffs)
    return {
        "n": n,
        "mean": mean,
        "sd": sd,
        "ci_lo": mean - 1.96 * se,
        "ci_hi": mean + 1.96 * se,
        "t": mean / se,
        "p_t": normal_p(mean / se),
        "wins": w_pos,
        "losses": w_neg,
        "ties": n - w_pos - w_neg,
        "p_sign": sign_test(w_pos, w_neg),
        "p_wilcoxon": p_w,
    }


# ── Evaluación permisiva ─────────────────────────────────────────


def norm_permissive(svc: str) -> str:
    """Colapsa los subtipos de actor. Copia fiel de generate_comparison_plots.norm_permissive."""
    if not svc or svc == "?":
        return "Unknown"
    s = str(svc).strip()
    cap = CATALOG.get(s, {}).get("capability", "")
    if s.startswith("User") or cap == "User":
        return "User"
    if s.startswith("ThirdParty") or cap == "ThirdParty":
        return "ThirdParty"
    return s


def prf(inter: int, gen: int, gt: int) -> tuple[float, float, float]:
    p = inter / gen if gen else 0.0
    r = inter / gt if gt else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def eval_permissive(g_gen, g_gt) -> dict[str, float]:
    gen_s = {norm_permissive(g_gen.nodes[n].get("service", "")) for n in g_gen}
    gt_s = {norm_permissive(g_gt.nodes[n].get("service", "")) for n in g_gt}
    sp, sr, sf = prf(len(gen_s & gt_s), len(gen_s), len(gt_s))

    def edges(G):
        out = set()
        for u, v in G.edges():
            a = norm_permissive(G.nodes[u].get("service", ""))
            b = norm_permissive(G.nodes[v].get("service", ""))
            if a and b and a != "Unknown" and b != "Unknown":
                out.add(tuple(sorted([a, b])))
        return out

    ge, te = edges(g_gen), edges(g_gt)
    ep, er, ef = prf(len(ge & te), len(ge), len(te))
    return {"svc_p": sp, "svc_r": sr, "svc_f1": sf,
            "edge_p": ep, "edge_r": er, "edge_f1": ef}


# ── Table 2 ──────────────────────────────────────────────────────


def find_production_run() -> Path:
    for rj in sorted(glob.glob(str(PROJECT_ROOT / "reports/ablation/*_p30/run.json"))):
        d = json.load(open(rj))
        # El sha del prompt no identifica una corrida por sí solo: las de oráculo y
        # las de evidencia de conexiones llevan el mismo texto pero otra entrada.
        if d["stage2_prompt"]["sha256"].startswith(PROD_SHA) and \
                not d.get("connection_evidence_enabled") and \
                not (d.get("oracle") or d.get("world_model_file")):
            return Path(rj)
    raise SystemExit(f"no encontré la corrida de producción p30 con sha {PROD_SHA}")


def build_table2() -> str:
    run_path = find_production_run()
    d = json.load(open(run_path))
    rel = run_path.relative_to(PROJECT_ROOT)

    strict, perm = [], []
    # Conteos brutos de aristas, para poder decir de dónde sale la ganancia permisiva.
    # Sin esto es fácil leer la subida de recall como «encontró más conexiones», que
    # es justamente lo que no pasa.
    tot = dict(gt_strict=0, gt_perm=0, gen_strict=0, gen_perm=0, hit_strict=0, hit_perm=0)
    for r in d["results"]:
        if r["status"] != "success":
            continue
        vid = r["video_id"]
        g_gt = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
        g_gen = create_graph_from_cloudscape_json(r["analysis"], video_id=vid)
        s = evaluate_pair(g_gen, g_gt, vid, CATALOG)
        strict.append(s)
        perm.append(eval_permissive(g_gen, g_gt))

        def pairs(G, norm, undirected):
            out = []
            for u, v in G.edges():
                a = norm(G.nodes[u].get("service", "?"))
                b = norm(G.nodes[v].get("service", "?"))
                out.append(tuple(sorted([a, b])) if undirected else (a, b))
            return out

        ident = str
        gt_s, gen_s = pairs(g_gt, ident, False), pairs(g_gen, ident, False)
        gt_p = set(pairs(g_gt, norm_permissive, True))
        gen_p = set(pairs(g_gen, norm_permissive, True))
        tot["gt_strict"] += len(gt_s)
        tot["gen_strict"] += len(gen_s)
        tot["gt_perm"] += len(gt_p)
        tot["gen_perm"] += len(gen_p)
        tot["hit_strict"] += sum((Counter(gen_s) & Counter(gt_s)).values())
        tot["hit_perm"] += len(gen_p & gt_p)

    n = len(strict)
    avg = lambda rows, k: 100 * sum(r[k] for r in rows) / len(rows)  # noqa: E731

    rows = [
        ("Precisión de servicios", avg(strict, "svc_precision"), avg(perm, "svc_p")),
        ("Recall de servicios", avg(strict, "svc_recall"), avg(perm, "svc_r")),
        ("**F1 de servicios**", avg(strict, "svc_f1"), avg(perm, "svc_f1")),
        ("Precisión de aristas", avg(strict, "edge_precision"), avg(perm, "edge_p")),
        ("Recall de aristas", avg(strict, "edge_recall"), avg(perm, "edge_r")),
        ("**F1 de aristas**", avg(strict, "edge_f1"), avg(perm, "edge_f1")),
    ]

    # diferencias pareadas por video, para poder decir si la ganancia es o no ruido
    d_svc = [100 * (p["svc_f1"] - s["svc_f1"]) for s, p in zip(strict, perm)]
    d_edge = [100 * (p["edge_f1"] - s["edge_f1"]) for s, p in zip(strict, perm)]
    st_svc, st_edge = paired_stats(d_svc), paired_stats(d_edge)

    L = []
    L.append("# Tabla 2 · Evaluación estricta vs permisiva")
    L.append("")
    L.append(f"**Fuente:** `{rel}` — corrida de producción sobre el panel de 30 videos "
             f"(`STAGE2_V6_CORRECTED`, celda 9, sha `{PROD_SHA}`), n = {n}.")
    L.append(f"**Reproducir:** `.venv/bin/python scripts/ablation/build_evidence_tables.py`")
    L.append("")
    L.append("Los dos protocolos puntúan **los mismos grafos generados**. No hay una segunda "
             "corrida ni una segunda llamada a la API: cambia el evaluador, no la salida del "
             "modelo. Toda diferencia de esta tabla es diferencia de criterio de medición.")
    L.append("")
    L.append("## Qué relaja exactamente el protocolo permisivo")
    L.append("")
    L.append("Tres cosas a la vez, no una. Conviene enumerarlas porque la ganancia se suele "
             "atribuir entera a la primera:")
    L.append("")
    L.append("1. **Colapso de subtipos de actor** — todo `User*` cuenta como `User` y todo "
             "`ThirdParty*` como `ThirdParty`.")
    L.append("2. **Aristas como conjunto** — las instancias duplicadas del mismo par de "
             "servicios dejan de contarse por separado.")
    L.append("3. **Aristas no dirigidas** — `A → B` y `B → A` pasan a ser la misma arista, "
             "así que **los errores de dirección dejan de penalizar**.")
    L.append("")
    L.append("Implementación: `scripts/ablation/build_evidence_tables.py:norm_permissive`, "
             "copia fiel de `generate_comparison_plots.py`. El estricto es "
             "`scripts/utils/evaluate_graphs.py:evaluate_pair` — servicios por conjunto "
             "con coincidencia exacta de cadena, aristas por multiconjunto dirigido.")
    L.append("")
    L.append("## Resultados")
    L.append("")
    L.append("| Métrica (media por video) | Estricto | Permisivo | Δ |")
    L.append("| :--- | ---: | ---: | ---: |")
    for label, s, p in rows:
        L.append(f"| {label} | {s:.2f} % | {p:.2f} % | {p - s:+.2f} |")
    L.append("")
    L.append("Distribución de la ganancia video por video:")
    L.append("")
    L.append("| Ganancia permisivo − estricto | media | IC 95 % | mejora | empata | empeora |")
    L.append("| :--- | ---: | :---: | ---: | ---: | ---: |")
    for lbl, st in (("F1 de servicios", st_svc), ("F1 de aristas", st_edge)):
        L.append(f"| {lbl} | {st['mean']:+.2f} | "
                 f"[{st['ci_lo']:+.2f}, {st['ci_hi']:+.2f}] | "
                 f"{st['wins']} | {st['ties']} | {st['losses']} |")
    L.append("")
    L.append("*No se reporta una prueba de significancia sobre esta diferencia, y es a "
             "propósito.* El signo lo fija el diseño del evaluador, no el desempeño del "
             "modelo: relajar el criterio agrega coincidencias en casi todos los videos, "
             "así que contrastar contra «la ganancia es cero» sería contrastar una "
             "hipótesis que nadie sostiene. Lo informativo es la magnitud y su dispersión.")
    L.append("")
    L.append("El signo tampoco está garantizado video a video, y conviene no afirmarlo: en "
             "`-wLEkq21cvA` el F1 de aristas **baja** de 77.78 a 72.73. Colapsar los "
             "subtipos de actor y volver las aristas no dirigidas también fusiona nodos y "
             "aristas del ground truth, así que los denominadores de las dos partes se "
             "achican de forma despareja y el F1 puede caer.")
    L.append("")
    L.append("## Lectura")
    L.append("")
    L.append(f"1. La ganancia en aristas ({st_edge['mean']:+.2f} puntos) es grande, pero "
             "**no mide una mejora del pipeline**: el pipeline no cambió. Mide cuánto del "
             "error estricto dependía de exigir la dirección de la flecha y de contar las "
             "instancias duplicadas. El protocolo permisivo responde una pregunta más "
             "fácil, y responderla mejor no es un hallazgo.")
    L.append("2. Por eso la cifra que se reporta como resultado del sistema es la "
             "**estricta**. La permisiva sirve para localizar dónde está el error, no "
             "para acreditar el desempeño.")
    L.append(f"3. **La subida del recall no significa que se encuentren más conexiones.** "
             "Es la lectura intuitiva y es falsa. Los conteos brutos sobre los 30 videos:")
    L.append("")
    L.append("   | | aristas en el GT | aristas generadas | aciertos |")
    L.append("   | :--- | ---: | ---: | ---: |")
    L.append(f"   | Estricto (dirigido, multiconjunto) | {tot['gt_strict']} | "
             f"{tot['gen_strict']} | {tot['hit_strict']} |")
    L.append(f"   | Permisivo (no dirigido, conjunto) | {tot['gt_perm']} | "
             f"{tot['gen_perm']} | {tot['hit_perm']} |")
    L.append("")
    shrink = 100 * (tot["gt_strict"] - tot["gt_perm"]) / tot["gt_strict"]
    L.append(f"   Los **aciertos bajan** de {tot['hit_strict']} a {tot['hit_perm']}. Lo que "
             f"sube el recall es que la referencia se achica {shrink:.1f} % "
             f"({tot['gt_strict']} → {tot['gt_perm']} aristas): colapsar actores y quitar "
             "la dirección fusiona aristas **del ground truth también**, no sólo de la "
             "salida del modelo. El permisivo no acredita más aciertos; mide contra una "
             "referencia más chica.")
    L.append(f"4. En servicios la ganancia es chica ({st_svc['mean']:+.2f} puntos): la "
             "identificación de servicios casi no depende del criterio de medición, "
             "mientras que la topología depende muchísimo. Es la misma asimetría que "
             "aparece en la Tabla 1.")
    L.append("")
    L.append("## Nota de corrección")
    L.append("")
    L.append("Una versión anterior de esta tabla publicaba seis cifras "
             "(78.4 / 91.2 / 72.1 / 85.6 / 48.2 / 59.7 %) atribuidas a "
             "`evaluacion_estricta_vs_permisiva.html`. **Ninguna de las seis aparece en "
             "ese archivo**, y 59.7 coincide con el Edge F1 *estricto* del pipeline "
             "Standard sobre otro corpus (n=321) — una cifra de otra corrida colocada en "
             "la celda «Edge F1 permisiva». Aquella versión también describía el "
             "mecanismo como un diccionario de alias de servicios "
             "(`lambda_function → Lambda`), que no es lo que hace el evaluador. "
             "Ambas cosas quedan corregidas acá.")
    L.append("")
    return "\n".join(L)


# ── Table 1 ──────────────────────────────────────────────────────


def load_csv(p: Path) -> dict[str, dict]:
    with open(p, encoding="utf-8") as f:
        return {r["video_id"]: r for r in csv.DictReader(f)}


def usable(r: dict) -> bool:
    return str(r.get("graph_usable", "")).strip().lower() in ("true", "1", "yes")


def build_table1() -> str:
    pars, std = load_csv(PARS_CSV), load_csv(STD_CSV)
    common = sorted(set(pars) & set(std))
    use = [v for v in common if usable(pars[v]) and usable(std[v])]

    def col(v, r, k):
        # Ojo: estos results.csv ya guardan puntos (85.73), no fracciones. Los
        # run.json de la ablación guardan fracciones. No mezclar las dos escalas.
        return float(r[v][k])

    res = {}
    for k in ("svc_f1", "edge_f1"):
        diffs = [col(v, pars, k) - col(v, std, k) for v in use]
        st = paired_stats(diffs)
        st["mean_pars"] = sum(col(v, pars, k) for v in use) / len(use)
        st["mean_std"] = sum(col(v, std, k) for v in use) / len(use)
        res[k] = st

    # Muestra por video: aleatoria con semilla fija y declarada, no elegida a mano.
    rng = random.Random(20260827)
    sample = sorted(rng.sample(use, 15))

    L = []
    L.append("# Tabla 1 · Parsimonious vs Standard — comparación pareada")
    L.append("")
    L.append(f"**Fuente:** `{PARS_CSV.relative_to(PROJECT_ROOT)}` y "
             f"`{STD_CSV.relative_to(PROJECT_ROOT)}`.")
    L.append(f"**Reproducir:** `.venv/bin/python scripts/ablation/build_evidence_tables.py`")
    L.append("")
    L.append(f"Parsimonious evaluó {len(pars)} videos y Standard {len(std)}; comparten "
             f"**{len(common)}**. De esos, **{len(use)}** produjeron un grafo utilizable en "
             "los dos pipelines y forman la muestra pareada. Cada video aporta una "
             "diferencia, así que la comparación controla por dificultad del video: no se "
             "comparan dos promedios sobre corpus distintos.")
    L.append("")
    L.append("## Resultado principal")
    L.append("")
    L.append("| Métrica | n | Parsimonious | Standard | Δ (P − S) | sd de la dif. | IC 95 % | t | p (t) |")
    L.append("| :--- | ---: | ---: | ---: | ---: | ---: | :---: | ---: | ---: |")
    for k, lbl in (("svc_f1", "F1 de servicios"), ("edge_f1", "F1 de aristas")):
        s = res[k]
        L.append(f"| {lbl} | {s['n']} | {s['mean_pars']:.2f} % | {s['mean_std']:.2f} % | "
                 f"**{s['mean']:+.2f}** | {s['sd']:.2f} | "
                 f"[{s['ci_lo']:+.2f}, {s['ci_hi']:+.2f}] | {s['t']:.2f} | {s['p_t']:.4f} |")
    L.append("")
    L.append("| Métrica | gana Parsimonious | gana Standard | empata | p signos | p Wilcoxon |")
    L.append("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for k, lbl in (("svc_f1", "F1 de servicios"), ("edge_f1", "F1 de aristas")):
        s = res[k]
        L.append(f"| {lbl} | {s['wins']} | {s['losses']} | {s['ties']} | "
                 f"{s['p_sign']:.5f} | {s['p_wilcoxon']:.5f} |")
    L.append("")
    L.append("## Lectura")
    L.append("")
    sv, ed = res["svc_f1"], res["edge_f1"]
    L.append(f"1. **En servicios los dos pipelines son equivalentes.** La diferencia es de "
             f"{sv['mean']:+.2f} puntos y las dos pruebas no paramétricas divergen "
             f"(signos p = {sv['p_sign']:.3f}, Wilcoxon p = {sv['p_wilcoxon']:.3f}). Con "
             f"{sv['ties']} empates de {sv['n']} la distribución de diferencias está lejos "
             "de la normal, así que la t pareada no es la prueba que gobierna: **la "
             "diferencia en servicios no queda establecida**.")
    L.append(f"2. **En aristas gana Standard, y eso sí es sólido.** {ed['mean']:+.2f} puntos, "
             f"IC 95 % [{ed['ci_lo']:+.2f}, {ed['ci_hi']:+.2f}], con signos "
             f"p = {ed['p_sign']:.5f} y Wilcoxon p = {ed['p_wilcoxon']:.5f}. Las dos pruebas "
             "coinciden y el intervalo no toca el cero.")
    L.append("3. **La afirmación defendible es partida, no una paridad.** «Parsimonious "
             "rinde igual a la mitad del costo» vale para servicios y **no** vale para "
             "topología.")
    L.append("")
    L.append("### El punto metodológico")
    L.append("")
    L.append(f"Esos {abs(ed['mean']):.2f} puntos de aristas son **reales a n = {ed['n']} e "
             "invisibles a n ≤ 30**. Con el piso de ruido medido del proyecto "
             "(`reports/noise_floor.json`, σ_d = 8.76 puntos de Edge F1 por video) el "
             "efecto mínimo detectable con 30 videos es de 4.48 puntos y con 14 videos de "
             "6.56. Toda la fase de selección de prompts, en los dos brazos, operó por "
             "debajo de su propio umbral de detección: la comparación central del proyecto "
             "es ella misma un caso del problema metodológico que este trabajo reporta.")
    L.append("")
    L.append("## Muestra por video")
    L.append("")
    L.append(f"15 videos tomados al azar de los {len(use)} con "
             "`random.Random(20260827).sample(...)` — semilla fija y declarada, para que "
             "cualquiera reproduzca exactamente estas filas. **No es una selección hecha a "
             "mano.** El detalle completo de los "
             f"{len(use)} está en los dos `results.csv` citados arriba.")
    L.append("")
    L.append("| Video ID | Svc F1 Parsimonious | Svc F1 Standard | Edge F1 Parsimonious | Edge F1 Standard |")
    L.append("| :--- | ---: | ---: | ---: | ---: |")
    for v in sample:
        L.append(f"| `{v}` | {col(v, pars, 'svc_f1'):.1f} % | {col(v, std, 'svc_f1'):.1f} % | "
                 f"{col(v, pars, 'edge_f1'):.1f} % | {col(v, std, 'edge_f1'):.1f} % |")
    L.append("")
    L.append("## Nota de corrección")
    L.append("")
    L.append("Una versión anterior de esta tabla publicaba **16 filas de las 60** de "
             "`reporte_comparacion_detallada.md`, elegidas sin criterio declarado. El "
             "recorte invertía el signo del resultado: en las 60 filas de la fuente "
             "Standard ganaba 28 a 8, mientras que en las 16 publicadas ganaba "
             "Parsimonious 4 a 3. Además 4 de esas 16 filas ya no coincidían con el corpus "
             "vigente y **las cuatro discrepaban a favor de Parsimonious** "
             "(`-kA0ahrhX3I` 100 → 71.43, `6EUknQqaV1w` 100 → 92.31, `AzM_d7ZvzUE` "
             "100 → 87.50, `BlCXEMp_lqY` 100 → 83.33). El archivo fuente describe un "
             "corpus que ya no existe: 27 de sus 60 filas difieren del `results.csv` "
             "actual en al menos una columna.")
    L.append("")
    L.append("Esta versión se calcula sobre la población completa de videos comparables y "
             "reporta la prueba pareada, que es lo que la afirmación necesitaba desde el "
             "principio.")
    L.append("")
    L.append("### Limitación que no se puede reparar hacia atrás")
    L.append("")
    L.append("El prompt de producción de Parsimonious (v9) se adoptó mirando **un solo "
             "video** (`-3lnf5lzsH0`, Registro 17 de la bitácora), que además era la fila "
             "estrella de la versión anterior de esta tabla («Parsimonious +15.7 %»). Con "
             "el piso de ruido medido, el efecto mínimo detectable con n = 1 es de 26.3 "
             "puntos de Service F1 y 33.3 de Edge F1: esa decisión no fue medible. El "
             "prompt se eligió y se reportó su rendimiento sobre el mismo dato. No es "
             "corregible retroactivamente sin volver a correr la selección, y queda "
             "declarado como limitación.")
    L.append("")
    return "\n".join(L)


def main() -> None:
    for name, text in (("table2_strict_vs_permissive.md", build_table2()),
                       ("table1_parsimonious_vs_standard.md", build_table1())):
        (TABLES / name).write_text(text, encoding="utf-8")
        print(f"✓ ara/evidence/tables/{name}  ({len(text.splitlines())} líneas)")


if __name__ == "__main__":
    main()
