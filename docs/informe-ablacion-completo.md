# Extracción automática de arquitecturas cloud desde video: metodología, experimentos y hallazgos

**Versión:** 2026-08-26 · **Alcance:** pipeline Standard, ablación de prompts de Stage 2,
evaluación estricta y permisiva.

Documento de lectura detallada. Reúne el contexto, la metodología, qué se corrió bajo
qué condiciones, qué se actualizó hoy, y qué se puede y no se puede concluir.

Regla que gobierna todo lo que sigue: **ningún número entra acá si no se puede señalar
el archivo que lo produjo.**

---

## 1. Contexto

### 1.1 El problema

Las arquitecturas cloud se comunican, en la práctica, dibujándolas. La serie *This Is My
Architecture* de AWS es un corpus natural de eso: un ingeniero explica su arquitectura
frente a una pizarra mientras la señala. El contenido está ahí, pero en una forma que
ningún sistema puede consultar — es video.

El objetivo del trabajo es convertir ese video en un **grafo dirigido y tipado** de la
arquitectura: nodos que son servicios AWS o actores, aristas que son flujos de datos,
control o monitoreo.

### 1.2 El benchmark

Se evalúa contra **Cloudscape** (FAST '25), un dataset de 396 arquitecturas anotadas a
mano a partir de esa misma serie. Cada entrada es un `.graphml` con nodos etiquetados
por servicio y aristas tipadas. Da una referencia externa y no auto-generada, que es lo
que hace la evaluación defendible.

> **Advertencia de licencia:** Cloudscape no declara licencia — ni el repositorio
> canónico (`WiscADSL/Cloudscape`) ni el del primer autor. Redistribuir sus 396
> `.graphml` y `services.csv` no está permitido por defecto. Lo correcto es fijar el
> commit upstream en un script de descarga y citar el BibTeX de FAST '25, no incluir
> los archivos.

### 1.3 Las dos arquitecturas comparadas

El proyecto contrasta dos pipelines. **Esto no es una comparación de prompts, son dos
arquitecturas distintas**, y el artículo debe declararlo o la comparación no se sostiene
ante un revisor:

| | Standard | Parsimonious |
|---|---|---|
| Llamadas a Gemini | **2** (Modeler → Planner) | **1** |
| Contrato de salida | esquema Pydantic forzado | JSON libre, parseo manual |
| Reintentos | 5 con backoff exponencial | solo rota clave en 429 |

Este documento cubre **Standard**. Parsimonious es trabajo de la otra integrante y sus
archivos no se tocan.

---

## 2. El pipeline de ejecución

### 2.1 Vista general

```
video de YouTube
      │
      ├─→ descarga (yt-dlp)  ──────────────→  .mp4 + .info.json
      │
      ├─→ transcripción (Whisper) ─────────→  {id}_transcript.json
      │
      ├─→ extracción de frames ────────────→  candidatos de pizarra
      │        │
      │        └─→ selección automática ───→  data/bad_whiteboard/{id}.jpg
      │                   │
      │                   └─→ CURACIÓN MANUAL ─→ data/good_whiteboard/{id}.jpg
      │
      └─→ análisis de visión (2 etapas)
                 │
                 ├─ Stage 1 · Modeler  →  World Model (inventario visual)
                 │                        entities[] + visual_connections[]
                 │
                 └─ Stage 2 · Planner  →  grafo final
                                          nodes[] + edges[] tipadas
                                              │
                                              └─→ data/graphs/{id}.graphml
```

### 2.2 Las dos etapas del análisis

**Stage 1 — Modeler ("los ojos").** Extrae un inventario literal: qué entidades hay
dibujadas, cómo están agrupadas visualmente, qué líneas las conectan. **No** produce el
grafo final. Su salida es el *World Model*, un JSON con `entities[]` y
`visual_connections[]`.

**Stage 2 — Planner ("el cerebro").** Toma el World Model como entrada principal, más la
imagen y la transcripción completa, y compila el grafo final: poda, fusiona, expande
abstracciones genéricas según lo que diga el audio, y tipa las aristas.

Separar las etapas tiene dos consecuencias que importan para los experimentos:

1. **Aísla la variable.** Si el World Model se mantiene fijo, cualquier diferencia medida
   es atribuible a Stage 2.
2. **Permite cachear.** El World Model se genera una vez por video y se reutiliza en
   todas las variantes de Stage 2. Un panel completo cuesta *n* llamadas en vez de *2n*.

> **Detalle importante:** producción **nunca persiste** el World Model
> ([`vision_analyzer.py:365`](../scripts/core/vision_analyzer.py)) — lo genera en memoria,
> lo usa y lo descarta. Solo guarda la salida de Stage 2. Por eso ampliar el panel a
> videos que el laboratorio nunca tocó obliga a pagar Stage 1 una vez para ellos.

### 2.3 Configuración de ejecución

| Aspecto | Valor |
|---|---|
| Modelo | `gemini-3.6-flash` |
| Temperatura | **0.0**, ambas etapas |
| Contrato de salida | Pydantic `response_schema` vía `types.GenerateContentConfig` |
| Reintentos | 5, backoff exponencial (10 → 20 → 40 → 80 s) |
| Rotación de claves | ante 429 / `RESOURCE_EXHAUSTED` |
| Entrada de imagen | frame aprobado de `data/good_whiteboard/{id}.jpg` |
| Salida | `data/graphs/{id}.graphml` |

La temperatura 0 se fijó como consecuencia de un hallazgo empírico, no por convención
— ver §5.1.

### 2.4 Algoritmos de visión

**Selección de frame de pizarra.** El pipeline extrae candidatos y puntúa cuál muestra
mejor la arquitectura completa. Módulos: [`scripts/core/frame_selector.py`](../scripts/core/frame_selector.py), más una
familia de filtros en `scripts/utils/` (`pizarra_occlusion_filter.py`,
`pizarra_outro_filter.py`, `pizarra_template_matching.py`).

**Detector adaptativo de pizarra**
([`scripts/core/adaptive_whiteboard_detector.py`](../scripts/core/adaptive_whiteboard_detector.py)). Distingue dos
entornos —estudio clásico con franja negra vs. pizarra digital a pantalla completa— y
sobre el área detectada:

1. Segmenta **íconos de servicio** por máscaras híbridas de color y blanco, con filtrado
   por anillo de contraste local. Devuelve caja, centroide y etiqueta de cada uno.
2. Calcula una máscara de **trazos de conexión**: Canny sobre la imagen suavizada, con
   las cajas de íconos recortadas, y dilatación.

La salida de (1) se inyecta a Stage 1 como texto (posiciones de íconos). **La de (2) solo
se dibujaba en una imagen de depuración y se descartaba** — ver §6.3.

**Curación manual.** No existe camino automático hacia `data/good_whiteboard/`. Todo
frame que llegó ahí fue aprobado a mano por una persona tras revisar la propuesta
automática. El mecanismo de registro de esa curación es el mensaje de commit.

---

## 3. Cómo se evalúa

### 3.1 Evaluación estricta (la métrica principal)

Implementada en [`scripts/utils/evaluate_graphs.py`](../scripts/utils/evaluate_graphs.py),
función `evaluate_pair`. Es **agnóstica al identificador**: compara por **nombre de
servicio**, no por ID de nodo, porque el grafo generado y el ground truth numeran sus
nodos de forma independiente.

**Service F1** — sobre el *multiconjunto* de servicios. Si el GT tiene tres Lambdas y el
modelo produce dos, cuenta como 2 de 3, no como acierto binario.

**Edge F1** — sobre el *multiconjunto* de pares `(servicio_origen, servicio_destino)`,
**dirigidos**, ignorando el tipo de arista.

**Filtros de elegibilidad.** El GT marca `graph_usable=False` en 56 de 396 grafos, y hay
21 con cero aristas donde el Edge F1 es 0 por construcción. Ambos se excluyen de los
promedios publicados.

### 3.2 Evaluación permisiva (métrica secundaria)

Origen: [`whiteboard_selection_lab/evaluacion_permisiva.py`](../whiteboard_selection_lab/evaluacion_permisiva.py),
introducida el **2026-07-26**
durante las primeras pruebas de prompts. Su docstring declara **dos** intenciones:

1. **Normalización permisiva de nodos.** Todo actor `User*` (o con `capability='User'`)
   colapsa a `User`; todo sistema externo u on-prem colapsa a `ThirdParty`. Los servicios
   AWS se mantienen exactos.
2. **Conectividad base no dirigida.** Evalúa si *existe estructuralmente* una conexión
   entre dos servicios normalizados, sin importar la dirección.

Pero la implementación efectiva relaja **tres** cosas, no dos. La tercera —usar conjuntos
en vez de multiconjuntos— merece su propia sección.

### 3.3 La regla de conjuntos: qué hace y de dónde salió

**Qué hace.** Un multiconjunto cuenta repeticiones; un conjunto las colapsa a una.

Ejemplo real del panel — `-wLEkq21cvA`, una migración on-prem a AWS. Su ground truth
tiene:

```
EC2 ×3            ThirdParty ×3
arista  ThirdParty → EC2  ×3      (tres servidores, cada uno a su propia instancia)
```

- **Con multiconjunto:** son tres aristas distintas. Un modelo que detecta un solo par
  `ThirdParty→EC2` obtiene recall 1/3 en ese patrón.
- **Con conjunto:** las tres colapsan a un único `{EC2, ThirdParty}`. **El modelo que
  encontró una de tres obtiene crédito completo.**

No es un caso marginal: en el GT de los 30 videos del panel ampliado, **47 de 361 aristas
(13.0%)** repiten un par ya conectado y **40 de 262 nodos (15.3%)** son instancias
repetidas de un servicio ya presente.

**Por qué probablemente se usó.** La arqueología del código sugiere que **no fue una
decisión deliberada sino una consecuencia de cómo se formuló la pregunta**, y hay
evidencia concreta:

- El docstring original enumera solo dos relajaciones. La de conjuntos **no se menciona**.
- Para **nodos**, el autor calculó explícitamente *ambas* versiones —
  `gen_norm_set = set(...)` y `c_gen = Counter(...)` — o sea que la distinción estaba
  presente y era consciente.
- Para **aristas**, en cambio, solo existe la versión de conjunto:
  `edges = set()` con `pair = tuple(sorted([su, sv]))`.

La explicación más plausible: la pregunta que se estaba haciendo era *"¿existe
estructuralmente una conexión base entre A y B?"*, y eso es inherentemente binario por
par — un conjunto es la estructura natural para representarlo. La deduplicación no fue el
objetivo, fue el vehículo.

Después, cuando [`scripts/generate_comparison_plots.py`](../scripts/generate_comparison_plots.py)
(2026-08-04) reimplementó la evaluación
permisiva para las gráficas comparativas, copió **solo la variante de conjunto** también
para los nodos, descartando el multiconjunto que el original sí calculaba. Así la
relajación se extendió de aristas a nodos sin que mediara una decisión explícita.

**Por qué importa.** El prompt de producción tiene una regla dedicada precisamente a esta
distinción:

> `4. **Dynamic Logical Fusion:** Evaluate multiple icons of the same service dynamically.
> If they act as a single logical unit, FUSE them. If they perform distinct architectural
> steps (e.g., three Lambda functions doing different processing stages), KEEP THEM
> SEPARATE as distinct nodes.`

Es decir: **el pipeline está diseñado para decidir fusionar-o-separar, y la regla de
conjuntos hace esa decisión inmedible** — da el mismo puntaje al modelo que acierta la
multiplicidad y al que la ignora. Ver §7.3 para la recomendación.

### 3.4 Prueba estadística

Todas las variantes corren sobre **los mismos videos**, así que la comparación correcta
es **pareada**: por cada video se mira cuál de las dos variantes ganó, y se aplica un
**test de signos** de dos colas sobre los no empatados.

Es mucho más potente que comparar promedios contra un piso de ruido, porque elimina la
varianza entre videos, que es la dominante. Cuando hay muchas comparaciones se aplica
además **corrección de Bonferroni**.

---

## 4. Resultados a escala completa

### 4.1 Cobertura del dataset

| | n |
|---|---:|
| Ground truth de Cloudscape | 396 |
| Pareados (grafo generado + GT) | 385 |
| Evaluados en la corrida publicada | 370 |
| **Elegibles** (pareado ∧ `graph_usable` ∧ no especial) | **336** |
| Puntuados para aristas | 321 |

Los 11 sin grafo son 7 episodios especiales o recopilatorios detectados por título, dos
detectados en vivo por `main.py` que la auditoría por catálogo no ve, y dos con
`gt_usable=False` omitidos a propósito.

### 4.2 Métricas de la corrida completa

`reports/runs/2026-08-20_standard_v6corrected_370v/` · commit `a415d5d` ·
`gemini-3.6-flash` · n = 370, aristas sobre n = 321.

| Métrica | Media | Mediana | Mín | Máx |
|---|---:|---:|---:|---:|
| Service precision | 88.61 | 88.89 | 50.0 | 100.0 |
| Service recall | 85.70 | 85.71 | 50.0 | 100.0 |
| **Service F1** | **86.78** | 87.50 | 50.0 | 100.0 |
| Edge precision | 70.36 | 75.00 | 0.0 | 100.0 |
| Edge recall | 53.99 | 53.33 | 0.0 | 100.0 |
| **Edge F1** | **59.65** | 60.87 | 0.0 | 100.0 |

**La asimetría es el hecho central del proyecto:** identificar *qué servicios* aparece
resuelto (86.78%); identificar *cómo se conectan* no (59.65%). Y dentro del Edge F1, la
precisión (70.36) supera holgadamente al recall (53.99): el modelo es conservador —
cuando emite una arista suele acertar, pero **deja de emitir casi la mitad de las que
existen**.

### 4.3 Standard vs Parsimonious

| Conjunto | n | Standard | Parsimonious | Δ |
|---|---:|---:|---:|---:|
| Todos los pareados | 385 | 86.2% | 85.0% | −1.2 |
| **Elegibles** | **336** | **86.7%** | **85.5%** | **−1.2** |

El resultado **no depende del criterio de inclusión** (±0.6 puntos entre conjuntos), lo
cual es buena noticia; pero hay que elegir uno y declararlo. Recomendación: reportar
sobre los 336 elegibles y poner el resto como análisis de sensibilidad.

### 4.4 Un resultado contraintuitivo

Los videos en idiomas distintos del inglés (42 en el conjunto elegible) puntúan **más
alto** que los ingleses: Service F1 90.93 vs 86.30, Edge F1 67.84 vs 58.71. No se explica
por arquitecturas más simples — sus grafos GT tienen en promedio *más* nodos (9.91 vs
9.01) y más aristas (12.85 vs 12.37).

Explicación probable: los nombres de servicios AWS se mantienen en inglés
independientemente del idioma de la narración. Salvedad: el *n* por idioma individual es
diminuto (mandarín 2, árabe 1, hebreo 1), así que los deltas por idioma son ruido; solo
el agregado es interpretable.

---

## 5. La ablación de prompts

### 5.1 Generación 1 — el hallazgo que fijó la metodología

Panel de 14 videos, `gemini-3.5-flash`. Fuente:
`whiteboard_selection_lab/experiment_history.json`.

| Variante | Svc F1 | Edge F1 |
|---|---:|---:|
| V0 Baseline | 90.88 | 61.11 |
| v1_default_3.5_flash | 88.92 | 59.77 |
| v1_monitoring | 86.87 | 55.10 |
| v1_stage2_strict | 86.09 | 58.81 |
| **v2_verbal** (V0 re-corrido, **sin cambios**) | **87.90** | **57.47** |

`v2_verbal` es la fila importante: **es V0 re-ejecutado sin modificar nada**, y dio 87.90
en vez de 90.88. **Tres puntos de puro ruido de muestreo**, más que la diferencia entre
varias variantes que se estaban comparando entre sí.

Ese resultado motivó bajar la temperatura a 0.0 y estableció la barra de significancia:
**ninguna diferencia menor a ~3 puntos en ese panel es señal.**

*(Salvedad: ese piso se midió en 3.5-flash. Aplicarlo a generación 2 es una extrapolación
razonable, no una medición. Una medición independiente aparece en §5.4.)*

### 5.2 El problema de trazabilidad, y cómo se resolvió

Los archivos históricos `batch_results_*.json` guardaban el **nombre** de la variante, no
el hash de su texto. Y el notebook redefine las mismas constantes en celdas distintas: un
solo nombre, `STAGE2_V6_CORRECTED`, corresponde a **tres textos diferentes** (3887, 3974 y
3835 caracteres). Las filas de generación 2 no se podían atar a un prompt concreto.

**Solución implementada.** Los prompts se extrajeron a `src/configs/prompts/*.txt` con
SHA-256 sobre el texto normalizado por espacios, registrados en `MANIFEST.json`. El
runner [`scripts/ablation/rerun_panel.py`](../scripts/ablation/rerun_panel.py):

- carga el prompt del archivo y **aborta si el hash no coincide** con el manifest;
- reutiliza el World Model cacheado, y lo genera solo si falta;
- guarda checkpoint **después de cada video**, así un corte por cuota no cuesta trabajo ya
  pagado;
- **se niega a publicar un panel incompleto**, para que un promedio parcial nunca se cite
  como resultado;
- registra en `run.json` el hash del prompt, modelo, commit, y la procedencia de Stage 1 y
  de la pizarra por video.

Resultado de la desambiguación: el `V6_corrected_v2` histórico **era la celda 9**
(producción) — re-correrla reprodujo su Service F1 casi exacto (89.79 vs 89.94). Y la
comparación histórica `V7_RETURN_FLOWS_V6` vs `V6_corrected_v2` **estaba confundida**:
V7_V6 se construye sobre el V6 de celda 10, que carece de la regla `Unidirectional
Default` — justamente sobre direccionalidad, que es lo que V7 modifica.

### 5.3 El panel ampliado

El panel original de 14 se amplió a **30**: los 14 más 16 videos muestreados al azar
(`seed=42`) del conjunto elegible, restringidos al mismo rango de complejidad del panel
original (GT de 6–13 nodos y 5–20 aristas) para no introducir un cambio de dificultad, y
excluyendo los que ya tenían caches de Stage 1 de otros experimentos.

**Los 16 nuevos nunca se usaron para elegir nada.** Son la partición limpia.

### 5.4 Condiciones de ejecución de la ablación

Todas las variantes de §6, sin excepción:

- `gemini-3.6-flash`, temperatura 0.0
- mismos 30 videos
- mismo World Model de Stage 1, cacheado (`STAGE1_V0_BASELINE`, hash verificado)
- mismo evaluador `evaluate_pair`
- una sola imagen de entrada (la pizarra limpia), salvo la variante de evidencia visual
- prompt verificado por SHA-256 antes de la primera llamada

**Medición independiente del ruido:** el mismo prompt de producción sobre los mismos 14
videos, en dos corridas separadas por días, dio **63.21 y 63.99** de Edge F1. Es una
medición directa de la variación corrida-a-corrida en generación 2, independiente del
`v2_verbal` de generación 1.

---

## 6. Los experimentos

### 6.1 Las once variantes sobre el panel de 30

| Variante | Celda | sha | Svc F1 | Edge F1 | Aristas | Ratio | %bidir |
|---|---|---|---:|---:|---:|---:|---:|
| V7_RETURN_FLOWS_V6 | 10 | `7ad8d9368bce` | 88.07 | **60.10** | 292 | 0.81 | 21.9 |
| V6_OPTIMIZED | 8 | `079b0aa855d7` | 86.75 | 59.14 | 269 | 0.75 | 13.5 |
| **V6_CORRECTED ← producción** | 9 | `ed1d85054d73` | 88.07 | 58.99 | 269 | 0.75 | 12.4 |
| V7_RETURN_FLOWS | 7 | `1ed4ebf91e68` | 86.91 | 58.65 | 305 | 0.84 | 17.2 |
| V5_STRICT_ROUTING | 8 | `a792c1328d02` | 86.78 | 58.45 | 261 | 0.72 | 10.5 |
| V8_ACTORS_AND_RETURNS | — | `277020bacda4` | 86.21 | 58.40 | 299 | 0.83 | 17.9 |
| V6_CORRECTED | 10 | `dbddf1f30bfb` | **88.47** | 58.10 | 284 | 0.79 | 12.0 |
| V5_STRICT_ROUTING | 7 | `53f8d9124406` | 86.65 | 58.08 | 281 | 0.78 | 14.3 |
| V6_CORRECTED | 7 | `7228956f5fc6` | 85.92 | 57.52 | 281 | 0.78 | 11.9 |
| V6_CORRECTED + evidencia visual | 9 | `ed1d85054d73` | 86.31 | 57.39 | 272 | 0.75 | 11.3 |
| V4_ANTI_HALLUCINATION | 8 | `cdb8998f48eb` | 85.62 | 57.10 | 260 | 0.72 | 11.0 |
| **GROUND TRUTH** | — | — | — | — | **361** | 1.00 | **46.7** |

**Las once caben en 3.00 puntos de Edge F1.**

### 6.2 El panel de 14 no generaliza

Para el prompt de producción:

| Muestra | n | Svc F1 | Edge F1 |
|---|---:|---:|---:|
| Panel original | 14 | 89.79 | 63.99 |
| **16 nuevos** | 16 | 86.56 | **54.60** |
| Combinado | 30 | 88.07 | 58.99 |

El número de 30 (88.07 / 58.99) queda mucho más cerca del promedio real sobre los 370
completos (86.78 / 59.65) que el optimista de 14.

**Y el ranking tampoco sobrevive.** De las 9 variantes con ambos paneles medidos:

| Variante | Celda | Edge@14 | Edge@30 | Δ |
|---|---|---:|---:|---:|
| V4_ANTI_HALLUCINATION | 8 | **65.60** *(1º)* | 57.10 *(9º)* | −8.50 |
| V5_STRICT_ROUTING | 7 | 64.51 *(2º)* | 58.08 *(7º)* | −6.43 |
| V5_STRICT_ROUTING | 8 | 64.11 *(3º–4º)* | 58.45 *(5º)* | −5.66 |
| V6_OPTIMIZED | 8 | 64.11 *(3º–4º)* | 59.14 *(2º)* | −4.97 |
| V7_RETURN_FLOWS | 7 | 63.89 *(5º–6º)* | 58.65 *(4º)* | −5.24 |
| V7_RETURN_FLOWS_V6 | 10 | 63.89 *(5º–6º)* | **60.10** *(1º)* | −3.79 |
| V6_CORRECTED ← producción | 9 | 63.21 *(7º)* | 58.99 *(3º)* | −4.22 |
| V6_CORRECTED | 7 | 61.64 *(8º)* | 57.52 *(8º)* | −4.12 |
| V6_CORRECTED | 10 | 60.48 *(9º)* | 58.10 *(6º)* | −2.38 |

- **Spearman ρ = −0.185** (rangos promediados; hay dos pares de empates exactos a 14). El
  orden del panel chico **no predice** el del grande.
- **r = −0.858** entre el Edge F1 a 14 y la variación al ampliar: **cuanto mejor puntuaba
  una variante en el panel chico, más perdió**. Es la firma cuantificada del sobreajuste a
  la muestra de selección.

### 6.3 Experimento: inyectar la topología visual en Stage 2

**Motivación.** El detector ya calcula la máscara de trazos entre íconos (§2.4) pero solo
la dibuja. Siendo que el Edge F1 es la métrica débil y todas las variantes *sub-generan*
aristas, parecía un canal de información calculado y desperdiciado.

**Implementación** ([`connection_evidence.py`](../scripts/ablation/connection_evidence.py)).
Los trazos se convierten en vínculos candidatos `ícono ↔ ícono` mediante transformada de
Hough probabilística, asociando cada extremo al ícono más cercano; `support` cuenta cuántos
segmentos respaldan cada vínculo. A Stage 2 se le pasa una **segunda imagen con badges
numerados** sobre cada ícono, más la lista de vínculos como texto.

Dos decisiones de diseño:

- **Badges, no coordenadas.** La convención espacial de Gemini es normalizada 0–1000 y la
  imagen se reescala internamente; los píxeles del original no son una referencia que el
  modelo pueda resolver de forma confiable. Con badges dibujados encima del ícono no hace
  falta ningún razonamiento espacial.
- **Sin las etiquetas `AWS_Icon_N [C:… W:…]`** que el detector estampa en su imagen de
  depuración. Esas etiquetas son lo que **destruye los nombres de servicio escritos a
  mano**, y duplican datos que ya van como texto. Los badges van en la esquina superior
  izquierda; los rótulos manuscritos están debajo de los íconos, así que quedan legibles.

**Resultado: sin efecto.**

| | Svc F1 | Edge F1 | Aristas | Ratio |
|---|---:|---:|---:|---:|
| V6 c9 (producción) | 88.07 | 58.99 | 269 | 0.75 |
| V6 c9 + evidencia | 86.31 | 57.39 | 272 | 0.75 |

Pareado: gana 4, pierde 7, **empata 19** → p = 0.549. Se inyectaron **244 vínculos**
(8.1 por video) y el modelo generó **3 aristas más en total**. Precisión y recall
prácticamente planas (69.6→68.8 y 53.8→52.2). **El modelo ignoró la evidencia.**

Eso descarta el riesgo que motivaba la cautela —que tomara los vínculos como permiso para
alucinar— y descarta también el beneficio.

### 6.4 Anatomía del error de aristas

Descomposición de las **178 aristas del GT que pierde producción** (de 361, un 49.3%):

| Causa | aristas | % |
|---|---:|---:|
| **Falta la arista de retorno** (puso `b→a` pero no `a→b`) | **80** | 45% |
| **Falta un nodo** — el 91% son actores `User*` o `ThirdParty` | 58 | 33% |
| Ambos nodos presentes, sin conexión en ningún sentido | 40 | 22% |

**Las dos causas principales son reglas que el prompt de producción dicta
explícitamente:**

1. `**Unidirectional Default:** Treat data and control flows as strictly unidirectional`
   → las 80 aristas de retorno.
2. `5. **Pruning:** Remove generic human actors or purely physical concepts` → los
   actores ausentes. **El prompt se contradice a sí mismo**: ofrece un vocabulario
   `User and Client Actors` en su encabezado y luego ordena eliminarlos. El GT tiene 34
   actores `User*`, el 13% de sus nodos.

Juntas explican **133 de 178 aristas perdidas (75%)**.

**El techo direccional.** Colapsando a pares no dirigidos, el Edge F1 de producción pasa
de 62.23 a 73.40: si la dirección fuera gratis se ganarían **+11.17 puntos**.

> *Advertencia metodológica:* una primera medición dio "+2.6 puntos" usando
> multiconjuntos, que **siguen penalizando** la arista de retorno ausente y por lo tanto
> no aíslan la dirección. El número correcto exige colapsar a un conjunto de pares no
> ordenados.

### 6.5 Experimento: V8, corregir las dos reglas culpables

Se construyó `STAGE2_V8_ACTORS_AND_RETURNS` (sha `277020bacda4`), idéntico a V6 celda 9
salvo tres bloques, verificado por diff:

1. La regla 5 pasa de podar actores a **mapearlos** contra la lista
   `User and Client Actors`. Se conservó a propósito la poda de conceptos físicos sin
   flujo *(incluidos los presentadores)*, porque en estos videos siempre hay dos personas
   frente a la pizarra.
2. Se elimina `Unidirectional Default`.
3. Se agrega el bloque de retornos de V7, **copiado textual** para que el efecto sea
   atribuible a una formulación ya probada y no a redacción nueva.

**Los mecanismos respondieron exactamente como se esperaba:**

| | Svc F1 | Edge F1 | Aristas | %bidir | Actores `User*` |
|---|---:|---:|---:|---:|---:|
| V6 c9 (producción) | 88.07 | 58.99 | 269 | 12.4 | 20 |
| **V8** | **86.21** | **58.40** | **299** | **17.9** | **29** |
| Ground truth | — | — | 361 | 46.7 | 34 |

**Y el Edge F1 no se movió** (p = 0.607). Peor: **degrada el Service F1 de forma
significativa** (pareado 1-8 con 21 empates, **p = 0.039**) — con 9 actores más, algunos
se mapean a la entrada equivocada. **V8 no debe ir a producción.**

**La lección:** el razonamiento era *"133 aristas se pierden por estas dos reglas,
arreglalas y las recuperás"*. **La contabilidad de errores no es un mapa de mejoras
disponibles.** El modelo ahora *puede* emitir retornos y actores, y los emite, pero no
acierta *cuáles*. Saber que falta una arista de retorno no es saber entre qué dos
servicios va.

### 6.6 Experimento: la evaluación permisiva

**Hipótesis.** Si la métrica estricta está dominada por ruido que las variantes no
controlan, quitarlo debería dejar ver las diferencias reales. Costo cero de API: el
`analysis` completo está guardado en cada `run.json`.

**Aporte aislado de cada relajación** (promedio de las 11, Edge F1):

| Métrica | Edge F1 | sobre estricto |
|---|---:|---:|
| Estricta | 58.36 | — |
| + solo actores | 62.00 | +3.65 |
| + solo no dirigido | 60.21 | +1.86 |
| + solo conjunto | 61.65 | +3.30 |
| **Permisiva sin la regla de conjuntos** | **63.88** | **+5.52** |
| Permisiva completa | 76.67 | +18.31 |

Dos observaciones:

- **La interacción es super-aditiva.** Las tres por separado suman +8.81; juntas dan
  +18.31. Achicar los conjuntos por tres vías simultáneas hace mucho más fácil emparejar.
  No es "estricto más tres perdones chicos".
- **La regla de conjuntos aporta +12.79 de los +18.31**, más que las otras dos juntas.

**Y el resultado principal: no discrimina mejor — discrimina peor.**

| | significativas (p<0.05) | empates promedio |
|---|---:|---:|
| Estricta | 3 de 55 | 14.9 / 30 |
| Permisiva | 2 de 55 | 20.4 / 30 |
| **Esperadas por azar** | **2.8 de 55** | — |

- El conteo de "significativas" es **exactamente el que predice el azar**. Con corrección
  de Bonferroni (α = 0.05/55 = 0.00091) **no sobrevive ninguna, en ninguna métrica**.
- **Cero pares son significativos en ambas.** `V6_OPTIMIZED vs V6_CORRECTED c7` da
  p=0.007 estricto y p=0.344 permisivo. Una diferencia real sobreviviría al cambio de
  métrica.
- Los **empates suben** de 14.9 a 20.4 de 30.

Aparece además un **tercer ordenamiento**: ρ = +0.618 entre el ranking estricto y el
permisivo.

---

## 7. Hallazgos

### 7.1 Ninguna diferencia entre variantes de prompt es significativa

| Intervención | Mecanismo | Resultado | p |
|---|---|---|---:|
| 11 variantes de prompt | reescrituras de reglas | indistinguibles | 0.118–1.000 |
| Few-shot RAG | 2 arquitecturas GT en contexto | nulo | — |
| Evidencia visual de conexiones | topología detectada por CV | nulo, el modelo la ignoró | 0.549 |
| V8, reglas dirigidas por error | actores + retornos | mecanismos sí, F1 no | 0.607 |
| V7_RETURN_FLOWS_V6 | retornos sobre base sin regla unidireccional | mejor de la tabla, no significativo | 0.581 |

Sostenido bajo **dos métricas independientes**, con corrección por comparaciones
múltiples, y con el conteo de falsos positivos coincidiendo con lo que predice el azar.

**El dato que lo explica:** entre 12 y 19 empates de 30 por comparación, y en **9 de 30
videos las cuatro variantes principales dan Edge F1 idéntico**. Los prompts se
diferencian mucho menos de lo que sugieren sus promedios.

### 7.2 Elegir prompt con una muestra chica produce un ranking que no existe

Tres ordenamientos distintos de las mismas once variantes según muestra (14 vs 30) y
métrica (estricta vs permisiva), ninguno estable. Y la caída al ampliar es proporcional a
lo bien que le había ido a cada variante en el panel chico (r = −0.858).

Es un aviso metodológico concreto sobre ablaciones de prompts con muestras pequeñas —
poco documentado y directamente publicable.

### 7.3 La regla de conjuntos infla el resultado sin justificación

Aporta dos tercios de la ganancia permisiva y es la única de las tres relajaciones sin
defensa metodológica: borra una capacidad que el prompt implementa a propósito
(*Dynamic Logical Fusion*) y que el GT codifica en el 13% de sus aristas.

Las otras dos sí se defienden: distinguir `UserConsumerWeb` de `UserConsumerMobile` a
menudo no es determinable visualmente, y la dirección de una flecha en pizarra es
genuinamente ambigua.

**Recomendación: reportar la permisiva sin la regla de conjuntos (63.88) como métrica
secundaria, y la completa (76.67) solo como cota superior declarada.**

### 7.4 El cuello de botella no está en el prompt de Stage 2

Cuatro intervenciones independientes, cada una mejor fundamentada que la anterior,
ninguna movió el Edge F1. **Conclusión defendible: el Edge F1 de ~59% no está limitado
por el prompt de Stage 2.**

Los candidatos que quedan: Stage 1 (la calidad del World Model), la ontología de
evaluación, o la ambigüedad inherente entre lo que se dibuja y lo que se narra.

### 7.5 La brecha de bidireccionalidad sigue abierta

El GT tiene **46.7%** de sus pares conectados en ambos sentidos; producción produce
**12.4%** y la mejor variante llega a **21.9%**. Es la diferencia estructural más grande
entre lo generado y la referencia, y **ninguna intervención la cerró**.

### 7.6 Reutilizar scores de producción para ampliar un panel es válido

El primer panel de 30 se armó de forma híbrida: 14 de la ablación más 16 tomados del CSV
de la corrida de 370 videos, sin pagar llamadas nuevas. Dio 87.23 / 59.10 contra
88.07 / 58.99 de la corrida limpia de punta a punta — **0.11 puntos de diferencia en Edge
F1**. Abarata cualquier ampliación futura.

---

## 8. Conclusión

El pipeline resuelve bien **qué servicios** hay (86.78% Service F1 sobre 336 videos
elegibles) y mal **cómo se conectan** (59.65% Edge F1), con un patrón claro: es
conservador — precisión 70.36 contra recall 53.99, dejando de emitir casi la mitad de las
aristas que existen.

El resultado metodológico más sólido de este trabajo es **negativo, y por eso mismo
valioso**: las variantes de prompt de Stage 2 son **estadísticamente indistinguibles**
entre sí, y el panel de 14 videos con el que se eligió el prompt de producción generaba
un ranking que no sobrevive ni a duplicar la muestra ni a cambiar de métrica. Cuatro
intervenciones cada vez mejor fundamentadas —incluida una dirigida por un análisis de
error que identificó 133 aristas perdidas una por una— fallaron en mover la aguja.

Ese conjunto de resultados sostiene una afirmación que sí se puede defender ante un
revisor: **el techo de ~59% en Edge F1 no lo impone el prompt de Stage 2.** Y sostiene un
aviso metodológico generalizable: en ablaciones de prompts sobre LLMs, una muestra de 14
ítems produce ordenamientos que son artefactos del ruido de esa muestra.

Nota sobre la decisión de producción: el prompt que quedó en producción (V6 celda 9)
**aguanta la ampliación mejor** que la variante que el panel de 14 señalaba como
ganadora. Pero eso fue **suerte, no fundamento** — con el número del panel de 14 la
elección "correcta" habría sido V4_ANTI_HALLUCINATION, que resultó la peor de las nueve
sobre datos nuevos.

---

## 9. Trabajo futuro

### 9.1 Bloqueante para el artículo

- **`V5_with_vision` no es reproducible.** El experimento de solo-visión (86.67 Service /
  53.87 Edge) sostiene el claim C01 sobre fusión audio-visual, pero sus cifras vienen solo
  de `Proyecto/Avances/Avance Semanal 3.md`, que **no está en el repositorio**, y a
  diferencia de los demás experimentos **no existe prompt ni script**. Hay que
  reconstruirlo: definir el prompt de Stage 2 sin transcripción, registrarlo con hash, y
  correrlo sobre el panel de 30 contra el baseline (88.07 / 58.99).
- Regenerar `evidence/table1` y `evidence/table2` del ARA desde los CSV — sus cifras
  actuales no aparecen en las fuentes que citan.

### 9.2 Donde buscar la mejora de Edge F1

Descartado el prompt de Stage 2, los candidatos por orden de expectativa:

1. **Calidad de Stage 1.** El World Model es la entrada dominante de Stage 2 y nunca se
   ablacionó a 30 videos. Existen 12 World Models **escritos a mano** en
   `lab_workspace/*/world_model_vision.json` que sirven como condición oráculo: *si Stage 1
   fuera perfecto, ¿cuánto mejora Stage 2?* Están validables con la herramienta de
   `reports/vision_validation/` pero **la revisión visual quedó pendiente**.
2. **La brecha de bidireccionalidad** (46.7% vs 12.4%), que es la mayor diferencia
   estructural y ninguna intervención de prompt tocó.
3. **Revisar la ontología de evaluación.** Que el 13% de las aristas del GT repita pares
   ya conectados sugiere que "arista" no significa lo mismo en el GT que en la salida del
   modelo.

### 9.3 Potencia estadística

Con 30 videos y ~15 empates por comparación, **una diferencia de 2 puntos de Edge F1 no es
detectable**. Cualquier comparación futura entre variantes necesita más videos, no más
variantes. Los 336 elegibles están disponibles y el costo de ampliar se abarató (§7.6).

### 9.4 Completar la tabla

Cuatro variantes quedaron sin medir a 30 (`V0_BASELINE` celdas 7 y 8,
`V4_ANTI_HALLUCINATION` celda 7, `V4_DYNAMIC_FEW_SHOT`) — las de menor Edge F1 en el panel
de 14. No bloquean ninguna conclusión; completan la tabla. Dos tienen checkpoint parcial.

### 9.5 Higiene del repositorio

El repositorio es público. Contiene 3 PDF con derechos de autor en `referencias/`
(presentes en el historial desde el commit inicial, así que borrarlos de la punta no los
elimina), los 396 `.graphml` de Cloudscape sin licencia, y 446 transcripciones de YouTube.
La opción más simple es repositorio privado con la profesora como colaboradora; la
alternativa es reescritura de historial con `git filter-repo` y force push.

---

## Anexo · Artefactos citables

| Qué | Dónde |
|---|---|
| Reporte HTML de la ablación | `reports/ablation_report.html` |
| Datos consolidados de la ablación | `reports/ablation_report_data.json` |
| Evaluación permisiva | `reports/permissive_panel.json` |
| Corridas individuales con procedencia | `reports/ablation/*/run.json` |
| Respaldo del panel de 14 | `reports/ablation_backup_2026-08-24_14v/` |
| Corrida de producción a escala | `reports/runs/2026-08-20_standard_v6corrected_370v/` |
| Auditoría por video (396 filas) | `reports/dataset_audit_2026-08-20.{md,csv}` |
| Prompts con SHA-256 (17) | `src/configs/prompts/MANIFEST.json` |
| Validación de World Models manuales | `reports/vision_validation/index.html` |
| Linaje y arquitectura del pipeline | `docs/standard-pipeline.md` |
| Auditoría del ARA | `ara/TODO_PARA_EL_ARTICULO.md` |

**Regenerar:**

```bash
.venv/bin/python scripts/ablation/build_report_data.py
.venv/bin/python scripts/ablation/build_report_html.py
.venv/bin/python scripts/ablation/evaluate_permissive_panel.py
```

**Correr una variante sobre el panel:**

```bash
.venv/bin/python scripts/ablation/rerun_panel.py --list
.venv/bin/python scripts/ablation/rerun_panel.py --prompt stage2_v6_corrected__cell9.txt --panel 30
```
