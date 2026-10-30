"""
c1_normalizador.py — C1: mapea los nombres literales (A1) y hablados (A2) al catálogo.

Orden de resolución para un texto:
  1. clave exacta en el diccionario de alias (datos/alias.json);
  2. la n-grama de palabras más larga que sea un alias ("S3 bucket raw data" → S3);
  3. coincidencia aproximada con difflib sobre el texto entero (umbral 0,88).
Lo que no se resuelve va a `sin_resolver`, y A3 decide con el catálogo a la vista. El
subtipo de actor (User*) no se resuelve aquí: lo elige A3.

No modifica la salida de los agentes: agrega `servicio` (o None) a cada elemento.
"""
from __future__ import annotations

import difflib
import json
from functools import lru_cache
from pathlib import Path

from multiagent.construir_datos import PARTICION, limpiar, verificar

DATOS = Path(__file__).resolve().parent / "datos"
UMBRAL_DIFUSO = 0.88
ACTORES = {"user", "users", "customer", "customers", "client", "clients", "enduser", "endusers"}


@lru_cache(maxsize=1)
def alias() -> dict[str, str]:
    datos = json.loads((DATOS / "alias.json").read_text(encoding="utf-8"))
    verificar(datos["construido_con"], "alias")
    return datos["alias"]


def resolver(texto: str) -> tuple[str | None, str]:
    """(servicio, cómo) — `cómo` es exacto, ngrama, difuso, actor o ninguno."""
    a = alias()
    t = limpiar(texto or "")
    if not t or t == "ilegible":
        return None, "ninguno"
    clave = t.replace(" ", "")
    if clave in ACTORES:
        return None, "actor"
    if clave in a:
        return a[clave], "exacto"
    palabras = t.split()
    for n in range(min(len(palabras), 5), 0, -1):
        for i in range(len(palabras) - n + 1):
            g = "".join(palabras[i:i + n])
            if len(g) >= 2 and g in a:
                return a[g], "ngrama"
    cerca = difflib.get_close_matches(clave, a.keys(), n=1, cutoff=UMBRAL_DIFUSO)
    if cerca:
        return a[cerca[0]], "difuso"
    return None, "ninguno"


def normalizar(lectura: dict | None, narracion: dict | None) -> dict:
    """Copia de A1 y A2 con `servicio` agregado, más la lista `sin_resolver`."""
    sin_resolver: list[dict] = []

    def marcar(item: dict, campo: str, fuente: str, destino: str = "servicio") -> None:
        servicio, como = resolver(item.get(campo, ""))
        item[destino] = servicio
        if servicio is None and limpiar(item.get(campo, "")) not in ("", "ilegible"):
            sin_resolver.append({"fuente": fuente, "texto": item[campo]})
        elif como == "difuso":
            item[destino + "_difuso"] = True

    a1 = json.loads(json.dumps(lectura)) if lectura else None
    a2 = json.loads(json.dumps(narracion)) if narracion else None
    if a1:
        for c in a1["cajas"]:
            marcar(c, "texto_literal", "a1.caja")
        for c in a1["contenedores"]:
            marcar(c, "texto_literal", "a1.contenedor")
    if a2:
        for m in a2["servicios_mencionados"]:
            marcar(m, "nombre_hablado", "a2.mencion")
        for f in a2["flujos_hablados"] + a2["retornos_hablados"]:
            marcar(f, "origen", "a2.flujo", "servicio_origen")
            marcar(f, "destino", "a2.flujo", "servicio_destino")
        for c in a2["contenido_de_contenedores"]:
            marcar(c, "contenedor", "a2.contenedor")
    # Un mismo texto no resuelto se lista una vez.
    vistos, unicos = set(), []
    for s in sin_resolver:
        k = s["texto"].lower()
        if k not in vistos:
            vistos.add(k)
            unicos.append(s)
    return {"a1": a1, "a2": a2, "sin_resolver": unicos}


if __name__ == "__main__":
    for t in ["Amazon S3 bucket", "Lambda function", "Kinesis Data Firehose", "API Gateway",
              "Dynamo DB", "Kafka cluster", "Salesforce", "ilegible", "users", "SageMaker endpoint",
              "Aurora PostgreSQL", "Elastic Search", "CloudWatch Logs", "on-prem data center"]:
        print(f"{t!r:28} → {resolver(t)}")
    print("alias construidos con", PARTICION.name)
