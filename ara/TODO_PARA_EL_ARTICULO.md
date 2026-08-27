# Qué falta en el ARA para que sirva de base al artículo

**Fecha:** 2026-08-20 · **Revisado:** 2026-08-26 (§1.3, §2.3–2.9, §3, §5)
· **Estado del pipeline:** todo procesado (370 Standard / 344 Parsimonious contra 396 GT)
· **Ablación:** 11 variantes de Stage 2 medidas sobre el panel de 30 (§2.3)

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
  *El experimento correcto sería* la ablación `V5_with_vision` (solo visión):
  86.67% Service / 53.87% Edge contra 90.88% / 61.11% del baseline.
  **Pero esas cifras tampoco son citables hoy** (verificado 2026-08-24): su única
  fuente es `Avances/Avance Semanal 3.md`, que no está en el repositorio, y **no
  existe** ningún `batch_results` de esa variante — los cinco que hay son
  `v4_anti_hallucination`, `V5_STRICT_ROUTING`, `V6_corrected_v2`,
  `V7_RETURN_FLOWS` y `V7_RETURN_FLOWS_V6`. Tampoco hay prompt ni script. **C01
  queda sin evidencia de reemplazo**: hay que recuperar ese material o volver a
  correr la ablación de solo-visión antes de poder sostener el claim. Ver §2.4.

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

Panel fijo de 14 videos, evaluados con el mismo `evaluate_pair` que producción.
**Nada de esto está en el ARA** y es el corazón metodológico.

#### Generación 1 (`gemini-3.5-flash`) — histórica, sin hash

| Gen 1 (`3.5-flash`) | Svc F1 | Edge F1 |
|---|---:|---:|
| V0 Baseline | 90.88% | 61.11% |
| v1_default_3.5_flash | 88.92% | 59.77% |
| v1_monitoring | 86.87% | 55.10% |
| v1_stage2_strict | 86.09% | 58.81% |
| **v2_verbal** (V0 re-corrido, sin cambios) | **87.90%** | **57.47%** |

**`v2_verbal` merece un párrafo propio en el artículo:** es V0 re-corrido sin
cambiar nada y dio 87.90% en vez de 90.88%. Tres puntos de puro ruido de
muestreo, más que la diferencia entre varias variantes comparadas. Justifica
por qué se bajó la temperatura a 0 y **fija la barra de significancia**: ninguna
diferencia menor a ~3 puntos en ese panel es señal.

Salvedad: ese piso de ruido se midió **en 3.5-flash**. Aplicarlo a comparaciones
de generación 2 es una extrapolación razonable, no una medición.

Fuente: `whiteboard_selection_lab/experiment_history.json`.

#### Generación 2 — re-corrida completa y verificada por hash (2026-08-24)

La tabla histórica de generación 2 guardaba **el nombre de la variante, no el
hash del texto**, y el notebook redefine las mismas constantes en celdas
distintas — así que sus filas no se podían atar a un prompt concreto. Se
re-corrieron **las 13 variantes de Stage 2**, todas en `gemini-3.6-flash` con
temperatura 0.0, cargando el prompt desde `src/configs/prompts/` y abortando si
el SHA-256 no coincide con `MANIFEST.json`. Stage 1 fijo en `STAGE1_V0_BASELINE`
(cacheado, no se recalcula), que es el de producción.

| Variante | Celda | sha (12) | Svc F1 | Edge F1 |
|---|---|---|---:|---:|
| V4_ANTI_HALLUCINATION | 8 | `cdb8998f48eb` | 90.58% | **65.60%** |
| V5_STRICT_ROUTING | 7 | `53f8d9124406` | **90.99%** | 64.51% |
| V5_STRICT_ROUTING | 8 | `a792c1328d02` | 89.44% | 64.11% |
| V6_OPTIMIZED | 8 | `079b0aa855d7` | 88.43% | 64.11% |
| V7_RETURN_FLOWS | 7 | `1ed4ebf91e68` | 89.75% | 63.89% |
| V7_RETURN_FLOWS_V6 | 10 | `7ad8d9368bce` | 88.15% | 63.89% |
| **V6_CORRECTED** ← producción | 9 | `ed1d85054d73` | 89.79% | 63.21% |
| V6_CORRECTED | 7 | `7228956f5fc6` | 88.26% | 61.64% |
| V6_CORRECTED | 10 | `dbddf1f30bfb` | 89.76% | 60.48% |
| V0_BASELINE | 8 | `feba1e16eb78` | 88.45% | 58.99% |
| V4_ANTI_HALLUCINATION | 7 | `0b9217ea2267` | 88.94% | 58.73% |
| V0_BASELINE | 7 | `4d0def75596f` | 90.75% | 58.29% |
| V4_DYNAMIC_FEW_SHOT | (`.py`) | `45da674e4495` | 89.36% | 56.80% |

Corridas en `reports/ablation/`, cada una con su `run.json` (hash del prompt,
modelo, commit, procedencia del Stage 1 y de la pizarra por video).

**Tres cosas que esta re-corrida corrige de la tabla vieja:**

1. **La fila `V0 (Baseline)` de la tabla de generación 2 estaba medida en
   3.5-flash** (venía arrastrada de `experiment_history.json`). O sea que la
   tabla comparaba dos modelos en un mismo eje. Ahora hay un V0 medido en el
   mismo modelo que el resto.
2. **`v4_dynamic_few_shot` también era 3.5-flash**, y su script
   ([`run_dynamic_few_shot_batch.py:66`](../whiteboard_selection_lab/run_dynamic_few_shot_batch.py))
   nunca fija `temperature`, así que corrió con el default de la API, no en 0.
   Estaba archivada bajo «Gen 2, temp 0» y no era ninguna de las dos cosas.
3. **`V7_RETURN_FLOWS_V6` vs `V6_corrected_v2` estaba confundida.** V7_V6 se
   construye sobre el V6 de la celda 10, no sobre el de la celda 9 (producción).
   La línea que distingue esas dos bases es justamente
   `**Unidirectional Default:** Treat data and control flows as strictly
   unidirectional…` — es decir, exactamente sobre direccionalidad, que es lo que
   V7 modifica. Con la misma base (celda 10): 60.48% → 63.89%.

**Patrón sistemático al re-correr:** Service F1 reproduce casi exacto (±0.15
puntos) pero Edge F1 cae de forma consistente 2–4.7 puntos respecto del
histórico, en las cuatro variantes que tenían número previo. Es un sesgo
direccional, no dispersión aleatoria. No está explicado; el artículo debería
declararlo antes que ignorarlo.

#### Generación 2 sobre el panel ampliado de 30 (2026-08-26) — **la tabla a citar**

El panel se amplió a 30 videos: los 14 originales más 16 elegibles muestreados al
azar (`seed=42`) dentro del mismo rango de complejidad (GT 6–13 nodos, 5–20
aristas), excluyendo los que ya tenían caches de Stage 1 de otros experimentos.
El Stage 1 de esos 16 se generó y cacheó una sola vez (producción nunca lo
persiste), así que cada variante cuesta 30 llamadas de Stage 2.

**11 variantes completas**, todas en `gemini-3.6-flash` a temperatura 0, mismo
Stage 1 cacheado, mismo `evaluate_pair`, cada prompt verificado por SHA-256:

| Variante | Celda | sha (12) | Svc F1 | Edge F1 |
|---|---|---|---:|---:|
| V7_RETURN_FLOWS_V6 | 10 | `7ad8d9368bce` | 88.07% | **60.10%** |
| V6_OPTIMIZED | 8 | `079b0aa855d7` | 86.75% | 59.14% |
| **V6_CORRECTED** ← producción | 9 | `ed1d85054d73` | 88.07% | 58.99% |
| V7_RETURN_FLOWS | 7 | `1ed4ebf91e68` | 86.91% | 58.65% |
| V5_STRICT_ROUTING | 8 | `a792c1328d02` | 86.78% | 58.45% |
| V8_ACTORS_AND_RETURNS | — | `277020bacda4` | 86.21% | 58.40% |
| V6_CORRECTED | 10 | `dbddf1f30bfb` | **88.47%** | 58.10% |
| V5_STRICT_ROUTING | 7 | `53f8d9124406` | 86.65% | 58.08% |
| V6_CORRECTED | 7 | `7228956f5fc6` | 85.92% | 57.52% |
| V6_CORRECTED + evidencia visual | 9 | `ed1d85054d73` | 86.31% | 57.39% |
| V4_ANTI_HALLUCINATION | 8 | `cdb8998f48eb` | 85.62% | 57.10% |

Las once caben en **3 puntos de Edge F1** (57.10–60.10). Corridas en
`reports/ablation/*_p30*/`.

Quedaron sin completar a 30 (checkpoint parcial, no bloquean ninguna conclusión):
`V0_BASELINE` celdas 7 y 8, `V4_ANTI_HALLUCINATION` celda 7 y
`V4_DYNAMIC_FEW_SHOT` — las de menor Edge F1 en el panel de 14.

#### El panel de 14 no generaliza — y no solo en las cifras absolutas

Para el prompt de producción, el desglose:

| Muestra | n | Svc F1 | Edge F1 |
|---|---:|---:|---:|
| Panel original | 14 | 89.79% | 63.99% |
| 16 nuevos | 16 | 86.56% | 54.60% |
| **Combinado** | **30** | **88.07%** | **58.99%** |

*(Esas tres filas salen de una sola corrida de 30, partida en dos. La corrida
independiente sobre los 14 —hecha días antes, con las mismas entradas— había dado
63.21% de Edge F1 contra el 63.99% de acá: **0.78 puntos de diferencia entre dos
corridas del mismo prompt sobre los mismos videos**. Es otra medición directa del
ruido de corrida a corrida, en la línea de lo que estableció `v2_verbal`.)*

El número de 30 queda **mucho más cerca del promedio real sobre los 370
completos** (86.78% / 59.65%, `reports/MANIFEST.md`) que el optimista de 14.

**El ranking tampoco sobrevive.** De las 9 variantes con ambos paneles medidos:

| Variante | Celda | Edge@14 | Edge@30 | Δ |
|---|---|---:|---:|---:|
| V4_ANTI_HALLUCINATION | 8 | **65.60** *(1º)* | 57.10 *(9º)* | −8.50 |
| V5_STRICT_ROUTING | 7 | 64.51 *(2º)* | 58.08 *(7º)* | −6.43 |
| V5_STRICT_ROUTING | 8 | 64.11 *(3º)* | 58.45 *(5º)* | −5.66 |
| V6_OPTIMIZED | 8 | 64.11 *(4º)* | 59.14 *(2º)* | −4.97 |
| V7_RETURN_FLOWS | 7 | 63.89 *(5º)* | 58.65 *(4º)* | −5.24 |
| V7_RETURN_FLOWS_V6 | 10 | 63.89 *(6º)* | **60.10** *(1º)* | −3.79 |
| V6_CORRECTED ← producción | 9 | 63.21 *(7º)* | 58.99 *(3º)* | −4.22 |
| V6_CORRECTED | 7 | 61.64 *(8º)* | 57.52 *(8º)* | −4.12 |
| V6_CORRECTED | 10 | 60.48 *(9º)* | 58.10 *(6º)* | −2.38 |

- **Correlación de rangos Spearman entre ambos paneles: ρ = −0.233.** El orden que
  produce el panel de 14 **no predice** el de 30; si acaso, lo invierte levemente.
  La que salía primera termina última; la que termina primera salía sexta.
- **Correlación entre la posición en el ranking de 14 y la caída al ampliar:
  r = +0.925.** Cuanto mejor puntuaba una variante en el panel chico, más cayó.
  Es la firma cuantificada del sobreajuste a la muestra de selección: el panel de
  14 premiaba el ruido que le era propio.

**Corrección a una versión anterior de este documento**, que decía *"esto no
invalida el orden entre variantes, pero sí cualquier cifra absoluta"*. La segunda
mitad se sostiene; **la primera es falsa** y está desmentida por la tabla de
arriba.

*(Nota metodológica útil: el primer panel de 30 se armó de forma híbrida — los 14
de la ablación más los 16 tomados del CSV de la corrida de producción de 370
videos, sin pagar llamadas nuevas. Dio 87.23 / 59.10 contra 88.07 / 58.99 de la
corrida limpia de punta a punta: **0.11 puntos de diferencia en Edge F1**.
Reutilizar scores de producción para ampliar un panel es válido, y abarata
cualquier ampliación futura.)*

### 2.4 Dos callejones sin salida que valen como resultado

#### Few-shot RAG: resultado nulo, no regresión (corregido 2026-08-24)

El ARA decía *«regresó… el modelo sobre-conectó, reproduciendo la topología de
los ejemplos en vez del video»*. **Las dos mitades de esa frase eran incorrectas**
y se verificaron contra la re-corrida en 3.6-flash / temp 0 (89.36% / 56.80%):

- **«Sobre-conectó» es falso.** Contando aristas generadas contra GT en el panel
  completo, el few-shot dio ratio **0.785**, dentro del rango de las otras 12
  variantes (0.689–0.893) y por debajo de `V7_RETURN_FLOWS` (0.893). Además
  **todas las variantes sub-generan aristas** (ningún ratio llega a 1.0): el
  sesgo sistemático del pipeline es el contrario de sobre-conectar. La
  afirmación no tenía respaldo en ningún dato del repo.
- **«Regresó» hay que matizarlo.** Contra el baseline en el mismo modelo
  (V0 celda 7: 90.75% / 58.29%) da −1.39 / −1.49, **dentro del piso de ruido de
  ~3 puntos**. Contra la mejor variante (65.60%) la brecha sí es real: 8.8
  puntos de Edge F1.

Formulación defendible: **el few-shot RAG no mejora sobre el baseline y queda
claramente por detrás de las variantes con reglas explícitas.** Es un dead end
por no aportar nada, no por romper nada.

**Salvedad metodológica que no estaba documentada:** el retriever
([`dynamic_rag_matcher.py:237`](../whiteboard_selection_lab/algorithms/dynamic_rag_matcher.py))
excluye solo el video objetivo, no el resto del panel. En **4 de 14 casos** el
modelo recibió como ejemplo el ground truth de otro video del mismo panel de
evaluación (`BZ32w0SSAoY` ×2, `wjtSHyENv0I` ×2). No es fuga directa de la
respuesta —cada video se puntúa contra su propio GT— pero el método se midió con
acceso a GT del mismo corpus, algo que en despliegue real no existe. El 56.80%
es por tanto un **techo optimista**, lo que refuerza la conclusión.

El prompt estaba hardcodeado en un `.py` fuera del alcance de
`extract_prompts.py` (que solo escanea el notebook); por eso era el único del
linaje sin hash. Ya está extraído a `src/configs/prompts/stage2_v4_dynamic_few_shot.txt`
(`45da674e4495…`) y registrado en `MANIFEST.json`.

#### Solo-visión: **no reproducible, no citable todavía**

- **Solo-visión colapsa en aristas** (86.67% / 53.87% vs 61.11%). Buena parte de
  la conectividad del GT se enuncia en el audio y nunca se dibuja: la
  transcripción no es un complemento, **aporta aristas que la imagen no
  contiene**. Es el techo de cualquier enfoque puramente visual y sería un
  resultado publicable.

**Pero esas cifras no se pueden verificar hoy.** Su única fuente es
`Proyecto/Avances/Avance Semanal 3.md`, que **no está en el repositorio**, y a
diferencia del few-shot **no existe ni script ni prompt** de este experimento en
ningún lado. No hay `batch_results`, ni entrada en `experiment_history.json`, ni
artefactos en `lab_workspace/`. Antes de citarlo hay que recuperar ese material
o volver a correrlo; tal como está incumple la regla de trabajo de este
documento.

### 2.5 El linaje de prompts, ahora con hash — **resuelto**

Los 17 prompts están extraídos en `src/configs/prompts/` con SHA-256 en
`MANIFEST.json` (13 de Stage 2 + 4 de Stage 1). Producción corre
`STAGE2_V6_CORRECTED` (`ed1d85054d73…`, celda 9) + `STAGE1_V0_BASELINE`
(`497d30164f48…`), verificado byte a byte.

El problema que había: el notebook redefine las mismas constantes en celdas
distintas, así que un nombre cubre varios textos (`STAGE2_V6_CORRECTED` tiene
tres versiones: 3887, 3974 y 3835 chars) y los `batch_results_*.json` guardan el
nombre, no el hash. **Las filas de generación 2 no se podían atar a un texto
exacto.**

**Ya no aplica.** Se re-corrieron las 13 variantes con verificación de hash
(§2.3), así que cada fila de la tabla nueva apunta a un texto concreto. Dos
resultados de esa desambiguación:

- El `V6_corrected_v2` histórico **era la celda 9** (producción): re-correrla
  reprodujo su Service F1 casi exacto (89.79 vs 89.94).
- La comparación `V7_RETURN_FLOWS_V6` vs `V6_corrected_v2` de la tabla vieja
  **estaba confundida** por bases distintas — ver §2.3, punto 3.

Queda un residuo menor: para `v4_anti_hallucination` y `V5_STRICT_ROUTING` hay
dos textos (celda 7 y celda 8) y ambos están medidos, pero **no se sabe cuál de
los dos produjo la fila histórica**. Como las dos versiones están en la tabla
nueva con su hash, el artículo puede citar cualquiera sin ambigüedad; lo que no
puede es citar el número histórico.

El único prompt que vivía fuera del notebook (`STAGE2_V4_DYNAMIC_FEW_SHOT`,
hardcodeado en un `.py`) ya está extraído y hasheado — ver §2.4. Conviene
extender `extract_prompts.py` para que escanee también los `.py` del laboratorio,
o el próximo prompt definido fuera del notebook se perderá igual.

### 2.6 El `trace/` está casi vacío

Tiene 10 nodos y termina en el cambio a parsimonious. Falta prácticamente todo
el recorrido real, que está documentado en `Proyecto/Chats/` (24 notas) y
`Proyecto/Avances/`: dual-agent, double-shot, few-shot RAG, temperatura 0,
Fleiss kappa, razonamiento semántico contra la ontología Cloudscape, el gap de
bidireccionalidad (33% del GT vs 11% en V6), el borde `-3lnf5lzsH0`, la
exclusión de videos por idioma, y el salto del selector de 60% a 100%.

Los dead ends son ciudadanos de primera en un ARA y además son material de la
sección de discusión del artículo.

**`Proyecto/` no está en este repositorio.** Todo lo que esa lista cita como
fuente es hoy inverificable. De esa lista, `few-shot RAG` sí se pudo reconstruir
(tenía script y prompt en el repo, ver §2.4); **`double-shot` no**: aparece una
única vez, como palabra suelta en esta misma línea, sin script, prompt ni
resultados en ningún lado. Puede que sea otro nombre para el few-shot RAG
(`top_k=2`, dos ejemplos), pero eso no se puede confirmar con lo que hay.
Antes de citar cualquier cosa de esta lista hay que traer `Proyecto/` al
repositorio o volver a correr el experimento.

### 2.7 Anatomía del error de aristas — y un experimento negativo (2026-08-26)

Edge F1 es la métrica débil del pipeline (~59% contra 88% de Service F1). Se
descompuso el error del prompt de producción sobre el panel de 30 para saber
**por qué** falla, en vez de seguir probando variantes a ciegas.

#### El experimento: inyectar la topología visual en Stage 2

El detector de pizarra ya calcula dos cosas: las cajas de los íconos **y** una
máscara de los trazos dibujados entre ellos. Solo sobrevive la primera —
`format_symbols_for_prompt` inyecta posiciones (y solo en Stage 1); la máscara de
trazos se pinta de amarillo en una imagen de debug y se descarta.

Se recuperó ese canal (`scripts/ablation/connection_evidence.py`): los trazos se
convierten en vínculos candidatos `ícono ↔ ícono`, y se le pasa a Stage 2 una
segunda imagen con **badges numerados** sobre cada ícono más la lista de vínculos.
Se usaron badges y no coordenadas porque la convención espacial de Gemini es
normalizada 0–1000 y la imagen se reescala internamente: los píxeles del original
no son una referencia que el modelo pueda resolver de forma confiable.

**Resultado: sin efecto.**

| | Svc F1 | Edge F1 | aristas gen. | ratio vs GT |
|---|---:|---:|---:|---:|
| V6 c9 (producción) | 88.07 | 58.99 | 269 | 0.75 |
| V6 c9 + evidencia | 86.31 | 57.39 | 272 | 0.75 |

Pareado: gana 4, pierde 7, **empata 19** → p = 0.549. Se inyectaron **244 pares**
(8.1 por video) y el modelo generó **3 aristas más en total**. Precisión y recall
de aristas quedaron planas (69.6→68.8 y 53.8→52.2). El modelo, sencillamente,
**ignoró la evidencia**.

Descarta el riesgo que motivaba la cautela (que tomara los pares como permiso para
alucinar) y descarta también el beneficio. Corrida en
`reports/ablation/2026-08-26_0135_STAGE2_V6_CORRECTED_cell9_p30_connev/`.

#### Por qué no sirvió: la anatomía del error

Descomponiendo las **178 aristas del GT que se pierden** (de 361, un 49.3%):

| Causa | aristas | % |
|---|---:|---:|
| **Falta la arista de RETORNO** (el modelo puso `b→a` pero no `a→b`) | **80** | 45% |
| **Falta un nodo** (no puede conectar lo que no existe) | 58 | 33% |
| Ambos nodos presentes, sin conexión en ningún sentido | 40 | 22% |

Y de las 58 por nodo ausente, **53 (91%) son actores `User*` o `ThirdParty`** —
`UserConsumerWeb` sola cuesta 22 aristas.

**Las dos causas principales son reglas explícitas del prompt de producción:**

1. `**Unidirectional Default:** Treat data and control flows as strictly
   unidirectional` → las 80 aristas de retorno.
2. `5. **Pruning:** Remove generic human actors or purely physical concepts` →
   los actores `User*`. **El prompt se contradice a sí mismo**: ofrece un
   vocabulario `User and Client Actors` en su encabezado y luego ordena eliminar
   actores humanos. El GT tiene **34 actores `User*`, el 13% de todos sus nodos**.

Juntas explican **133 de 178 aristas perdidas (75%)**.

#### El techo de la direccionalidad

El GT tiene **41.1%** de sus pares conectados en ambos sentidos; producción produce
**6.4%**, y ni el prompt que permite retornos llega lejos:

| | % pares bidireccionales |
|---|---:|
| Ground truth | 41.1% |
| V7_RETURN_FLOWS | 10.3% |
| V6_CORRECTED (producción) | 6.4% |
| V4_ANTI_HALLUCINATION | 4.4% |

Colapsando a pares no dirigidos, el Edge F1 de producción pasa de **62.23 a
73.40**: si la dirección fuera gratis se ganarían **+11.17 puntos**.

*(Advertencia metodológica: una primera medición dio "+2.6 puntos" usando
multiconjuntos, que siguen penalizando la arista de retorno ausente y por lo tanto
no aíslan la dirección. El número correcto exige colapsar a un conjunto de pares no
ordenados. El `ara/` no debe citar la cifra de 2.6.)*

*(El `ara/` decía antes "33% del GT vs 11% en V6". Sobre el panel de 30 medido con
hash da 41.1% vs 6.4%.)*

### 2.8 V8: arreglar las dos reglas culpables — los mecanismos funcionan, el F1 no (2026-08-26)

§2.7 identificó dos reglas del prompt de producción responsables de 133 de las 178
aristas perdidas. Se construyó `STAGE2_V8_ACTORS_AND_RETURNS`
(`src/configs/prompts/stage2_v8_actors_and_returns.txt`, sha `277020bacda4…`),
idéntico a V6 celda 9 salvo **tres bloques**, verificado por diff:

1. La regla 5 pasa de `**Pruning:** Remove generic human actors…` a
   `**Actor Mapping (CRITICAL — DO NOT PRUNE ACTORS)**`: los actores humanos y
   clientes se mapean contra la lista `User and Client Actors` en vez de podarse.
   Se conservó a propósito la poda de conceptos físicos sin flujo *(incluidos los
   presentadores)*, porque en estos videos siempre hay dos personas frente a la
   pizarra.
2. Se elimina `**Unidirectional Default:** Treat data and control flows as
   strictly unidirectional`.
3. Se agrega el bloque `## EXPLICIT RETURN PATHS & BIDIRECTIONALITY RULES` de V7,
   copiado textual para que el efecto sea atribuible a una formulación ya probada
   y no a redacción nueva.

Corrida con una sola imagen (igual que producción) y Stage 1 cacheado, sobre el
panel de 30.

**Los dos mecanismos hicieron exactamente lo previsto:**

| | Svc F1 | Edge F1 | aristas gen. | % bidir | actores `User*` |
|---|---:|---:|---:|---:|---:|
| V6 c9 (producción) | 88.07 | 58.99 | 269 | 12.4% | 20 |
| **V8** | **86.21** | **58.40** | **299** | **17.9%** | **29** |
| Ground truth | — | — | 361 | 41.1% | 34 |

Actores recuperados: 20 → 29 de 34. Bidireccionalidad: 12.4% → 17.9%. Aristas
generadas: +30.

**Y el Edge F1 no se movió**: 58.99 → 58.40, pareado 6-9 con 15 empates,
**p = 0.607**. Las 30 aristas nuevas son mayoritariamente incorrectas.

**Además degrada Service F1 de forma significativa:** pareado 1-8 con 21 empates,
**p = 0.039**. Con 9 actores más, algunos se mapean a la entrada equivocada de la
lista. El daño es chico pero sistemático — **V8 no debe ir a producción**.

Corrida en `reports/ablation/2026-08-26_0307_STAGE2_V8_ACTORS_AND_RETURNS_cellNone_p30/`.

#### La lección metodológica

El razonamiento era: *"133 aristas se pierden por estas dos reglas, arreglalas y
las recuperás"*. **La contabilidad de errores no es un mapa de mejoras
disponibles.** El modelo ahora *puede* emitir retornos y actores, y los emite —
pero no acierta *cuáles*. Saber que falta una arista de retorno no es lo mismo que
saber entre qué dos servicios va.

### 2.9 Ninguna intervención movió el Edge F1 — y ninguna diferencia es significativa

Es el patrón más citable de toda la auditoría. Sobre el mismo panel de 30, mismo
modelo, mismo Stage 1 cacheado, evaluación **pareada por video** (test de signos):

| Intervención | Mecanismo | Resultado | p |
|---|---|---|---:|
| 11 variantes de prompt (§2.3) | reescrituras de reglas | indistinguibles entre sí | 0.118–1.000 |
| Few-shot RAG (§2.4) | 2 arquitecturas GT en contexto | nulo | — |
| Evidencia visual de conexiones (§2.7) | topología detectada por CV | nulo, el modelo la ignoró | 0.549 |
| V8, reglas dirigidas por error (§2.8) | actores + retornos | mecanismos sí, F1 no | 0.607 |
| V7_RETURN_FLOWS_V6 (§2.3) | retornos sobre base V6 sin regla unidireccional | mejor de la tabla, **no significativo** | 0.581 |

Cada intervención estuvo mejor fundamentada que la anterior y ninguna movió el
Edge F1 de forma detectable. El dato que lo explica: en las comparaciones pareadas
hay **entre 12 y 19 empates de 30**, y en **9 de 30 videos las cuatro variantes
principales dan Edge F1 idéntico**. Los prompts se diferencian mucho menos de lo
que sugieren sus promedios.

**Conclusión defendible: el Edge F1 de ~59% no está limitado por el prompt de
Stage 2.** El cuello de botella está en otro lado — Stage 1, la ontología de
evaluación, o la ambigüedad inherente entre lo que se dibuja y lo que se narra.
Seguir iterando prompts de Stage 2 tiene rendimiento esperado bajo y entra en
terreno de ajustar hasta que el número guste.

#### La única candidata, y por qué NO se cambia producción

`V7_RETURN_FLOWS_V6` (celda 10) encabeza la tabla de 30 con **60.10%** de Edge F1
contra **58.99%** de producción, con **el mismo Service F1 (88.07%)** y sin la
degradación que sí mostró V8. Es la única variante que queda por encima de
producción en aristas sin costo en servicios, y su mecanismo avanzó más que
ninguna otra: **21.9% de pares bidireccionales contra 12.4% de producción**
(GT: 41.1%).

Pero pareado da **8-5 con 17 empates, p = 0.581**. **No hay evidencia para
cambiar el prompt de producción.** Es la candidata a re-evaluar si alguna vez se
mide sobre una muestra mayor, no un resultado.

Tiene además un interés teórico: es exactamente V6 sin `Unidirectional Default`
más las reglas de retorno de V7 — o sea, la hipótesis de §2.7 y §2.8 aplicada
sobre la base que mejor identifica pares. Que sea la mejor de las once es
coherente con el diagnóstico; que no sea significativa es coherente con todo lo
demás.

---

## 3. Hallazgos nuevos que el artículo debería mencionar

Cosas descubiertas al auditar, que no estaban en ningún documento:

1. **`videos.csv` tenía 14 filas con el `video_id` equivocado** — el título
   nombra un episodio real de la serie pero el ID apunta a otro video de otro
   canal. 9 de esos IDs correctos estaban en el propio catálogo como filas
   huérfanas sin título. Es un problema de calidad del dataset de origen que
   vale la pena reportar.

2. **Resolución: correlación con la confianza del selector automático, no con si
   el frame sirve.** El selector automático emite un candidato de alta confianza
   100% de las veces sobre 404 videos a ≥720p, y solo 26.5% sobre 67 a 360p. Esa
   cifra describe la seguridad del *scorer automático*, no la usabilidad real del
   frame — `constraints.md` los confundía y pedía 720p como requisito de entrada.
   Corregido el 2026-08-21 con evidencia directa: de 17 videos nuevos procesados
   (todos cayeron a 640×360 por falta de un PO-Token provider local para yt-dlp,
   un problema distinto al de las cookies), 3 fueron aprobados a mano como pizarra
   válida a la misma resolución en la que otros 12 fallaron. La resolución sola no
   explica el resultado. Hipótesis de trabajo, sin validar todavía: el detector de
   íconos (`symbol_detector.py`) usa umbrales HSV fijos que pueden estar calibrados
   para un estilo particular de pizarra/marcador, y fallar en otros estilos
   independientemente de la resolución. Ver `constraints.md` §2.3 para el detalle
   y la evidencia. `VIDEO_FORMAT` sigue degradando en silencio — eso sigue siendo
   cierto y sigue siendo forzable — pero "forzar 720p" ya no es la corrección que
   hay que documentar como la causa raíz.

3. **42 videos no-inglés**, no los 12 que documentaba `Casos especiales.md`.
   Aparecen coreano (7), alemán (3), árabe (2), mandarín (2), hebreo (1).
   Contraintuitivo: **quitarlos baja el score** (85.8% vs 86.4%), o sea que
   Whisper los maneja bien y no son la fuente de error que se suponía.

4. **21 grafos del GT no tienen aristas**, donde Edge F1 es 0 por construcción.
   Ya se excluyen del promedio de aristas en los evaluadores nuevos; el reporte
   viejo los promediaba.

5. **El panel de 14 videos con el que se eligió el prompt de producción no
   generaliza — ni en las cifras ni en el orden** (medido 2026-08-24/26 sobre 11
   variantes). Ampliado a 30 videos elegibles del mismo rango de complejidad, el
   prompt de producción cae de 89.79% / 63.99% a 88.07% / 58.99%, quedando cerca
   del promedio real sobre los 370 completos (86.78% / 59.65%). Y el ranking entre
   variantes **se desarma**: correlación de Spearman ρ = −0.233 entre ambos
   paneles, con r = +0.925 entre lo bien que puntuaba una variante a 14 y lo mucho
   que caía a 30. Ver §2.3.

6. **Dos filas de la tabla de ablación estaban archivadas bajo el modelo
   equivocado** (2026-08-24): `V0 (Baseline)` y `v4_dynamic_few_shot` figuraban
   como generación 2 (`3.6-flash`, temp 0) cuando ambas se midieron en
   `3.5-flash`, y el few-shot además nunca fijó temperatura. La tabla comparaba
   dos modelos en un mismo eje. Ya está re-medido todo en un solo modelo (§2.3).

7. **El 75% de las aristas que se pierden lo causan dos reglas del propio prompt
   de producción** (2026-08-26): la que fuerza flujos unidireccionales (80 aristas
   de retorno) y la que ordena podar actores humanos (53 aristas, con el prompt
   contradiciendo su propio vocabulario `User and Client Actors`). Ver §2.7. Es
   el hallazgo más accionable de toda la auditoría: a diferencia de las variantes
   de prompt —estadísticamente indistinguibles entre sí (§2.3)— acá hay un
   mecanismo medido con ~133 aristas en juego.

---

## 4. Orden sugerido

1. **Decidir el conjunto de evaluación** (recomendado: los 302 elegibles) y
   declararlo. Todo lo demás depende de esto.
2. **Regenerar `evidence/`** desde `reports/dataset_audit_2026-08-20.csv` y los
   `reports/runs/*/results.csv`. Nada escrito a mano.
3. **Reescribir los 4 claims** contra esas tablas, con C03 reformulado. C01 no
   se puede cerrar todavía: su evidencia de reemplazo (solo-visión) resultó ser
   inverificable — hay que recuperar `Proyecto/` o volver a correr esa ablación
   (§1.3, §2.4).
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
| Prompts con SHA-256 (17: 13 Stage 2 + 4 Stage 1) | `src/configs/prompts/MANIFEST.json` |
| **Ablación verificada por hash: 14 variantes a 14 videos, 11 a 30** | `reports/ablation/*/run.json` |
| Tabla principal del artículo (11 variantes × 30 videos) | `reports/ablation/*_p30*/run.json` |
| Respaldo del panel de 14 antes de ampliar | `reports/ablation_backup_2026-08-24_14v/` |
| Evidencia visual de conexiones (experimento nulo) | `reports/connection_evidence/`, `scripts/ablation/connection_evidence.py` |
| Ablación 14 videos (histórica, solo por nombre) | `whiteboard_selection_lab/batch_results_*.json` |
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

La ablación se re-corre por variante (14 llamadas cada una, Stage 1 cacheado):

```bash
.venv/bin/python scripts/ablation/rerun_panel.py --list
.venv/bin/python scripts/ablation/rerun_panel.py --prompt stage2_v6_corrected__cell9.txt
```

---

## 6. Advertencia sobre el ARA actual

Tal como está, `ara/` **le daría datos falsos a cualquier agente que lo lea**:
cifras que no existen en las fuentes, una muestra sesgada presentada como
completa, y referencias a código que no resuelven. Es lo contrario de para lo
que sirve el formato.

Hasta rehacer `claims.md` y `evidence/`, **no conviene usarlo como insumo del
artículo ni compartirlo**.
