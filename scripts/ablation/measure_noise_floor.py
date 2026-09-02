#!/usr/bin/env python3
"""
measure_noise_floor.py — ¿Cuánta diferencia produce un prompt consigo mismo?

Por qué existe
--------------
La regla heredada "una diferencia menor a ~3 puntos no es señal" viene de una
sola observación: V0 re-corrido en gemini-3.5-flash dio 90.88 y luego 87.90.
Un único par no estima una distribución, y además se midió en otro modelo y a
otra temperatura. Aplicarla a gemini-3.6-flash a temperatura 0.0 es una
extrapolación, no una medición.

Resulta que la medición ya está pagada. El panel de 14 es un subconjunto exacto
del de 30, y nueve prompts se corrieron en ambos paneles en fechas distintas.
Restringiendo cada corrida de 30 a esos mismos 14 videos, cada prompt queda con
**dos ejecuciones independientes sobre entradas idénticas** — mismo whiteboard
(sha verificado), mismo World Model de Stage 1 (mismo timestamp de caché), mismo
modelo, misma temperatura. La única diferencia es el momento de la llamada.

Eso es un estudio test-retest de 9 pares y 126 observaciones pareadas por video,
donde la diferencia verdadera es exactamente cero por construcción. Todo lo que
se mida acá es ruido.

Qué reporta
-----------
1. Determinismo: ¿temperatura 0.0 devuelve el mismo JSON dos veces?
2. Piso de ruido empírico: distribución de |Δ media| entre un prompt y sí mismo.
3. sigma_d: desvío de la diferencia pareada por video, la cantidad que gobierna
   la potencia de cualquier comparación futura.
4. MDE: el efecto mínimo detectable con n=14 y n=30 al 80% de potencia — el
   número que reemplaza a la regla de los 3 puntos.
5. Tasa de falsos positivos de la prueba de signos sobre pares nulos.

No cuesta ninguna llamada a la API.

Uso
---
    .venv/bin/python scripts/ablation/measure_noise_floor.py
"""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import numpy as np  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

console = Console()
OUT = PROJECT_ROOT / "reports" / "noise_floor.json"

# (1.96 + 0.8416): z de dos colas al 5% más z de una cola al 80% de potencia.
Z_MDE = 2.8016


def sign_test(w: int, l: int) -> float:
    n = w + l
    if n == 0:
        return 1.0
    k = min(w, l)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def load_runs() -> dict[str, dict]:
    runs = {}
    for rj in sorted(glob.glob(str(PROJECT_ROOT / "reports/ablation/*/run.json"))):
        d = json.load(open(rj))
        if not any(r.get("status") == "success" for r in d["results"]):
            continue
        runs[os.path.basename(os.path.dirname(rj))] = d
    return runs


def comparable(d: dict) -> bool:
    """¿Esta corrida puede emparejarse con otra del mismo prompt como réplica nula?

    Dos corridas sólo miden ruido si difieren *únicamente* en la llamada al modelo.
    El sha256 del prompt no alcanza para garantizarlo, y hay dos formas de romperlo:

    - `connection_evidence_enabled` agrega evidencia de conexiones al contexto.
    - `oracle` reemplaza el world model de Stage 1 por otro —el ground truth, o una
      transcripción hecha a mano—. Lleva el mismo prompt de Stage 2, así que se cuela
      como si fuera una repetición, pero recibió una entrada distinta: emparejarla
      con producción mide el efecto del oráculo y lo reporta como ruido.

    Esto último pasó de verdad: al aparecer la corrida del oráculo, sigma_d de Edge
    saltó de 8.76 a 11.71 y tres comparaciones nulas dieron significativas. Lo detectó
    correr el script dentro del repositorio publicable y comparar contra el resultado
    ya establecido.

    Ojo con `world_model_file`: una versión anterior de este guard lo usaba como señal
    de oráculo, y es incorrecto. Las corridas normales también lo graban, con el valor
    por defecto `world_model.json`; solo las de oráculo apuntan a otro archivo, y esas
    ya quedan atrapadas por la clave `oracle`. Filtrar por `world_model_file` excluía
    réplicas legítimas (rep3, rep4) y dejaba el piso de ruido con 2 pares en vez de 6,
    subiendo sigma_d de 6.43 a 10.31 — el mismo tipo de error que el guard busca evitar,
    en la dirección opuesta.

    `transcript_enabled=False` sí excluye: quitar la transcripción del contexto cambia
    la entrada, no el prompt. Es una ablación de información, hermana de las de oráculo.
    """
    if d.get("connection_evidence_enabled"):
        return False
    if d.get("oracle"):
        return False
    if d.get("transcript_enabled") is False:
        return False
    return True


def find_replicates(runs: dict[str, dict], min_common: int = 14) -> list[tuple[str, str, str]]:
    """Todo par de corridas del mismo prompt, comparadas sobre los videos que comparten.

    Cubre dos fuentes: las réplicas cruzadas panel-14/panel-30 (el de 14 es un
    subconjunto exacto del de 30, así que restringir da entradas idénticas) y las
    réplicas explícitas hechas con `--replicate`.
    """
    by_sha: dict[str, list[str]] = defaultdict(list)
    for name, d in runs.items():
        if not comparable(d):
            continue
        by_sha[d["stage2_prompt"]["sha256"][:10]].append(name)

    out = []
    for sha, names in sorted(by_sha.items()):
        for i, a in enumerate(sorted(names)):
            for b in sorted(names)[i + 1:]:
                common = set(runs[a]["video_ids"]) & set(runs[b]["video_ids"])
                if len(common) >= min_common:
                    out.append((sha, a, b))
    return out


def canonical(analysis) -> str:
    return json.dumps(analysis, sort_keys=True, ensure_ascii=False)


def main() -> None:
    runs = load_runs()
    reps = find_replicates(runs)
    if not reps:
        console.print("[red]No hay prompts corridos en ambos paneles.[/]")
        return

    # Verificación de que las entradas fueron realmente idénticas. Sin esto, una
    # diferencia podría venir de un whiteboard recortado distinto o de un Stage 1
    # regenerado, y ya no mediría ruido del modelo.
    mismatches = []
    for sha, a, b in reps:
        ra = {r["video_id"]: r for r in runs[a]["results"] if r.get("status") == "success"}
        rb = {r["video_id"]: r for r in runs[b]["results"] if r.get("status") == "success"}
        for vid in sorted(set(ra) & set(rb)):
            if ra[vid]["whiteboard_sha256"] != rb[vid]["whiteboard_sha256"]:
                mismatches.append((sha, vid, "whiteboard"))
            if ra[vid].get("stage1_cached_at") != rb[vid].get("stage1_cached_at"):
                mismatches.append((sha, vid, "stage1"))
    temps = {d.get("temperature") for d in runs.values()}
    models = {d.get("model") for d in runs.values()}
    console.print(f"[bold]Réplicas encontradas:[/] {len(reps)} pares del mismo prompt  ·  "
                  f"modelo {'/'.join(sorted(map(str, models)))}  ·  temperatura "
                  f"{'/'.join(sorted(map(str, temps)))}")
    console.print(f"Entradas idénticas verificadas (whiteboard sha + caché Stage 1): "
                  f"{'[green]sí[/]' if not mismatches else f'[red]{len(mismatches)} discrepancias[/]'}\n")

    per_pair, pooled_d, ident_json, ident_f1, n_vids = [], {"svc": [], "edge": []}, 0, 0, 0
    for sha, a, b in reps:
        ra = {r["video_id"]: r for r in runs[a]["results"] if r.get("status") == "success"}
        rb = {r["video_id"]: r for r in runs[b]["results"] if r.get("status") == "success"}
        vids = sorted(set(ra) & set(rb))
        rec = {"sha": sha, "run_a": a, "run_b": b, "n": len(vids), "videos": {}}
        for vid in vids:
            x, y = ra[vid], rb[vid]
            same_json = canonical(x["analysis"]) == canonical(y["analysis"])
            ident_json += same_json
            ident_f1 += abs(x["edge_f1"] - y["edge_f1"]) < 1e-9
            n_vids += 1
            # `results[].svc_f1` es fracción; `metrics.*_mean` está en puntos.
            # Todo lo que sigue se expresa en puntos, como la tabla de ablación.
            sa, sb = 100 * x["svc_f1"], 100 * y["svc_f1"]
            ea, eb = 100 * x["edge_f1"], 100 * y["edge_f1"]
            pooled_d["svc"].append(sa - sb)
            pooled_d["edge"].append(ea - eb)
            rec["videos"][vid] = {"svc_a": sa, "svc_b": sb, "edge_a": ea, "edge_b": eb,
                                  "identical_json": same_json}
        for k in ("svc", "edge"):
            va = np.array([rec["videos"][v][f"{k}_a"] for v in vids])
            vb = np.array([rec["videos"][v][f"{k}_b"] for v in vids])
            rec[f"{k}_a"], rec[f"{k}_b"] = float(va.mean()), float(vb.mean())
            rec[f"{k}_delta"] = float(va.mean() - vb.mean())
        w = sum(1 for v in vids if rec["videos"][v]["edge_a"] > rec["videos"][v]["edge_b"] + 1e-9)
        l = sum(1 for v in vids if rec["videos"][v]["edge_b"] > rec["videos"][v]["edge_a"] + 1e-9)
        rec["sign_w"], rec["sign_l"], rec["sign_t"] = w, l, len(vids) - w - l
        rec["sign_p"] = sign_test(w, l)
        per_pair.append(rec)

    # ── 1. determinismo ──────────────────────────────────────────────
    console.print("[bold]1 · ¿Es determinista a temperatura 0.0?[/]")
    console.print(f"   Salidas JSON byte-idénticas entre corridas: "
                  f"[bold]{ident_json}/{n_vids}[/] ({100*ident_json/n_vids:.1f}%)")
    console.print(f"   Edge F1 idéntico:                           "
                  f"[bold]{ident_f1}/{n_vids}[/] ({100*ident_f1/n_vids:.1f}%)")
    console.print("   [dim]Temperatura 0.0 fija el muestreo, no la aritmética: el batching y el "
                  "orden de reducción en GPU varían entre llamadas.[/]\n")

    # ── 2. piso de ruido a nivel panel ───────────────────────────────
    t = Table(title="2 · Un prompt contra sí mismo — entradas idénticas, dos llamadas",
              border_style="cyan")
    t.add_column("prompt (sha)", style="bold")
    for c in ("n", "Svc A", "Svc B", "Δ Svc", "Edge A", "Edge B", "Δ Edge", "G-P-E", "p signos"):
        t.add_column(c, justify="right")
    for r in sorted(per_pair, key=lambda r: -abs(r["edge_delta"])):
        de = r["edge_delta"]
        t.add_row(r["sha"], str(r["n"]),
                  f"{r['svc_a']:.2f}", f"{r['svc_b']:.2f}", f"{r['svc_delta']:+.2f}",
                  f"{r['edge_a']:.2f}", f"{r['edge_b']:.2f}",
                  f"[bold red]{de:+.2f}[/]" if abs(de) >= 3 else f"{de:+.2f}",
                  f"{r['sign_w']}-{r['sign_l']}-{r['sign_t']}",
                  f"[bold red]{r['sign_p']:.3f}[/]" if r["sign_p"] < 0.05 else f"{r['sign_p']:.3f}")
    console.print(t)

    summary = {}
    for k, label in (("svc", "Service F1"), ("edge", "Edge F1")):
        d = np.array([abs(r[f"{k}_delta"]) for r in per_pair])
        summary[k] = {"mean_abs": float(d.mean()), "median_abs": float(np.median(d)),
                      "max_abs": float(d.max()), "p95_abs": float(np.percentile(d, 95)),
                      "over_3pts": int((d >= 3).sum())}
        console.print(f"   {label:<11} |Δ| media [bold]{d.mean():.2f}[/] · mediana "
                      f"{np.median(d):.2f} · máx [bold]{d.max():.2f}[/] · "
                      f"≥3 pts en [bold]{(d >= 3).sum()}/{len(d)}[/] réplicas nulas")

    # ── 3. sigma_d y MDE ─────────────────────────────────────────────
    # Un prompt corrido tres veces produce tres pares, pero esos pares comparten
    # corridas: juntar sus diferencias en una sola bolsa reusa las mismas
    # observaciones y finge más grados de libertad de los que hay. Para sigma_d
    # se toma un subconjunto de pares que no compartan ninguna corrida,
    # prefiriendo los de panel más grande.
    used_runs: set[str] = set()
    indep = []
    for r in sorted(per_pair, key=lambda r: -r["n"]):
        if r["run_a"] in used_runs or r["run_b"] in used_runs:
            continue
        used_runs |= {r["run_a"], r["run_b"]}
        indep.append(r)
    indep_d = {"svc": [], "edge": []}
    for r in indep:
        for v, rec in r["videos"].items():
            indep_d["svc"].append(rec["svc_a"] - rec["svc_b"])
            indep_d["edge"].append(rec["edge_a"] - rec["edge_b"])
    if len(indep) < len(per_pair):
        console.print(f"\n[dim]Para sigma_d se usan {len(indep)} pares independientes de "
                      f"{len(per_pair)} ({len(indep_d['edge'])} observaciones): los demás "
                      f"reusan una corrida ya contada.[/]")
    pooled_d = indep_d

    console.print("\n[bold]3 · Ruido por video y efecto mínimo detectable[/]")
    t3 = Table(border_style="cyan")
    for c in ("métrica", "sigma_d por video", "MDE n=14", "MDE n=30", "MDE n=100", "n para 3 pts"):
        t3.add_column(c, justify="right" if c != "métrica" else "left")
    for k, label in (("svc", "Service F1"), ("edge", "Edge F1")):
        d = np.array(pooled_d[k])
        sd = float(d.std(ddof=1))
        mde = lambda n: Z_MDE * sd / sqrt(n)
        n_for_3 = int(np.ceil((Z_MDE * sd / 3.0) ** 2))
        summary[k].update({"sigma_d": sd, "mde_14": mde(14), "mde_30": mde(30),
                           "mde_100": mde(100), "n_for_3pts": n_for_3})
        t3.add_row(label, f"{sd:.2f}", f"{mde(14):.2f}", f"{mde(30):.2f}",
                   f"{mde(100):.2f}", str(n_for_3))
    console.print(t3)
    console.print("[dim]sigma_d = desvío de la diferencia pareada por video entre dos corridas "
                  "del MISMO prompt.\nMDE = 2.80·sigma_d/√n: la diferencia más chica que un panel "
                  "de ese tamaño puede detectar al 80% de potencia.[/]")

    # ── 4. falsos positivos de la prueba de signos ───────────────────
    ps = [r["sign_p"] for r in per_pair]
    fp = sum(1 for p in ps if p < 0.05)
    console.print(f"\n[bold]4 · Prueba de signos sobre comparaciones nulas:[/] "
                  f"{fp}/{len(ps)} dan p<0.05 (esperado ~{0.05*len(ps):.1f}). "
                  f"p mínimo {min(ps):.3f}")

    # ── 5. ¿difiere el ruido nulo del ruido entre prompts distintos? ──
    # Si sigma_d entre prompts distintos no supera al de las réplicas nulas,
    # entonces las variantes no están introduciendo variación por encima del ruido.
    cross = []
    p30 = {d["stage2_prompt"]["sha256"][:10]: d for n, d in runs.items()
           if len(d["video_ids"]) == 30 and comparable(d)}
    shas = sorted(p30)
    for i, sa in enumerate(shas):
        for sb in shas[i + 1:]:
            ra = {r["video_id"]: r for r in p30[sa]["results"] if r.get("status") == "success"}
            rb = {r["video_id"]: r for r in p30[sb]["results"] if r.get("status") == "success"}
            for v in sorted(set(ra) & set(rb)):
                cross.append(100 * (ra[v]["edge_f1"] - rb[v]["edge_f1"]))
    sd_null = float(np.array(pooled_d["edge"]).std(ddof=1))
    sd_cross = float(np.array(cross).std(ddof=1))
    summary["sigma_d_cross_prompt_edge"] = sd_cross
    console.print(f"\n[bold]5 · sigma_d entre prompts DISTINTOS (Edge, panel 30):[/] "
                  f"[bold]{sd_cross:.2f}[/] vs [bold]{sd_null:.2f}[/] entre réplicas del mismo "
                  f"prompt — razón {sd_cross/sd_null:.2f}×")
    console.print("[dim]Una razón cercana a 1 significa que cambiar el prompt no mueve un video "
                  "más de lo que lo mueve repetir la misma llamada.[/]")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "note": "Réplicas test-retest: mismo prompt, mismos 14 videos, mismo whiteboard y mismo "
                "World Model de Stage 1, dos llamadas independientes. La diferencia verdadera es "
                "cero por construcción, así que todo lo medido es ruido.",
        "model": sorted(map(str, models)), "temperature": sorted(map(str, temps)),
        "input_mismatches": mismatches,
        "determinism": {"identical_json": ident_json, "identical_edge_f1": ident_f1,
                        "n_observations": n_vids},
        "summary": summary,
        "sign_test_false_positives": {"n_significant": fp, "n_comparisons": len(ps),
                                      "min_p": min(ps)},
        "pairs": per_pair,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    console.print(f"\n[green]✓[/] {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
