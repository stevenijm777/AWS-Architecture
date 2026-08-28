#!/usr/bin/env python3
"""
report_to_artifact.py — Adapta un reporte HTML completo al formato de publicación.

El publicador de artefactos envuelve el contenido en su propio
`<!doctype html><head>…</head><body>`, así que un documento que ya trae esas etiquetas
queda anidado dentro de otro y el resultado es HTML inválido. Este script extrae las
tres piezas que sí van —el `<style>`, el contenido del `<body>` y el `<script>`— y las
escribe planas, sin envoltorio.

No cambia una sola regla de estilo ni una línea de marcado: el reporte se ve igual.

Uso
---
    python scripts/report_to_artifact.py reporte_comparativo_actor_only.html
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def extraer(html: str) -> tuple[str, str, str, str]:
    """Devuelve (titulo, css, cuerpo, js). Falla ruidosamente si falta el cuerpo."""
    m_title = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    titulo = m_title.group(1).strip() if m_title else ""

    css = "\n".join(m.group(1) for m in
                    re.finditer(r"<style[^>]*>(.*?)</style>", html, re.S | re.I))
    js = "\n".join(m.group(1) for m in
                   re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>",
                               html, re.S | re.I))

    m_body = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    if not m_body:
        raise SystemExit("no encontré <body>…</body>; ¿es un documento HTML completo?")
    cuerpo = m_body.group(1)
    # el <script> ya se extrajo aparte; sacarlo del cuerpo evita duplicarlo
    cuerpo = re.sub(r"<script(?![^>]*\bsrc=)[^>]*>.*?</script>", "", cuerpo, flags=re.S | re.I)
    return titulo, css, cuerpo, js


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("entrada", type=Path)
    ap.add_argument("-o", "--salida", type=Path, default=None,
                    help="por defecto, el mismo nombre con sufijo _artifact")
    args = ap.parse_args()

    html = args.entrada.read_text(encoding="utf-8")
    titulo, css, cuerpo, js = extraer(html)

    # Referencias a archivos externos: dentro del artefacto no existe el disco local
    # y la política de seguridad bloquea cualquier host externo, así que una imagen o
    # una hoja de estilo por URL quedaría rota y en silencio. Mejor avisar acá.
    externos = re.findall(r'(?:src|href)="(?!data:|#|https?://fonts\.gstatic)([^"]+)"', cuerpo)
    externos = [u for u in externos if not u.startswith(("data:", "#", "javascript:"))]
    if externos:
        print(f"  ! {len(externos)} referencia(s) externa(s) que no van a cargar:",
              file=sys.stderr)
        for u in externos[:5]:
            print(f"      {u}", file=sys.stderr)

    salida = args.salida or args.entrada.with_name(args.entrada.stem + "_artifact.html")
    partes = [f"<title>{titulo}</title>" if titulo else "",
              f"<style>\n{css}\n</style>" if css.strip() else "",
              cuerpo.strip(),
              f"<script>\n{js}\n</script>" if js.strip() else ""]
    salida.write_text("\n".join(p for p in partes if p), encoding="utf-8")

    print(f"✓ {salida.name}  ({salida.stat().st_size/1e6:.2f} MB)")
    print(f"  título: {titulo or '(sin <title>)'}")
    print(f"  css {len(css)/1e3:.0f} KB · cuerpo {len(cuerpo)/1e6:.2f} MB · js {len(js)/1e3:.0f} KB")


if __name__ == "__main__":
    main()
