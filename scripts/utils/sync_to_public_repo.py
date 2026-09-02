#!/usr/bin/env python3
"""
sync_to_public_repo.py — Migra artefactos citables al repositorio publicable.

El repo de trabajo (`AWS-Architecture`) es la bitácora: tiene credenciales, audio,
frames, PDFs con copyright y ramas muertas. El repo publicable
(`aws-architecture-extraction`) contiene solo lo que hace falta para regenerar cada
cifra del paper.

Este script hace la copia **con las traducciones de ruta e import que el repo
publicable ya estableció**, en vez de a mano:

    reports/                    ->  results/
    scripts.core.graph_builder  ->  scripts.evaluation.graph_builder
    scripts.utils.evaluate_graphs -> scripts.evaluation.evaluate_graphs
    .venv/bin/python            ->  python
    lab_workspace/<vid>/world_model_vision.json -> data/manual_world_models/<vid>.json

Es idempotente: correrlo dos veces no duplica nada. No borra nada del destino.

Uso
---
    .venv/bin/python scripts/utils/sync_to_public_repo.py --dry-run
    .venv/bin/python scripts/utils/sync_to_public_repo.py
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

from rich.console import Console
from rich.table import Table

SRC = Path(__file__).resolve().parent.parent.parent
DST = SRC.parent / "aws-architecture-extraction"

console = Console()

# Traducciones aplicadas a todo archivo de texto que se migra (.py y .ipynb).
REWRITES = [
    (r"scripts\.core\.graph_builder", "scripts.evaluation.graph_builder"),
    (r"scripts\.utils\.evaluate_graphs", "scripts.evaluation.evaluate_graphs"),
    (r"scripts/core/graph_builder", "scripts/evaluation/graph_builder"),
    (r"scripts/utils/evaluate_graphs", "scripts/evaluation/evaluate_graphs"),
    (r"\.\./reports/", "../results/"),
    # En el repo de trabajo services.csv está suelto en data/; en el publicable llega
    # dentro del clon de Cloudscape. Verificado byte-idéntico antes de traducir.
    (r"\.\./data/services\.csv", "../data/cloudscape_gt/services.csv"),
    # Los prompts materializados: en el repo de trabajo cuelgan de src/configs/,
    # en el publicable estan en la raiz como prompts/.
    (r"\.\./src/configs/prompts", "../prompts"),
    # Rutas que difieren entre los dos repos. Son la inversa exacta de las de
    # sync_notebooks_from_public.py; si se toca una, hay que tocar la otra.
    (r"\.\./videos\.csv", "../data/videos.csv"),
    (r"\.\./data/good_whiteboard/", "../data/example_frames/"),
    (r"\.\./whiteboard_selection_lab/parsimonious_prompt_history\.md",
     "../data/provenance/parsimonious_prompt_history.md"),
    (r'PROJECT_ROOT / "reports"', 'PROJECT_ROOT / "results"'),
    (r"reports/ablation", "results/ablation"),
    (r"reports/piso_ruido_panel30", "results/piso_ruido_panel30"),
    (r"reports/evaluacion_metricas_panel30", "results/evaluacion_metricas_panel30"),
    (r"reports/permissive_panel", "results/permissive_panel"),
    # `config.settings` carga el .env con las claves de la API y no viaja al repo
    # publicable. De ahi solo se usan dos constantes; se definen en su lugar. Mismo
    # tratamiento que ya se le habia dado a graph_builder.py.
    (r"from config\.settings import DATA_DIR, GEMINI_MODEL",
     'DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"\n'
     'GEMINI_MODEL = "gemini-3.6-flash"  # modelo con el que se produjeron las corridas'),
    (r"\.venv/bin/python", "python"),
]

# Corridas del panel de 30 que el repo publicable todavía no tiene.
RUN_DIRS = [
    "2026-08-28_2211_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt_rep2",
    "2026-08-29_0442_STAGE2_V6_CORRECTED_cell9_p30_rep3",
    "2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4",
    "2026-08-29_0725_STAGE2_V6_CORRECTED_cell9_p30_oracle-vision",
    "2026-08-29_0910_RETURN_EDGE_AUDIT_base-2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4",
    "2026-08-30_0203_STAGE2_V6_CORRECTED_cell9_p30_notranscript",
    "2026-08-30_0224_STAGE2_V6_CORRECTED_cell9_p30_oracle-vision_notranscript",
    "2026-08-30_1733_STAGE2_V4_DYNAMIC_FEW_SHOT_cellNone_p30",
]

SCRIPTS = [
    ("scripts/ablation/return_edge_audit.py", "scripts/ablation/return_edge_audit.py"),
    ("scripts/ablation/connection_evidence.py", "scripts/ablation/connection_evidence.py"),
    ("scripts/ablation/build_oracle_world_models.py", "scripts/ablation/build_oracle_world_models.py"),
    ("scripts/ablation/evaluate_permissive_panel.py", "scripts/ablation/evaluate_permissive_panel.py"),
    ("scripts/ablation/measure_frame_selector.py", "scripts/ablation/measure_frame_selector.py"),
    ("scripts/utils/build_whiteboard_manifest.py", "scripts/build_whiteboard_manifest.py"),
    ("scripts/utils/build_frame_selector_review.py", "scripts/build_frame_selector_review.py"),
    ("scripts/utils/merge_frame_selector_votes.py", "scripts/merge_frame_selector_votes.py"),
    # Evaluador principal: se le agregaron las columnas ms_* (multiconjunto) al CSV.
    ("scripts/utils/evaluate_standard.py", "scripts/evaluation/evaluate_standard.py"),
    # Analisis de tarea downstream: replicacion de Santillan y Abad (IC2E 2025).
    # El paquete de los autores NO viaja: se baja con data/fetch_santillan_abad.sh.
    ("scripts/santillan_abad/_paths.py", "scripts/santillan_abad/_paths.py"),
    ("scripts/santillan_abad/build_extended_corpus.py", "scripts/santillan_abad/build_extended_corpus.py"),
    ("scripts/santillan_abad/make_analysis_notebook.py", "scripts/santillan_abad/make_analysis_notebook.py"),
    ("scripts/santillan_abad/run_notebooks.py", "scripts/santillan_abad/run_notebooks.py"),
    ("scripts/santillan_abad/compare_update.py", "scripts/santillan_abad/compare_update.py"),
    ("scripts/santillan_abad/error_propagation.py", "scripts/santillan_abad/error_propagation.py"),
    ("scripts/santillan_abad/requirements.txt", "scripts/santillan_abad/requirements.txt"),
]

DOCS = [
    ("docs/actualizacion-santillan-abad.md", "docs/actualizacion-santillan-abad.md"),
    ("docs/propagacion-error-santillan-abad.md", "docs/propagacion-error-santillan-abad.md"),
]

JSON_ARTIFACTS = [
    ("reports/piso_ruido_panel30.json", "results/piso_ruido_panel30.json"),
    ("reports/evaluacion_metricas_panel30.json", "results/evaluacion_metricas_panel30.json"),
]

LAB = SRC / "whiteboard_selection_lab" / "lab_workspace"


def rewrite(text: str) -> str:
    for pat, rep in REWRITES:
        text = re.sub(pat, rep, text)
    return text


def copy_text(src: Path, dst: Path, dry: bool) -> str:
    if not src.exists():
        return "FALTA EN ORIGEN"
    new = rewrite(src.read_text(encoding="utf-8"))
    if dst.exists() and dst.read_text(encoding="utf-8") == new:
        return "ya igual"
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(new, encoding="utf-8")
    return "escrito"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    dry = args.dry_run

    if not DST.exists():
        console.print(f"[bold red]✗ No existe el repo destino: {DST}[/]")
        raise SystemExit(1)

    t = Table(title=f"Migración → {DST.name}" + (" [DRY-RUN]" if dry else ""),
              border_style="cyan")
    t.add_column("qué", style="bold"); t.add_column("destino"); t.add_column("estado", justify="right")

    # 1 · corridas
    for d in RUN_DIRS:
        s, dd = SRC / "reports/ablation" / d, DST / "results/ablation" / d
        if not s.exists():
            t.add_row("corrida", d[:52], "[red]FALTA EN ORIGEN[/]"); continue
        if dd.exists():
            t.add_row("corrida", d[:52], "ya estaba")
        else:
            if not dry:
                shutil.copytree(s, dd)
            t.add_row("corrida", d[:52], "[green]copiada[/]")

    # 2 · world models manuales (brazo A): 30 archivos, renombrados
    n_new = n_same = 0
    for wm in sorted(LAB.glob("*/world_model_vision.json")):
        dd = DST / "data/manual_world_models" / f"{wm.parent.name}.json"
        txt = wm.read_text(encoding="utf-8")
        if dd.exists() and dd.read_text(encoding="utf-8") == txt:
            n_same += 1
        else:
            if not dry:
                dd.parent.mkdir(parents=True, exist_ok=True)
                dd.write_text(txt, encoding="utf-8")
            n_new += 1
    t.add_row("world models manuales", "data/manual_world_models/*.json",
              f"[green]{n_new} nuevos/actualizados[/], {n_same} iguales")

    # 3 · notebooks, con rutas e imports traducidos
    for nb in sorted((SRC / "notebooks").glob("*.ipynb")):
        estado = copy_text(nb, DST / "notebooks" / nb.name, dry)
        t.add_row("notebook", f"notebooks/{nb.name}", estado)

    # 4 · scripts
    for rel_s, rel_d in SCRIPTS:
        t.add_row("script", rel_d, copy_text(SRC / rel_s, DST / rel_d, dry))

    # 5 · artefactos json
    for rel_s, rel_d in JSON_ARTIFACTS:
        t.add_row("artefacto", rel_d, copy_text(SRC / rel_s, DST / rel_d, dry))

    # 5b · documentos de la tarea downstream
    for rel_s, rel_d in DOCS:
        t.add_row("doc", rel_d, copy_text(SRC / rel_s, DST / rel_d, dry))

    # 6 · paquetes importables (los notebooks hacen `from scripts...`)
    for pkg in ("scripts", "scripts/evaluation", "scripts/ablation"):
        p = DST / pkg / "__init__.py"
        if p.exists():
            t.add_row("__init__.py", f"{pkg}/__init__.py", "ya estaba")
        else:
            if not dry:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("", encoding="utf-8")
            t.add_row("__init__.py", f"{pkg}/__init__.py", "[green]creado[/]")

    console.print(t)

    # 7 · aviso sobre el piso de ruido deprecado
    old = DST / "results/noise_floor.json"
    if old.exists():
        console.print("\n[yellow]⚠ results/noise_floor.json sigue presente.[/] "
                      "Está calculado sobre pares del panel de 14 (σ=8.76, MDE=4.48) y lo "
                      "reemplaza results/piso_ruido_panel30.json (σ=6.43, MDE=3.29).\n"
                      "  El README del repo publicable todavía cita las cifras viejas.")

    if dry:
        console.print("\n[dim]— dry-run: no se escribió nada —[/]")


if __name__ == "__main__":
    main()
