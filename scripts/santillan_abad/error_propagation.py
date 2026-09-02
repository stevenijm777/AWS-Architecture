#!/usr/bin/env python3
"""
error_propagation.py — ¿Cuánto distorsiona nuestro error de extracción las conclusiones?

La actualización del análisis de Santillán y Abad usa el ground truth para las 396
arquitecturas de Cloudscape y sólo aporta extracción propia en las 61 nuevas. Eso
responde "¿cambian sus conclusiones al sumar 2024?", pero deja abierta otra pregunta:
si el análisis se corriera enteramente sobre salida de nuestro pipeline, ¿daría lo
mismo?

Se puede responder sin gastar una sola llamada a la API, porque hay 385 arquitecturas
donde existen las dos versiones: la anotada a mano por UW–Madison y la que extrajo el
pipeline. Correr el análisis de los autores sobre cada una y comparar aísla el efecto
del error de extracción, con el corpus fijo: mismos videos, mismo código, misma
clasificación. Lo único que cambia es quién leyó la pizarra.

Es la validación que un F1 no da. Un F1 dice cuántos servicios se acertaron; esto dice
si esos errores mueven las conclusiones que un investigador publicaría.

Escribe `docs/propagacion-error-santillan-abad.md`.

Uso
---
    python scripts/santillan_abad/error_propagation.py
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from _paths import find_pkg  # noqa: E402

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent.parent
PKG = find_pkg()
GT, EX = PKG / "run_gt385", PKG / "run_extracted385"
SALIDA = PROJECT / "docs" / "propagacion-error-santillan-abad.md"

ORDEN = ["HPC", "Edge", "Edge+HPC", "None"]


def etiquetadas(d: Path) -> pd.DataFrame:
    x = pd.read_pickle(d / "arquitecturas_etiquetadas.pkl")
    x["tipo_arquitectura"] = x["tipo_arquitectura"].astype(str)
    return x


def main() -> None:
    g, e = etiquetadas(GT), etiquetadas(EX)
    n = len(g)
    assert len(e) == n, f"los corpus no son pareados: {n} vs {len(e)}"

    tg = dict(zip(g["architecture"], g["tipo_arquitectura"]))
    te = dict(zip(e["architecture"], e["tipo_arquitectura"]))
    vids = sorted(set(tg) & set(te))
    iguales = sum(1 for v in vids if tg[v] == te[v])

    L: list[str] = []
    L.append("# ¿Cuánto distorsiona nuestro error de extracción las conclusiones?")
    L.append("")
    L.append(f"Hay **{n} arquitecturas** donde existen las dos versiones: la anotada a "
             "mano por UW–Madison y la que extrajo nuestro pipeline. Se corrió el "
             "análisis de Santillán y Abad sobre cada una por separado.")
    L.append("")
    L.append("Mismos videos, mismo código, misma clasificación automática. Lo único que "
             "cambia es **quién leyó la pizarra**. Toda diferencia de este documento es "
             "error de extracción propagado a las conclusiones — no es un F1, es el "
             "efecto de ese F1 sobre lo que un investigador publicaría.")
    L.append("")
    L.append("**Reproducir:** `python scripts/santillan_abad/error_propagation.py`")
    L.append("")

    # ── clasificación ──
    cg, ce = g["tipo_arquitectura"].value_counts(), e["tipo_arquitectura"].value_counts()
    L.append("## Clasificación HPC / edge")
    L.append("")
    L.append(f"| Grupo | anotación humana | extracción automática | Δ |")
    L.append("| :--- | ---: | ---: | ---: |")
    for t in ORDEN:
        a, b = int(cg.get(t, 0)), int(ce.get(t, 0))
        L.append(f"| {t} | {a} ({100*a/n:.1f} %) | {b} ({100*b/n:.1f} %) | {b-a:+d} |")
    L.append("")
    L.append(f"**Coincidencia arquitectura por arquitectura: {iguales}/{len(vids)} "
             f"({100*iguales/len(vids):.1f} %).** Es el número que importa: no que los "
             "totales se parezcan, sino que cada arquitectura caiga en el mismo grupo.")
    L.append("")
    desac = [(v, tg[v], te[v]) for v in vids if tg[v] != te[v]]
    if desac:
        L.append(f"Las {len(desac)} que no coinciden:")
        L.append("")
        L.append("| Video | humano | automático |")
        L.append("| :--- | :--- | :--- |")
        for v, a, b in desac[:25]:
            L.append(f"| `{v}` | {a} | {b} |")
        if len(desac) > 25:
            L.append(f"| … | | *{len(desac)-25} más* |")
        L.append("")
        mov = Counter(f"{a} → {b}" for _, a, b in desac)
        L.append("Direcciones del desacuerdo: " +
                 " · ".join(f"**{k}** {v}" for k, v in mov.most_common()) + ".")
        L.append("")

    # ── servicios más frecuentes ──
    L.append("## Servicios más frecuentes (RQ1–RQ2)")
    L.append("")
    L.append("Lo que un lector se lleva del paper es el ranking, no el conteo exacto. "
             "La pregunta útil es si el ranking sobrevive.")
    L.append("")
    for t in ORDEN:
        fg = Counter(s for l in g[g["tipo_arquitectura"] == t]["services"] for s in l)
        fe = Counter(s for l in e[e["tipo_arquitectura"] == t]["services"] for s in l)
        if not fe or not fg:
            continue
        rg = [s for s, _ in fg.most_common(10)]
        re_ = [s for s, _ in fe.most_common(10)]
        coinciden = len(set(rg) & set(re_))
        L.append(f"### {t} — {coinciden}/10 servicios en común en el top 10")
        L.append("")
        L.append("| # | humano | | automático | |")
        L.append("| ---: | :--- | ---: | :--- | ---: |")
        for i in range(10):
            a = rg[i] if i < len(rg) else "—"
            b = re_[i] if i < len(re_) else "—"
            va = str(fg[a]) if a != "—" else ""
            vb = str(fe[b]) if b != "—" else ""
            marca = "" if b in rg or b == "—" else " ⚠"
            L.append(f"| {i+1} | {a} | {va} | {b}{marca} | {vb} |")
        L.append("")

    # ── servicios por arquitectura ──
    L.append("## Servicios por arquitectura (Fig. 5)")
    L.append("")
    L.append("| Grupo | media humana | media automática | Δ |")
    L.append("| :--- | ---: | ---: | ---: |")
    for t in ORDEN:
        sg = g[g["tipo_arquitectura"] == t]["services"].apply(len)
        se = e[e["tipo_arquitectura"] == t]["services"].apply(len)
        if not len(sg) or not len(se):
            continue
        L.append(f"| {t} | {sg.mean():.2f} | {se.mean():.2f} | {se.mean()-sg.mean():+.2f} |")
    L.append("")

    # ── almacenamiento y ML ──
    for f, titulo in (("porcentaje_almacenamiento_por_tipo_arquitectura.csv",
                       "Almacenamiento (RQ3)"),
                      ("ml_por_tipo_arquitectura.csv", "Machine learning (RQ4)")):
        if not (GT / f).exists() or not (EX / f).exists():
            continue
        xg, xe = pd.read_csv(GT / f, index_col=0), pd.read_csv(EX / f, index_col=0)
        cols = [c for c in xe.columns if c in xg.columns]
        L.append(f"## {titulo}")
        L.append("")
        L.append("| | " + " | ".join(str(c) for c in cols) + " |")
        L.append("| :--- | " + " | ".join("---:" for _ in cols) + " |")
        for idx in xe.index:
            if idx not in xg.index:
                continue
            etiq = "None" if str(idx).lower() in ("nan", "none") else str(idx)
            fila = []
            for c in cols:
                try:
                    fila.append(f"{float(xg.loc[idx, c]):.1f} → {float(xe.loc[idx, c]):.1f}")
                except (TypeError, ValueError):
                    fila.append(f"{xg.loc[idx, c]} → {xe.loc[idx, c]}")
            L.append(f"| {etiq} | " + " | ".join(fila) + " |")
        L.append("")

    L.append("## Cómo leer esto")
    L.append("")
    L.append("Este documento **no valida el pipeline** — para eso está el F1 contra el "
             "ground truth. Valida algo distinto y más útil para el artículo: si los "
             "errores del pipeline **cambian las conclusiones** que se publicarían.")
    L.append("")
    L.append("Un pipeline puede tener 86 % de F1 y aun así reproducir el ranking de "
             "servicios entero, si los errores se reparten en la cola. O puede tener el "
             "mismo 86 % y romper el ranking, si se concentran en los servicios "
             "frecuentes. La diferencia importa y el F1 solo no la distingue.")
    L.append("")
    L.append("Límite de este análisis: cubre lo que depende del **conjunto de "
             "servicios**. No cubre workflows (RQ7), que dependen de las aristas, donde "
             "el pipeline mide 59.7 % de F1 contra 86.8 % en servicios.")
    L.append("")

    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print(f"✓ {SALIDA.relative_to(PROJECT)}")
    print(f"  {n} arquitecturas pareadas · clasificación idéntica "
          f"{iguales}/{len(vids)} ({100*iguales/len(vids):.1f} %)")


if __name__ == "__main__":
    main()
