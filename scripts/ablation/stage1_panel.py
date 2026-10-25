#!/usr/bin/env python3
"""
stage1_panel.py — Cuánto de la pizarra alcanza a leer Stage 1, modelo por modelo.

Qué hace
--------
Corre solo Stage 1 (el World Model) sobre el panel con el modelo que se pida y lo compara
contra la transcripción manual de la misma pizarra (`world_model_vision.json`). Stage 2 no
interviene: lo que se mide es la lectura, no el grafo final.

Stage 1 se arma igual que en `rerun_panel.ensure_stage1` — prompt de producción verificado
por hash, bloque de símbolos del detector, URL y transcript — con dos diferencias a propósito:

  * lee la pizarra de `data/good_whiteboard/`, que es la que transcribió la persona y la que
    recibe Stage 2; `ensure_stage1` usa la copia de `lab_workspace`, que en dos videos del
    panel es otra imagen;
  * escribe `lab_workspace/<vid>/world_model_<nombre>.json`, nunca `world_model.json`, así
    que el cache de producción no se toca. Con ese nombre el archivo queda además usable
    como `--oracle <nombre>` en rerun_panel.py.

Cómo se compara
---------------
Un World Model se reduce a lo mismo que puntúa el evaluador: el multiconjunto de servicios
de sus entidades y el multiconjunto de pares (servicio origen, servicio destino) de sus
conexiones, resolviendo cada etiqueta contra el nombre o el servicio de una entidad. Se
reporta contra la transcripción manual (cuánto coincide con lo que leyó una persona) y
contra el ground truth (el techo que tendría Stage 2 si copiara ese World Model tal cual).

Uso
---
    .venv/Scripts/python scripts/ablation/stage1_panel.py run --model gemini-3.1-pro-preview --name s1-pro
    .venv/Scripts/python scripts/ablation/stage1_panel.py compare --names s1-flash s1-pro
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import statistics as st
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.ablation import rerun_panel as rp  # noqa: E402
from scripts.ablation.compare_models import bootstrap_ci, sign_test  # noqa: E402

OUT = PROJECT_ROOT / "reports" / "stage1_vs_manual"
MANUAL = "vision"                      # world_model_vision.json: la transcripción humana
STAGE1_PROMPT = "stage1_v0_baseline.txt"


def wm_path(vid: str, name: str) -> Path:
    return rp.LAB_WORKSPACE / vid / f"world_model_{name}.json"


# ── run ──────────────────────────────────────────────────────────────
def stage1_claude(claude: str, prompt: str, image: Path, model: str, effort: str, raw: Path, timeout: int) -> dict:
    """Stage 1 con Claude vía `claude -p`: la misma llamada sin historial ni herramientas que usa
    claude_panel.py para Stage 2, con el esquema del World Model como salida forzada."""
    from scripts.ablation import claude_panel as cp
    result = cp.call_claude(claude, prompt, image, model, effort, rp.WorldModelSchema.model_json_schema(), raw, timeout)
    if result.get("is_error") or result.get("subtype") not in (None, "success"):
        raise RuntimeError(f"{result.get('subtype')}: {str(result.get('result'))[:200]}")
    wm = result.get("structured_output")
    if wm is None:
        text = (result.get("result") or "").strip()
        if text.startswith("```"):
            text = text.strip("`").removeprefix("json").strip()
        wm = json.loads(text)
    rp.WorldModelSchema.model_validate(wm)
    return wm


def cmd_run(args) -> None:
    manifest = rp.load_manifest()
    tmpl, entry = rp.load_verified_prompt(STAGE1_PROMPT, manifest)
    aws_str, users_str, _ = rp.load_catalogs()
    panel = rp.PANELS[args.panel]
    pending = [v for v in panel if not wm_path(v, args.name).exists()]
    out = OUT / args.name
    out.mkdir(parents=True, exist_ok=True)
    print(f"Stage 1 · {args.model} · {entry['name']} ({entry['sha256'][:12]}) · "
          f"{len(pending)} de {len(panel)} pendientes → world_model_{args.name}.json")

    es_claude = args.model.startswith("claude")
    rot = rp.KeyRotator(rp.GEMINI_API_KEYS) if pending and not es_claude else None
    if es_claude:
        from scripts.ablation import claude_panel as cp
        claude_bin = cp.find_claude()
    p1 = tmpl.replace("<AWS_SERVICES_PLACEHOLDER>", aws_str).replace("<USER_ACTORS_PLACEHOLDER>", users_str)
    meta_path = out / "videos.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}

    for i, vid in enumerate(pending, 1):
        wb = rp.GOOD_WHITEBOARD_DIR / f"{vid}.jpg"
        # El detector escribe una copia procesada de la imagen: va a un directorio propio
        # para no pisar la que ya hay en lab_workspace.
        sym_dir = out / "_simbolos" / vid
        sym_dir.mkdir(parents=True, exist_ok=True)
        symbols = rp.detect_symbols(wb, sym_dir)
        parts = [p1] + ([symbols] if symbols else [])
        parts.append(f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={vid}")
        # `--no-transcript` deja a Stage 1 solo con la imagen, que es la condición en la que
        # se hizo la transcripción manual: así «solo lo ve el modelo» no puede venir del audio.
        transcript = "" if args.no_transcript else rp.read_transcript(vid)
        if transcript:
            parts.append(f"\n## FULL TRANSCRIPT:\n{transcript}")
        image = wb.read_bytes()
        try:
            if es_claude:
                wm = stage1_claude(claude_bin, "\n".join(parts), wb, args.model, args.effort,
                                   sym_dir / "claude_raw.jsonl", args.timeout)
            else:
                wm = rp.call_gemini(rot, "\n".join(parts), base64.b64encode(image).decode("utf-8"),
                                    args.model, schema=rp.WorldModelSchema)
        except rp.QuotaExhausted as e:
            print(f"🛑 {e}. Lo ya generado queda guardado; el mismo comando retoma.")
            break
        except Exception as e:
            print(f"[{i}/{len(pending)}] {vid}  ✗ {str(e)[:120]}")
            continue
        payload = json.dumps(wm, indent=2, ensure_ascii=False)
        wm_path(vid, args.name).write_text(payload, encoding="utf-8")
        meta[vid] = {"world_model_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                     "whiteboard_sha256": hashlib.sha256(image).hexdigest(),
                     "symbols_injected": bool(symbols), "transcript": bool(transcript),
                     "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[{i}/{len(pending)}] {vid}  ✓ {len(wm.get('entities', []))} entidades, "
              f"{len(wm.get('visual_connections', []))} conexiones")
        time.sleep(1.0)

    done = [v for v in panel if wm_path(v, args.name).exists()]
    (out / "run.json").write_text(json.dumps({
        "generated_on": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "panel": f"{len(panel)}_videos", "video_ids": panel, "complete": len(done) == len(panel),
        "model": args.model, "temperature": None if es_claude else 0.0, "git_commit": rp.git_commit(),
        "via": f"claude -p (Claude Code, suscripción), effort {args.effort}" if es_claude else "API de Gemini",
        "stage1_prompt": {"name": entry["name"], "file": entry["file"], "sha256": entry["sha256"]},
        "world_model_file": f"world_model_{args.name}.json",
        "whiteboard_source": "data/good_whiteboard/<vid>.jpg",
        "transcript_enabled": not args.no_transcript,
        "usage_this_invocation": rp.usage_summary(), "videos": meta,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(done)}/{len(panel)} World Models listos · {(out / 'run.json').relative_to(PROJECT_ROOT)}")
    if len(done) < len(panel):
        sys.exit(2)


# ── compare ──────────────────────────────────────────────────────────
def reducir(wm: dict) -> tuple[Counter, Counter, int]:
    """(servicios, pares de servicio, conexiones cuya etiqueta no resuelve a ninguna entidad)."""
    resolve: dict[str, str] = {}
    for e in wm.get("entities", []):
        for key in (e.get("name"), e.get("service")):
            if key:
                resolve.setdefault(key.strip().lower(), e["service"])
    pares, sin_resolver = Counter(), 0
    for c in wm.get("visual_connections", []):
        s = resolve.get((c.get("source_label") or "").strip().lower())
        t = resolve.get((c.get("target_label") or "").strip().lower())
        if s and t:
            pares[(s, t)] += 1
        else:
            sin_resolver += 1
    # Servicios como conjunto de tipos, que es como los puntúa el protocolo estricto.
    return Counter({e["service"] for e in wm.get("entities", [])}), pares, sin_resolver


def prf(gen: Counter, ref: Counter) -> tuple[float, float, float]:
    inter = sum((gen & ref).values())
    p = inter / sum(gen.values()) if gen else 0.0
    r = inter / sum(ref.values()) if ref else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def gt_reducido(vid: str) -> tuple[Counter, Counter]:
    G = nx.read_graphml(str(rp.GT_DIR / f"{vid}.graphml"))
    svc = lambda n: G.nodes[n].get("service", "?")
    return Counter({svc(n) for n in G.nodes}), Counter((svc(u), svc(v)) for u, v in G.edges())


def cmd_compare(args) -> None:
    panel = rp.PANELS[args.panel]
    names = args.names + [MANUAL]
    faltan = {n: [v for v in panel if not wm_path(v, n).exists()] for n in names}
    if any(faltan.values()):
        sys.exit("✗ Faltan World Models: " + "; ".join(f"{n}: {', '.join(v)}" for n, v in faltan.items() if v))

    rows = []
    for vid in panel:
        manual_wm = json.loads(wm_path(vid, MANUAL).read_text(encoding="utf-8"))
        manual_svc, manual_par, _ = reducir(manual_wm)
        gt_svc, gt_par = gt_reducido(vid)
        for n in names:
            wm = json.loads(wm_path(vid, n).read_text(encoding="utf-8"))
            svc, par, sin = reducir(wm)
            ps, rs, fs = prf(svc, manual_svc)
            pc, rc, fc = prf(par, manual_par)
            rows.append({"video_id": vid, "world_model": n,
                         "entidades": len(wm.get("entities", [])), "conexiones": sum(par.values()) + sin,
                         "conexiones_sin_resolver": sin,
                         "manual_entidades": len(manual_wm.get("entities", [])), "manual_conexiones": sum(manual_par.values()),
                         "svc_p_vs_manual": ps, "svc_r_vs_manual": rs, "svc_f1_vs_manual": fs,
                         "con_p_vs_manual": pc, "con_r_vs_manual": rc, "con_f1_vs_manual": fc,
                         "svc_f1_vs_gt": prf(svc, gt_svc)[2], "con_f1_vs_gt": prf(par, gt_par)[2],
                         "gt_nodos": nx.read_graphml(str(rp.GT_DIR / f"{vid}.graphml")).number_of_nodes(), "gt_aristas": sum(gt_par.values())})

    by = {n: {r["video_id"]: r for r in rows if r["world_model"] == n} for n in names}
    mean = lambda n, k: st.mean(by[n][v][k] for v in panel)
    lines = [f"# Stage 1 contra la transcripción manual — panel de {len(panel)}", "",
             "Cada World Model se reduce a servicios y pares de servicio, igual que el evaluador. "
             "«vs manual» mide cuánto coincide con lo que una persona leyó en la pizarra; "
             "«vs GT» es el techo que tendría Stage 2 si copiara ese World Model sin tocarlo.", "",
             "| World Model | entidades | conexiones | sin resolver | servicios F1 vs manual | conexiones P / R / F1 vs manual | servicios F1 vs GT | conexiones F1 vs GT |",
             "|---|---:|---:|---:|---:|:---:|---:|---:|"]
    for n in names:
        lines.append(f"| `{n}` | {mean(n, 'entidades'):.2f} | {mean(n, 'conexiones'):.2f} | "
                     f"{sum(by[n][v]['conexiones_sin_resolver'] for v in panel)} | "
                     f"{100 * mean(n, 'svc_f1_vs_manual'):.2f} | "
                     f"{100 * mean(n, 'con_p_vs_manual'):.1f} / {100 * mean(n, 'con_r_vs_manual'):.1f} / "
                     f"{100 * mean(n, 'con_f1_vs_manual'):.2f} | "
                     f"{100 * mean(n, 'svc_f1_vs_gt'):.2f} | {100 * mean(n, 'con_f1_vs_gt'):.2f} |")
    gt_n = st.mean(by[MANUAL][v]["gt_nodos"] for v in panel)
    gt_e = st.mean(by[MANUAL][v]["gt_aristas"] for v in panel)
    lines += ["", f"Ground truth: {gt_n:.2f} nodos y {gt_e:.2f} aristas por arquitectura.", "",
              "## Diferencias pareadas (B − A)", "",
              "| A | B | métrica | Δ | IC 95 % | gana B / gana A / empate | p (signos) |",
              "|---|---|---|---:|:---:|:---:|---:|"]
    pares, out_pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]], []
    for a, b in pares:
        for k, etiqueta in (("con_f1_vs_manual", "conexiones F1 vs manual"), ("svc_f1_vs_manual", "servicios F1 vs manual"),
                            ("con_f1_vs_gt", "conexiones F1 vs GT"), ("svc_f1_vs_gt", "servicios F1 vs GT")):
            if MANUAL in (a, b) and k.endswith("vs_manual"):
                continue                      # la manual contra sí misma es 100 por construcción
            d = [100 * (by[b][v][k] - by[a][v][k]) for v in panel]
            lo, hi = bootstrap_ci(d)
            pos, neg, ties, p = sign_test(d)
            lines.append(f"| `{a}` | `{b}` | {etiqueta} | {st.mean(d):+.2f} | [{lo:+.2f}, {hi:+.2f}] | "
                         f"{pos} / {neg} / {ties} | {p:.3f} |")
            out_pairs.append({"a": a, "b": b, "metric": k, "diff": st.mean(d), "ci95": [lo, hi],
                              "b_wins": pos, "a_wins": neg, "ties": ties, "sign_p": p})

    OUT.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + "\n"
    print(text)
    (OUT / "comparacion.md").write_text(text, encoding="utf-8")
    (OUT / "comparacion.json").write_text(json.dumps(
        {"panel": panel, "world_models": names, "reference": MANUAL, "pairs": out_pairs, "rows": rows},
        indent=2, ensure_ascii=False), encoding="utf-8")
    with open(OUT / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"✓ comparacion.md, comparacion.json y results.csv en {OUT.relative_to(PROJECT_ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Stage 1 por modelo, contra la transcripción manual")
    ap.add_argument("--panel", type=int, default=30, choices=sorted(rp.PANELS))
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--model", required=True)
    r.add_argument("--name", required=True, help="sufijo del archivo: world_model_<name>.json")
    r.add_argument("--no-transcript", action="store_true",
                   help="Stage 1 recibe solo la imagen de la pizarra, sin el transcript del audio")
    r.set_defaults(fn=cmd_run)
    r.add_argument("--effort", default="high", help="solo para modelos Claude")
    r.add_argument("--timeout", type=int, default=600, help="segundos por video, solo para modelos Claude")
    c = sub.add_parser("compare")
    c.add_argument("--names", nargs="+", required=True, help="World Models a comparar contra la manual")
    c.set_defaults(fn=cmd_compare)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
