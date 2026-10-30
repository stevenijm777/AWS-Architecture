#!/usr/bin/env python3
"""
linea_base.py — Configuración 1: Standard (V6 producción) con el modelo del config, en las dos etapas.

La línea base del paper (58,99 en el panel) es de gemini-3.6-flash, con un World Model de
Stage 1 cacheado en lab_workspace/. Comparar el multiagente (3.8) contra eso mezcla modelo y
arquitectura, así que aquí se re-corren ambas etapas con el mismo modelo del multiagente:

  Stage 1  stage1_v0_baseline.txt (hash verificado) + símbolos + transcripción, con la pizarra
           de data/good_whiteboard/. Se guarda en reports/multiagente/<etiqueta>/stage1/<vid>/,
           sin tocar las cachés de lab_workspace/.
  Stage 2  stage2_v6_corrected__cell9.txt vía `run_video` de rerun_panel, leyendo ese World
           Model. Mismo armado de prompt, mismo evaluador.

Reanuda: un World Model ya guardado no se repite y un video ya evaluado no se repaga.

    .venv/Scripts/python -m multiagent.linea_base --max-llamadas 60
"""
from __future__ import annotations

import argparse
import base64
import json
import shutil
from datetime import datetime

from config.settings import GEMINI_API_KEYS
from multiagent.llm import CONFIG, ruta
from scripts.ablation.rerun_panel import (
    GOOD_WHITEBOARD_DIR, PANEL_30, USAGE, KeyRotator, QuotaExhausted, WorldModelSchema,
    call_gemini, detect_symbols, git_commit, load_catalogs, load_manifest, load_verified_prompt,
    read_transcript, run_video, usage_summary,
)

STAGE1, STAGE2 = "stage1_v0_baseline.txt", "stage2_v6_corrected__cell9.txt"


def main() -> None:
    ap = argparse.ArgumentParser(description="Standard con el modelo del multiagente, ambas etapas")
    ap.add_argument("--videos", nargs="+", default=PANEL_30)
    ap.add_argument("--max-llamadas", type=int, default=60)
    ap.add_argument("--etiqueta", default=None)
    args = ap.parse_args()

    modelo = CONFIG["modelo"]
    etiqueta = args.etiqueta or f"standard_v6_{modelo}" + ("_p30" if args.videos == PANEL_30 else "")
    salida = ruta("salida") / etiqueta
    (salida / "stage1").mkdir(parents=True, exist_ok=True)
    run_path = salida / "run.json"

    manifest = load_manifest()
    s1_tmpl, s1_entry = load_verified_prompt(STAGE1, manifest)
    s2_tmpl, s2_entry = load_verified_prompt(STAGE2, manifest)
    aws, actores, catalogo = load_catalogs()

    previas = json.loads(run_path.read_text(encoding="utf-8"))["results"] if run_path.exists() else []
    filas = {r["video_id"]: r for r in previas if r.get("status") == "success"}
    meta = {"config": "1_standard", "modelo": modelo, "stage1": {"file": STAGE1, "sha256": s1_entry["sha256"]},
            "stage2": {"file": STAGE2, "sha256": s2_entry["sha256"]}, "commit": git_commit(),
            "inicio": datetime.now().isoformat(timespec="seconds")}

    rot = KeyRotator(GEMINI_API_KEYS)
    nuevas = 0

    def guardar() -> None:
        orden = [filas[v] for v in args.videos if v in filas]
        run_path.write_text(json.dumps({**meta, "uso": usage_summary(), "results": orden}, indent=1,
                                       ensure_ascii=False, default=str), encoding="utf-8")

    for i, vid in enumerate(args.videos, 1):
        if vid in filas:
            continue
        carpeta = salida / "stage1" / vid
        carpeta.mkdir(parents=True, exist_ok=True)
        wm_path = carpeta / "world_model.json"
        pendientes = (0 if wm_path.exists() else 1) + 1
        if nuevas + pendientes > args.max_llamadas:
            print(f"[{i}/{len(args.videos)}] {vid}: DETENIDO — tope de {args.max_llamadas} llamadas nuevas")
            break
        try:
            if not wm_path.exists():
                wb = carpeta / "best_whiteboard.jpg"
                shutil.copy2(GOOD_WHITEBOARD_DIR / f"{vid}.jpg", wb)
                partes = [s1_tmpl.replace("<AWS_SERVICES_PLACEHOLDER>", aws)
                          .replace("<USER_ACTORS_PLACEHOLDER>", actores)]
                simbolos = detect_symbols(wb, carpeta)
                if simbolos:
                    partes.append(simbolos)
                partes.append(f"\n## VIDEO URL:\nhttps://www.youtube.com/watch?v={vid}")
                t = read_transcript(vid)
                if t:
                    partes.append(f"\n## FULL TRANSCRIPT:\n{t}")
                wm = call_gemini(rot, "\n".join(partes), base64.b64encode(wb.read_bytes()).decode(),
                                 modelo, schema=WorldModelSchema)
                nuevas += 1
                wm_path.write_text(json.dumps(wm, indent=2, ensure_ascii=False), encoding="utf-8")
            # run_video arma LAB_WORKSPACE / vid / wm_name; con una ruta absoluta, pathlib la toma tal cual.
            fila = run_video(vid, s2_tmpl, rot, modelo, aws, actores, catalogo, wm_name=str(wm_path.resolve()))
            nuevas += 1
        except QuotaExhausted as e:
            print(f"[{i}/{len(args.videos)}] {vid}: DETENIDO — {e}")
            break
        except Exception as e:
            print(f"[{i}/{len(args.videos)}] {vid}: error — {type(e).__name__}: {str(e)[:200]}")
            continue
        filas[vid] = fila
        guardar()
        print(f"[{i}/{len(args.videos)}] {vid}: svc {100*fila['svc_f1']:.1f}  edge {100*fila['edge_f1']:.1f}  "
              f"aristas {fila['gen_edges']}/{fila['gt_edges']}  (llamadas nuevas {nuevas})")

    meta["fin"] = datetime.now().isoformat(timespec="seconds")
    guardar()
    ok = list(filas.values())
    u = usage_summary()
    usd = (u["input_tokens"] * 0.75 + (u["output_tokens"] + u["thinking_tokens"]) * 3.75) / 1e6
    if ok:
        print(f"\n{etiqueta}: {len(ok)}/{len(args.videos)} · svc {100*sum(r['svc_f1'] for r in ok)/len(ok):.2f}"
              f" · edge {100*sum(r['edge_f1'] for r in ok)/len(ok):.2f} · llamadas nuevas {nuevas} · ${usd:.2f}")


if __name__ == "__main__":
    main()
