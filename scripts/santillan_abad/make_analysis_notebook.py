#!/usr/bin/env python3
"""
make_analysis_notebook.py — Genera la copia local ejecutable del notebook de Santillán y Abad.

El paquete de reproducibilidad de los autores está hecho para Google Colab y, corrido
tal cual, **sobrescribe sus propios archivos de entrada** (las celdas 2, 6, 8 y 26
regeneran los pickles y el CSV de metadata). Esos archivos son nuestro oráculo: son la
única evidencia independiente de que reproducimos sus cifras publicadas. Así que el
original no se toca nunca y todo pasa en una copia.

Qué hace este script
--------------------
Lee `hpc_n_edge_clouds_archs.ipynb` y escribe dos variantes: `_local` (396) y `_extended` (457)
al lado, con cuatro cambios y ninguno más:

1. **Celda de preparación al principio.** Fija las rutas absolutas y hace `chdir` a un
   directorio de salida propio (`run_local/`, `run_extended/`), de modo que toda escritura relativa
   del notebook caiga ahí y el paquete original quede intacto.
2. **Rutas de Colab.** `/content/` desaparece; el directorio de graphml apunta a
   nuestro `data/cloudscape_gt/`, que ya verificamos idéntico al de Cloudscape
   (396/396 en servicios y en metadata).
3. **Se quitan las líneas de shell** (`!git clone`, `!pip install`): el entorno se
   arma afuera, con versiones fijas.
4. **La celda 40 se reemplaza.** La original consulta la API de YouTube con una clave
   hardcodeada en el repositorio público de los autores. No se usa —no es nuestra
   credencial— y además ataría la corrida a la red. El año sale de los `info.json`
   que ya tenemos en disco, y la celda contrasta ese año contra el CSV que ellos
   publicaron: si coinciden, es una verificación extra regalada.

Las salidas guardadas se limpian en la copia, para que lo que se vea después de
ejecutar sea inequívocamente de esta corrida y no residuo de la de ellos.

Uso
---
    .venv/bin/python scripts/santillan_abad/make_analysis_notebook.py
"""
from __future__ import annotations

import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
PKG = find_pkg()
ORIG = PKG / "hpc_n_edge_clouds_archs.ipynb"

RAW_DIR = PROJECT / "data" / "raw"

# Las dos variantes. La base reproduce el paper publicado; la extendida es la
# actualización, con las 61 arquitecturas que Cloudscape no tiene. El único cambio
# entre las dos es el directorio de graphml que leen — nada más, para que cualquier
# diferencia en los resultados sea atribuible al corpus y no al código.
VARIANTES = {
    "local": dict(
        graphml=PROJECT / "data" / "cloudscape_gt",
        salida="run_local",
        nota="396 arquitecturas de Cloudscape — reproduce el paper publicado",
    ),
    "extended": dict(
        graphml=PROJECT / "data" / "cloudscape_extended",
        salida="run_extended",
        nota="457 arquitecturas — Cloudscape + las 61 nuevas de nuestro pipeline",
    ),
    # Par para medir propagación de error: mismas 385 arquitecturas, una vez con
    # anotación humana y otra con extracción automática. Cualquier diferencia entre
    # estas dos corridas es error del pipeline, no del corpus.
    "gt385": dict(
        graphml=PROJECT / "data" / "cloudscape_gt385",
        salida="run_gt385",
        nota="385 arquitecturas con anotación humana (referencia del par)",
    ),
    "extracted385": dict(
        graphml=PROJECT / "data" / "cloudscape_extracted385",
        salida="run_extracted385",
        nota="las MISMAS 385, extraídas por nuestro pipeline",
    ),
}

def celda_setup(graphml: Path, salida: str, nota: str) -> str:
    return f'''# === Celda agregada para la corrida local (no está en el original) ===
# {nota}
#
# El notebook de los autores escribe sobre sus propios archivos de entrada. Acá se
# redirige todo a un directorio aparte para que el paquete original quede intacto:
# esos archivos son la única referencia independiente contra la cual comparar.
import os, shutil
from pathlib import Path

from _paths import find_pkg  # noqa: E402

GT_DIR = r"{graphml}"         # directorio de graphml que alimenta todo el análisis
RAW_DIR = Path(r"{RAW_DIR}")  # metadatos de YouTube ya descargados
DATA = Path(r"{PKG}")         # paquete original — sólo lectura
OUT = DATA / "{salida}"       # todo lo que se escriba cae acá

OUT.mkdir(exist_ok=True)
# único insumo que el notebook no regenera por su cuenta
for f in ("diccionario_traducido.csv",):
    if (DATA / f).exists():
        shutil.copy(DATA / f, OUT / f)

os.chdir(OUT)
print("directorio de trabajo:", os.getcwd())
print("graphml desde       :", GT_DIR)
'''

CELDA_40 = '''# === Celda reemplazada (la original está en el notebook de los autores) ===
# El original consulta la API de YouTube con una clave hardcodeada en el repositorio
# público de los autores. No se usa: no es nuestra credencial, y ataría el resultado
# a la red. El año de publicación sale de los metadatos que ya tenemos en disco.
import json, re
import pandas as pd

def anio_local(link):
    m = re.search(r"v=([\\w\\-]+)", str(link))
    if not m:
        return None
    p = RAW_DIR / f"{m.group(1)}.info.json"
    if not p.exists():
        return None
    up = str(json.load(open(p)).get("upload_date") or "")
    return int(up[:4]) if up[:4].isdigit() else None

df = pd.read_csv("arquitecturas_clasificadas_con_metadata.csv")
df["anio_local"] = df["link"].apply(anio_local)

# Verificación: ¿nuestro año coincide con el que ellos sacaron por API?
ref = pd.read_csv(DATA / "arquitecturas_con_anio.csv")[["architecture", "anio_video"]]
df = df.merge(ref, on="architecture", how="left")
ambos = df["anio_local"].notna() & df["anio_video"].notna()
iguales = int((df.loc[ambos, "anio_local"] == df.loc[ambos, "anio_video"]).sum())
print(f"GATE año: {iguales}/{int(ambos.sum())} coinciden donde tenemos metadato local")
disc = df[ambos & (df["anio_local"] != df["anio_video"])]
if len(disc):
    print(disc[["architecture", "anio_local", "anio_video"]].head(15).to_string(index=False))

# Para las 396 de Cloudscape el año de referencia es el de los autores: es su dato y
# es el oráculo contra el cual se compara. Las arquitecturas nuevas no están en su CSV,
# así que ahí manda el metadato local — sin este fillna quedarían sin año y se caerían
# de todo el análisis por año.
df["anio_video"] = df["anio_video"].fillna(df["anio_local"])
sin_publicado = int(df["anio_video"].notna().sum() - ambos.sum())
print(f"  año tomado del metadato local (no están en el CSV de ellos): {sin_publicado}")
sin_anio = int(df["anio_video"].isna().sum())
if sin_anio:
    print(f"  SIN AÑO: {sin_anio}")
df = df.drop(columns=["anio_local"])
df.to_csv("arquitecturas_con_anio.csv", index=False)
'''


def parchear(src: str, graphml: Path) -> str:
    """Aplica los tres cambios mecánicos a una celda de código."""
    # 1. fuera las líneas de shell de Colab
    lineas = [l for l in src.splitlines(keepends=True)
              if not l.lstrip().startswith("!")]
    out = "".join(lineas)
    # 2. rutas de Colab -> relativas (caen en OUT por el chdir de la celda de setup)
    out = out.replace("/content/", "")
    # 3. el directorio de graphml -> el del corpus que toca a esta variante
    out = out.replace('"Cloudscape/data/graphs"', f'r"{graphml}"')
    out = out.replace("'Cloudscape/data/graphs'", f"r'{graphml}'")
    return out


def construir(nombre: str, graphml: Path, salida: str, nota: str) -> None:
    if not graphml.exists():
        raise SystemExit(f"no existe {graphml} — ¿corriste build_extended_corpus.py?")
    nb = json.loads(ORIG.read_text(encoding="utf-8"))
    celdas = nb["cells"]

    # índice de la celda de la API de YouTube, localizada por contenido y no por
    # número, para que el script no se rompa si el notebook cambia de orden
    idx_api = [i for i, c in enumerate(celdas)
               if c["cell_type"] == "code" and "googleapis.com/youtube" in "".join(c["source"])]
    if len(idx_api) != 1:
        raise SystemExit(f"esperaba una sola celda con la API de YouTube, encontré {idx_api}")
    idx_api = idx_api[0]

    tocadas = {"shell": 0, "content": 0, "graphml": 0}
    for i, c in enumerate(celdas):
        if c["cell_type"] != "code":
            continue
        c["outputs"] = []          # la copia se ejecuta limpia
        c["execution_count"] = None
        if i == idx_api:
            c["source"] = CELDA_40.splitlines(keepends=True)
            continue
        antes = "".join(c["source"])
        despues = parchear(antes, graphml)
        if any(l.lstrip().startswith("!") for l in antes.splitlines()):
            tocadas["shell"] += 1
        if "/content/" in antes:
            tocadas["content"] += 1
        if "Cloudscape/data/graphs" in antes:
            tocadas["graphml"] += 1
        c["source"] = despues.splitlines(keepends=True)

    celdas.insert(0, {
        "cell_type": "code", "execution_count": None, "metadata": {},
        "outputs": [],
        "source": celda_setup(graphml, salida, nota).splitlines(keepends=True),
    })

    destino = PKG / f"hpc_n_edge_clouds_archs_{nombre}.ipynb"
    destino.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
    n = len(list(graphml.glob("*.graphml")))
    print(f"✓ {destino.name}  —  {n} arquitecturas, salida en {salida}/")
    print(f"    celdas {len(celdas)} (1 agregada) · API reemplazada en la {idx_api} · "
          f"parcheadas: shell {tocadas['shell']}, /content {tocadas['content']}, "
          f"graphml {tocadas['graphml']}")


def main() -> None:
    for nombre, cfg in VARIANTES.items():
        construir(nombre, cfg["graphml"], cfg["salida"], cfg["nota"])


if __name__ == "__main__":
    main()
