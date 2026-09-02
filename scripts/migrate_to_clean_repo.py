#!/usr/bin/env python3
"""
migrate_to_clean_repo.py — Copia al repositorio publicable sólo lo que sostiene el paper.

Este repositorio de trabajo tiene 36 GB de video, PDFs con copyright, claves de API y
artefactos de exploraciones que otra corrida reemplazó. El repositorio publicable lleva
otra cosa: el conjunto mínimo con el que un tercero puede regenerar cada número del
paper y comprobarlo.

El manifiesto de abajo es *datos*, no comandos. Se puede leer y discutir sin ejecutar
nada, y `--dry-run` (el modo por defecto) imprime exactamente qué se copiaría.

Qué NO viaja, y por qué
-----------------------
- `referencias/`      tres PDFs con copyright. El remoto es público.
- `data/raw/`         36 GB de video y transcripciones de AWS.
- `data/cloudscape_gt/` el dataset de UW–Madison **no declara licencia**, así que sin
                      permiso explícito no se redistribuye. En su lugar va un script
                      que lo baja del repositorio original.
- los notebooks derivados del paquete de Santillán y Abad: contienen una clave de API
                      que los autores dejaron en su repositorio público. Viaja el
                      script que los reconstruye, no el notebook.
- las tablas viejas de evidencia, `reporte_comparacion_detallada.md` y los claims que
                      contradicen la implementación: superados o incorrectos. Se
                      publica la versión corregida, no la equivocada.

Uso
---
    python scripts/migrate_to_clean_repo.py            # simula, no toca nada
    python scripts/migrate_to_clean_repo.py --apply    # copia
"""
from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from pathlib import Path

ORIGEN = Path("/home/stemjara/Projects/AWS-Architecture")
DESTINO = Path("/home/stemjara/Projects/aws-architecture-extraction")
LAB = ORIGEN / "whiteboard_selection_lab" / "lab_workspace"

# (origen, destino, patrón, descripción). El patrón None significa "un archivo".
MANIFIESTO: list[tuple[str, str, str | None, str]] = [
    # ── Datos: los grafos que produjimos ──────────────────────────
    ("data/graphs", "data/graphs", "*.graphml",
     "Grafos del pipeline Standard"),
    ("data/graphs_parsimonious", "data/graphs_parsimonious", "*.graphml",
     "Grafos del pipeline Parsimonious (autoría de Melissa)"),
    ("data/graphs_parsimonious", "data/graphs_parsimonious", "PROVENANCE.md",
     "Procedencia del corpus Parsimonious"),

    # ── Prompts, con sus hashes ───────────────────────────────────
    ("src/configs/prompts", "prompts", "*.txt",
     "Prompts de Stage 1 y Stage 2"),
    ("src/configs/prompts", "prompts", "MANIFEST.json",
     "SHA-256 de cada prompt — es lo que hace verificable la ablación"),

    # ── Resultados ────────────────────────────────────────────────
    ("reports/runs", "results/runs", "*/results.csv",
     "Evaluación sobre el corpus completo (la comparación pareada n=321)"),
    # TODAS las corridas, no sólo las del panel de 30. El piso de ruido se deriva de
    # los pares panel-14 ↔ panel-30: el panel chico es un subconjunto exacto del
    # grande, así que un prompt corrido en los dos da una réplica nula sin pagar
    # llamadas. Migrar sólo los p30 deja al script sin la mayoría de sus réplicas y
    # cambia sigma_d — lo detectó la prueba de aceptación.
    ("reports/ablation", "results/ablation", "*/run.json",
     "Corridas de ablación: 11 variantes, réplicas, oráculo, y los paneles de 14"),
    ("reports/ablation", "results/ablation", "*/results.csv",
     "Métricas por video de cada corrida de ablación"),
    ("reports", "results", "noise_floor.json",
     "El piso de ruido medido (sigma_d, MDE)"),
    ("reports", "results", "permissive_panel.json",
     "Evaluación permisiva vs estricta sobre el panel de 30"),

    # ── El experimento del oráculo ────────────────────────────────
    (str(LAB.relative_to(ORIGEN)), "data/manual_world_models",
     "*/world_model_vision.json",
     "Lecturas de la pizarra transcritas a mano (entrada del oráculo)"),

    # ── Código ────────────────────────────────────────────────────
    ("scripts/utils", "scripts/evaluation", "evaluate_graphs.py",
     "El evaluador estricto — sin esto ninguna cifra es verificable"),
    ("scripts/core", "scripts/evaluation", "graph_builder.py",
     "Construcción del grafo desde el JSON del modelo"),
    ("scripts/ablation", "scripts/ablation", "measure_noise_floor.py",
     "Mide el piso de ruido test-retest (cero API)"),
    ("scripts/ablation", "scripts/ablation", "build_evidence_tables.py",
     "Regenera las dos tablas de evidencia"),
    ("scripts/ablation", "scripts/ablation", "evaluate_permissive_panel.py",
     "Re-puntúa la ablación con el protocolo permisivo"),
    ("scripts/ablation", "scripts/ablation", "rerun_panel.py",
     "El runner del panel (rotación de llaves, checkpoints, réplicas)"),
    ("scripts/santillan_abad", "scripts/santillan_abad", "*.py",
     "Actualización del análisis de Santillán y Abad"),
    ("scripts/santillan_abad", "scripts/santillan_abad", "requirements.txt",
     "Versiones fijadas del entorno de ese análisis"),

    # ── Documentos ────────────────────────────────────────────────
    ("ara/evidence/tables", "evidence", "*.md",
     "Tablas de evidencia (versión corregida)"),
    ("docs", "docs", "actualizacion-santillan-abad.md",
     "El antes/después de la actualización"),
]

# El repositorio publicable reorganiza las carpetas (`reports/` pasa a `results/`,
# `ara/evidence/tables/` a `evidence/`, `scripts/utils` y `scripts/core` se unen en
# `scripts/evaluation`). Los scripts traen esas rutas escritas, así que se reescriben
# al copiarlos: si no, quedan apuntando a un layout que allá no existe y la prueba de
# aceptación —correr los scripts dentro del repositorio limpio— falla.
#
# Se hace acá y no a mano para que el mapeo viva en un solo lugar, junto al manifiesto
# que lo define.
REESCRITURAS: list[tuple[str, str]] = [
    ('from scripts.core.graph_builder', 'from scripts.evaluation.graph_builder'),
    ('from scripts.utils.evaluate_graphs', 'from scripts.evaluation.evaluate_graphs'),
    # Los notebooks referencian el árbol desde `notebooks/`, con `../`. Sin estas dos
    # reglas quedan apuntando a una carpeta que en el repositorio publicable no existe,
    # y el notebook falla recién al ejecutarse. Pasó de verdad: copiar un notebook a
    # mano, sin reescribir, dejó `Path("../reports/ablation")` en un árbol donde esa
    # carpeta se llama `results/`.
    ('Path("../reports/', 'Path("../results/'),
    ('`reports/ablation/', '`results/ablation/'),
    ('PROJECT_ROOT / "reports"', 'PROJECT_ROOT / "results"'),
    ('PROJECT_ROOT / "reports/', 'PROJECT_ROOT / "results/'),
    ('"reports/runs/', '"results/runs/'),
    ('"reports/ablation/', '"results/ablation/'),
    ('PROJECT_ROOT / "ara" / "evidence" / "tables"', 'PROJECT_ROOT / "evidence"'),
    ('ara/evidence/tables/', 'evidence/'),
    ('`reports/noise_floor.json`', '`results/noise_floor.json`'),
    ('.venv/bin/python scripts/', 'python scripts/'),
    # `config/settings.py` carga el .env y expone las claves de la API, así que no
    # viaja. graph_builder lo usa sólo para GRAPHS_DIR, un directorio de salida por
    # defecto que la ruta de evaluación nunca escribe, así que se define en el lugar.
    ('from config.settings import GRAPHS_DIR',
     '# `config.settings` no viaja al repositorio publicable: carga el .env y las\n'
     '# claves de la API. De ahí sólo se usaba GRAPHS_DIR, como directorio de salida\n'
     '# por defecto, y la ruta de evaluación nunca escribe. Se define acá.\n'
     'GRAPHS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "graphs"'),
]

# Nada que se copie puede contener algo que se parezca a una credencial.
SECRETOS = [
    (re.compile(rb"AIza[A-Za-z0-9_\-]{35}"), "clave de Google/Gemini"),
    (re.compile(rb"sk-[A-Za-z0-9]{32,}"), "clave estilo OpenAI"),
    (re.compile(rb"AKIA[0-9A-Z]{16}"), "clave de acceso de AWS"),
    (re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "clave privada"),
]
BINARIOS = {".graphml", ".json", ".csv", ".txt", ".py", ".md"}


def escanear(p: Path) -> list[str]:
    if p.suffix not in BINARIOS:
        return []
    try:
        datos = p.read_bytes()
    except OSError:
        return []
    return [q for rx, q in SECRETOS if rx.search(datos)]


def resolver() -> list[tuple[Path, Path, str]]:
    """Expande el manifiesto a una lista concreta de (origen, destino, descripción)."""
    plan: list[tuple[Path, Path, str]] = []
    for src_dir, dst_dir, patron, desc in MANIFIESTO:
        base = ORIGEN / src_dir
        if not base.exists():
            print(f"  ! no existe {src_dir} — se saltea")
            continue
        for p in sorted(base.glob(patron)):
            if not p.is_file():
                continue
            rel = p.relative_to(base)
            # los world models viven en <video_id>/world_model_vision.json;
            # se aplanan a <video_id>.json, que es más útil aguas abajo
            if p.name == "world_model_vision.json":
                destino = DESTINO / dst_dir / f"{p.parent.name}.json"
            else:
                destino = DESTINO / dst_dir / rel
            plan.append((p, destino, desc))
    return plan


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="copia de verdad; sin esto sólo simula")
    args = ap.parse_args()

    if not DESTINO.exists():
        raise SystemExit(f"no existe el repositorio destino: {DESTINO}")

    plan = resolver()

    # agrupado por descripción, para que la lista se lea
    print(f"{'SIMULACIÓN — no se copia nada' if not args.apply else 'COPIANDO'}\n")
    por_desc: dict[str, list[tuple[Path, Path]]] = {}
    for src, dst, desc in plan:
        por_desc.setdefault(desc, []).append((src, dst))

    total_bytes = 0
    for desc, items in por_desc.items():
        n = len(items)
        b = sum(s.stat().st_size for s, _ in items)
        total_bytes += b
        destino_rel = items[0][1].parent.relative_to(DESTINO)
        print(f"  {n:>4} archivo(s)  {b/1e6:>6.2f} MB  →  {destino_rel}/")
        print(f"       {desc}")

    print(f"\n  TOTAL: {len(plan)} archivos, {total_bytes/1e6:.1f} MB")

    # compuerta de secretos, antes de copiar nada
    print("\nEscaneo de credenciales…")
    hallazgos = [(s, q) for s, _, _ in plan for q in escanear(s)]
    if hallazgos:
        print(f"  ✗ {len(hallazgos)} archivo(s) con algo que parece una credencial:")
        for s, q in hallazgos[:10]:
            print(f"      {q}: {s.relative_to(ORIGEN)}")
        print("\n  MIGRACIÓN ABORTADA. El repositorio destino es público.")
        sys.exit(1)
    print(f"  ✓ {len(plan)} archivos limpios")

    if not args.apply:
        print("\nCorré con --apply para copiar.")
        return

    copiados = reescritos = 0
    for src, dst, _ in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in (".py", ".md"):
            texto = src.read_text(encoding="utf-8")
            nuevo = texto
            for viejo, actual in REESCRITURAS:
                nuevo = nuevo.replace(viejo, actual)
            dst.write_text(nuevo, encoding="utf-8")
            if nuevo != texto:
                reescritos += 1
        else:
            shutil.copy2(src, dst)
            if hashlib.sha256(src.read_bytes()).digest() != \
                    hashlib.sha256(dst.read_bytes()).digest():
                raise SystemExit(f"✗ copia corrupta: {dst}")
        copiados += 1
    print(f"\n✓ {copiados} archivos copiados "
          f"({reescritos} con rutas reescritas al layout publicable)")


if __name__ == "__main__":
    main()
