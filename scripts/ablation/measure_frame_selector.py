#!/usr/bin/env python3
"""
measure_frame_selector.py — Re-corre el selector de pizarra y lo compara con la curación humana.

Qué mide, y qué NO mide
-----------------------
No existe un "frame óptimo" anotado de forma independiente: la única etiqueta disponible
es la imagen que un humano aprobó, y ese humano aprobó mirando **la propuesta del propio
selector**. Así que esto **no es la precisión de un clasificador contra un ground truth
independiente** y no debe reportarse como tal.

Lo que sí es medible, y honesto:

  * **tasa de aceptación**: en cuántos videos el frame que el selector elige hoy es
    exactamente el que quedó aprobado (byte a byte, vía el manifiesto);
  * **distancia cuando falla**: cuántos frames separan la elección automática de la
    aprobada, que distingue "erró por un frame contiguo" de "erró de escena".

Los videos cuya imagen curada fue un **reemplazo manual** (`origen = reemplazo_manual` en
el manifiesto) son, por construcción, casos donde el humano descartó la propuesta: se
cuentan aparte como fallos conocidos del selector.

Garantía de seguridad
---------------------
**Solo lectura.** Nunca escribe en `data/good_whiteboard/` ni en `data/frames/`. La única
salida es el JSON de resultados. No gasta llamadas a la API: es OpenCV sobre frames ya
extraídos.

Uso
---
    .venv/bin/python scripts/ablation/measure_frame_selector.py --limit 20
    .venv/bin/python scripts/ablation/measure_frame_selector.py
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.core.frame_selector import select_best_frame  # noqa: E402

console = Console()
MANIFEST = PROJECT_ROOT / "data" / "whiteboard_manifest.csv"
FRAMES = PROJECT_ROOT / "data" / "frames"
OUT = PROJECT_ROOT / "reports" / "frame_selector_eval.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    if not MANIFEST.exists():
        console.print("[red]✗ Falta data/whiteboard_manifest.csv — "
                      "corré scripts/utils/build_whiteboard_manifest.py primero.[/]")
        raise SystemExit(1)

    filas = [r for r in csv.DictReader(open(MANIFEST, encoding="utf-8"))
             if (FRAMES / r["video_id"]).is_dir()]
    if args.limit:
        filas = filas[:args.limit]
    console.print(f"[bold]{len(filas)}[/] videos con frames locales\n")

    res, errores = [], 0
    for i, r in enumerate(filas, 1):
        vid = r["video_id"]
        try:
            # write_outputs=False es lo que hace de esto una medicion no destructiva:
            # sin ese flag, select_best_frame sobrescribe <video>_pizarra/ y vuelve a
            # sembrar bad_whiteboard/, que es la bandeja de revision manual.
            pick = select_best_frame(vid, frames_dir=FRAMES, write_outputs=False)
        except Exception as e:  # un video sin frames legibles no debe cortar la corrida
            console.print(f"  [yellow]⚠ {vid}: {str(e)[:70]}[/]")
            errores += 1
            continue

        elegido = Path(pick["source_frame"]).name       # el frame ORIGINAL, no la copia
        aprobado = r["frame_archivo"]

        def num(nombre: str) -> int | None:
            try:
                return int(nombre.split("_frame_")[-1].split(".")[0])
            except Exception:
                return None

        n_auto, n_hum = num(elegido), num(aprobado)
        res.append({
            "video_id": vid,
            "origen_curado": r["origen"],
            "frame_aprobado": aprobado,
            "frame_automatico": elegido,
            "coincide": bool(aprobado) and elegido == aprobado,
            "distancia_frames": (abs(n_auto - n_hum) if n_auto is not None and n_hum is not None else None),
            "frames_totales": int(r["frames_extraidos"] or 0),
            # Señales de confianza: sirven para triar a mano cuáles de los 446 conviene
            # mirar. `uso_fallback` es la bandera roja fuerte — el selector no encontró
            # ni un candidato válido y devolvió el último frame por descarte.
            "uso_fallback": bool(pick.get("uso_fallback")),
            "num_iconos": int(pick.get("num_iconos", 0)),
            "score": round(float(pick.get("final_score", 0.0)), 3),
            "oclusion_pct": round(float(pick.get("occlusion_pct", 0.0)), 2),
            "descartados": int(pick.get("discarded_count", 0)),
            "candidatos": int(pick.get("candidatos_analizados", 0)),
        })
        if i % 25 == 0:
            console.print(f"[dim]  {i}/{len(filas)}[/]")

    extraidos = [r for r in res if r["origen_curado"] == "frame_extraido"]
    reemplazos = [r for r in res if r["origen_curado"] == "reemplazo_manual"]
    aciertos = sum(r["coincide"] for r in extraidos)

    t = Table(title="Selector automático vs curación humana", border_style="cyan")
    t.add_column("caso"); t.add_column("n", justify="right"); t.add_column("%", justify="right")
    if extraidos:
        t.add_row("elige el MISMO frame que quedó aprobado", str(aciertos),
                  f"{100*aciertos/len(extraidos):.1f} %")
        t.add_row("elige otro frame", str(len(extraidos) - aciertos),
                  f"{100*(len(extraidos)-aciertos)/len(extraidos):.1f} %")
    t.add_row("[dim]fallo conocido (el humano reemplazó la imagen)[/]", str(len(reemplazos)), "—")
    console.print(t)

    fallos = [r["distancia_frames"] for r in extraidos
              if not r["coincide"] and r["distancia_frames"] is not None]
    if fallos:
        fallos.sort()
        console.print(f"\ncuando no coincide, distancia mediana: "
                      f"[bold]{fallos[len(fallos)//2]}[/] frames "
                      f"(min {fallos[0]}, max {fallos[-1]})")

    fallbacks = [r for r in res if r["uso_fallback"]]
    pobres = [r for r in res if not r["uso_fallback"] and r["num_iconos"] <= 1]
    console.print(f"\n[bold]Señales para triar a mano:[/]")
    console.print(f"  usó FALLBACK (ningún candidato válido) : [bold red]{len(fallbacks)}[/]")
    console.print(f"  eligió con 0–1 íconos detectados        : [yellow]{len(pobres)}[/]")

    # CSV además del JSON: es lo que se abre en una planilla para revisar video por video.
    CSV_OUT = OUT.with_suffix(".csv")
    if res:
        with open(CSV_OUT, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(res[0]))
            w.writeheader()
            # Los sospechosos primero: fallback, después pocos íconos, después score bajo.
            w.writerows(sorted(res, key=lambda r: (not r["uso_fallback"], r["num_iconos"], r["score"])))
        console.print(f"[green]✓[/] {CSV_OUT.relative_to(PROJECT_ROOT)}  [dim](ordenado: sospechosos primero)[/]")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "generado_por": "scripts/ablation/measure_frame_selector.py",
        "advertencia": "NO es precision contra un ground truth independiente: la etiqueta "
                       "humana se produjo mirando la propuesta del propio selector.",
        "n_evaluados": len(res),
        "n_frame_extraido": len(extraidos),
        "n_reemplazo_manual": len(reemplazos),
        "aciertos_exactos": aciertos,
        "tasa_aceptacion": round(100 * aciertos / len(extraidos), 2) if extraidos else None,
        "errores_de_lectura": errores,
        "por_video": res,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}")
    console.print("[dim]Solo lectura: no se tocó ninguna imagen.[/]")


if __name__ == "__main__":
    main()
