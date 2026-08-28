#!/usr/bin/env python3
"""
build_vision_lab.py — Banco de trabajo para los World Models hechos a mano.

Qué resuelve
------------
El experimento del oráculo necesita un World Model transcrito por un humano
desde la pizarra: la "trampa" que se le pasa a Stage 2 para medir cuánto
mejoraría si Stage 1 fuera perfecto. Hay 12 hechos sobre un panel de 30, y no
existía forma de (a) verificar que los 12 son fieles a la pizarra ni (b)
escribir los 18 que faltan viendo la pizarra y el grafo al mismo tiempo.

Este script arma una página autocontenida con, para cada uno de los 30 videos:
el mejor frame de pizarra, el enlace al video, el grafo de Cloudscape ya
renderizado, el World Model hecho a mano si existe, un editor de JSON con
botón de renderizado, y un cuadro de anotaciones.

El renderizador vive en el navegador, no acá: el mismo código dibuja el grafo
de Cloudscape, el hecho a mano y el que se pegue en el editor. Sin eso, probar
una corrección exigiría volver a correr este script.

Salida
------
    reports/vision_lab/index.html   (autocontenido, se abre con doble clic)

Uso
---
    .venv/bin/python scripts/ablation/build_vision_lab.py
"""
from __future__ import annotations

import base64
import csv
import io
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402
from PIL import Image  # noqa: E402
from rich.console import Console  # noqa: E402

console = Console()

GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
ICONS = PROJECT_ROOT / "graph_renderer" / "icons"
SERVICES_CSV = PROJECT_ROOT / "graph_renderer" / "services.csv"
OUT = PROJECT_ROOT / "reports" / "vision_lab" / "index.html"

PANEL_14 = [
    "-3lnf5lzsH0", "-kA0ahrhX3I", "-wLEkq21cvA", "07lfvavMdfU", "1aYoIZvabbk",
    "2L0m28ZLmtE", "2e3vOxsHekE", "6CgqEzyWpeA", "6EUknQqaV1w", "6YkguepAQuQ",
    "BZ32w0SSAoY", "Cgv0kfp_6xQ", "wjtSHyENv0I", "ww5fiygF6eg",
]
NEW_16 = [
    "2XVgpMwY5iE", "7V8wTCkjOqo", "90rWUjKjnAE", "9qTEHITVeLE", "BlCXEMp_lqY",
    "FfSNnH2bbNc", "H2fOkeXxpyw", "JYeXbUdFOdw", "SSWwnNVYi_Q", "a6kqyqTNJM4",
    "c-1GXhOOOww", "f5EJBUfGZtw", "hMK2NJ-q9nc", "jV8DwutbXbg", "jg85DzUZ9Ac",
    "u3ZwnulzLnU",
]
PANEL_30 = PANEL_14 + NEW_16

# La pizarra es el documento que se está transcribiendo, así que se degrada lo
# menos posible: a 1600 px de ancho todavía se leen las etiquetas escritas a
# mano, y 30 imágenes entran en un HTML que abre sin pelear.
MAX_W = 1600
JPEG_Q = 85


def load_catalog() -> dict[str, dict]:
    with open(SERVICES_CSV, encoding="utf-8") as f:
        return {r["name"]: r for r in csv.DictReader(f)}


def icon_data_uris() -> dict[str, str]:
    out = {}
    for p in sorted(ICONS.glob("*.png")):
        out[p.stem] = "data:image/png;base64," + base64.b64encode(p.read_bytes()).decode()
    return out


def whiteboard_b64(vid: str) -> tuple[str, int, int]:
    p = LAB / vid / "best_whiteboard.jpg"
    im = Image.open(p).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q, optimize=True)
    return ("data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(),
            im.width, im.height)


def gt_graph(vid: str) -> dict:
    """Cloudscape en la misma forma {nodes, edges} que consume el renderizador."""
    g = nx.read_graphml(GT_DIR / f"{vid}.graphml")
    nodes = [{"id": str(n), "service": a.get("service", ""),
              "name": a.get("name", "") or a.get("service", ""),
              "notes": a.get("notes", "")} for n, a in g.nodes(data=True)]
    edges = [{"source": str(u), "target": str(v),
              "flow_id": int(a.get("flow_id", 0) or 0), "seq": str(a.get("seq", "")),
              "type": a.get("type", ""), "notes": a.get("notes", "")}
             for u, v, a in g.edges(data=True)]
    return {"nodes": nodes, "edges": edges,
            "meta": {"name": g.graph.get("name", ""), "link": g.graph.get("link", ""),
                     "categories": g.graph.get("categories", ""),
                     "graph_usable": bool(g.graph.get("graph_usable", True))}}


def main() -> None:
    catalog = load_catalog()
    icons = icon_data_uris()
    # servicio -> stem del icono, resuelto acá para que el navegador no cargue el CSV
    svc_icon = {name: (r.get("image_url") or "").strip()
                for name, r in catalog.items()}

    videos = []
    for vid in PANEL_30:
        img, w, h = whiteboard_b64(vid)
        gt = gt_graph(vid)
        wm_path = LAB / vid / "world_model_vision.json"
        wm = json.loads(wm_path.read_text(encoding="utf-8")) if wm_path.exists() else None
        videos.append({
            "id": vid,
            "panel": 14 if vid in PANEL_14 else 16,
            "title": gt["meta"]["name"] or vid,
            "link": gt["meta"]["link"] or f"https://www.youtube.com/watch?v={vid}",
            "categories": gt["meta"]["categories"],
            "img": img, "img_w": w, "img_h": h,
            "gt": {"nodes": gt["nodes"], "edges": gt["edges"]},
            "wm": wm,
        })
        console.print(f"  [green]✓[/] {vid}  GT {len(gt['nodes'])}n/{len(gt['edges'])}e"
                      f"{'  · trampa' if wm else '  · [yellow]sin trampa[/]'}")

    payload = {"videos": videos, "icons": icons, "svc_icon": svc_icon,
               "services": sorted(catalog)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(HTML.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False)),
                   encoding="utf-8")
    n_wm = sum(1 for v in videos if v["wm"])
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}  "
                  f"({OUT.stat().st_size/1e6:.1f} MB · {len(videos)} videos · "
                  f"{n_wm} con trampa · {len(videos)-n_wm} por hacer)")


HTML = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Banco de trabajo · World Models a mano</title>
<style>
:root{
  --bg:#f6f7f9; --card:#fff; --ink:#11161d; --ink2:#5a6572; --line:#dfe3e8;
  --accent:#2b6cb0; --ok:#2f855a; --warn:#b7791f; --bad:#c53030; --code:#f2f4f7;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#12151a; --card:#191d24; --ink:#e8ecf1; --ink2:#98a2b0; --line:#2b313a;
  --accent:#7cb0e8; --ok:#68d391; --warn:#f6c667; --bad:#fc8181; --code:#0f1218;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.wrap{max-width:1720px;margin:0 auto;padding:22px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--ink2);font-size:14px;margin-bottom:18px}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:18px;
  position:sticky;top:0;background:var(--bg);padding:10px 0;z-index:20;border-bottom:1px solid var(--line)}
button,select{font:inherit;padding:7px 13px;border:1px solid var(--line);border-radius:7px;
  background:var(--card);color:var(--ink);cursor:pointer}
button:hover{border-color:var(--accent)}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600}
.pill{padding:3px 9px;border-radius:99px;font-size:12px;font-weight:600;border:1px solid var(--line)}
.pill.has{color:var(--ok);border-color:var(--ok)}
.pill.miss{color:var(--warn);border-color:var(--warn)}
.pill.p14{color:var(--accent);border-color:var(--accent)}
details.doc{background:var(--card);border:1px solid var(--line);border-radius:10px;
  padding:12px 16px;margin-bottom:20px}
details.doc summary{cursor:pointer;font-weight:600}
pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:12px;
  overflow-x:auto;font:12.5px/1.5 ui-monospace,"Cascadia Code",Menlo,monospace}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:16px;margin-bottom:22px}
.card h2{font-size:16px;margin:0 0 3px}
.card h2 a{color:var(--ink);text-decoration:none}
.card h2 a:hover{color:var(--accent)}
.meta{color:var(--ink2);font-size:12.5px;margin-bottom:12px;display:flex;gap:8px;
  flex-wrap:wrap;align-items:center}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:1100px){.grid{grid-template-columns:1fr}}
.panel{border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--bg)}
.panel>.hd{padding:6px 11px;font-size:12.5px;font-weight:600;color:var(--ink2);
  border-bottom:1px solid var(--line);background:var(--card);display:flex;
  justify-content:space-between;align-items:center;gap:8px}
.panel img{width:100%;display:block;cursor:zoom-in}
.gbox{width:100%;height:400px;overflow:auto;background:var(--bg)}
.gbox svg{display:block}
textarea{width:100%;font:12.5px/1.5 ui-monospace,Menlo,monospace;padding:10px;
  border:1px solid var(--line);border-radius:8px;background:var(--code);color:var(--ink);
  resize:vertical}
.editor{margin-top:16px}
.editor .row{display:flex;gap:8px;align-items:center;margin:8px 0;flex-wrap:wrap}
.notes{margin-top:14px}
.notes textarea{background:var(--card);font:14px/1.55 system-ui,sans-serif;min-height:72px}
.warn{margin:8px 0 0;padding:9px 11px;border-radius:7px;font-size:13px;
  background:color-mix(in srgb,var(--warn) 12%,transparent);border:1px solid var(--warn)}
.warn.bad{background:color-mix(in srgb,var(--bad) 12%,transparent);border-color:var(--bad)}
.warn ul{margin:5px 0 0 18px;padding:0}
.saved{color:var(--ok);font-size:12px;font-weight:600;opacity:0;transition:opacity .2s}
.saved.on{opacity:1}
#lb{position:fixed;inset:0;background:rgba(0,0,0,.93);display:none;z-index:100;
  overflow:auto;cursor:zoom-out}
#lb img{display:block;margin:auto;max-width:none}
#lb.on{display:block}
.hidden{display:none!important}
</style></head><body>
<div class="wrap">
  <h1>Banco de trabajo · World Models a mano</h1>
  <div class="sub">Panel de 30 videos. Compará la pizarra con el grafo de Cloudscape,
    escribí o corregí el World Model, y renderizalo para ver si se parece a lo dibujado.</div>

  <div class="bar">
    <select id="filter">
      <option value="all">Todos (30)</option>
      <option value="has">Con trampa hecha</option>
      <option value="miss">Sin trampa — por hacer</option>
      <option value="p14">Solo el panel de 14</option>
    </select>
    <button id="expAll" class="primary">Exportar todo mi trabajo</button>
    <button id="impAll">Importar</button>
    <input type="file" id="impFile" accept=".json" class="hidden">
    <span id="count" class="pill"></span>
  </div>

  <details class="doc">
    <summary>Formato del JSON que acepta el renderizador</summary>
    <p>Reconoce dos formas y las detecta solo. Para escribir la trampa usá la
       <b>primera</b>: es la que Stage 2 recibe como entrada.</p>
    <p><b>1 · World Model</b> — lo que ve el modelo de visión. Las conexiones
       referencian entidades por su <code>name</code> o su <code>service</code>,
       no por índice.</p>
<pre>{
  "entities": [
    { "service": "S3", "name": "S3", "type": "S3",
      "rationale": "bucket dibujado arriba a la izquierda" },
    { "service": "StepFunctions", "name": "STEP FUNCTIONS", "type": "StepFunctions",
      "rationale": "caja central que orquesta" }
  ],
  "visual_connections": [
    { "source_label": "S3", "target_label": "STEP FUNCTIONS",
      "arrow_direction": "right",
      "description": "flecha sólida del bucket al orquestador" }
  ]
}</pre>
    <p><b>2 · Grafo Cloudscape</b> — la forma del ground truth y de la salida de
       Stage 2. Las aristas referencian nodos por <code>id</code>.</p>
<pre>{
  "nodes": [
    { "id": "0", "service": "S3", "name": "", "notes": "" },
    { "id": "1", "service": "StepFunctions", "name": "", "notes": "" }
  ],
  "edges": [
    { "source": "0", "target": "1", "flow_id": 0, "seq": "1",
      "type": "data", "notes": "" }
  ]
}</pre>
    <p>El campo <code>service</code> debe salir del catálogo de Cloudscape para que
       tenga icono; si no lo reconoce te avisa y dibuja el genérico. Los colores de
       las flechas siguen el <code>flow_id</code>. Los avisos bajo cada render
       marcan etiquetas que no resuelven, entidades sin ninguna conexión y
       servicios fuera del catálogo.</p>
  </details>

  <div id="cards"></div>
</div>
<div id="lb"><img id="lbimg" alt=""></div>

<script type="application/json" id="payload">/*__DATA__*/</script>
<script>
const D = JSON.parse(document.getElementById('payload').textContent);
const ICONS = D.icons, SVC_ICON = D.svc_icon;
const SVC_SET = new Set(D.services);
const FLOW = ['#1a1a1a','#e53935','#43a047','#1e88e5','#8e24aa','#f4511e','#00897b',
              '#d81b60','#c9a227','#00acc1','#757575','#795548','#546e7a','#9e9d24'];
const KEY = v => 'vlab:' + v;

/* ── normalización: acepta las dos formas y devuelve {nodes,edges,warns} ── */
function normalize(raw){
  const warns = [];
  let o = raw;
  for (const k of ['graph','analysis','world_model']) if (o && o[k] && typeof o[k]==='object') o = o[k];

  let nodes = [], edges = [];
  if (Array.isArray(o?.entities)){
    // World Model: las conexiones vienen por etiqueta, hay que resolverlas.
    const byLabel = new Map();
    nodes = o.entities.map((e,i) => {
      const id = String(i);
      for (const k of [e.name, e.service]) if (k && !byLabel.has(k)) byLabel.set(k, id);
      return {id, service:e.service||'', name:e.name||e.service||'', notes:e.rationale||''};
    });
    const lower = new Map([...byLabel].map(([k,v])=>[String(k).toLowerCase().trim(),v]));
    const resolve = l => byLabel.get(l) ?? lower.get(String(l||'').toLowerCase().trim());
    (o.visual_connections||[]).forEach(c => {
      const s = resolve(c.source_label), t = resolve(c.target_label);
      if (s===undefined || t===undefined){
        warns.push(`Conexión sin resolver: "${c.source_label}" → "${c.target_label}"`);
        return;
      }
      edges.push({source:s, target:t, flow_id:0, seq:'', type:'', notes:c.description||''});
    });
  } else if (Array.isArray(o?.nodes)){
    nodes = o.nodes.map((n,i) => ({id:String(n.id ?? i), service:n.service||'',
      name:n.name||n.service||'', notes:n.notes||''}));
    const ids = new Set(nodes.map(n=>n.id));
    (o.edges||[]).forEach(e => {
      const s=String(e.source), t=String(e.target);
      if(!ids.has(s)||!ids.has(t)){ warns.push(`Arista a un id inexistente: ${s} → ${t}`); return; }
      edges.push({source:s,target:t,flow_id:+e.flow_id||0,seq:String(e.seq??''),
        type:e.type||'',notes:e.notes||''});
    });
  } else {
    throw new Error('No encuentro ni "entities" ni "nodes" en el JSON.');
  }

  const deg = new Map(nodes.map(n=>[n.id,0]));
  edges.forEach(e=>{deg.set(e.source,deg.get(e.source)+1); deg.set(e.target,deg.get(e.target)+1);});
  const orph = nodes.filter(n=>!deg.get(n.id)).map(n=>n.name||n.service);
  if (orph.length) warns.push(`Sin ninguna conexión: ${orph.join(', ')}`);
  const unk = [...new Set(nodes.map(n=>n.service).filter(s=>s && !SVC_SET.has(s)))];
  if (unk.length) warns.push(`Fuera del catálogo (icono genérico): ${unk.join(', ')}`);
  return {nodes, edges, warns};
}

/* ── layout por capas: x = profundidad, y = orden dentro de la capa ── */
function layout(nodes, edges){
  const idx = new Map(nodes.map((n,i)=>[n.id,i]));
  const pred = nodes.map(()=>[]), succ = nodes.map(()=>[]);
  edges.forEach(e=>{
    const s=idx.get(e.source), t=idx.get(e.target);
    if(s===undefined||t===undefined||s===t) return;
    succ[s].push(t); pred[t].push(s);
  });
  // Relajación acotada al número de nodos: converge en un DAG y no se cuelga
  // si el grafo tiene ciclos, que en una pizarra pasa seguido.
  const lay = nodes.map(()=>0);
  for(let it=0; it<nodes.length; it++){
    let moved=false;
    nodes.forEach((_,i)=> pred[i].forEach(p=>{
      if(lay[p]+1>lay[i]){ lay[i]=lay[p]+1; moved=true; }
    }));
    if(!moved) break;
  }
  const maxL = Math.max(0,...lay);
  const cols = Array.from({length:maxL+1},()=>[]);
  nodes.forEach((_,i)=>cols[lay[i]].push(i));
  // barycenter: dos pasadas alcanzan para desenredar grafos de 6-15 nodos
  const pos = nodes.map(()=>0);
  cols.forEach(c=>c.forEach((n,k)=>pos[n]=k));
  for(let s=0;s<3;s++){
    cols.forEach((col,ci)=>{
      if(!ci) return;
      col.sort((a,b)=>{
        const ba = pred[a].length? pred[a].reduce((x,p)=>x+pos[p],0)/pred[a].length : pos[a];
        const bb = pred[b].length? pred[b].reduce((x,p)=>x+pos[p],0)/pred[b].length : pos[b];
        return ba-bb;
      });
      col.forEach((n,k)=>pos[n]=k);
    });
  }
  const CW=230, RH=132, PAD=46;
  const tallest = Math.max(1,...cols.map(c=>c.length));
  const xy = nodes.map(()=>({x:0,y:0}));
  cols.forEach((col,ci)=> col.forEach((n,k)=>{
    xy[n].x = PAD + ci*CW;
    xy[n].y = PAD + (tallest-col.length)*RH/2 + k*RH;
  }));
  return {xy, w: PAD*2 + Math.max(0,maxL)*CW + 150, h: PAD*2 + (tallest-1)*RH + 84};
}

const esc = s => String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

function renderSVG(g){
  const {nodes, edges} = g;
  if(!nodes.length) return '<div style="padding:22px;color:var(--ink2)">Sin nodos.</div>';
  const {xy, w, h} = layout(nodes, edges);
  const idx = new Map(nodes.map((n,i)=>[n.id,i]));
  const S=58, out=[];
  out.push(`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">`);
  const used=[...new Set(edges.map(e=>e.flow_id%FLOW.length))];
  out.push('<defs>'+used.map(f=>`<marker id="a${f}" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="${FLOW[f]}"/></marker>`).join('')+'</defs>');

  edges.forEach(e=>{
    const s=idx.get(e.source), t=idx.get(e.target);
    if(s===undefined||t===undefined) return;
    const c=FLOW[e.flow_id%FLOW.length];
    const a=xy[s], b=xy[t];
    let d;
    if(s===t){
      d=`M${a.x+S/2},${a.y-S/2} c 42,-34 82,10 32,26`;
    } else if(Math.abs(a.x-b.x)<2){
      const dir = b.y>a.y?1:-1, off=Math.max(64,Math.abs(b.y-a.y)/2);
      d=`M${a.x},${a.y+dir*S/2} C${a.x+off},${a.y+dir*S/2} ${b.x+off},${b.y-dir*S/2} ${b.x},${b.y-dir*S/2}`;
    } else {
      const x1=a.x+(b.x>a.x?S/2:-S/2), x2=b.x+(b.x>a.x?-S/2-6:S/2+6);
      const m=(x1+x2)/2;
      d=`M${x1},${a.y} C${m},${a.y} ${m},${b.y} ${x2},${b.y}`;
    }
    out.push(`<path d="${d}" fill="none" stroke="${c}" stroke-width="2" marker-end="url(#a${e.flow_id%FLOW.length})" opacity=".85"><title>${esc(e.notes||e.type)}</title></path>`);
    if(e.seq){
      out.push(`<text x="${(xy[s].x+xy[t].x)/2}" y="${(xy[s].y+xy[t].y)/2-6}" font-size="10.5" fill="${c}" text-anchor="middle" font-family="ui-monospace,monospace">${esc(e.seq)}</text>`);
    }
  });

  nodes.forEach((n,i)=>{
    const {x,y}=xy[i];
    const stem = SVC_ICON[n.service] || '';
    const uri = ICONS[stem] || ICONS['user'] || '';
    out.push(`<g><title>${esc(n.service)}${n.notes?' — '+esc(n.notes):''}</title>`);
    if(uri) out.push(`<image href="${uri}" x="${x-S/2}" y="${y-S/2}" width="${S}" height="${S}"/>`);
    else out.push(`<rect x="${x-S/2}" y="${y-S/2}" width="${S}" height="${S}" rx="9" fill="#cbd5e0"/>`);
    const lbl=(n.name||n.service||'?').slice(0,26);
    out.push(`<text x="${x}" y="${y+S/2+15}" font-size="11.5" text-anchor="middle" fill="currentColor" font-family="system-ui,sans-serif">${esc(lbl)}</text>`);
    if(n.name && n.service && n.name!==n.service)
      out.push(`<text x="${x}" y="${y+S/2+28}" font-size="10" text-anchor="middle" fill="currentColor" opacity=".55" font-family="system-ui,sans-serif">${esc(n.service.slice(0,26))}</text>`);
    out.push('</g>');
  });
  out.push('</svg>');
  return out.join('');
}

function drawInto(el, raw, warnEl){
  try{
    const g = normalize(raw);
    el.innerHTML = renderSVG(g);
    if(warnEl){
      warnEl.innerHTML = g.warns.length
        ? `<div class="warn"><b>${g.warns.length} aviso(s)</b><ul>${g.warns.map(w=>'<li>'+esc(w)+'</li>').join('')}</ul></div>` : '';
    }
    return g;
  }catch(err){
    el.innerHTML='';
    if(warnEl) warnEl.innerHTML = `<div class="warn bad"><b>No se pudo renderizar:</b> ${esc(err.message)}</div>`;
    return null;
  }
}

const TEMPLATE = {entities:[{service:"",name:"",type:"",rationale:""}],
                  visual_connections:[{source_label:"",target_label:"",
                                       arrow_direction:"right",description:""}]};

const store = {
  get(v){ try{ return JSON.parse(localStorage.getItem(KEY(v))||'{}'); }catch{ return {}; } },
  set(v,o){ localStorage.setItem(KEY(v), JSON.stringify(o)); }
};

const cards = document.getElementById('cards');
D.videos.forEach(v=>{
  const saved = store.get(v.id);
  const has = !!v.wm;
  const el = document.createElement('div');
  el.className='card'; el.dataset.has = has?'has':'miss'; el.dataset.panel=v.panel;
  el.innerHTML = `
    <h2><a href="${v.link}" target="_blank" rel="noopener">${esc(v.title)}</a></h2>
    <div class="meta">
      <code>${v.id}</code>
      <span class="pill ${v.panel===14?'p14':''}">panel ${v.panel===14?'14':'+16'}</span>
      <span class="pill ${has?'has':'miss'}">${has?'trampa hecha':'sin trampa'}</span>
      <span>${esc(v.categories)}</span>
      <a href="${v.link}" target="_blank" rel="noopener">ver video ↗</a>
    </div>
    <div class="grid">
      <div class="panel">
        <div class="hd"><span>Pizarra · mejor frame</span><span>${v.img_w}×${v.img_h}</span></div>
        <img src="${v.img}" alt="pizarra ${v.id}" data-zoom>
      </div>
      <div class="panel">
        <div class="hd"><span>Cloudscape (ground truth)</span>
          <span>${v.gt.nodes.length} nodos · ${v.gt.edges.length} aristas</span></div>
        <div class="gbox" data-gt></div>
      </div>
    </div>
    <div class="editor">
      <div class="row">
        <b style="font-size:13.5px">World Model — editá y renderizá</b>
        <button data-render class="primary">Renderizar</button>
        <button data-reset>Restaurar original</button>
        <button data-fmt>Formatear</button>
        <button data-copy>Copiar</button>
        <span class="saved" data-saved>guardado</span>
      </div>
      <div class="grid">
        <div>
          <textarea data-json rows="18" spellcheck="false"></textarea>
          <div data-warn></div>
        </div>
        <div class="panel">
          <div class="hd"><span>Render de tu JSON</span></div>
          <div class="gbox" data-out></div>
        </div>
      </div>
    </div>
    <div class="notes">
      <b style="font-size:13.5px">Anotaciones y correcciones</b>
      <textarea data-notes rows="3" placeholder="p. ej.: DynamoDB en realidad va conectado a EKS, no solo a EC2 — la flecha apunta a la caja entera"></textarea>
    </div>`;
  cards.appendChild(el);

  const ta = el.querySelector('[data-json]');
  const outBox = el.querySelector('[data-out]');
  const warnBox = el.querySelector('[data-warn]');
  const notes = el.querySelector('[data-notes]');
  const savedTag = el.querySelector('[data-saved]');
  const original = v.wm ? JSON.stringify(v.wm, null, 2) : JSON.stringify(TEMPLATE, null, 2);

  drawInto(el.querySelector('[data-gt]'), v.gt, null);
  ta.value = saved.json ?? original;
  notes.value = saved.notes ?? '';
  if (v.wm || saved.json) drawInto(outBox, JSON.parse(ta.value||'{}'), warnBox);

  let t;
  const persist = () => {
    store.set(v.id, {json: ta.value, notes: notes.value});
    savedTag.classList.add('on');
    clearTimeout(t); t=setTimeout(()=>savedTag.classList.remove('on'), 900);
  };
  ta.addEventListener('input', persist);
  notes.addEventListener('input', persist);

  el.querySelector('[data-render]').onclick = () => {
    // Guardar también acá: pegar con el mouse dispara `input`, pero un render sin
    // haber tocado el teclado no, y perder una transcripción a mano por cerrar la
    // pestaña sería el peor error posible en esta herramienta.
    persist();
    try{ drawInto(outBox, JSON.parse(ta.value), warnBox); }
    catch(e){ warnBox.innerHTML = `<div class="warn bad"><b>JSON inválido:</b> ${esc(e.message)}</div>`; }
  };
  el.querySelector('[data-reset]').onclick = () => { ta.value = original; persist();
    try{ drawInto(outBox, JSON.parse(ta.value), warnBox); }catch{} };
  el.querySelector('[data-fmt]').onclick = () => {
    try{ ta.value = JSON.stringify(JSON.parse(ta.value), null, 2); persist(); }
    catch(e){ warnBox.innerHTML = `<div class="warn bad"><b>JSON inválido:</b> ${esc(e.message)}</div>`; }
  };
  el.querySelector('[data-copy]').onclick = () => navigator.clipboard.writeText(ta.value);
});

/* filtro */
const filter = document.getElementById('filter'), countEl = document.getElementById('count');
function applyFilter(){
  const f = filter.value; let n=0;
  document.querySelectorAll('.card').forEach(c=>{
    const ok = f==='all' || (f==='has'&&c.dataset.has==='has') ||
               (f==='miss'&&c.dataset.has==='miss') || (f==='p14'&&c.dataset.panel==='14');
    c.classList.toggle('hidden', !ok); if(ok) n++;
  });
  countEl.textContent = `${n} visibles`;
}
filter.onchange = applyFilter; applyFilter();

/* exportar / importar */
document.getElementById('expAll').onclick = () => {
  const out = {exported_at:new Date().toISOString(), videos:{}};
  D.videos.forEach(v=>{
    const s = store.get(v.id);
    if(s.json || s.notes) out.videos[v.id] = s;
  });
  const b = new Blob([JSON.stringify(out,null,2)],{type:'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(b);
  a.download = 'world_models_a_mano.json'; a.click();
};
const impFile = document.getElementById('impFile');
document.getElementById('impAll').onclick = () => impFile.click();
impFile.onchange = e => {
  const f = e.target.files[0]; if(!f) return;
  const r = new FileReader();
  r.onload = () => {
    try{
      const d = JSON.parse(r.result);
      Object.entries(d.videos||{}).forEach(([k,val])=>store.set(k,val));
      location.reload();
    }catch(err){ alert('No pude leer el archivo: '+err.message); }
  };
  r.readAsText(f);
};

/* zoom */
const lb=document.getElementById('lb'), lbimg=document.getElementById('lbimg');
document.addEventListener('click', e=>{
  if(e.target.matches('img[data-zoom]')){ lbimg.src=e.target.src; lb.classList.add('on'); }
  else if(e.target.closest('#lb')) lb.classList.remove('on');
});
document.addEventListener('keydown', e=>{ if(e.key==='Escape') lb.classList.remove('on'); });
</script></body></html>
"""


if __name__ == "__main__":
    main()
