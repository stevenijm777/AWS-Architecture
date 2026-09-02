#!/usr/bin/env python3
"""
sync_notebooks_from_public.py — Trae los notebooks del repo publicable al de trabajo.

Dirección y por qué
-------------------
Este repo (`AWS-Architecture`) es el **entorno de pruebas**: acá se desarrollan y se
analizan los notebooks, con acceso a los datos crudos que el repo publicable no lleva
(frames, audio, lab_workspace). El repo publicable es el destino de publicación, y
`sync_to_public_repo.py` empuja hacia allá.

Los notebooks 04–10 se escribieron directamente contra el repo publicable, así que hay que
traerlos de vuelta una vez. A partir de ahí, el flujo normal es al revés:

    editar acá  →  sync_to_public_repo.py  →  repo publicable

Traducciones (inversas a las de sync_to_public_repo.py)
-------------------------------------------------------
    ../results/                     ->  ../reports/
    scripts.evaluation.graph_builder->  scripts.core.graph_builder
    scripts.evaluation.evaluate_graphs -> scripts.utils.evaluate_graphs
    ../data/videos.csv              ->  ../videos.csv          (acá vive en la raíz)
    ../data/example_frames/X.jpg    ->  ../data/good_whiteboard/X.jpg
    ../data/provenance/parsimonious_prompt_history.md
                                    ->  ../whiteboard_selection_lab/...

Es idempotente y no borra nada. Uso:

    .venv/bin/python scripts/utils/sync_notebooks_from_public.py --dry-run
    .venv/bin/python scripts/utils/sync_notebooks_from_public.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

DST = Path(__file__).resolve().parent.parent.parent          # AWS-Architecture
SRC = DST.parent / "aws-architecture-extraction"             # repo publicable

console = Console()

REWRITES = [
    (r"scripts\.evaluation\.graph_builder", "scripts.core.graph_builder"),
    (r"scripts\.evaluation\.evaluate_graphs", "scripts.utils.evaluate_graphs"),
    (r"scripts/evaluation/graph_builder", "scripts/core/graph_builder"),
    (r"scripts/evaluation/evaluate_graphs", "scripts/utils/evaluate_graphs"),
    # Rutas de datos que difieren entre los dos repos.
    (r"\.\./data/videos\.csv", "../videos.csv"),
    (r"\.\./data/example_frames/", "../data/good_whiteboard/"),
    (r"\.\./data/provenance/parsimonious_prompt_history\.md",
     "../whiteboard_selection_lab/parsimonious_prompt_history.md"),
    # results/ -> reports/  (va al final: es la regla más general)
    (r"\.\./results/", "../reports/"),
    (r'PROJECT_ROOT / "results"', 'PROJECT_ROOT / "reports"'),
]


def rewrite(text: str) -> str:
    for pat, rep in REWRITES:
        text = re.sub(pat, rep, text)
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not SRC.exists():
        console.print(f"[bold red]✗ No existe el repo publicable: {SRC}[/]")
        raise SystemExit(1)

    (DST / "notebooks").mkdir(exist_ok=True)
    t = Table(title="Notebooks ← repo publicable" + (" [DRY-RUN]" if args.dry_run else ""),
              border_style="cyan")
    t.add_column("notebook", style="bold"); t.add_column("estado", justify="right")

    for nb in sorted((SRC / "notebooks").glob("*.ipynb")):
        dst = DST / "notebooks" / nb.name
        nuevo = rewrite(nb.read_text(encoding="utf-8"))
        if dst.exists() and dst.read_text(encoding="utf-8") == nuevo:
            t.add_row(nb.name, "ya igual")
            continue
        if not args.dry_run:
            dst.write_text(nuevo, encoding="utf-8")
        t.add_row(nb.name, "[green]escrito[/]")

    console.print(t)
    if args.dry_run:
        console.print("[dim]— dry-run: no se escribió nada —[/]")


if __name__ == "__main__":
    main()
