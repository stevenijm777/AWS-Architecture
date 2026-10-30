#!/usr/bin/env python3
"""
orquestador.py — Corre una configuración del sistema multiagente sobre una lista de videos.

  A1 ─┐
      ├─ C1 ─ A3 ─ C2 ─ C3 ─┬─ export (.graphml + procedencia)
  A2 ─┘                     └─ A4 (si C3 o C2 avisan, una vuelta) ─ C3 ─ export

Configuraciones (la 1, Standard, se corre con rerun_panel; ver README):
  completo        3 · sistema completo
  sin_a2          4 · sin narración
  sin_c2          5 · sin reglas de convención
  sin_a4          6 · sin crítico (sale gratis de la caché de `completo`)
  unica           2 · una sola llamada con pizarra y transcripción, más C2 y C3 en código
  brazo_b         7 · el GT reemplaza a A1 (sin llamada), con C2
  brazo_b_sin_c2      el mismo brazo B sin C2, para aislar el efecto de las reglas
  brazo_b_sin_a4      el brazo B sin crítico (A4 no corrigió nada en el panel con `completo`)

Salida en reports/multiagente/<etiqueta>/: <vid>/ con cada paso intermedio, el .graphml y la
procedencia, y run.json con una fila por video (compatible con compare_models.py).

    .venv/Scripts/python -m multiagent.orquestador --config completo --videos ID1 ID2
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime
from pathlib import Path

from multiagent import agentes, c1_normalizador, c2_reglas, c3_validacion
from multiagent.evaluar import evaluar, uso
from multiagent.llm import CONFIG, Cliente, TopeDeLlamadas, ruta
from scripts.ablation.rerun_panel import PANEL_30, QuotaExhausted, git_commit

CONFIGS = {
    "completo":       {"a2": True,  "c2": True,  "a4": True},
    "sin_a2":         {"a2": False, "c2": True,  "a4": True},
    "sin_c2":         {"a2": True,  "c2": False, "a4": True},
    "sin_a4":         {"a2": True,  "c2": True,  "a4": False},
    "unica":          {"unica": True, "a2": False, "c2": True, "a4": False},
    "brazo_b":        {"a2": True,  "c2": True,  "a4": True, "brazo_b": True},
    "brazo_b_sin_c2": {"a2": True,  "c2": False, "a4": True, "brazo_b": True},
    "brazo_b_sin_a4": {"a2": True,  "c2": True,  "a4": False, "brazo_b": True},
}


def guardar(carpeta: Path, nombre: str, datos) -> None:
    (carpeta / f"{nombre}.json").write_text(json.dumps(datos, indent=1, ensure_ascii=False), encoding="utf-8")


def procesar(vid: str, flags: dict, cli: Cliente, carpeta: Path, k: int) -> dict:
    carpeta.mkdir(parents=True, exist_ok=True)
    n0 = len(cli.registros)
    versiones = {}

    if flags.get("unica"):
        grafo, versiones["unica"] = agentes.unica(cli, vid, k)
        norm = None
    else:
        if flags.get("brazo_b"):
            lectura, versiones["a1"] = agentes.lectura_desde_gt(vid), "gt"
        else:
            lectura, versiones["a1"] = agentes.a1(cli, vid, k)
        narracion = None
        if flags["a2"]:
            narracion, versiones["a2"] = agentes.a2(cli, vid)
        guardar(carpeta, "a1", lectura)
        guardar(carpeta, "a2", narracion)
        norm = c1_normalizador.normalizar(lectura, narracion)
        guardar(carpeta, "c1", norm)
        grafo, versiones["a3"] = agentes.a3(cli, vid, norm)
    guardar(carpeta, "unica" if flags.get("unica") else "a3", grafo)

    cambios, ambiguos = [], []
    if flags["c2"]:
        grafo, cambios, ambiguos = c2_reglas.aplicar(grafo)
    guardar(carpeta, "c2", {"cambios": cambios, "ambiguos": ambiguos})

    grafo, problemas = c3_validacion.validar(grafo)
    critica, hechas = None, []
    avisos = [p for p in problemas if p["tipo"] in c3_validacion.DISPARAN_A4] + \
             [{"tipo": "par_ambiguo", **a} for a in ambiguos]
    if flags.get("a4") and avisos:
        critica, versiones["a4"] = agentes.a4(cli, vid, grafo, avisos, norm)
        grafo, hechas = agentes.aplicar_correcciones(grafo, critica)
        grafo, problemas_finales = c3_validacion.validar(grafo)
    else:
        problemas_finales = problemas
    guardar(carpeta, "c3", {"problemas": problemas, "avisos_a4": avisos, "critica": critica,
                            "correcciones": hechas, "problemas_finales": problemas_finales})

    G, _ = c3_validacion.exportar(grafo, vid, carpeta)
    fila = evaluar(vid, G, grafo, cli.registros[n0:])
    fila.update({"prompts": versiones, "reglas_c2": len(cambios), "a4_corrio": critica is not None,
                 "correcciones_aplicadas": sum(h["aplicada"] for h in hechas)})
    return fila


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--config", required=True, choices=CONFIGS)
    ap.add_argument("--videos", nargs="+", help="ids; o --panel")
    ap.add_argument("--panel", action="store_true", help="los 30 de PANEL_30")
    ap.add_argument("--replica", type=int, default=0, help="0 = normal; 1..n = réplicas sin caché")
    ap.add_argument("--k", type=int, default=CONFIG["k"])
    ap.add_argument("--max-llamadas", type=int, default=CONFIG["max_llamadas"])
    ap.add_argument("--etiqueta", default=None)
    args = ap.parse_args()

    vids = PANEL_30 if args.panel else args.videos
    if not vids:
        sys.exit("Indicar --videos o --panel")
    flags = {**CONFIG["agentes"], **CONFIGS[args.config]}
    cfg = copy.deepcopy(CONFIG)
    cfg["max_llamadas"] = args.max_llamadas
    cli = Cliente(cfg, replica=args.replica)

    etiqueta = args.etiqueta or (f"{args.config}_k{args.k}" + (f"_rep{args.replica}" if args.replica else "")
                                 + ("_p30" if args.panel else ""))
    salida = ruta("salida") / etiqueta
    salida.mkdir(parents=True, exist_ok=True)
    meta = {"config": args.config, "flags": flags, "modelo": cli.modelo, "k": args.k,
            "replica": args.replica, "commit": git_commit(), "inicio": datetime.now().isoformat(timespec="seconds")}

    filas = []
    for i, vid in enumerate(vids, 1):
        try:
            fila = procesar(vid, flags, cli, salida / vid, args.k)
        except (TopeDeLlamadas, QuotaExhausted) as e:
            print(f"[{i}/{len(vids)}] {vid}: DETENIDO — {e}")
            filas.append({"video_id": vid, "status": "pendiente", "error": str(e)})
            break
        except Exception as e:  # un video que falla no tira la corrida
            print(f"[{i}/{len(vids)}] {vid}: error — {type(e).__name__}: {str(e)[:200]}")
            filas.append({"video_id": vid, "status": "error", "error": f"{type(e).__name__}: {e}"})
            continue
        filas.append(fila)
        print(f"[{i}/{len(vids)}] {vid}: svc {100*fila['svc_f1']:.1f}  edge {100*fila['edge_f1']:.1f}  "
              f"aristas {fila['gen_edges']}/{fila['gt_edges']}  llamadas {fila['uso']['llamadas']} "
              f"({fila['uso']['nuevas']} nuevas)  ${fila['uso']['usd']:.3f}")
        (salida / "run.json").write_text(json.dumps({**meta, "uso_total": uso(cli.registros), "results": filas},
                                                    indent=1, ensure_ascii=False, default=str), encoding="utf-8")

    meta["fin"] = datetime.now().isoformat(timespec="seconds")
    (salida / "run.json").write_text(json.dumps({**meta, "uso_total": uso(cli.registros), "results": filas},
                                                indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    ok = [f for f in filas if f["status"] == "success"]
    if ok:
        print(f"\n{etiqueta}: {len(ok)}/{len(vids)} videos · svc {100*sum(f['svc_f1'] for f in ok)/len(ok):.2f}"
              f" · edge {100*sum(f['edge_f1'] for f in ok)/len(ok):.2f} · llamadas nuevas {cli.nuevas}"
              f" · ${uso(cli.registros)['usd']:.3f}")


if __name__ == "__main__":
    main()
