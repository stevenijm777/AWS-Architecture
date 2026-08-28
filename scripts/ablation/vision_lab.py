#!/usr/bin/env python3
"""
vision_lab.py — Banco de trabajo para los World Models hechos a mano.

Por qué es un servidor y no un HTML suelto
------------------------------------------
La primera versión dibujaba los grafos en el navegador con un layout propio, y
se veía mal: el lienzo salía mucho más grande que su caja y arrancaba
desplazado, así que el panel parecía vacío. Las imágenes que ya usaba
`reporte_14_videos.html` se leen bastante mejor, y las produce
`graph_renderer/render_graph.mjs` (Cytoscape + klay + canvas).

Ese renderizador es Node y necesita el disco, así que un archivo estático no
puede llamarlo. Con un servidor local chico se consigue lo que hace falta:
arriba se comparan imágenes ya renderizadas, y abajo hay un único renderizador
al que se le pega un JSON y devuelve una imagen con exactamente el mismo
aspecto que las de la comparación.

Qué hace
--------
  1. Genera las imágenes que falten (GT, Standard, Parsimonious y la trampa
     hecha a mano) para los 30 videos del panel. Saltea las que ya existen.
  2. Sirve la página de comparación con esas imágenes.
  3. Expone /render: recibe un JSON (World Model o grafo Cloudscape), lo pasa a
     graphml, lo renderiza con el mismo motor y devuelve el PNG.
  4. Guarda las anotaciones en disco, no en el navegador.

Uso
---
    .venv/bin/python scripts/ablation/vision_lab.py
    # abre http://localhost:8765

    .venv/bin/python scripts/ablation/vision_lab.py --rerender   # rehace las imágenes
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402
from rich.console import Console  # noqa: E402

from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402

console = Console()

DATA = PROJECT_ROOT / "data"
GT_DIR = DATA / "cloudscape_gt"
LAB = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
RENDERER = PROJECT_ROOT / "graph_renderer"
GRAPHS_IN = RENDERER / "graphs_input"
GRAPHS_OUT = RENDERER / "graphs_output"
OUT_DIR = PROJECT_ROOT / "reports" / "vision_lab"
NOTES_FILE = OUT_DIR / "annotations.json"

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

# Ninguno termina en `_vision`: el renderizador le estampa una etiqueta
# "[Parsimonious]" a lo que tenga ese sufijo, y acá cada variante ya se rotula
# en la página.
VARIANTS = {
    "gt":     ("Cloudscape (ground truth)", lambda v: GT_DIR / f"{v}.graphml"),
    "std":    ("Gemini Standard",           lambda v: DATA / "graphs" / f"{v}.graphml"),
    "pars":   ("Gemini Parsimonious",       lambda v: DATA / "graphs_parsimonious" / f"{v}.graphml"),
    "manual": ("Trampa (hecha a mano)",     None),  # se construye del world_model_vision
}


# ── World Model → forma Cloudscape ───────────────────────────────────
def wm_to_cloudscape(wm: dict) -> tuple[dict, list[str]]:
    """El World Model anota flechas dibujadas, no flujos lógicos tipados.

    Cada conexión sale como una arista sin tipo. Las que referencian una etiqueta
    que no existe se descartan y se reportan, en vez de adivinar a qué apuntaban.
    """
    warns = []
    ents = wm.get("entities", []) or []
    nodes, by_label = [], {}
    for i, e in enumerate(ents):
        nid = str(i)
        nodes.append({"id": nid, "service": e.get("service", "") or "",
                      "name": e.get("name", "") or e.get("service", "") or "",
                      "notes": e.get("rationale", "") or ""})
        for key in (e.get("name", ""), e.get("service", "")):
            if key:
                by_label.setdefault(str(key), nid)
    lower = {k.lower().strip(): v for k, v in by_label.items()}

    def resolve(lbl):
        s = str(lbl or "")
        return by_label.get(s) or lower.get(s.lower().strip())

    edges = []
    for c in wm.get("visual_connections", []) or []:
        s, t = resolve(c.get("source_label")), resolve(c.get("target_label"))
        if s is None or t is None:
            warns.append(f'Conexión sin resolver: "{c.get("source_label")}" → '
                         f'"{c.get("target_label")}"')
            continue
        edges.append({"source": s, "target": t, "flow_id": 0, "seq": "",
                      "type": "data", "notes": c.get("description", "") or ""})
    return {"nodes": nodes, "edges": edges}, warns


def any_json_to_analysis(raw: dict) -> tuple[dict, list[str]]:
    """Acepta las dos formas y devuelve {nodes, edges} más los avisos."""
    o = raw
    for k in ("graph", "analysis", "world_model"):
        if isinstance(o, dict) and isinstance(o.get(k), dict):
            o = o[k]
    if isinstance(o.get("entities"), list):
        return wm_to_cloudscape(o)
    if isinstance(o.get("nodes"), list):
        warns = []
        nodes = [{"id": str(n.get("id", i)), "service": n.get("service", "") or "",
                  "name": n.get("name", "") or n.get("service", "") or "",
                  "notes": n.get("notes", "") or ""}
                 for i, n in enumerate(o["nodes"])]
        ids = {n["id"] for n in nodes}
        edges = []
        for e in o.get("edges", []) or []:
            s, t = str(e.get("source")), str(e.get("target"))
            if s not in ids or t not in ids:
                warns.append(f"Arista a un id inexistente: {s} → {t}")
                continue
            edges.append({"source": s, "target": t, "flow_id": int(e.get("flow_id", 0) or 0),
                          "seq": str(e.get("seq", "") or ""), "type": e.get("type", "") or "",
                          "notes": e.get("notes", "") or ""})
        return {"nodes": nodes, "edges": edges}, warns
    raise ValueError('No encuentro ni "entities" ni "nodes" en el JSON.')


# ── renderizado por lotes ────────────────────────────────────────────
def render_graphmls(paths: list[Path]) -> None:
    if not paths:
        return
    # En tandas: 120 rutas en un solo argv es innecesariamente frágil.
    for i in range(0, len(paths), 20):
        chunk = paths[i:i + 20]
        # RG_COMPACT reparte las capas grandes en varias columnas. Sin eso el
        # ground truth sale como una tira de un nodo de ancho y miles de píxeles
        # de alto, que dentro de una tarjeta no se lee.
        r = subprocess.run(["node", "render_graph.mjs", *[str(p) for p in chunk]],
                           cwd=RENDERER, capture_output=True, text=True,
                           env={**os.environ, "RG_COMPACT": "1"})
        if r.returncode != 0:
            console.print(f"[red]render_graph.mjs falló:[/]\n{r.stderr[-1500:]}")
            raise SystemExit(1)
        console.print(f"  [dim]{i + len(chunk)}/{len(paths)}[/]")


def ensure_images(force: bool = False) -> dict[str, dict[str, bool]]:
    """Genera las imágenes que falten. Devuelve qué variante tiene cada video."""
    GRAPHS_IN.mkdir(parents=True, exist_ok=True)
    GRAPHS_OUT.mkdir(parents=True, exist_ok=True)
    pending, avail = [], {}

    for vid in PANEL_30:
        avail[vid] = {}
        for var, (_, src) in VARIANTS.items():
            png = GRAPHS_OUT / f"{vid}_{var}.png"
            gml = GRAPHS_IN / f"{vid}_{var}.graphml"

            if var == "manual":
                wmp = LAB / vid / "world_model_vision.json"
                if not wmp.exists():
                    avail[vid][var] = False
                    continue
                if force or not png.exists() or wmp.stat().st_mtime > png.stat().st_mtime:
                    analysis, _ = wm_to_cloudscape(json.loads(wmp.read_text(encoding="utf-8")))
                    G = create_graph_from_cloudscape_json(analysis, video_id=vid)
                    nx.write_graphml(G, str(gml))
                    pending.append(gml)
                avail[vid][var] = True
                continue

            source = src(vid)
            if not source.exists():
                avail[vid][var] = False
                continue
            if force or not png.exists():
                shutil.copyfile(source, gml)
                pending.append(gml)
            avail[vid][var] = True

    if pending:
        console.print(f"[bold]Renderizando {len(pending)} grafos…[/] "
                      f"[dim](solo los que faltaban)[/]")
        render_graphmls(pending)
    else:
        console.print("[dim]Todas las imágenes ya estaban generadas.[/]")

    for vid in PANEL_30:
        for var in VARIANTS:
            if avail[vid].get(var) and not (GRAPHS_OUT / f"{vid}_{var}.png").exists():
                avail[vid][var] = False
    return avail


STATS_TAG = "__stats__"


def render_json_to_png(raw: dict) -> tuple[bytes, list[str]]:
    """JSON → graphml → PNG, con el mismo motor que las imágenes de arriba."""
    analysis, warns = any_json_to_analysis(raw)
    if not analysis["nodes"]:
        raise ValueError("El JSON no tiene ni un nodo.")

    # Nombre único por pedido: el servidor atiende en hilos, y dos renders
    # simultáneos sobre el mismo archivo se pisarían.
    name = f"adhoc_{uuid.uuid4().hex[:10]}"
    gml = GRAPHS_IN / f"{name}.graphml"
    png = GRAPHS_OUT / f"{name}.png"
    try:
        G = create_graph_from_cloudscape_json(analysis, video_id=name)
        nx.write_graphml(G, str(gml))
        render_graphmls([gml])
        if not png.exists():
            raise ValueError("El renderizador no produjo imagen.")
        data = png.read_bytes()
    finally:
        png.unlink(missing_ok=True)
        gml.unlink(missing_ok=True)

    stats = f"{G.number_of_nodes()} nodos · {G.number_of_edges()} aristas"
    return data, warns + [STATS_TAG + stats]


# ── datos de la página ───────────────────────────────────────────────
def build_index(avail: dict) -> list[dict]:
    out = []
    for vid in PANEL_30:
        g = nx.read_graphml(GT_DIR / f"{vid}.graphml")
        wmp = LAB / vid / "world_model_vision.json"
        out.append({
            "id": vid,
            "panel": 14 if vid in PANEL_14 else 16,
            "title": g.graph.get("name", "") or vid,
            "link": g.graph.get("link", "") or f"https://www.youtube.com/watch?v={vid}",
            "categories": g.graph.get("categories", ""),
            "gt_n": g.number_of_nodes(), "gt_e": g.number_of_edges(),
            "has_manual": bool(wmp.exists()),
            "wm": json.loads(wmp.read_text(encoding="utf-8")) if wmp.exists() else None,
            "avail": avail[vid],
        })
    return out


def load_notes() -> dict:
    if NOTES_FILE.exists():
        try:
            return json.loads(NOTES_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_notes(d: dict) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    NOTES_FILE.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


# ── servidor ─────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    index: list[dict] = []
    notes_lock = threading.Lock()

    def log_message(self, *a):  # silencio: el ruido de acceso no aporta acá
        pass

    def _send(self, code, ctype, body: bytes, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path: Path, ctype: str):
        if not path.exists():
            self._send(404, "text/plain; charset=utf-8", b"no encontrado")
            return
        self._send(200, ctype, path.read_bytes())

    def do_GET(self):
        p = urlparse(self.path).path
        if p == "/" or p == "/tool":
            html = PAGE.replace("/*__DATA__*/", json.dumps(
                {"videos": self.index, "notes": load_notes()}, ensure_ascii=False))
            # /tool: sólo el renderizador, sin las 30 tarjetas de comparación arriba —
            # para pegar un JSON y verlo sin scrollear cada vez.
            if p == "/tool":
                html = html.replace('id="cards"', 'id="cards" class="hidden"')
                html = html.replace('class="bar"', 'class="bar hidden"')
                html = html.replace(
                    '<div class="sub">Panel de 30 videos.',
                    '<div class="sub"><a href="/">← volver al panel completo</a> · '
                    'Panel de 30 videos.')
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
        elif p.startswith("/img/"):
            self._file(GRAPHS_OUT / Path(p[5:]).name, "image/png")
        elif p.startswith("/wb/"):
            vid = Path(p[4:]).stem
            self._file(LAB / vid / "best_whiteboard.jpg", "image/jpeg")
        elif p == "/notes":
            self._send(200, "application/json; charset=utf-8",
                       json.dumps(load_notes()).encode("utf-8"))
        else:
            self._send(404, "text/plain; charset=utf-8", b"no encontrado")

    def do_POST(self):
        p = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n) if n else b"{}"
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception as e:
            self._send(400, "application/json; charset=utf-8",
                       json.dumps({"error": f"JSON inválido: {e}"}).encode("utf-8"))
            return

        if p == "/render":
            try:
                png, warns = render_json_to_png(payload.get("json", {}))
            except Exception as e:
                self._send(200, "application/json; charset=utf-8",
                           json.dumps({"error": str(e)}, ensure_ascii=False).encode("utf-8"))
                return
            import base64
            self._send(200, "application/json; charset=utf-8", json.dumps({
                "png": "data:image/png;base64," + base64.b64encode(png).decode(),
                "warns": [w for w in warns if not w.startswith(STATS_TAG)],
                "stats": next((w[len(STATS_TAG):] for w in warns
                               if w.startswith(STATS_TAG)), ""),
            }, ensure_ascii=False).encode("utf-8"))

        elif p == "/notes":
            with self.notes_lock:
                cur = load_notes()
                cur[payload["id"]] = payload.get("text", "")
                save_notes(cur)
            self._send(200, "application/json", b'{"ok":true}')

        elif p == "/save_wm":
            vid = payload.get("id")
            wm_data = payload.get("json")
            if not vid or not wm_data:
                self._send(400, "application/json", b'{"error":"Falta id o json"}')
                return
            try:
                vdir = LAB / vid
                vdir.mkdir(parents=True, exist_ok=True)
                wmp = vdir / "world_model_vision.json"
                wmp.write_text(json.dumps(wm_data, indent=2, ensure_ascii=False), encoding="utf-8")
                
                # Regenerar imagen manual
                analysis, warns = wm_to_cloudscape(wm_data)
                G = create_graph_from_cloudscape_json(analysis, video_id=vid)
                gml = GRAPHS_IN / f"{vid}_manual.graphml"
                nx.write_graphml(G, str(gml))
                render_graphmls([gml])
                
                # Actualizar índice en memoria
                for item in self.index:
                    if item["id"] == vid:
                        item["has_manual"] = True
                        item["wm"] = wm_data
                        item["avail"]["manual"] = True
                        break
                
                self._send(200, "application/json; charset=utf-8",
                           json.dumps({"ok": True, "message": f"Guardado y renderizado {vid}"}).encode("utf-8"))
            except Exception as e:
                self._send(500, "application/json; charset=utf-8",
                           json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self._send(404, "text/plain; charset=utf-8", b"no encontrado")


PAGE = r"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Banco de trabajo · World Models a mano</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#f4f6f9;--card:#fff;--ink:#0f1419;--ink2:#5b6878;--line:#dde2ea;
 --accent:#3b7dd8;--accent-soft:rgba(59,125,216,.10);--ok:#22875a;--ok-soft:rgba(34,135,90,.10);
 --warn:#b07a1b;--warn-soft:rgba(176,122,27,.10);--bad:#c53030;--bad-soft:rgba(197,48,48,.10);
 --code:#f0f2f5;--shadow:0 1px 3px rgba(0,0,0,.06);
 --gradient:linear-gradient(135deg,#3b7dd8 0%,#6c5ce7 100%);
 --trampa:#d97706;--trampa-soft:rgba(217,119,6,.08);--trampa-border:rgba(217,119,6,.35)}
@media(prefers-color-scheme:dark){:root{--bg:#0e1117;--card:#161b22;--ink:#e6edf3;
 --ink2:#8b949e;--line:#30363d;--accent:#79b8ff;--accent-soft:rgba(121,184,255,.10);
 --ok:#56d364;--ok-soft:rgba(86,211,100,.08);--warn:#e3b341;--warn-soft:rgba(227,179,65,.08);
 --bad:#f85149;--bad-soft:rgba(248,81,73,.08);--code:#0d1117;
 --shadow:0 1px 3px rgba(0,0,0,.3);
 --gradient:linear-gradient(135deg,#79b8ff 0%,#b392f0 100%);
 --trampa:#f59e0b;--trampa-soft:rgba(245,158,11,.08);--trampa-border:rgba(245,158,11,.30)}}
*{box-sizing:border-box;margin:0}
body{background:var(--bg);color:var(--ink);
 font:15px/1.6 'Inter',system-ui,-apple-system,"Segoe UI",sans-serif;
 -webkit-font-smoothing:antialiased}
.wrap{max-width:1920px;margin:0 auto;padding:24px 28px}

/* ── Header ── */
.header{margin-bottom:6px}
h1{font-size:24px;font-weight:700;letter-spacing:-.02em;
 background:var(--gradient);-webkit-background-clip:text;-webkit-text-fill-color:transparent;
 background-clip:text;display:inline-block}
.sub{color:var(--ink2);font-size:14px;margin-bottom:18px;line-height:1.5}
.sub a{color:var(--accent);text-decoration:none;font-weight:500}
.sub a:hover{text-decoration:underline}

/* ── Sticky bar ── */
.bar{display:flex;gap:8px;align-items:center;flex-wrap:wrap;position:sticky;top:0;
 background:color-mix(in srgb,var(--bg) 85%,transparent);
 backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);
 padding:12px 0;z-index:30;border-bottom:1px solid var(--line);margin-bottom:20px}

/* ── Buttons ── */
button,select{font:inherit;font-size:13px;font-weight:500;padding:7px 14px;
 border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);
 cursor:pointer;transition:all .15s ease;box-shadow:var(--shadow)}
button:hover{border-color:var(--accent);background:var(--accent-soft)}
button:active{transform:scale(.97)}
button.primary{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600;
 box-shadow:0 2px 8px rgba(59,125,216,.25)}
button.primary:hover{filter:brightness(1.08);box-shadow:0 4px 12px rgba(59,125,216,.35)}
select{appearance:none;padding-right:28px;
 background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 4.5L6 7.5L9 4.5' fill='none' stroke='%235b6878' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
 background-repeat:no-repeat;background-position:right 8px center}

/* ── Pills ── */
.pill{padding:3px 10px;border-radius:99px;font-size:11.5px;font-weight:600;
 border:1px solid var(--line);letter-spacing:.02em;text-transform:uppercase}
.pill.has{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}
.pill.miss{color:var(--warn);border-color:var(--warn);background:var(--warn-soft)}
.pill.p14{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}

/* ── Cards ── */
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;
 padding:18px;margin-bottom:22px;box-shadow:var(--shadow);transition:box-shadow .2s ease}
.card:hover{box-shadow:0 4px 16px rgba(0,0,0,.08)}
.card h2{font-size:17px;font-weight:600;margin-bottom:4px;letter-spacing:-.01em}
.card h2 a{color:var(--ink);text-decoration:none;transition:color .15s}
.card h2 a:hover{color:var(--accent)}
.meta{color:var(--ink2);font-size:12.5px;margin-bottom:14px;display:flex;gap:8px;
 flex-wrap:wrap;align-items:center}
.meta code{font-family:'JetBrains Mono',ui-monospace,monospace;font-size:11.5px;
 background:var(--code);padding:2px 7px;border-radius:5px;border:1px solid var(--line)}
.meta a{color:var(--accent);text-decoration:none;font-weight:500}
.meta a:hover{text-decoration:underline}

/* ── Action buttons row (below meta) ── */
.card-actions{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.card-actions button{font-size:12px;padding:5px 12px;border-radius:7px}

/* ── Trampa JSON button — prominente ── */
.btn-trampa{background:var(--trampa-soft)!important;border-color:var(--trampa-border)!important;
 color:var(--trampa)!important;font-weight:600!important;position:relative}
.btn-trampa:hover{background:var(--warn-soft)!important;border-color:var(--trampa)!important}
.btn-trampa .badge{display:inline-block;background:var(--trampa);color:#fff;font-size:9px;
 padding:1px 5px;border-radius:99px;margin-left:6px;vertical-align:middle;font-weight:700;
 letter-spacing:.03em}
.btn-toggle-imgs{position:relative}
.btn-toggle-imgs .chevron{display:inline-block;transition:transform .2s ease;margin-right:4px;font-size:10px}
.btn-toggle-imgs.folded .chevron{transform:rotate(-90deg)}

/* ── Images section — smooth collapse ── */
.wb{margin-bottom:12px}
.wb img{max-height:470px;object-fit:contain;background:#0e1013;border-radius:4px}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(420px,1fr));gap:12px}
figure{margin:0;border:1px solid var(--line);border-radius:10px;overflow:hidden;
 background:var(--bg);transition:transform .15s ease}
figure:hover{transform:translateY(-1px)}
figcaption{padding:7px 12px;font-size:12.5px;font-weight:600;color:var(--ink2);
 background:var(--card);border-bottom:1px solid var(--line);
 cursor:pointer;display:flex;justify-content:space-between;align-items:center;user-select:none}
figcaption:hover{color:var(--accent);background:var(--accent-soft)}
.fig-toggle{font-size:11px;opacity:.6;transition:transform .2s ease}
figure.fig-collapsed .fig-toggle{transform:rotate(-90deg)}
figure.fig-collapsed img,
figure.fig-collapsed>div:not(figcaption){display:none}
figure.fig-collapsed{min-height:auto!important}
figure.fig-collapsed figcaption{border-bottom:none}
figure img{width:100%;display:block;cursor:zoom-in;background:#fff}
figure.none{display:flex;align-items:center;justify-content:center;min-height:150px;
 color:var(--ink2);font-size:13px;flex-direction:column;gap:6px}
figure.none.fig-collapsed{min-height:auto;display:block}
/* Smooth collapse animation */
.imgs{overflow:hidden;transition:max-height .35s ease,opacity .25s ease;
 max-height:5000px;opacity:1}
.imgs.collapsed{max-height:0!important;opacity:0;margin:0;padding:0}
/* Copy button in wmbox */
.btn-copy{font-size:11px;padding:3px 10px;border-radius:5px;cursor:pointer;
 background:var(--accent);color:#fff;border:none;font-weight:600;margin-left:auto;
 transition:all .15s ease}
.btn-copy:hover{filter:brightness(1.1)}
.btn-copy.copied{background:var(--ok)}

/* ── World Model JSON viewer ── */
.wmbox{margin-bottom:14px;border:2px solid var(--trampa-border);border-radius:10px;
 overflow:hidden;background:var(--card);box-shadow:0 2px 8px rgba(217,119,6,.08)}
.wmbox.collapsed{max-height:0;opacity:0;overflow:hidden;margin:0;border:0;
 transition:max-height .3s ease,opacity .2s ease,margin .3s ease}
.wmbox:not(.collapsed){max-height:3000px;opacity:1;
 transition:max-height .4s ease,opacity .3s ease .1s}
.wmbox .wm-header{padding:10px 14px;background:var(--trampa-soft);
 border-bottom:1px solid var(--trampa-border);display:flex;align-items:center;gap:10px}
.wmbox .wm-header .wm-icon{font-size:16px}
.wmbox .wm-header .wm-title{font-weight:600;font-size:13.5px;color:var(--trampa)}
.wmbox .wm-header .wm-hint{font-size:12px;color:var(--ink2);font-style:italic}
.wmbox table{width:100%;border-collapse:collapse;font-size:12.5px}
.wmbox th{text-align:left;padding:8px 12px;background:var(--code);color:var(--ink2);
 font-weight:600;font-size:11.5px;text-transform:uppercase;letter-spacing:.04em;
 border-bottom:1px solid var(--line);position:sticky;top:0}
.wmbox td{padding:7px 12px;border-bottom:1px solid var(--line);vertical-align:top}
.wmbox tr:last-child td{border-bottom:0}
.wmbox tr:hover td{background:var(--accent-soft)}
.wmbox code{font-family:'JetBrains Mono',ui-monospace,monospace;
 background:var(--code);padding:2px 6px;border-radius:4px;font-size:11.5px}
.wmbox .sec{padding:8px 12px;background:var(--code);font-weight:600;font-size:12.5px;
 border-bottom:1px solid var(--line);border-top:1px solid var(--line);
 display:flex;align-items:center;gap:6px}
.wmbox .sec .sec-icon{font-size:13px}
.wmbox .rat{color:var(--ink2);font-style:italic;font-size:12px;line-height:1.5}
.wmbox details{border-top:1px solid var(--line)}
.wmbox details summary{padding:8px 12px;cursor:pointer;font-size:12.5px;font-weight:600;
 color:var(--ink2);transition:color .15s}
.wmbox details summary:hover{color:var(--accent)}
.wmbox pre{margin:0;border:0;border-radius:0;max-height:420px;overflow:auto}

/* ── Notes ── */
.notes{margin-top:14px}
.notes b{font-size:13.5px;font-weight:600}
.notes textarea{width:100%;min-height:64px;font:14px/1.55 'Inter',system-ui,sans-serif;padding:10px;
 border:1px solid var(--line);border-radius:9px;background:var(--code);color:var(--ink);
 resize:vertical;transition:border-color .15s;margin-top:6px}
.notes textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
.saved{color:var(--ok);font-size:12px;font-weight:600;opacity:0;transition:opacity .25s;margin-left:8px}
.saved.on{opacity:1}

/* ── Tool section ── */
#tool{background:var(--card);border:2px solid var(--accent);border-radius:14px;
 padding:22px;margin:34px 0 24px;box-shadow:0 4px 20px rgba(59,125,216,.10)}
#tool h2{margin:0 0 4px;font-size:20px;font-weight:700;letter-spacing:-.02em}
.tgrid{display:grid;grid-template-columns:minmax(340px,1fr) minmax(340px,1.25fr);gap:18px;margin-top:14px}
@media(max-width:1000px){.tgrid{grid-template-columns:1fr}}
#tool textarea{width:100%;min-height:420px;
 font:12.5px/1.5 'JetBrains Mono',ui-monospace,Menlo,monospace;
 padding:12px;border:1px solid var(--line);border-radius:9px;background:var(--code);
 color:var(--ink);resize:vertical;transition:border-color .15s}
#tool textarea:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft)}
#outWrap{border:1px solid var(--line);border-radius:10px;background:#fff;min-height:420px;
 display:flex;align-items:center;justify-content:center;overflow:auto}
@media(prefers-color-scheme:dark){#outWrap{background:#1a1d23}}
#outWrap img{max-width:100%;display:block;cursor:zoom-in}
#outWrap .ph{color:var(--ink2);font-size:13.5px;padding:20px;text-align:center}

/* ── Warnings ── */
.warn{margin-top:10px;padding:10px 13px;border-radius:8px;font-size:13px;
 background:var(--warn-soft);border:1px solid var(--warn)}
.warn.bad{background:var(--bad-soft);border-color:var(--bad)}
.warn ul{margin:5px 0 0 18px;padding:0}

/* ── Smooth Toast Notification ── */
.toast{position:fixed;bottom:20px;right:20px;background:var(--ok);color:#fff;
 padding:12px 20px;border-radius:10px;font-weight:600;font-size:14px;z-index:200;
 box-shadow:0 4px 16px rgba(0,0,0,.2);opacity:0;transform:translateY(10px);
 transition:all .25s ease;pointer-events:none}
.toast.show{opacity:1;transform:translateY(0)}

/* ── Docs ── */
details.doc{background:var(--bg);border:1px solid var(--line);border-radius:10px;
 padding:12px 16px;margin-top:14px}
details.doc summary{cursor:pointer;font-weight:600;font-size:13.5px;transition:color .15s}
details.doc summary:hover{color:var(--accent)}
pre{background:var(--code);border:1px solid var(--line);border-radius:9px;padding:12px;
 overflow-x:auto;font:12px/1.5 'JetBrains Mono',ui-monospace,Menlo,monospace}

/* ── Lightbox ── */
#lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;z-index:100;
 overflow:auto;cursor:zoom-out;backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px)}
#lb img{display:block;margin:auto;background:#fff;border-radius:4px;max-height:95vh;max-width:95vw}
#lb.on{display:flex;align-items:center;justify-content:center;animation:fadeIn .15s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

.hidden{display:none!important}
</style></head><body>
<div class="wrap">
<div class="header">
  <h1>Banco de trabajo · World Models a mano</h1>
</div>
<div class="sub">Panel de 30 videos. Arriba se comparan las imágenes; abajo hay un
 renderizador al que le pegás un JSON y devuelve una imagen con el mismo motor.</div>

<div class="bar">
  <select id="filter">
    <option value="all">Todos (30)</option>
    <option value="has">Con trampa hecha</option>
    <option value="miss">Sin trampa — por hacer</option>
    <option value="p14">Solo el panel de 14</option>
  </select>
  <button id="goTool">Ir al renderizador ↓</button>
  <a href="/tool" style="font-size:13px;color:var(--accent);text-decoration:none;font-weight:500">renderizador solo ↗</a>
  <button id="collapseAll">⊟ Plegar todas las imágenes</button>
  <button id="exp">⬇ Exportar anotaciones</button>
  <span id="count" class="pill"></span>
  <span class="pill" style="color:var(--ink2)">📁 anotaciones guardadas en disco</span>
</div>

<div id="cards"></div>

<div id="tool">
  <h2>🔧 Renderizador de grafos</h2>
  <div class="sub" style="margin:0">Pegá un World Model o un grafo Cloudscape y
    obtené la imagen — mismo motor que las de arriba, así que se ven igual.</div>
  <div class="tgrid">
    <div>
      <div style="display:flex;gap:8px;margin-bottom:10px;flex-wrap:wrap;align-items:center">
        <button id="render" class="primary">▶ Renderizar</button>
        <button id="fmt">{ } Formatear</button>
        <button id="clear">✕ Limpiar</button>
        <button id="dl">⬇ Descargar PNG</button>
        <div style="margin-left:auto;display:flex;gap:6px;align-items:center">
          <select id="saveTarget" style="font-size:12px;padding:5px 10px"></select>
          <button id="saveWmBtn" class="btn-trampa" style="font-size:12px;padding:6px 12px">💾 Guardar como trampa</button>
        </div>
        <span id="stats" class="pill" style="color:var(--ink2)"></span>
      </div>
      <textarea id="src" spellcheck="false" placeholder='Pegá acá el JSON…'></textarea>
      <div id="twarn"></div>
      <details class="doc"><summary>📋 Formatos que acepta</summary>
        <p style="margin:10px 0 6px"><b>1 · World Model</b> — el que recibe Stage 2. Las conexiones van por
           <code>name</code> o <code>service</code>, no por índice.</p>
<pre>{
  "entities": [
    {"service":"S3","name":"S3","type":"S3","rationale":"bucket arriba a la izquierda"},
    {"service":"StepFunctions","name":"STEP FUNCTIONS","type":"StepFunctions","rationale":"caja central"}
  ],
  "visual_connections": [
    {"source_label":"S3","target_label":"STEP FUNCTIONS",
     "arrow_direction":"right","description":"flecha sólida"}
  ]
}</pre>
        <p style="margin:10px 0 6px"><b>2 · Grafo Cloudscape</b> — el del ground truth y la salida de Stage 2.
           Las aristas van por <code>id</code>; el color sigue el <code>flow_id</code>.</p>
<pre>{
  "nodes": [{"id":"0","service":"S3","name":"","notes":""},
            {"id":"1","service":"StepFunctions","name":"","notes":""}],
  "edges": [{"source":"0","target":"1","flow_id":0,"seq":"1","type":"data","notes":""}]
}</pre>
      </details>
    </div>
    <div id="outWrap"><div class="ph">La imagen aparece acá.</div></div>
  </div>
</div>
</div>
<div id="lb"><img id="lbimg" alt=""></div>
<div id="toast" class="toast"></div>

<script type="application/json" id="payload">/*__DATA__*/</script>
<script>
const D=JSON.parse(document.getElementById('payload').textContent);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const LABEL={gt:'Cloudscape (ground truth)',std:'Gemini Standard',
             pars:'Gemini Parsimonious',manual:'Trampa (hecha a mano)'};
const cards=document.getElementById('cards');
const saveTarget=document.getElementById('saveTarget');

// Llenar selector de videos en el renderizador
D.videos.forEach(v=>{
  const opt=document.createElement('option');
  opt.value=v.id;
  opt.textContent=`${v.id} — ${v.title.slice(0,35)}`;
  saveTarget.appendChild(opt);
});

function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),3000);
}

D.videos.forEach(v=>{
  const figs=['gt','std','pars','manual'].map(k=>{
    if(v.avail[k]) return `<figure id="fig_${v.id}_${k}">
      <figcaption onclick="this.parentNode.classList.toggle('fig-collapsed')">
        <span>${LABEL[k]}</span><span class="fig-toggle">⊟</span>
      </figcaption>
      <img loading="lazy" src="/img/${v.id}_${k}.png?t=${Date.now()}" alt="${k}">
    </figure>`;
    const why = k==='manual' ? 'todavía no la hiciste' : 'no hay grafo generado';
    return `<figure class="none" id="fig_${v.id}_${k}">
      <figcaption onclick="this.parentNode.classList.toggle('fig-collapsed')">
        <span>${LABEL[k]}</span><span class="fig-toggle">⊟</span>
      </figcaption>
      <div style="padding:20px">sin imagen — ${why}</div>
    </figure>`;
  }).join('');
  const wmEntCount = v.wm ? (v.wm.entities||[]).length : 0;
  const wmConCount = v.wm ? (v.wm.visual_connections||[]).length : 0;
  const el=document.createElement('div');
  el.className='card'; el.id=`card_${v.id}`; el.dataset.has=v.has_manual?'has':'miss'; el.dataset.panel=v.panel;
  el.innerHTML=`
    <h2><a href="${v.link}" target="_blank" rel="noopener">${esc(v.title)}</a></h2>
    <div class="meta">
      <code>${v.id}</code>
      <span class="pill ${v.panel===14?'p14':''}">panel ${v.panel===14?'14':'+16'}</span>
      <span class="pill ${v.has_manual?'has':'miss'}">${v.has_manual?'trampa hecha':'sin trampa'}</span>
      <span>GT ${v.gt_n} nodos · ${v.gt_e} aristas</span>
      <span>${esc(v.categories)}</span>
      <a href="${v.link}" target="_blank" rel="noopener">ver video ↗</a>
    </div>
    <div class="card-actions">
      <button class="btn-toggle-imgs" data-toggle-imgs><span class="chevron">▼</span> Ocultar todas las imágenes</button>
      ${v.has_manual?`<button class="btn-trampa" data-toggle-wm>📄 Ver JSON de la trampa <span class="badge">${wmEntCount} ent · ${wmConCount} con</span></button>`:''}
      <button data-load style="font-size:12px">
        ${v.has_manual?'⚙ Cargar trampa en el renderizador':'⚙ Empezar trampa en el renderizador'}</button>
    </div>
    ${v.has_manual?`<div class="wmbox collapsed" data-wm></div>`:''}
    <div class="imgs">
      <figure class="wb" id="fig_${v.id}_wb">
        <figcaption onclick="this.parentNode.classList.toggle('fig-collapsed')">
          <span>Pizarra · mejor frame</span><span class="fig-toggle">⊟</span>
        </figcaption>
        <img loading="lazy" src="/wb/${v.id}.jpg" alt="pizarra">
      </figure>
      <div class="strip">${figs}</div>
    </div>
    <div class="notes">
      <b>Anotaciones y correcciones</b><span class="saved" data-saved>✓ guardado</span>
      <textarea data-notes placeholder="p. ej.: DynamoDB en realidad va conectado a EKS, no solo a EC2 — la flecha apunta a la caja entera"></textarea>
    </div>`;
  cards.appendChild(el);

  const ta=el.querySelector('[data-notes]'), tag=el.querySelector('[data-saved]');
  ta.value=D.notes[v.id]||'';
  let t;
  ta.addEventListener('input',()=>{
    clearTimeout(t);
    t=setTimeout(async()=>{
      await fetch('/notes',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({id:v.id,text:ta.value})});
      tag.classList.add('on'); setTimeout(()=>tag.classList.remove('on'),1200);
    },500);
  });

  /* Collapse all card images */
  const imgs=el.querySelector('.imgs'), bImgs=el.querySelector('[data-toggle-imgs]');
  bImgs.onclick=()=>{
    const willCollapse=!imgs.classList.contains('collapsed');
    if(willCollapse){
      imgs.style.maxHeight=imgs.scrollHeight+'px';
      requestAnimationFrame(()=>{
        imgs.style.maxHeight=imgs.scrollHeight+'px';
        requestAnimationFrame(()=>imgs.classList.add('collapsed'));
      });
    } else {
      imgs.classList.remove('collapsed');
      imgs.style.maxHeight=imgs.scrollHeight+'px';
      setTimeout(()=>imgs.style.maxHeight='',400);
    }
    bImgs.classList.toggle('folded',willCollapse);
    bImgs.innerHTML=willCollapse
      ?'<span class="chevron">▼</span> Mostrar todas las imágenes'
      :'<span class="chevron">▼</span> Ocultar todas las imágenes';
  };

  /* World Model JSON viewer */
  const bWm=el.querySelector('[data-toggle-wm]');
  if(bWm){
    const box=el.querySelector('[data-wm]');
    const ents=(v.wm.entities||[]).map((e,i)=>`<tr>
      <td style="color:var(--ink2);font-size:11px">${i}</td>
      <td><b>${esc(e.name||e.service)}</b></td>
      <td><code>${esc(e.service)}</code></td>
      <td>${esc(e.type)||'<span style="opacity:.4">—</span>'}</td>
      <td class="rat">${esc(e.rationale)||'<span style="opacity:.4">— sin rationale —</span>'}</td></tr>`).join('');
    const cons=(v.wm.visual_connections||[]).map((c,i)=>`<tr>
      <td style="color:var(--ink2);font-size:11px">${i}</td>
      <td><b>${esc(c.source_label)}</b> → <b>${esc(c.target_label)}</b></td>
      <td><code>${esc(c.arrow_direction)||'—'}</code></td>
      <td class="rat">${esc(c.description)||'<span style="opacity:.4">— sin descripción —</span>'}</td></tr>`).join('');
    box.innerHTML=`
      <div class="wm-header">
        <span class="wm-icon">📋</span>
        <span class="wm-title">JSON de la trampa — contexto que Stage 2 recibe pero que no aparece en la imagen</span>
      </div>
      <div class="sec"><span class="sec-icon">📦</span> ${(v.wm.entities||[]).length} entidades</div>
      <table><thead><tr><th style="width:30px">#</th><th style="width:180px">etiqueta</th>
        <th style="width:120px">service</th><th style="width:100px">type</th><th>rationale ⬅ no se ve en la imagen</th></tr></thead><tbody>${ents}</tbody></table>
      <div class="sec"><span class="sec-icon">🔗</span> ${(v.wm.visual_connections||[]).length} conexiones</div>
      <table><thead><tr><th style="width:30px">#</th><th style="width:220px">arista</th>
        <th style="width:120px">dirección</th><th>description ⬅ no se ve en la imagen</th></tr></thead><tbody>${cons}</tbody></table>
      <div class="sec" style="justify-content:space-between">
        <span>📝 JSON crudo</span>
        <button class="btn-copy" data-copy-json="${v.id}">📋 Copiar JSON al portapapeles</button>
      </div>
      <pre style="max-height:300px;overflow:auto">${esc(JSON.stringify(v.wm,null,2))}</pre>`;
    bWm.onclick=()=>{
      const off=box.classList.toggle('collapsed');
      bWm.innerHTML=off
        ?`📄 Ver JSON de la trampa <span class="badge">${wmEntCount} ent · ${wmConCount} con</span>`
        :`📄 Ocultar JSON de la trampa`;
    };

    /* Copy JSON to clipboard */
    const copyBtn=box.querySelector('[data-copy-json]');
    if(copyBtn){
      copyBtn.onclick=(e)=>{
        e.stopPropagation();
        const jsonStr=JSON.stringify(v.wm,null,2);
        navigator.clipboard.writeText(jsonStr).then(()=>{
          copyBtn.textContent='✓ Copiado!';
          copyBtn.classList.add('copied');
          setTimeout(()=>{
            copyBtn.textContent='📋 Copiar JSON al portapapeles';
            copyBtn.classList.remove('copied');
          },2000);
        });
      };
    }
  }

  el.querySelector('[data-load]').onclick=()=>{
    const tpl={entities:[{service:"",name:"",type:"",rationale:""}],
               visual_connections:[{source_label:"",target_label:"",
                                    arrow_direction:"right",description:""}]};
    src.value=JSON.stringify(v.wm||tpl,null,2);
    saveTarget.value=v.id;
    document.getElementById('tool').scrollIntoView({behavior:'smooth'});
    if(v.wm) doRender();
  };
});

/* filtro */
const filter=document.getElementById('filter'),countEl=document.getElementById('count');
function applyFilter(){
  const f=filter.value; let n=0;
  document.querySelectorAll('.card').forEach(c=>{
    const ok=f==='all'||(f==='has'&&c.dataset.has==='has')||
             (f==='miss'&&c.dataset.has==='miss')||(f==='p14'&&c.dataset.panel==='14');
    c.classList.toggle('hidden',!ok); if(ok)n++;
  });
  countEl.textContent=`${n} visibles`;
}
filter.onchange=applyFilter; applyFilter();

/* renderizador */
const src=document.getElementById('src'), outWrap=document.getElementById('outWrap');
const twarn=document.getElementById('twarn'), statsEl=document.getElementById('stats');
let lastPng=null;
async function doRender(){
  let parsed;
  try{ parsed=JSON.parse(src.value); }
  catch(e){ twarn.innerHTML=`<div class="warn bad"><b>JSON inválido:</b> ${esc(e.message)}</div>`; return; }
  outWrap.innerHTML='<div class="ph">renderizando…</div>'; twarn.innerHTML=''; statsEl.textContent='';
  try{
    const r=await fetch('/render',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({json:parsed})});
    const d=await r.json();
    if(d.error){ outWrap.innerHTML='<div class="ph">—</div>';
      twarn.innerHTML=`<div class="warn bad"><b>No se pudo renderizar:</b> ${esc(d.error)}</div>`; return; }
    lastPng=d.png;
    outWrap.innerHTML=`<img src="${d.png}" alt="grafo renderizado">`;
    statsEl.textContent=d.stats||'';
    twarn.innerHTML=d.warns.length
      ? `<div class="warn"><b>${d.warns.length} aviso(s)</b><ul>${d.warns.map(w=>'<li>'+esc(w)+'</li>').join('')}</ul></div>`:'';
  }catch(e){
    outWrap.innerHTML='<div class="ph">—</div>';
    twarn.innerHTML=`<div class="warn bad"><b>Error de red:</b> ${esc(e.message)}</div>`;
  }
}
document.getElementById('render').onclick=doRender;
document.getElementById('fmt').onclick=()=>{
  try{ src.value=JSON.stringify(JSON.parse(src.value),null,2); twarn.innerHTML=''; }
  catch(e){ twarn.innerHTML=`<div class="warn bad"><b>JSON inválido:</b> ${esc(e.message)}</div>`; }
};
document.getElementById('clear').onclick=()=>{
  src.value=''; outWrap.innerHTML='<div class="ph">La imagen aparece acá.</div>';
  twarn.innerHTML=''; statsEl.textContent=''; lastPng=null;
};
document.getElementById('dl').onclick=()=>{
  if(!lastPng) return;
  const a=document.createElement('a'); a.href=lastPng; a.download='grafo.png'; a.click();
};

// Botón para guardar trampa en disco
document.getElementById('saveWmBtn').onclick=async()=>{
  const targetId=saveTarget.value;
  let parsed;
  try{ parsed=JSON.parse(src.value); }
  catch(e){ twarn.innerHTML=`<div class="warn bad"><b>JSON inválido:</b> ${esc(e.message)}</div>`; return; }
  
  try{
    const r=await fetch('/save_wm',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({id:targetId, json:parsed})});
    const d=await r.json();
    if(d.error){
      twarn.innerHTML=`<div class="warn bad"><b>Error al guardar:</b> ${esc(d.error)}</div>`;
    } else {
      showToast(`✓ Trampa guardada y renderizada para ${targetId}`);
      // Actualizar imagen manual en el card si existe en la página
      const figManual=document.getElementById(`fig_${targetId}_manual`);
      if(figManual){
        figManual.className='';
        figManual.innerHTML=`<figcaption onclick="this.parentNode.classList.toggle('fig-collapsed')">
          <span>Trampa (hecha a mano)</span><span class="fig-toggle">⊟</span>
        </figcaption>
        <img loading="lazy" src="/img/${targetId}_manual.png?t=${Date.now()}" alt="manual">`;
      }
      doRender();
    }
  }catch(e){
    twarn.innerHTML=`<div class="warn bad"><b>Error de red:</b> ${esc(e.message)}</div>`;
  }
};

document.getElementById('goTool').onclick=()=>
  document.getElementById('tool').scrollIntoView({behavior:'smooth'});

let allFolded=false;
document.getElementById('collapseAll').onclick=e=>{
  allFolded=!allFolded;
  document.querySelectorAll('.card .imgs').forEach(x=>x.classList.toggle('collapsed',allFolded));
  document.querySelectorAll('[data-toggle-imgs]').forEach(b=>{
    b.classList.toggle('folded',allFolded);
    b.innerHTML=allFolded
      ?'<span class="chevron">▼</span> Mostrar todas las imágenes'
      :'<span class="chevron">▼</span> Ocultar todas las imágenes';
  });
  e.target.textContent=allFolded?'⊞ Desplegar todas las imágenes':'⊟ Plegar todas las imágenes';
};
src.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){ e.preventDefault(); doRender(); }
});

/* exportar anotaciones */
document.getElementById('exp').onclick=async()=>{
  const n=await (await fetch('/notes')).json();
  const b=new Blob([JSON.stringify(n,null,2)],{type:'application/json'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(b);
  a.download='anotaciones.json'; a.click();
};

/* zoom */
const lb=document.getElementById('lb'), lbimg=document.getElementById('lbimg');
document.addEventListener('click',e=>{
  if(e.target.tagName==='IMG'&&e.target.closest('figure,#outWrap')){
    lbimg.src=e.target.src; lb.classList.add('on');
  } else if(e.target.closest('#lb')) lb.classList.remove('on');
});
document.addEventListener('keydown',e=>{ if(e.key==='Escape') lb.classList.remove('on'); });
</script></body></html>
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--rerender", action="store_true",
                    help="rehace todas las imágenes aunque ya existan")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    if not shutil.which("node"):
        console.print("[bold red]✗ No encuentro `node`, y el renderizador lo necesita.[/]")
        sys.exit(1)

    avail = ensure_images(force=args.rerender)
    Handler.index = build_index(avail)

    tot = {k: sum(1 for v in avail.values() if v.get(k)) for k in VARIANTS}
    console.print(f"\n[bold]Imágenes disponibles[/] sobre {len(PANEL_30)} videos: " +
                  " · ".join(f"{k} {n}" for k, n in tot.items()))

    url = f"http://localhost:{args.port}"
    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    console.print(f"[green]▶[/] {url}   [dim](Ctrl-C para cortar)[/]")
    if not args.no_browser:
        threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        console.print("\n[dim]listo.[/]")


if __name__ == "__main__":
    main()
