#!/usr/bin/env python3
"""
fase1b_debate_retornos.py — Fase 1b: ¿qué señal del video predice si el GT anota retornos?

La fase 0 mostró que la vuelta (B→A además de A→B) es la clase de error más grande y que
depende del grafo, no del par de servicios. Aquí agentes LLM buscan esa señal en la narración
y el código la mide; ningún LLM decide si una hipótesis funciona.

  Proponente   ve 8 grafos de inducción sin retornos y 8 con retornos (título, transcripción y
               aristas) y propone hasta 5 preguntas sí/no respondibles con título y
               transcripción solamente.
  Clasificador responde esas preguntas en videos que el proponente no vio, sin ver el grafo.
  Código       compara las respuestas con el estilo real y mide el F1 de aristas de la
               producción si se agrega la vuelta donde la hipótesis predice retornos.
  Escéptico    recibe las cifras y los contraejemplos y devuelve un conjunto corregido.

  ronda 1: hipótesis del proponente  → lote 1 (100 videos de inducción)
  ronda 2: hipótesis del escéptico   → lote 2 (los 102 restantes)
  final:   la mejor de la ronda 2    → validación (73), solo si mejora en el lote 2

Unas 17 llamadas a gemini-3.8-flash; `llm.MAX_LLAMADAS` corta en 30. El panel no se abre.

    .venv/Scripts/python scripts/reglas/fase1b_debate_retornos.py
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import llm  # noqa: E402
from fase0_diagnostico import GEN_DIR, GT_DIR, OUT, estilo, f1, leer, spearman  # noqa: E402
from fase1a_huella_y_reglas import transcripcion  # noqa: E402
from scripts.utils.evaluate_graphs import extract_edge_service_pairs_no_type  # noqa: E402

SEMILLA, POR_GRUPO, LOTE1, POR_LLAMADA = 42, 8, 100, 20
SALIDA = OUT / "fase1b"


class Hipotesis(BaseModel):
    nombre: str
    pregunta: str
    two_way: bool
    razon: str


class Propuesta(BaseModel):
    analisis: str
    hipotesis: list[Hipotesis]


class RespuestaVideo(BaseModel):
    video_id: str
    respuestas: list[bool]


class Clasificacion(BaseModel):
    videos: list[RespuestaVideo]


# ── Datos ────────────────────────────────────────────────────────────
def datos(vid: str) -> dict:
    gt = leer(GT_DIR / f"{vid}.graphml")
    return {"vid": vid, "titulo": str(gt.graph.get("name", "")), "texto": transcripcion(vid),
            "aristas": extract_edge_service_pairs_no_type(gt), "bidir": estilo(gt)["frac_bidireccional"],
            "pares": estilo(gt)["pares"]}


def bloque(d: dict, con_aristas: bool = False, max_palabras: int | None = None) -> str:
    texto = d["texto"] if max_palabras is None else " ".join(d["texto"].split()[:max_palabras])
    s = f"### VIDEO {d['vid']}\nTitle: {d['titulo']}\nTranscript: {texto}\n"
    if con_aristas:
        s += "Annotated edges:\n" + "\n".join(f"  {a} -> {b}" for a, b in d["aristas"]) + "\n"
    return s


def repartir(ind: list[str]) -> tuple[list, list, list, list]:
    D = {v: datos(v) for v in ind}
    candidatos = [v for v in ind if D[v]["texto"] and 6 <= len(D[v]["aristas"]) <= 20 and D[v]["pares"] >= 4]
    uno = sorted(v for v in candidatos if D[v]["bidir"] == 0)
    dos = sorted(v for v in candidatos if D[v]["bidir"] >= 0.6)
    r = random.Random(SEMILLA)
    ej_uno, ej_dos = r.sample(uno, POR_GRUPO), r.sample(dos, POR_GRUPO)
    resto = sorted(v for v in ind if v not in set(ej_uno + ej_dos) and D[v]["texto"])
    r.shuffle(resto)
    return ej_uno, ej_dos, resto[:LOTE1], resto[LOTE1:]


# ── Agentes ──────────────────────────────────────────────────────────
def proponer(ej_uno: list[str], ej_dos: list[str]) -> dict:
    plantilla, version = llm.prompt("proponente_v1.txt")
    ejemplos = ("## GROUP ONE_WAY\n\n" + "\n".join(bloque(datos(v), True) for v in ej_uno) +
                "\n## GROUP TWO_WAY\n\n" + "\n".join(bloque(datos(v), True) for v in ej_dos))
    texto = plantilla.replace("<N_EJEMPLOS>", str(len(ej_uno) + len(ej_dos))).replace("<EJEMPLOS>", ejemplos)
    r = llm.llamar(texto, Propuesta, "proponente", f"proponente_v1@{version}")
    r["hipotesis"] = r["hipotesis"][:5]
    return r


def clasificar(hipotesis: list[dict], videos: list[str], etiqueta: str) -> dict[str, list[bool]]:
    plantilla, version = llm.prompt("clasificador_v1.txt")
    preguntas = "\n".join(f"  Q{i + 1}. {h['pregunta']}" for i, h in enumerate(hipotesis))
    out = {}
    for i in range(0, len(videos), POR_LLAMADA):
        lote = videos[i:i + POR_LLAMADA]
        texto = (plantilla.replace("<PREGUNTAS>", preguntas).replace("<N_PREGUNTAS>", str(len(hipotesis)))
                 .replace("<VIDEOS>", "\n".join(bloque(datos(v)) for v in lote)))
        r = llm.llamar(texto, Clasificacion, etiqueta, f"clasificador_v1@{version}")
        for x in r["videos"]:
            if x["video_id"] in lote and len(x["respuestas"]) == len(hipotesis):
                out[x["video_id"]] = x["respuestas"]
    return out


def criticar(hipotesis: list[dict], medidas: list[dict], respuestas: dict, videos: list[str]) -> dict:
    plantilla, version = llm.prompt("esceptico_v1.txt")
    resultados = "\n".join(
        f"- {h['nombre']} (yes predicts {'TWO_WAY' if h['two_way'] else 'ONE_WAY'}): \"{h['pregunta']}\"\n"
        f"    answered yes on {m['si']}/{m['n']} videos; balanced accuracy {m['exactitud_balanceada']}%; "
        f"Spearman with the real fraction of two-way pairs {m['spearman']}; "
        f"edge F1 if returns are added where it predicts TWO_WAY: {m['f1_politica']} "
        f"(never adding: {m['f1_nunca']}, perfect style oracle: {m['f1_oraculo']})"
        for h, m in zip(hipotesis, medidas))
    # Contraejemplos: los videos donde más hipótesis fallan, mitad de cada estilo real.
    fallos = []
    for v in videos:
        if v not in respuestas:
            continue
        d = datos(v)
        real = d["bidir"] >= 0.5
        err = sum((r == h["two_way"]) != real for r, h in zip(respuestas[v], hipotesis))
        fallos.append((err, real, v))
    fallos.sort(key=lambda x: (-x[0], x[2]))
    elegidos = [f for f in fallos if f[1]][:3] + [f for f in fallos if not f[1]][:3]
    contra = "\n".join(
        f"Real style: {'TWO_WAY' if real else 'ONE_WAY'} ({round(100 * datos(v)['bidir'])}% of pairs two-way); "
        f"answers: {dict(zip([h['nombre'] for h in hipotesis], respuestas[v]))}\n{bloque(datos(v), max_palabras=1200)}"
        for _, real, v in elegidos)
    texto = (plantilla.replace("<N_VIDEOS>", str(len(respuestas))).replace("<RESULTADOS>", resultados)
             .replace("<CONTRAEJEMPLOS>", contra))
    r = llm.llamar(texto, Propuesta, "esceptico", f"esceptico_v1@{version}")
    r["hipotesis"] = r["hipotesis"][:5]
    return r


# ── Medición (código) ────────────────────────────────────────────────
def medir(hipotesis: list[dict], respuestas: dict[str, list[bool]]) -> list[dict]:
    vids = sorted(respuestas)
    G = {v: (Counter(extract_edge_service_pairs_no_type(leer(GEN_DIR / f"{v}.graphml"))),
             Counter(extract_edge_service_pairs_no_type(leer(GT_DIR / f"{v}.graphml")))) for v in vids}
    bid = {v: datos(v)["bidir"] for v in vids}

    def con_vueltas(gen_c: Counter) -> Counter:
        return gen_c + Counter({(b, a): 1 for a, b in gen_c if a != b and (b, a) not in gen_c})

    f_nunca = mean(f1(G[v][0], G[v][1]) for v in vids)
    f_orac = mean(f1(con_vueltas(G[v][0]) if bid[v] >= 0.5 else G[v][0], G[v][1]) for v in vids)
    medidas = []
    for i, h in enumerate(hipotesis):
        pred = {v: respuestas[v][i] == h["two_way"] for v in vids}
        real = {v: bid[v] >= 0.5 for v in vids}
        sens = mean(pred[v] for v in vids if real[v]) if any(real.values()) else 0
        espe = mean(not pred[v] for v in vids if not real[v]) if not all(real.values()) else 0
        medidas.append({
            "hipotesis": h["nombre"], "n": len(vids), "si": sum(respuestas[v][i] for v in vids),
            "exactitud_balanceada": round(100 * (sens + espe) / 2, 1),
            "spearman": round(spearman([float(pred[v]) for v in vids], [bid[v] for v in vids]), 3),
            "f1_politica": round(mean(f1(con_vueltas(G[v][0]) if pred[v] else G[v][0], G[v][1]) for v in vids), 2),
            "f1_nunca": round(f_nunca, 2), "f1_oraculo": round(f_orac, 2)})
    return medidas


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    p = json.loads((OUT / "particion.json").read_text(encoding="utf-8"))
    ej_uno, ej_dos, lote1, lote2 = repartir(p["induccion"])
    reparto = {"ejemplos_one_way": ej_uno, "ejemplos_two_way": ej_dos, "lote1": lote1, "lote2": lote2}
    (SALIDA / "reparto.json").write_text(json.dumps(reparto, indent=1), encoding="utf-8")
    print(f"ejemplos {len(ej_uno)}+{len(ej_dos)} · lote 1 {len(lote1)} · lote 2 {len(lote2)}")

    prop = proponer(ej_uno, ej_dos)
    r1 = clasificar(prop["hipotesis"], lote1, "clasificador_r1")
    m1 = medir(prop["hipotesis"], r1)
    (SALIDA / "ronda1.json").write_text(json.dumps({"propuesta": prop, "medidas": m1}, indent=1, ensure_ascii=False), encoding="utf-8")
    print("ronda 1:"); [print(" ", m) for m in m1]

    crit = criticar(prop["hipotesis"], m1, r1, lote1)
    r2 = clasificar(crit["hipotesis"], lote2, "clasificador_r2")
    m2 = medir(crit["hipotesis"], r2)
    (SALIDA / "ronda2.json").write_text(json.dumps({"propuesta": crit, "medidas": m2}, indent=1, ensure_ascii=False), encoding="utf-8")
    print("ronda 2:"); [print(" ", m) for m in m2]

    mejor = max(range(len(m2)), key=lambda i: m2[i]["f1_politica"])
    final = {"elegida": crit["hipotesis"][mejor], "lote2": m2[mejor]}
    if m2[mejor]["f1_politica"] > m2[mejor]["f1_nunca"]:
        rv = clasificar([crit["hipotesis"][mejor]], p["validacion"], "clasificador_validacion")
        final["validacion"] = medir([crit["hipotesis"][mejor]], rv)[0]
    else:
        final["validacion"] = "no se corrió: ninguna hipótesis mejora el F1 en el lote 2"
    final["llamadas_nuevas"] = llm.nuevas
    (SALIDA / "final.json").write_text(json.dumps(final, indent=1, ensure_ascii=False), encoding="utf-8")
    print("final:", json.dumps(final, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
