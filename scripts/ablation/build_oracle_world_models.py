#!/usr/bin/env python3
"""
build_oracle_world_models.py — Brazo B del experimento del oráculo.

Qué es
------
Convierte el ground truth de Cloudscape al formato World Model que consume
Stage 2, de forma determinista y sin llamar a la API. El resultado es una
entrada *perfecta* para Stage 2: si el pipeline no la transporta hasta el final,
la pérdida es de Stage 2 y no de la visión.

Es el control de instrumento del experimento del oráculo. El brazo A (la
transcripción humana de la pizarra, `world_model_vision.json`) mide el techo
visual; sin este brazo B no se puede saber si un resultado bajo en A viene de la
pizarra o de Stage 2, así que B va primero.

Por qué el graphml y no el json
-------------------------------
`data/cloudscape_gt_json/` tiene 165 archivos y le faltan 7 videos del panel de
30. `data/cloudscape_gt/` tiene 397 graphml, los cubre a todos, y es la fuente
que ya usa el evaluador (`rerun_panel.GT_DIR`). Una sola fuente de verdad.

Etiquetas duplicadas
--------------------
`visual_connections` referencia entidades por etiqueta, no por índice, y 13 de
los grafos del panel tienen nodos que comparten etiqueta (los 2 Macie, los 2 S3
de `-kA0ahrhX3I`). Para la métrica da igual — ambos resuelven al mismo servicio
y el multiset de pares (src_service, tgt_service) se conserva — pero **no da
igual para Stage 2**: la regla 4 del prompt ("Dynamic Logical Fusion") le pide
explícitamente fusionar iconos repetidos del mismo servicio, así que dos
entidades llamadas "S3" son una invitación a emitir una sola y perder recall.

Se desambigua con el propio texto de `notes` del GT cuando existe
("S3 — Production data" / "S3 — Metadata of risky data"): queda único y además
natural. Un "#1"/"#2" sintético sería una etiqueta que Stage 1 jamás produce.

Campos sintéticos
-----------------
El GT no tiene geometría, así que `arrow_direction` queda vacío, y `rationale` /
`description` sólo copian las notas del GT — no se inventa prosa. El prompt de
Stage 2 no menciona ninguno de esos tres campos (sólo dice "use this as your
visual inventory"), así que el impacto es menor, pero queda registrado como el
cambio de distribución que es.

Uso
---
    .venv/bin/python scripts/ablation/build_oracle_world_models.py --verify
    .venv/bin/python scripts/ablation/build_oracle_world_models.py --write
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx
from rich.console import Console
from rich.table import Table

from scripts.ablation.rerun_panel import GT_DIR, LAB_WORKSPACE, PANELS

console = Console()

# Nombre propio: no pisa `world_model.json` (producción) ni
# `world_model_vision.json` (brazo A, transcrito a mano).
OUT_NAME = "world_model_oracle_gt.json"
LEDGER = PROJECT_ROOT / "ara" / "evidence" / "oracle"

# El GT prefija sus notas con etiquetas de su propio esquema.
NOTE_PREFIX = re.compile(r"^(DATA_PEEK|NAME|NOTE|LABEL)\s*:\s*", re.I)


def note_hint(notes: str) -> str:
    """El texto útil de una nota del GT, sin el prefijo de esquema."""
    return NOTE_PREFIX.sub("", (notes or "").strip()).strip()


def build_labels(G: nx.DiGraph) -> dict[str, str]:
    """Una etiqueta única por nodo, preferentemente derivada del GT y no inventada."""
    base = {n: (a.get("name") or "").strip() or a.get("service", "?")
            for n, a in G.nodes(data=True)}
    repeated = {b for b, c in Counter(base.values()).items() if c > 1}

    labels: dict[str, str] = {}
    for n, b in base.items():
        if b not in repeated:
            labels[n] = b
            continue
        hint = note_hint(G.nodes[n].get("notes", ""))
        labels[n] = f"{b} — {hint}" if hint else b

    # Si tras usar las notas siguen colisionando, recién ahí un sufijo numérico.
    seen: Counter = Counter()
    dupes = {l for l, c in Counter(labels.values()).items() if c > 1}
    for n in list(labels):
        if labels[n] in dupes:
            seen[labels[n]] += 1
            labels[n] = f"{labels[n]} #{seen[labels[n]]}"
    return labels


def gt_to_world_model(G: nx.DiGraph) -> dict:
    labels = build_labels(G)
    entities = [
        {
            "service": a.get("service", "?"),
            "name": labels[n],
            "type": a.get("service", "?"),
            "rationale": note_hint(a.get("notes", "")),
        }
        for n, a in G.nodes(data=True)
    ]
    connections = [
        {
            "source_label": labels[u],
            "target_label": labels[v],
            "arrow_direction": "",          # el GT no tiene geometría
            "description": note_hint(a.get("notes", "")),
        }
        for u, v, a in G.edges(data=True)
    ]
    return {"entities": entities, "visual_connections": connections}


# ── Verificación: la conversión tiene que ser sin pérdida ────────────
def _prf(gen: list, gt: list) -> float:
    g, t = Counter(gen), Counter(gt)
    inter = sum((g & t).values())
    p = inter / sum(g.values()) if g else 0.0
    r = inter / sum(t.values()) if t else 0.0
    return 2 * p * r / (p + r) if (p + r) else 0.0


def passthrough_scores(wm: dict, G: nx.DiGraph) -> tuple[float, float, int]:
    """Si Stage 2 copiara el World Model literalmente, ¿qué daría contra el GT?

    Usa la misma métrica que `evaluate_graphs.py`: servicios en multiset, aristas
    en multiset sobre (src_service, tgt_service) ignorando el tipo. Cualquier
    resultado distinto de 100/100 significa que el formato pierde información y
    que el experimento no tendría techo interpretable.
    """
    resolve: dict[str, str] = {}
    for e in wm["entities"]:
        for key in (e.get("name"), e.get("service")):
            if key:
                resolve.setdefault(key, e["service"])

    gen_edges, unresolved = [], 0
    for c in wm["visual_connections"]:
        s, t = resolve.get(c["source_label"]), resolve.get(c["target_label"])
        if s and t:
            gen_edges.append((s, t))
        else:
            unresolved += 1

    gt_services = [a.get("service", "?") for _, a in G.nodes(data=True)]
    gt_edges = [(G.nodes[u].get("service", "?"), G.nodes[v].get("service", "?"))
                for u, v in G.edges()]

    svc = _prf([e["service"] for e in wm["entities"]], gt_services)
    edge = _prf(gen_edges, gt_edges)
    return svc * 100, edge * 100, unresolved


def ceiling_report(panel: list[str], wm_name: str, arm: str) -> None:
    """El techo de un brazo cualquiera, sin gastar una sola llamada.

    Un World Model no puede producir un grafo mejor que él mismo: si Stage 2 lo
    copiara literalmente, éste es el resultado. Sirve de cordura previa — un brazo
    cuyo techo ya está por debajo de producción no puede ganarle, y correrlo sólo
    compra un número que se malinterpreta como "el oráculo no ayuda".
    """
    rows = []
    for vid in panel:
        wm_path = LAB_WORKSPACE / vid / wm_name
        gt_path = GT_DIR / f"{vid}.graphml"
        if not wm_path.exists() or not gt_path.exists():
            continue
        wm = json.loads(wm_path.read_text(encoding="utf-8"))
        G = nx.read_graphml(str(gt_path))
        svc, edge, unresolved = passthrough_scores(wm, G)
        rows.append({
            "video_id": vid, "svc_f1": svc, "edge_f1": edge, "unresolved": unresolved,
            "entities": len(wm.get("entities", [])),
            "connections": len(wm.get("visual_connections", [])),
            "gt_nodes": G.number_of_nodes(), "gt_edges": G.number_of_edges(),
        })

    if not rows:
        console.print(f"[bold red]🛑 Ningún video del panel tiene {wm_name}.[/]")
        sys.exit(2)

    t = Table(title=f"Techo de pass-through — brazo '{arm}' ({wm_name})", border_style="magenta")
    for col in ("video", "ent/GT", "con/GT", "Svc F1", "Edge F1", "sin resolver"):
        t.add_column(col, justify="right" if col != "video" else "left")
    for r in rows:
        t.add_row(r["video_id"], f"{r['entities']}/{r['gt_nodes']}",
                  f"{r['connections']}/{r['gt_edges']}",
                  f"{r['svc_f1']:.1f}", f"{r['edge_f1']:.1f}", str(r["unresolved"]))
    console.print(t)

    n = len(rows)
    svc = sum(r["svc_f1"] for r in rows) / n
    edge = sum(r["edge_f1"] for r in rows) / n
    console.print(f"\n[bold]Techo ({n} videos):[/] Svc F1 [green]{svc:.2f}%[/] · "
                  f"Edge F1 [green]{edge:.2f}%[/]")
    console.print("[dim]Es el máximo alcanzable si Stage 2 fuera una copia perfecta. "
                  "Comparar contra producción sobre estos mismos videos antes de correr.[/]")
    bad = [r["video_id"] for r in rows if r["unresolved"]]
    if bad:
        console.print(f"[yellow]⚠ Conexiones que no resuelven a ninguna entidad en: "
                      f"{', '.join(bad)} — son aristas perdidas por un typo, no por visión.[/]")


def main() -> None:
    ap = argparse.ArgumentParser(description="Genera los World Model oráculo (brazo B) desde el GT")
    ap.add_argument("--panel", type=int, default=30, choices=sorted(PANELS))
    ap.add_argument("--write", action="store_true",
                    help="escribe los archivos (por defecto sólo verifica)")
    ap.add_argument("--verify", action="store_true", help="sólo verifica, no escribe")
    ap.add_argument("--ceiling", metavar="NOMBRE",
                    help="no genera nada: mide el techo de pass-through de los "
                         "world_model_<NOMBRE>.json que ya existan. 'vision' da el techo del "
                         "brazo A. Si ese techo está por debajo de producción, la corrida no "
                         "puede salir bien y no vale la pena pagarla.")
    args = ap.parse_args()

    panel = PANELS[args.panel]

    if args.ceiling:
        ceiling_report(panel, f"world_model_{args.ceiling}.json", args.ceiling)
        return
    rows, written, missing = [], [], []

    for vid in panel:
        gt_path = GT_DIR / f"{vid}.graphml"
        if not gt_path.exists():
            missing.append(vid)
            continue
        G = nx.read_graphml(str(gt_path))
        wm = gt_to_world_model(G)
        svc, edge, unresolved = passthrough_scores(wm, G)

        labels = [e["name"] for e in wm["entities"]]
        rows.append({
            "video_id": vid,
            "entities": len(wm["entities"]),
            "connections": len(wm["visual_connections"]),
            "svc_f1": svc,
            "edge_f1": edge,
            "unresolved": unresolved,
            "dup_labels": len(labels) - len(set(labels)),
        })

        if args.write:
            out = LAB_WORKSPACE / vid / OUT_NAME
            out.parent.mkdir(parents=True, exist_ok=True)
            payload = json.dumps(wm, indent=2, ensure_ascii=False)
            out.write_text(payload, encoding="utf-8")
            written.append({
                "video_id": vid,
                "path": str(out.relative_to(PROJECT_ROOT)),
                "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                "entities": len(wm["entities"]),
                "connections": len(wm["visual_connections"]),
            })

    t = Table(title=f"Brazo B — conversión GT → World Model (panel de {len(panel)})",
              border_style="cyan")
    for col, just in (("video", "left"), ("ent", "right"), ("con", "right"),
                      ("Svc F1", "right"), ("Edge F1", "right"), ("sin resolver", "right"),
                      ("labels dup", "right")):
        t.add_column(col, justify=just)
    for r in rows:
        bad = r["svc_f1"] < 99.99 or r["edge_f1"] < 99.99 or r["unresolved"]
        style = "red" if bad else None
        t.add_row(r["video_id"], str(r["entities"]), str(r["connections"]),
                  f"{r['svc_f1']:.1f}", f"{r['edge_f1']:.1f}",
                  str(r["unresolved"]), str(r["dup_labels"]), style=style)
    console.print(t)

    n = len(rows)
    svc_mean = sum(r["svc_f1"] for r in rows) / n if n else 0.0
    edge_mean = sum(r["edge_f1"] for r in rows) / n if n else 0.0
    lossy = [r["video_id"] for r in rows
             if r["svc_f1"] < 99.99 or r["edge_f1"] < 99.99 or r["unresolved"]]

    console.print(f"\n[bold]Techo de pass-through ({n} videos):[/] "
                  f"Svc F1 [green]{svc_mean:.2f}%[/] · Edge F1 [green]{edge_mean:.2f}%[/]")
    if missing:
        console.print(f"[yellow]⚠ Sin graphml de GT: {', '.join(missing)}[/]")
    if lossy:
        console.print(f"[bold red]🛑 La conversión pierde información en: {', '.join(lossy)}[/]\n"
                      f"El experimento no tendría techo interpretable. No escribo nada.")
        sys.exit(2)
    console.print("[green]✓[/] Conversión sin pérdida: el techo del brazo B es 100/100, "
                  "así que todo lo que falte después es de Stage 2.")

    if not args.write:
        console.print("[dim]— verificación solamente; usá --write para escribir los archivos —[/]")
        return

    LEDGER.mkdir(parents=True, exist_ok=True)
    manifest = LEDGER / f"brazo_b_world_models_p{len(panel)}.json"
    manifest.write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "data/cloudscape_gt/<vid>.graphml",
        "output_name": OUT_NAME,
        "panel": f"{len(panel)}_videos",
        "deterministic": True,
        "api_calls": 0,
        "passthrough_ceiling": {"service_f1": round(svc_mean, 2), "edge_f1": round(edge_mean, 2)},
        "label_policy": "name o service; si repite, se desambigua con el texto de notes del GT",
        "synthetic_fields": ["arrow_direction (vacío: el GT no tiene geometría)"],
        "files": written,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    console.print(f"[green]✓[/] {len(written)} World Model escritos como "
                  f"[bold]{OUT_NAME}[/] en lab_workspace/")
    console.print(f"[green]✓[/] Manifiesto → [bold]{manifest.relative_to(PROJECT_ROOT)}[/]")


if __name__ == "__main__":
    main()
