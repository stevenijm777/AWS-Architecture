#!/usr/bin/env python3
"""
migrar_a_repo_oficial.py — Lleva al repositorio oficial lo que respalda la revisión de octubre.

Copia, desde este repositorio de trabajo (AWS-Architecture) al oficial
(aws-architecture-extraction), solo lo necesario para verificar las cifras nuevas del paper:

  prompts/                       V9 y la variante sin "Unidirectional Default", con su entrada
                                 en MANIFEST.json
  results/<carpeta>/             run.json, results.csv, comparaciones y documentación de cada
                                 corrida (sin las salidas crudas de Claude ni los fotogramas)
  data/stage1_world_models/      las lecturas de Stage 1 de Flash, Pro y Claude, y el Stage 1 en
                                 caché que usaron las corridas de producción
  scripts/                       los scripts nuevos o modificados, con las rutas del repo oficial
  notebooks/hipotesis/           los notebooks H1–H7 y su módulo `comun.py`

No copia el ground truth ni las pizarras, que el repositorio oficial no redistribuye, ni el
World Model oráculo, que es una conversión del ground truth.

No hace commit: deja los archivos en el árbol de trabajo para revisarlos con `git status`.

    python scripts/utils/migrar_a_repo_oficial.py            # muestra qué copiaría
    python scripts/utils/migrar_a_repo_oficial.py --aplicar
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ORIGEN = Path(__file__).resolve().parent.parent.parent
DESTINO = ORIGEN.parent / "aws-architecture-extraction"
REP = ORIGEN / "reports"
LAB = ORIGEN / "whiteboard_selection_lab" / "lab_workspace"
PANEL = [
    "-3lnf5lzsH0", "-kA0ahrhX3I", "-wLEkq21cvA", "07lfvavMdfU", "1aYoIZvabbk", "2L0m28ZLmtE",
    "2e3vOxsHekE", "6CgqEzyWpeA", "6EUknQqaV1w", "6YkguepAQuQ", "BZ32w0SSAoY", "Cgv0kfp_6xQ",
    "wjtSHyENv0I", "ww5fiygF6eg", "2XVgpMwY5iE", "7V8wTCkjOqo", "90rWUjKjnAE", "9qTEHITVeLE",
    "BlCXEMp_lqY", "FfSNnH2bbNc", "H2fOkeXxpyw", "JYeXbUdFOdw", "SSWwnNVYi_Q", "a6kqyqTNJM4",
    "c-1GXhOOOww", "f5EJBUfGZtw", "hMK2NJ-q9nc", "jV8DwutbXbg", "jg85DzUZ9Ac", "u3ZwnulzLnU",
]
PROMPTS_NUEVOS = ["stage2_v9_connection_ledger.txt", "stage2_v6_no_unidirectional.txt"]
# Carpetas de resultados que se copian enteras (solo los archivos de RESULTADO).
CARPETAS = ["pro_vs_flash", "prompt_v9", "stage1_vs_manual", "permisivo_semana", "claude",
            "claude_oracle_gt", "claude_oracle_gt_v9", "claude_oracle_gt_v9_rep2", "claude_produccion_v9"]
RESULTADO = {"run.json", "results.csv", "comparacion.md", "comparacion.json", "README.md",
             "PROMPT_STAGE2.md", "schema.json", "videos.json", "permisivo_semana.md", "permisivo_semana.json"}
LECTURAS = {"s1-flash": "world_model_s1-flash.json", "s1-pro": "world_model_s1-pro.json",
            "s1-claude": "world_model_s1-claude.json", "s1-flash-img": "world_model_s1-flash-img.json",
            "s1-pro-img": "world_model_s1-pro-img.json", "s1-claude-img": "world_model_s1-claude-img.json",
            "produccion_flash": "world_model.json"}
SCRIPTS = ["scripts/ablation/rerun_panel.py", "scripts/ablation/claude_panel.py",
           "scripts/ablation/compare_models.py", "scripts/ablation/stage1_panel.py",
           "scripts/ablation/evaluate_permissive_week.py", "scripts/ablation/figuras_paper_v3.py",
           "scripts/utils/ejecutar_notebooks.py", "scripts/utils/migrar_a_repo_oficial.py"]


def adaptar(texto: str) -> str:
    """Rutas e imports del repositorio de trabajo → los del oficial."""
    texto = texto.replace("from scripts.core.graph_builder", "from scripts.evaluation.graph_builder")
    texto = texto.replace("from scripts.utils.evaluate_graphs", "from scripts.evaluation.evaluate_graphs")
    texto = texto.replace('/ "reports"', '/ "results"').replace('"reports" /', '"results" /')
    texto = re.sub(r"(?<![\w.])reports([/\\])", r"results\1", texto)
    texto = texto.replace(".venv/Scripts/python ", "python ").replace(".venv/bin/python ", "python ")
    texto = re.sub(r"lab_workspace/<vid>/world_model_(s1-[a-z-]+)\.json", r"data/stage1_world_models/\1/<vid>.json", texto)
    return texto


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true", help="copiar de verdad (sin esto solo lista)")
    args = ap.parse_args()
    if not DESTINO.exists():
        raise SystemExit(f"No encuentro el repositorio oficial en {DESTINO}")
    plan: list[tuple[Path, Path, bool]] = []          # (origen, destino, adaptar texto)

    for f in PROMPTS_NUEVOS:
        plan.append((ORIGEN / "src/configs/prompts" / f, DESTINO / "prompts" / f, False))
    for carpeta in CARPETAS:
        for f in sorted((REP / carpeta).rglob("*")):
            rel = f.relative_to(REP / carpeta)
            if f.is_file() and f.name in RESULTADO and "videos" not in rel.parts and "_simbolos" not in rel.parts:
                plan.append((f, DESTINO / "results" / carpeta / rel, f.suffix == ".md"))
    for nombre, archivo in LECTURAS.items():
        for vid in PANEL:
            src = LAB / vid / archivo
            if src.exists():
                plan.append((src, DESTINO / "data" / "stage1_world_models" / nombre / f"{vid}.json", False))
    for s in SCRIPTS:
        plan.append((ORIGEN / s, DESTINO / s, True))
    for f in sorted((ORIGEN / "hipotesis").glob("*")):
        if f.is_file() and f.suffix in (".ipynb", ".py", ".md"):
            plan.append((f, DESTINO / "notebooks" / "hipotesis" / f.name, f.suffix in (".ipynb", ".md")))

    faltan = [o for o, _, _ in plan if not o.exists()]
    if faltan:
        raise SystemExit("Faltan en origen: " + ", ".join(map(str, faltan)))
    print(f"{len(plan)} archivos → {DESTINO}")
    por_destino: dict[str, int] = {}
    for _, d, _ in plan:
        k = str(d.relative_to(DESTINO).parts[0] + "/" + (d.relative_to(DESTINO).parts[1] if len(d.relative_to(DESTINO).parts) > 2 else ""))
        por_destino[k] = por_destino.get(k, 0) + 1
    for k, n in sorted(por_destino.items()):
        print(f"  {k:40s} {n}")
    if not args.aplicar:
        print("— solo listado; usa --aplicar para copiar —")
        return

    for o, d, texto in plan:
        d.parent.mkdir(parents=True, exist_ok=True)
        if o.suffix == ".ipynb":
            # Se adaptan solo las fuentes; las salidas se borran y se regeneran ejecutando el
            # notebook en el repo oficial (así tampoco viajan las pizarras incrustadas).
            nb = json.loads(o.read_text(encoding="utf-8"))
            for cell in nb["cells"]:
                src = adaptar("".join(cell["source"]))
                ls = src.split("\n")
                cell["source"] = [l + "\n" for l in ls[:-1]] + [ls[-1]]
                if cell["cell_type"] == "code":
                    cell["outputs"], cell["execution_count"] = [], None
            d.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
        elif texto:
            d.write_text(adaptar(o.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(o, d)

    # Entradas del MANIFEST para los prompts nuevos, sin tocar las existentes.
    m_origen = json.loads((ORIGEN / "src/configs/prompts/MANIFEST.json").read_text(encoding="utf-8"))
    m_dest_p = DESTINO / "prompts" / "MANIFEST.json"
    m_dest = json.loads(m_dest_p.read_text(encoding="utf-8"))
    ya = {p["file"] for p in m_dest["prompts"]}
    nuevas = [p for p in m_origen["prompts"] if p["file"] in PROMPTS_NUEVOS and p["file"] not in ya]
    m_dest["prompts"] += nuevas
    m_dest_p.write_text(json.dumps(m_dest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ copiado · {len(nuevas)} entradas nuevas en prompts/MANIFEST.json")


if __name__ == "__main__":
    main()
