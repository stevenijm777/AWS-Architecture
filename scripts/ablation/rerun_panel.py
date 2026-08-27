#!/usr/bin/env python3
"""
rerun_panel.py — Re-run the 14-video ablation panel with a hash-verified prompt.

Why this exists
---------------
The historical `whiteboard_selection_lab/batch_results_*.json` files record a
version *name* ("V6_corrected_v2"), not a prompt hash. Because the source
notebook has five alternative selection cells that each redefine the same
constants, one name can denote several different texts — e.g.
`STAGE2_V6_CORRECTED` exists as 3887 (cell 7), 3974 (cell 9, = production) and
3835 (cell 10) characters. That makes the generation-2 rows of the ablation
table impossible to attribute to a specific prompt after the fact.

This runner closes that gap:

  * prompts are loaded from `src/configs/prompts/*.txt` and their SHA-256 is
    checked against `MANIFEST.json` before any API call — never re-typed inline,
    so the text cannot silently drift the way `batch_prompt_test.py` did;
  * the resolved hashes, model, image digest and Stage 1 provenance are written
    into the run's own `run.json`, so a result can never again name a prompt it
    cannot prove;
  * output goes to `reports/ablation/`, never overwriting the historical files.

Methodology it reproduces
-------------------------
Stage 1 (the World Model) is expensive and is *not* the variable under test, so
the original experiments generated it once per video and reused it across every
Stage 2 variant. This script does the same: it reads the cached
`lab_workspace/<vid>/world_model.json` and only pays for Stage 2. That keeps a
full panel run at 14 calls instead of 28, and — more importantly — holds Stage 1
fixed so any measured difference is attributable to Stage 2 alone.

Prompt assembly, the Gemini schema and the evaluator all mirror
`prompt_batch_ablation_lab.ipynb` cell 13 exactly, so numbers are comparable to
the historical table.

Usage
-----
    # identify which cell produced the historical "V6_corrected_v2" row
    .venv/bin/python scripts/ablation/rerun_panel.py --prompt stage2_v6_corrected__cell9.txt
    .venv/bin/python scripts/ablation/rerun_panel.py --prompt stage2_v6_corrected__cell10.txt

    .venv/bin/python scripts/ablation/rerun_panel.py --list
    .venv/bin/python scripts/ablation/rerun_panel.py --prompt <file> --dry-run
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

warnings.filterwarnings("ignore")

import networkx as nx
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from config.settings import GEMINI_API_KEYS, GEMINI_MODEL
from scripts.core.graph_builder import create_graph_from_cloudscape_json
from scripts.utils.evaluate_graphs import evaluate_pair

console = Console()

# ── Paths ────────────────────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / "data"
GT_DIR = DATA_DIR / "cloudscape_gt"
RAW_DIR = DATA_DIR / "raw"
GOOD_WHITEBOARD_DIR = DATA_DIR / "good_whiteboard"
SERVICES_CSV = GT_DIR / "services.csv"
LAB_WORKSPACE = PROJECT_ROOT / "whiteboard_selection_lab" / "lab_workspace"
PROMPTS_DIR = PROJECT_ROOT / "src" / "configs" / "prompts"
MANIFEST = PROMPTS_DIR / "MANIFEST.json"
OUT_ROOT = PROJECT_ROOT / "reports" / "ablation"
CKPT_DIR = OUT_ROOT / ".checkpoints"
EVIDENCE_DIR = PROJECT_ROOT / "reports" / "connection_evidence"


class QuotaExhausted(RuntimeError):
    """Every configured API key hit its quota. Stop, don't burn the rest of the panel."""

# ── The fixed 14-video panel ─────────────────────────────────────────
# All 14 are graph_usable=True, English, non-special, and none has a zero-edge
# ground truth, so both Service F1 and Edge F1 are meaningful throughout
# (verified against reports/dataset_audit_2026-08-21.csv).
PANEL_14 = [
    "-3lnf5lzsH0", "-kA0ahrhX3I", "-wLEkq21cvA", "07lfvavMdfU", "1aYoIZvabbk",
    "2L0m28ZLmtE", "2e3vOxsHekE", "6CgqEzyWpeA", "6EUknQqaV1w", "6YkguepAQuQ",
    "BZ32w0SSAoY", "Cgv0kfp_6xQ", "wjtSHyENv0I", "ww5fiygF6eg",
]

# Widening set. Sampled at random (seed 42) from the eligible pool — graph_usable,
# non-special, edges scored, no exclusion_reason — restricted to the panel's own
# complexity band (GT 6-13 nodes, 5-20 edges) so the extension does not smuggle in
# a difficulty shift. Videos already carrying ad-hoc Stage 1 caches from other
# experiments were excluded, to keep one single Stage 1 methodology across the set.
NEW_16 = [
    "2XVgpMwY5iE", "7V8wTCkjOqo", "90rWUjKjnAE", "9qTEHITVeLE", "BlCXEMp_lqY",
    "FfSNnH2bbNc", "H2fOkeXxpyw", "JYeXbUdFOdw", "SSWwnNVYi_Q", "a6kqyqTNJM4",
    "c-1GXhOOOww", "f5EJBUfGZtw", "hMK2NJ-q9nc", "jV8DwutbXbg", "jg85DzUZ9Ac",
    "u3ZwnulzLnU",
]

PANEL_30 = PANEL_14 + NEW_16
PANELS = {14: PANEL_14, 30: PANEL_30}

# Historical numbers from the generation-2 table, for side-by-side comparison.
# These are exactly what this script is meant to reproduce (or fail to).
HISTORICAL = {
    "V0 (Baseline)":         (90.88, 61.11),
    "v4_anti_hallucination": (91.62, 63.45),
    "V5_STRICT_ROUTING":     (90.99, 65.14),
    "V6_corrected_v2":       (89.94, 65.28),
    "V7_RETURN_FLOWS":       (90.58, 65.73),
    "V7_RETURN_FLOWS_V6":    (89.30, 66.52),
}


# ── Pydantic schema (mirrors the notebook / production contract) ─────
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


# Stage 1 contract — only needed when a World Model has to be generated because
# no cache exists for that video (see ensure_stage1).
class Entity(BaseModel):
    service: str
    name: str
    type: str
    rationale: str


class VisualConnection(BaseModel):
    source_label: str
    target_label: str
    arrow_direction: str
    description: str


class WorldModelSchema(BaseModel):
    entities: list[Entity]
    visual_connections: list[VisualConnection]


# ── Prompt loading with hash verification ────────────────────────────
def normalise(text: str) -> str:
    """Whitespace-insensitive form — matches scripts/utils/extract_prompts.py."""
    return re.sub(r"\s+", " ", text).strip()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_manifest() -> dict:
    if not MANIFEST.exists():
        console.print(f"[bold red]✗ No existe {MANIFEST}. Corré extract_prompts.py primero.[/]")
        sys.exit(1)
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_verified_prompt(filename: str, manifest: dict) -> tuple[str, dict]:
    """Read a prompt file and refuse to continue if its hash left the manifest."""
    path = PROMPTS_DIR / filename
    if not path.exists():
        console.print(f"[bold red]✗ No existe el prompt: {path}[/]")
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    actual = sha256(normalise(text))

    entry = next((p for p in manifest["prompts"] if p["file"] == filename), None)
    if entry is None:
        console.print(f"[bold red]✗ {filename} no figura en MANIFEST.json — no puedo verificar su identidad.[/]")
        sys.exit(1)

    if actual != entry["sha256"]:
        console.print(
            f"[bold red]✗ HASH MISMATCH en {filename}[/]\n"
            f"  manifest: {entry['sha256']}\n"
            f"  archivo : {actual}\n"
            f"  El texto cambió desde que se generó el manifest. Abortando para no "
            f"repetir el problema que este script existe para evitar."
        )
        sys.exit(1)

    return text, entry


def list_variants(manifest: dict) -> None:
    t = Table(title="Prompts disponibles (verificados por SHA-256)", border_style="cyan")
    t.add_column("archivo", style="bold")
    t.add_column("nombre")
    t.add_column("celda", justify="right")
    t.add_column("chars", justify="right")
    t.add_column("sha", style="dim")
    t.add_column("producción", justify="center")
    for p in manifest["prompts"]:
        if p["stage"] != 2:
            continue
        t.add_row(
            p["file"], p["name"], str(p.get("source_cell", "?")),
            str(p["chars"]), p["sha256"][:12],
            "✓" if p.get("matches_production") else "",
        )
    console.print(t)
    console.print(f"[dim]Stage 1 usado siempre: stage1_v0_baseline.txt "
                  f"({manifest['production_stage1_sha256'][:12]}) — es el de producción.[/]")


# ── Catalog (mirrors the notebook's load_services_catalogs) ──────────
def build_rag_db():
    """Ground-truth corpus for the few-shot retriever. Loaded once, only when needed."""
    sys.path.insert(0, str(PROJECT_ROOT / "whiteboard_selection_lab"))
    from algorithms.dynamic_rag_matcher import (  # noqa: E402
        load_all_ground_truths, find_similar_ground_truths,
        format_few_shot_prompt, extract_services_from_world_model,
    )
    db = load_all_ground_truths(GT_DIR)
    console.print(f"[dim]RAG: {len(db)} grafos GT cargados para recuperación.[/]")
    return db, find_similar_ground_truths, format_few_shot_prompt, extract_services_from_world_model


def load_catalogs() -> tuple[str, str, dict]:
    aws_services, user_actors, catalog = set(), set(), {}
    with open(SERVICES_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("name", "").strip()
            if not name:
                continue
            capability = row.get("capability", "").strip().lower()
            catalog[name] = {"capability": capability}
            if capability == "user" or name.startswith("User"):
                user_actors.add(name)
            else:
                aws_services.add(name)
    return ", ".join(sorted(aws_services)), ", ".join(sorted(user_actors)), catalog


def checkpoint_path(prompt_sha: str, model: str, panel: int, tag: str = "") -> Path:
    """One checkpoint per (prompt, model, panel), so resuming never mixes runs."""
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    safe_model = re.sub(r"[^a-zA-Z0-9._-]", "_", model)
    return CKPT_DIR / f"{prompt_sha[:12]}_{safe_model}_p{panel}{tag}.json"


def load_checkpoint(path: Path) -> dict[str, dict]:
    """Returns {video_id: result} for videos already completed successfully."""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return {r["video_id"]: r for r in data.get("results", []) if r.get("status") == "success"}
    except Exception:
        return {}


def save_checkpoint(path: Path, rows: list[dict], meta: dict) -> None:
    """Written after every video, so a quota wall never costs completed work."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps({**meta, "results": rows}, indent=2,
                              ensure_ascii=False, default=str), encoding="utf-8")
    tmp.replace(path)


def git_commit() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


# ── Gemini call with key rotation ────────────────────────────────────
class KeyRotator:
    """Rotates through the configured API keys when one hits its quota."""

    def __init__(self, keys: list[str]):
        if not keys:
            console.print("[bold red]✗ No hay GEMINI_API_KEYS configuradas en .env[/]")
            sys.exit(1)
        from google import genai
        self._genai = genai
        self.keys = keys
        self.idx = 0
        self.client = genai.Client(api_key=keys[0])

    def rotate(self) -> bool:
        self.idx += 1
        if self.idx >= len(self.keys):
            return False
        console.print(f"[yellow]🔄 Rotando a la llave #{self.idx + 1}/{len(self.keys)}[/]")
        self.client = self._genai.Client(api_key=self.keys[self.idx])
        return True


def call_gemini(rot: KeyRotator, prompt: str, image_b64: str | list[str], model: str,
                schema=FinalArchitectureSchema) -> dict:
    """One Gemini call. Retries transient errors, rotates keys on quota.

    Accepts several images so a variant can pass the clean whiteboard plus an
    annotated copy; order is preserved, and the prompt is responsible for saying
    which is which.
    """
    from google.genai import types

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=schema,
        temperature=0.0,
    )
    imgs = [image_b64] if isinstance(image_b64, str) else list(image_b64)
    contents = [{"parts": [
        {"text": prompt},
        *({"inline_data": {"mime_type": "image/jpeg", "data": b}} for b in imgs),
    ]}]

    # 503 UNAVAILABLE means the model is under load, not that anything is wrong with
    # the request — it clears on its own. Backing off exponentially (as the original
    # notebook did) rather than failing after a few seconds, because giving up here
    # throws away the whole panel run.
    max_attempts, delay = 5, 10
    while True:
        for attempt in range(1, max_attempts + 1):
            try:
                res = rot.client.models.generate_content(
                    model=model, contents=contents, config=config
                )
                return json.loads(res.text)
            except Exception as e:
                err = str(e).upper()
                if any(k in err for k in ("429", "RESOURCE_EXHAUSTED", "QUOTA")):
                    if not rot.rotate():
                        raise QuotaExhausted("Se agotaron todas las llaves API") from e
                    break  # retry immediately with the new key
                console.print(f"  [yellow]⚠ intento {attempt}/{max_attempts}: {str(e)[:90]}[/]")
                if attempt == max_attempts:
                    raise
                time.sleep(delay)
                delay *= 2


# ── Stage 1, only when no cache exists ───────────────────────────────
def read_transcript(vid: str) -> str:
    p = RAW_DIR / f"{vid}_transcript.json"
    if not p.exists():
        return ""
    data = json.loads(p.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return " ".join(s.get("text", "").strip() for s in data)
    return data.get("text", "") if isinstance(data, dict) else ""


def detect_symbols(wb: Path, workspace: Path) -> str:
    """Symbol block injected into Stage 1.

    Both the ablation notebook (cell 13) and production `vision_analyzer.py` run
    the detector before Stage 1, so a World Model generated without it would not
    be comparable to the cached ones. Uses the lab's copy of the detector at its
    own default threshold (40.0), which is what the notebook passed.
    """
    try:
        sys.path.insert(0, str(PROJECT_ROOT / "whiteboard_selection_lab"))
        from algorithms.adaptive_whiteboard_detector import (  # noqa: E402
            procesar_y_resaltar_conclusiones_pizarra, format_symbols_for_prompt,
        )
        syms, _ = procesar_y_resaltar_conclusiones_pizarra(wb, workspace,
                                                           delta_contraste_min=40.0)
        return format_symbols_for_prompt(syms)
    except Exception as e:
        console.print(f"  [yellow]⚠ detector de símbolos falló ({str(e)[:60]}); "
                      f"Stage 1 sigue sin ese bloque[/]")
        return ""


def ensure_stage1(vids: list[str], stage1_tmpl: str, rot: KeyRotator, model: str,
                  aws_str: str, users_str: str) -> list[str]:
    """Generate and cache the World Model for any video lacking one.

    Production never persists Stage 1 (`vision_analyzer.py` builds it in memory and
    discards it), so widening the panel to videos the lab never touched means
    paying for Stage 1 once. It is cached to the same path the original panel uses,
    so every later variant reads it for free.
    """
    missing = [v for v in vids if not (LAB_WORKSPACE / v / "world_model.json").exists()]
    if not missing:
        return []

    console.print(f"[yellow]Stage 1 ausente en {len(missing)} videos — se genera y cachea "
                  f"una sola vez (las demás variantes lo reutilizan).[/]")

    generated = []
    for i, vid in enumerate(missing, 1):
        wb = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        if not wb.exists():
            console.print(f"  [red]✗ {vid}: sin pizarra[/]")
            continue

        workspace = LAB_WORKSPACE / vid
        workspace.mkdir(parents=True, exist_ok=True)
        local_wb = workspace / "best_whiteboard.jpg"
        if not local_wb.exists():
            shutil.copy2(wb, local_wb)

        console.print(f"  [cyan][S1 {i}/{len(missing)}][/] {vid} …")
        p1 = (stage1_tmpl
              .replace("<AWS_SERVICES_PLACEHOLDER>", aws_str)
              .replace("<USER_ACTORS_PLACEHOLDER>", users_str))
        parts = [p1]
        symbols = detect_symbols(local_wb, workspace)
        if symbols:
            parts.append(symbols)
        parts.append(f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={vid}")
        transcript = read_transcript(vid)
        if transcript:
            parts.append(f"\n## FULL TRANSCRIPT:\n{transcript}")

        img_b64 = base64.b64encode(local_wb.read_bytes()).decode("utf-8")
        try:
            wm = call_gemini(rot, "\n".join(parts), img_b64, model, schema=WorldModelSchema)
        except QuotaExhausted:
            raise
        except Exception as e:
            # One video failing (a load spike that outlasts the backoff) should not
            # discard the World Models already paid for in this pass.
            console.print(f"      [red]✗ falló: {str(e)[:90]}[/]")
            continue

        (workspace / "world_model.json").write_text(
            json.dumps(wm, indent=2, ensure_ascii=False), encoding="utf-8")
        generated.append(vid)
        console.print(f"      {len(wm.get('entities', []))} entidades, "
                      f"{len(wm.get('visual_connections', []))} conexiones")
        time.sleep(1.0)

    return generated


# ── Per-video Stage 2 ────────────────────────────────────────────────
def run_video(vid: str, stage2_tmpl: str, rot: KeyRotator, model: str,
              aws_str: str, users_str: str, catalog: dict, rag=None,
              conn_evidence: bool = False) -> dict:
    """Reuses the cached Stage 1 World Model; only Stage 2 costs an API call."""
    wb = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
    if not wb.exists():
        return {"video_id": vid, "status": "error", "error": "sin pizarra en good_whiteboard/"}

    wm_path = LAB_WORKSPACE / vid / "world_model.json"
    if not wm_path.exists():
        return {"video_id": vid, "status": "error",
                "error": "sin World Model cacheado (correr Stage 1 primero)"}
    world_model = json.loads(wm_path.read_text(encoding="utf-8"))

    transcript_text = ""
    t_path = RAW_DIR / f"{vid}_transcript.json"
    if t_path.exists():
        data = json.loads(t_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            transcript_text = " ".join(s.get("text", "").strip() for s in data)
        elif isinstance(data, dict):
            transcript_text = data.get("text", "")

    image_bytes = wb.read_bytes()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Prompt assembly, verbatim from the notebook's cell 13.
    p2 = (stage2_tmpl
          .replace("<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False))
          .replace("<AWS_SERVICES_PLACEHOLDER>", aws_str)
          .replace("<USER_ACTORS_PLACEHOLDER>", users_str))

    # Few-shot variants only: retrieve 2 similar ground-truth graphs as in-context
    # examples (run_dynamic_few_shot_batch.py:299, top_k=2, target video excluded).
    rag_matches = None
    if rag is not None:
        db, find_similar, fmt_fewshot, extract_services = rag
        matches = find_similar(vid, extract_services(world_model), db, top_k=2)
        rag_matches = [m["video_id"] for m in matches]
        p2 = p2.replace("<FEW_SHOT_PLACEHOLDER>", fmt_fewshot(matches))

    parts = [p2, f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={vid}"]

    # Connection-evidence variant: a badged copy of the whiteboard plus the candidate
    # links between badges. The block goes in before the transcript so it reads as
    # input evidence alongside the World Model, not as a trailing instruction.
    images = [image_b64]
    ev_meta = None
    if conn_evidence:
        from scripts.ablation.connection_evidence import build_evidence  # noqa: E402
        ev = build_evidence(vid, wb, EVIDENCE_DIR / vid)
        if ev["prompt_block"]:
            parts.append(ev["prompt_block"])
            images.append(base64.b64encode(ev["overlay_path"].read_bytes()).decode("utf-8"))
        ev_meta = {"n_symbols": ev["n_symbols"], "n_pairs_kept": len(ev["pairs_kept"]),
                   "overlay_sent": bool(ev["prompt_block"])}

    if transcript_text:
        parts.append(f"\n## FULL TRANSCRIPT:\n{transcript_text}")

    analysis = call_gemini(rot, "\n".join(parts), images, model)

    G = create_graph_from_cloudscape_json(analysis, video_id=vid)
    gt = nx.read_graphml(str(GT_DIR / f"{vid}.graphml"))
    ev = evaluate_pair(G, gt, vid, catalog)

    wm_stat = wm_path.stat()
    return {
        "video_id": vid,
        "status": "success",
        "svc_f1": ev["svc_f1"],
        "edge_f1": ev["edge_f1"],
        "gen_nodes": G.number_of_nodes(),
        "gen_edges": G.number_of_edges(),
        "gt_nodes": gt.number_of_nodes(),
        "gt_edges": gt.number_of_edges(),
        "graph_usable": ev["graph_usable"],
        "services_missing": ev["services_missing"],
        "services_hallucinated": ev["services_hallucinated"],
        # provenance — the whole point of this rewrite
        "whiteboard_sha256": hashlib.sha256(image_bytes).hexdigest(),
        "rag_matches": rag_matches,
        "connection_evidence": ev_meta,
        "stage1_cache": str(wm_path.relative_to(PROJECT_ROOT)),
        "stage1_cached_at": datetime.fromtimestamp(wm_stat.st_mtime).isoformat(timespec="seconds"),
        "analysis": analysis,
    }


# ── Reporting ────────────────────────────────────────────────────────
def report(rows: list[dict], entry: dict, label: str) -> tuple[float, float]:
    ok = [r for r in rows if r["status"] == "success"]
    svc = 100 * sum(r["svc_f1"] for r in ok) / len(ok) if ok else 0.0
    edge = 100 * sum(r["edge_f1"] for r in ok) / len(ok) if ok else 0.0

    t = Table(title=f"Panel de 14 — {entry['name']} (celda {entry.get('source_cell')})",
              border_style="cyan")
    t.add_column("video", style="bold")
    t.add_column("Svc F1", justify="right")
    t.add_column("Edge F1", justify="right")
    t.add_column("nodos", justify="right")
    t.add_column("aristas", justify="right")
    for r in rows:
        if r["status"] == "success":
            t.add_row(r["video_id"], f"{100*r['svc_f1']:.1f}%", f"{100*r['edge_f1']:.1f}%",
                      f"{r['gen_nodes']}/{r['gt_nodes']}", f"{r['gen_edges']}/{r['gt_edges']}")
        else:
            t.add_row(r["video_id"], "[red]error[/]", "—", "—", "—")
    console.print(t)

    console.print(f"\n[bold]Promedio ({len(ok)}/{len(rows)} exitosos):[/] "
                  f"Service F1 [green]{svc:.2f}%[/]  ·  Edge F1 [green]{edge:.2f}%[/]")

    ref = HISTORICAL.get(label)
    if ref:
        d_svc, d_edge = svc - ref[0], edge - ref[1]
        console.print(
            f"[bold]Histórico '{label}':[/] Service F1 {ref[0]:.2f}%  ·  Edge F1 {ref[1]:.2f}%\n"
            f"[bold]Delta:[/] Service {d_svc:+.2f} pts  ·  Edge {d_edge:+.2f} pts"
        )
        console.print(
            "[dim]Recordá el piso de ruido de ~3 puntos que estableció v2_verbal "
            "(mismo prompt re-corrido, 90.88% → 87.90%): diferencias menores a eso "
            "en este panel no son señal.[/]"
        )
    return svc, edge


def main() -> None:
    ap = argparse.ArgumentParser(description="Re-corre el panel de 14 con un prompt verificado por hash")
    ap.add_argument("--prompt", help="archivo en src/configs/prompts/ (ej. stage2_v6_corrected__cell9.txt)")
    ap.add_argument("--label", default=None, help="etiqueta histórica a comparar (default: se infiere)")
    ap.add_argument("--model", default=GEMINI_MODEL)
    ap.add_argument("--list", action="store_true", help="listar prompts disponibles y salir")
    ap.add_argument("--dry-run", action="store_true", help="verificar todo sin llamar a la API")
    ap.add_argument("--panel", type=int, default=14, choices=sorted(PANELS),
                    help="tamaño del panel: 14 (original) o 30 (ampliado)")
    ap.add_argument("--connection-evidence", action="store_true",
                    help="añade la imagen con badges + los vínculos candidatos a Stage 2")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    panel = PANELS[args.panel]

    manifest = load_manifest()

    if args.list:
        list_variants(manifest)
        return
    if not args.prompt:
        ap.error("hace falta --prompt (o --list)")

    stage2, entry = load_verified_prompt(args.prompt, manifest)
    # Stage 1 is hash-verified too: widening the panel means generating some, and a
    # drifted Stage 1 would silently make new videos incomparable to the cached ones.
    stage1_prompt_text, stage1_entry = load_verified_prompt("stage1_v0_baseline.txt", manifest)

    console.print(f"[green]✓[/] Prompt verificado: [bold]{entry['name']}[/] "
                  f"(celda {entry.get('source_cell')}, {entry['chars']} chars, sha {entry['sha256'][:12]})")
    if entry.get("matches_production"):
        console.print("[green]  ✓ Es byte-idéntico al que corre producción.[/]")
    else:
        console.print(f"[yellow]  ⚠ NO es el de producción "
                      f"(producción = {manifest['production_stage2_sha256'][:12]}).[/]")
    console.print(f"[dim]Stage 1: {stage1_entry['name']} ({stage1_entry['sha256'][:12]}) — cacheado, no se recalcula.[/]")

    # Stage 1 cache freshness: a World Model older than its whiteboard describes
    # a different image than the one Stage 2 now receives.
    stale = []
    for vid in panel:
        wm = LAB_WORKSPACE / vid / "world_model.json"
        wb = GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        if wm.exists() and wb.exists() and wb.stat().st_mtime > wm.stat().st_mtime:
            stale.append(vid)
    if stale:
        console.print(f"[yellow]⚠ World Model más viejo que su pizarra en: {', '.join(stale)} "
                      f"— su Stage 1 describe una imagen anterior.[/]")

    label = args.label or entry["name"].replace("STAGE2_", "")

    need_s1 = [v for v in panel if not (LAB_WORKSPACE / v / "world_model.json").exists()]
    console.print(f"[dim]Panel de {len(panel)} · Stage 2: {len(panel)} llamadas · "
                  f"Stage 1 a generar: {len(need_s1)}[/]")

    if args.dry_run:
        if need_s1:
            console.print(f"[yellow]Sin cache de Stage 1: {', '.join(need_s1)}[/]")
        console.print("[bold yellow]— dry-run: todo verificado, sin llamadas a la API —[/]")
        return

    aws_str, users_str, catalog = load_catalogs()

    # The few-shot variant is the only one carrying this placeholder. Leaving it
    # unfilled would silently send the literal token to the model, so treat its
    # presence as the switch that turns the retriever on.
    rag = build_rag_db() if "<FEW_SHOT_PLACEHOLDER>" in stage2 else None

    ev_tag = "_connev" if args.connection_evidence else ""
    ckpt = checkpoint_path(entry["sha256"], args.model, args.panel, ev_tag)
    done = load_checkpoint(ckpt)
    if done:
        console.print(f"[green]✓[/] Checkpoint encontrado: {len(done)}/{len(panel)} videos ya "
                      f"completados, se saltean (no se re-pagan).")
        console.print(f"[dim]  {ckpt.relative_to(PROJECT_ROOT)}[/]")

    pending = [v for v in panel if v not in done]
    if not pending:
        console.print("[bold green]Todos los videos ya estaban completos en el checkpoint.[/]")

    rot = KeyRotator(GEMINI_API_KEYS)
    console.print(f"[dim]{len(GEMINI_API_KEYS)} llaves cargadas · modelo {args.model} · "
                  f"{len(pending)} llamadas pendientes (Stage 2)[/]\n")

    # Pay for Stage 1 once; every later variant on this panel reads the cache.
    try:
        stage1_generated = ensure_stage1(pending, stage1_prompt_text, rot, args.model,
                                         aws_str, users_str)
    except QuotaExhausted as e:
        console.print(f"[bold red]🛑 {e} durante Stage 1.[/]\n"
                      f"Los World Models ya generados quedaron cacheados; volvé a correr "
                      f"el mismo comando cuando se renueve la cuota.")
        sys.exit(2)

    # Stage 2 on an incomplete panel would cost 30 calls for a result that cannot be
    # published anyway, so stop before spending them.
    still_missing = [v for v in pending
                     if not (LAB_WORKSPACE / v / "world_model.json").exists()]
    if still_missing:
        console.print(f"[bold red]🛑 Sin World Model tras reintentar: {', '.join(still_missing)}[/]\n"
                      f"[dim]{len(stage1_generated)} generados y cacheados en esta pasada.[/]\n"
                      f"No sigo con Stage 2: el panel quedaría incompleto y gastaría "
                      f"{len(pending)} llamadas para nada. Volvé a correr el mismo comando — "
                      f"retoma solo los que faltan.")
        sys.exit(2)

    ckpt_meta = {
        "prompt_file": entry["file"], "prompt_sha256": entry["sha256"],
        "model": args.model, "panel": f"{len(panel)}_videos",
    }
    rows = [done[v] for v in panel if v in done]
    quota_wall = False

    for i, vid in enumerate(pending, 1):
        console.print(f"[cyan][{i}/{len(pending)}][/] {vid} …")
        try:
            r = run_video(vid, stage2, rot, args.model, aws_str, users_str, catalog,
                          rag, args.connection_evidence)
        except QuotaExhausted as e:
            # Stop here on purpose: burning the remaining videos would only
            # produce errors and would not save any work.
            console.print(f"[bold red]🛑 {e}[/]")
            quota_wall = True
            break
        except Exception as e:
            r = {"video_id": vid, "status": "error", "error": str(e)[:200]}

        if r["status"] == "success":
            console.print(f"    Svc F1 {100*r['svc_f1']:.1f}%  Edge F1 {100*r['edge_f1']:.1f}%")
        else:
            console.print(f"    [red]✗ {r.get('error')}[/]")
        rows.append(r)
        save_checkpoint(ckpt, rows, ckpt_meta)   # ← after every single video
        time.sleep(1.0)

    ok_n = sum(1 for r in rows if r["status"] == "success")
    if quota_wall:
        save_checkpoint(ckpt, rows, ckpt_meta)
        console.print(
            f"\n[bold yellow]Progreso guardado: {ok_n}/{len(panel)} videos completos.[/]\n"
            f"[dim]Checkpoint: {ckpt.relative_to(PROJECT_ROOT)}[/]\n"
            f"Cuando se renueve la cuota, volvé a correr el MISMO comando y retoma "
            f"desde donde quedó — no re-paga lo ya hecho."
        )

    # Any shortfall, not just a quota wall: a lone 503 that outlives the backoff also
    # leaves the panel incomplete, and a mean over 29 of 30 videos published as "the
    # 30-panel" is exactly the kind of silent inaccuracy this runner exists to prevent.
    if ok_n < len(panel):
        save_checkpoint(ckpt, rows, ckpt_meta)
        failed = [r["video_id"] for r in rows if r["status"] != "success"]
        console.print(
            f"[yellow]⚠ Panel incompleto ({ok_n}/{len(panel)}): no escribo run.json para no "
            f"publicar un promedio parcial como si fuera el resultado.[/]\n"
            f"[dim]Fallaron: {', '.join(failed) or '—'}[/]\n"
            f"Volvé a correr el mismo comando: retoma solo los que faltan."
        )
        sys.exit(2)

    order = {v: i for i, v in enumerate(panel)}
    rows.sort(key=lambda r: order.get(r["video_id"], 999))
    svc, edge = report(rows, entry, label)

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    suffix = (f"_p{len(panel)}" if len(panel) != 14 else "") + ev_tag
    out_dir = Path(args.out).resolve() if args.out else OUT_ROOT / f"{stamp}_{entry['name']}_cell{entry.get('source_cell')}{suffix}"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "run.json").write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "panel": f"{len(panel)}_videos",
        "video_ids": panel,
        "model": args.model,
        "temperature": 0.0,
        "git_commit": git_commit(),
        "stage2_prompt": {
            "name": entry["name"], "file": entry["file"],
            "source_cell": entry.get("source_cell"), "chars": entry["chars"],
            "sha256": entry["sha256"], "matches_production": entry.get("matches_production", False),
        },
        "stage1_prompt": {
            "name": stage1_entry["name"], "sha256": stage1_entry["sha256"],
            "note": "leído del cache lab_workspace/<vid>/world_model.json salvo los listados "
                    "en stage1_generated_now, que se generaron en esta corrida con inyección "
                    "de símbolos (mismo camino que el notebook y que producción).",
        },
        "connection_evidence_enabled": args.connection_evidence,
        "stage1_generated_now": stage1_generated,
        "stale_stage1_cache": stale,
        "metrics": {
            "service_f1_mean": round(svc, 2),
            "edge_f1_mean": round(edge, 2),
            "n_success": sum(1 for r in rows if r["status"] == "success"),
        },
        "historical_reference": HISTORICAL.get(label),
        "results": rows,
    }, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    with open(out_dir / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["video_id", "status", "svc_f1", "edge_f1", "gen_nodes", "gt_nodes",
                    "gen_edges", "gt_edges", "whiteboard_sha256", "stage1_cached_at"])
        for r in rows:
            w.writerow([
                r["video_id"], r["status"],
                f"{100*r['svc_f1']:.2f}" if r["status"] == "success" else "",
                f"{100*r['edge_f1']:.2f}" if r["status"] == "success" else "",
                r.get("gen_nodes", ""), r.get("gt_nodes", ""),
                r.get("gen_edges", ""), r.get("gt_edges", ""),
                r.get("whiteboard_sha256", "")[:16], r.get("stage1_cached_at", ""),
            ])

    console.print(f"\n[green]✓[/] Corrida escrita → [bold]{out_dir.relative_to(PROJECT_ROOT)}[/]")

    # Panel complete and published: the checkpoint has done its job.
    if ok_n == len(panel) and ckpt.exists():
        ckpt.unlink()
        console.print("[dim]Checkpoint consumido y borrado (panel completo).[/]")


if __name__ == "__main__":
    main()
