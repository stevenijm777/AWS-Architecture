#!/usr/bin/env python3
"""
extract_prompts_parsimonious.py — Materializa el linaje de prompts del brazo Parsimonious.

Por qué existe
--------------
El brazo Standard ya tiene sus prompts extraídos a `.txt` con SHA-256
(`extract_prompts.py` + `MANIFEST.json`), y por eso cada corrida suya es atribuible a un
texto concreto. Parsimonious no: sus prompts viven **dentro de la bitácora**
`whiteboard_selection_lab/parsimonious_prompt_history.md`, como bloques de código bajo
encabezados del tipo *"### Prompt Utilizado (Prompt v9)"*.

Consecuencia práctica, la misma que tenía Standard antes de arreglarlo: las tablas
publicadas de Parsimonious guardan el **nombre** de la variante ("Prompt v9"), no el hash
del texto, así que sus filas no se pueden atribuir a un prompt concreto después del hecho.

Este script cierra ese hueco sin tocar la bitácora: la lee, extrae cada bloque, lo asocia
al Registro y al nombre de versión que lo encabeza, y escribe:

    src/configs/prompts/parsimonious/<version>__reg<N>.txt
    src/configs/prompts/parsimonious/MANIFEST.json

Es de **solo lectura** sobre la bitácora y sobre cualquier archivo de Melissa. La única
salida es el directorio de prompts materializados.

Deduplicación
-------------
La bitácora repite el mismo texto en registros consecutivos cuando una corrida reusa el
prompt anterior. Se deduplica por hash: un texto = una entrada, con la lista de todos los
registros que lo usaron. Así el manifiesto dice *"este texto se usó en los registros 12 y
13"*, que es exactamente lo que hace falta para atribuir una corrida.

Uso
---
    .venv/bin/python scripts/utils/extract_prompts_parsimonious.py
    .venv/bin/python scripts/utils/extract_prompts_parsimonious.py --check
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
HISTORIA = PROJECT_ROOT / "whiteboard_selection_lab" / "parsimonious_prompt_history.md"
OUT_DIR = PROJECT_ROOT / "src" / "configs" / "prompts" / "parsimonious"
PRODUCCION = PROJECT_ROOT / "scripts" / "core" / "vision_analyzer_parsimonious.py"

console = Console()

RE_REGISTRO = re.compile(r"^## \[Registro (\d+)\][^(]*\(([^)]*)\)")
RE_ENCABEZADO = re.compile(r"^#{3,4}\s*Prompt Utilizado[^\n]*", re.I)
RE_VERSION = re.compile(r"[Pp]rompt\s+(v\d+)")


def normalizar(t: str) -> str:
    """Insensible a espacios: reformatear no cambia la identidad del prompt."""
    return re.sub(r"\s+", " ", t).strip()


def sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def extraer() -> list[dict]:
    lineas = HISTORIA.read_text(encoding="utf-8").splitlines()
    registro = titulo = encabezado = None
    fuera: list[dict] = []
    i = 0
    while i < len(lineas):
        l = lineas[i]
        m = RE_REGISTRO.match(l)
        if m:
            registro, titulo = int(m.group(1)), m.group(2).strip()
        if RE_ENCABEZADO.match(l.strip()):
            encabezado = l.strip()
        if l.strip().startswith("```"):
            j = i + 1
            cuerpo: list[str] = []
            while j < len(lineas) and not lineas[j].strip().startswith("```"):
                cuerpo.append(lineas[j]); j += 1
            texto = "\n".join(cuerpo)
            # Solo bloques que son realmente un prompt, no salidas ni JSON de ejemplo.
            if len(texto) > 500 and ("You are" in texto or "PLACEHOLDER" in texto):
                v = RE_VERSION.search(encabezado or "") or RE_VERSION.search(titulo or "")
                fuera.append({
                    "registro": registro,
                    "titulo_registro": titulo,
                    "version": v.group(1) if v else None,
                    "texto": texto,
                    "chars": len(texto),
                    "sha256": sha(normalizar(texto)),
                })
            i = j
        i += 1
    return fuera


NOTEBOOK_LAB = (PROJECT_ROOT / "whiteboard_selection_lab"
                / "prompt_batch_ablation_lab_parsimonious.ipynb")


def texto_de_produccion() -> str | None:
    if not PRODUCCION.exists():
        return None
    m = re.search(r'CLOUDSCAPE_PROMPT_TEMPLATE\s*=\s*"""(.*?)"""',
                  PRODUCCION.read_text(encoding="utf-8"), re.S)
    return m.group(1) if m else None


def texto_del_notebook() -> str | None:
    """El notebook de ablación define su propio PROMPT_V9_TEXT, que no tiene por qué
    coincidir con el de producción ni con el de la bitácora — y de hecho no coincide."""
    if not NOTEBOOK_LAB.exists():
        return None
    nb = json.loads(NOTEBOOK_LAB.read_text(encoding="utf-8"))
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        m = re.search(r'PROMPT_V9_TEXT\s*=\s*[f]?"""(.*?)"""', "".join(c["source"]), re.S)
        if m:
            return m.group(1)
    return None


def prompt_de_produccion() -> str | None:
    t = texto_de_produccion()
    return sha(normalizar(t)) if t else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verificar sin escribir")
    args = ap.parse_args()

    if not HISTORIA.exists():
        console.print(f"[red]✗ No existe {HISTORIA}[/]"); raise SystemExit(1)

    bloques = extraer()
    console.print(f"bloques de prompt encontrados en la bitácora: [bold]{len(bloques)}[/]")

    # Deduplicar por hash, conservando todos los registros que usaron ese texto.
    por_hash: dict[str, dict] = {}
    for b in bloques:
        e = por_hash.setdefault(b["sha256"], {**b, "registros": []})
        e["registros"].append(b["registro"])
        if e["version"] is None and b["version"]:
            e["version"] = b["version"]
    # El primer bloque de la bitácora aparece ANTES del primer `## [Registro N]`, así que
    # su lista de registros queda vacía. Se ordena al frente en vez de romper.
    def primer_registro(e: dict) -> int:
        regs = [r for r in e["registros"] if r]
        return min(regs) if regs else 0

    unicos = sorted(por_hash.values(), key=primer_registro)
    console.print(f"textos ÚNICOS tras deduplicar por hash: [bold]{len(unicos)}[/]\n")

    sha_prod = prompt_de_produccion()
    # Se evalúa contra los textos de la BITÁCORA únicamente. Si se calculara después de
    # añadir la entrada de producción daría True siempre, que es justo lo contrario de lo
    # que la bandera quiere decir.
    prod_en_bitacora = bool(sha_prod) and any(e["sha256"] == sha_prod for e in unicos)
    entradas = []
    for e in unicos:
        regs = sorted(r for r in e["registros"] if r)
        version = e["version"] or "vNA"
        nombre = f"{version}__reg{regs[0] if regs else 0}.txt"
        entradas.append({
            "name": f"PARSIMONIOUS_{version.upper()}",
            "file": nombre,
            "version": version,
            "registros": regs,
            "titulo_registro": e["titulo_registro"],
            "chars": e["chars"],
            "sha256": e["sha256"],
            "matches_production": e["sha256"] == sha_prod,
        })
        if not args.check:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            (OUT_DIR / nombre).write_text(e["texto"], encoding="utf-8")

    # Dos fuentes que la bitácora NO contiene y que sí corrieron: el prompt de producción
    # y el que define el notebook de ablación. Se materializan igual, porque sin ellos el
    # linaje no explica qué texto generó `data/graphs_parsimonious/`.
    for etiqueta, texto, fuente in [
        ("PRODUCCION", texto_de_produccion(), "scripts/core/vision_analyzer_parsimonious.py"),
        ("NOTEBOOK_ABLACION", texto_del_notebook(),
         "whiteboard_selection_lab/prompt_batch_ablation_lab_parsimonious.ipynb"),
    ]:
        if not texto:
            continue
        h = sha(normalizar(texto))
        if any(e["sha256"] == h for e in entradas):
            continue                      # ya estaba en la bitácora, no duplicar
        nombre = f"{etiqueta.lower()}.txt"
        entradas.append({
            "name": f"PARSIMONIOUS_{etiqueta}",
            "file": nombre,
            "version": "v9?",             # se declara como v9 pero no coincide con el v9 de la bitácora
            "registros": [],
            "titulo_registro": f"(no está en la bitácora — extraído de {fuente})",
            "chars": len(texto),
            "sha256": h,
            "matches_production": h == sha_prod,
            "fuente": fuente,
        })
        if not args.check:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            (OUT_DIR / nombre).write_text(texto, encoding="utf-8")

    t = Table(title="Linaje Parsimonious materializado", border_style="cyan")
    for c, j in [("archivo", "left"), ("versión", "left"), ("registros", "left"),
                 ("chars", "right"), ("sha", "left"), ("producción", "center")]:
        t.add_column(c, justify=j)
    for e in entradas:
        t.add_row(e["file"], e["version"],
                  ",".join(map(str, e["registros"]))[:22],
                  str(e["chars"]), e["sha256"][:12],
                  "← RUNNING" if e["matches_production"] else "")
    console.print(t)

    if not prod_en_bitacora:
        console.print("[yellow]⚠ El prompt de producción (vision_analyzer_parsimonious.py) "
                      "NO coincide con ningún texto de la bitácora.[/]\n"
                      f"  sha producción: {sha_prod[:12]}\n"
                      "  Es el mismo problema que este script existe para evitar: lo que corre "
                      "no está registrado. Queda declarado en el manifiesto.")

    manifiesto = {
        "generated_on": str(date.today()),
        "source": "whiteboard_selection_lab/parsimonious_prompt_history.md",
        "note": "Prompts del brazo Parsimonious extraidos de la bitacora. Deduplicados por "
                "SHA-256 sobre el texto normalizado en espacios; `registros` lista todos los "
                "registros que usaron ese mismo texto.",
        "production_sha256": sha_prod,
        "production_in_history": prod_en_bitacora,
        "n_bloques_leidos": len(bloques),
        "n_textos_unicos": len(entradas),
        "brechas_de_trazabilidad": {
            "v10_sin_texto": ("El Registro 27 reporta resultados con 'Prompt v10' pero su "
                              "texto no aparece en ningun bloque de la bitacora ni en el "
                              "codigo. Esa variante no es reproducible."),
            "tres_textos_llamados_v9": ("La bitacora (reg 17-18), el notebook de ablacion "
                                        "(PROMPT_V9_TEXT) y produccion "
                                        "(vision_analyzer_parsimonious.py) declaran ser v9 "
                                        "y tienen tres SHA-256 distintos."),
            "implicacion": ("Las tablas publicadas de Parsimonious citan el NOMBRE de la "
                            "variante, no su hash, asi que sus filas no son atribuibles a "
                            "un texto concreto. Mismo problema que Standard tenia antes de "
                            "extract_prompts.py."),
        },
        "prompts": entradas,
    }
    if not args.check:
        (OUT_DIR / "MANIFEST.json").write_text(
            json.dumps(manifiesto, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"\n[green]✓[/] {OUT_DIR.relative_to(PROJECT_ROOT)} "
                      f"({len(entradas)} .txt + MANIFEST.json)")
    else:
        console.print("\n[dim]— --check: no se escribió nada —[/]")
    console.print("[dim]Solo lectura sobre la bitácora: no se modificó ningún archivo de Melissa.[/]")


if __name__ == "__main__":
    main()
