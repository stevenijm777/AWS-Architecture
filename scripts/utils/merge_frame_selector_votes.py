#!/usr/bin/env python3
"""
merge_frame_selector_votes.py — Cruza el voto humano con las métricas del selector.

Junta `reports/frame_selector_eval.csv` (calculado por measure_frame_selector.py) con
`reports/frame_selector_review/frame_selector_votes.csv` (exportado a mano desde la
galería HTML) y calcula las métricas de precisión del selector — sobre el universo
completo de los 440 videos evaluados, sin excluir ninguno por otra razón (p. ej. GT
marcado `graph_usable=False`): esta medición evalúa la ETAPA DE SELECCIÓN DE FRAME en
sí misma, no el resultado final del pipeline, así que su denominador es independiente de
qué video terminó siendo usable para las métricas de arquitectura.

Dos preguntas, dos métricas, no una sola:

  1. **Reproducibilidad**: ¿el selector de HOY reproduce, byte a byte, el frame que
     realmente se usó en el estudio? (`coincide` en frame_selector_eval.csv — no
     requiere juicio humano, es un hash).
  2. **Precisión funcional**: cuando NO lo reproduce, ¿la alternativa que elige HOY
     sigue siendo una pizarra utilizable? (el voto humano — "si"/"no"/"duda").

La cifra que importa para el paper es la combinación de las dos: cuántos de los 440
casos, hoy, terminan en una imagen utilizable — sea porque coincide con la usada, sea
porque la alternativa también sirve.

Uso
---
    .venv/bin/python scripts/utils/merge_frame_selector_votes.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
EVAL_CSV = PROJECT_ROOT / "reports" / "frame_selector_eval.csv"
VOTES_CSV = PROJECT_ROOT / "reports" / "frame_selector_review" / "frame_selector_votes.csv"
OUT = PROJECT_ROOT / "reports" / "frame_selector_precision.json"

console = Console()


def main() -> None:
    for p in (EVAL_CSV, VOTES_CSV):
        if not p.exists():
            console.print(f"[red]✗ Falta {p}[/]")
            raise SystemExit(1)

    ev = {r["video_id"]: r for r in csv.DictReader(open(EVAL_CSV, encoding="utf-8"))}
    votos = {r["video_id"]: r["juicio"] for r in csv.DictReader(open(VOTES_CSV, encoding="utf-8"))}

    faltan = set(ev) - set(votos)
    if faltan:
        console.print(f"[yellow]⚠ {len(faltan)} videos de frame_selector_eval.csv sin voto "
                      f"en el CSV exportado — se excluyen del cálculo: {sorted(faltan)[:5]}…[/]")

    filas = [{**ev[v], "juicio": votos[v]} for v in ev if v in votos]
    n = len(filas)
    console.print(f"[bold]{n}[/] videos con voto y métrica cruzados\n")

    # ── 1. Reproducibilidad: coincide byte a byte con la imagen usada ──
    coincide = [r for r in filas if r["coincide"] == "True"]
    no_coincide = [r for r in filas if r["coincide"] != "True"]
    tasa_reproducibilidad = len(coincide) / n

    # ── 2. De las que NO coinciden, ¿la alternativa de hoy sirve? ──
    si = [r for r in no_coincide if r["juicio"] == "si"]
    no = [r for r in no_coincide if r["juicio"] == "no"]
    duda = [r for r in no_coincide if r["juicio"] == "duda"]
    tasa_alternativa_valida = len(si) / len(no_coincide) if no_coincide else 0.0

    # ── 3. Precisión funcional combinada: cuantos terminan en imagen utilizable HOY ──
    # coincide=True cuenta como utilizable salvo que el propio voto lo marque en duda
    # (es el caso e3N5ZuHh7G0: coincide=True, pero el humano marco 'duda' porque la
    # imagen aprobada -y por lo tanto tambien la de hoy, son la misma- tiene un problema
    # de calidad visible). Ese caso NO se cuenta como funcionalmente valido.
    coincide_ok = [r for r in coincide if r["juicio"] != "duda"]
    coincide_duda = [r for r in coincide if r["juicio"] == "duda"]
    utilizables_hoy = len(coincide_ok) + len(si)
    precision_funcional = utilizables_hoy / n

    # ── 4. Desglose por severidad (dentro de los que NO coinciden) ──
    por_seccion = {}
    for sec in ("fallback", "pobres", "discrepancia"):
        grp = [r for r in no_coincide if r["uso_fallback"] == "True"] if sec == "fallback" else \
              [r for r in no_coincide if r["uso_fallback"] != "True" and int(r["num_iconos"]) <= 1] if sec == "pobres" else \
              [r for r in no_coincide if r["uso_fallback"] != "True" and int(r["num_iconos"]) > 1]
        if not grp:
            continue
        s = sum(1 for r in grp if r["juicio"] == "si")
        por_seccion[sec] = {"n": len(grp), "validas": s, "tasa": round(s / len(grp), 4)}

    # ── 5. Cruce con origen de la imagen APROBADA (frame extraído vs reemplazo manual) ──
    por_origen = {}
    for origen in ("frame_extraido", "reemplazo_manual"):
        grp = [r for r in filas if r["origen_curado"] == origen]
        if not grp:
            continue
        coinc = sum(1 for r in grp if r["coincide"] == "True")
        ok = sum(1 for r in grp if (r["coincide"] == "True" and r["juicio"] != "duda")
                 or (r["coincide"] != "True" and r["juicio"] == "si"))
        por_origen[origen] = {
            "n": len(grp), "coincide": coinc, "tasa_coincide": round(coinc / len(grp), 4),
            "utilizables_hoy": ok, "tasa_utilizable": round(ok / len(grp), 4),
        }

    # ── reporte ──
    t = Table(title="Precisión del selector de pizarra — 440 videos, voto humano cruzado", border_style="cyan")
    t.add_column("métrica", style="bold"); t.add_column("valor", justify="right")
    t.add_row("Reproducibilidad (coincide byte a byte)", f"{len(coincide)}/{n} = {100*tasa_reproducibilidad:.1f}%")
    t.add_row("  · de esos, con problema de calidad (duda)", f"{len(coincide_duda)}")
    t.add_row("Alternativa válida cuando NO coincide", f"{len(si)}/{len(no_coincide)} = {100*tasa_alternativa_valida:.1f}%")
    t.add_row("  · no válida", f"{len(no)}")
    t.add_row("  · dudosa", f"{len(duda)}")
    t.add_row("[bold]Precisión funcional combinada[/]", f"[bold]{utilizables_hoy}/{n} = {100*precision_funcional:.1f}%[/]")
    console.print(t)

    t2 = Table(title="Por severidad (dentro de los que NO coinciden)", border_style="cyan")
    t2.add_column("categoría"); t2.add_column("n", justify="right"); t2.add_column("válidas", justify="right"); t2.add_column("tasa", justify="right")
    for sec, d in por_seccion.items():
        t2.add_row(sec, str(d["n"]), str(d["validas"]), f"{100*d['tasa']:.1f}%")
    console.print(t2)

    t3 = Table(title="Por origen de la imagen aprobada", border_style="cyan")
    t3.add_column("origen"); t3.add_column("n", justify="right")
    t3.add_column("coincide hoy", justify="right"); t3.add_column("utilizable hoy", justify="right")
    for origen, d in por_origen.items():
        t3.add_row(origen, str(d["n"]), f"{d['coincide']} ({100*d['tasa_coincide']:.1f}%)",
                   f"{d['utilizables_hoy']} ({100*d['tasa_utilizable']:.1f}%)")
    console.print(t3)

    OUT.write_text(json.dumps({
        "generado_por": "scripts/utils/merge_frame_selector_votes.py",
        "n_total": n,
        "n_sin_voto_excluidos": len(faltan),
        "reproducibilidad": {"n": len(coincide), "tasa": round(tasa_reproducibilidad, 4)},
        "alternativa_valida_si_no_coincide": {
            "n_no_coincide": len(no_coincide), "si": len(si), "no": len(no), "duda": len(duda),
            "tasa": round(tasa_alternativa_valida, 4),
        },
        "precision_funcional_combinada": {"n": utilizables_hoy, "tasa": round(precision_funcional, 4)},
        "coincide_pero_calidad_dudosa": [r["video_id"] for r in coincide_duda],
        "por_severidad": por_seccion,
        "por_origen_imagen_aprobada": por_origen,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
