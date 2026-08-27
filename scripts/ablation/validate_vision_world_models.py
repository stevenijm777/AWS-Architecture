#!/usr/bin/env python3
"""
validate_vision_world_models.py — Visual check of the hand-authored World Models.

Why this exists
---------------
`whiteboard_selection_lab/lab_workspace/<vid>/world_model_vision.json` holds 12
World Models written **by hand** on 2026-07-31, transcribing what a human read off
the whiteboard: entities plus the arrows between them. They are the raw material
of the `with_vision` experiment — the oracle condition that asks "if Stage 1 were
perfect, how much better would Stage 2 get?".

Nothing in the repository reads them today, and their fidelity to the whiteboards
has never been checked. Feeding an unvalidated oracle into Stage 2 would produce a
number nobody could defend, so this script does the checking first:

  1. structural consistency (every connection label resolves to an entity, every
     service exists in the catalog);
  2. renders each JSON as a graph image via `graph_renderer/render_graph.mjs`;
  3. builds an HTML putting each rendered graph beside its source whiteboard, so
     the fidelity call is made by looking, not by assuming.

Only after that review should these World Models be handed to Stage 2.

Usage
-----
    .venv/bin/python scripts/ablation/validate_vision_world_models.py
"""
from __future__ import annotations

import base64
import csv
import html
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402

LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
GOOD_WB = PROJECT_ROOT / "data" / "good_whiteboard"
SERVICES_CSV = PROJECT_ROOT / "data" / "cloudscape_gt" / "services.csv"
RENDERER = PROJECT_ROOT / "graph_renderer"
OUT_DIR = PROJECT_ROOT / "reports" / "vision_validation"
WORK = OUT_DIR / "_graphml"


def load_catalog() -> set[str]:
    names = set()
    with open(SERVICES_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = row.get("name", "").strip()
            if n:
                names.add(n)
    return names


def audit(wm: dict, catalog: set[str]) -> dict:
    """Structural problems that would make the rendered graph misleading."""
    ents = wm.get("entities", [])
    conns = wm.get("visual_connections", [])
    names = {e.get("name", "") for e in ents} | {e.get("service", "") for e in ents}

    broken, touched = [], set()
    for c in conns:
        for side in ("source_label", "target_label"):
            lbl = c.get(side, "")
            if lbl in names:
                touched.add(lbl)
            else:
                broken.append(f"{side}={lbl!r}")

    return {
        "n_entities": len(ents),
        "n_connections": len(conns),
        "broken_labels": broken,
        "services_off_catalog": sorted({e.get("service", "") for e in ents
                                        if e.get("service") not in catalog}),
        "orphan_entities": sorted({e.get("name", "") for e in ents
                                   if e.get("name") not in touched
                                   and e.get("service") not in touched}),
    }


def to_cloudscape(wm: dict, vid: str) -> dict:
    """World Model (entities + visual_connections) → Cloudscape analysis shape.

    A World Model records *drawn arrows*, not typed logical flows, so every edge
    is emitted as a single untyped flow. Connections whose label does not resolve
    to an entity are dropped rather than guessed at — they surface in the audit.
    """
    ents = wm.get("entities", [])
    nodes, by_label = [], {}
    for i, e in enumerate(ents):
        nid = str(i)
        nodes.append({
            "id": nid,
            "service": e.get("service", ""),
            "name": e.get("name", "") or e.get("service", ""),
            "notes": e.get("rationale", ""),
        })
        for key in (e.get("name", ""), e.get("service", "")):
            if key:
                by_label.setdefault(key, nid)

    edges = []
    for c in wm.get("visual_connections", []):
        s = by_label.get(c.get("source_label", ""))
        t = by_label.get(c.get("target_label", ""))
        if s is None or t is None:
            continue
        edges.append({
            "source": s, "target": t, "flow_id": 0, "seq": "0",
            "type": "data", "notes": c.get("description", ""),
        })

    return {
        "step_by_step_reasoning": "Hand-authored World Model transcribed from the whiteboard.",
        "graph": {
            "name": f"{vid} — World Model manual",
            "link": f"https://www.youtube.com/watch?v={vid}",
            "categories": "", "graph_usable": True,
            "notes": "Transcripción visual hecha a mano el 2026-07-31.",
        },
        "nodes": nodes,
        "edges": edges,
    }


def b64_img(p: Path) -> str:
    return base64.b64encode(p.read_bytes()).decode("ascii")


def build_html(rows: list[dict]) -> str:
    cards = []
    for r in rows:
        a = r["audit"]
        flags = []
        if a["broken_labels"]:
            flags.append(f'<li class="bad">Conexión sin entidad: {html.escape(", ".join(a["broken_labels"]))}</li>')
        if a["services_off_catalog"]:
            flags.append(f'<li class="bad">Servicio fuera del catálogo: {html.escape(", ".join(a["services_off_catalog"]))}</li>')
        if a["orphan_entities"]:
            flags.append(f'<li class="warn">Sin conexiones: {html.escape(", ".join(a["orphan_entities"]))}</li>')
        if not flags:
            flags.append('<li class="ok">Sin problemas estructurales</li>')

        render = (f'<img src="data:image/png;base64,{r["render_b64"]}" alt="grafo">'
                  if r["render_b64"] else
                  '<div class="missing">No se pudo renderizar</div>')

        cards.append(f"""
<section class="card" data-vid="{html.escape(r['vid'])}">
  <header>
    <h2>{html.escape(r['vid'])}</h2>
    <span class="counts">{a['n_entities']} entidades · {a['n_connections']} conexiones
      · {r['edges_kept']} aristas en el grafo</span>
  </header>
  <div class="pair">
    <figure><figcaption>Pizarra (best frame)</figcaption>
      <img src="data:image/jpeg;base64,{r['wb_b64']}" alt="pizarra"></figure>
    <figure><figcaption>World Model manual, renderizado</figcaption>{render}</figure>
  </div>
  <ul class="flags">{''.join(flags)}</ul>
  <div class="verdict">
    <button data-v="ok">Fiel</button>
    <button data-v="partial">Parcial</button>
    <button data-v="bad">No fiel</button>
    <span class="mark"></span>
  </div>
</section>""")

    return f"""<!doctype html>
<meta charset="utf-8">
<title>Validación de World Models manuales</title>
<style>
:root {{ color-scheme: light dark; --bg:#fff; --fg:#111; --mut:#666; --line:#ddd; --card:#fafafa; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg:#14161a; --fg:#e8e8e8; --mut:#9aa; --line:#2c313a; --card:#1b1e24; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:2rem 1.5rem; background:var(--bg); color:var(--fg);
  font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
h1 {{ font-size:1.5rem; margin:0 0 .3rem; }}
.lede {{ color:var(--mut); max-width:68ch; margin:0 0 1.5rem; }}
.bar {{ position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line);
  padding:.7rem 0; margin-bottom:1.5rem; font-variant-numeric:tabular-nums; z-index:5; }}
.card {{ border:1px solid var(--line); border-radius:10px; background:var(--card);
  padding:1rem 1.2rem 1.2rem; margin-bottom:1.5rem; }}
.card header {{ display:flex; align-items:baseline; gap:.8rem; flex-wrap:wrap; margin-bottom:.8rem; }}
h2 {{ font-size:1.05rem; margin:0; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; }}
.counts {{ color:var(--mut); font-size:.85rem; }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:1rem; }}
@media (max-width:820px) {{ .pair {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; }}
figcaption {{ font-size:.78rem; text-transform:uppercase; letter-spacing:.05em;
  color:var(--mut); margin-bottom:.4rem; }}
figure img {{ width:100%; height:auto; border:1px solid var(--line); border-radius:6px;
  background:#fff; cursor:zoom-in; }}
figure img.zoom {{ position:fixed; inset:2vh; width:96vw; height:96vh; object-fit:contain;
  z-index:50; cursor:zoom-out; background:#fff; box-shadow:0 0 0 100vmax rgba(0,0,0,.8); }}
.missing {{ padding:2rem; text-align:center; color:var(--mut); border:1px dashed var(--line); border-radius:6px; }}
.flags {{ list-style:none; padding:0; margin:.9rem 0 0; font-size:.87rem; }}
.flags li {{ padding:.15rem 0 .15rem .95rem; position:relative; }}
.flags li::before {{ position:absolute; left:0; }}
.ok {{ color:#1a7f37; }} .ok::before {{ content:"✓"; }}
.warn {{ color:#9a6700; }} .warn::before {{ content:"•"; }}
.bad {{ color:#cf222e; }} .bad::before {{ content:"✗"; }}
.verdict {{ margin-top:.9rem; display:flex; gap:.5rem; align-items:center; }}
.verdict button {{ font:inherit; font-size:.85rem; padding:.3rem .8rem; cursor:pointer;
  border:1px solid var(--line); border-radius:999px; background:transparent; color:var(--fg); }}
.verdict button[aria-pressed="true"] {{ background:var(--fg); color:var(--bg); border-color:var(--fg); }}
.mark {{ color:var(--mut); font-size:.85rem; }}
</style>

<h1>Validación de los World Models manuales</h1>
<p class="lede">Los 12 <code>world_model_vision.json</code> se escribieron a mano el
2026-07-31 transcribiendo lo que se veía en cada pizarra. Antes de usarlos como
condición oráculo del experimento <code>with_vision</code>, hay que confirmar que
representan fielmente el dibujo. Compará cada par y marcá el veredicto — se guarda
en el navegador. Clic en una imagen para ampliarla.</p>
<div class="bar" id="bar">—</div>
{''.join(cards)}

<script>
const KEY = 'wm-vision-verdicts';
const store = JSON.parse(localStorage.getItem(KEY) || '{{}}');

function paint() {{
  document.querySelectorAll('.card').forEach(c => {{
    const v = store[c.dataset.vid];
    c.querySelectorAll('.verdict button').forEach(b =>
      b.setAttribute('aria-pressed', String(b.dataset.v === v)));
    c.querySelector('.mark').textContent =
      v ? {{ok:'marcado fiel', partial:'marcado parcial', bad:'marcado no fiel'}}[v] : '';
  }});
  const n = Object.keys(store).length, t = document.querySelectorAll('.card').length;
  const c = v => Object.values(store).filter(x => x === v).length;
  document.getElementById('bar').textContent =
    `${{n}}/${{t}} revisados · ${{c('ok')}} fieles · ${{c('partial')}} parciales · ${{c('bad')}} no fieles`;
}}

document.addEventListener('click', e => {{
  const b = e.target.closest('.verdict button');
  if (b) {{
    const vid = b.closest('.card').dataset.vid;
    store[vid] === b.dataset.v ? delete store[vid] : store[vid] = b.dataset.v;
    localStorage.setItem(KEY, JSON.stringify(store));
    paint();
    return;
  }}
  if (e.target.matches('figure img')) e.target.classList.toggle('zoom');
}});

paint();
</script>
"""


def main() -> None:
    catalog = load_catalog()
    files = sorted(LAB.glob("*/world_model_vision.json"), key=lambda p: p.parent.name)
    if not files:
        print("No hay world_model_vision.json"); sys.exit(1)

    WORK.mkdir(parents=True, exist_ok=True)
    rows, graphmls = [], []

    for f in files:
        vid = f.parent.name
        wm = json.loads(f.read_text(encoding="utf-8"))
        a = audit(wm, catalog)
        analysis = to_cloudscape(wm, vid)

        # `_manual` on purpose: render_graph.mjs stamps a "[Parsimonious]" tag on
        # anything ending in `_vision`, which these are not.
        gml = WORK / f"{vid}_manual.graphml"
        G = create_graph_from_cloudscape_json(analysis, video_id=vid)
        nx.write_graphml(G, str(gml))
        graphmls.append(gml)

        rows.append({"vid": vid, "audit": a, "gml": gml,
                     "edges_kept": G.number_of_edges(), "render_b64": None})
        print(f"{vid:<14} {a['n_entities']:>2} ents · {a['n_connections']:>2} conns "
              f"→ {G.number_of_nodes()} nodos, {G.number_of_edges()} aristas")

    print("\nRenderizando…")
    r = subprocess.run(["node", "render_graph.mjs", *[str(p) for p in graphmls]],
                       cwd=RENDERER, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-2000:]); print(r.stderr[-2000:])
        print("✗ El renderer falló."); sys.exit(1)
    print(r.stdout.strip()[-500:])

    for row in rows:
        png = RENDERER / "graphs_output" / f"{row['vid']}_manual.png"
        row["render_b64"] = b64_img(png) if png.exists() else None
        wb = GOOD_WB / f"{row['vid']}.jpg"
        row["wb_b64"] = b64_img(wb) if wb.exists() else ""

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "index.html"
    out.write_text(build_html(rows), encoding="utf-8")

    (OUT_DIR / "audit.json").write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "whiteboard_selection_lab/lab_workspace/*/world_model_vision.json",
        "note": "World Models escritos a mano el 2026-07-31; material del experimento with_vision.",
        "videos": [{"video_id": r["vid"], "edges_in_graph": r["edges_kept"], **r["audit"]}
                   for r in rows],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    shutil.rmtree(WORK, ignore_errors=True)
    n_ok = sum(1 for r in rows if r["render_b64"])
    print(f"\n✓ {n_ok}/{len(rows)} renderizados → {out.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
