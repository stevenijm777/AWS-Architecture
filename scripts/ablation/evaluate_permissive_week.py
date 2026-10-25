#!/usr/bin/env python3
"""
evaluate_permissive_week.py — Protocolo permisivo sobre las corridas de la semana del 8 de octubre.

Qué hace
--------
Vuelve a puntuar, sin llamar a ningún modelo, todas las corridas de modelos, oráculos y
prompt V9 (las que usan los notebooks de hipotesis/) y las lecturas de Stage 1, bajo el
protocolo permisivo del paper. Para ver de dónde sale cada punto, aplica las tres reglas
de una en una y en el mismo orden que la Figura del protocolo:

    estricto   pares dirigidos, multiconjunto, servicio exacto (lo que da el evaluador)
    + regla i  todo `User*` cuenta como `User` y todo `ThirdParty*` como `ThirdParty`
    + regla ii aristas como conjunto: los pares repetidos cuentan una vez
    + regla iii aristas sin dirección

La normalización de servicios es la de `evaluate_permissive_panel.norm_permissive`, así que
el resultado con las tres reglas es comparable con `reports/permissive_panel.json`.

Uso
---
    .venv/Scripts/python scripts/ablation/evaluate_permissive_week.py
"""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.ablation.compare_models import bootstrap_ci, sign_test  # noqa: E402
from scripts.ablation.evaluate_permissive_panel import norm_permissive  # noqa: E402

REP = PROJECT_ROOT / "reports"
GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
OUT = REP / "permisivo_semana"
_A, _P, _V = REP / "ablation", REP / "pro_vs_flash", REP / "prompt_v9"

# (condición, modelo, prompt, corrida) → directorio con run.json
RUNS = {
    ("Producción", "Flash", "V6", 1): _P / "flash_gemini-3.6-flash",
    ("Producción", "Pro", "V6", 1): _P / "pro_gemini-3.1-pro-preview",
    ("Producción", "Flash", "V9", 1): _V / "flash_produccion",
    ("Producción", "Flash", "V9", 2): _V / "flash_produccion_rep2",
    ("Brazo A", "Flash", "V6", 1): _P / "flash_gemini-3.6-flash_stage1-manual",
    ("Brazo A", "Flash", "V6", 2): _A / "2026-08-29_0725_STAGE2_V6_CORRECTED_cell9_p30_oracle-vision",
    ("Brazo A", "Pro", "V6", 1): _P / "pro_gemini-3.1-pro-preview_stage1-manual",
    ("Brazo A", "Claude", "V6", 1): REP / "claude",
    ("Brazo A", "Flash", "V9", 1): _V / "flash_stage1-manual",
    ("Brazo A", "Flash", "V9", 2): _V / "flash_stage1-manual_rep2",
    ("Brazo B", "Flash", "V6", 1): _A / "2026-08-28_0315_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt",
    ("Brazo B", "Flash", "V6", 2): _A / "2026-08-28_2211_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt_rep2",
    ("Brazo B", "Pro", "V6", 1): _P / "pro_gemini-3.1-pro-preview_oracle-gt",
    ("Brazo B", "Pro", "V6", 2): _P / "pro_gemini-3.1-pro-preview_oracle-gt_rep2",
    ("Brazo B", "Claude", "V6", 1): REP / "claude_oracle_gt",
    ("Brazo B", "Flash", "V6 sin unidir.", 1): _V / "flash_oracle-gt_v6-sin-unidireccional",
    ("Brazo B", "Flash", "V9", 1): _V / "flash_oracle-gt",
    ("Brazo B", "Flash", "V9", 2): _V / "flash_oracle-gt_rep2",
    ("Brazo B", "Pro", "V9", 1): _V / "pro_oracle-gt",
    ("Brazo B", "Pro", "V9", 2): _V / "pro_oracle-gt_rep2",
    ("Brazo B", "Claude", "V9", 1): REP / "claude_oracle_gt_v9",
    ("Brazo B", "Claude", "V9", 2): REP / "claude_oracle_gt_v9_rep2",
    ("Brazo B solo WM", "Flash", "V6", 1): _P / "flash_gemini-3.6-flash_oracle-gt_solo-wm",
    ("Brazo B solo WM", "Pro", "V6", 1): _P / "pro_gemini-3.1-pro-preview_oracle-gt_solo-wm",
    ("Brazo B solo WM", "Pro", "V6", 2): _P / "pro_gemini-3.1-pro-preview_oracle-gt_solo-wm_rep2",
    ("Brazo B solo WM", "Flash", "V9", 1): _V / "flash_oracle-gt_solo-wm",
}
# Lecturas de Stage 1 (World Models): nombre → archivo world_model_<nombre>.json
LECTURAS = {
    "Persona · pizarra": "vision", "Flash · pizarra + audio": "s1-flash", "Pro · pizarra + audio": "s1-pro",
    "Flash · pizarra": "s1-flash-img", "Pro · pizarra": "s1-pro-img",
}
NIVELES = ["estricto", "+ regla i", "+ regla ii", "+ regla iii"]


def gt(vid: str) -> tuple[list, list]:
    G = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
    svc = lambda n: G.nodes[n].get("service", "?")
    return [svc(n) for n in G.nodes], [(svc(u), svc(v)) for u, v in G.edges()]


def de_analysis(a: dict) -> tuple[list, list]:
    svc = {n["id"]: n["service"] for n in a["nodes"]}
    return list(svc.values()), [(svc.get(e["source"], "?"), svc.get(e["target"], "?")) for e in a["edges"]]


def de_world_model(wm: dict) -> tuple[list, list]:
    res = {}
    for e in wm.get("entities", []):
        for k in (e.get("name"), e.get("service")):
            if k:
                res.setdefault(k.strip().lower(), e["service"])
    pares = [(res.get((c.get("source_label") or "").strip().lower()), res.get((c.get("target_label") or "").strip().lower()))
             for c in wm.get("visual_connections", [])]
    return [e["service"] for e in wm.get("entities", [])], [p for p in pares if p[0] and p[1]]


def f1(a: Counter, b: Counter) -> float:
    inter = sum((a & b).values())
    tot = sum(a.values()) + sum(b.values())
    return 2 * inter / tot if tot else 0.0


def puntuar(nodos, aristas, nodos_gt, aristas_gt) -> dict:
    """F1 de servicios y de aristas en los cuatro niveles, más precisión y recall del último."""
    out = {}
    for nivel in range(4):
        norm = norm_permissive if nivel >= 1 else (lambda s: s)

        def red(pares):
            ps = [(norm(a), norm(b)) for a, b in pares]
            if nivel >= 3:
                ps = [tuple(sorted(p)) for p in ps]
            c = Counter(ps)
            return Counter(set(c)) if nivel >= 2 else c

        g, t = red(aristas), red(aristas_gt)
        out[f"edge_{nivel}"] = f1(g, t)
        out[f"svc_{nivel}"] = f1(Counter({norm(s) for s in nodos}), Counter({norm(s) for s in nodos_gt}))
        if nivel == 3:
            inter = sum((g & t).values())
            out["edge_p"] = inter / sum(g.values()) if g else 0.0
            out["edge_r"] = inter / sum(t.values()) if t else 0.0
    return out


def media(filas: dict, k: str) -> float:
    return 100 * st.mean(r[k] for r in filas.values())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    res = {}
    for clave, path in RUNS.items():
        rj = path / "run.json"
        if not rj.exists():
            print(f"(sin run.json: {path.relative_to(PROJECT_ROOT)})")
            continue
        run = json.loads(rj.read_text(encoding="utf-8"))
        filas = {}
        for r in run["results"]:
            if r.get("status") != "success":
                continue
            n, e = de_analysis(r["analysis"])
            filas[r["video_id"]] = {**puntuar(n, e, *gt(r["video_id"])), "strict_eval": r["edge_f1"]}
        res[clave] = filas
    videos = list(next(iter(res.values())))
    lect = {}
    for nombre, wm in LECTURAS.items():
        if all((LAB / v / f"world_model_{wm}.json").exists() for v in videos):
            lect[nombre] = {v: puntuar(*de_world_model(json.loads((LAB / v / f"world_model_{wm}.json").read_text(encoding="utf-8"))), *gt(v))
                            for v in videos}

    L = ["# Protocolo permisivo sobre las corridas de la semana (panel de 30)", "",
         "Las reglas se acumulan de izquierda a derecha: (i) colapsa subtipos de `User*` y `ThirdParty*`; "
         "(ii) cuenta cada par una sola vez; (iii) ignora la dirección. «Estricto» es lo que reporta el evaluador.", "",
         "## Corridas de Stage 2", "",
         "| condición | modelo | prompt | corrida | svc estr. | svc perm. | aristas estr. | + i | + ii | + iii | P perm. | R perm. | ganancia |",
         "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for (cond, modelo, prompt, rep), f in res.items():
        L.append(f"| {cond} | {modelo} | {prompt} | {rep} | {media(f, 'svc_0'):.2f} | {media(f, 'svc_3'):.2f} | "
                 f"{media(f, 'edge_0'):.2f} | {media(f, 'edge_1'):.2f} | {media(f, 'edge_2'):.2f} | {media(f, 'edge_3'):.2f} | "
                 f"{media(f, 'edge_p'):.1f} | {media(f, 'edge_r'):.1f} | {media(f, 'edge_3') - media(f, 'edge_0'):+.2f} |")
    L += ["", "## Lecturas de Stage 1 contra el ground truth", "",
          "| lectura | svc estr. | svc perm. | conexiones estr. | + i | + ii | + iii | P perm. | R perm. | ganancia |",
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for nombre, f in lect.items():
        L.append(f"| {nombre} | {media(f, 'svc_0'):.2f} | {media(f, 'svc_3'):.2f} | {media(f, 'edge_0'):.2f} | "
                 f"{media(f, 'edge_1'):.2f} | {media(f, 'edge_2'):.2f} | {media(f, 'edge_3'):.2f} | "
                 f"{media(f, 'edge_p'):.1f} | {media(f, 'edge_r'):.1f} | {media(f, 'edge_3') - media(f, 'edge_0'):+.2f} |")

    # Las comparaciones que el estricto dejó sin efecto: ¿aparece algo debajo?
    comparaciones = [
        ("Brazo A · Pro − Flash", res.get(("Brazo A", "Flash", "V6", 1)), res.get(("Brazo A", "Pro", "V6", 1))),
        ("Brazo A · Claude − Flash", res.get(("Brazo A", "Flash", "V6", 1)), res.get(("Brazo A", "Claude", "V6", 1))),
        ("Brazo A · Flash réplica − Flash (ruido)", res.get(("Brazo A", "Flash", "V6", 1)), res.get(("Brazo A", "Flash", "V6", 2))),
        ("Brazo A · V9 − V6 (Flash)", res.get(("Brazo A", "Flash", "V6", 1)), res.get(("Brazo A", "Flash", "V9", 1))),
        ("Producción · V9 − V6 (Flash)", res.get(("Producción", "Flash", "V6", 1)), res.get(("Producción", "Flash", "V9", 1))),
        ("Producción · Pro − Flash", res.get(("Producción", "Flash", "V6", 1)), res.get(("Producción", "Pro", "V6", 1))),
        ("Brazo A − Producción (Flash, V6)", res.get(("Producción", "Flash", "V6", 1)), res.get(("Brazo A", "Flash", "V6", 1))),
        ("Brazo B · V9 − V6 (Flash)", res.get(("Brazo B", "Flash", "V6", 1)), res.get(("Brazo B", "Flash", "V9", 1))),
        ("Brazo B · Pro − Flash (V6)", res.get(("Brazo B", "Flash", "V6", 1)), res.get(("Brazo B", "Pro", "V6", 1))),
        ("Stage 1 · Pro − Flash (pizarra)", lect.get("Flash · pizarra"), lect.get("Pro · pizarra")),
        ("Stage 1 · Persona − Flash (pizarra)", lect.get("Flash · pizarra"), lect.get("Persona · pizarra")),
        ("Stage 1 · Persona − Pro (pizarra)", lect.get("Pro · pizarra"), lect.get("Persona · pizarra")),
    ]
    L += ["", "## Diferencias pareadas (B − A) en F1 de aristas: estricto frente a permisivo", "",
          "| comparación | Δ estricto | IC 95 % | Δ permisivo | IC 95 % | gana / pierde / empata (perm.) | p (signos) |",
          "|---|---:|:---:|---:|:---:|:---:|---:|"]
    pares_out = []
    for nombre, A, B in comparaciones:
        if not A or not B:
            continue
        fila = {"comparacion": nombre}
        celdas = []
        for nivel in (0, 3):
            d = [100 * (B[v][f"edge_{nivel}"] - A[v][f"edge_{nivel}"]) for v in videos]
            lo, hi = bootstrap_ci(d)
            fila[f"nivel_{nivel}"] = {"diff": st.mean(d), "ci95": [lo, hi]}
            celdas += [f"{st.mean(d):+.2f}", f"[{lo:+.2f}, {hi:+.2f}]"]
        pos, neg, ties, p = sign_test(d)
        L.append(f"| {nombre} | " + " | ".join(celdas) + f" | {pos} / {neg} / {ties} | {p:.3f} |")
        pares_out.append(fila)

    texto = "\n".join(L) + "\n"
    print(texto)
    (OUT / "permisivo_semana.md").write_text(texto, encoding="utf-8")
    (OUT / "permisivo_semana.json").write_text(json.dumps({
        "niveles": NIVELES,
        "corridas": [{"condicion": k[0], "modelo": k[1], "prompt": k[2], "corrida": k[3],
                      "carpeta": str(RUNS[k].relative_to(PROJECT_ROOT)).replace("\\", "/"),
                      "medias": {m: media(f, m) for m in ("svc_0", "svc_3", "edge_0", "edge_1", "edge_2", "edge_3", "edge_p", "edge_r")},
                      "videos": f} for k, f in res.items()],
        "lecturas": [{"lectura": n, "medias": {m: media(f, m) for m in ("svc_0", "svc_3", "edge_0", "edge_1", "edge_2", "edge_3")},
                      "videos": f} for n, f in lect.items()],
        "comparaciones": pares_out,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    # Control: el nivel estricto recalculado debe coincidir con el F1 que guardó el evaluador.
    dist = sum(abs(r["edge_0"] - r["strict_eval"]) > 1e-6 for f in res.values() for r in f.values())
    tot = sum(len(f) for f in res.values())
    print(f"Control: el estricto recalculado coincide con el del evaluador en {tot - dist} de {tot} filas.")
    print(f"✓ {(OUT / 'permisivo_semana.md').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
