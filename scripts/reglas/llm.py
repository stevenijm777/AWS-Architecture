"""
llm.py — Llamadas a Gemini para los agentes de reglas, con caché en disco y log por llamada.

Reutiliza `KeyRotator` y `call_gemini` de rerun_panel (rotación de llaves, espera ante 429,
reintentos con espera exponencial ante 503, `response_schema` y temperatura 0).

  caché  reports/reglas_convencion/cache/<etiqueta>/<sha(modelo+esquema+prompt)>.json
  log    reports/reglas_convencion/llamadas.jsonl   (tokens, latencia, versión de prompt)

Una reejecución con el mismo prompt no gasta cuota. `MAX_LLAMADAS` corta la ejecución
antes de pasar el tope acordado de llamadas nuevas.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from config.settings import GEMINI_API_KEYS
from scripts.ablation.rerun_panel import USAGE, KeyRotator, call_gemini

ROOT = Path(__file__).resolve().parent.parent.parent
CACHE = ROOT / "reports" / "reglas_convencion" / "cache"
LOG = ROOT / "reports" / "reglas_convencion" / "llamadas.jsonl"
PROMPTS = Path(__file__).resolve().parent / "prompts"
MODELO = "gemini-3.8-flash"
MAX_LLAMADAS = 30

_rot: KeyRotator | None = None
nuevas = 0


def prompt(nombre: str) -> tuple[str, str]:
    """Plantilla versionada y su sha corto."""
    texto = (PROMPTS / nombre).read_text(encoding="utf-8")
    return texto, hashlib.sha256(texto.encode()).hexdigest()[:12]


def llamar(texto: str, esquema: type[BaseModel], etiqueta: str, version: str,
           modelo: str = MODELO) -> dict:
    global _rot, nuevas
    clave = hashlib.sha256(f"{modelo}\n{esquema.__name__}\n{texto}".encode()).hexdigest()[:20]
    ruta = CACHE / etiqueta / f"{clave}.json"
    if ruta.exists():
        return json.loads(ruta.read_text(encoding="utf-8"))["respuesta"]
    if nuevas >= MAX_LLAMADAS:
        raise RuntimeError(f"Tope de {MAX_LLAMADAS} llamadas nuevas alcanzado: pedir permiso antes de seguir.")
    _rot = _rot or KeyRotator(GEMINI_API_KEYS)
    n0, t0 = len(USAGE), time.time()
    respuesta = call_gemini(_rot, texto, [], modelo, schema=esquema)
    nuevas += 1
    uso = USAGE[-1] if len(USAGE) > n0 else {}
    registro = {"cuando": datetime.now(timezone.utc).isoformat(timespec="seconds"), "etiqueta": etiqueta,
                "modelo": modelo, "prompt": version, "latencia_s": round(time.time() - t0, 1),
                "entrada": uso.get("input", 0), "salida": uso.get("output", 0),
                "thinking": uso.get("thinking", 0)}
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(json.dumps({**registro, "respuesta": respuesta}, indent=1, ensure_ascii=False),
                    encoding="utf-8")
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
    return respuesta
