#!/usr/bin/env python3
"""
ejecutar_notebooks.py — Re-ejecuta notebooks en su lugar, sin Jupyter ni nbconvert.

Corre cada celda de código en un espacio de nombres compartido, desde la carpeta del
notebook, y reemplaza sus salidas: texto impreso, el valor de la última expresión (con su
representación HTML si la tiene) y las figuras de matplotlib abiertas. Sirve para los
notebooks de hipotesis/, que solo necesitan numpy, matplotlib y Pillow.

    python scripts/utils/ejecutar_notebooks.py hipotesis/H1_*.ipynb
"""
from __future__ import annotations

import ast
import base64
import contextlib
import io
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
import matplotlib.pyplot as plt  # noqa: E402


def lineas(texto: str) -> list[str]:
    ls = texto.split("\n")
    return [l + "\n" for l in ls[:-1]] + [ls[-1]]


def ejecutar_celda(codigo: str, ns: dict) -> list[dict]:
    outs, buf = [], io.StringIO()
    arbol = ast.parse(codigo)
    ultimo = arbol.body.pop() if arbol.body and isinstance(arbol.body[-1], ast.Expr) else None
    valor = None
    with contextlib.redirect_stdout(buf):
        exec(compile(arbol, "<celda>", "exec"), ns)
        if ultimo is not None:
            valor = eval(compile(ast.Expression(ultimo.value), "<celda>", "eval"), ns)
    if buf.getvalue():
        outs.append({"output_type": "stream", "name": "stdout", "text": lineas(buf.getvalue())})
    if valor is not None:
        data = {"text/plain": lineas(repr(valor))}
        if hasattr(valor, "_repr_html_"):
            data["text/html"] = lineas(valor._repr_html_())
        outs.append({"output_type": "execute_result", "execution_count": None, "metadata": {}, "data": data})
    for num in plt.get_fignums():
        png = io.BytesIO()
        plt.figure(num).savefig(png, format="png", dpi=110, bbox_inches="tight")
        outs.append({"output_type": "display_data", "metadata": {},
                     "data": {"image/png": base64.b64encode(png.getvalue()).decode("ascii"),
                              "text/plain": ["<Figure>"]}})
    plt.close("all")
    return outs


def ejecutar(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))
    previo = os.getcwd()
    os.chdir(path.parent)
    sys.path.insert(0, str(path.parent))
    for m in [m for m in sys.modules if m == "comun"]:
        del sys.modules[m]
    ns, k = {"__name__": "__main__"}, 0
    try:
        for cell in nb["cells"]:
            if cell["cell_type"] != "code":
                continue
            k += 1
            outs = ejecutar_celda("".join(cell["source"]), ns)
            for o in outs:
                if o["output_type"] == "execute_result":
                    o["execution_count"] = k
            cell["outputs"], cell["execution_count"] = outs, k
    finally:
        os.chdir(previo)
        sys.path.remove(str(path.parent))
    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"✓ {path.name} · {k} celdas")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        ejecutar(Path(p).resolve())
