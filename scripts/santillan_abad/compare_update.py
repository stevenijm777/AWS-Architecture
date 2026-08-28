#!/usr/bin/env python3
"""
compare_update.py — Antes/después de actualizar el análisis de Santillán y Abad.

Compara las dos corridas del notebook de los autores: la base (396 arquitecturas de
Cloudscape, que reproduce el paper publicado) contra la extendida (457, con las 61
que extrajo nuestro pipeline). El código del análisis es el mismo en las dos; lo
único que cambia es el directorio de graphml, así que toda diferencia es del corpus.

Escribe `docs/actualizacion-santillan-abad.md`.

Uso
---
    $SA_VENV/bin/python scripts/santillan_abad/compare_update.py

Requiere el entorno con versiones fijadas del análisis (ver requirements.txt de
scripts/santillan_abad/), no el venv del pipeline: los pickles los escribe pandas
2.1.4 y leerlos con otra versión no está garantizado.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parent.parent.parent
PKG = Path("/home/stemjara/Projects/hpc-and-edge-cloud-architectures/Workshop_paper")
BASE, EXT = PKG / "run_local", PKG / "run_extended"
GT_DIR = PROJECT / "data" / "cloudscape_gt"
SALIDA = PROJECT / "docs" / "actualizacion-santillan-abad.md"

ORDEN = ["HPC", "Edge", "Edge+HPC", "None"]


def etiquetadas(d: Path) -> pd.DataFrame:
    x = pd.read_pickle(d / "arquitecturas_etiquetadas.pkl")
    x["tipo_arquitectura"] = x["tipo_arquitectura"].astype(str)
    return x


def pct(n: int, tot: int) -> str:
    return f"{100 * n / tot:.1f} %"


def main() -> None:
    b, e = etiquetadas(BASE), etiquetadas(EXT)
    nb, ne = len(b), len(e)
    gt = {p.stem for p in GT_DIR.glob("*.graphml")}
    nuevos = sorted(set(e["architecture"]) - gt)

    L: list[str] = []
    L.append("# Actualización del análisis de Santillán y Abad (2025)")
    L.append("")
    L.append("Santillán, S. y Abad, C. L. (2025). *An Analysis of HPC and Edge "
             "Architectures in the Cloud*. IC2E 2025, pp. 259–266. "
             "DOI [10.1109/IC2E65552.2025.00043](https://doi.org/10.1109/IC2E65552.2025.00043). "
             "Paquete de reproducibilidad bajo licencia MIT.")
    L.append("")
    L.append(f"El paper analiza las **{nb} arquitecturas** de Cloudscape, que cubren "
             "videos de marzo 2019 a diciembre 2023. Nuestro pipeline extrajo "
             f"**{len(nuevos)} arquitecturas** que ese dataset no tiene. Este documento "
             f"reporta el análisis de los autores corrido sobre las **{ne}**.")
    L.append("")
    L.append("**Método.** Se ejecutó el notebook de los autores sin modificar su lógica. "
             "Las dos corridas usan el mismo código; lo único que cambia es el directorio "
             "de graphml que leen. Antes de actualizar nada se verificó que la corrida "
             "base reproduce el paper publicado: la Tabla I (280/101/11/4) y las medias de "
             "workflows de la Fig. 9 (4.0 / 3.3 / 4.5 / 3.1) salen exactas, y los archivos "
             "que el notebook regenera coinciden 396/396 con los que los autores "
             "publicaron.")
    L.append("")
    L.append("**Reproducir:**")
    L.append("")
    L.append("```bash")
    L.append("# entorno con versiones fijadas: ver scripts/santillan_abad/requirements.txt")
    L.append("python scripts/santillan_abad/build_extended_corpus.py")
    L.append("python scripts/santillan_abad/make_analysis_notebook.py")
    L.append("python scripts/santillan_abad/run_notebooks.py       # ejecuta las dos variantes")
    L.append("python scripts/santillan_abad/compare_update.py")
    L.append("```")
    L.append("")

    # ── composición del aporte ──
    anios = Counter()
    for v in nuevos:
        p = PROJECT / "data" / "raw" / f"{v}.info.json"
        if p.exists():
            anios[str(json.load(open(p)).get("upload_date", "????"))[:4]] += 1
    L.append("## Qué agregan las arquitecturas nuevas")
    L.append("")
    L.append("| Año | Arquitecturas nuevas |")
    L.append("| :--- | ---: |")
    for a, n in sorted(anios.items()):
        L.append(f"| {a} | {n} |")
    L.append(f"| **Total** | **{sum(anios.values())}** |")
    L.append("")
    L.append(f"Las **{anios.get('2024', 0)} de 2024** son el hueco que el dataset original "
             "no cubre. Las de 2020–2023 son videos que la curación manual de Cloudscape "
             "no incluyó.")
    L.append("")

    # ── RQ6 / Tabla I ──
    cb = b["tipo_arquitectura"].value_counts()
    ce = e["tipo_arquitectura"].value_counts()
    L.append("## Prevalencia por tipo (Tabla I y RQ6)")
    L.append("")
    L.append(f"| Grupo | {nb} arq. (publicado) | | {ne} arq. (actualizado) | | Δ puntos |")
    L.append("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for t in ORDEN:
        x, y = int(cb.get(t, 0)), int(ce.get(t, 0))
        d = 100 * y / ne - 100 * x / nb
        L.append(f"| {t} | {x} | {pct(x, nb)} | {y} | {pct(y, ne)} | {d:+.1f} |")
    L.append("")
    solo_nuevas = e[e["architecture"].isin(nuevos)]["tipo_arquitectura"].value_counts()
    L.append("Sólo entre las nuevas: " + " · ".join(
        f"**{t}** {int(solo_nuevas.get(t, 0))}" for t in ORDEN) + ".")
    L.append("")

    # ── evolución por año ──
    for f, titulo in (("evolucion_absoluta_por_anio.csv", "Conteo absoluto por año"),):
        xb, xe = pd.read_csv(BASE / f, index_col=0), pd.read_csv(EXT / f, index_col=0)
        anios_todos = sorted(set(xb.index.astype(str)) | set(xe.index.astype(str)))
        L.append(f"### {titulo}")
        L.append("")
        cols = [c for c in ORDEN if c in xe.columns]
        L.append("| Año | " + " | ".join(f"{c} base → ext" for c in cols) + " |")
        L.append("| :--- | " + " | ".join("---:" for _ in cols) + " |")
        for a in anios_todos:
            fila = []
            for c in cols:
                v1 = xb.loc[int(a), c] if int(a) in xb.index and c in xb.columns else 0
                v2 = xe.loc[int(a), c] if int(a) in xe.index and c in xe.columns else 0
                fila.append(f"{int(v1)} → {int(v2)}" if int(v1) != int(v2) else f"{int(v1)}")
            L.append(f"| {a} | " + " | ".join(fila) + " |")
        L.append("")
        L.append("2024 no existe en el análisis publicado. Es la fila que este trabajo agrega.")
        L.append("")

    # ── RQ1/RQ2 top servicios ──
    L.append("## Servicios más frecuentes (RQ1–RQ2)")
    L.append("")
    L.append("Cuenta en cuántas arquitecturas del grupo aparece cada servicio.")
    L.append("")
    for t in ORDEN:
        fb = Counter(s for l in b[b["tipo_arquitectura"] == t]["services"] for s in l)
        fe = Counter(s for l in e[e["tipo_arquitectura"] == t]["services"] for s in l)
        tb, te = int(cb.get(t, 0)), int(ce.get(t, 0))
        if not te:
            continue
        L.append(f"### {t} ({tb} → {te} arquitecturas)")
        L.append("")
        L.append("| # | Publicado | | Actualizado | | Movimiento |")
        L.append("| ---: | :--- | ---: | :--- | ---: | :--- |")
        rb = [s for s, _ in fb.most_common(10)]
        re_ = [s for s, _ in fe.most_common(10)]

        def rango(f: Counter, s: str) -> int:
            """Rango por conteo, no por posición en la lista.

            `most_common` desempata de forma arbitraria, así que comparar posiciones
            hace parecer que un servicio 'subió' cuando en realidad tiene el mismo
            conteo que el de al lado. Acá dos servicios empatados comparten rango.
            """
            return 1 + sum(1 for v in f.values() if v > f[s])

        for i in range(10):
            sb = rb[i] if i < len(rb) else "—"
            se = re_[i] if i < len(re_) else "—"
            vb = f"{fb[sb]} ({100*fb[sb]/tb:.0f} %)" if sb != "—" and tb else "—"
            ve = f"{fe[se]} ({100*fe[se]/te:.0f} %)" if se != "—" else "—"
            if se == "—":
                mov = ""
            elif fb.get(se, 0) == 0:
                mov = "**entra**"
            else:
                d = rango(fb, se) - rango(fe, se)
                mov = "=" if d == 0 else (f"sube {d}" if d > 0 else f"baja {-d}")
            L.append(f"| {i+1} | {sb} | {vb} | {se} | {ve} | {mov} |")
        salen = [s for s in rb if s not in re_]
        if salen:
            L.append("")
            L.append(f"Sale del top 10: {', '.join(salen)}.")
        L.append("")

    # ── servicios por arquitectura ──
    L.append("## Servicios por arquitectura (Fig. 5)")
    L.append("")
    L.append("| Grupo | media base | media ext | mediana base | mediana ext |")
    L.append("| :--- | ---: | ---: | ---: | ---: |")
    for t in ORDEN:
        sb = b[b["tipo_arquitectura"] == t]["services"].apply(len)
        se = e[e["tipo_arquitectura"] == t]["services"].apply(len)
        if not len(se):
            continue
        L.append(f"| {t} | {sb.mean():.2f} | {se.mean():.2f} | "
                 f"{sb.median():.1f} | {se.median():.1f} |")
    L.append("")

    # ── RQ3 y RQ4 ──
    for f, titulo, nota in (
        ("porcentaje_almacenamiento_por_tipo_arquitectura.csv", "Almacenamiento (RQ3)",
         "Porcentaje de arquitecturas del grupo que usan cada servicio de almacenamiento."),
        ("ml_por_tipo_arquitectura.csv", "Machine learning (RQ4)",
         "Arquitecturas con al menos un servicio de ML."),
    ):
        if not (BASE / f).exists() or not (EXT / f).exists():
            continue
        xb, xe = pd.read_csv(BASE / f, index_col=0), pd.read_csv(EXT / f, index_col=0)
        L.append(f"## {titulo}")
        L.append("")
        L.append(nota)
        L.append("")
        cols = [c for c in xe.columns if c in xb.columns]
        L.append("| | " + " | ".join(str(c) for c in cols) + " |")
        L.append("| :--- | " + " | ".join("---:" for _ in cols) + " |")
        for idx in xe.index:
            if idx not in xb.index:
                continue
            # el grupo "None" viaja como NaN en estos CSV; mostrarlo como 'nan' haría
            # pensar que es una fila rota
            etiq = "None" if str(idx).lower() in ("nan", "none") else str(idx)
            fila = []
            for c in cols:
                v1, v2 = xb.loc[idx, c], xe.loc[idx, c]
                try:
                    fila.append(f"{float(v1):.1f} → {float(v2):.1f}")
                except (TypeError, ValueError):
                    fila.append(f"{v1} → {v2}")
            L.append(f"| {etiq} | " + " | ".join(fila) + " |")
        L.append("")

    # ── limitaciones ──
    L.append("## Qué NO se actualizó, y por qué")
    L.append("")
    L.append("| Análisis | Estado | Razón |")
    L.append("| :--- | :--- | :--- |")
    L.append("| RQ5 — objetivos funcionales | **fuera** | Cloudscape usa un vocabulario "
             "controlado (`data_ingestion`, `interactive`, `control`, `compute_intensive`, "
             "`other`) y nuestro pipeline genera texto libre. Requiere etiquetar a mano las "
             f"{len(nuevos)} nuevas. |")
    L.append("| RQ7 — workflows | **fuera** | Depende de las aristas y de `flow_id`. "
             "Nuestro pipeline mide 59.7 % de F1 en aristas contra 86.8 % en servicios: "
             "publicar una distribución de workflows construida sobre eso sería publicar "
             "ruido. |")
    L.append("| Fig. 2 — industrias | **fuera** | El dato de industria no está en el "
             "paquete de reproducibilidad de los autores; lo hicieron a mano y no lo "
             "publicaron. La celda falla con su propio "
             "`assert len(df_meta) == 396`. |")
    L.append("| §III-G — clustering k-means | **fuera** | No es reproducible: da resultados "
             "distintos entre dos corridas consecutivas en la misma máquina, porque el "
             "orden de entrada no está fijado. |")
    L.append("")
    L.append("## Limitaciones de esta actualización")
    L.append("")
    aut = {"HPC": 8, "Edge": 100, "Edge+HPC": 1}
    L.append("1. **Las arquitecturas nuevas no recibieron curación manual.** Los autores "
             "clasifican por lista de servicios y después corrigen a mano: sobre las 396, "
             f"el clasificador automático da HPC {aut['HPC']}, Edge {aut['Edge']}, "
             f"Edge+HPC {aut['Edge+HPC']}, y la curación manual lo lleva a "
             f"{int(cb.get('HPC',0))} / {int(cb.get('Edge',0))} / "
             f"{int(cb.get('Edge+HPC',0))}. Las {len(nuevos)} nuevas sólo pasaron por el "
             "clasificador automático, así que es esperable que estén **sub-clasificadas** "
             "como HPC y Edge+HPC respecto de las originales.")
    L.append("2. **Las arquitecturas nuevas son extracción automática, no anotación "
             "humana.** Las 396 originales las anotó a mano un equipo de UW–Madison; las "
             f"{len(nuevos)} nuevas salen de nuestro pipeline, con F1 de servicios de "
             "86.8 % medido contra ese mismo ground truth. Todo número de este documento "
             f"mezcla {nb} filas curadas a mano con {len(nuevos)} filas extraídas "
             "automáticamente, y el error de extracción afecta a esas últimas.")
    L.append("3. **Ningún servicio de las nuevas cae fuera del catálogo de Cloudscape**, "
             "lo cual acota el punto anterior en la dimensión que más importa acá: no hay "
             "nombres inventados contaminando los conteos de frecuencia.")
    L.append("")

    SALIDA.write_text("\n".join(L), encoding="utf-8")
    print(f"✓ {SALIDA.relative_to(PROJECT)}  ({len(L)} líneas)")
    print(f"  base {nb} · extendido {ne} · nuevas {len(nuevos)}")


if __name__ == "__main__":
    main()
