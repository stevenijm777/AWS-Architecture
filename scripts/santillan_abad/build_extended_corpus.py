#!/usr/bin/env python3
"""
build_extended_corpus.py — Arma el corpus extendido y le corre las compuertas de control.

Santillán y Abad analizaron las 396 arquitecturas de Cloudscape, que cubren videos de
marzo 2019 a diciembre 2023. Nuestro pipeline extrajo 61 arquitecturas que no están en
ese dataset, 33 de ellas de 2024 — el hueco que el enunciado del proyecto nombra.

Este script construye `data/cloudscape_extended/`, un directorio con enlaces simbólicos
a los 457 graphml (396 del ground truth + 61 nuestros). Se usan enlaces y no copias por
dos razones: no duplica datos, y deja visible de dónde viene cada archivo.

El notebook de los autores lee un directorio de graphml y arma todo desde ahí, así que
apuntarlo a este directorio actualiza el análisis completo sin tocarles una línea.

Compuertas
----------
Ninguna de estas es opcional. Si una falla, el corpus no se arma.

  1. Los 61 no pisan ningún ID de las 396.
  2. Los 457 archivos quedan enlazados y se leen.
  3. Todo servicio de los 61 está en el catálogo de Cloudscape. Un nombre fuera del
     catálogo es un error de extracción o un servicio nuevo de 2024, y en cualquiera
     de los dos casos lo decide una persona, no este script.
  4. Los 61 declaran `graph_usable`.
  5. Los 61 tienen `info.json`, que es de donde sale el año.

Uso
---
    .venv/bin/python scripts/santillan_abad/build_extended_corpus.py
"""
from __future__ import annotations

import csv
import glob
import json
import os
import sys
from collections import Counter
from pathlib import Path

import networkx as nx

PROJECT = Path(__file__).resolve().parent.parent.parent
GT_DIR = PROJECT / "data" / "cloudscape_gt"
GEN_DIR = PROJECT / "data" / "graphs"          # brazo Standard
RAW_DIR = PROJECT / "data" / "raw"
EXT_DIR = PROJECT / "data" / "cloudscape_extended"

# Corpus pareados para medir propagación de error. Son las MISMAS arquitecturas en
# los dos, una vez con la anotación humana y otra con nuestra extracción, así que la
# diferencia entre correr el análisis sobre uno y sobre el otro no puede venir del
# corpus: viene enteramente del error del pipeline.
#
# Hace falta porque el corpus extendido usa el ground truth para las 396 y sólo aporta
# extracción propia en las 61 nuevas. Eso responde "¿cambian las conclusiones al sumar
# 2024?" pero no responde "¿cuánto las distorsiona nuestro error de extracción?".
GT385_DIR = PROJECT / "data" / "cloudscape_gt385"
EXTRACTED385_DIR = PROJECT / "data" / "cloudscape_extracted385"


def ids(d: Path) -> set[str]:
    return {os.path.basename(p)[:-8] for p in glob.glob(str(d / "*.graphml"))}


def catalogo() -> set[str]:
    with open(GT_DIR / "services.csv", encoding="utf-8") as f:
        return {next(iter(r.values())) for r in csv.DictReader(f)}


def main() -> None:
    gt, gen = ids(GT_DIR), ids(GEN_DIR)
    nuevos = sorted(gen - gt)
    fallos: list[str] = []

    print(f"Cloudscape (ground truth) : {len(gt)}")
    print(f"nuestro pipeline          : {len(gen)}")
    print(f"arquitecturas nuevas      : {len(nuevos)}")

    # Gate 1 — sin colisión de IDs
    if gt & set(nuevos):
        fallos.append(f"GATE 1 colisión de IDs: {sorted(gt & set(nuevos))[:5]}")

    # Gate 3/4/5 — vocabulario, usabilidad, metadato de año
    cat = catalogo()
    fuera: Counter[str] = Counter()
    no_usable, sin_info = [], []
    anios: Counter[str] = Counter()
    for v in nuevos:
        G = nx.read_graphml(str(GEN_DIR / f"{v}.graphml"))
        if str(G.graph.get("graph_usable")).lower() != "true":
            no_usable.append(v)
        for s in {d.get("service", "") for _, d in G.nodes(data=True)} - cat:
            fuera[s] += 1
        p = RAW_DIR / f"{v}.info.json"
        if not p.exists():
            sin_info.append(v)
        else:
            anios[str(json.load(open(p)).get("upload_date", "????"))[:4]] += 1

    if fuera:
        fallos.append(f"GATE 3 servicios fuera del catálogo: {dict(fuera)}")
    if no_usable:
        fallos.append(f"GATE 4 grafos no usables: {no_usable}")
    if sin_info:
        fallos.append(f"GATE 5 sin info.json: {sin_info}")

    print(f"por año                   : {dict(sorted(anios.items()))}")

    if fallos:
        print("\n".join("✗ " + f for f in fallos))
        sys.exit(1)

    # Armado del directorio
    if EXT_DIR.exists():
        for p in EXT_DIR.glob("*.graphml"):
            p.unlink()
    EXT_DIR.mkdir(exist_ok=True)
    for v in sorted(gt):
        (EXT_DIR / f"{v}.graphml").symlink_to(GT_DIR / f"{v}.graphml")
    for v in nuevos:
        (EXT_DIR / f"{v}.graphml").symlink_to(GEN_DIR / f"{v}.graphml")
    # el notebook lee services.csv desde el mismo directorio
    dst = EXT_DIR / "services.csv"
    if not dst.exists():
        dst.symlink_to(GT_DIR / "services.csv")

    # Gate 2 — los 457 se leen de verdad
    enlazados = ids(EXT_DIR)
    ilegibles = []
    for v in sorted(enlazados):
        try:
            nx.read_graphml(str(EXT_DIR / f"{v}.graphml"))
        except Exception as e:  # noqa: BLE001
            ilegibles.append((v, str(e)[:60]))
    if len(enlazados) != len(gt) + len(nuevos) or ilegibles:
        print(f"✗ GATE 2 enlazados {len(enlazados)}, esperados {len(gt) + len(nuevos)}; "
              f"ilegibles {ilegibles[:3]}")
        sys.exit(1)

    # ── Corpus pareados para propagación de error ─────────────────
    solapan = sorted(gt & gen)
    for destino, origen, etiqueta in ((GT385_DIR, GT_DIR, "ground truth"),
                                      (EXTRACTED385_DIR, GEN_DIR, "extracción propia")):
        if destino.exists():
            for p in destino.glob("*.graphml"):
                p.unlink()
        destino.mkdir(exist_ok=True)
        for v in solapan:
            (destino / f"{v}.graphml").symlink_to(origen / f"{v}.graphml")
        dst = destino / "services.csv"
        if not dst.exists():
            dst.symlink_to(GT_DIR / "services.csv")
        n = len(list(destino.glob("*.graphml")))
        if n != len(solapan):
            print(f"✗ {destino.name}: {n} enlazados, esperados {len(solapan)}")
            sys.exit(1)
        print(f"✓ {destino.relative_to(PROJECT)} — {n} arquitecturas ({etiqueta})")

    print(f"\n✓ todas las compuertas pasaron")
    print(f"✓ {EXT_DIR.relative_to(PROJECT)} con {len(enlazados)} arquitecturas "
          f"({len(gt)} del GT + {len(nuevos)} nuestras)")
    print(f"  las dos carpetas de {len(solapan)} son el mismo conjunto de videos con "
          f"anotación humana vs extracción automática")


if __name__ == "__main__":
    main()
