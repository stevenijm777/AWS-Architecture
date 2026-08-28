#!/usr/bin/env python3
"""
build_report_html.py — Render the ablation report from the consolidated JSON.

Reads `reports/ablation_report_data.json` (see build_report_data.py) and writes a
self-contained `reports/ablation_report.html`: the per-variant table on the 30-video
panel, the 14 / 16 / 30 split, the ranking comparison against the original panel,
the edge-volume diagnostics, per-video detail, and the written findings.

Usage
-----
    .venv/bin/python scripts/ablation/build_report_html.py
"""
from __future__ import annotations

import html
import json
import statistics
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA = PROJECT_ROOT / "reports" / "ablation_report_data.json"
OUT = PROJECT_ROOT / "reports" / "ablation_report.html"

# Sequential blue ramp, light->dark (validated default palette). Magnitude encoding
# only: these bars mean "how big", never "which one".
RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95"]


def e(x):
    return html.escape(str(x))


def bar(value, lo, hi, width=64):
    """Inline magnitude bar. Scaled to the observed range, which is narrow here —
    the whole point of the report is that these variants barely differ."""
    if value is None:
        return ""
    frac = max(0.0, min(1.0, (value - lo) / (hi - lo))) if hi > lo else 0.5
    step = RAMP[min(len(RAMP) - 1, int(frac * len(RAMP)))]
    return (f'<span class="bar" style="--w:{frac*width:.1f}px;--c:{step}" '
            f'aria-hidden="true"></span>')


def main() -> None:
    if not DATA.exists():
        print("Falta el JSON. Corré build_report_data.py primero."); sys.exit(1)
    d = json.loads(DATA.read_text(encoding="utf-8"))
    perm_path = PROJECT_ROOT / "reports" / "permissive_panel.json"
    perm = json.loads(perm_path.read_text(encoding="utf-8")) if perm_path.exists() else None

    v30 = [v for v in d["variants"] if v["panel"] == 30]
    v14 = {(v["sha"], v["connection_evidence"]): v for v in d["variants"] if v["panel"] == 14}
    v30.sort(key=lambda v: -v["edge_f1"])

    e_lo = min(v["edge_f1"] for v in v30)
    e_hi = max(v["edge_f1"] for v in v30)
    s_lo = min(v["svc_f1"] for v in v30)
    s_hi = max(v["svc_f1"] for v in v30)

    def label(v):
        n = v["name"] + (" + evidencia visual" if v["connection_evidence"] else "")
        c = f"celda {v['cell']}" if v["cell"] else "derivado"
        return n, c

    # ── main table ──────────────────────────────────────────────────────
    main_rows = []
    for v in v30:
        n, c = label(v)
        sp = v["split"]["p30"]
        ratio = sp["gen_edges"] / sp["gt_edges"]
        tag = ' <span class="pill">producción</span>' if v["is_production"] else ""
        main_rows.append(f"""<tr>
<td class="name">{e(n)}{tag}<span class="sub">{e(c)} · <code>{e(v['sha'])}</code></span></td>
<td class="num">{bar(v['svc_f1'], s_lo, s_hi)}{v['svc_f1']:.2f}</td>
<td class="num strong">{bar(v['edge_f1'], e_lo, e_hi)}{v['edge_f1']:.2f}</td>
<td class="num">{sp['gen_edges']}</td>
<td class="num">{ratio:.2f}</td>
<td class="num">{sp['pct_bidirectional']:.1f}%</td>
<td class="num">{sp['user_actors']}</td>
</tr>""")

    g30 = d["gt"]["p30"]
    main_rows.append(f"""<tr class="gt">
<td class="name">GROUND TRUTH<span class="sub">referencia, 30 videos</span></td>
<td class="num">—</td><td class="num">—</td>
<td class="num">{g30['edges']}</td><td class="num">1.00</td>
<td class="num">{g30['pct_bidirectional']:.1f}%</td>
<td class="num">{g30['user_actors']}</td></tr>""")

    # ── 14 / 16 / 30 split ──────────────────────────────────────────────
    split_rows = []
    for v in v30:
        n, c = label(v)
        s = v["split"]
        split_rows.append(f"""<tr>
<td class="name">{e(n)}<span class="sub">{e(c)}</span></td>
<td class="num">{s['p14']['svc_f1']:.2f}</td><td class="num">{s['p14']['edge_f1']:.2f}</td>
<td class="num sep">{s['p16']['svc_f1']:.2f}</td><td class="num">{s['p16']['edge_f1']:.2f}</td>
<td class="num sep strong">{s['p30']['svc_f1']:.2f}</td><td class="num strong">{s['p30']['edge_f1']:.2f}</td>
<td class="num delta">{s['p16']['edge_f1'] - s['p14']['edge_f1']:+.2f}</td>
</tr>""")

    # ── ranking comparison, standalone 14-run vs 30-run ─────────────────
    paired = []
    for v in v30:
        k = (v["sha"], v["connection_evidence"])
        if k in v14:
            paired.append((v, v14[k]))
    by14 = sorted(paired, key=lambda p: -p[1]["edge_f1"])
    by30 = sorted(paired, key=lambda p: -p[0]["edge_f1"])
    r14 = {id(p[0]): i + 1 for i, p in enumerate(by14)}
    r30 = {id(p[0]): i + 1 for i, p in enumerate(by30)}

    rank_rows = []
    for a, b in by14:
        n, c = label(a)
        delta = a["edge_f1"] - b["edge_f1"]
        move = r14[id(a)] - r30[id(a)]
        arrow = "→" if move == 0 else ("↑" if move > 0 else "↓")
        cls = "up" if move > 0 else ("down" if move < 0 else "")
        rank_rows.append(f"""<tr>
<td class="name">{e(n)}<span class="sub">{e(c)}</span></td>
<td class="num">{b['edge_f1']:.2f}</td><td class="num rk">#{r14[id(a)]}</td>
<td class="num sep">{a['edge_f1']:.2f}</td><td class="num rk">#{r30[id(a)]}</td>
<td class="num delta">{delta:+.2f}</td>
<td class="num {cls}">{arrow} {abs(move) if move else ''}</td>
</tr>""")

    # Spearman on *averaged* ranks: two pairs of variants tie exactly on the 14-video
    # panel (64.11 and 63.89), and breaking those ties by sort order silently changes
    # the coefficient. Pearson-on-ranks is the tie-correct form.
    def avg_ranks(vals):
        order = sorted(range(len(vals)), key=lambda i: -vals[i])
        out = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            for k in range(i, j + 1):
                out[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return out

    def pearson(x, y):
        mx, my = statistics.mean(x), statistics.mean(y)
        num = sum((p - mx) * (q - my) for p, q in zip(x, y))
        den = (sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y)) ** 0.5
        return num / den if den else float("nan")

    e14 = [b["edge_f1"] for _, b in paired]
    e30 = [a["edge_f1"] for a, _ in paired]
    n = len(paired)
    rho = pearson(avg_ranks(e14), avg_ranks(e30)) if n > 2 else float("nan")
    # Negative: the better a variant scored on the small panel, the more it lost.
    corr = pearson(e14, [x - y for x, y in zip(e30, e14)]) if n > 2 else float("nan")

    # ── video panels ────────────────────────────────────────────────────
    def vid_rows(items, cls):
        return "".join(
            f'<tr class="{cls}"><td><code>{e(v["video_id"])}</code></td>'
            f'<td class="vname">{e(v["name"])}</td>'
            f'<td class="num">{v["gt_nodes"]}</td><td class="num">{v["gt_edges"]}</td></tr>'
            for v in items)

    # ── per-video detail, production vs best ────────────────────────────
    prod = next((v for v in v30 if v["is_production"]), v30[0])
    best = v30[0]
    pv = {r["video_id"]: r for r in prod["videos"]}
    bv = {r["video_id"]: r for r in best["videos"]}
    order = [x["video_id"] for x in d["panel14"]] + [x["video_id"] for x in d["panel16"]]
    detail_rows = []
    for i, vid in enumerate(order):
        a, b = pv.get(vid), bv.get(vid)
        if not a or not b:
            continue
        grp = "p14" if i < 14 else "p16"
        diff = b["edge_f1"] - a["edge_f1"]
        cls = "up" if diff > 0.05 else ("down" if diff < -0.05 else "tie")
        detail_rows.append(f"""<tr class="{grp}">
<td><code>{e(vid)}</code><span class="sub">{'panel 14' if grp=='p14' else 'nuevo'}</span></td>
<td class="num">{a['gt_nodes']}/{a['gt_edges']}</td>
<td class="num">{a['svc_f1']:.0f}</td><td class="num">{a['edge_f1']:.0f}</td>
<td class="num">{a['gen_edges']}</td>
<td class="num sep">{b['svc_f1']:.0f}</td><td class="num">{b['edge_f1']:.0f}</td>
<td class="num">{b['gen_edges']}</td>
<td class="num {cls}">{diff:+.0f}</td></tr>""")

    perm_section = ""
    if perm:
        pv = sorted(perm["variants"], key=lambda v: -v["perm_edge_f1"])
        prows = "".join(
            f'<tr><td class="name">{e(v["name"])}'
            + (' <span class="pill">producción</span>' if v["is_production"] else "")
            + f'<span class="sub">celda {e(v["cell"])}</span></td>'
              f'<td class="num">{v["strict_edge_f1"]:.2f}</td>'
              f'<td class="num sep">{v["perm_node_f1"]:.2f}</td>'
              f'<td class="num strong">{v["perm_edge_f1"]:.2f}</td>'
              f'<td class="num delta">+{v["perm_edge_f1"] - v["strict_edge_f1"]:.2f}</td></tr>'
            for v in pv)
        n_pairs = len(perm["pairwise"])
        sig_s = sum(1 for x in perm["pairwise"] if x["estricto"]["p"] < 0.05)
        sig_p = sum(1 for x in perm["pairwise"] if x["permisivo"]["p"] < 0.05)
        bonf = 0.05 / n_pairs
        surv = sum(1 for x in perm["pairwise"]
                   if min(x["estricto"]["p"], x["permisivo"]["p"]) < bonf)
        ties_s = sum(x["estricto"]["tie"] for x in perm["pairwise"]) / n_pairs
        ties_p = sum(x["permisivo"]["tie"] for x in perm["pairwise"]) / n_pairs
        perm_section = f"""<h2>6. Evaluación permisiva — ¿aparecen diferencias?</h2>
<p class="note">La permisiva relaja <b>tres cosas a la vez</b>, no solo los actores:
(1) colapsa <code>User*</code>→<code>User</code> y <code>ThirdParty*</code>→<code>ThirdParty</code>;
(2) usa <b>conjuntos</b> en vez de multiconjuntos, o sea ignora servicios duplicados;
(3) usa aristas <b>no dirigidas</b>. Cuesta cero llamadas: el <code>analysis</code> completo
está guardado en cada <code>run.json</code>.</p>
<div class="scroll"><table>
<thead><tr><th>Variante</th><th class="num">Edge estricto</th>
<th class="num sep">Node permisivo</th><th class="num">Edge permisivo</th>
<th class="num">Ganancia</th></tr></thead>
<tbody>{prows}</tbody></table></div>

<h3>Aporte aislado de cada relajación (promedio de las 11)</h3>
<div class="scroll"><table>
<thead><tr><th>Métrica</th><th class="num">Edge F1</th><th class="num">Sobre estricto</th></tr></thead>
<tbody>
<tr><td class="name">Estricta</td><td class="num">58.36</td><td class="num">—</td></tr>
<tr><td class="name">+ solo actores</td><td class="num">62.00</td><td class="num delta">+3.65</td></tr>
<tr><td class="name">+ solo no dirigido</td><td class="num">60.21</td><td class="num delta">+1.86</td></tr>
<tr><td class="name">+ solo conjunto</td><td class="num">61.65</td><td class="num delta">+3.30</td></tr>
<tr><td class="name"><b>Permisiva sin la regla 2</b><span class="sub">actores + no dirigido</span></td>
<td class="num strong">63.88</td><td class="num delta">+5.52</td></tr>
<tr><td class="name">Permisiva completa</td><td class="num">76.67</td><td class="num delta">+18.31</td></tr>
</tbody></table></div>
<p class="note">Las tres por separado suman +8.81; juntas dan +18.31 — la interacción es
<b>super-aditiva</b>, porque achicar los conjuntos por tres vías a la vez hace mucho más fácil
emparejar. Y <b>la regla 2 sola aporta +12.79 de los +18.31</b>, más que las otras dos juntas.</p>

<div class="find warn"><b>La regla de conjuntos borra una capacidad que el prompt implementa</b>
<p>El prompt tiene una regla dedicada a esto: <em>«Dynamic Logical Fusion: …if they perform
distinct architectural steps, KEEP THEM SEPARATE as distinct nodes»</em>. Colapsar a conjunto
da el mismo puntaje al modelo que acierta la multiplicidad y al que la ignora.</p>
<p>Ejemplo real del panel — <code>-wLEkq21cvA</code>, una migración on-prem: el GT tiene
<code>EC2 ×3</code>, <code>ThirdParty ×3</code> y la arista <code>ThirdParty → EC2</code>
<b>tres veces</b>. Con multiconjunto son 3 aristas y encontrar 1 da recall 1/3; con conjunto
colapsan a una y ese mismo modelo obtiene crédito completo. En el GT de los 30 videos,
<b>47 de 361 aristas (13.0%)</b> repiten un par ya conectado y <b>40 de 262 nodos (15.3%)</b>
son instancias repetidas.</p>
<p><b>Recomendación:</b> reportar la permisiva <b>sin la regla 2</b> (63.88) como métrica
secundaria y la completa solo como cota superior declarada. Las otras dos relajaciones sí tienen
defensa: distinguir <code>UserConsumerWeb</code> de <code>UserConsumerMobile</code> a menudo no
es determinable visualmente, y la dirección de una flecha en pizarra es genuinamente ambigua.</p></div>

<h3>¿Discrimina mejor? No — discrimina peor</h3>
<div class="stats">
  <div class="stat"><div class="k">Significativas, estricta</div><div class="v">{sig_s} / {n_pairs}</div>
    <div class="d">esperadas por azar: {n_pairs*0.05:.1f}</div></div>
  <div class="stat"><div class="k">Significativas, permisiva</div><div class="v">{sig_p} / {n_pairs}</div>
    <div class="d">esperadas por azar: {n_pairs*0.05:.1f}</div></div>
  <div class="stat"><div class="k">Sobreviven Bonferroni</div><div class="v">{surv}</div>
    <div class="d">α = 0.05/{n_pairs} = {bonf:.5f}</div></div>
  <div class="stat"><div class="k">Empates promedio</div><div class="v">{ties_s:.1f} → {ties_p:.1f}</div>
    <div class="d">de 30, estricta → permisiva</div></div>
</div>
<div class="find neg"><b>El conteo de significativas es el que predice el azar</b>
<p>Con {n_pairs} comparaciones a α=0.05 se esperan {n_pairs*0.05:.1f} falsos positivos; salieron
{sig_s} y {sig_p}. Con Bonferroni no sobrevive ninguna. <b>Cero pares son significativos en ambas
métricas</b> — una diferencia real sobreviviría al cambio de métrica. Y los empates
<em>suben</em> de {ties_s:.1f} a {ties_p:.1f} de 30: quitar tres fuentes de variación vuelve a las
variantes más parecidas, no menos.</p></div>

<div class="find"><b>Un tercer ordenamiento</b>
<p>ρ = +0.618 entre el ranking estricto y el permisivo. <code>V6_OPTIMIZED</code> pasa de 2º a 1º,
<code>V7_RETURN_FLOWS_V6</code> de 1º a 3º, <code>V5_STRICT_ROUTING c7</code> de 8º a último.
Sumado al cambio entre paneles, ya son <b>tres rankings distintos</b> de las mismas variantes
según muestra y métrica — ninguno estable.</p></div>"""

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")

    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ablación de prompts — reporte</title>
<style>
:root {{
  color-scheme: light dark;
  --surface: #fcfcfb; --panel: #fff; --line: #e4e3df;
  --ink: #0b0b0b; --ink2: #52514e; --ink3: #86857f;
  --good: #1a7f37; --bad: #cf222e; --warn: #9a6700; --accent: #2a78d6;
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) {{
    --surface: #1a1a19; --panel: #212120; --line: #34342f;
    --ink: #fff; --ink2: #c3c2b7; --ink3: #8b8a80;
    --good: #3fb950; --bad: #f85149; --warn: #d29922; --accent: #3987e5;
  }}
}}
:root[data-theme="dark"] {{
  --surface: #1a1a19; --panel: #212120; --line: #34342f;
  --ink: #fff; --ink2: #c3c2b7; --ink3: #8b8a80;
  --good: #3fb950; --bad: #f85149; --warn: #d29922; --accent: #3987e5;
}}
* {{ box-sizing: border-box; }}
body {{ margin:0; padding:2.2rem 1.6rem 5rem; background:var(--surface); color:var(--ink);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,sans-serif;
  max-width:1180px; margin-inline:auto; }}
h1 {{ font-size:1.65rem; margin:0 0 .3rem; letter-spacing:-.01em; }}
h2 {{ font-size:1.15rem; margin:2.8rem 0 .5rem; padding-top:1.4rem; border-top:1px solid var(--line); }}
h3 {{ font-size:.95rem; margin:1.6rem 0 .5rem; color:var(--ink2); }}
.lede {{ color:var(--ink2); max-width:74ch; margin:.2rem 0 1.4rem; }}
.meta {{ color:var(--ink3); font-size:.82rem; margin-bottom:2rem; }}
.note {{ color:var(--ink2); font-size:.89rem; max-width:78ch; margin:.6rem 0 1rem; }}
.scroll {{ overflow-x:auto; border:1px solid var(--line); border-radius:10px; background:var(--panel); }}
table {{ border-collapse:collapse; width:100%; font-size:.87rem; }}
th {{ text-align:left; font-weight:600; font-size:.72rem; text-transform:uppercase;
  letter-spacing:.05em; color:var(--ink3); padding:.7rem .7rem .5rem; white-space:nowrap;
  border-bottom:1px solid var(--line); position:sticky; top:0; background:var(--panel); }}
td {{ padding:.5rem .7rem; border-bottom:1px solid var(--line); vertical-align:top; }}
tr:last-child td {{ border-bottom:0; }}
.num {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
.strong {{ font-weight:650; }}
.sep {{ border-left:1px solid var(--line); }}
.name {{ font-weight:550; min-width:15rem; }}
.sub {{ display:block; font-weight:400; font-size:.74rem; color:var(--ink3); margin-top:.1rem; }}
code {{ font:12px ui-monospace,SFMono-Regular,Menlo,monospace; color:var(--ink2); }}
.bar {{ display:inline-block; width:var(--w); height:8px; background:var(--c);
  border-radius:2px; margin-right:.45rem; vertical-align:baseline; }}
.pill {{ display:inline-block; font-size:.66rem; text-transform:uppercase; letter-spacing:.05em;
  background:var(--accent); color:#fff; border-radius:999px; padding:.05rem .45rem;
  margin-left:.4rem; vertical-align:middle; }}
.gt td {{ background:color-mix(in srgb, var(--accent) 7%, transparent); font-weight:600; }}
.up {{ color:var(--good); }} .down {{ color:var(--bad); }} .tie {{ color:var(--ink3); }}
.rk {{ color:var(--ink3); font-size:.8rem; }}
.delta {{ color:var(--ink2); }}
.stats {{ display:flex; gap:1.6rem; flex-wrap:wrap; margin:1.1rem 0 .4rem; }}
.stat {{ border:1px solid var(--line); border-radius:10px; padding:.8rem 1.1rem;
  background:var(--panel); min-width:12rem; }}
.stat .v {{ font-size:1.5rem; font-weight:650; font-variant-numeric:tabular-nums; }}
.stat .k {{ font-size:.74rem; text-transform:uppercase; letter-spacing:.05em; color:var(--ink3); }}
.stat .d {{ font-size:.8rem; color:var(--ink2); margin-top:.3rem; }}
.find {{ border:1px solid var(--line); border-left:3px solid var(--accent); border-radius:8px;
  background:var(--panel); padding:.9rem 1.1rem; margin:.9rem 0; }}
.find.neg {{ border-left-color:var(--bad); }}
.find.pos {{ border-left-color:var(--good); }}
.find.warn {{ border-left-color:var(--warn); }}
.find b {{ display:block; margin-bottom:.25rem; }}
.find p {{ margin:.35rem 0; color:var(--ink2); font-size:.9rem; }}
details {{ margin:.8rem 0; }}
summary {{ cursor:pointer; font-size:.88rem; color:var(--accent); padding:.3rem 0; }}
.p16 td:first-child {{ border-left:2px solid var(--warn); }}
footer {{ margin-top:3rem; padding-top:1.2rem; border-top:1px solid var(--line);
  color:var(--ink3); font-size:.8rem; }}
</style></head><body>

<h1>Ablación de prompts — Stage 2</h1>
<p class="lede">Cada variante corrida sobre el mismo panel de videos, con
<code>gemini-3.6-flash</code> a temperatura 0, el mismo World Model de Stage 1 cacheado
y el mismo evaluador. Cada prompt se carga desde <code>src/configs/prompts/</code> y se
verifica por SHA-256 antes de la primera llamada.</p>
<p class="meta">Generado {ts} · {len(v30)} variantes sobre 30 videos · datos en
<code>reports/ablation_report_data.json</code></p>

<div class="stats">
  <div class="stat"><div class="k">Rango Edge F1</div><div class="v">{e_hi - e_lo:.2f}</div>
    <div class="d">puntos entre la mejor y la peor de {len(v30)}</div></div>
  <div class="stat"><div class="k">Spearman @14 vs @30</div><div class="v">{rho:+.3f}</div>
    <div class="d">el orden del panel chico no predice el grande</div></div>
  <div class="stat"><div class="k">Correlación puntaje↔caída</div><div class="v">{corr:+.3f}</div>
    <div class="d">cuanto mejor puntuaba a 14, más cayó a 30</div></div>
  <div class="stat"><div class="k">Bidireccionalidad</div><div class="v">{g30['pct_bidirectional']:.0f}%</div>
    <div class="d">en el GT; el mejor modelo llega a {max(v['split']['p30']['pct_bidirectional'] for v in v30):.0f}%</div></div>
</div>

<h2>1. Rendimiento por variante — panel de 30</h2>
<p class="note">Todo lo que sigue se mide <b>por servicio</b>, no por identificador de nodo —
es la convención del evaluador (<code>evaluate_graphs.py</code>: <em>ID-agnostic, we compare by
service names</em>), así que estas cifras son directamente comparables con el Edge F1.
<b>Aristas</b> es el total generado contra las {g30['edges']} del ground truth;
<b>ratio</b> es esa proporción. Todas las variantes <em>sub-generan</em> aristas — ninguna
llega a 1.00. <b>%bidir</b> es la fracción de pares conectados que tienen arista en ambos
sentidos, y <b>actores</b> cuenta los nodos <code>User*</code>, que el GT sí incluye.</p>
<div class="scroll"><table>
<thead><tr><th>Variante</th><th class="num">Service F1</th><th class="num">Edge F1</th>
<th class="num">Aristas</th><th class="num">Ratio</th><th class="num">%bidir</th>
<th class="num">Actores</th></tr></thead>
<tbody>{''.join(main_rows)}</tbody></table></div>

<h2>2. Desglose 14 / 16 / 30</h2>
<p class="note">Los 14 originales son el panel con el que se eligió el prompt de producción.
Los 16 nuevos se muestrearon al azar (<code>seed=42</code>) del conjunto elegible dentro del
mismo rango de complejidad, y <b>nunca se usaron para elegir nada</b> — son la partición
limpia. La última columna es cuánto cae el Edge F1 entre unos y otros.</p>
<div class="scroll"><table>
<thead><tr><th rowspan="2">Variante</th><th class="num" colspan="2">14 originales</th>
<th class="num sep" colspan="2">16 nuevos</th><th class="num sep" colspan="2">30 combinados</th>
<th class="num" rowspan="2">Δ Edge<br>16 − 14</th></tr>
<tr><th class="num">Svc</th><th class="num">Edge</th><th class="num sep">Svc</th><th class="num">Edge</th>
<th class="num sep">Svc</th><th class="num">Edge</th></tr></thead>
<tbody>{''.join(split_rows)}</tbody></table></div>

<h2>3. El ranking no sobrevive a la ampliación</h2>
<p class="note">Compara la corrida independiente sobre los 14 contra la corrida sobre los 30.
Son llamadas distintas a la API, así que parte de la diferencia es ruido de corrida a corrida
— pero el <em>reordenamiento</em> no lo es.</p>
<div class="scroll"><table>
<thead><tr><th>Variante</th><th class="num">Edge @14</th><th class="num">Puesto</th>
<th class="num sep">Edge @30</th><th class="num">Puesto</th><th class="num">Δ</th>
<th class="num">Movimiento</th></tr></thead>
<tbody>{''.join(rank_rows)}</tbody></table></div>
<p class="note"><b>Spearman ρ = {rho:+.3f}</b> entre ambos ordenamientos (rangos promediados,
porque hay dos pares de empates exactos en el panel de 14): el orden del panel chico
<b>no predice</b> el del grande. Y <b>r = {corr:+.3f}</b> entre el Edge F1 a 14 y la variación al
pasar a 30 — negativo significa que <b>cuanto mejor puntuaba una variante en el panel chico,
más perdió al ampliar</b>. Es la firma cuantificada del sobreajuste a la muestra de
selección.</p>

<h2>4. Los videos</h2>
<details><summary>Ver los 30 videos con su ground truth</summary>
<div class="scroll" style="margin-top:.6rem"><table>
<thead><tr><th>Video</th><th>Arquitectura (GT)</th><th class="num">Nodos</th><th class="num">Aristas</th></tr></thead>
<tbody>{vid_rows(d['panel14'], 'p14')}{vid_rows(d['panel16'], 'p16')}</tbody></table></div>
<p class="note">Los marcados con barra ámbar son los 16 nuevos. GT de los 14:
{d['gt']['p14']['nodes']} nodos y {d['gt']['p14']['edges']} aristas · GT de los 16:
{d['gt']['p16']['nodes']} nodos y {d['gt']['p16']['edges']} aristas.</p>
</details>

<h2>5. Detalle por video — producción contra la mejor</h2>
<p class="note">Columnas izquierda: <b>{e(label(prod)[0])}</b> ({e(label(prod)[1])}).
Derecha: <b>{e(label(best)[0])}</b> ({e(label(best)[1])}). La última columna es la diferencia
de Edge F1; gris significa empate exacto, que es el caso más frecuente.</p>
<details><summary>Ver comparación video por video</summary>
<div class="scroll" style="margin-top:.6rem"><table>
<thead><tr><th>Video</th><th class="num">GT n/a</th>
<th class="num">Svc</th><th class="num">Edge</th><th class="num">Arist.</th>
<th class="num sep">Svc</th><th class="num">Edge</th><th class="num">Arist.</th>
<th class="num">Δ Edge</th></tr></thead>
<tbody>{''.join(detail_rows)}</tbody></table></div>
</details>

{perm_section}

<h2>7. Hallazgos</h2>

<div class="find warn"><b>El panel de 14 estaba sobreajustado</b>
<p>Las {len(v30)} variantes caben en <b>{e_hi - e_lo:.2f} puntos</b> de Edge F1. En el panel de
14 las diferencias parecían mayores y ordenaban un ranking; a 30 ese orden se desarma
(ρ = {rho:+.3f}) y la pérdida es proporcional a lo bien que le había ido a cada una
(r = {corr:+.3f}).</p></div>

<div class="find neg"><b>Ninguna diferencia entre variantes es estadísticamente significativa</b>
<p>Test de signos pareado por video: p entre 0.118 y 1.000 en todas las comparaciones, con
<b>12 a 19 empates de 30</b> según el par. En 9 de los 30 videos las cuatro variantes
principales dan Edge F1 <em>idéntico</em>. Los prompts se diferencian mucho menos de lo que
sugieren sus promedios.</p></div>

<div class="find neg"><b>Cuatro intervenciones independientes, ningún efecto</b>
<p>Reescrituras de reglas, few-shot RAG con arquitecturas de ejemplo, inyección de la
topología detectada por visión por computadora, y corrección de reglas dirigida por análisis
del error. Cada una mejor fundamentada que la anterior; ninguna movió el Edge F1.
<b>Conclusión defendible: el Edge F1 de ~59% no está limitado por el prompt de Stage 2.</b></p></div>

<div class="find"><b>El volumen de aristas es la métrica que más informa</b>
<p>Todas las variantes sub-generan: ratio entre
{min(v['split']['p30']['gen_edges']/v['split']['p30']['gt_edges'] for v in v30):.2f} y
{max(v['split']['p30']['gen_edges']/v['split']['p30']['gt_edges'] for v in v30):.2f} contra el GT.
De las 178 aristas que pierde producción: <b>80 (45%)</b> son aristas de retorno que el modelo
no emitió (puso <code>b→a</code> pero no <code>a→b</code>), <b>58 (33%)</b> son por un nodo
ausente —y el 91% de esos son actores <code>User*</code> o <code>ThirdParty</code>—, y
<b>40 (22%)</b> son pares sin conexión en ningún sentido.</p></div>

<div class="find warn"><b>Dos reglas del propio prompt causan el 75% de la pérdida</b>
<p><code>Unidirectional Default</code> explica las 80 aristas de retorno.
<code>Pruning: Remove generic human actors</code> explica los actores ausentes — y
<b>contradice el propio vocabulario</b> del prompt, que ofrece una lista
<code>User and Client Actors</code>. El GT tiene {g30['user_actors']} actores <code>User*</code>
en estos 30 videos.</p></div>

<div class="find neg"><b>Pero arreglarlas no mejoró el resultado</b>
<p>V8 corrigió ambas reglas. Los mecanismos respondieron —actores de 20 a 29, bidireccionalidad
de 12.4% a 17.9%, 30 aristas más— y el Edge F1 no se movió (p = 0.607), mientras el Service F1
se degradó de forma significativa (p = 0.039). <b>La contabilidad de errores no es un mapa de
mejoras disponibles</b>: saber que falta una arista de retorno no es saber entre qué dos
servicios va.</p></div>

<div class="find pos"><b>La brecha de bidireccionalidad sigue abierta</b>
<p>El GT tiene <b>{g30['pct_bidirectional']:.1f}%</b> de pares conectados en ambos sentidos.
La mejor variante llega a
{max(v['split']['p30']['pct_bidirectional'] for v in v30):.1f}% y producción a
{next(v['split']['p30']['pct_bidirectional'] for v in v30 if v['is_production']):.1f}%.
Es la diferencia estructural más grande entre lo generado y la referencia, y ninguna
intervención la cerró.</p></div>

<div class="find"><b>Reutilizar scores de producción para ampliar un panel es válido</b>
<p>El primer panel de 30 se armó de forma híbrida (14 de la ablación + 16 tomados del CSV de la
corrida de 370 videos, sin pagar llamadas). Dio 87.23 / 59.10 contra 88.07 / 58.99 de la corrida
limpia de punta a punta: <b>0.11 puntos de diferencia en Edge F1</b>. Abarata cualquier
ampliación futura.</p></div>

<footer>Prompts verificados por SHA-256 contra <code>src/configs/prompts/MANIFEST.json</code>.
Corridas individuales en <code>reports/ablation/</code>, cada una con su <code>run.json</code>
(hash del prompt, modelo, commit, procedencia de Stage 1 y de la pizarra por video).
Regenerar: <code>build_report_data.py</code> y luego <code>build_report_html.py</code>.</footer>
</body></html>"""

    OUT.write_text(doc, encoding="utf-8")
    print(f"✓ {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
