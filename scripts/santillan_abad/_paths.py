#!/usr/bin/env python3
"""
_paths.py — Resolución de rutas para el análisis de Santillán y Abad.

Por qué existe
--------------
Los cuatro scripts de esta carpeta apuntaban al paquete de reproducibilidad de los
autores con una ruta absoluta del tipo `/home/<usuario>/Projects/...`. Eso rompía en
cualquier otra máquina y, además, filtra el nombre de usuario — un problema concreto para
la revisión doble ciego.

Acá se resuelve en un solo lugar, con este orden de precedencia:

  1. la variable de entorno `SANTILLAN_PKG`, si está definida;
  2. `data/external/hpc-and-edge-cloud-architectures/Workshop_paper` dentro del repo
     (donde lo deja `fetch_santillan_abad.sh`);
  3. un directorio hermano del repo, que es como estaba montado en la máquina original.

El paquete NO se redistribuye: es obra de terceros (MIT, DiSEL/ESPOL) y se baja con el
script de fetch, igual que Cloudscape. Ver `docs/actualizacion-santillan-abad.md`.
"""
from __future__ import annotations

import os
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent

_CANDIDATOS = [
    Path(os.environ["SANTILLAN_PKG"]) if os.environ.get("SANTILLAN_PKG") else None,
    PROJECT / "data" / "external" / "hpc-and-edge-cloud-architectures" / "Workshop_paper",
    PROJECT.parent / "hpc-and-edge-cloud-architectures" / "Workshop_paper",
]

_AYUDA = """
No se encontró el paquete de reproducibilidad de Santillán y Abad (2025).

Es obra de terceros y no se redistribuye con este repo. Para obtenerlo:

    bash data/fetch_santillan_abad.sh

o, si ya lo tenés en otro lado:

    export SANTILLAN_PKG=/ruta/a/hpc-and-edge-cloud-architectures/Workshop_paper

Buscado en:
"""


def find_pkg(requerido: bool = True) -> Path | None:
    """Devuelve el Workshop_paper del paquete de los autores, o falla con instrucciones."""
    for c in _CANDIDATOS:
        if c is not None and c.is_dir():
            return c
    if not requerido:
        return None
    listado = "\n".join(f"  - {c}" for c in _CANDIDATOS if c is not None)
    raise SystemExit(_AYUDA + listado)
