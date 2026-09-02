#!/usr/bin/env python3
"""
parsimonious_panel.py — Corre el brazo Parsimonious sobre el panel de 30, con o sin transcript.

Qué mide
--------
El notebook 06 mostró que en Standard **quitar el transcript no derrumba el Edge F1**
(−1.52 pts = 0.46× MDE). Eso puso en duda la explicación de RQ3. La pregunta que queda es
si ese hallazgo es de la **tarea** o del **pipeline**: Standard tiene dos etapas y un World
Model intermedio que ya resumió la pizarra, así que podría estar absorbiendo la pérdida.

Parsimonious no tiene esa estructura — es **una sola llamada** con imagen + transcript — así
que es la réplica limpia. Si acá tampoco duele quitar el transcript, el hallazgo es de la
tarea y RQ3 se sostiene sobre dos arquitecturas distintas.

Por qué un runner nuevo y no el de Melissa
------------------------------------------
`run_batch_gemini_36_multikey.py` es su script de producción y no se toca. Este reusa **su
prompt** (materializado y verificado por hash en
`src/configs/prompts/parsimonious/produccion.txt`) pero agrega lo que hace falta para que
el resultado sea comparable con el resto del trabajo: panel fijo de 30, checkpoint que
retoma, evaluación con el mismo `evaluate_pair`, y un `run.json` con procedencia.

Uso
---
    .venv/bin/python scripts/ablation/parsimonious_panel.py --dry-run
    .venv/bin/python scripts/ablation/parsimonious_panel.py                  # con transcript
    .venv/bin/python scripts/ablation/parsimonious_panel.py --no-transcript  # sin transcript
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import networkx as nx
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.ablation.rerun_panel import (  # noqa: E402
    KeyRotator, QuotaExhausted, call_gemini, read_transcript,
    GOOD_WHITEBOARD_DIR, GT_DIR, PANELS,
)
from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog  # noqa: E402
from config.settings import GEMINI_API_KEYS, GEMINI_MODEL  # noqa: E402

console = Console()

PROMPT_FILE = PROJECT_ROOT / "src" / "configs" / "prompts" / "parsimonious" / "produccion.txt"
MANIFEST = PROMPT_FILE.parent / "MANIFEST.json"
SERVICES = PROJECT_ROOT / "data" / "cloudscape_gt" / "services.csv"
OUT_ROOT = PROJECT_ROOT / "reports" / "ablation"
CKPT_DIR = OUT_ROOT / ".checkpoints"


# Mismo contrato de salida que usa el runner de Melissa (response_schema).
class GraphMetadata(BaseModel):
    name: str
    link: str
    categories: str
    graph_usable: bool
    notes: str


class Node(BaseModel):
    id: str
    service: str
    name: str
    notes: str


class Edge(BaseModel):
    source: str
    target: str
    flow_id: int
    seq: str
    type: str
    notes: str


class FinalArchitectureSchema(BaseModel):
    step_by_step_reasoning: str
    graph: GraphMetadata
    nodes: list[Node]
    edges: list[Edge]


def normalizar(t: str) -> str:
    import re
    return re.sub(r"\s+", " ", t).strip()


def cargar_prompt_verificado() -> tuple[str, dict]:
    """Aborta si el .txt derivó del hash del manifiesto — misma disciplina que rerun_panel."""
    if not PROMPT_FILE.exists():
        console.print(f"[red]✗ Falta {PROMPT_FILE}[/]\n"
                      "  Corré: .venv/bin/python scripts/utils/extract_prompts_parsimonious.py")
        raise SystemExit(1)
    texto = PROMPT_FILE.read_text(encoding="utf-8")
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entrada = next((p for p in man["prompts"] if p["file"] == PROMPT_FILE.name), None)
    if entrada is None:
        console.print(f"[red]✗ {PROMPT_FILE.name} no figura en el manifiesto[/]"); raise SystemExit(1)
    real = hashlib.sha256(normalizar(texto).encode("utf-8")).hexdigest()
    if real != entrada["sha256"]:
        console.print(f"[red]✗ HASH MISMATCH en {PROMPT_FILE.name}[/]\n"
                      f"  manifiesto: {entrada['sha256'][:16]}\n  archivo   : {real[:16]}")
        raise SystemExit(1)
    return texto, entrada


def catalogos() -> tuple[str, str]:
    """Las dos listas que el prompt de Parsimonious inyecta, igual que su runner."""
    actores, aws = [], []
    with open(SERVICES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            n = (row.get("name") or "").strip()
            if not n:
                continue
            (aws if row.get("is_aws", "").strip() == "True" else actores).append(n)
    return ", ".join(dict.fromkeys(actores)), ", ".join(dict.fromkeys(aws))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-transcript", action="store_true",
                    help="corta el canal verbal: solo imagen + prompt")
    ap.add_argument("--panel", type=int, default=30, choices=sorted(PANELS))
    ap.add_argument("--model", default=GEMINI_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    panel = PANELS[args.panel]
    prompt_tmpl, entrada = cargar_prompt_verificado()
    console.print(f"[green]✓[/] Prompt verificado: [bold]{entrada['name']}[/] "
                  f"({entrada['chars']} chars, sha {entrada['sha256'][:12]})")
    console.print("[dim]  Es el que corre en producción de Parsimonious "
                  "(vision_analyzer_parsimonious.py).[/]")
    actores, aws = catalogos()
    prompt_base = (prompt_tmpl
                   .replace("<USER_ACTORS_PLACEHOLDER>", actores)
                   .replace("<ACTORS_PLACEHOLDER>", actores)
                   .replace("<AWS_SERVICES_PLACEHOLDER>", aws))

    tag = "_notranscript" if args.no_transcript else ""
    console.print(f"[bold]Condición:[/] {'SIN' if args.no_transcript else 'CON'} transcript · "
                  f"panel de {len(panel)} · arquitectura de UNA llamada\n")

    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    ckpt = CKPT_DIR / f"parsimonious_{entrada['sha256'][:12]}_{args.model}_p{args.panel}{tag}.json"
    done = json.loads(ckpt.read_text(encoding="utf-8")) if ckpt.exists() else {}
    pendientes = [v for v in panel if v not in done]
    if done:
        console.print(f"[green]✓[/] Checkpoint: {len(done)}/{len(panel)} ya hechos, no se re-pagan.")

    if args.dry_run:
        console.print(f"Pendientes: [bold]{len(pendientes)}[/] llamadas — dry-run, sin API.")
        return

    catalog = load_services_catalog(GT_DIR / "services.csv")
    rot = KeyRotator(GEMINI_API_KEYS)
    console.print(f"[dim]{len(GEMINI_API_KEYS)} llaves · modelo {args.model} · "
                  f"{len(pendientes)} llamadas[/]\n")

    for i, vid in enumerate(pendientes, 1):
        wb = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        if not wb.exists():
            console.print(f"  [red]✗ {vid}: sin pizarra[/]"); continue
        console.print(f"[cyan][{i}/{len(pendientes)}][/] {vid} …")

        partes = [prompt_base]
        if not args.no_transcript:
            t = read_transcript(vid)
            if t:
                partes.append(f"\n\n## FULL TRANSCRIPT:\n{t}")

        img = base64.b64encode(wb.read_bytes()).decode("utf-8")
        try:
            analysis = call_gemini(rot, "".join(partes), img, args.model,
                                   schema=FinalArchitectureSchema)
        except QuotaExhausted as e:
            console.print(f"[bold red]🛑 {e}[/]")
            console.print(f"Progreso guardado: {len(done)}/{len(panel)}. Volvé a correr el mismo comando.")
            break
        except Exception as e:
            console.print(f"  [red]✗ falló: {str(e)[:100]}[/]"); continue

        G = create_graph_from_cloudscape_json(analysis, video_id=vid)
        ev = evaluate_pair(G, nx.read_graphml(GT_DIR / f"{vid}.graphml"), vid, catalog)
        done[vid] = {"video_id": vid, "status": "success",
                     "svc_f1": ev["svc_f1"], "edge_f1": ev["edge_f1"],
                     "gen_nodes": ev["gen_nodes"], "gen_edges": ev["gen_edges"],
                     "gt_nodes": ev["gt_nodes"], "gt_edges": ev["gt_edges"],
                     "analysis": analysis}
        ckpt.write_text(json.dumps(done, indent=1, ensure_ascii=False), encoding="utf-8")
        console.print(f"    Svc F1 {100*ev['svc_f1']:.1f}%  Edge F1 {100*ev['edge_f1']:.1f}%")

    exitosos = [r for r in done.values() if r["status"] == "success"]
    if len(exitosos) < len(panel):
        console.print(f"\n[yellow]⚠ Panel incompleto ({len(exitosos)}/{len(panel)}): "
                      f"no escribo run.json para no publicar un promedio parcial.[/]")
        return

    svc = 100 * sum(r["svc_f1"] for r in exitosos) / len(exitosos)
    edge = 100 * sum(r["edge_f1"] for r in exitosos) / len(exitosos)
    t = Table(title=f"Parsimonious · panel {args.panel} · "
                    f"{'SIN' if args.no_transcript else 'CON'} transcript", border_style="cyan")
    t.add_column("video"); t.add_column("Svc F1", justify="right"); t.add_column("Edge F1", justify="right")
    for r in sorted(exitosos, key=lambda x: x["video_id"]):
        t.add_row(r["video_id"], f"{100*r['svc_f1']:.1f}%", f"{100*r['edge_f1']:.1f}%")
    console.print(t)
    console.print(f"\n[bold]Promedio ({len(exitosos)}/{len(panel)}):[/] "
                  f"Service F1 {svc:.2f}%  ·  Edge F1 {edge:.2f}%")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    out = OUT_ROOT / f"{ts}_PARSIMONIOUS_PRODUCCION_p{args.panel}{tag}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "run.json").write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(),
        "brazo": "parsimonious",
        "arquitectura": "una sola llamada (sin separacion Stage1/Stage2)",
        "panel": args.panel, "video_ids": panel, "model": args.model,
        "stage2_prompt": {"name": entrada["name"], "file": entrada["file"],
                          "chars": entrada["chars"], "sha256": entrada["sha256"],
                          "source": "src/configs/prompts/parsimonious/produccion.txt"},
        "transcript_enabled": not args.no_transcript,
        "metrics": {"service_f1_mean": round(svc, 2), "edge_f1_mean": round(edge, 2),
                    "n_success": len(exitosos)},
        "results": list(done.values()),
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] {out.relative_to(PROJECT_ROOT)}")
    if ckpt.exists():
        ckpt.unlink()
        console.print("[dim]Checkpoint consumido.[/]")


if __name__ == "__main__":
    main()
