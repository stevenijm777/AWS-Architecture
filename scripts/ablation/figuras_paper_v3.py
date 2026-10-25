#!/usr/bin/env python3
"""
figuras_paper_v3.py — Las dos figuras nuevas del paper (revisión de octubre de 2026).

  fig_permisivo_por_modelo   reglas del protocolo permisivo apiladas, por modelo (brazo A)
  fig_v9_cuatro_condiciones  F1 de aristas de Flash con el prompt de producción y con V9

Lee reports/permisivo_semana/permisivo_semana.json y los run.json de prompt_v9; no llama a
ningún modelo. Mismo estilo que fig5_permisivo_3reglas (estricto azul, regla i verde,
regla ii naranja, regla iii violeta).

    python scripts/ablation/figuras_paper_v3.py
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent
REP = ROOT / "reports"
OUT = ROOT / "SOA_Proyecto_entregado" / "imgs"
COL = ["#2a78d6", "#1baf7a", "#eb6834", "#7e5bd6"]
NIVELES = ["estricto", "regla i · agrupar actores", "regla ii · sin duplicados", "regla iii · sin dirección"]

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#52514e", "axes.grid": True, "grid.color": "#ececea", "axes.axisbelow": True,
    "xtick.color": "#52514e", "ytick.color": "#52514e", "legend.frameon": False, "savefig.dpi": 300,
})


def guardar(fig, nombre):
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{nombre}.{ext}", bbox_inches="tight")


def fig_permisivo():
    d = json.loads((REP / "permisivo_semana" / "permisivo_semana.json").read_text(encoding="utf-8"))
    modelos = {r["modelo"]: r["videos"] for r in d["corridas"]
               if r["condicion"] == "Brazo A" and r["prompt"] == "V6" and r["corrida"] == 1}
    orden = ["Flash", "Pro", "Claude"]
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.4), sharey=True)
    for a, pref, titulo in ((ax[0], "svc", "F1 de servicios"), (ax[1], "edge", "F1 de aristas")):
        for x, m in enumerate(orden):
            v = [100 * st.mean(r[f"{pref}_{i}"] for r in modelos[m].values()) for i in range(4)]
            if pref == "edge":
                # El estricto es el que guardó el evaluador, para que coincida con las tablas del paper.
                v[0] = 100 * st.mean(r["strict_eval"] for r in modelos[m].values())
            base = 0.0
            for i in range(4):
                h = v[i] - (v[i - 1] if i else 0.0)
                if h <= 0.05:
                    continue
                a.bar(x, h, bottom=base, width=0.6, color=COL[i], edgecolor="white", linewidth=1.2,
                      label=NIVELES[i] if x == 0 else None)
                if i == 0:
                    a.text(x, h / 2, f"{h:.1f}", ha="center", va="center", color="white", fontweight="bold", fontsize=9)
                base += h
            a.text(x, base + 1.5, f"{base:.1f}", ha="center", va="bottom", fontweight="bold", fontsize=9.5)
        a.set_xticks(range(3), orden)
        a.set_ylim(0, 108)
        a.set_title(titulo, fontsize=10.5)
        a.grid(axis="x", visible=False)
    ax[0].set_ylabel("F1 (%)")
    h, l = ax[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=2, fontsize=8.5, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    guardar(fig, "fig_permisivo_por_modelo")


def fig_v9():
    def media(p):
        R = json.loads((p / "run.json").read_text(encoding="utf-8"))["results"]
        return 100 * st.mean(r["edge_f1"] for r in R)
    A, P, V = REP / "ablation", REP / "pro_vs_flash", REP / "prompt_v9"
    cond = [
        ("Ground truth\n(brazo B)", A / "2026-08-28_0315_STAGE2_V6_CORRECTED_cell9_p30_oracle-oracle_gt", V / "flash_oracle-gt"),
        ("Ground truth,\nsin imagen ni audio", P / "flash_gemini-3.6-flash_oracle-gt_solo-wm", V / "flash_oracle-gt_solo-wm"),
        ("Transcripción\nhumana (brazo A)", P / "flash_gemini-3.6-flash_stage1-manual", V / "flash_stage1-manual"),
        ("Etapa 1\nautomática", P / "flash_gemini-3.6-flash", V / "flash_produccion"),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    for x, (nombre, v6, v9) in enumerate(cond):
        for dx, p, alfa, lab in ((-0.19, v6, 0.45, "prompt de producción"), (0.19, v9, 1.0, "prompt V9")):
            y = media(p)
            ax.bar(x + dx, y, width=0.36, color=COL[0], alpha=alfa, edgecolor="white", linewidth=1.2,
                   label=lab if x == 0 else None)
            ax.text(x + dx, y + 1.5, f"{y:.1f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax.set_xticks(range(len(cond)), [c[0] for c in cond], fontsize=8.5)
    ax.set_ylim(0, 112)
    ax.set_ylabel("F1 de aristas (%)")
    ax.legend(loc="upper right", ncol=2, fontsize=8.5)
    ax.grid(axis="x", visible=False)
    fig.tight_layout()
    guardar(fig, "fig_v9_cuatro_condiciones")


if __name__ == "__main__":
    fig_permisivo()
    fig_v9()
    print("✓ figuras en", OUT.relative_to(ROOT))


def fig_asimetria():
    """F1 de servicios frente a F1 de aristas por arquitectura, solo Standard (n = 321)."""
    import csv
    R = [r for r in csv.DictReader(open(REP / "runs" / "2026-08-20_standard_v6corrected_370v" / "results.csv", encoding="utf-8"))
         if r["scored_for_edges"] == "True" and r["graph_usable"] == "True" and not r["exclusion_reason"]]
    x = [float(r["svc_f1"]) for r in R]
    y = [float(r["edge_f1"]) for r in R]
    fig, ax = plt.subplots(figsize=(3.6, 3.4))
    ax.plot([0, 100], [0, 100], color="#898781", linewidth=1, linestyle=(0, (4, 3)))
    ax.scatter(x, y, s=14, color=COL[0], alpha=0.55, edgecolor="none")
    ax.set_xlim(0, 102)
    ax.set_ylim(0, 102)
    ax.set_aspect("equal")
    ax.set_xlabel("F1 de servicios (%)")
    ax.set_ylabel("F1 de aristas (%)")
    debajo = sum(b < a for a, b in zip(x, y))
    ax.text(4, 94, f"{debajo} de {len(R)} bajo la diagonal", fontsize=8.5, color="#52514e")
    fig.tight_layout()
    guardar(fig, "fig_asimetria_standard")


fig_asimetria()
