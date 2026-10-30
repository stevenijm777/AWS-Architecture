#!/usr/bin/env python3
"""
estadistica.py — Comparación pareada de una configuración contra la línea base.

Reutiliza de compare_models.py la prueba de signos exacta y el IC por bootstrap. Agrega:
  - Wilcoxon de rangos con signo, exacto: distribución por permutación de signos con los
    rangos promediados en empates (sin aproximación normal; n ≤ 30 es enumerable).
  - Â12 de Vargha-Delaney: P(B > A) + ½ P(B = A) sobre todos los pares de videos.
  - |Δ| frente al MDE de 3,29 puntos del panel de 30.

Las corridas pueden ser run.json del orquestador o de rerun_panel (mismo formato de filas).

    .venv/Scripts/python -m multiagent.estadistica --a <línea base> --b <corrida> [--b ...]
"""
from __future__ import annotations

import argparse
import json
import statistics as st
from collections import Counter

from scripts.ablation.compare_models import bootstrap_ci, load_run, sign_test

MDE = 3.29


def wilcoxon(d: list[float]) -> tuple[float, float]:
    """(W+, p bilateral exacto)."""
    x = [v for v in d if abs(v) > 1e-12]
    n = len(x)
    if n == 0:
        return 0.0, 1.0
    orden = sorted(range(n), key=lambda i: abs(x[i]))
    rangos = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs(abs(x[orden[j + 1]]) - abs(x[orden[i]])) < 1e-12:
            j += 1
        for t in range(i, j + 1):
            rangos[orden[t]] = (i + j) / 2 + 1
        i = j + 1
    w_mas = sum(r for r, v in zip(rangos, x) if v > 0)
    dobles = [round(2 * r) for r in rangos]             # rangos enteros para la convolución
    dist = Counter({0: 1})
    for r in dobles:
        nueva = Counter()
        for s, c in dist.items():
            nueva[s] += c
            nueva[s + r] += c
        dist = nueva
    total = 2 ** n
    centro = sum(dobles) / 2
    obs = abs(2 * w_mas - centro)
    p = sum(c for s, c in dist.items() if abs(s - centro) >= obs - 1e-9) / total
    return w_mas, min(1.0, p)


def a12(a: list[float], b: list[float]) -> float:
    gana = sum((y > x) + 0.5 * (y == x) for x in a for y in b)
    return gana / (len(a) * len(b))


def comparar(base: dict, otra: dict, metrica: str) -> dict:
    ids = sorted(set(base["_by_id"]) & set(otra["_by_id"]))
    a = [100 * base["_by_id"][v][metrica] for v in ids]
    b = [100 * otra["_by_id"][v][metrica] for v in ids]
    d = [y - x for x, y in zip(a, b)]
    lo, hi = bootstrap_ci(d)
    gana_b, gana_a, empates, p_signos = sign_test(d)
    w, p_w = wilcoxon(d)
    delta = st.mean(d)
    return {"n": len(ids), "base": round(st.mean(a), 2), "otra": round(st.mean(b), 2),
            "delta": round(delta, 2), "ic95": [round(lo, 2), round(hi, 2)],
            "signos": {"mejora": gana_b, "empeora": gana_a, "empates": empates, "p": round(p_signos, 4)},
            "wilcoxon": {"W+": w, "p": round(p_w, 4)}, "a12": round(a12(a, b), 3),
            "supera_mde": abs(delta) >= MDE}


def main() -> None:
    ap = argparse.ArgumentParser(description="Comparación pareada contra la línea base")
    ap.add_argument("--a", required=True, help="línea base (dir o run.json)")
    ap.add_argument("--b", required=True, nargs="+", help="corridas a comparar; se reporta B − A")
    ap.add_argument("--metricas", nargs="+", default=["edge_f1", "svc_f1", "edge_type_accuracy"])
    ap.add_argument("--out", default=None, help="json de salida")
    args = ap.parse_args()

    base = load_run(args.a)
    salida = {}
    for ruta_b in args.b:
        otra = load_run(ruta_b)
        salida[ruta_b] = {}
        for m in args.metricas:
            if not all(m in r for r in list(base["_by_id"].values()) + list(otra["_by_id"].values())):
                continue
            r = comparar(base, otra, m)
            salida[ruta_b][m] = r
            print(f"{ruta_b} · {m}: {r['base']:.2f} → {r['otra']:.2f}  Δ {r['delta']:+.2f} "
                  f"IC95 [{r['ic95'][0]:+.2f}, {r['ic95'][1]:+.2f}]  signos {r['signos']['mejora']}/"
                  f"{r['signos']['empeora']}/{r['signos']['empates']} p={r['signos']['p']:.3f}  "
                  f"Wilcoxon p={r['wilcoxon']['p']:.3f}  Â12={r['a12']:.2f}  "
                  f"{'≥' if r['supera_mde'] else '<'} MDE {MDE}  (n={r['n']})")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(salida, fh, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
