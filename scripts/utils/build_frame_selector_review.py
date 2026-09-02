#!/usr/bin/env python3
"""
build_frame_selector_review.py — Galería local para auditar a ojo el selector de pizarra.

Por cada video en `reports/frame_selector_eval.csv`, pone lado a lado:
  - la imagen APROBADA (la que realmente se usó, de data/good_whiteboard/)
  - la elección del selector AUTOMÁTICO de hoy (de data/frames/)

Ordenado por gravedad: primero los `uso_fallback` (el selector no encontró ni un
candidato válido), después los de 0–1 íconos, después el resto de las discrepancias, y por
último los 213 aciertos (imagen idéntica). Cubre los 440 videos evaluados, para que el
conteo final de "válidos" sea sobre el total, no solo sobre los problemáticos.

Cada imagen queda etiquetada con el número de frame exacto dentro del video
(`frame #04795 de 76`), no solo la miniatura — así se ve explícitamente CUÁL toma se usó
en el dataset, sin tener que inferirlo del nombre de archivo.

Garantía de seguridad
----------------------
**Solo lectura sobre el corpus.** Nunca toca `good_whiteboard/`, `bad_whiteboard/` ni
`frames/<video>_pizarra/`. Toda la salida (miniaturas + HTML) va a
`reports/frame_selector_review/`, una carpeta nueva.

Las imágenes NO se publican ni se suben a ningún lado: es un archivo HTML local, para
abrir en el navegador de esta máquina. Son capturas de video con copyright de terceros.

Uso
---
    .venv/bin/python scripts/utils/build_frame_selector_review.py
    .venv/bin/python scripts/utils/build_frame_selector_review.py --max-por-grupo 40
"""
from __future__ import annotations

import argparse
import csv
import html
import re
from pathlib import Path

from PIL import Image
from rich.console import Console

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CSV_IN = PROJECT_ROOT / "reports" / "frame_selector_eval.csv"
GOOD_WB = PROJECT_ROOT / "data" / "good_whiteboard"
FRAMES = PROJECT_ROOT / "data" / "frames"
OUT_DIR = PROJECT_ROOT / "reports" / "frame_selector_review"
THUMB_W = 480
FRAME_NUM_RE = re.compile(r"_frame_(\d+)\.jpg$")

console = Console()


def frame_label(filename: str) -> str:
    """'<video>_frame_04795.jpg' -> 'frame #4795'. Es lo que identifica, dentro del
    video completo, cuál toma exacta se usó — no solo que "se parece", sino cuál es."""
    if not filename:
        return ""
    m = FRAME_NUM_RE.search(filename)
    return f"frame #{int(m.group(1))}" if m else filename


def thumb(src: Path, dst: Path) -> bool:
    if dst.exists():
        return True
    if not src.exists():
        return False
    try:
        with Image.open(src) as im:
            w, h = im.size
            im.convert("RGB").resize((THUMB_W, int(h * THUMB_W / w))).save(dst, "JPEG", quality=82)
        return True
    except Exception:
        return False


def tarjeta(row: dict, seccion_id: str) -> str:
    vid = row["video_id"]
    aprob_thumb = f"thumbs/{vid}_aprobada.jpg"
    auto_thumb = f"thumbs/{vid}_automatica.jpg"
    ok_a = thumb(GOOD_WB / f"{vid}.jpg", OUT_DIR / aprob_thumb)
    ok_b = thumb(FRAMES / vid / row["frame_automatico"], OUT_DIR / auto_thumb)

    def img(ok: bool, path: str, etiqueta: str) -> str:
        if not ok:
            return f'<div class="ph">(sin imagen)<br>{html.escape(etiqueta)}</div>'
        return (f'<figure><img src="{path}" loading="lazy">'
                f'<figcaption>{html.escape(etiqueta)}</figcaption></figure>')

    total = row["frames_totales"]
    if row["origen_curado"] == "frame_extraido":
        # Es EL frame que se uso, identificado por su numero dentro del video completo.
        etiqueta_a = f"aprobada — {frame_label(row['frame_aprobado'])} de {total} · usada en el estudio"
    else:
        # Un humano la reemplazo por otra toma: no coincide con ningun frame extraido tal cual.
        etiqueta_a = "aprobada — reemplazo manual · usada en el estudio (no es un frame extraído sin editar)"
    etiqueta_b = f"automática (hoy) — {frame_label(row['frame_automatico'])} de {total}"

    meta = (f"origen: {row['origen_curado']} · coincide: {row['coincide']} · "
            f"íconos: {row['num_iconos']} · score: {row['score']} · "
            f"oclusión: {row['oclusion_pct']}% · descartados: {row['descartados']}/{row['candidatos']}"
            + (f" · distancia: {row['distancia_frames']} frames" if row["distancia_frames"] else ""))
    return f"""
    <div class="card{' fallback' if row['uso_fallback'] == 'True' else ''}" data-vid="{html.escape(vid)}" data-seccion="{seccion_id}">
      <h3>{html.escape(vid)}</h3>
      <div class="pair">
        {img(ok_a, aprob_thumb, etiqueta_a)}
        {img(ok_b, auto_thumb, etiqueta_b)}
      </div>
      <p class="meta">{html.escape(meta)}</p>
      <div class="votebar">
        <button class="vote-btn v-si" data-val="si">✓ válida</button>
        <button class="vote-btn v-no" data-val="no">✗ no válida</button>
        <button class="vote-btn v-duda" data-val="duda">? dudosa</button>
      </div>
    </div>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-por-grupo", type=int, default=None,
                     help="limitar cuántas tarjetas generar por grupo (por defecto: todas)")
    ap.add_argument("--calibracion", type=int, default=None,
                     help="limitar cuántos aciertos mostrar (por defecto: los 213 completos)")
    args = ap.parse_args()

    if not CSV_IN.exists():
        console.print(f"[red]✗ Falta {CSV_IN} — corré measure_frame_selector.py primero.[/]")
        raise SystemExit(1)

    rows = list(csv.DictReader(open(CSV_IN, encoding="utf-8")))
    (OUT_DIR / "thumbs").mkdir(parents=True, exist_ok=True)

    # Categorias mutuamente excluyentes, por prioridad: un video cae en la PRIMERA que
    # aplique. Sin esto, un acierto (coincide=True) cuyo frame aprobado tiene 0-1 iconos
    # detectados terminaba contado dos veces (en "pobres" y en "aciertos") — se veian 459
    # tarjetas para 440 videos. Confirmado: 19 videos caian en ese solape.
    fallback, pobres, aciertos, discrepancia = [], [], [], []
    for r in rows:
        if r["uso_fallback"] == "True":
            fallback.append(r)
        elif r["coincide"] == "True":
            aciertos.append(r)
        elif int(r["num_iconos"]) <= 1:
            pobres.append(r)
        else:
            discrepancia.append(r)
    if args.calibracion:
        aciertos = aciertos[:args.calibracion]

    grupos = [
        ("fallback", "1 · Usó FALLBACK — el selector descartó todos los candidatos", fallback,
         "El caso más grave: no encontró ni un ícono válido y devolvió el último frame sin puntuarlo."),
        ("pobres", "2 · Eligió con 0–1 íconos detectados", pobres,
         "Encontró candidatos, pero con evidencia muy débil de que hubiera pizarra en el frame."),
        ("discrepancia", "3 · Elige un frame distinto al aprobado (resto)", discrepancia,
         "El selector converge a otra escena del video."),
        ("calibracion", "4 · Acierta", aciertos,
         "Cuando el selector de hoy SÍ reproduce el frame que se usó en el estudio — las dos "
         "imágenes son idénticas. Ya son válidos por definición; no hace falta votarlos, quedan "
         "acá para que el conteo final sea sobre los 440 videos, no solo sobre los problemáticos."),
    ]

    secciones_html = []
    for sec_id, titulo, grupo, nota in grupos:
        mostrar = grupo[:args.max_por_grupo] if args.max_por_grupo else grupo
        console.print(f"[bold]{titulo}[/] — {len(grupo)} en total, generando {len(mostrar)}…")
        tarjetas = "".join(tarjeta(r, sec_id) for r in mostrar)
        recorte = (f'<p class="nota">Mostrando {len(mostrar)} de {len(grupo)}.</p>'
                   if len(mostrar) < len(grupo) else "")
        secciones_html.append(f"""
        <section data-seccion="{sec_id}">
          <h2>{html.escape(titulo)} <span class="badge">{len(grupo)}</span>
              <span class="sec-tally" data-seccion-tally="{sec_id}"></span></h2>
          <p class="nota">{html.escape(nota)}</p>
          {recorte}
          <div class="grid">{tarjetas}</div>
        </section>""")

    html_doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<title>Auditoría del selector de pizarra</title>
<style>
  body {{ font-family: -apple-system, sans-serif; margin: 0; padding: 84px 32px 64px;
         background: #0f1115; color: #e6e6e6; }}
  h1 {{ font-size: 1.4rem; }} h2 {{ font-size: 1.1rem; border-bottom: 1px solid #333; padding-bottom: 6px; }}
  .badge {{ background: #333; border-radius: 10px; padding: 2px 10px; font-size: .85rem; }}
  .sec-tally {{ font-size: .8rem; color: #999; margin-left: 8px; }}
  .nota {{ color: #999; font-size: .88rem; margin: 4px 0 14px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(560px, 1fr)); gap: 18px; }}
  .card {{ background: #1a1d24; border-radius: 10px; padding: 12px 14px; border: 2px solid transparent; }}
  .card.fallback {{ box-shadow: inset 0 0 0 1px #c0392b; }}
  .card.voted-si {{ border-color: #2ecc71; }}
  .card.voted-no {{ border-color: #e74c3c; }}
  .card.voted-duda {{ border-color: #f39c12; }}
  .card h3 {{ margin: 0 0 8px; font-size: .95rem; font-family: monospace; color: #7fd0ff; }}
  .pair {{ display: flex; gap: 8px; }}
  figure {{ margin: 0; flex: 1; min-width: 0; }}
  figure img {{ width: 100%; border-radius: 6px; display: block; }}
  figcaption {{ font-size: .75rem; color: #aaa; text-align: center; margin-top: 4px; }}
  .ph {{ flex: 1; display: flex; align-items: center; justify-content: center; text-align: center;
        background: #222; border-radius: 6px; color: #666; font-size: .8rem; min-height: 120px; }}
  .meta {{ font-size: .75rem; color: #888; margin: 8px 0 0; }}
  .votebar {{ display: flex; gap: 6px; margin-top: 10px; }}
  .vote-btn {{ flex: 1; padding: 6px 0; border-radius: 6px; border: 1px solid #444;
              background: #22252c; color: #ccc; cursor: pointer; font-size: .82rem; }}
  .vote-btn:hover {{ background: #2a2e37; }}
  .vote-btn.active.v-si {{ background: #1e5c37; border-color: #2ecc71; color: #fff; }}
  .vote-btn.active.v-no {{ background: #6e2a22; border-color: #e74c3c; color: #fff; }}
  .vote-btn.active.v-duda {{ background: #7a5a10; border-color: #f39c12; color: #fff; }}
  #toolbar {{ position: fixed; top: 0; left: 0; right: 0; background: #14161b; z-index: 10;
             padding: 10px 32px; border-bottom: 1px solid #2a2d34; display: flex;
             align-items: center; gap: 18px; font-size: .88rem; flex-wrap: wrap; }}
  #toolbar b.ok {{ color: #2ecc71; }} #toolbar b.bad {{ color: #e74c3c; }} #toolbar b.warn {{ color: #f39c12; }}
  #toolbar button {{ background: #2c313a; color: #eee; border: 1px solid #444; border-radius: 6px;
                     padding: 6px 12px; cursor: pointer; font-size: .82rem; }}
  #toolbar button:hover {{ background: #3a4048; }}
  #toolbar input[type=file] {{ font-size: .78rem; color: #999; max-width: 160px; }}
  progress {{ width: 140px; height: 8px; }}
</style></head>
<body>
<div id="toolbar">
  <strong>Auditoría del selector</strong>
  <progress id="prog" value="0" max="1"></progress>
  <span id="tally">cargando…</span>
  <button id="export-btn">⬇ exportar CSV</button>
  <label style="cursor:pointer">⬆ importar
    <input type="file" id="import-input" accept=".csv" style="display:none">
  </label>
  <span style="color:#666; font-size:.78rem">el voto se guarda en este navegador (localStorage) —
    exportá seguido para no perderlo</span>
</div>
<h1>Auditoría del selector de pizarra — izquierda: aprobada · derecha: automática (hoy)</h1>
<p class="nota">Generado por scripts/utils/build_frame_selector_review.py sobre
reports/frame_selector_eval.csv. Solo lectura sobre el corpus; nada de esto se publica.
"válida" = la elección automática, aunque distinta de la aprobada, es una pizarra usable.</p>
{''.join(secciones_html)}
<script>
(function(){{
  const KEY = 'frameSelectorVotes_v1';
  let votes = JSON.parse(localStorage.getItem(KEY) || '{{}}');
  const save = () => localStorage.setItem(KEY, JSON.stringify(votes));

  function render(){{
    document.querySelectorAll('.card[data-vid]').forEach(card => {{
      const v = votes[card.dataset.vid];
      card.classList.remove('voted-si','voted-no','voted-duda');
      if (v) card.classList.add('voted-' + v);
      card.querySelectorAll('.vote-btn').forEach(b => b.classList.toggle('active', b.dataset.val === v));
    }});
    const cards = [...document.querySelectorAll('.card[data-vid]')];
    let si=0, no=0, duda=0;
    cards.forEach(c => {{ const v = votes[c.dataset.vid]; if (v==='si') si++; else if (v==='no') no++; else if (v==='duda') duda++; }});
    const revisadas = si+no+duda, total = cards.length;
    document.getElementById('tally').innerHTML =
      `revisadas <b>${{revisadas}}</b>/${{total}} — válida <b class="ok">${{si}}</b> · ` +
      `no válida <b class="bad">${{no}}</b> · dudosa <b class="warn">${{duda}}</b>`;
    document.getElementById('prog').value = total ? revisadas/total : 0;
    document.querySelectorAll('[data-seccion-tally]').forEach(sp => {{
      const secId = sp.dataset.seccionTally;
      const secCards = cards.filter(c => c.dataset.seccion === secId);
      const r = secCards.filter(c => votes[c.dataset.vid]).length;
      sp.textContent = secCards.length ? `(${{r}}/${{secCards.length}} revisadas)` : '';
    }});
  }}

  document.addEventListener('click', e => {{
    if (!e.target.classList.contains('vote-btn')) return;
    const card = e.target.closest('.card');
    const val = e.target.dataset.val;
    const cur = votes[card.dataset.vid];
    if (cur === val) delete votes[card.dataset.vid]; else votes[card.dataset.vid] = val;
    save(); render();
  }});

  document.getElementById('export-btn').addEventListener('click', () => {{
    const rows = [['video_id','seccion','juicio']];
    document.querySelectorAll('.card[data-vid]').forEach(c =>
      rows.push([c.dataset.vid, c.dataset.seccion, votes[c.dataset.vid] || '']));
    const csv = rows.map(r => r.map(x => `"${{String(x).replace(/"/g,'""')}}"`).join(',')).join('\\n');
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], {{type:'text/csv'}}));
    a.download = 'frame_selector_votes.csv';
    a.click();
  }});

  document.getElementById('import-input').addEventListener('change', e => {{
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = ev => {{
      ev.target.result.split('\\n').slice(1).forEach(line => {{
        const m = line.match(/^"([^"]*)","([^"]*)","([^"]*)"/);
        if (m && m[3]) votes[m[1]] = m[3];
      }});
      save(); render();
    }};
    reader.readAsText(file);
  }});

  render();
}})();
</script>
</body></html>"""

    (OUT_DIR / "index.html").write_text(html_doc, encoding="utf-8")
    console.print(f"\n[green]✓[/] {OUT_DIR / 'index.html'}")
    console.print("[dim]Abrir en el navegador de esta máquina. Solo lectura: no se tocó good_whiteboard/ ni frames/*_pizarra/.[/]")


if __name__ == "__main__":
    main()
