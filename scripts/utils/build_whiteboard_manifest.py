#!/usr/bin/env python3
"""
build_whiteboard_manifest.py — Registra QUÉ frame exacto se usó en el estudio.

El problema que resuelve
------------------------
Las 446 imágenes de `data/good_whiteboard/` son la entrada visual real de cada llamada
a Gemini, pero **no se pueden redistribuir**: son capturas de los videos de AWS
*This is My Architecture*, obra de terceros. La misma razón por la que este proyecto no
republica Cloudscape.

Sin las imágenes, alguien que reproduzca el trabajo va a re-extraer frames del video y
obtener **otro** frame — y no habría forma de saber cuál se usó. Este script deja ese
registro: para cada video, el hash exacto de la imagen usada y, cuando la imagen es un
frame extraído sin modificar, **qué frame es**.

Con eso, un tercero puede: extraer los frames, tomar el que dice el manifiesto, y
verificar por SHA-256 que tiene byte a byte la misma imagen que se usó acá.

Garantía de seguridad
---------------------
**Este script es de solo lectura.** No escribe, mueve ni sobrescribe nada dentro de
`data/good_whiteboard/` ni de `data/frames/`. Su única salida es el CSV del manifiesto.

Uso
---
    .venv/bin/python scripts/utils/build_whiteboard_manifest.py
    .venv/bin/python scripts/utils/build_whiteboard_manifest.py --limit 40   # prueba rápida
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
from pathlib import Path

from rich.console import Console
from rich.progress import track

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
GOOD_WB = PROJECT_ROOT / "data" / "good_whiteboard"
FRAMES = PROJECT_ROOT / "data" / "frames"
OUT = PROJECT_ROOT / "data" / "whiteboard_manifest.csv"

console = Console()
FRAME_RE = re.compile(r"_frame_(\d+)\.jpg$")


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def localizar_frame(img: Path, carpeta: Path) -> tuple[str, str]:
    """Devuelve (nombre_del_frame, numero_de_frame) si la imagen ES un frame extraído.

    Compara primero por tamaño en bytes —que descarta casi todo sin leer— y solo
    entonces por hash. Devuelve ("", "") si ningún frame coincide, que es el caso de las
    imágenes que un humano reemplazó por otra toma.
    """
    if not carpeta.is_dir():
        return "", ""
    objetivo, n = sha256(img), img.stat().st_size
    for f in sorted(carpeta.glob("*.jpg")):
        if f.stat().st_size == n and sha256(f) == objetivo:
            m = FRAME_RE.search(f.name)
            return f.name, (m.group(1) if m else "")
    return "", ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=None, help="procesar solo N videos (prueba)")
    args = ap.parse_args()

    # Un jpg por video: se excluyen las variantes anotadas que genera el detector.
    imgs = sorted(p for p in GOOD_WB.glob("*.jpg")
                  if not re.search(r"_(annotated|processed|symbols)", p.stem))
    if args.limit:
        imgs = imgs[:args.limit]
    console.print(f"[bold]{len(imgs)}[/] pizarras curadas a registrar\n")

    filas, exactos, reemplazadas, sin_frames = [], 0, 0, 0
    for img in track(imgs, description="verificando…"):
        vid = img.stem
        carpeta = FRAMES / vid
        if carpeta.is_dir():
            nombre, num = localizar_frame(img, carpeta)
            if nombre:
                origen, exactos = "frame_extraido", exactos + 1
            else:
                origen, exactos = "reemplazo_manual", exactos
                reemplazadas += 1
            n_frames = len(list(carpeta.glob("*.jpg")))
        else:
            nombre = num = ""
            origen = "sin_frames_locales"
            n_frames = 0
            sin_frames += 1

        filas.append({
            "video_id": vid,
            "sha256": sha256(img),
            "bytes": img.stat().st_size,
            "origen": origen,
            "frame_archivo": nombre,
            "frame_numero": num,
            "frames_extraidos": n_frames,
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)

    n = len(filas)
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}  ({n} filas)")
    console.print(f"  frame extraído sin modificar : [bold]{exactos}[/] ({100*exactos/n:.1f} %)")
    console.print(f"  reemplazo manual             : [bold]{reemplazadas}[/] ({100*reemplazadas/n:.1f} %)")
    if sin_frames:
        console.print(f"  [yellow]sin frames locales           : {sin_frames}[/] "
                      f"(no se puede determinar el origen sin re-extraer)")
    console.print("\n[dim]Solo lectura: no se tocó ninguna imagen.[/]")


if __name__ == "__main__":
    main()
