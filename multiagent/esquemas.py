"""
esquemas.py — Contratos Pydantic de los agentes LLM.

Cada esquema se pasa como `response_schema` a Gemini, así que la salida llega como JSON
validado. Los campos de texto que el agente debe copiar del insumo se llaman `*_literal`
o `cita`: el código (C1) es quien normaliza, no el agente.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


# ── A1 · Lector visual ───────────────────────────────────────────────
class Caja(BaseModel):
    id: str
    texto_literal: str            # tal como está escrito; "ilegible" si no se lee
    fotograma: int                # índice del fotograma (0 = el primero enviado)


class Linea(BaseModel):
    origen: str                   # id de caja
    destino: str                  # id de caja; con punta "una", la punta está aquí
    punta: Literal["ninguna", "una", "ambas"]
    etiqueta_literal: str


class Contenedor(BaseModel):
    id: str
    texto_literal: str
    hijos: list[str]              # ids de cajas dibujadas dentro


class LecturaVisual(BaseModel):
    cajas: list[Caja]
    lineas: list[Linea]
    contenedores: list[Contenedor]


# ── A2 · Narración ───────────────────────────────────────────────────
class Mencion(BaseModel):
    nombre_hablado: str
    cita: str
    tiempo: float


class FlujoHablado(BaseModel):
    origen: str                   # nombre tal como se dice
    destino: str
    cita: str                     # cita literal corta de la transcripción
    tiempo: float                 # segundo de inicio del segmento citado
    seguridad: Literal["alta", "baja"]


class ContenidoContenedor(BaseModel):
    contenedor: str
    hijos: list[str]
    cita: str


class Narracion(BaseModel):
    servicios_mencionados: list[Mencion]
    flujos_hablados: list[FlujoHablado]
    retornos_hablados: list[FlujoHablado]
    contenido_de_contenedores: list[ContenidoContenedor]


# ── A3 · Reconciliador (y la llamada única de la configuración 2) ────
class NodoR(BaseModel):
    id: str
    service: str
    name: str
    notes: str
    evidencia: Literal["visual", "hablada", "ambas"]


class AristaR(BaseModel):
    source: str
    target: str
    flow_id: int
    seq: str
    type: Literal["data", "control", "meta"]
    notes: str
    procedencia: Literal["dibujada", "hablada", "ambas"]
    respaldo: str                 # id de línea de A1 y/o cita de A2


class GrafoReconciliado(BaseModel):
    razonamiento: str
    nombre: str
    nodes: list[NodoR]
    edges: list[AristaR]


# ── A4 · Crítico ─────────────────────────────────────────────────────
class Correccion(BaseModel):
    accion: Literal["agregar", "quitar", "invertir"]
    source: str                   # ids de nodo del grafo recibido
    target: str
    type: Literal["data", "control", "meta"]
    motivo: str


class Critica(BaseModel):
    analisis: str
    correcciones: list[Correccion]
