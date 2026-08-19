# Estado y pendientes — 2026-08-16

Sesión enfocada **solo en Standard**. Parsimonious quedó congelado a propósito:
no se tocó `graphs_parsimonious*`, ni `vision_analyzer_parsimonious.py`, ni el
dashboard comparativo.

Rama: `fix/standard-pipeline-integrity` · 4 commits, sin push.

```
c58ccd9  docs(standard): document the 2-stage architecture and its prompt lineage
3883018  feat(standard): process 26 pending Standard graphs, reaching 299 GT videos
0a1de77  feat(standard): reproducible evaluation runs + pipeline hygiene
c047767  fix(standard): atomic GraphML export + read-only state baseline
```

---

## 1. Lo que se hizo

### Cobertura y métricas

| | Antes | Después |
|---|---:|---:|
| Grafos standard | 290 | 316 |
| Evaluables contra GT | 273 | **299** |
| Service F1 (estricto) | 85.69% | **86.03%** |
| Edge F1 (sin GT sin aristas) | 57.80% (n=261) | **58.20%** (n=286) |
| Edge F1 (legacy, con todos) | 55.26% | 55.67% |

Se procesaron los 26 videos que quedaron colgados cuando el batch murió con un
429. 26/26 exitosos. Hubo 429 y 503 durante la corrida pero la rotación de
claves y el backoff los absorbieron.

### Correcciones de código

**Escritura de grafos** — `export_graphml` ([graph_builder.py](../scripts/core/graph_builder.py))
sanea atributos no escalares (listas → `"a, b"`, dicts → JSON, `None` → `""`) y
escribe atómicamente vía `.tmp` + `os.replace`. Antes, un fallo del writer dejaba
un archivo de 0 bytes; así aparecieron los 3 rotos de `graphs_parsimonious_v10`.
Verificado: re-exportar 40 grafos existentes da resultado byte-idéntico al
round-trip crudo de networkx, o sea que sobre los datos actuales es un no-op.

**Detección de pendientes** — el batch consideraba "hecho" cualquier archivo que
existiera, incluido uno de 0 bytes, y ese video no se reintentaba nunca. Ahora
exige que exista, pese >0 y parsee.

**Filtro de videos especiales** ([main.py](../main.py)) — una sola función
`is_special_video()` en los tres puntos donde antes había lógica duplicada,
incluido el fast-path, que se lo saltaba entero: con transcript y pizarra en
caché, un episodio recopilatorio se iba derecho a la API de visión. 12/12 casos
de prueba. La duración quedó unificada en **> 12:00**; antes la rama del CSV
usaba `>= 12:00`, así que un video de exactamente 12:00 ahora pasa.

**Selector de frames** — solo corre con `--skip-vision`. En modo visión su
resultado se descartaba cuatro líneas después; era trabajo perdido. Efecto
secundario: en modo visión ya no se regenera
`data/frames/{id}_pizarra/best_whiteboard.jpg`.

**Modelo por defecto** ([settings.py](../config/settings.py)) — alineado a
`gemini-3.6-flash`. Antes el default era `3.5` y solo el `.env` corregía, así que
cualquiera sin `.env` evaluaba con otro modelo sin enterarse.

### Herramientas nuevas

| Script | Qué hace |
|---|---|
| [snapshot_state.py](../scripts/utils/snapshot_state.py) | Foto read-only: cobertura, integridad de archivos, métricas. No toca `data/` ni llama a ninguna API. |
| [evaluate_standard.py](../scripts/utils/evaluate_standard.py) | Punto de verdad único. Emite `results.csv` + `run.json` con procedencia y exclusiones. |
| [render_standard_report.py](../scripts/utils/render_standard_report.py) | Genera el HTML **desde el CSV**, nunca desde los grafos. |
| [build_manifest.py](../scripts/utils/build_manifest.py) | Regenera `reports/MANIFEST.md` desde los `run.json`. |

Los GT con 0 aristas (13 de 299) cuentan en servicios pero salen del promedio de
aristas, donde su F1 es 0 por construcción. El valor viejo se conserva como
`edge_f1_legacy_including_zero_edge_gt` para poder comparar con reportes previos.

### Documentación

[docs/standard-pipeline.md](standard-pipeline.md) — qué es Standard realmente
(pipeline de 2 agentes Perceptor/Razonador, no una variante de prompt), el
protocolo de los 14 videos, las dos generaciones completas de la ablación, y los
callejones sin salida que vale la pena preservar.

---

## 2. Pendientes

### 2.1 Standard

- [ ] **Sincronizar el prompt del lab con producción y re-correr los 14.**
      `batch_prompt_test.py` tiene su propia copia bajo un comentario que dice
      *"Identical to vision_analyzer.py"*, y ya no lo es: producción corre
      *"Expert Cloud Architecture Transcriber… transcribe EXACTLY"* (3984 chars),
      el lab sigue con *"expert AWS Solutions Architect… generalize your
      reasoning"* (2523 chars). Instrucciones opuestas. Consecuencia medida: el
      lab da 65.28% de Edge F1 sobre los mismos 14 videos que producción puntúa
      en 58.01%. **Bloquea todo lo demás de esta sección** — hasta resolverlo no
      se sabe qué mide el lab.
- [ ] **Decidir sobre V7.** Gana a V6 en ambas métricas (90.58/65.73 vs
      89.94/65.28) y ataca la debilidad conocida: ~33% del GT es bidireccional
      contra ~11% en V6. No promover hasta cerrar el punto anterior — la mejora
      atribuida (~1.2 puntos) es menor que la discrepancia de 7.
- [ ] **Re-correr 28 grafos.** Se escribieron el 3 ago a las 11:41, antes del
      commit `a7b218f` (12:34) que cambió el prompt de Stage 2. Lo normal es
      editar y commitear después, así que casi seguro usaron el prompt actual,
      pero no es demostrable por timestamps.
- [ ] **Archivar el prompt en cada corrida.** Hashear el texto del prompt dentro
      del `run.json`. Los prompts de la generación 2 (V5, V6, V7) ya son
      irrecuperables: `--experiment-label` solo pone sufijo al archivo de salida
      y las variantes se editaban en el mismo sitio, pisándose. Parsimonious sí
      lo tiene resuelto con `parsimonious_prompt_history.md` (79 registros con
      texto completo).
- [ ] **Tracker.** `processed_tracker.json` arrastra 5 etiquetas históricas
      (`version_1/2/3/9_parsimonious/10_parsimonious`) y hoy hay tres fuentes de
      verdad para lo mismo: el tracker, el progress JSON del batch y los
      `run.json`. Renombrar huerfanía 246 entradas. Renombrar, migrar o deprecar
      son decisiones distintas — **requiere decisión, no es mecánico**.

### 2.2 Organización de carpetas y reportes

- [ ] **Archivar los 4 HTML huérfanos de la raíz.** Ninguno tiene script que lo
      genere; se produjeron ad-hoc y no son reproducibles. Mover tal cual a
      `reports/archive/`, etiquetados como corridas históricas:
      `analisis_con_prompt_parsimonio_elegido.html` (60 videos, subconjunto del
      de 79 → obsoleto), `reporte_comparacion_detallada.html` + `.md` (60),
      `evaluacion_estricta_vs_permisiva.html` (61),
      `prompt_ablation_detailed_report_parsimonious.html` (79).
- [ ] **`index.html` y `reporte_comparativo_v6_vs_parsimonious.html` son el mismo
      archivo** (md5 idéntico, 1.1 MB cada uno, 2.2 MB duplicados por commit).
      Dejarlos hasta entrar al parsimonious, porque son el dashboard comparativo.
- [ ] **25 HTML de debug en `data/frames/`** (junio, experimentos de pizarra) →
      `reports/archive/frames_debug_junio/`.
- [ ] **Nombres que colisionan:** `Graphs/` (470 png de render), `graficas/`
      (5 png de charts) y `data/graphs/` (316 graphml).
- [ ] **Carpetas muertas.** `UNPROCESSED_DIR` y `PROCESADOS_DIR` se crean en
      `settings.py` y ningún script las usa; ambas vacías. El flujo real de
      revisión es `bad_whiteboard/` → `good_whiteboard/`, pero la promoción es
      manual y no está escrita en ningún lado. Hay 92 imágenes esperando en
      `bad_whiteboard/`. `handoff_notes.md` documenta el flujo muerto.

### 2.3 Parsimonious — Resuelto y Homologado (2026-08-19)

- [x] **Overlay y Aislamiento (A1, A2, B4):** RESUELTO. Se parametrizaron las rutas de entrada/salida (`--graphs-dir` / `--output-dir`). Los 335 grafos del Prompt v9 están aislados y respaldados en `data/graphs_parsimonious_v9/`.
- [x] **Grafos de 0 bytes en v10 (A3):** RESUELTO. Se recuperaron los 3 vídeos (`6YkguepAQuQ`, `F4KDOGNpSoI`, `FfSNnH2bbNc`) desde su caché JSON sin gasto de cuota API (10/6, 14/15 y 8/10 nodos/aristas).
- [x] **Vídeo faltante Jz2RPRhF6Fs (A4):** RESUELTO. Procesado exitosamente (10 nodos / 10 aristas).
- [x] **Evaluador Dedicado e Integridad C1-C4:** RESUELTO. Se implementó `scripts/evaluation/evaluate_parsimonious.py` que genera automáticamente `results_parsimonious.csv` (299 pares evaluados, 83.66% Service F1, 54.28% Edge F1) e `info_parsimonious.json`, aplicando el ajuste C4 para GTs con 0 aristas.
- [x] **Robustez API y Convención de Caché (B1, B2, A5, B3):** RESUELTO. Reintentos exponenciales para 503/429 integrados en los scripts de ejecución y formato de caché estandarizado en `data/raw/*_vision_analysis_parsimonious.json`.

### 2.4 Dashboard comparativo

- [ ] **El encabezado no corresponde con el contenido.** `index.html` dice
      *"273 vídeos"*; las tablas tienen **139 filas**. `generate_html_report.py`
      arma `eval_vids` = standard∩GT y luego hace `continue` cuando falta el par
      parsimonious, pero imprime `len(eval_vids)`. Regenerado hoy daría 155.
      118 videos quedan fuera en silencio.
- [ ] **Declarar el confound.** Standard es 2 fases con esquema Pydantic y 5
      reintentos; parsimonious es 1 fase con parseo manual. Ningún reporte lo
      dice; todos presentan la comparación como si fuera de prompts.

### 2.5 El ARA (`ara/`, gitignorado)

Revisado el primer día, sin tocar. Requiere rehacer `claims.md`, ambas tablas de
`evidence/` y el `exploration_tree`:

- [ ] C03 está **falsificado por su propio criterio** (−5.57% de media contra un
      umbral de −5%) pero marcado `Validated`. Su Tabla 1 son 16 filas de 60,
      elegidas de modo que quedan 4 victorias contra 3, cuando la población real
      es 8 contra 28.
- [ ] Los números de la Tabla 2 no existen en la fuente que cita. Los reales son
      82.43→90.49 (Service F1), 86.07→93.89 (Recall), 51.09→58.09 (Edge F1),
      n=61, prompt v9.
- [ ] C01 cita un *"24% de reducción"* que no aparece en ninguna fuente, y su
      prueba apunta a la tabla equivocada. El experimento real sí existe:
      `V5_with_vision` en `Avance Semanal 3`.
- [ ] Ninguna referencia a código resuelve: apuntan a `scripts/*.py` cuando el
      código vive en `scripts/core/` y `scripts/utils/`.
- [ ] Falta `src/configs/` — los prompts son la variable independiente de toda la
      investigación y no están versionados ahí.
- [ ] Links `file:///home/stemjara/...` absolutos: el artefacto no es portable.

---

## 3. Orden sugerido

1. Sincronizar lab ↔ producción y re-correr los 14 (2.1) — desbloquea V7 y
   cualquier comparación futura.
2. Archivado de carpetas y reportes (2.2) — barato, sin riesgo, y quita el ruido
   que hizo que el ARA leyera las fuentes equivocadas.
3. Parsimonious (2.3), y recién ahí el dashboard comparativo (2.4).
4. El ARA (2.5) al final, cuando los números que debe citar ya sean estables.

## 4. Comandos

```bash
.venv/bin/python scripts/utils/snapshot_state.py
.venv/bin/python scripts/utils/evaluate_standard.py --label v6corrected
.venv/bin/python scripts/utils/render_standard_report.py reports/runs/<run-dir>
.venv/bin/python scripts/utils/build_manifest.py
.venv/bin/python scripts/batch_process_standard_missing.py
```
