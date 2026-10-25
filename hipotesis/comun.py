"""
comun.py — Carga, estadística y figuras compartidas por los notebooks de hipotesis/.

Solo lee `run.json` ya escritos en reports/ y el ground truth de data/cloudscape_gt/;
no llama a ningún modelo. Depende de numpy, matplotlib y Pillow, nada más, para que
corra con el mismo kernel que los notebooks de notebooks/.

Las aristas se comparan igual que el evaluador (`scripts/utils/evaluate_graphs.py`):
multiconjunto de pares (servicio origen, servicio destino). `verificar()` comprueba que
el F1 recalculado aquí coincide con el que guardó el evaluador en cada corrida.
"""
from __future__ import annotations

import json
import math
import os
import random
import xml.etree.ElementTree as ET
from collections import Counter
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# El módulo funciona en los dos repositorios. En el de trabajo (AWS-Architecture) vive en
# hipotesis/ y los resultados están en reports/; en el oficial (aws-architecture-extraction)
# vive en notebooks/hipotesis/ y los resultados están en results/.
_AQUI = Path(__file__).resolve().parent
OFICIAL = (_AQUI.parent.parent / "results").exists() and _AQUI.parent.name == "notebooks"
ROOT = _AQUI.parent.parent if OFICIAL else _AQUI.parent
REP = ROOT / ("results" if OFICIAL else "reports")
# El ground truth no se redistribuye en el repositorio oficial: se baja con
# data/fetch_cloudscape.sh, o se apunta CLOUDSCAPE_GT a una copia local.
GT_DIR = Path(os.environ.get("CLOUDSCAPE_GT", ROOT / "data" / "cloudscape_gt"))
# Las pizarras tampoco se redistribuyen; sin ellas, las figuras de ejemplo muestran un aviso.
PIZARRAS = ROOT / "data" / "good_whiteboard"
FIG = _AQUI / "figuras"


def _claude(nombre_lab: str, nombre_oficial: str) -> Path:
    # Las carpetas de Claude conservan el mismo nombre en los dos repositorios.
    return REP / nombre_lab


# ── Corridas ─────────────────────────────────────────────────────────
# Clave = <condición>_<modelo>[_rep2]. Condiciones:
#   A    Stage 1 manual (transcripción humana de la pizarra) + pizarra + transcript
#   B    ground truth convertido a World Model + pizarra + transcript
#   Bwm  ground truth convertido a World Model, sin pizarra ni transcript
_ABL, _PVF = REP / "ablation", REP / "pro_vs_flash"
RUNS = {
    "A_flash":       _PVF / "flash_gemini-3.6-flash_stage1-manual",
    "A_flash_rep2":  _ABL / "2026-08-29_0725_STAGE2_V6_CORRECTED_cell9_p30_oracle-vision",
    "A_pro":         _PVF / "pro_gemini-3.1-pro-preview_stage1-manual",
    "A_claude":      _claude("claude", "stage1-manual"),
    "A_argon":       _PVF / "argon_gemini-4-argon_stage1-manual",
    "B_flash":       _ABL / "2026-08-28_0315_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt",
    "B_flash_rep2":  _ABL / "2026-08-28_2211_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt_rep2",
    "B_pro":         _PVF / "pro_gemini-3.1-pro-preview_oracle-gt",
    "B_pro_rep2":    _PVF / "pro_gemini-3.1-pro-preview_oracle-gt_rep2",
    "B_claude":      _claude("claude_oracle_gt", "oracle-gt"),
    "Bwm_flash":     _PVF / "flash_gemini-3.6-flash_oracle-gt_solo-wm",
    "Bwm_pro":       _PVF / "pro_gemini-3.1-pro-preview_oracle-gt_solo-wm",
    "Bwm_pro_rep2":  _PVF / "pro_gemini-3.1-pro-preview_oracle-gt_solo-wm_rep2",
    # P = producción (Stage 1 automático cacheado). El sufijo 9 en la condición es el prompt
    # stage2_v9_connection_ledger.txt; sin sufijo, el de producción (V6).
    "P_flash":       _PVF / "flash_gemini-3.6-flash",
    "P9_flash":      REP / "prompt_v9" / "flash_produccion",
    "A9_flash":      REP / "prompt_v9" / "flash_stage1-manual",
    "B9_flash":      REP / "prompt_v9" / "flash_oracle-gt",
    "Bwm9_flash":    REP / "prompt_v9" / "flash_oracle-gt_solo-wm",
    "P9_flash_rep2": REP / "prompt_v9" / "flash_produccion_rep2",
    "P_pro":         _PVF / "pro_gemini-3.1-pro-preview",
    "P9_pro":        REP / "prompt_v9" / "pro_produccion",
    "P9_claude":     _claude("claude_produccion_v9", "produccion_v9"),
    "P9_argon":      REP / "prompt_v9" / "argon_produccion",
    "A9_flash_rep2": REP / "prompt_v9" / "flash_stage1-manual_rep2",
    "B9_pro":        REP / "prompt_v9" / "pro_oracle-gt",
    "B9_claude":     _claude("claude_oracle_gt_v9", "oracle-gt_v9"),
    "B9_flash_rep2": REP / "prompt_v9" / "flash_oracle-gt_rep2",
    "B9_pro_rep2":   REP / "prompt_v9" / "pro_oracle-gt_rep2",
    "B9_claude_rep2": _claude("claude_oracle_gt_v9_rep2", "oracle-gt_v9_rep2"),
    # Bu = brazo B con el prompt de producción menos la regla "Unidirectional Default".
    "Bu_flash":      REP / "prompt_v9" / "flash_oracle-gt_v6-sin-unidireccional",
}

# El color sigue al modelo en todos los notebooks, nunca a la posición en la figura.
COLOR = {"flash": "#2a78d6", "pro": "#eb6834", "claude": "#1baf7a"}
NOMBRE = {"flash": "Gemini 3.6 Flash", "pro": "Gemini 3.1 Pro", "claude": "Claude Opus 5.5"}
TINTA, TINTA2, TENUE, REJILLA, FONDO = "#0b0b0b", "#52514e", "#898781", "#e6e5e1", "#fcfcfb"
FALTA, SOBRA, NEUTRO = "#d03b3b", "#4a3aa7", "#b9b8b2"   # arista perdida / inventada / referencia

TIPOS = ["ida y vuelta", "par repetido", "servicio con varios nodos", "con actor User*",
         "auto-arista", "simple"]


def modelo(clave: str) -> str:
    return clave.split("_")[1]


def etiqueta(clave: str) -> str:
    return NOMBRE[modelo(clave)] + (" · réplica 2" if clave.endswith("rep2") else "")


@lru_cache(maxsize=None)
def cargar(clave: str) -> dict:
    run = json.loads((RUNS[clave] / "run.json").read_text(encoding="utf-8"))
    run["_by_id"] = {r["video_id"]: r for r in run["results"] if r.get("status") == "success"}
    return run


def existe(clave: str) -> bool:
    return (RUNS[clave] / "run.json").exists()


def filas(clave: str) -> dict:
    return cargar(clave)["_by_id"]


def ruta(clave: str) -> str:
    return RUNS[clave].relative_to(ROOT).as_posix()


# ── Ground truth y aristas ───────────────────────────────────────────
@lru_cache(maxsize=None)
def gt(vid: str) -> tuple[dict, Counter]:
    """(servicio por nodo, multiconjunto de pares de servicio) del graphml de Cloudscape."""
    ns = {"g": "http://graphml.graphdrawing.org/xmlns"}
    root = ET.parse(GT_DIR / f"{vid}.graphml").getroot()
    key = next(k.get("id") for k in root.findall("g:key", ns)
               if k.get("for") == "node" and k.get("attr.name") == "service")
    svc = {}
    for n in root.iter("{%s}node" % ns["g"]):
        d = next((x.text for x in n.findall("g:data", ns) if x.get("key") == key), None)
        svc[n.get("id")] = d or "?"
    edges = Counter((svc[e.get("source")], svc[e.get("target")])
                    for e in root.iter("{%s}edge" % ns["g"]))
    return svc, edges


def gen(fila: dict) -> Counter:
    svc = {n["id"]: n["service"] for n in fila["analysis"]["nodes"]}
    return Counter((svc.get(e["source"], "?"), svc.get(e["target"], "?"))
                   for e in fila["analysis"]["edges"])


def tipo_arista(vid: str, a: str, b: str) -> str:
    """Clase excluyente de una arista del ground truth, en este orden de prioridad."""
    svc, edges = gt(vid)
    n_nodos = Counter(svc.values())
    if a == b:
        return "auto-arista"
    if edges[(a, b)] > 1:
        return "par repetido"
    if n_nodos[a] > 1 or n_nodos[b] > 1:
        return "servicio con varios nodos"
    if edges[(b, a)] > 0:
        return "ida y vuelta"
    if a.startswith("User") or b.startswith("User"):
        return "con actor User*"
    return "simple"


def verificar(claves) -> tuple[int, int]:
    """(filas revisadas, filas donde el F1 recalculado aquí difiere del que guardó el evaluador)."""
    n = distintas = 0
    for k in claves:
        for vid, f in filas(k).items():
            g, e = gt(vid)[1], gen(f)
            inter = sum((g & e).values())
            f1 = 2 * inter / (sum(g.values()) + sum(e.values())) if g and e else 0.0
            n += 1
            distintas += abs(f1 - f["edge_f1"]) > 1e-6
    return n, distintas


# ── Resúmenes y estadística ──────────────────────────────────────────
def resumen(clave: str) -> dict:
    R = list(filas(clave).values())
    n = len(R)
    falta = sobra = tp = 0
    for f in R:
        g, e = gt(f["video_id"])[1], gen(f)
        falta += sum((g - e).values())
        sobra += sum((e - g).values())
        tp += sum((g & e).values())
    tot_gen = sum(f["gen_edges"] for f in R)
    tot_gt = sum(f["gt_edges"] for f in R)
    return {
        "n": n,
        "svc": 100 * sum(f["svc_f1"] for f in R) / n,
        "edge": 100 * sum(f["edge_f1"] for f in R) / n,
        "aristas": tot_gen / n, "aristas_gt": tot_gt / n,
        "faltan": falta, "sobran": sobra,
        "precision": 100 * tp / tot_gen, "recall": 100 * tp / tot_gt,
        "inventados": sum(len(f.get("services_hallucinated") or []) for f in R),
        "perfectos": sum(f["edge_f1"] > 0.999 for f in R),
    }


def pareado(a: str, b: str, metrica: str = "edge_f1", n_boot: int = 20_000) -> dict:
    """Diferencia pareada B − A por video: media, IC 95 % por bootstrap y prueba de signos."""
    A, B = filas(a), filas(b)
    ids = [v for v in A if v in B]
    return {"a": a, "b": b, **diferencias({v: 100 * (B[v][metrica] - A[v][metrica]) for v in ids}, n_boot)}


def diferencias(por_video: dict, n_boot: int = 20_000) -> dict:
    """Media, IC 95 % por bootstrap y prueba de signos de un conjunto de diferencias por video."""
    ids, d = list(por_video), list(por_video.values())
    rng = random.Random(0)
    medias = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(n_boot))
    gana = sum(x > 1e-9 for x in d)
    pierde = sum(x < -1e-9 for x in d)
    m = gana + pierde
    p = min(1.0, 2 * sum(math.comb(m, i) for i in range(min(gana, pierde) + 1)) / 2 ** m) if m else 1.0
    return {"n": len(d), "dif": sum(d) / len(d),
            "lo": medias[int(0.025 * n_boot)], "hi": medias[int(0.975 * n_boot) - 1],
            "gana": gana, "pierde": pierde, "empata": len(d) - m, "p": p, "d": dict(zip(ids, d))}


class Tabla:
    """Tabla mínima que se ve bien en Jupyter y también como texto."""

    def __init__(self, columnas, filas_):
        self.columnas, self.filas = columnas, filas_

    def _repr_html_(self) -> str:
        th = "".join(f"<th style='text-align:{'left' if i == 0 else 'right'}'>{c}</th>"
                     for i, c in enumerate(self.columnas))
        trs = "".join("<tr>" + "".join(
            f"<td style='text-align:{'left' if i == 0 else 'right'}'>{v}</td>" for i, v in enumerate(r))
            + "</tr>" for r in self.filas)
        return f"<table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>"

    def __repr__(self) -> str:
        w = [max(len(str(x)) for x in col) for col in zip(self.columnas, *self.filas)]
        fmt = lambda r: "  ".join(str(v).ljust(w[i]) if i == 0 else str(v).rjust(w[i]) for i, v in enumerate(r))
        return "\n".join([fmt(self.columnas), "  ".join("-" * x for x in w)] + [fmt(r) for r in self.filas])


def tabla_resumen(claves) -> Tabla:
    cols = ["corrida", "F1 servicios", "F1 aristas", "aristas / GT", "faltan", "sobran",
            "precisión", "recall", "servicios inventados", "videos perfectos", "carpeta"]
    out = []
    for k in claves:
        r = resumen(k)
        out.append([etiqueta(k), f"{r['svc']:.2f}", f"{r['edge']:.2f}",
                    f"{r['aristas']:.2f} / {r['aristas_gt']:.2f}", r["faltan"], r["sobran"],
                    f"{r['precision']:.1f}", f"{r['recall']:.1f}", r["inventados"], r["perfectos"],
                    f"<code>{ruta(k)}</code>"])
    return Tabla(cols, out)


def tabla_pareada(pares, metrica: str = "edge_f1") -> Tabla:
    cols = ["comparación (B − A)", "Δ", "IC 95 %", "gana / pierde / empata", "p (signos)"]
    out = []
    for a, b in pares:
        s = pareado(a, b, metrica)
        out.append([f"{etiqueta(b)} − {etiqueta(a)}", f"{s['dif']:+.2f}",
                    f"[{s['lo']:+.2f}, {s['hi']:+.2f}]",
                    f"{s['gana']} / {s['pierde']} / {s['empata']}", f"{s['p']:.3f}"])
    return Tabla(cols, out)


# ── Figuras ──────────────────────────────────────────────────────────
def estilo() -> None:
    plt.rcParams.update({
        "figure.facecolor": FONDO, "axes.facecolor": FONDO, "savefig.facecolor": FONDO,
        "font.family": "DejaVu Sans", "font.size": 10.5,
        "text.color": TINTA, "axes.labelcolor": TINTA2, "axes.edgecolor": REJILLA,
        "xtick.color": TENUE, "ytick.color": TENUE, "xtick.labelcolor": TINTA2, "ytick.labelcolor": TINTA2,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": REJILLA, "grid.linewidth": 0.8, "axes.axisbelow": True,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "figure.dpi": 110, "savefig.dpi": 160, "legend.frameon": False,
    })


def guardar(fig, nombre: str) -> None:
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f"{nombre}.png", bbox_inches="tight")


def barras(ax, claves, campo: str, titulo: str, ymax: float = 100, ref: dict | None = None) -> None:
    """Una barra por corrida, con el valor escrito encima y el color del modelo."""
    vals = [resumen(k)[campo] for k in claves]
    x = np.arange(len(claves))
    for xi, k, v in zip(x, claves, vals):
        ax.bar(xi, v, width=0.62, color=COLOR[modelo(k)], alpha=0.55 if k.endswith("rep2") else 1.0,
               edgecolor=FONDO, linewidth=2)
        ax.text(xi, v + ymax * 0.015, str(v) if isinstance(v, int) else f"{v:.1f}", ha="center", va="bottom", fontweight="bold", color=TINTA)
    for texto, y in (ref or {}).items():
        ax.axhline(y, color=TENUE, linewidth=1, linestyle=(0, (4, 3)))
        ax.text(len(claves) - 0.45, y, f" {texto}", va="center", ha="left", color=TINTA2, fontsize=9)
    # Nombre corto: con cinco barras el nombre completo se pisa con el de al lado.
    ax.set_xticks(x, [modelo(k).capitalize() + ("\nréplica 2" if k.endswith("rep2") else "")
                      for k in claves])
    ax.set_ylim(0, ymax * 1.08)
    ax.set_title(titulo)
    ax.grid(axis="x", visible=False)


def bosque(ax, pares, metrica: str = "edge_f1", titulo: str = "", banda: float | None = None,
           banda_txt: str = "ruido entre réplicas") -> None:
    """Diferencias pareadas con su IC 95 %. Un intervalo que cruza el cero no es efecto."""
    if banda:
        ax.axvspan(-banda, banda, color=NEUTRO, alpha=0.28, linewidth=0)
        ax.text(0, len(pares) - 0.42, f"{banda_txt} ±{banda:.1f}", ha="center", va="bottom",
                color=TINTA2, fontsize=9)
    ax.axvline(0, color=TINTA2, linewidth=1)
    for i, (a, b) in enumerate(pares):
        s = pareado(a, b, metrica)
        y = len(pares) - 1 - i
        c = COLOR[modelo(b)]
        ax.plot([s["lo"], s["hi"]], [y, y], color=c, linewidth=2.2, solid_capstyle="round")
        ax.plot(s["dif"], y, "o", color=c, markersize=9, markeredgecolor=FONDO, markeredgewidth=2)
        ax.text(s["hi"], y + 0.2, f"  {s['dif']:+.1f}  [{s['lo']:+.1f}, {s['hi']:+.1f}]", va="bottom",
                ha="left", color=TINTA, fontsize=9.5)
    ax.set_yticks(range(len(pares)),
                  [f"{etiqueta(b)}\n− {etiqueta(a)}" for a, b in reversed(pares)])
    ax.set_ylim(-0.6, len(pares) - 0.1)
    ax.margins(x=0.25)
    ax.set_xlabel("diferencia pareada por video (puntos de F1)")
    ax.set_title(titulo)
    ax.grid(axis="y", visible=False)


def dispersion(ax, a: str, b: str, metrica: str = "edge_f1") -> None:
    """Un punto por video. Sobre la diagonal gana el modelo del eje vertical."""
    A, B = filas(a), filas(b)
    ids = [v for v in A if v in B]
    x = [100 * A[v][metrica] for v in ids]
    y = [100 * B[v][metrica] for v in ids]
    ax.plot([0, 100], [0, 100], color=TENUE, linewidth=1, linestyle=(0, (4, 3)))
    ax.scatter(x, y, s=70, color=COLOR[modelo(b)], edgecolor=FONDO, linewidth=2, alpha=0.9, zorder=3)
    ax.set_xlim(0, 104)
    ax.set_ylim(0, 104)
    ax.set_aspect("equal")
    ax.set_xlabel(etiqueta(a))
    ax.set_ylabel(etiqueta(b))
    arriba = sum(yy > xx + 1e-9 for xx, yy in zip(x, y))
    abajo = sum(yy < xx - 1e-9 for xx, yy in zip(x, y))
    ax.set_title(f"{arriba} arriba · {abajo} abajo · {len(ids) - arriba - abajo} iguales")


def pendientes(ax, a: str, b: str, nombres=("con pizarra\ny transcript", "solo\nWorld Model"),
               metrica: str = "edge_f1") -> None:
    """Una línea por video entre dos condiciones del mismo modelo, y la media encima."""
    A, B = filas(a), filas(b)
    ids = [v for v in A if v in B]
    c = COLOR[modelo(b)]
    for v in ids:
        ya, yb = 100 * A[v][metrica], 100 * B[v][metrica]
        ax.plot([0, 1], [ya, yb], color=c if yb >= ya else TENUE, linewidth=1.1, alpha=0.45)
    ma = sum(100 * A[v][metrica] for v in ids) / len(ids)
    mb = sum(100 * B[v][metrica] for v in ids) / len(ids)
    ax.plot([0, 1], [ma, mb], color=TINTA, linewidth=2.6, marker="o", markersize=9,
            markeredgecolor=FONDO, markeredgewidth=2, zorder=5)
    ax.text(-0.04, ma, f"{ma:.1f}", ha="right", va="center", fontweight="bold")
    ax.text(1.04, mb, f"{mb:.1f}", ha="left", va="center", fontweight="bold")
    ax.set_xticks([0, 1], nombres)
    ax.set_xlim(-0.3, 1.3)
    ax.set_ylim(0, 104)
    ax.set_title(f"{etiqueta(b)}: {mb - ma:+.1f} puntos")
    ax.grid(axis="x", visible=False)


def pizarra(ax, vid: str, titulo: str | None = None) -> None:
    ruta_ = PIZARRAS / f"{vid}.jpg"
    if ruta_.exists():
        ax.imshow(plt.imread(ruta_))
    else:
        ax.text(0.5, 0.5, f"Pizarra no incluida\n(los fotogramas no se redistribuyen;\n"
                f"youtube.com/watch?v={vid})", ha="center", va="center", color=TINTA2, fontsize=10)
    ax.set_axis_off()
    ax.set_title(titulo or f"Pizarra · {vid}")


def _circulo(ax, nodos_ref: set, e_ref: Counter, e_gen: Counter | None, titulo: str,
             que: str = "aristas") -> None:
    """Dibuja un grafo sobre un círculo de servicios y, si hay `e_gen`, lo compara con `e_ref`:
    gris = está en los dos, rojo punteado = solo en la referencia, violeta = solo en el generado."""
    e_dib = e_gen if e_gen is not None else e_ref
    nodos = sorted(set(nodos_ref) | {s for par in e_dib for s in par} | {s for par in e_ref for s in par})
    ang = np.linspace(0, 2 * np.pi, len(nodos), endpoint=False) + np.pi / 2
    pos = {n: (np.cos(a), np.sin(a)) for n, a in zip(nodos, ang)}

    def flecha(par, color, estilo_, ancho, z):
        a, b = par
        if a == b:
            x, y = pos[a]
            ax.add_patch(plt.Circle((x * 1.13, y * 1.13), 0.09, fill=False, color=color,
                                    linewidth=ancho, linestyle=estilo_, zorder=z))
            return
        ax.add_patch(FancyArrowPatch(pos[a], pos[b], connectionstyle="arc3,rad=0.16",
                                     arrowstyle="-|>", mutation_scale=13, shrinkA=13, shrinkB=13,
                                     color=color, linewidth=ancho, linestyle=estilo_, zorder=z))

    for par, n in (e_ref & e_dib).items():
        flecha(par, TINTA2, "-", 1.2 + 0.6 * (n - 1), 2)
    if e_gen is not None:
        for par in (e_ref - e_gen):
            flecha(par, FALTA, (0, (3, 2)), 1.8, 3)
        for par in (e_gen - e_ref):
            flecha(par, SOBRA, "-", 1.8, 3)
    extra = set(nodos) - set(nodos_ref)
    for n, (x, y) in pos.items():
        ax.plot(x, y, "o", markersize=11, color=SOBRA if n in extra else FONDO,
                markeredgecolor=SOBRA if n in extra else TINTA2, markeredgewidth=1.6, zorder=4)
        ax.text(x * 1.2, y * 1.2, n, ha="left" if x > 0.15 else "right" if x < -0.15 else "center",
                va="bottom" if y > 0.15 else "top" if y < -0.15 else "center", fontsize=8.5,
                color=SOBRA if n in extra else TINTA)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal")
    ax.set_axis_off()
    if e_gen is not None:
        inter = sum((e_ref & e_gen).values())
        tot = sum(e_ref.values()) + sum(e_gen.values())
        f1 = 200 * inter / tot if tot else 0.0
        titulo = (f"{titulo}\nF1 {que} {f1:.0f} · faltan {sum((e_ref - e_gen).values())} · "
                  f"sobran {sum((e_gen - e_ref).values())}")
    else:
        titulo = f"{titulo}\n{sum(e_ref.values())} {que}"
    ax.set_title(titulo, fontsize=10.5)


def grafo(ax, vid: str, fila: dict | None = None, titulo: str = "") -> None:
    """El grafo de un video contra el ground truth. Sin `fila` dibuja el ground truth."""
    svc_gt, e_gt = gt(vid)
    _circulo(ax, set(svc_gt.values()), e_gt, gen(fila) if fila else None,
             titulo or ("" if fila else "Ground truth"))


def leyenda_grafo(fig, ref: str = "el ground truth") -> None:
    from matplotlib.lines import Line2D
    h = [Line2D([], [], color=TINTA2, linewidth=1.6, label="coincide"),
         Line2D([], [], color=FALTA, linewidth=1.8, linestyle=(0, (3, 2)), label=f"falta (está en {ref})"),
         Line2D([], [], color=SOBRA, linewidth=1.8, label=f"sobra (no está en {ref})")]
    fig.legend(handles=h, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))


# ── Stage 1: World Models contra la transcripción manual (H6) ─────────
LAB = ROOT / "whiteboard_selection_lab" / "lab_workspace"
S1_DIR = REP / "stage1_vs_manual"


def ruta_wm(vid: str, nombre: str) -> Path:
    """World Model `nombre` de un video. En el repositorio oficial la transcripción manual está
    en data/manual_world_models/ y las lecturas de Stage 1 en data/stage1_world_models/<nombre>/."""
    if not OFICIAL:
        return LAB / vid / f"world_model_{nombre}.json"
    if nombre == "vision":
        return ROOT / "data" / "manual_world_models" / f"{vid}.json"
    return ROOT / "data" / "stage1_world_models" / nombre / f"{vid}.json"


def aristas_gt_sin_nota(vid: str) -> tuple[int, int]:
    """(aristas del ground truth sin nota, total). La conversión del oráculo copia esa nota como
    descripción de la conexión, así que es el número de conexiones que llegan sin explicar."""
    ns = {"g": "http://graphml.graphdrawing.org/xmlns"}
    root = ET.parse(GT_DIR / f"{vid}.graphml").getroot()
    key = next((k.get("id") for k in root.findall("g:key", ns)
                if k.get("for") == "edge" and k.get("attr.name") == "notes"), None)
    edges = list(root.iter("{%s}edge" % ns["g"]))
    vacias = sum(not (next((x.text for x in e.findall("g:data", ns) if x.get("key") == key), None) or "").strip()
                 for e in edges)
    return vacias, len(edges)
# Clave = nombre del archivo world_model_<clave>.json. "vision" es la transcripción humana.
S1 = {
    "vision":       ("Persona", TINTA2, "solo la pizarra"),
    "s1-flash":     ("Flash", COLOR["flash"], "pizarra + transcript"),
    "s1-pro":       ("Pro", COLOR["pro"], "pizarra + transcript"),
    "s1-flash-img": ("Flash", COLOR["flash"], "solo la pizarra"),
    "s1-pro-img":   ("Pro", COLOR["pro"], "solo la pizarra"),
    "s1-claude":     ("Claude", COLOR["claude"], "pizarra + transcript"),
    "s1-claude-img": ("Claude", COLOR["claude"], "solo la pizarra"),
}


def s1_etiqueta(nombre: str, salto: str = "\n") -> str:
    quien, _, entrada = S1[nombre]
    return f"{quien}{salto}{entrada}"


@lru_cache(maxsize=None)
def s1_filas(nombre: str) -> dict:
    """Filas por video de reports/stage1_vs_manual/comparacion.json para un World Model."""
    data = json.loads((S1_DIR / "comparacion.json").read_text(encoding="utf-8"))
    return {r["video_id"]: r for r in data["rows"] if r["world_model"] == nombre}


def s1_media(nombre: str, campo: str) -> float:
    R = s1_filas(nombre).values()
    return sum(r[campo] for r in R) / len(R) * (100 if "f1" in campo or "_p_" in campo or "_r_" in campo else 1)


def s1_pareado(a: str, b: str, campo: str) -> dict:
    A, B = s1_filas(a), s1_filas(b)
    return diferencias({v: 100 * (B[v][campo] - A[v][campo]) for v in A})


@lru_cache(maxsize=None)
def wm_reducido(vid: str, nombre: str) -> tuple[frozenset, Counter]:
    """(servicios, pares de servicio) de un World Model, como en scripts/ablation/stage1_panel.py."""
    wm = json.loads(ruta_wm(vid, nombre).read_text(encoding="utf-8"))
    resolver = {}
    for e in wm.get("entities", []):
        for clave in (e.get("name"), e.get("service")):
            if clave:
                resolver.setdefault(clave.strip().lower(), e["service"])
    pares = Counter()
    for con in wm.get("visual_connections", []):
        s_ = resolver.get((con.get("source_label") or "").strip().lower())
        t_ = resolver.get((con.get("target_label") or "").strip().lower())
        if s_ and t_:
            pares[(s_, t_)] += 1
    return frozenset(e["service"] for e in wm.get("entities", [])), pares


def grafo_wm(ax, vid: str, nombre: str, ref: str = "vision", titulo: str = "") -> None:
    """Un World Model contra otro (por defecto, contra la transcripción manual)."""
    s_ref, e_ref = wm_reducido(vid, ref)
    e_gen = None if nombre == ref else wm_reducido(vid, nombre)[1]
    _circulo(ax, set(s_ref), e_ref, e_gen, titulo or s1_etiqueta(nombre, " · "), que="conexiones")


def s1_barras(ax, nombres, campo: str, titulo: str, ymax: float = 100, ref: dict | None = None) -> None:
    for x, n in enumerate(nombres):
        v = s1_media(n, campo)
        ax.bar(x, v, width=0.62, color=S1[n][1], alpha=0.55 if n.endswith("-img") else 1.0,
               edgecolor=FONDO, linewidth=2)
        ax.text(x, v + ymax * 0.015, f"{v:.1f}", ha="center", va="bottom", fontweight="bold", color=TINTA)
    for texto, y in (ref or {}).items():
        ax.axhline(y, color=TENUE, linewidth=1, linestyle=(0, (4, 3)))
        ax.text(len(nombres) - 0.45, y, f" {texto}", va="center", ha="left", color=TINTA2, fontsize=9)
    ax.set_xticks(range(len(nombres)), [s1_etiqueta(n).replace(" + ", "\n+ ").replace("solo la ", "solo la\n") for n in nombres],
                  fontsize=9)
    ax.set_ylim(0, ymax * 1.08)
    ax.set_title(titulo)
    ax.grid(axis="x", visible=False)


def s1_bosque(ax, comparaciones, titulo: str = "") -> None:
    """comparaciones = [(A, B, campo, texto)]: diferencia pareada B − A con su IC 95 %."""
    ax.axvline(0, color=TINTA2, linewidth=1)
    for i, (a, b, campo, texto) in enumerate(comparaciones):
        s_ = s1_pareado(a, b, campo)
        y = len(comparaciones) - 1 - i
        ax.plot([s_["lo"], s_["hi"]], [y, y], color=S1[b][1], linewidth=2.2, solid_capstyle="round")
        ax.plot(s_["dif"], y, "o", color=S1[b][1], markersize=9, markeredgecolor=FONDO, markeredgewidth=2)
        ax.text(s_["hi"], y + 0.2, f"  {s_['dif']:+.1f}  [{s_['lo']:+.1f}, {s_['hi']:+.1f}]", va="bottom",
                ha="left", color=TINTA, fontsize=9.5)
    ax.set_yticks(range(len(comparaciones)), [t for *_, t in reversed(comparaciones)])
    ax.set_ylim(-0.6, len(comparaciones) - 0.1)
    ax.margins(x=0.25)
    ax.set_xlabel("diferencia pareada por video (puntos de F1)")
    ax.set_title(titulo)
    ax.grid(axis="y", visible=False)


def s1_tabla_pareada(comparaciones) -> Tabla:
    out = []
    for a, b, campo, texto in comparaciones:
        s_ = s1_pareado(a, b, campo)
        out.append([texto.replace("\n", " "), f"{s_['dif']:+.2f}", f"[{s_['lo']:+.2f}, {s_['hi']:+.2f}]",
                    f"{s_['gana']} / {s_['pierde']} / {s_['empata']}", f"{s_['p']:.3f}"])
    return Tabla(["comparación (B − A)", "Δ", "IC 95 %", "gana / pierde / empata", "p (signos)"], out)
