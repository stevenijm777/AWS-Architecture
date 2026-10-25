#!/usr/bin/env python3
"""
claude_panel.py — El panel de 30 con Claude en Stage 2, vía `claude -p` (plan de suscripción).

Qué hace
--------
Repite la condición "Stage 1 manual" (`--oracle vision` de rerun_panel.py) cambiando solo
el modelo de Stage 2 por Claude. El prompt, el World Model transcrito a mano, la imagen de
la pizarra, el transcript y el evaluador son los mismos que recibieron Flash y Pro: el
texto se arma con las mismas funciones de rerun_panel.py, no se re-tipea.

Como no hay API de Anthropic, cada video es una llamada independiente a Claude Code en
modo no interactivo (`claude -p`): contexto vacío por video, sin herramientas, con el
esquema de salida forzado por `--json-schema` (el equivalente del `response_schema` de
Gemini).

Tres pasos, cada uno idempotente:

    export     arma reports/claude/: PROMPT_STAGE2.md, schema.json y, por video,
               prompt.md + world_model_manual.json + pizarra.jpg
    run        llama a `claude -p` por cada video sin salida y guarda output.json
    evaluate   construye los grafos, los evalúa y escribe run.json (mismo formato que
               rerun_panel.py, comparable con compare_models.py)

Uso
---
    .venv/Scripts/python scripts/ablation/claude_panel.py export
    .venv/Scripts/python scripts/ablation/claude_panel.py run --limit 2
    .venv/Scripts/python scripts/ablation/claude_panel.py run
    .venv/Scripts/python scripts/ablation/claude_panel.py evaluate

Brazo B
-------
`--oracle oracle_gt` repite lo mismo con el ground truth convertido a World Model
(`world_model_oracle_gt.json`, de build_oracle_world_models.py) como entrada de Stage 2,
y escribe en reports/claude_oracle_gt/. Mide el techo de Stage 2 con Claude; la referencia
es la corrida `--oracle oracle_gt` de rerun_panel.py sobre el mismo panel.

    .venv/Scripts/python scripts/ablation/claude_panel.py --oracle oracle_gt export
    .venv/Scripts/python scripts/ablation/claude_panel.py --oracle oracle_gt run
    .venv/Scripts/python scripts/ablation/claude_panel.py --oracle oracle_gt evaluate

Diferencias con las corridas de Gemini que hay que declarar
-----------------------------------------------------------
  * la temperatura no se puede fijar (Gemini corrió a 0.0);
  * Claude Code exige un system prompt: se reemplaza el suyo por una sola línea neutra
    (SYSTEM_PROMPT); Gemini no recibió ninguno;
  * el cupo es el de la suscripción, no hay costo por token facturado.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.ablation import rerun_panel as rp  # noqa: E402
from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402
from scripts.utils.evaluate_graphs import evaluate_pair  # noqa: E402

PROMPT_FILE = "stage2_v6_corrected__cell9.txt"      # el de producción, igual que Flash y Pro
# Qué World Model entra a Stage 2. Mismos nombres que `--oracle` de rerun_panel.py; cada
# condición tiene su propio directorio para que una no pise las salidas de la otra.
ORACLES = {
    "vision": {       # brazo A: Stage 1 transcrito a mano
        "out": "claude", "copy_as": "world_model_manual.json",
        "what": "tu transcripción manual de la pizarra",
        "note": "Stage 1 NO corrió: Stage 2 recibió la transcripción manual de la pizarra.",
    },
    "oracle_gt": {    # brazo B: el ground truth convertido, techo 100/100
        "out": "claude_oracle_gt", "copy_as": "world_model_oracle_gt.json",
        "what": "el ground truth de Cloudscape convertido a World Model",
        "note": "Stage 1 NO corrió: Stage 2 recibió el ground truth convertido a World Model. "
                "Igual recibe la imagen de la pizarra y el transcript completo, así que mide "
                "Stage 2 en configuración de producción con la mejor entrada posible.",
    },
    "produccion": {   # sin oráculo: la lectura automática de la etapa 1 que está en caché
        "out": "claude_produccion", "copy_as": "world_model_produccion.json", "wm_file": "world_model.json",
        "what": "la lectura automática de la pizarra que produjo la etapa 1 (Gemini Flash, en caché)",
        "note": "Sin oráculo: Stage 2 recibe el World Model que generó Stage 1 en producción "
                "(lab_workspace/<vid>/world_model.json, el mismo que usaron las corridas de Gemini).",
    },
}
ORACLE = "vision"
OUT = PROJECT_ROOT / "reports" / ORACLES[ORACLE]["out"]
VIDEOS = OUT / "videos"
WM_NAME = f"world_model_{ORACLE}.json"
MANUAL_SRC = PROJECT_ROOT / "data" / "manual_world_models"
DEFAULT_MODEL = "claude-opus-5-5"
DEFAULT_EFFORT = "high"
SYSTEM_PROMPT = "Responde a la solicitud del usuario siguiendo exactamente sus instrucciones."


def configure(oracle: str, prompt: str = PROMPT_FILE, replicate: int | None = None) -> None:
    global ORACLE, OUT, VIDEOS, WM_NAME, PROMPT_FILE
    ORACLE = oracle
    # Otro prompt que el de producción va a su propio directorio (p. ej. claude_oracle_gt_v9).
    tag = re.search(r"stage2_(v\d+)", prompt)
    suffix = "" if prompt == PROMPT_FILE else f"_{tag.group(1) if tag else Path(prompt).stem}"
    PROMPT_FILE = prompt
    # Una replica repite la misma condicion en su propio directorio, sin tocar la corrida original.
    suffix += f"_rep{replicate}" if replicate else ""
    OUT = PROJECT_ROOT / "reports" / (ORACLES[oracle]["out"] + suffix)
    VIDEOS = OUT / "videos"
    WM_NAME = ORACLES[oracle].get("wm_file", f"world_model_{oracle}.json")


# ── Prompt: el mismo ensamblado que rerun_panel.run_video ────────────
def build_prompt(vid: str, stage2_tmpl: str, aws_str: str, users_str: str) -> tuple[str, dict]:
    wm_path = rp.LAB_WORKSPACE / vid / WM_NAME
    world_model = json.loads(wm_path.read_text(encoding="utf-8"))
    p2 = (stage2_tmpl
          .replace("<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False))
          .replace("<AWS_SERVICES_PLACEHOLDER>", aws_str)
          .replace("<USER_ACTORS_PLACEHOLDER>", users_str))
    parts = [p2, f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={vid}"]
    transcript = rp.read_transcript(vid)
    if transcript:
        parts.append(f"\n## FULL TRANSCRIPT:\n{transcript}")
    return "\n".join(parts), world_model


def load_inputs() -> tuple[str, dict, str, str, dict]:
    manifest = rp.load_manifest()
    stage2, entry = rp.load_verified_prompt(PROMPT_FILE, manifest)
    aws_str, users_str, catalog = rp.load_catalogs()
    return stage2, entry, aws_str, users_str, catalog


# ── export ───────────────────────────────────────────────────────────
def cmd_export(args) -> None:
    stage2, entry, aws_str, users_str, _ = load_inputs()
    panel = rp.PANELS[args.panel]
    VIDEOS.mkdir(parents=True, exist_ok=True)
    schema = rp.FinalArchitectureSchema.model_json_schema()
    (OUT / "schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")

    if ORACLE == "oracle_gt":
        from scripts.ablation.build_oracle_world_models import gt_to_world_model
    missing = []
    for vid in panel:
        wb = rp.GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        wm = rp.LAB_WORKSPACE / vid / WM_NAME
        src = MANUAL_SRC / f"{vid}.json"
        if not (wb.exists() and wm.exists()):
            missing.append(vid)
            continue
        # La copia del lab es la que leyeron Flash y Pro; tiene que ser tu original.
        if ORACLE == "vision" and src.exists() and json.loads(src.read_text(encoding="utf-8")) != json.loads(wm.read_text(encoding="utf-8")):
            sys.exit(f"✗ {vid}: {WM_NAME} difiere de data/manual_world_models/. No exporto.")
        # El brazo B solo tiene techo 100/100 si el archivo es exactamente la conversión del GT.
        if ORACLE == "oracle_gt" and gt_to_world_model(nx.read_graphml(str(rp.GT_DIR / f"{vid}.graphml"))) != json.loads(wm.read_text(encoding="utf-8")):
            sys.exit(f"✗ {vid}: {WM_NAME} no es la conversión del ground truth. No exporto.")
        d = VIDEOS / vid
        d.mkdir(exist_ok=True)
        prompt, _ = build_prompt(vid, stage2, aws_str, users_str)
        (d / "prompt.md").write_text(prompt, encoding="utf-8")
        shutil.copy2(wm, d / ORACLES[ORACLE]["copy_as"])
        shutil.copy2(wb, d / "pizarra.jpg")
    if missing:
        sys.exit(f"✗ Faltan pizarra o {WM_NAME}: {', '.join(missing)}")

    (OUT / "PROMPT_STAGE2.md").write_text(_prompt_doc(stage2, entry, aws_str, users_str, schema), encoding="utf-8")
    print(f"✓ {len(panel)} videos exportados en {OUT.relative_to(PROJECT_ROOT)}")


def _prompt_doc(stage2: str, entry: dict, aws_str: str, users_str: str, schema: dict) -> str:
    return f"""# Prompt de Stage 2 enviado a Claude

Prompt de Stage 2: `{entry['name']}` (archivo `{entry['file']}`, sha256
`{entry['sha256'][:12]}`{', el de producción' if entry.get('matches_production') else ', una variante del de producción'}).

## Qué recibe Claude por video

Una sola llamada, sin historial, con dos bloques en este orden:

1. **Texto** — `videos/<id>/prompt.md`. Es la plantilla de abajo con tres reemplazos y dos
   anexos:
   - `<WORLD_MODEL_PLACEHOLDER>` → el JSON de `videos/<id>/{ORACLES[ORACLE]['copy_as']}`
     ({ORACLES[ORACLE]['what']}: `entities` + `visual_connections`);
   - `<AWS_SERVICES_PLACEHOLDER>` → el catálogo de servicios de Cloudscape
     ({len(aws_str.split(', '))} nombres);
   - `<USER_ACTORS_PLACEHOLDER>` → el catálogo de actores ({len(users_str.split(', '))} nombres);
   - al final, `## VIDEO URL:` y `## FULL TRANSCRIPT:` con la transcripción completa.
2. **Imagen** — `videos/<id>/pizarra.jpg`, el frame de pizarra de `good_whiteboard/`.

La forma de la respuesta se fuerza con `schema.json` (`claude -p --json-schema`), que es
el mismo esquema que Gemini recibió como `response_schema`. El prompt no cambia.

Para hacerlo a mano en claude.ai: conversación nueva, adjuntar `pizarra.jpg`, pegar
`prompt.md` y añadir al final «Responde únicamente con un objeto JSON que cumpla este
esquema:» seguido del contenido de `schema.json`. Guardar la respuesta como
`videos/<id>/output.json`.

## Plantilla (antes de los reemplazos)

````text
{stage2}
````

## Esquema de salida

```json
{json.dumps(schema, indent=2)}
```
"""


# ── run ──────────────────────────────────────────────────────────────
def find_claude() -> str:
    if os.environ.get("CLAUDE_BIN"):
        return os.environ["CLAUDE_BIN"]
    found = shutil.which("claude")
    if found:
        return found
    # La app de escritorio trae su propio binario; se toma la versión más nueva.
    # Según la versión de la app, el binario está en %APPDATA%\Claude o en %LOCALAPPDATA%\Claude-Data\<paquete>.
    cands = list((Path(os.environ.get("APPDATA", "")) / "Claude" / "claude-code").glob("*/*/claude.exe"))
    cands += list((Path(os.environ.get("LOCALAPPDATA", "")) / "Claude-Data").glob("*/claude-code/*/*/claude.exe"))
    cands = sorted(cands, key=lambda p: [int(x) for x in p.parts[-3].split(".")])
    if cands:
        return str(cands[-1])
    sys.exit("✗ No encuentro el ejecutable de Claude Code. Definir CLAUDE_BIN.")


def call_claude(claude: str, prompt: str, image: Path, model: str, effort: str, schema: dict,
                raw_path: Path, timeout: int) -> dict:
    """Una llamada sin historial ni herramientas. Devuelve el evento `result`."""
    message = {"type": "user", "message": {"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                     "data": base64.b64encode(image.read_bytes()).decode("ascii")}},
    ]}}
    cmd = [claude, "-p", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
           "--model", model, "--effort", effort, "--tools", "", "--system-prompt", SYSTEM_PROMPT,
           "--json-schema", json.dumps(schema), "--no-session-persistence",
           "--setting-sources", "", "--strict-mcp-config"]
    # Directorio vacío: sin CLAUDE.md ni memoria de proyecto que se cuelen en el contexto.
    with tempfile.TemporaryDirectory() as cwd:
        proc = subprocess.run(cmd, input=json.dumps(message) + "\n", capture_output=True, text=True,
                              encoding="utf-8", cwd=cwd, timeout=timeout)
    raw_path.write_text(proc.stdout or "", encoding="utf-8")
    result = None
    for line in (proc.stdout or "").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
    if result is None:
        raise RuntimeError(f"sin evento result (exit {proc.returncode}): {(proc.stderr or proc.stdout)[:300]}")
    return result


def extract_analysis(result: dict) -> dict:
    if result.get("is_error") or result.get("subtype") not in (None, "success"):
        raise RuntimeError(f"{result.get('subtype') or result.get('terminal_reason')}: {str(result.get('result'))[:300]}")
    out = result.get("structured_output")
    if out is None:
        text = (result.get("result") or "").strip()
        if text.startswith("```"):
            text = text.strip("`").removeprefix("json").strip()
        out = json.loads(text)
    rp.FinalArchitectureSchema.model_validate(out)   # misma validación que el esquema de Gemini
    return out


def cmd_run(args) -> None:
    claude = find_claude()
    schema = json.loads((OUT / "schema.json").read_text(encoding="utf-8"))
    panel = args.videos or rp.PANELS[args.panel]
    pending = [v for v in panel if not (VIDEOS / v / "output.json").exists()]
    if args.limit:
        pending = pending[: args.limit]
    print(f"{claude}\nmodelo {args.model} · effort {args.effort} · {len(pending)} videos pendientes")
    for i, vid in enumerate(pending, 1):
        d = VIDEOS / vid
        prompt = (d / "prompt.md").read_text(encoding="utf-8")
        t0 = time.perf_counter()
        try:
            result = call_claude(claude, prompt, d / "pizarra.jpg", args.model, args.effort, schema,
                                 d / "claude_raw.jsonl", args.timeout)
            analysis = extract_analysis(result)
        except Exception as e:
            print(f"[{i}/{len(pending)}] {vid}  ✗ {str(e)[:200]}")
            (d / "error.txt").write_text(str(e), encoding="utf-8")
            if "api_error" in str(e) or "login" in str(e).lower() or "limit" in str(e).lower():
                print("Corto acá: es un problema de sesión o de cupo, no del video.")
                break
            continue
        (d / "error.txt").unlink(missing_ok=True)
        u = result.get("usage") or {}
        meta = {
            "model_requested": args.model, "models_used": sorted((result.get("modelUsage") or {}).keys()),
            "effort": args.effort, "system_prompt": SYSTEM_PROMPT, "seconds": round(time.perf_counter() - t0, 1),
            "input_tokens": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0),
            "thinking_tokens": (u.get("output_tokens_details") or {}).get("thinking_tokens", 0),
            "api_equivalent_cost_usd": result.get("total_cost_usd"),
            "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "claude_code_session": result.get("session_id"),
        }
        (d / "output.json").write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding="utf-8")
        (d / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[{i}/{len(pending)}] {vid}  ✓ {len(analysis['nodes'])} nodos, {len(analysis['edges'])} aristas · "
              f"{meta['seconds']}s · {meta['output_tokens']} tok salida · {', '.join(meta['models_used'])}")


# ── evaluate ─────────────────────────────────────────────────────────
def cmd_evaluate(args) -> None:
    _, entry, _, _, catalog = load_inputs()
    panel = rp.PANELS[args.panel]
    rows, metas = [], []
    for vid in panel:
        d = VIDEOS / vid
        if not (d / "output.json").exists():
            continue
        analysis = json.loads((d / "output.json").read_text(encoding="utf-8"))
        meta = json.loads((d / "meta.json").read_text(encoding="utf-8")) if (d / "meta.json").exists() else {}
        G = create_graph_from_cloudscape_json(analysis, video_id=vid)
        nx.write_graphml(G, str(d / "grafo.graphml"))
        gt = nx.read_graphml(str(rp.GT_DIR / f"{vid}.graphml"))
        ev = evaluate_pair(G, gt, vid, catalog)
        wm_path = rp.LAB_WORKSPACE / vid / WM_NAME
        row = {
            "video_id": vid, "status": "success", "svc_f1": ev["svc_f1"], "edge_f1": ev["edge_f1"],
            "gen_nodes": G.number_of_nodes(), "gen_edges": G.number_of_edges(),
            "gt_nodes": gt.number_of_nodes(), "gt_edges": gt.number_of_edges(),
            "graph_usable": ev["graph_usable"], "services_missing": ev["services_missing"],
            "services_hallucinated": ev["services_hallucinated"],
            "whiteboard_sha256": hashlib.sha256((d / "pizarra.jpg").read_bytes()).hexdigest(),
            "rag_matches": None, "connection_evidence": None,
            "stage1_cache": str(wm_path.relative_to(PROJECT_ROOT)),
            "stage1_cached_at": datetime.fromtimestamp(wm_path.stat().st_mtime).isoformat(timespec="seconds"),
            "world_model_sha256": hashlib.sha256(wm_path.read_bytes()).hexdigest(),
            "analysis": analysis,
        }
        (d / "evaluacion.json").write_text(json.dumps({k: v for k, v in row.items() if k != "analysis"},
                                                      indent=2, ensure_ascii=False), encoding="utf-8")
        rows.append(row)
        metas.append(meta)
        print(f"{vid}  Svc F1 {100*row['svc_f1']:.1f}%  Edge F1 {100*row['edge_f1']:.1f}%  "
              f"aristas {row['gen_edges']}/{row['gt_edges']}")
    if not rows:
        sys.exit("No hay salidas todavía.")

    svc = 100 * sum(r["svc_f1"] for r in rows) / len(rows)
    edge = 100 * sum(r["edge_f1"] for r in rows) / len(rows)
    complete = len(rows) == len(panel)
    models = sorted({m for meta in metas for m in meta.get("models_used", [])}) or [DEFAULT_MODEL]
    print(f"\nPromedio ({len(rows)}/{len(panel)}): Service F1 {svc:.2f}%  ·  Edge F1 {edge:.2f}%"
          + ("" if complete else "   ← PARCIAL, no es el resultado del panel"))

    run = {
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "panel": f"{len(panel)}_videos", "video_ids": panel, "complete": complete,
        "model": models[0] if len(models) == 1 else models,
        "temperature": None, "effort": sorted({m.get("effort") for m in metas if m.get("effort")}),
        "via": "claude -p (Claude Code, suscripción); una llamada sin historial ni herramientas por video",
        "system_prompt": SYSTEM_PROMPT, "git_commit": rp.git_commit(),
        "stage2_prompt": {"name": entry["name"], "file": entry["file"], "source_cell": entry.get("source_cell"),
                          "chars": entry["chars"], "sha256": entry["sha256"],
                          "matches_production": entry.get("matches_production", False)},
        "stage1_prompt": None,
        "oracle": {"name": ORACLE, "world_model_file": WM_NAME, "note": ORACLES[ORACLE]["note"]},
        "world_model_file": WM_NAME, "connection_evidence_enabled": False, "transcript_enabled": True,
        "usage": {"calls": len(metas),
                  "input_tokens": sum(m.get("input_tokens", 0) for m in metas),
                  "output_tokens": sum(m.get("output_tokens", 0) for m in metas),
                  "thinking_tokens": sum(m.get("thinking_tokens", 0) for m in metas),
                  "api_equivalent_cost_usd": round(sum(m.get("api_equivalent_cost_usd") or 0 for m in metas), 4)},
        "metrics": {"service_f1_mean": round(svc, 2), "edge_f1_mean": round(edge, 2), "n_success": len(rows)},
        "results": rows,
    }
    # run.json solo con el panel completo: un promedio parcial no se publica como resultado.
    name = "run.json" if complete else "run_parcial.json"
    (OUT / name).write_text(json.dumps(run, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    with open(OUT / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["video_id", "svc_f1", "edge_f1", "gen_nodes", "gt_nodes", "gen_edges", "gt_edges"])
        for r in rows:
            w.writerow([r["video_id"], f"{100*r['svc_f1']:.2f}", f"{100*r['edge_f1']:.2f}",
                        r["gen_nodes"], r["gt_nodes"], r["gen_edges"], r["gt_edges"]])
    print(f"✓ {name} y results.csv en {OUT.relative_to(PROJECT_ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Panel con Claude en Stage 2 vía `claude -p`")
    ap.add_argument("--panel", type=int, default=30, choices=sorted(rp.PANELS))
    ap.add_argument("--oracle", default="vision", choices=sorted(ORACLES),
                    help="World Model que entra a Stage 2: 'vision' (brazo A, transcripción "
                         "manual) u 'oracle_gt' (brazo B, ground truth convertido)")
    ap.add_argument("--prompt", default=PROMPT_FILE,
                    help="prompt de Stage 2 en src/configs/prompts/ (por defecto, el de producción)")
    ap.add_argument("--replicate", type=int, default=None, metavar="N",
                    help="repeticion N de la misma condicion, en su propio directorio (ruido test-retest)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("export").set_defaults(fn=cmd_export)
    r = sub.add_parser("run")
    r.add_argument("--model", default=DEFAULT_MODEL)
    r.add_argument("--effort", default=DEFAULT_EFFORT, choices=["low", "medium", "high", "xhigh", "max"])
    r.add_argument("--limit", type=int, default=None, help="correr solo los primeros N pendientes")
    r.add_argument("--videos", nargs="+", default=None)
    r.add_argument("--timeout", type=int, default=600)
    r.set_defaults(fn=cmd_run)
    sub.add_parser("evaluate").set_defaults(fn=cmd_evaluate)
    args = ap.parse_args()
    configure(args.oracle, args.prompt, args.replicate)
    args.fn(args)


if __name__ == "__main__":
    main()
