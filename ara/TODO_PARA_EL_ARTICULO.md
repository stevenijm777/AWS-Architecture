# Qué falta en el ARA para que sirva de base al artículo

**Fecha:** 2026-08-20 · **Estado del pipeline:** todo procesado (370 Standard / 344 Parsimonious contra 396 GT)

El artículo lo escriben ustedes. Este documento no propone texto: lista qué del
ARA actual **no se puede citar todavía** porque contradice los datos, y qué
evidencia real existe hoy para reemplazarlo.

Regla de trabajo sugerida: **ningún número entra al artículo si no se puede
señalar el archivo que lo produjo.** Casi todo lo de abajo es aplicar eso.

---

## 0. Resumen de un vistazo

| Capa del ARA | Estado | Acción |
|---|---|---|
| `PAPER.md` | claims con cifras sin fuente | reescribir §claims_summary |
| `logic/claims.md` | C01–C04: 1 falso, 2 desactualizados, 1 sin prueba | rehacer los cuatro |
| `logic/experiments.md` | describe experimentos que no son los que se corrieron | rehacer |
| `logic/problem.md` | **correcto**, sirve tal cual | revisar cifras finales |
| `logic/solution/architecture.md` | describe 7 etapas; falta que Standard es 2 agentes | corregir |
| `logic/solution/algorithm.md` | **correcto** | añadir umbral de resolución |
| `logic/solution/constraints.md` | correcto, ampliar | añadir 3 exclusiones nuevas |
| `logic/related_work.md` | correcto | sin cambios urgentes |
| `src/environment.md` | desactualizado (modelo, versiones) | actualizar |
| `src/configs/` | **no existe en el ARA** | enlazar a `src/configs/prompts/` |
| `trace/exploration_tree.yaml` | 10 nodos; falta ~80% del recorrido | ampliar |
| `evidence/` | **ambas tablas inservibles** | regenerar desde los CSV |

---

## 1. Lo que hay que corregir sí o sí (bloquea el artículo)

### 1.1 `evidence/table2_strict_vs_permissive.md` — cifras inventadas

Ninguno de sus números (78.4 / 91.2 / 72.1 / 85.6 / 48.2 / 59.7) aparece en el
HTML que la tabla dice como fuente. Los reales de esa corrida eran
82.43→90.49 (Service F1), 86.07→93.89 (Recall), 51.09→58.09 (Edge F1), n=61.

Además describe mal el mecanismo permisivo: dice *"diccionario de alias
`lambda_function → Lambda`"*, cuando lo que hace el evaluador es **agrupación
ontológica por superclases de actores** (`UserConsumer`, `UserCompany`,
`ThirdParty`). Esa distinción es conceptualmente importante y conviene que el
artículo la explique bien.

**Reemplazar por:** una tabla generada desde `reports/dataset_audit_2026-08-20.csv`.

### 1.2 `evidence/table1_parsimonious_vs_standard.md` — muestra sesgada

Son 16 filas elegidas de 60, con 4 victorias de Parsimonious contra 3 de
Standard. En la población de entonces era 8 contra 28.

**Con el dataset completo de hoy (n=344 pareados):**

```
Standard      86.36%   gana en 93 videos
Parsimonious  85.41%   gana en 69 videos
                       empatan  182
delta (P − S) −0.95 puntos
```

**Reemplazar por:** la tabla completa, sin recortar. El CSV ya la tiene.

### 1.3 `logic/claims.md` — los cuatro claims

- **C01** (fusión audio-visual) afirma *"reduce la alucinación de servicios un
  24%"*. Ese número **no existe en ninguna fuente del repo**, y su "Proof"
  apunta a la Tabla 1, que mide otra cosa (prompting, no fusión).
  *La evidencia real sí existe:* la ablación `V5_with_vision` (solo visión)
  da 86.67% Service / 53.87% Edge contra 90.88% / 61.11% del baseline. Es el
  experimento correcto y está en `Avances/Avance Semanal 3.md` y en
  `whiteboard_selection_lab/batch_results*.json`.

- **C02** (oclusión + apertura morfológica) está bien conceptualmente y el
  algoritmo se sostiene, pero cita rutas que no existen
  (`scripts/pizarra_occlusion_filter.py` → hoy `scripts/utils/`). Además hay un
  hallazgo nuevo que **fortalece** el claim y conviene incorporar: en un
  experimento controlado, bajar los mismos frames de 1080p a 360p hizo que el
  selector cambiara de frame en 3/3 casos y el score cayera de 22–43 a ≤0.7,
  porque el detector de iconos deja de disparar bajo `min_area_icono=2000` px².
  Eso da un **umbral de operación medido**, no supuesto.

- **C03** (prompting parsimonioso) decía *"mantiene F1 igual o superior"* y con
  los datos viejos quedaba **falsificado por su propio criterio** (−5.57% contra
  un umbral de −5%). **Con el dataset completo ya no**: el delta es −0.95.
  Sigue siendo negativo, así que el claim debe reformularse a lo que la
  evidencia sostiene: *elimina los nodos fantasma a un costo de ~1 punto de
  Service F1*, no *"igual o superior"*.

- **C04** (evaluación permisiva) es correcto en la idea; hay que rehacer sus
  cifras junto con la Tabla 2.

### 1.4 Rutas rotas en todo el ARA

Todas las referencias a código apuntan a `scripts/*.py`. El código vive en
`scripts/core/` y `scripts/utils/`. Ninguna resuelve, y los rangos de línea
(`#L55`, `#L20-L40`) por tanto no son verificables. Es el único punto donde el
formato ARA promete algo — que cada claim resuelva a evidencia — y hoy no cumple.

### 1.5 Links absolutos

Todo está como `file:///home/stemjara/...`. El artefacto no es portable ni
compartible con el jurado o con otro equipo. Pasar a rutas relativas.

---

## 2. Lo que hay que añadir (evidencia que existe y el ARA no recoge)

### 2.1 El confound principal, sin declarar

**Standard y Parsimonious no son dos prompts: son dos arquitecturas.**

| | Standard | Parsimonious |
|---|---|---|
| Llamadas a Gemini | **2** (Modeler → Planner) | **1** |
| Contrato de salida | esquema Pydantic forzado | JSON libre, parseo manual |
| Reintentos | 5 con backoff | solo rota clave en 429 |

Ningún reporte lo dice y todos presentan la comparación como si fuera de
prompts. **Si el artículo compara ambos, esto tiene que estar en el texto**, o
la comparación no es defendible ante un revisor. Está documentado en
`docs/standard-pipeline.md` §1.

### 2.2 Los 56 grafos que Cloudscape marca como inservibles

El GT trae `graph_usable=False` en **56 de 396**, y el pipeline no lo respeta:
`evaluate_graphs.py` filtra con `r.get("graph_usable", True)` pero
`evaluate_pair` nunca setea esa clave, así que **42 grafos inservibles están
dentro de las métricas publicadas**.

Impacto medido (pareados, Service F1):

| Conjunto | n | Standard | Parsimonious |
|---|---:|---:|---:|
| Todos (como se reporta hoy) | 344 | 86.4% | 85.4% |
| Sin `graph_usable=False` | 302 | 86.5% | 85.6% |
| Elegibles y solo inglés | 273 | 86.1% | 85.1% |

Buena noticia para el artículo: **el resultado no depende de a quién incluyas**
(±0.6 puntos). Pero hay que elegir un criterio y declararlo. Recomendación:
reportar sobre los **302 elegibles** y poner el resto como análisis de
sensibilidad — es la postura defendible.

Fuente: `reports/dataset_audit_2026-08-20.md`.

### 2.3 La ablación de prompts completa

Dos generaciones, panel fijo de 14 videos, evaluadas con el mismo `evaluate_pair`
que producción. **Nada de esto está en el ARA** y es el corazón metodológico:

| Gen 1 (`3.5-flash`) | Svc F1 | Edge F1 |
|---|---:|---:|
| V0 Baseline | 90.88% | 61.11% |
| v1_monitoring | 86.87% | 55.10% |
| v1_stage2_strict | 86.09% | 58.81% |
| **v2_verbal** (V0 re-corrido, sin cambios) | **87.90%** | **57.47%** |

| Gen 2 (`3.6-flash`, temp 0) | Svc F1 | Edge F1 |
|---|---:|---:|
| v4_anti_hallucination | **91.62%** | 63.45% |
| v4_dynamic_few_shot (RAG) | 90.09% | 61.51% |
| V5_with_vision (solo visión) | 86.67% | 53.87% |
| V5_STRICT_ROUTING | 90.99% | 65.14% |
| **V6_corrected_v2** ← producción | 89.94% | 65.28% |
| V7_RETURN_FLOWS | 90.58% | 65.73% |
| V7_RETURN_FLOWS_V6 | 89.30% | **66.52%** |

**`v2_verbal` merece un párrafo propio en el artículo:** es V0 re-corrido sin
cambiar nada y dio 87.90% en vez de 90.88%. Tres puntos de puro ruido de
muestreo, más que la diferencia entre varias variantes comparadas. Justifica
por qué se bajó la temperatura a 0 y **fija la barra de significancia**: ninguna
diferencia menor a ~3 puntos en ese panel es señal.

Fuentes: `whiteboard_selection_lab/batch_results_*.json`,
`experiment_history.json`, `Avances/Avance Semanal 3.md`.

### 2.4 Dos callejones sin salida que valen como resultado

- **Few-shot RAG regresó.** Con dos arquitecturas de ejemplo en contexto el
  modelo sobre-conectó, reproduciendo la topología de los ejemplos en vez del
  video.
- **Solo-visión colapsa en aristas** (53.87% vs 61.11%). Buena parte de la
  conectividad del GT se enuncia en el audio y nunca se dibuja: la transcripción
  no es un complemento, **aporta aristas que la imagen no contiene**. Es el
  techo de cualquier enfoque puramente visual y es un resultado publicable.

### 2.5 El linaje de prompts, ahora con hash

Los 16 prompts están extraídos en `src/configs/prompts/` con SHA-256 en
`MANIFEST.json`. Producción corre `STAGE2_V6_CORRECTED` (`ed1d85054d73…`) +
`STAGE1_V0_BASELINE` (`497d30164f48…`), verificado byte a byte.

**Salvedad honesta que el artículo debe respetar:** el notebook redefine las
mismas constantes en celdas distintas, así que un nombre cubre varios textos
(`STAGE2_V6_CORRECTED` tiene tres versiones: 3887, 3974 y 3835 chars). Los
`batch_results_*.json` guardan el nombre, no el hash. **Las filas de generación 2
de la tabla de ablación no se pueden atar a un texto exacto.** O se resuelve
mirando qué celda se ejecutó antes de cada corrida, o se declara como
aproximación.

### 2.6 El `trace/` está casi vacío

Tiene 10 nodos y termina en el cambio a parsimonious. Falta prácticamente todo
el recorrido real, que está documentado en `Proyecto/Chats/` (24 notas) y
`Proyecto/Avances/`: dual-agent, double-shot, few-shot RAG, temperatura 0,
Fleiss kappa, razonamiento semántico contra la ontología Cloudscape, el gap de
bidireccionalidad (33% del GT vs 11% en V6), el borde `-3lnf5lzsH0`, la
exclusión de videos por idioma, y el salto del selector de 60% a 100%.

Los dead ends son ciudadanos de primera en un ARA y además son material de la
sección de discusión del artículo.

---

## 3. Hallazgos nuevos que el artículo debería mencionar

Cosas descubiertas al auditar, que no estaban en ningún documento:

1. **`videos.csv` tenía 14 filas con el `video_id` equivocado** — el título
   nombra un episodio real de la serie pero el ID apunta a otro video de otro
   canal. 9 de esos IDs correctos estaban en el propio catálogo como filas
   huérfanas sin título. Es un problema de calidad del dataset de origen que
   vale la pena reportar.

2. **Resolución como variable oculta.** El selector logra 100% sobre 404 videos
   a ≥720p y 26.5% sobre 67 a 360p. `constraints.md` ya exigía 720p pero nada
   lo hacía cumplir: `VIDEO_FORMAT` degradaba en silencio. Es un requisito
   operativo medido.

3. **42 videos no-inglés**, no los 12 que documentaba `Casos especiales.md`.
   Aparecen coreano (7), alemán (3), árabe (2), mandarín (2), hebreo (1).
   Contraintuitivo: **quitarlos baja el score** (85.8% vs 86.4%), o sea que
   Whisper los maneja bien y no son la fuente de error que se suponía.

4. **21 grafos del GT no tienen aristas**, donde Edge F1 es 0 por construcción.
   Ya se excluyen del promedio de aristas en los evaluadores nuevos; el reporte
   viejo los promediaba.

---

## 4. Orden sugerido

1. **Decidir el conjunto de evaluación** (recomendado: los 302 elegibles) y
   declararlo. Todo lo demás depende de esto.
2. **Regenerar `evidence/`** desde `reports/dataset_audit_2026-08-20.csv` y los
   `reports/runs/*/results.csv`. Nada escrito a mano.
3. **Reescribir los 4 claims** contra esas tablas, con C03 reformulado y C01
   apuntando a la ablación de solo-visión.
4. **Arreglar rutas** (código y links relativos).
5. **Ampliar el `trace/`** desde `Proyecto/Chats/`.
6. **Añadir la sección del confound de arquitectura** (2 fases vs 1).

Los pasos 1–4 son los que bloquean; 5 y 6 enriquecen.

---

## 5. Artefactos citables que ya existen

| Qué | Dónde |
|---|---|
| Auditoría por video (396 filas, todos los flags) | `reports/dataset_audit_2026-08-20.{md,csv}` |
| Corrida Standard con procedencia | `reports/runs/2026-08-16_standard_v6corrected_299v/` |
| Corrida Parsimonious v9 | `reports/runs/2026-08-19_parsimonious_v9/` |
| Prompts con SHA-256 | `src/configs/prompts/MANIFEST.json` |
| Ablación 14 videos | `whiteboard_selection_lab/batch_results_*.json` |
| Historial de prompts parsimonious (42 registros) | `whiteboard_selection_lab/parsimonious_prompt_history.md` |
| Arquitectura de 2 fases y linaje | `docs/standard-pipeline.md` |
| Estado y pendientes | `docs/estado-y-pendientes.md` |
| Línea base congelada | `reports/baseline_2026-08-16.json` |

Regenerables con:

```bash
.venv/bin/python scripts/utils/audit_dataset_coverage.py
.venv/bin/python scripts/utils/evaluate_standard.py --label v6corrected
.venv/bin/python scripts/evaluation/evaluate_parsimonious.py
.venv/bin/python scripts/utils/extract_prompts.py
.venv/bin/python scripts/utils/snapshot_state.py
```

---

## 6. Advertencia sobre el ARA actual

Tal como está, `ara/` **le daría datos falsos a cualquier agente que lo lea**:
cifras que no existen en las fuentes, una muestra sesgada presentada como
completa, y referencias a código que no resuelven. Es lo contrario de para lo
que sirve el formato.

Hasta rehacer `claims.md` y `evidence/`, **no conviene usarlo como insumo del
artículo ni compartirlo**.
