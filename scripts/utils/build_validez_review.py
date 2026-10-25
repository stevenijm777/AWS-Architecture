#!/usr/bin/env python3
"""
build_validez_review.py — Hoja de revisión: ¿son válidas las aristas en que modelos y referencia discrepan?

Por qué existe
--------------
El evaluador mide si una arista calza con la anotación de Cloudscape, no si es correcta. En el
brazo A (Flash, Pro y Claude con la misma transcripción manual de la pizarra) los tres modelos
coinciden entre sí bastante más que con la referencia, y la discrepancia se concentra en dos
listas:

  * consenso  — pares que dibujan los TRES modelos y la referencia no tiene;
  * ausente   — pares de la referencia que NINGÚN modelo dibuja.

Esta hoja las pone delante de una persona, caso por caso, con la pizarra y los fragmentos del
transcript donde aparecen los dos servicios, para decidir si la conexión existe en el video.
Por defecto la revisión es a ciegas: no dice de qué lista viene cada caso.

No llama a ningún modelo. Lee los `run.json` del brazo A, el ground truth y los transcripts.

Uso
---
    .venv/Scripts/python scripts/utils/build_validez_review.py
    # abre reports/validez_review/index.html
"""
from __future__ import annotations

import html
import itertools
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402
from PIL import Image  # noqa: E402

REP = PROJECT_ROOT / "reports"
RUNS = {
    "Flash": REP / "pro_vs_flash" / "flash_gemini-3.6-flash_stage1-manual",
    "Pro": REP / "pro_vs_flash" / "pro_gemini-3.1-pro-preview_stage1-manual",
    "Claude": REP / "claude",
}
GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PIZARRAS = PROJECT_ROOT / "data" / "good_whiteboard"
LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
OUT = REP / "validez_review"
MAX_FRAGMENTOS = 6


def cargar_run(path: Path) -> dict:
    run = json.loads((path / "run.json").read_text(encoding="utf-8"))
    return {r["video_id"]: r["analysis"] for r in run["results"] if r.get("status") == "success"}


def aristas_modelo(analysis: dict) -> dict:
    """{(servicio origen, servicio destino): [aristas]} de la salida de un modelo."""
    svc = {n["id"]: n["service"] for n in analysis["nodes"]}
    out: dict = {}
    for e in analysis["edges"]:
        out.setdefault((svc.get(e["source"], "?"), svc.get(e["target"], "?")), []).append(e)
    return out


def aristas_gt(G) -> dict:
    out: dict = {}
    for u, v, a in G.edges(data=True):
        out.setdefault((G.nodes[u].get("service", "?"), G.nodes[v].get("service", "?")), []).append(a)
    return out


def aristas_manual(vid: str) -> set:
    p = LAB / vid / "world_model_vision.json"
    if not p.exists():
        return set()
    wm = json.loads(p.read_text(encoding="utf-8"))
    res = {}
    for e in wm.get("entities", []):
        for k in (e.get("name"), e.get("service")):
            if k:
                res.setdefault(k.strip().lower(), e["service"])
    return {(res.get((c.get("source_label") or "").strip().lower()), res.get((c.get("target_label") or "").strip().lower()))
            for c in wm.get("visual_connections", [])}


def palabras_clave(servicio: str, nombres: set[str]) -> list[str]:
    """Términos con los que buscar un servicio en el transcript: su tipo y los nombres que le dieron."""
    cands = set(nombres)
    if not servicio.startswith("User") and servicio not in ("ThirdParty", "OnPremDC"):
        cands |= {servicio, re.sub(r"(?<=[a-z])(?=[A-Z])", " ", servicio)}
    limpios = set()
    for c in cands:
        c = re.sub(r"\s*[—#(].*$", "", c or "").strip()        # quita sufijos tipo "S3 — notas" o "S3 #2"
        if len(c) >= 2 and c.lower() not in {"aws", "user", "users", "data", "the"}:
            limpios.add(c)
    return sorted(limpios, key=len, reverse=True)


def fragmentos(vid: str, kw_a: list[str], kw_b: list[str]) -> list[dict]:
    p = RAW_DIR / f"{vid}_transcript.json"
    if not p.exists():
        return []
    segs = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(segs, list):
        return []

    def patron(kws):
        return re.compile("|".join(r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?![A-Za-z0-9])" for k in kws), re.I) if kws else None

    pa, pb = patron(kw_a), patron(kw_b)
    cand = []
    for i, s in enumerate(segs):
        t = s.get("text", "")
        a, b = bool(pa and pa.search(t)), bool(pb and pb.search(t))
        if not (a or b):
            continue
        # Vale más un fragmento que nombra a los dos; después, uno pegado a un fragmento del otro.
        vecino = any((pb if a else pa) and (pb if a else pa).search(segs[j].get("text", ""))
                     for j in (i - 1, i + 1) if 0 <= j < len(segs))
        cand.append((0 if a and b else 1 if vecino else 2, i, s, a, b))
    cand.sort(key=lambda x: (x[0], x[1]))
    elegidos = sorted(cand[:MAX_FRAGMENTOS], key=lambda x: x[1])

    def marcar(t):
        t = html.escape(t)
        for p_, cls in ((pa, "ka"), (pb, "kb")):
            if p_:
                t = p_.sub(lambda m: f'<mark class="{cls}">{m.group(0)}</mark>', t)
        return t

    return [{"t": int(s.get("start", 0)), "html": marcar(s.get("text", "")), "ambos": a and b}
            for _, _, s, a, b in elegidos]


def main() -> None:
    runs = {m: cargar_run(p) for m, p in RUNS.items()}
    videos = [v for v in runs["Flash"] if all(v in r for r in runs.values())]
    (OUT / "pizarras").mkdir(parents=True, exist_ok=True)

    casos, por_video = [], []
    for vid in videos:
        G = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
        e_gt = aristas_gt(G)
        e_mod = {m: aristas_modelo(runs[m][vid]) for m in runs}
        manual = aristas_manual(vid)

        nombres: dict[str, set] = {}
        for _, a in G.nodes(data=True):
            nombres.setdefault(a.get("service", "?"), set()).add((a.get("name") or "").strip())
        for m in runs:
            for n in runs[m][vid]["nodes"]:
                nombres.setdefault(n["service"], set()).add((n.get("name") or "").strip())
        servicios = sorted(nombres)

        del_video = []
        for a, b in itertools.permutations(servicios, 2):
            n_mod = sum((a, b) in e_mod[m] for m in runs)
            en_gt = (a, b) in e_gt
            if n_mod == 3 and not en_gt:
                grupo = "consenso"
            elif n_mod == 0 and en_gt:
                grupo = "ausente"
            else:
                continue
            kw_a, kw_b = palabras_clave(a, nombres[a]), palabras_clave(b, nombres[b])
            detalle = []
            if grupo == "consenso":
                for m in runs:
                    for e in e_mod[m][(a, b)]:
                        detalle.append(f"{m} · {e.get('type', '')} · {e.get('notes', '')}")
            else:
                for e in e_gt[(a, b)]:
                    detalle.append(f"Ground truth · flujo {e.get('flow_id', '')} paso {e.get('seq', '')} · "
                                   f"{e.get('type', '')} · {e.get('notes') or 'sin nota'}")
            del_video.append({
                "id": f"{vid}|{a}|{b}", "video": vid, "a": a, "b": b, "grupo": grupo,
                "nombres_a": sorted(x for x in nombres[a] if x and x != a)[:4],
                "nombres_b": sorted(x for x in nombres[b] if x and x != b)[:4],
                "en_manual": (a, b) in manual,
                "inversa_en_gt": (b, a) in e_gt,
                "inversa_en_modelos": sum((b, a) in e_mod[m] for m in runs),
                "detalle": detalle,
                "fragmentos": fragmentos(vid, kw_a, kw_b),
            })
        if not del_video:
            continue
        # Orden alfabético dentro del video: mezcla los dos grupos, que es lo que pide la revisión a ciegas.
        del_video.sort(key=lambda c: (c["a"], c["b"]))
        casos += del_video
        src = PIZARRAS / f"{vid}.jpg"
        if src.exists():
            im = Image.open(src).convert("RGB")
            im.thumbnail((1400, 1400))
            im.save(OUT / "pizarras" / f"{vid}.jpg", quality=82)
        por_video.append({"video": vid, "titulo": G.graph.get("name", ""), "n": len(del_video)})

    n_c = sum(c["grupo"] == "consenso" for c in casos)
    n_a = sum(c["grupo"] == "ausente" for c in casos)
    (OUT / "casos.json").write_text(json.dumps(casos, indent=1, ensure_ascii=False), encoding="utf-8")
    datos = json.dumps({"videos": por_video, "casos": casos}, ensure_ascii=False).replace("</", "<\\/")
    (OUT / "index.html").write_text(PAGINA.replace("__DATOS__", datos), encoding="utf-8")
    print(f"{len(casos)} casos en {len(por_video)} videos: {n_c} de consenso y {n_a} ausentes")
    print(f"→ {(OUT / 'index.html').relative_to(PROJECT_ROOT)}")


PAGINA = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Validez de aristas — revisión</title>
<style>
:root{--fondo:#f7f7f5;--panel:#fff;--tinta:#141413;--tinta2:#56554f;--borde:#dddcd6;--acento:#2a78d6;
      --si:#0c8a0c;--no:#c93434;--duda:#b97a00;--ka:#cfe3fb;--kb:#fde2c8}
@media (prefers-color-scheme:dark){:root{--fondo:#121211;--panel:#1c1c1a;--tinta:#f2f1ec;--tinta2:#b3b1a8;
      --borde:#34342f;--acento:#5a9cf0;--si:#3fbf3f;--no:#ef6b6b;--duda:#e0a530;--ka:#1f3f66;--kb:#5a3a1a}}
*{box-sizing:border-box}
body{margin:0;background:var(--fondo);color:var(--tinta);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--panel);border-bottom:1px solid var(--borde);padding:10px 16px;
       display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center}
header h1{font-size:1rem;margin:0 8px 0 0}
header input[type=text]{padding:5px 8px;border:1px solid var(--borde);border-radius:6px;background:var(--fondo);color:var(--tinta);width:150px}
button,.btn{padding:5px 11px;border:1px solid var(--borde);border-radius:6px;background:var(--fondo);color:var(--tinta);cursor:pointer;font:inherit;font-size:.86rem}
button:hover{border-color:var(--acento)}
#progreso{font-variant-numeric:tabular-nums;font-weight:600}
main{max-width:1180px;margin:0 auto;padding:18px 16px 80px}
.intro{background:var(--panel);border:1px solid var(--borde);border-radius:10px;padding:14px 18px;margin-bottom:22px}
.intro p{margin:6px 0}
section.video{margin-bottom:38px}
section.video h2{font-size:1.02rem;margin:0 0 8px}
section.video h2 a{color:var(--acento);font-weight:400;font-size:.86rem;margin-left:8px}
.rejilla{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:16px;align-items:start}
@media (max-width:900px){.rejilla{grid-template-columns:1fr}}
.pizarra{position:sticky;top:64px}
.pizarra img{width:100%;border-radius:8px;border:1px solid var(--borde);display:block}
@media (max-width:900px){.pizarra{position:static}}
.caso{background:var(--panel);border:1px solid var(--borde);border-left:4px solid var(--borde);border-radius:8px;padding:11px 14px;margin-bottom:12px}
.caso.v-valida{border-left-color:var(--si)} .caso.v-no{border-left-color:var(--no)} .caso.v-dudosa{border-left-color:var(--duda)}
.arista{font-size:1.02rem;font-weight:600;display:flex;flex-wrap:wrap;gap:6px;align-items:baseline}
.arista .fl{color:var(--tinta2)}
.sa{background:var(--ka);border-radius:4px;padding:0 6px} .sb{background:var(--kb);border-radius:4px;padding:0 6px}
.alias{font-size:.82rem;color:var(--tinta2);margin:2px 0 6px}
.frag{font-size:.88rem;margin:5px 0;padding-left:8px;border-left:2px solid var(--borde)}
.frag.ambos{border-left-color:var(--acento)}
.frag a{color:var(--acento);text-decoration:none;font-variant-numeric:tabular-nums;margin-right:6px}
mark.ka{background:var(--ka);color:inherit} mark.kb{background:var(--kb);color:inherit}
.sinfrag{font-size:.86rem;color:var(--tinta2);font-style:italic}
.controles{display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;margin-top:9px;padding-top:9px;border-top:1px solid var(--borde)}
.controles label{font-size:.88rem;display:flex;gap:5px;align-items:center;cursor:pointer}
.veredicto{display:flex;gap:6px;margin-left:auto}
.veredicto button.on[data-v=valida]{background:var(--si);border-color:var(--si);color:#fff}
.veredicto button.on[data-v=no]{background:var(--no);border-color:var(--no);color:#fff}
.veredicto button.on[data-v=dudosa]{background:var(--duda);border-color:var(--duda);color:#fff}
.nota{width:100%;padding:5px 8px;border:1px solid var(--borde);border-radius:6px;background:var(--fondo);color:var(--tinta);font:inherit;font-size:.86rem}
details.origen{margin-top:8px;font-size:.84rem;color:var(--tinta2)}
details.origen li{margin:2px 0}
body.ciega details.origen{display:none}
body.pendientes .caso.hecho{display:none}
</style></head>
<body class="ciega">
<header>
  <h1>Validez de aristas</h1>
  <label>Revisor <input type="text" id="revisor" placeholder="tu nombre"></label>
  <span id="progreso"></span>
  <label><input type="checkbox" id="soloPend"> solo pendientes</label>
  <label><input type="checkbox" id="verOrigen"> mostrar origen (quita la revisión a ciegas)</label>
  <span style="margin-left:auto;display:flex;gap:8px">
    <button id="expJson">Exportar JSON</button><button id="expCsv">Exportar CSV</button>
    <label class="btn">Importar JSON<input type="file" id="imp" accept=".json" hidden></label>
  </span>
</header>
<main>
<div class="intro">
  <p><strong>Qué se decide en cada caso:</strong> ¿existe esta conexión, <em>en este sentido</em>, en la arquitectura que explica el video?</p>
  <p>Marca dónde está la evidencia (la pizarra, el audio, las dos o ninguna) y da un veredicto: <strong>válida</strong>, <strong>no válida</strong> o <strong>dudosa</strong>.
     Los fragmentos son las frases del transcript que nombran a uno de los dos servicios; los que nombran a los dos llevan la barra azul. El minuto abre el video en ese punto.</p>
  <p>La revisión es a ciegas: no se indica si la conexión la propusieron los modelos o viene de la anotación de referencia. Las respuestas se guardan en este navegador; al terminar, exporta el JSON.</p>
</div>
<div id="lista"></div>
</main>
<script id="datos" type="application/json">__DATOS__</script>
<script>
const D = JSON.parse(document.getElementById('datos').textContent);
const CLAVE = 'validez_review_v1';
let E = {revisor:'', r:{}};
try { E = Object.assign(E, JSON.parse(localStorage.getItem(CLAVE) || '{}')); } catch (e) {}
const guardar = () => { try { localStorage.setItem(CLAVE, JSON.stringify(E)); } catch (e) {} };
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const mmss = t => Math.floor(t/60) + ':' + String(t%60).padStart(2,'0');
const lista = document.getElementById('lista');

for (const v of D.videos) {
  const sec = document.createElement('section'); sec.className = 'video';
  const casos = D.casos.filter(c => c.video === v.video);
  sec.innerHTML = `<h2>${esc(v.titulo || v.video)} <span style="color:var(--tinta2);font-weight:400">· ${esc(v.video)} · ${casos.length} casos</span>
      <a href="https://www.youtube.com/watch?v=${encodeURIComponent(v.video)}" target="_blank" rel="noopener">abrir video</a></h2>
    <div class="rejilla"><div class="pizarra"><a href="pizarras/${encodeURIComponent(v.video)}.jpg" target="_blank">
      <img loading="lazy" src="pizarras/${encodeURIComponent(v.video)}.jpg" alt="Pizarra del video ${esc(v.video)}"></a></div>
    <div class="casos"></div></div>`;
  const cont = sec.querySelector('.casos');
  for (const c of casos) {
    const d = document.createElement('div'); d.className = 'caso'; d.dataset.id = c.id;
    const alias = [c.nombres_a.length ? `<span class="sa">${esc(c.a)}</span> también aparece como: ${c.nombres_a.map(esc).join(', ')}` : '',
                   c.nombres_b.length ? `<span class="sb">${esc(c.b)}</span> también aparece como: ${c.nombres_b.map(esc).join(', ')}` : ''].filter(Boolean).join('<br>');
    const frags = c.fragmentos.length
      ? c.fragmentos.map(f => `<div class="frag${f.ambos ? ' ambos' : ''}"><a href="https://www.youtube.com/watch?v=${encodeURIComponent(c.video)}&t=${f.t}s" target="_blank" rel="noopener">${mmss(f.t)}</a>${f.html}</div>`).join('')
      : '<div class="sinfrag">El transcript no nombra a ninguno de los dos servicios con estos términos.</div>';
    const origen = c.grupo === 'consenso' ? 'La dibujan los tres modelos y no está en la referencia.' : 'Está en la referencia y no la dibuja ningún modelo.';
    d.innerHTML = `<div class="arista"><span class="sa">${esc(c.a)}</span><span class="fl">→</span><span class="sb">${esc(c.b)}</span></div>
      <div class="alias">${alias}</div>${frags}
      <div class="controles">
        <label><input type="checkbox" data-k="pizarra"> está en la pizarra</label>
        <label><input type="checkbox" data-k="audio"> la dice el audio</label>
        <div class="veredicto"><button data-v="valida">Válida</button><button data-v="no">No válida</button><button data-v="dudosa">Dudosa</button></div>
        <input class="nota" type="text" placeholder="nota (opcional)">
      </div>
      <details class="origen"><summary>origen</summary><p>${origen}
        ${c.en_manual ? ' Está en la transcripción manual de la pizarra.' : ' No está en la transcripción manual de la pizarra.'}
        ${c.inversa_en_gt ? ' La referencia tiene el sentido inverso.' : ''}
        ${c.inversa_en_modelos ? ` ${c.inversa_en_modelos} de 3 modelos dibujan el sentido inverso.` : ''}</p>
        <ul>${c.detalle.map(x => `<li>${esc(x)}</li>`).join('')}</ul></details>`;
    cont.appendChild(d);
  }
  lista.appendChild(sec);
}

function pintar(d) {
  const r = E.r[d.dataset.id] || {};
  d.querySelectorAll('input[type=checkbox]').forEach(i => i.checked = !!r[i.dataset.k]);
  d.querySelectorAll('.veredicto button').forEach(b => b.classList.toggle('on', r.veredicto === b.dataset.v));
  d.querySelector('.nota').value = r.nota || '';
  d.classList.remove('v-valida', 'v-no', 'v-dudosa');
  if (r.veredicto) d.classList.add('v-' + r.veredicto);
  d.classList.toggle('hecho', !!r.veredicto);
}
function progreso() {
  const n = D.casos.filter(c => (E.r[c.id] || {}).veredicto).length;
  document.getElementById('progreso').textContent = `${n} de ${D.casos.length} revisados`;
}
function pintarTodo() { document.querySelectorAll('.caso').forEach(pintar); progreso(); document.getElementById('revisor').value = E.revisor || ''; }

lista.addEventListener('click', ev => {
  const b = ev.target.closest('.veredicto button'); if (!b) return;
  const d = b.closest('.caso'), r = E.r[d.dataset.id] || (E.r[d.dataset.id] = {});
  r.veredicto = r.veredicto === b.dataset.v ? '' : b.dataset.v;
  guardar(); pintar(d); progreso();
});
lista.addEventListener('change', ev => {
  const d = ev.target.closest('.caso'); if (!d) return;
  const r = E.r[d.dataset.id] || (E.r[d.dataset.id] = {});
  if (ev.target.matches('input[type=checkbox]')) r[ev.target.dataset.k] = ev.target.checked;
  if (ev.target.matches('.nota')) r.nota = ev.target.value;
  guardar();
});
document.getElementById('revisor').addEventListener('change', ev => { E.revisor = ev.target.value.trim(); guardar(); });
document.getElementById('soloPend').addEventListener('change', ev => document.body.classList.toggle('pendientes', ev.target.checked));
document.getElementById('verOrigen').addEventListener('change', ev => document.body.classList.toggle('ciega', !ev.target.checked));

function filas() {
  return D.casos.map(c => { const r = E.r[c.id] || {};
    return {id: c.id, video: c.video, origen: c.a, destino: c.b, grupo: c.grupo, en_manual: c.en_manual,
            pizarra: !!r.pizarra, audio: !!r.audio, veredicto: r.veredicto || '', nota: r.nota || '', revisor: E.revisor || ''}; });
}
function bajar(nombre, texto, tipo) {
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([texto], {type: tipo}));
  a.download = nombre; a.click(); URL.revokeObjectURL(a.href);
}
const sufijo = () => (E.revisor || 'sin_nombre').replace(/[^A-Za-z0-9_-]+/g, '_');
document.getElementById('expJson').onclick = () =>
  bajar(`validez_${sufijo()}.json`, JSON.stringify({revisor: E.revisor, exportado: new Date().toISOString(), casos: filas()}, null, 1), 'application/json');
document.getElementById('expCsv').onclick = () => {
  const f = filas(), cols = Object.keys(f[0]);
  const q = v => '"' + String(v).replace(/"/g, '""') + '"';
  bajar(`validez_${sufijo()}.csv`, '﻿' + [cols.join(',')].concat(f.map(r => cols.map(k => q(r[k])).join(','))).join('\r\n'), 'text/csv');
};
document.getElementById('imp').addEventListener('change', async ev => {
  const file = ev.target.files[0]; if (!file) return;
  try {
    const j = JSON.parse(await file.text());
    E.revisor = j.revisor || E.revisor;
    for (const c of j.casos || []) E.r[c.id] = {pizarra: !!c.pizarra, audio: !!c.audio, veredicto: c.veredicto || '', nota: c.nota || ''};
    guardar(); pintarTodo();
  } catch (e) { alert('No pude leer ese archivo como una exportación de esta hoja.'); }
  ev.target.value = '';
});
pintarTodo();
</script>
</body></html>
"""

if __name__ == "__main__":
    main()
