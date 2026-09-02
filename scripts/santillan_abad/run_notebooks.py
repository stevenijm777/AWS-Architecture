#!/usr/bin/env python3
"""
run_notebooks.py — Ejecuta las dos variantes del notebook de Santillán y Abad.

`local` corre sobre las 396 arquitecturas de Cloudscape y debe reproducir el paper
publicado; es el control. `extended` corre sobre las 457 e incluye las que extrajo
nuestro pipeline; es la actualización.

Se ejecutan con `allow_errors=True` a propósito: interesa ver todas las celdas que
fallan en una sola pasada, y en la variante extendida hay un fallo esperado —la celda
de industrias tiene un `assert len(df_meta) == 396` de los propios autores, que salta
justamente porque el corpus creció. Ese fallo es correcto y no debe silenciarse.

Uso
---
    python scripts/santillan_abad/run_notebooks.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

from _paths import find_pkg  # noqa: E402

import nbformat
from nbclient import NotebookClient

PKG = find_pkg()
VARIANTES = ("local", "extended", "gt385", "extracted385")

# Fallos conocidos y aceptados: (variante, subcadena del mensaje) -> por qué
ESPERADOS = {
    ("gt385", "Row count changed"): "misma celda de industrias, corpus de 385.",
    ("gt385", "metadata_actualizada_con_industrias_seguro.csv"): "cascada.",
    ("extracted385", "Row count changed"): "misma celda de industrias, corpus de 385.",
    ("extracted385", "metadata_actualizada_con_industrias_seguro.csv"): "cascada.",
    ("extended", "Row count changed"):
        "assert len(df_meta) == 396 de los autores: la celda de industrias no admite "
        "un corpus mayor. Fuera de alcance (el dato de industria no está en su paquete).",
    ("extended", "metadata_actualizada_con_industrias_seguro.csv"):
        "cae en cascada de la celda anterior.",
}


def main() -> None:
    problemas = 0
    for v in VARIANTES:
        f = PKG / f"hpc_n_edge_clouds_archs_{v}.ipynb"
        if not f.exists():
            raise SystemExit(f"falta {f.name} — corré primero make_analysis_notebook.py")
        nb = nbformat.read(f, as_version=4)
        t0 = time.time()
        NotebookClient(nb, timeout=900, kernel_name="python3", allow_errors=True,
                       resources={"metadata": {"path": str(PKG)}}).execute()
        nbformat.write(nb, f)

        errores = [(i, o["ename"], o["evalue"])
                   for i, c in enumerate(nb.cells) if c.cell_type == "code"
                   for o in c.get("outputs", []) if o.get("output_type") == "error"]
        print(f"\n{v}: {time.time() - t0:.0f}s · celdas con error {len(errores)}")
        for i, ename, evalue in errores:
            motivo = next((m for (var, clave), m in ESPERADOS.items()
                           if var == v and clave in evalue), None)
            if motivo:
                print(f"  · celda {i} {ename}: esperado — {motivo}")
            else:
                print(f"  ✗ celda {i} {ename}: {evalue[:120]}")
                problemas += 1

    if problemas:
        print(f"\n✗ {problemas} fallo(s) NO esperado(s)")
        sys.exit(1)
    print("\n✓ las dos variantes corrieron; sólo fallos esperados")


if __name__ == "__main__":
    main()
