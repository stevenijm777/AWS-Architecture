"""
llm.py — Una llamada a Gemini por agente, con caché en disco, log y tope de llamadas.

Reutiliza `KeyRotator` y `call_gemini` de rerun_panel tal cual: rotación de llaves ante
429, retiro de llaves sin cuota diaria, espera exponencial ante 503, `response_schema` y
`response_mime_type="application/json"`. La temperatura de `call_gemini` es 0.0 fija, que
es la del config; si el config pidiera otra, se aborta en vez de mentir en el log.

  caché  <cache>/<video>/<agente>/<sha(modelo+esquema+prompt+imágenes+réplica)>.json
  log    <log>  una línea por llamada nueva: tokens, latencia y versión de prompt

`replica` entra en la clave: la réplica 0 es la corrida normal y las réplicas 1..n del
piso de ruido no leen su caché, pero sí quedan cacheadas para reanudar.
"""
from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel

from config.settings import GEMINI_API_KEYS
from scripts.ablation.rerun_panel import USAGE, KeyRotator, call_gemini

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = Path(__file__).resolve().parent / "prompts"
CONFIG = yaml.safe_load((Path(__file__).resolve().parent / "config.yaml").read_text(encoding="utf-8"))


class TopeDeLlamadas(RuntimeError):
    pass


def ruta(clave: str) -> Path:
    return ROOT / CONFIG["rutas"][clave]


def prompt(nombre: str) -> tuple[str, str]:
    """Plantilla versionada y su versión (`archivo@sha12`)."""
    texto = (PROMPTS / nombre).read_text(encoding="utf-8")
    return texto, f"{nombre}@{hashlib.sha256(texto.encode()).hexdigest()[:12]}"


class Cliente:
    def __init__(self, cfg: dict = CONFIG, replica: int = 0):
        if float(cfg["temperatura"]) != 0.0:
            raise ValueError("call_gemini fija temperatura 0.0; otra temperatura requiere otro cliente")
        self.cfg, self.replica = cfg, replica
        self.modelo = cfg["modelo"]
        self.max_llamadas = int(cfg["max_llamadas"])
        self.nuevas = 0
        self.registros: list[dict] = []      # también las llamadas servidas desde caché
        self._rot: KeyRotator | None = None

    def llamar(self, video: str, agente: str, texto: str, version: str,
               esquema: type[BaseModel], imagenes: list[str] = ()) -> dict:
        h = hashlib.sha256()
        for parte in (self.modelo, esquema.__name__, texto, *imagenes, f"replica={self.replica}"):
            h.update(parte.encode())
            h.update(b"\0")
        archivo = ruta("cache") / video / agente / f"{h.hexdigest()[:20]}.json"

        if archivo.exists():
            guardado = json.loads(archivo.read_text(encoding="utf-8"))
            self.registros.append({**{k: v for k, v in guardado.items() if k != "respuesta"},
                                   "desde_cache": True})
            return guardado["respuesta"]

        if self.nuevas >= self.max_llamadas:
            raise TopeDeLlamadas(f"Tope de {self.max_llamadas} llamadas nuevas alcanzado "
                                 f"(faltaba {video}/{agente}): pedir permiso antes de seguir.")
        self._rot = self._rot or KeyRotator(GEMINI_API_KEYS)
        n0, t0 = len(USAGE), time.time()
        respuesta = call_gemini(self._rot, texto, list(imagenes), self.modelo, schema=esquema)
        self.nuevas += 1
        uso = USAGE[-1] if len(USAGE) > n0 else {}
        registro = {
            "cuando": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "video": video, "agente": agente, "modelo": self.modelo, "prompt": version,
            "replica": self.replica, "imagenes": len(imagenes),
            "latencia_s": round(time.time() - t0, 1),
            "entrada": uso.get("input", 0), "salida": uso.get("output", 0),
            "thinking": uso.get("thinking", 0),
        }
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(json.dumps({**registro, "respuesta": respuesta}, indent=1,
                                      ensure_ascii=False), encoding="utf-8")
        log = ruta("log")
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(registro, ensure_ascii=False) + "\n")
        self.registros.append({**registro, "desde_cache": False})
        return respuesta
