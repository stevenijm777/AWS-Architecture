#!/usr/bin/env python3
"""
build_invenciones_review.py — Galería para revisar a ojo las invenciones "puras".

Qué es una invención pura
-------------------------
De las 93 conexiones que el pipeline emite y no figuran en la transcripción humana ciega,
la mayoría tiene una causa identificable: 26 están en el ground truth (el anotador las
omitió), 51 arrastran un nodo que el anotador no registró, y 3 son la misma conexión en
sentido inverso.

Quedan **13** donde el modelo conectó dos servicios que **ambos** vieron, con una arista
que no está ni en la transcripción humana ni en el ground truth. Esas son las únicas
candidatas a error de percepción genuino, y son las que esta galería pone frente a la
pizarra para decidirlas mirando.

Condición usada: **Parsimonious sin transcript** — una sola llamada, sin canal verbal, que
es la comparación justa contra una lectura humana que tampoco tuvo audio.

Alcance
-------
Salida a `reports/invenciones_review/`, que **no se sincroniza al repositorio publicable**:
son capturas de video de terceros, igual que la galería del selector de pizarra. Solo
lectura sobre el corpus.

Uso
---
    .venv/bin/python scripts/utils/build_invenciones_review.py
"""
from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image
from rich.console import Console

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CASOS = PROJECT_ROOT / "reports" / "invenciones_puras.json"
GOOD_WB = PROJECT_ROOT / "data" / "good_whiteboard"
LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
OUT = PROJECT_ROOT / "reports" / "invenciones_review"
THUMB_W = 760

console = Console()


def thumb(src: Path, dst: Path) -> bool:
    if dst.exists():
        return True
    if not src.exists():
        return False
    with Image.open(src) as im:
        w, h = im.size
        im.convert("RGB").resize((THUMB_W, int(h * THUMB_W / w))).save(dst, "JPEG", quality=86)
    return True


def main() -> None:
    if not CASOS.exists():
        console.print(f"[red]✗ Falta {CASOS}[/]"); raise SystemExit(1)

    casos = json.loads(CASOS.read_text(encoding="utf-8"))
    por_video: dict[str, list[dict]] = defaultdict(list)
    for c in casos:
        por_video[c["video_id"]].append(c)

    (OUT / "thumbs").mkdir(parents=True, exist_ok=True)
    console.print(f"{len(casos)} invenciones puras en {len(por_video)} videos\n")

    tarjetas = []
    for vid, cs in sorted(por_video.items(), key=lambda x: -len(x[1])):
        rel = f"thumbs/{vid}.jpg"
        ok = thumb(GOOD_WB / f"{vid}.jpg", OUT / rel)

        # Qué anotó el humano, para tener a mano la referencia contra la que se compara.
        wm_path = LAB / vid / "world_model_vision.json"
        entidades = conexiones = "—"
        if wm_path.exists():
            wm = json.loads(wm_path.read_text(encoding="utf-8"))
            entidades = ", ".join(f"{e.get('name')}[{e.get('service')}]"
                                  for e in wm.get("entities", []))
            conexiones = " · ".join(f"{c.get('source_label')}→{c.get('target_label')}"
                                    for c in wm.get("visual_connections", []))

        filas = "".join(
            f'<li><code>{html.escape(c["origen"])}</code> '
            f'<span class="ar">→</span> <code>{html.escape(c["destino"])}</code>'
            f'<span class="votes" data-key="{html.escape(vid)}|{html.escape(c["origen"])}|{html.escape(c["destino"])}">'
            f'<button data-v="si">✓ sí está</button>'
            f'<button data-v="no">✗ no está</button>'
            f'<button data-v="duda">? dudosa</button></span></li>'
            for c in cs)

        tarjetas.append(f"""
        <section class="caso">
          <h2>{html.escape(vid)} <span class="n">{len(cs)} invención(es)</span></h2>
          {'<img src="' + rel + '" loading="lazy">' if ok else '<div class="ph">(sin pizarra)</div>'}
          <p class="pregunta">¿Se ve en la pizarra alguna de estas conexiones?</p>
          <ul>{filas}</ul>
          <details><summary>lo que anotó el humano</summary>
            <p class="wm"><b>entidades:</b> {html.escape(entidades)}</p>
            <p class="wm"><b>conexiones:</b> {html.escape(conexiones)}</p>
          </details>
        </section>""")

    doc = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><title>Invenciones puras — revisión</title>
<style>
 body{{font-family:-apple-system,sans-serif;margin:0;padding:76px 30px 60px;background:#0f1115;color:#e6e6e6}}
 h1{{font-size:1.35rem}} h2{{font-size:1rem;font-family:monospace;color:#7fd0ff;margin:0 0 10px}}
 .n{{font-family:sans-serif;color:#888;font-size:.8rem;font-weight:400}}
 .caso{{background:#1a1d24;border-radius:10px;padding:14px 16px;margin-bottom:20px;max-width:840px}}
 .caso img{{width:100%;border-radius:6px;display:block}}
 .ph{{background:#222;color:#666;padding:50px;text-align:center;border-radius:6px}}
 .pregunta{{font-size:.9rem;color:#ccc;margin:12px 0 6px}}
 ul{{list-style:none;padding:0;margin:0}}
 li{{display:flex;align-items:center;gap:8px;padding:7px 0;border-top:1px solid #2a2d34;flex-wrap:wrap}}
 code{{background:#22252c;padding:2px 8px;border-radius:4px;font-size:.85rem}}
 .ar{{color:#888}}
 .votes{{margin-left:auto;display:flex;gap:5px}}
 .votes button{{background:#22252c;border:1px solid #444;color:#ccc;border-radius:6px;
   padding:4px 10px;cursor:pointer;font-size:.78rem}}
 .votes button:hover{{background:#2a2e37}}
 .votes button.on[data-v=si]{{background:#1e5c37;border-color:#2ecc71;color:#fff}}
 .votes button.on[data-v=no]{{background:#6e2a22;border-color:#e74c3c;color:#fff}}
 .votes button.on[data-v=duda]{{background:#7a5a10;border-color:#f39c12;color:#fff}}
 details{{margin-top:10px}} summary{{cursor:pointer;color:#888;font-size:.8rem}}
 .wm{{font-size:.75rem;color:#999;margin:6px 0}}
 #bar{{position:fixed;top:0;left:0;right:0;background:#14161b;border-bottom:1px solid #2a2d34;
   padding:11px 30px;display:flex;gap:18px;align-items:center;font-size:.87rem;z-index:9}}
 #bar button{{background:#2c313a;color:#eee;border:1px solid #444;border-radius:6px;
   padding:6px 12px;cursor:pointer;font-size:.8rem}}
 b.ok{{color:#2ecc71}} b.bad{{color:#e74c3c}} b.warn{{color:#f39c12}}
</style></head><body>
<div id="bar"><strong>Invenciones puras</strong><span id="t">…</span>
  <button id="exp">⬇ exportar CSV</button>
  <span style="color:#666;font-size:.76rem">se guarda en este navegador — exportá al terminar</span></div>
<h1>Las {len(casos)} conexiones sin explicación conocida</h1>
<p style="color:#999;font-size:.87rem;max-width:840px">
 El modelo conectó dos servicios que el anotador humano <b>sí</b> vio, con una arista que no
 está ni en su lectura ni en el ground truth. Son las únicas candidatas a error de percepción
 genuino: las otras 80 divergencias ya tienen causa identificada.
 Condición: <b>Parsimonious sin transcript</b> (sin audio, igual que la lectura humana).</p>
{''.join(tarjetas)}
<script>
(function(){{
 const K='invencionesPuras_v1'; let v=JSON.parse(localStorage.getItem(K)||'{{}}');
 const save=()=>localStorage.setItem(K,JSON.stringify(v));
 function r(){{
  document.querySelectorAll('.votes').forEach(s=>{{
   const k=s.dataset.key;
   s.querySelectorAll('button').forEach(b=>b.classList.toggle('on',v[k]===b.dataset.v));}});
  const all=[...document.querySelectorAll('.votes')].map(s=>v[s.dataset.key]);
  const c=x=>all.filter(y=>y===x).length;
  document.getElementById('t').innerHTML=
   `revisadas <b>${{all.filter(Boolean).length}}</b>/${{all.length}} — sí está <b class="ok">${{c('si')}}</b> · `+
   `no está <b class="bad">${{c('no')}}</b> · dudosa <b class="warn">${{c('duda')}}</b>`;}}
 document.addEventListener('click',e=>{{
  if(e.target.tagName!=='BUTTON'||!e.target.dataset.v)return;
  const k=e.target.closest('.votes').dataset.key;
  v[k]=v[k]===e.target.dataset.v?undefined:e.target.dataset.v;
  if(!v[k])delete v[k]; save(); r();}});
 document.getElementById('exp').addEventListener('click',()=>{{
  const rows=[['video_id','origen','destino','juicio']];
  document.querySelectorAll('.votes').forEach(s=>{{
   const p=s.dataset.key.split('|'); rows.push([...p, v[s.dataset.key]||'']);}});
  const csv=rows.map(x=>x.map(y=>`"${{y}}"`).join(',')).join('\\n');
  const a=document.createElement('a');
  a.href=URL.createObjectURL(new Blob([csv],{{type:'text/csv'}}));
  a.download='invenciones_puras_votos.csv'; a.click();}});
 r();}})();
</script></body></html>"""

    (OUT / "index.html").write_text(doc, encoding="utf-8")
    console.print(f"[green]✓[/] {(OUT / 'index.html').relative_to(PROJECT_ROOT)}")
    console.print("[dim]No se sincroniza al repo publicable. Solo lectura sobre el corpus.[/]")


if __name__ == "__main__":
    main()
