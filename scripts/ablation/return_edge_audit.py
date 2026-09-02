#!/usr/bin/env python3
"""
return_edge_audit.py — Segunda pasada de auditoría de aristas de retorno.

Por qué esto y no otra reescritura de reglas
---------------------------------------------
`ara/TODO_PARA_EL_ARTICULO.md` §2.9 documenta 11 variantes de Stage 2 (reglas
más estrictas, más laxas, con o sin evidencia visual, con o sin few-shot) que
caen todas dentro de 3 puntos de Edge F1 — ninguna diferencia es significativa.
§2.7 explica por qué: de las 178 aristas del GT que producción pierde en el
panel de 30, un 45% (80) son la arista de RETORNO de un par que el modelo ya
conectó bien en un sentido (`b→a` puesto, `a→b` no). §2.8 intentó arreglarlo
agregando la regla en una sola pasada (V8_ACTORS_AND_RETURNS): el mecanismo
funcionó (bidireccionalidad 12.4%→17.9%) pero el Edge F1 no se movió, porque
el modelo también agregó nodos actor nuevos y los mapeó mal — degradó Service
F1 de forma significativa (p=0.039).

Este script prueba un mecanismo distinto, no otra regla: una SEGUNDA llamada,
posterior a la generación normal de producción, que:

  1. NO puede tocar el conjunto de nodos (se le pasa ya cerrado) — por
     construcción, Service F1 no puede empeorar.
  2. Solo puede proponer la arista INVERSA de una arista que YA existe en el
     borrador (b→a solo si a→b ya está). No puede inventar una relación entre
     dos nodos que no estaban conectados. Cualquier propuesta que no cumpla
     esto se descarta antes de evaluar, no se le confía al modelo.
  3. Reutiliza el borrador ya pagado de una corrida de producción existente
     (`--base`): NO vuelve a correr Stage 1 ni la primera pasada de Stage 2,
     así que cuesta 30 llamadas, no 60.

Referencia: `ara/TODO_PARA_EL_ARTICULO.md` §2.7, §2.8, §2.9.

Uso
---
    .venv/bin/python scripts/ablation/return_edge_audit.py --base <run_dir> --dry-run
    .venv/bin/python scripts/ablation/return_edge_audit.py --base <run_dir>
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.ablation.rerun_panel import (  # noqa: E402
    KeyRotator, QuotaExhausted, call_gemini, read_transcript,
    GOOD_WHITEBOARD_DIR, RAW_DIR,
)
from scripts.ablation.build_evidence_tables import sign_test, wilcoxon_signed_rank  # noqa: E402
from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402
from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog  # noqa: E402
from config.settings import GEMINI_API_KEYS, GEMINI_MODEL  # noqa: E402

import networkx as nx  # noqa: E402

console = Console()

GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
OUT_DIR = PROJECT_ROOT / "reports" / "ablation"
CKPT_DIR = OUT_DIR / ".checkpoints"
CATALOG = load_services_catalog(GT_DIR / "services.csv")


class ReturnEdgeProposal(BaseModel):
    source: str
    target: str
    type: str
    notes: str


class ReturnAuditSchema(BaseModel):
    step_by_step_reasoning: str
    missing_return_edges: list[ReturnEdgeProposal]


AUDIT_PROMPT_TEMPLATE = """You already produced an architecture graph for this AWS whiteboard video. Your job now is NARROW: check ONLY for missing RETURN edges.

## RULES (STRICT)
1. You may propose an edge B→A ONLY IF the edge A→B already exists in DRAFT EDGES below. You are auditing for the reverse of an existing connection, not proposing new relationships between previously unconnected nodes.
2. Do NOT propose any edge whose source or target is not in DRAFT NODES.
3. Do NOT propose an edge that already exists in DRAFT EDGES (in either direction) if a reverse edge is not what's missing — only propose genuinely missing reverse edges.
4. Only propose a return edge if there is explicit evidence for it: a bidirectional/double-headed arrow on the whiteboard, OR a verbal phrase in the transcript indicating a response/acknowledgment/return/callback/poll/notification going back (e.g. "responds to", "sends back", "returns the result to", "acknowledges", "polls", "notifies back to").
5. If you are not sure, do not propose it. An empty list is a valid and often correct answer.
6. "type" should be "data" (payload/result returned), "control" (ack/trigger back), or "meta" (monitoring/feedback) — same convention as DRAFT EDGES.

## DRAFT NODES
{nodes_json}

## DRAFT EDGES (already generated, do not modify)
{edges_json}

## WHITEBOARD IMAGE
(attached)

## FULL TRANSCRIPT
{transcript}
"""


def load_base_run(base_dir: Path) -> dict:
    p = base_dir / "run.json"
    if not p.exists():
        console.print(f"[bold red]✗ No existe {p}[/]")
        sys.exit(1)
    return json.loads(p.read_text(encoding="utf-8"))


def ckpt_path(base_name: str) -> Path:
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    return CKPT_DIR / f"return_audit_{base_name}.json"


def load_ckpt(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save_ckpt(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, indent=1), encoding="utf-8")


def build_key(edge: dict) -> tuple[str, str]:
    return (str(edge["source"]), str(edge["target"]))


def validate_and_merge(draft_nodes: list[dict], draft_edges: list[dict],
                        proposals: list[ReturnEdgeProposal]) -> tuple[list[dict], int, int]:
    """Aplica las reglas de admisión. Devuelve (aristas finales, aceptadas, rechazadas)."""
    node_ids = {str(n["id"]) for n in draft_nodes}
    existing = {build_key(e) for e in draft_edges}
    edges = list(draft_edges)
    accepted, rejected = 0, 0

    for p in proposals:
        s, t = str(p.source), str(p.target)
        if s not in node_ids or t not in node_ids:
            rejected += 1
            continue
        if (t, s) not in existing:          # debe ser el retorno de una arista YA presente
            rejected += 1
            continue
        if (s, t) in existing:              # ya existía en ese sentido, no es una novedad
            rejected += 1
            continue
        fwd = next(e for e in draft_edges if build_key(e) == (t, s))
        edges.append({
            "source": s, "target": t,
            "flow_id": fwd.get("flow_id", 0),
            "seq": f"{fwd.get('seq', '0')}'",
            "type": p.type if p.type in ("data", "control", "meta") else "meta",
            "notes": p.notes,
        })
        existing.add((s, t))
        accepted += 1

    return edges, accepted, rejected


def score(nodes: list[dict], edges: list[dict], video_id: str) -> tuple[float, float]:
    analysis = {"nodes": nodes, "edges": edges}
    G = create_graph_from_cloudscape_json(analysis, video_id=video_id)
    GT = nx.read_graphml(GT_DIR / f"{video_id}.graphml")
    r = evaluate_pair(G, GT, video_id, CATALOG)
    return r["svc_f1"], r["edge_f1"]


def main() -> None:
    ap = argparse.ArgumentParser(description="Segunda pasada: auditoría de aristas de retorno sobre un borrador ya generado")
    ap.add_argument("--base", required=True, metavar="DIR",
                     help="carpeta de reports/ablation/ con el run.json de producción a auditar")
    ap.add_argument("--model", default=GEMINI_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base_dir = Path(args.base)
    if not base_dir.is_absolute():
        base_dir = OUT_DIR / base_dir
    base = load_base_run(base_dir)
    results = [r for r in base["results"] if r["status"] == "success"]
    console.print(f"[green]✓[/] Base cargada: [bold]{base_dir.name}[/] "
                  f"({len(results)} videos exitosos, prompt {base['stage2_prompt']['name']} "
                  f"sha {base['stage2_prompt']['sha256'][:12]})")
    console.print("[dim]Mecanismo: 2ª pasada, solo audita retornos de aristas ya existentes. "
                  "Nodos congelados → Service F1 no puede moverse por construcción.[/]")

    ckpt = ckpt_path(base_dir.name)
    done = load_ckpt(ckpt)

    if args.dry_run:
        console.print(f"[dim]{len(results)} llamadas pendientes (Stage 2b) · "
                       f"{len(done)} ya en checkpoint[/]")
        console.print("— dry-run: todo verificado, sin llamadas a la API —")
        return

    rot = KeyRotator(GEMINI_API_KEYS)
    console.print(f"[dim]{len(GEMINI_API_KEYS)} llaves cargadas · modelo {args.model}[/]\n")

    rows = []
    for i, r in enumerate(results, 1):
        vid = r["video_id"]
        if vid in done:
            rows.append(done[vid])
            continue

        console.print(f"[{i}/{len(results)}] {vid} …")
        draft = r["analysis"]
        wb = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        if not wb.exists():
            console.print(f"  [red]✗ sin pizarra, se salta[/]")
            continue

        prompt = AUDIT_PROMPT_TEMPLATE.format(
            nodes_json=json.dumps(draft["nodes"], indent=1),
            edges_json=json.dumps(draft["edges"], indent=1),
            transcript=read_transcript(vid) or "(sin transcript)",
        )
        img_b64 = base64.b64encode(wb.read_bytes()).decode("utf-8")

        try:
            audit = call_gemini(rot, prompt, img_b64, args.model, schema=ReturnAuditSchema)
        except QuotaExhausted as e:
            console.print(f"[bold red]🛑 {e}[/]")
            break
        except Exception as e:
            console.print(f"  [red]✗ falló: {str(e)[:120]}[/]")
            continue

        proposals = [ReturnEdgeProposal(**p) for p in audit.get("missing_return_edges", [])]
        merged_edges, accepted, rejected = validate_and_merge(draft["nodes"], draft["edges"], proposals)

        svc_f1, edge_f1 = score(draft["nodes"], merged_edges, vid)
        row = {
            "video_id": vid,
            "draft_svc_f1": r["svc_f1"], "draft_edge_f1": r["edge_f1"],
            "audited_svc_f1": svc_f1, "audited_edge_f1": edge_f1,
            "proposed": len(proposals), "accepted": accepted, "rejected": rejected,
            "audited_nodes": draft["nodes"], "audited_edges": merged_edges,
        }
        rows.append(row)
        done[vid] = row
        save_ckpt(ckpt, done)

        d = edge_f1 - r["edge_f1"]
        console.print(f"    propuestas {len(proposals)} · aceptadas {accepted} · rechazadas {rejected} "
                       f"· Edge F1 {r['edge_f1']*100:.1f}% → {edge_f1*100:.1f}% ({d*100:+.1f})")

    if len(rows) < len(results):
        console.print(f"\n[yellow]⚠ Corrida incompleta ({len(rows)}/{len(results)}). "
                       f"Volvé a correr el mismo comando: retoma del checkpoint.[/]")
        return

    # ── reporte pareado ───────────────────────────────────────────
    svc_diffs = [r["audited_svc_f1"] - r["draft_svc_f1"] for r in rows]
    edge_diffs = [r["audited_edge_f1"] - r["draft_edge_f1"] for r in rows]

    t = Table(title="Auditoría de retornos — borrador vs auditado (pareado por video)", border_style="cyan")
    t.add_column("video")
    t.add_column("draft edgeF1", justify="right")
    t.add_column("audit edgeF1", justify="right")
    t.add_column("Δ", justify="right")
    t.add_column("prop/acc/rej", justify="right")
    for r in rows:
        d = r["audited_edge_f1"] - r["draft_edge_f1"]
        style = "green" if d > 1e-9 else ("red" if d < -1e-9 else "dim")
        t.add_row(r["video_id"], f"{r['draft_edge_f1']*100:.1f}%", f"{r['audited_edge_f1']*100:.1f}%",
                   f"[{style}]{d*100:+.1f}[/]", f"{r['proposed']}/{r['accepted']}/{r['rejected']}")
    console.print(t)

    n_svc = sum(1 for r in rows if r["draft_svc_f1"] != r["audited_svc_f1"])
    wins = sum(1 for d in edge_diffs if d > 1e-9)
    losses = sum(1 for d in edge_diffs if d < -1e-9)
    ties = len(edge_diffs) - wins - losses
    p_sign = sign_test(wins, losses)
    _, p_wilcoxon = wilcoxon_signed_rank(edge_diffs)

    mean_draft_svc = sum(r["draft_svc_f1"] for r in rows) / len(rows) * 100
    mean_draft_edge = sum(r["draft_edge_f1"] for r in rows) / len(rows) * 100
    mean_audit_svc = sum(r["audited_svc_f1"] for r in rows) / len(rows) * 100
    mean_audit_edge = sum(r["audited_edge_f1"] for r in rows) / len(rows) * 100
    total_prop = sum(r["proposed"] for r in rows)
    total_acc = sum(r["accepted"] for r in rows)
    total_rej = sum(r["rejected"] for r in rows)

    console.print(f"\n[bold]Service F1:[/] {mean_draft_svc:.2f}% → {mean_audit_svc:.2f}% "
                  f"(videos donde cambió: {n_svc} — debe ser 0 por construcción)")
    console.print(f"[bold]Edge F1:[/]    {mean_draft_edge:.2f}% → {mean_audit_edge:.2f}% "
                  f"({mean_audit_edge - mean_draft_edge:+.2f} pts)")
    console.print(f"[bold]Pareado:[/] {wins} gana · {losses} pierde · {ties} empata "
                  f"→ signos p={p_sign:.4f}, Wilcoxon p={p_wilcoxon:.4f}")
    console.print(f"[bold]Propuestas del modelo:[/] {total_prop} · aceptadas {total_acc} "
                  f"({100*total_acc/total_prop if total_prop else 0:.0f}%) · rechazadas {total_rej}")

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    out_dir = OUT_DIR / f"{ts}_RETURN_EDGE_AUDIT_base-{base_dir.name}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "run.json").write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(),
        "mechanism": "two_pass_return_edge_audit",
        "base_run": str(base_dir.relative_to(PROJECT_ROOT)),
        "base_stage2_prompt": base["stage2_prompt"],
        "model": args.model,
        "metrics": {
            "draft_service_f1_mean": round(mean_draft_svc, 2),
            "draft_edge_f1_mean": round(mean_draft_edge, 2),
            "audited_service_f1_mean": round(mean_audit_svc, 2),
            "audited_edge_f1_mean": round(mean_audit_edge, 2),
            "n_success": len(rows),
        },
        "paired_test": {
            "wins": wins, "losses": losses, "ties": ties,
            "p_sign": p_sign, "p_wilcoxon": p_wilcoxon,
        },
        "proposals": {"total": total_prop, "accepted": total_acc, "rejected": total_rej},
        "results": rows,
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] Corrida escrita → {out_dir.relative_to(PROJECT_ROOT)}")

    if ckpt.exists():
        ckpt.unlink()
        console.print("[dim]Checkpoint consumido y borrado.[/]")


if __name__ == "__main__":
    main()
