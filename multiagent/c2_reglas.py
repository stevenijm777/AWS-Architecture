"""
c2_reglas.py — C2: reglas de convención en código, aplicadas al grafo de A3.

Una función por regla, registradas en REGLAS. Los parámetros salen de datos/reglas_c2.json,
estimados solo en inducción (ver construir_datos.py); al cargarlos se verifica de nuevo que
ningún grafo del panel entró.

  actor_subtipo  el subtipo de actor que el GT usa en lugar del generado
                 (UserConsumerWebMobile → UserConsumerMobile)
  ida_y_vuelta   pares que el GT anota en ambos sentidos en ≥ 80 % de los grafos (≥ 5):
                 si solo existe A→B, se agrega B→A

Toda arista agregada lleva procedencia="regla" y el nombre de la regla. Los pares de
`dudosos_para_a4` (ida y vuelta en 50–80 % de los grafos) no se deciden aquí: si aparecen
en un solo sentido, se devuelven como casos ambiguos para A4.
"""
from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path

from multiagent.construir_datos import verificar

DATOS = Path(__file__).resolve().parent / "datos"


@lru_cache(maxsize=1)
def parametros() -> dict:
    datos = json.loads((DATOS / "reglas_c2.json").read_text(encoding="utf-8"))
    verificar(datos["estimado_con"], "reglas C2 (estimación)")
    verificar(datos["seleccionado_con"], "reglas C2 (selección)")
    return datos


def _servicio(grafo: dict) -> dict[str, str]:
    return {n["id"]: n["service"] for n in grafo["nodes"]}


def regla_actor_subtipo(grafo: dict) -> list[dict]:
    cambios = []
    mapa = parametros()["reglas"]["actor_subtipo"]
    for n in grafo["nodes"]:
        if n["service"] in mapa:
            cambios.append({"regla": "actor_subtipo", "nodo": n["id"],
                            "antes": n["service"], "despues": mapa[n["service"]]})
            n["service"] = mapa[n["service"]]
    return cambios


def regla_ida_y_vuelta(grafo: dict) -> list[dict]:
    pares = {tuple(p.split("|")) for p in parametros()["reglas"]["ida_y_vuelta"]}
    svc = _servicio(grafo)
    existentes = {(e["source"], e["target"]) for e in grafo["edges"]}
    cambios = []
    for e in list(grafo["edges"]):
        a, b = e["source"], e["target"]
        if a == b or (b, a) in existentes:
            continue
        if tuple(sorted((svc.get(a, ""), svc.get(b, "")))) in pares:
            nueva = {"source": b, "target": a, "flow_id": e["flow_id"], "seq": f"{e['seq']}'",
                     "type": e["type"], "notes": "", "procedencia": "regla",
                     "regla": "ida_y_vuelta", "respaldo": f"{svc[a]}|{svc[b]} en reglas_c2.json"}
            grafo["edges"].append(nueva)
            existentes.add((b, a))
            cambios.append({"regla": "ida_y_vuelta", "agregada": f"{b}->{a}",
                            "par": f"{svc[b]}->{svc[a]}"})
    return cambios


REGLAS = [regla_actor_subtipo, regla_ida_y_vuelta]


def ambiguos(grafo: dict) -> list[dict]:
    """Pares dudosos presentes en un solo sentido: los decide A4, no C2."""
    dudosos = parametros()["dudosos_para_a4"]
    svc = _servicio(grafo)
    existentes = {(e["source"], e["target"]) for e in grafo["edges"]}
    casos = []
    for a, b in sorted(existentes):
        if a == b or (b, a) in existentes:
            continue
        clave = "|".join(sorted((svc.get(a, ""), svc.get(b, ""))))
        if clave in dudosos:
            casos.append({"arista": f"{a}->{b}", "par": f"{svc[a]}->{svc[b]}",
                          "frac_ida_y_vuelta_en_referencia": dudosos[clave]})
    return casos


def aplicar(grafo: dict) -> tuple[dict, list[dict], list[dict]]:
    """(grafo nuevo, cambios hechos, casos ambiguos para A4)."""
    g = copy.deepcopy(grafo)
    cambios = [c for regla in REGLAS for c in regla(g)]
    return g, cambios, ambiguos(g)
