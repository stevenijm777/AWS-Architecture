#!/usr/bin/env python3
"""
compare_models.py — Comparación pareada de dos corridas del panel (p. ej. Pro vs Flash).

Qué compara
-----------
Dos `run.json` de `rerun_panel.py` sobre el mismo panel, el mismo prompt de Stage 2 y el
mismo World Model de Stage 1 cacheado. Lo único que cambia es el modelo de Stage 2, así
que la diferencia por video es atribuible a eso (más el ruido de muestreo del modelo).

Cómo decide si "influye"
------------------------
Una sola corrida por modelo no separa efecto de ruido. Por eso reporta tres cosas:

  * la diferencia media pareada con IC 95 % por bootstrap sobre videos;
  * una prueba de signos exacta (no supone normalidad; los empates se descartan);
  * la comparación contra el piso de ruido del propio panel: la dispersión entre
    réplicas de Flash con el mismo prompt (`--noise` acepta esas corridas). Si la
    diferencia Pro − Flash cabe dentro de lo que Flash difiere de sí mismo, no hay
    evidencia de efecto.

Uso
---
    .venv/Scripts/python scripts/ablation/compare_models.py \\
        --a reports/pro_vs_flash/flash_gemini-3.6-flash \\
        --b reports/pro_vs_flash/pro_gemini-3.1-pro-preview \\
        --noise "reports/ablation/*STAGE2_V6_CORRECTED_cell9_p30" \\
                "reports/ablation/*STAGE2_V6_CORRECTED_cell9_p30_rep[0-9]" \\
        --out reports/pro_vs_flash
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import random
import statistics as st
from pathlib import Path

METRICS = [("svc_f1", "Service F1"), ("edge_f1", "Edge F1")]


def load_run(path: str) -> dict:
    p = Path(path)
    p = p / "run.json" if p.is_dir() else p
    run = json.loads(p.read_text(encoding="utf-8"))
    run["_path"] = str(p.parent)
    run["_by_id"] = {r["video_id"]: r for r in run.get("results", []) if r.get("status") == "success"}
    return run


def bootstrap_ci(d: list[float], n: int = 20_000, seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    k = len(d)
    means = sorted(sum(rng.choice(d) for _ in range(k)) / k for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]


def sign_test(d: list[float]) -> tuple[int, int, int, float]:
    """Prueba de signos exacta bilateral. Devuelve (gana B, gana A, empates, p)."""
    pos = sum(1 for x in d if x > 1e-12)
    neg = sum(1 for x in d if x < -1e-12)
    n = pos + neg
    if n == 0:
        return pos, neg, len(d), 1.0
    k = min(pos, neg)
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    return pos, neg, len(d) - n, p


def paired(a: dict, b: dict, key: str, ids: list[str]) -> list[float]:
    return [100 * (b["_by_id"][v][key] - a["_by_id"][v][key]) for v in ids]


def main() -> None:
    ap = argparse.ArgumentParser(description="Comparación pareada de dos corridas del panel")
    ap.add_argument("--a", required=True, help="corrida de referencia (dir o run.json)")
    ap.add_argument("--b", required=True, help="corrida a comparar; se reporta B − A")
    ap.add_argument("--noise", nargs="*", default=[],
                    help="globs de corridas réplica del modelo A, para el piso de ruido")
    ap.add_argument("--exclude", nargs="*", default=[],
                    help="video_ids a excluir del piso de ruido (p. ej. Stage 1 regenerado)")
    ap.add_argument("--out", default=None, help="directorio donde escribir comparacion.md/.json")
    args = ap.parse_args()

    A, B = load_run(args.a), load_run(args.b)
    ids = [v for v in A["video_ids"] if v in A["_by_id"] and v in B["_by_id"]]

    checks = {
        "mismo panel": A["video_ids"] == B["video_ids"],
        "mismo prompt Stage 2": A["stage2_prompt"]["sha256"] == B["stage2_prompt"]["sha256"],
        "mismo World Model por video": all(
            A["_by_id"][v].get("stage1_cached_at") == B["_by_id"][v].get("stage1_cached_at") for v in ids),
        "misma pizarra por video": all(
            A["_by_id"][v].get("whiteboard_sha256") == B["_by_id"][v].get("whiteboard_sha256") for v in ids),
        "panel completo en ambas": len(ids) == len(A["video_ids"]),
    }

    # Piso de ruido: réplicas del modelo A contra la propia corrida A.
    noise_runs = []
    for g in args.noise:
        for p in sorted(glob.glob(g)):
            if not (Path(p) / "run.json").exists():
                continue
            r = load_run(p)
            # Otros artefactos del directorio (auditorías) no son corridas de Stage 2.
            if (r.get("model") == A["model"]
                    and (r.get("stage2_prompt") or {}).get("sha256") == A["stage2_prompt"]["sha256"]
                    and r.get("video_ids") == A["video_ids"] and not r.get("oracle")
                    and r.get("transcript_enabled", True) and not r.get("connection_evidence_enabled")
                    and Path(r["_path"]).resolve() != Path(A["_path"]).resolve()):
                noise_runs.append(r)
    noise_ids = [v for v in ids if v not in set(args.exclude)]

    out = {"a": {"model": A["model"], "path": A["_path"]}, "b": {"model": B["model"], "path": B["_path"]},
           "n_videos": len(ids), "checks": checks, "metrics": {}, "noise_runs": [r["_path"] for r in noise_runs],
           "noise_excluded": args.exclude}
    lines = [f"# {B['model']} vs {A['model']} — panel de {len(ids)} videos", "",
             f"Stage 2: `{A['stage2_prompt']['name']}` (sha `{A['stage2_prompt']['sha256'][:12]}`), "
             f"temperatura 0, mismo World Model de Stage 1 para ambos modelos.", "",
             "## Controles", ""]
    lines += [f"- {'✓' if ok else '✗'} {name}" for name, ok in checks.items()]
    lines += ["", "## Resultado", "",
              f"| métrica | {A['model']} | {B['model']} | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |",
              "|---|---:|---:|---:|:---:|:---:|---:|"]

    for key, name in METRICS:
        a_mean = 100 * st.mean(A["_by_id"][v][key] for v in ids)
        b_mean = 100 * st.mean(B["_by_id"][v][key] for v in ids)
        d = paired(A, B, key, ids)
        lo, hi = bootstrap_ci(d)
        pos, neg, ties, p = sign_test(d)
        m = {"a_mean": a_mean, "b_mean": b_mean, "diff": st.mean(d), "ci95": [lo, hi],
             "sd_diff": st.stdev(d), "b_wins": pos, "a_wins": neg, "ties": ties, "sign_p": p}
        lines.append(f"| {name} | {a_mean:.2f} | {b_mean:.2f} | {st.mean(d):+.2f} | "
                     f"[{lo:+.2f}, {hi:+.2f}] | {pos} / {neg} / {ties} | {p:.3f} |")
        if noise_runs:
            nd = [st.mean(paired(A, r, key, noise_ids)) for r in noise_runs]
            sds = [st.stdev(paired(A, r, key, noise_ids)) for r in noise_runs]
            means = [100 * st.mean(r["_by_id"][v][key] for v in noise_ids) for r in noise_runs]
            m["noise"] = {"replica_minus_a": nd, "sd_paired_diff": sds, "replica_means": means,
                          "a_mean_same_ids": 100 * st.mean(A["_by_id"][v][key] for v in noise_ids),
                          "b_mean_same_ids": 100 * st.mean(B["_by_id"][v][key] for v in noise_ids),
                          "b_minus_a_same_ids": st.mean(paired(A, B, key, noise_ids))}
        out["metrics"][key] = m

    if noise_runs:
        lines += ["", f"## Piso de ruido ({len(noise_runs)} réplicas de {A['model']}, mismo prompt"
                      + (f", sin {', '.join(args.exclude)}" if args.exclude else "") + ")", "",
                  "Cuánto difiere Flash de sí mismo entre corridas, sobre los mismos videos. "
                  "La diferencia entre modelos solo cuenta como efecto si sale de este rango.", "",
                  "| métrica | medias de las réplicas | réplica − A (rango) | B − A en esos videos | ¿|B − A| supera al mayor |réplica − A|? |",
                  "|---|---|:---:|---:|:---:|"]
        for key, name in METRICS:
            n = out["metrics"][key]["noise"]
            lo, hi = min(n["replica_minus_a"]), max(n["replica_minus_a"])
            ba = n["b_minus_a_same_ids"]
            # En magnitud: ¿B se aleja de A más de lo que cualquier réplica de A se aleja de A?
            outside = abs(ba) > max(abs(lo), abs(hi))
            n["outside_noise_range"] = outside
            lines.append(f"| {name} | {', '.join(f'{x:.2f}' for x in n['replica_means'])} | "
                         f"[{lo:+.2f}, {hi:+.2f}] | {ba:+.2f} | {'sí' if outside else 'no'} |")

    lines += ["", "## Por video (Edge F1, ordenado por diferencia)", "",
              f"| video | {A['model']} | {B['model']} | Δ | aristas A | aristas B | aristas GT |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for v in sorted(ids, key=lambda v: B["_by_id"][v]["edge_f1"] - A["_by_id"][v]["edge_f1"]):
        ra, rb = A["_by_id"][v], B["_by_id"][v]
        lines.append(f"| `{v}` | {100*ra['edge_f1']:.1f} | {100*rb['edge_f1']:.1f} | "
                     f"{100*(rb['edge_f1']-ra['edge_f1']):+.1f} | {ra['gen_edges']} | {rb['gen_edges']} | {ra['gt_edges']} |")

    text = "\n".join(lines) + "\n"
    print(text)
    if args.out:
        d = Path(args.out)
        d.mkdir(parents=True, exist_ok=True)
        (d / "comparacion.md").write_text(text, encoding="utf-8")
        (d / "comparacion.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
