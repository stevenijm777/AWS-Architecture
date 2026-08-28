# Auditoría metodológica — lado Parsimonious

**Alcance:** `C:\Users\USUARIO\Downloads\AWS-Architecture-main\AWS-Architecture-main`
**Fecha:** 2026-08-27 · **Modo:** solo lectura (no se modificó ningún archivo del repo)
**Rutas:** relativas a la raíz del repo. Los números de línea corresponden al estado del árbol el 2026-08-27.

**Convención de marcas**

| Marca | Significado |
|---|---|
| `[VERIFICADO]` | Comprobado leyendo el archivo o recalculando desde los datos del repo. Reproducible. |
| `[SOSPECHA]` | Evidencia fuerte pero indirecta; falta un dato para cerrarlo. |
| `[NO PUDE VERIFICAR]` | No hay material en el repo para decidirlo, o el material está fuera de alcance. |

---

## 0. Resumen ejecutivo

Cinco cosas, en orden de gravedad:

1. **Las tres corridas de agosto son incrementales, no repeticiones.** Los 344 videos de la corrida del 19 aparecen con métricas **byte-idénticas** en las corridas del 20 y del 21. Cero llamadas nuevas a la API. No sirven como medición de ruido. `[VERIFICADO]` — §2.

2. **Pero sí existe una medición de ruido real dentro del proyecto, y nadie la usó.** Los Registros 24 y 26 del historial de prompts (30 videos, prompt v9, `gemini-3.6-flash`) fueron **re-corridos completos** en el Registro 36 con la misma configuración. Resultado: solo **60 % de los videos dan Service F1 idéntico** y **37 % dan Edge F1 idéntico**; la desviación de la diferencia pareada por video es **9.40 pts (Service)** y **11.89 pts (Edge)**; la media de Edge F1 se movió **−3.61 pts sin cambiar nada**. Temperatura 0.0 no es determinista de este lado tampoco. `[VERIFICADO]` — §3.3.

3. **El prompt de producción (v9) se eligió mirando UN video.** El Registro 17 —la adopción de v9— se decidió sobre `-3lnf5lzsH0`. Con el piso de ruido del punto 2, el efecto mínimo detectable con n=1 es **26.3 pts de Service F1** y **33.3 de Edge F1**. Y ese mismo video es la fila estrella de `ara/evidence/tables/table1` («Parsimonious +15.7 %»). Se eligió el prompt y se reportó su rendimiento sobre el mismo dato. `[VERIFICADO]` — §3.

4. **`ara/evidence/` tiene una tabla con cifras que su fuente no contiene y otra con la muestra recortada de forma que invierte la conclusión.** Table 2: cinco de seis cifras no aparecen en el HTML citado. Table 1: 16 filas elegidas de 60; en las 60 gana Standard 28-8, en las 16 elegidas gana Parsimonious 4-3. `[VERIFICADO]` — §1.1 y §1.2. *(Ya documentado en `ara/TODO_PARA_EL_ARTICULO.md` §1.1–1.2; las tablas siguen sin corregir.)*

5. **La comparación 85.5 % vs 86.7 % nunca se sometió a una prueba pareada.** No hay un solo `ttest`, `wilcoxon` ni `scipy` en todo el repo. Hecha la prueba (§5.1): sobre 321 videos usables pareados, **Standard gana por 1.05 pts de Service F1 (p = 0.023)** y **2.64 pts de Edge F1 (p = 0.0007)**. La diferencia es pequeña pero detectable — y es **menor que el piso de ruido a cualquier tamaño de panel que el proyecto usó para decidir** (n=1 a n=30). `[VERIFICADO]` — §5.1.

Existe además una auditoría previa de este mismo lado: `docs/revision_parsimonious_2026-08-19.md`. Buena parte de sus hallazgos **sí se corrigieron** (§7.3). Este informe se centra en lo que quedó.

---

## Bloque 1 — ¿Están respaldados los números?

### 1.1 `ara/evidence/tables/table2_strict_vs_permissive.md` — cifras que la fuente no contiene `[VERIFICADO]`

La tabla (`ara/evidence/tables/table2_strict_vs_permissive.md:3`) cita como fuente
`evaluacion_estricta_vs_permisiva.html`. Búsqueda literal de cada cifra en ese HTML (233 168 bytes):

| Cifra de Table 2 | Apariciones en el HTML citado |
|---|---:|
| 78.4 % (Service Precision estricta) | **0** |
| 91.2 % (Service Precision permisiva) | **0** |
| 72.1 % (Service Recall estricta) | **0** |
| 85.6 % (Service Recall permisiva) | **0** |
| 48.2 % (Edge F1 estricta) | **0** |
| 59.7 % (Edge F1 permisiva) | **0** |

Ninguna de las seis está en el archivo citado. Recalculando el lado permisivo desde el
único CSV permisivo del repo (`whiteboard_selection_lab/permissive_batch_evaluation.csv`, 14 filas):

| Métrica permisiva | Table 2 dice | Valor real del CSV |
|---|---:|---:|
| Service Precision | 91.2 % | **91.17 %** ✔ |
| Service Recall | 85.6 % | **97.38 %** ✘ (+11.8) |
| Edge F1 | 59.7 % | **76.28 %** ✘ (−16.6) |

Una de tres coincide. Y **59.7 es exactamente el Edge F1 estricto de Standard**
(`reports/runs/2026-08-20_standard_v6corrected_370v/run.json` → `edge_f1.mean = 59.65`, n=321):
una cifra de otra corrida, de otro pipeline y de otro protocolo, colocada en la celda
«Edge F1 permisiva». `[SOSPECHA]` sobre el mecanismo (mezcla accidental de tablas);
`[VERIFICADO]` sobre el hecho de que la cifra no proviene de la fuente citada.

La tabla además describe mal el mecanismo: dice «alias dictionary mapping
(`lambda_function → Lambda`)». El evaluador permisivo real (`whiteboard_selection_lab/evaluacion_permisiva.py`)
agrupa por superclases ontológicas de actores, no por alias de servicios.

### 1.2 `ara/evidence/tables/table1_parsimonious_vs_standard.md` — muestra recortada `[VERIFICADO]`

Fuente citada: `reporte_comparacion_detallada.md`. Ese archivo tiene **60 filas**.
La tabla del ARA publica **16**.

| Conjunto | Media Pars | Media Std | Gana Pars | Gana Std | Empata |
|---|---:|---:|---:|---:|---:|
| Las 60 filas de la fuente | 82.37 % | 87.94 % | 8 | **28** | 24 |
| Las 16 filas publicadas | **89.73 %** | 88.83 % | **4** | 3 | 9 |

El recorte invierte el signo del resultado. En la población, Standard gana 28 a 8;
en la selección publicada, Parsimonious gana 4 a 3.

**Peor:** 4 de las 16 filas ya no coinciden con el corpus actual, y **las cuatro
discrepan a favor de Parsimonious**:

| Video | Table 1 (Pars) | `results.csv` 2026-08-21 | Diferencia |
|---|---:|---:|---:|
| `-kA0ahrhX3I` | 100.0 % | **71.43 %** | −28.6 |
| `6EUknQqaV1w` | 100.0 % | **92.31 %** | −7.7 |
| `AzM_d7ZvzUE` | 100.0 % | **87.50 %** | −12.5 |
| `BlCXEMp_lqY` | 100.0 % | **83.33 %** | −16.7 |

Dos de esas cuatro (`-kA0ahrhX3I`, `6EUknQqaV1w`) son precisamente filas marcadas como
«**Parsimonious +7.7 %**» en la tabla. Con los datos de hoy, las mismas 16 filas dan
**Pars 85.64 % vs Std 88.83 %**, con Parsimonious ganando 2 y perdiendo 6.

Que las cuatro desviaciones apunten en la misma dirección es lo que hay que explicarle a un
jurado. No encontré evidencia de manipulación deliberada — el patrón es compatible con una
tabla congelada de una generación anterior del corpus — pero el efecto neto sobre el lector es
el mismo. `[VERIFICADO]` los números; `[NO PUDE VERIFICAR]` la intención.

En 27 de las 60 filas de `reporte_comparacion_detallada.md` al menos una de las dos columnas
difiere del `results.csv` actual. Ese archivo describe un corpus que ya no existe.

### 1.3 `ara/logic/claims.md` `[VERIFICADO]`

- **C03** declara «Tested on Gemini Vision API (**temperature 0.1**)».
  El código fija **0.0** (`scripts/core/vision_analyzer_parsimonious.py:223`,
  `config={"response_mime_type": "application/json", "temperature": 0.0}`).
  Ninguna corrida del repo usó 0.1 según el código presente.
- **C03** afirma que el prompt parsimonioso «elimina nodos actor fantasma» y cita
  `handoff_notes.md:75` («UserCompanyDeveloper alucinado 15 veces»). Ese es el **conteo del
  problema**, no evidencia de su eliminación. Y el prompt de producción **ordena
  explícitamente** generar ese nodo:
  `vision_analyzer_parsimonious.py:94` → *"Default generic internal staff to
  'UserCompanyDeveloper'"*. El claim contradice su propia implementación.
- **C01** (fusión audio-visual reduce omisiones) está en estado *Validated* y su prueba es
  Table 1, que compara prompting (Parsimonious vs Standard), **no** fusión vs solo-visión.
  No existe en el repo ninguna ablación que quite el transcript. El criterio de falsación
  declarado («si solo-visión da Recall igual o mayor») nunca se ejecutó.
- **C02** cita `scripts/pizarra_occlusion_filter.py`. Ese archivo **no existe**; está en
  `scripts/utils/pizarra_occlusion_filter.py`.
- Todos los enlaces del ARA son `file:///home/stemjara/Projects/AWS-Architecture/...`,
  una ruta de otra máquina. El artefacto no es portable.

`ara/logic/experiments.md` tiene el mismo problema estructural: E01 describe una ablación de
**4 estrategias de selección de frame** y cita como evidencia Table 1, que no contiene ninguna
comparación de selección de frames. E02 dice «Evaluated across **62+** benchmark videos»; la
fuente tiene 60 filas y las corridas a escala tienen 385. `[VERIFICADO]`

### 1.4 `whiteboard_selection_lab/parsimonious_prompt_history.md`

606 KB, 42 secciones `[Registro N]`. Numeración rota: **Registro 22 no existe**, y los
números **9, 23 y 38 aparecen dos veces** con contenidos distintos. No hay forma estable de
citar «Registro 9» en un artículo. `[VERIFICADO]`

Las cifras del historial sí son internamente consistentes con lo que el propio documento
reporta; el problema no es que estén inventadas sino **sobre cuántos videos se midieron** (§3).

### 1.5 `prompt_ablation_detailed_report_parsimonious.html` — mezcla cuatro modelos `[VERIFICADO]`

Título: *«Reporte Detallado de Ablación Parsimoniosa (250 Videos Únicos) … evaluados con
Prompt v9 Parsimonioso»*. Etiqueta de modelo por video, contando las 250 tablas:

| Modelo etiquetado en la tabla del propio reporte | Videos |
|---|---:|
| `gemini-3.6-flash` | 145 (58 %) |
| `gemini-2.5-flash` | **79** |
| `gemini-3.5-flash` | **19** |
| `gemini-3.7-flash` | **7** |

Es decir: un reporte que se presenta como «Prompt v9 de producción» promedia cuatro
generaciones de modelo. Y no es una ablación: hay **un solo prompt**. El nombre del archivo
promete algo que el contenido no tiene.

Cruzando `Número de Nodos` / `Número de Aristas` de la cuarta columna («Nueva Prueba») contra
`gen_nodes` / `gen_edges` de `reports/runs/2026-08-21_parsimonious_v9/results.csv`:

| Modelo del reporte | Coinciden exacto con el corpus evaluado | No coinciden |
|---|---:|---:|
| `gemini-3.6-flash` | **145 / 145 (100 %)** | 0 |
| `gemini-2.5-flash` | **41 / 79** | 38 |
| `gemini-3.5-flash` | **11 / 19** | 8 |
| `gemini-3.7-flash` | **1 / 7** | 6 |

Al menos **53 grafos del corpus evaluado** tienen conteos idénticos a corridas etiquetadas con
un modelo distinto de `gemini-3.6-flash`, mientras el `run.json` declara ese modelo para los 385.
`[SOSPECHA]` fuerte — la coincidencia de dos enteros no es prueba individual, pero 53 de 53
en los que no hubo re-corrida posterior es un patrón, no una casualidad. Se cierra
definitivamente ejecutando §6.17-A.

### 1.6 `reports/MANIFEST.md` está desincronizado de los `run.json` que dice generar `[VERIFICADO]`

El encabezado dice: *«Every row is generated from a run's `run.json` … Do not edit by hand»*.
`build_manifest.py:57-60` lee `metrics.service_f1.mean`. Contraste de la fila
`2026-08-20_parsimonious_v9`:

| Campo | MANIFEST.md | `run.json` en disco hoy |
|---|---:|---:|
| Service F1 | 85.12 % | **85.73 %** |
| Edge F1 | 55.31 % (n=349) | **57.01 %** (n=321) |
| Excluidos de aristas | 21 (lista de 21 ids) | **0** (lista vacía) |
| Commit | `edf995f` | **`171d123`** |

Los tres valores del MANIFEST son irrecuperables desde el `run.json` actual (85.12 sí existe
allí, pero como `service_f1_legacy_including_unusable`). **El `run.json` de ese directorio fue
sobrescrito después de construirse el manifiesto, con otro commit y otras métricas.**

Causa raíz: `evaluate_parsimonious.py:182` nombra el directorio de corrida solo por fecha —
`reports/runs/{today}_parsimonious_v9` — sin label, sin hash, sin contador. **Dos evaluaciones
el mismo día se pisan en silencio.** Los directorios de corrida no son inmutables, así que no
constituyen registro de auditoría.

Además: la corrida `2026-08-21` (la que produce el 85.53 % que se reporta) **no está en el
MANIFEST**, y 3 de las 4 filas enlazan a `report.html` que no existe en esos directorios.

### 1.7 Pregunta 2 — ¿alcanzan los `run.json` para reproducir la corrida? **No.** `[VERIFICADO]`

Lo que sí registran (`reports/runs/2026-08-2*_parsimonious_v9/run.json`):

| Campo | Registrado | Comentario |
|---|---|---|
| `prompt_v9_sha256` | ✔ `a8f779627aba…` | **Verifiqué que coincide** con el SHA-256 de `CLOUDSCAPE_PROMPT_TEMPLATE` en `vision_analyzer_parsimonious.py`. Punto fuerte real. |
| `gemini_model` | ✖ literal | `evaluate_parsimonious.py:204` escribe la cadena `"gemini-3.6-flash"` **hardcodeada**. No lee `GEMINI_MODEL` ni la respuesta de la API. No es evidencia de nada. (`evaluate_standard.py:241` sí lee `GEMINI_MODEL` de config.) |
| `git_commit` | ⚠ | Es el commit **del momento de la evaluación**, no del momento de la generación de los grafos. Los grafos son meses anteriores. |
| `temperature` | **ausente** | El `run.json` de Standard la documenta en el campo `pipeline`; el de Parsimonious no la menciona. Está en el código (0.0) pero no en el artefacto. |
| Fecha/hora de generación de cada grafo | **ausente** | |
| Versión del SDK / de la API | **ausente** | |
| `response_schema` usado | **ausente** | y difiere según el script que generó el grafo (§7.2) |

**El fallo de fondo del hash.** `evaluate_parsimonious.py:48-53` hashea
`CLOUDSCAPE_PROMPT_TEMPLATE` — la plantilla **con los placeholders sin sustituir** (4 481
caracteres). El prompt que realmente viaja a la API tiene los catálogos inyectados y mide
**6 510 caracteres**. Y esa sustitución **no es única**: hay dos reglas distintas de partición
del catálogo en el repo, que producen dos prompts distintos con **el mismo hash registrado**:

| Regla de partición | Dónde | # actores | SHA-256 del prompt REAL |
|---|---|---:|---|
| `capability=="user" or name.startswith("User")` | `vision_analyzer_parsimonious.py:70` | 28 | `d7f26656a595c9bb…` |
| `is_aws == False` | `run_batch_gemini_36_multikey.py:36`, notebook celda 6 | **34** | `eb6eccfe8804d4a6…` |

Los 6 actores extra en la segunda regla son `CouchBase`, `MongoDBAtlas`, `OnPremDC`, `SAP`,
`ServiceNow`, `ThirdParty`. Es decir: **el script que realmente generó el corpus le dice al
modelo que puede usar `ThirdParty` como actor; el módulo de producción no.** Ambos casos
registran `a8f779627aba…`.

**Conclusión:** el hash identifica la plantilla, no el prompt. Es un avance real sobre el lado
Standard (que guardaba solo el nombre), pero no cierra la trazabilidad.

**Contradicción interna del propio prompt** `[VERIFICADO]`: la regla 2
(`vision_analyzer_parsimonious.py:95`) ordena mapear tecnologías externas a `` `ThirdParty` ``,
mientras la misma regla exige elegir actores **EXCLUSIVAMENTE** de
`<USER_ACTORS_PLACEHOLDER>`. Bajo la regla de partición del módulo, `ThirdParty` cae en la
lista de servicios AWS, **no** en la de actores. El prompt le pide al modelo una etiqueta que
él mismo excluyó de la lista permitida.

### 1.8 Pregunta 3 — los grafos de `data/graphs_parsimonious/` `[VERIFICADO]`

**Inventario:** 422 archivos = **421 `.graphml`** + `PROVENANCE.md`.
De los 421: **385 evaluados** (tienen GT) + **36 huérfanos** sin ground truth
(`run.json` → `skipped_no_gt`, 36 ids). `evaluate_parsimonious.py:84-86` los descarta con
`continue`; sí quedan registrados en `run.json`. Correcto.

**El agujero de procedencia.** `reports/parsimonious_provenance.csv` cubre **335** videos
(los que tienen caché `data/raw/*_vision_analysis_parsimonious.json`).

| | n |
|---|---:|
| Videos evaluados (2026-08-21) | 385 |
| …con fila en `parsimonious_provenance.csv` | 299 |
| …**sin caché de análisis de ningún tipo** | **86 (22 %)** |
| Filas de procedencia que no se evalúan | 36 |

`data/raw/*` está en `.gitignore` **salvo** `*.json` (`.gitignore:15-16`), así que las cachés
sí se versionan: **esos 86 no están ignorados, faltan.** Sus `.graphml` no se pueden regenerar
ni atribuir a un prompt, un modelo ni una fecha.

**Y de los que sí tienen caché, solo una minoría registra procedencia.** Descargué y leí las
55 cachés de esquema B:

| Esquema de caché | n | Registra `model` | Registra `prompt_version` |
|---|---:|---|---|
| B (`extracted_graph`) | 55 | ✔ (51 leídos: **todos** `gemini-3.6-flash`) | ✔ (todos `v9`) |
| A (`step_by_step_reasoning`/`graph`/`nodes`/`edges`) | 280 | **✖** | **✖** |

**51 de 385 videos (13 %) tienen procedencia de modelo y prompt verificable en el artefacto.**
El 87 % restante no.

**El veredicto de procedencia es, además, un artefacto del entorno donde corrió el auditor.**
`audit_parsimonious_provenance.py:131-138` confirma «v9_confirmado» por dos vías: esquema B con
`prompt_version=="v9"`, **o** esquema A cuyo JSON sea igual al de
`whiteboard_selection_lab/lab_workspace/<vid>/test_analysis.json`. El CSV publicado reporta
`lab_json_exists = 0` y `lab_json_matches = 0` **para los 335**. Pero:

- `whiteboard_selection_lab/lab_workspace/*` está en `.gitignore` (última línea), así que en
  cualquier checkout limpio esa rama **nunca puede dispararse**;
- en esta copia de trabajo el archivo **sí existe**: comprobé
  `lab_workspace/-3lnf5lzsH0/test_analysis.json` contra
  `data/raw/-3lnf5lzsH0_vision_analysis_parsimonious.json` con el criterio literal del auditor
  (`json.load(f1) == json.load(f2)`) → **`True`**.

Es decir: los 280 «v9_probable» no son un hallazgo sobre los datos; son el resultado de correr
el auditor donde faltaba una carpeta ignorada por git. El veredicto no es reproducible.

**Regenerados fuera del batch.** `data/graphs_parsimonious/-3lnf5lzsH0.graphml` (6 721 B,
md5 `365f340a…`) **no** es el archivo que produjo el generador
(`lab_workspace/-3lnf5lzsH0/test_graph.graphml`, 6 519 B, md5 `e9e65c5f…`), aunque ambos
derivan del mismo JSON y tienen los mismos 12 nodos y 12 aristas. El corpus evaluado es una
**re-derivación** del JSON, no la salida directa del pipeline. Las métricas no cambian, pero
la cadena de custodia sí.

**Mtimes:** los `.graphml` se agrupan en cuatro momentos (2026-07-10, 2026-07-20, 2026-08-21,
2026-08-27). Que haya varios grupos indica que es una copia de trabajo real y no una extracción
de ZIP, pero **no uso los mtimes como evidencia de generación** — solo de la última escritura.
`[SOSPECHA]`

---

## Bloque 2 — Las tres corridas de agosto

### 2.1 Son incrementales. Categóricamente. `[VERIFICADO]`

**Por los datos.** Comparación fila a fila de las tres `results.csv` sobre las 8 columnas de
métrica (`gen_nodes`, `gen_edges`, `svc_precision`, `svc_recall`, `svc_f1`, `edge_precision`,
`edge_recall`, `edge_f1`):

| Par de corridas | Videos en común | Filas **byte-idénticas** | sd de la diferencia pareada |
|---|---:|---:|---:|
| 19 ago (344) → 20 ago (370) | 344 | **344 / 344 (100 %)** | **0.0000** |
| 20 ago (370) → 21 ago (385) | 344 | **344 / 344 (100 %)** | **0.0000** |
| 19 ago → 21 ago | 344 | **344 / 344 (100 %)** | **0.0000** |

Anidamiento perfecto: `set(19) ⊂ set(20) ⊂ set(21)`; 0 videos exclusivos de la corrida
anterior en cada paso, +26 y +15 videos nuevos respectivamente.

**Por el código.** Tres mecanismos independientes lo confirman:

1. `scripts/evaluation/evaluate_parsimonious.py` **no llama a la API en absoluto**. Lee
   `.graphml` de disco (`:68 all_gen_files = sorted(graphs_dir.glob("*.graphml"))`) y aplica
   `evaluate_pair`. Una «corrida» aquí es una **evaluación**, no una generación.
2. `scripts/batch_process_parsimonious_v10.py:79` y `:91` — `if not out_graph.exists() or force`.
   `:113-118` — salta si el checkpoint dice `success` y el archivo existe.
3. `run_batch_gemini_36_multikey.py:106` —
   `if (lab_ws/"test_graph.graphml").exists() or json_cache.exists(): continue`.

Los tres saltan lo ya hecho. Nada re-llama a la API salvo con `--force`, y no hay registro de
que se haya usado.

### 2.2 Por qué NO sirve como medición de ruido — y qué se está midiendo en realidad

Las tres corridas **no** son tres muestras del mismo proceso estocástico. Son **tres
evaluaciones de un corpus creciente**, con métricas idénticas en la parte compartida. La
varianza observada entre ellas es exactamente cero por construcción. Usarlas como piso de
ruido daría «temperatura 0.0 es perfectamente determinista», que es **falso** (§3.3).

Peor: el movimiento aparente entre corridas **no es del modelo, es del evaluador y de la
muestra**. La corrida del 19 usó una versión anterior del evaluador, sin el filtro
`graph_usable`:

| | 19 ago | 20 ago | 21 ago |
|---|---|---|---|
| Clave `counts.excluded_unusable` | **ausente** | 49 | 49 |
| `exclusions.gt_has_zero_edges` | **17 ids** | vacío | vacío |
| `metrics.service_f1_legacy_including_unusable` | **ausente** | 85.12 | 84.97 |
| Service F1 publicado | 85.41 | 85.73 | 85.53 |

Los 17 videos de cero aristas del 19 están **contenidos** en los 49 `gt_marked_unusable` del 20
(verificado: `z ⊆ u`, diferencia vacía). Al introducirse el filtro, esos 17 dejan de aparecer
en la rama de cero-aristas porque la rama de inservibles los captura primero
(`evaluate_parsimonious.py:104-110`).

**Recalculé la corrida del 19 con el criterio del 21**, usando el mismo corpus de 344 videos:

| Corrida 19 ago | Publicado | Recalculado con el filtro actual |
|---|---:|---:|
| Service F1 | 85.41 % (n=344) | **85.58 %** (n=302) |
| Edge F1 | 55.37 % (n=327) | **56.83 %** (n=302) |

Es decir: de los +0.32 pts de Service F1 «ganados» entre el 19 y el 21, **+0.17 son cambio de
evaluador** y el resto es cambio de muestra. **Cero es cambio de modelo.** Las tres corridas
no son comparables entre sí ni siquiera como serie incremental.

### 2.3 Respuesta directa a las preguntas 4, 5 y 6

- **P4 — ¿independientes o incrementales?** **Incrementales.** Verificado por código y por
  identidad byte a byte de las 344 filas compartidas.
- **P5 — no aplica.** No hubo re-llamada a la API.
- **P6 — por qué no se puede usar como medición de ruido:** porque la diferencia verdadera no
  es cero *por construcción del experimento*, es cero *por construcción del artefacto* — se
  copió el mismo número. Un estudio test-retest exige que cada corrida vuelva a consultar el
  modelo. Aquí las tres leen el mismo `.graphml`. Cualquier conclusión sobre determinismo
  extraída de estas tres corridas sería circular.

**La medición de ruido que sí existe está en §3.3.** No hay que gastar una sola llamada a la
API para obtenerla.

---

## Bloque 3 — Cómo se eligieron los prompts

### 3.1 Pregunta 7 — tamaño de muestra por variante `[VERIFICADO]`

Extraje el video (o lista de videos) declarado en cada uno de los 18 primeros Registros — que
son los que contienen la evolución v1 → v9:

| Registro | Fecha | n videos | Prompt / cambio | Video(s) |
|---:|---|---:|---|---|
| 1 | 07-23 | **1** | prompt inicial | `-3lnf5lzsH0` |
| 2 | 07-23 | **1** | reglas + parsimonia | `-3lnf5lzsH0` |
| 3 | 07-24 | **1** | deduplicación estricta | `-3lnf5lzsH0` |
| 4 | 07-24 | **1** | anti-alucinación terceros | `-kA0ahrhX3I` |
| 5 | 07-26 | **1** | visual-first, actores simples | `-kA0ahrhX3I` |
| 6 | 07-26 | **7** | lote visual-first | 7 videos |
| 7 | 07-27 | **1** | estrictamente parsimonioso | `2e3vOxsHekE` |
| 8 | 07-31 | **1** | cambio de modelo a 3.6 | `2e3vOxsHekE` |
| 9a | 07-31 | **1** | ontología de actores | `2e3vOxsHekE` |
| 9b | 07-31 | **1** | carga dinámica pandas | `2e3vOxsHekE` |
| 10 | 07-31 | **1** | fallback de ruta CSV | `2e3vOxsHekE` |
| 11 | 07-31 | **5** | corrida «en vivo» | 5 videos |
| 12 | 07-31 | **1** | **prompt v6** | `6EUknQqaV1w` |
| 13 | 07-31 | **1** | v6 en otro video | `ww5fiygF6eg` |
| 14 | 07-31 | **1** | **prompt v7** | `ww5fiygF6eg` |
| 15 | 07-31 | **1** | v7 | `-3lnf5lzsH0` |
| 16 | 07-31 | **1** | **prompt v8** | `-3lnf5lzsH0` |
| 17 | 07-31 | **1** | **prompt v9 ← el de producción** | `-3lnf5lzsH0` |
| 18 | 07-31 | **1** | v9 en 3.5-flash | `ww5fiygF6eg` |

**16 de 18 registros son n = 1.** Los saltos de versión v6, v7, v8 y v9 se decidieron cada uno
sobre **un solo video**.

Las cifras reportadas en esa trayectoria:

| Registro | Video | Service F1 | Edge F1 |
|---:|---|---:|---:|
| 14 (v6→v7) | `ww5fiygF6eg` | 85.7 % | 35.7 % |
| 13 (v6) | `ww5fiygF6eg` | 85.7 % | 35.7 % |
| 15 (v7) | `-3lnf5lzsH0` | 70.0 % | 24.0 % |
| 16 (v8) | `-3lnf5lzsH0` | 70.0 % | 24.0 % |
| **17 (v9)** | `-3lnf5lzsH0` | **95.7 %** | **64.3 %** |

v6 → v7 dio literalmente los mismos dos números: cero evidencia. v7 → v8 idem.
El salto que justificó v9 fue **+25.7 pts de Service F1 y +40.3 de Edge F1 sobre un video.**

### 3.2 ¿Qué tan grande tendría que ser la diferencia para ser detectable con n=1?

Usando el piso de ruido medido **dentro de este mismo proyecto** (§3.3: sd de la diferencia
pareada por video = 9.40 pts Service, 11.89 pts Edge) y la aproximación estándar
MDE ≈ 2.8·sd/√n (80 % de potencia, α = 0.05 bilateral):

| n | MDE Service F1 | MDE Edge F1 |
|---:|---:|---:|
| **1** | **26.3 pts** | **33.3 pts** |
| 5 | 11.8 | 14.9 |
| 7 | 9.9 | 12.6 |
| 14 | 7.0 | 8.9 |
| 30 | 4.8 | 6.1 |
| 321 | 1.47 | 1.86 |

**Lectura.** Con n = 1, ninguna diferencia menor a ~26 pts de Service F1 es señal. Ni el salto
v6→v7 (0.0), ni v7→v8 (0.0), ni ninguno de los cambios de los Registros 1-16 llega. El único
que roza el umbral es v9 en el Registro 17: +25.7 Service (justo por debajo de 26.3) y +40.3
Edge (por encima de 33.3). Es decir: **de toda la trayectoria de nueve versiones de prompt,
como mucho una está por encima del ruido, y por un margen que una sola observación no puede
sostener.** El resto de las decisiones se tomaron dentro del ruido.

Hay además una observación de ruido incrustada en el propio historial: **Registros 9a y 9b**,
mismo video (`2e3vOxsHekE`), mismo modelo (3.6-flash), prompts que difieren solo en el
mecanismo de carga del catálogo (ontología vs pandas) — Service F1 idéntico 83.3 %, pero
**Edge F1 72.7 % vs 60.0 %: 12.7 pts de swing sin cambio sustantivo de prompt.** `[VERIFICADO]`

### 3.3 Pregunta 9 — sí hay una repetición, y es buena `[VERIFICADO]`

**Registro 24** (20 videos, 2026-08-06) y **Registro 26** (10 videos, 2026-08-07) usaron
`Prompt v9` + `Gemini 3.6`. **Registro 36** (2026-08-18) es explícitamente la
*«Re-evaluación del Lote de 30 Videos de los Registros 24 & 26 con Prompt v9 Parsimonioso en
gemini-3.6-flash»*. Mismo prompt, mismo modelo, mismos 30 videos, mismas imágenes y
transcripts. **La diferencia verdadera es cero por construcción.**

Extraje las 30 parejas de la columna «Nueva Prueba» de ambos bloques:

| | Service F1 | Edge F1 |
|---|---:|---:|
| Media primera corrida (Reg 24 & 26) | 84.50 % | 52.54 % |
| Media re-corrida (Reg 36) | 84.67 % | **48.93 %** |
| **Diferencia de medias** | +0.18 | **−3.61** |
| **sd de la diferencia pareada** | **9.40** | **11.89** |
| **Salidas idénticas** | **18/30 (60 %)** | **11/30 (37 %)** |
| Máximo \|diferencia\| en un video | **28.6 pts** | **32.3 pts** |
| Conteo de nodos idéntico | 24/30 | — |
| Conteo de aristas idéntico | — | 13/30 |

**Conclusiones:**

1. **Temperatura 0.0 no es determinista.** 40 % de los videos cambiaron su Service F1 y 63 %
   su Edge F1 sin que cambiara nada del input. Coincide con el hallazgo del lado Standard
   (0 de 170 salidas byte-idénticas) pero medido de forma independiente, con los datos de este
   lado del proyecto.
2. **El piso de ruido de este lado es 9.40 / 11.89 pts** de sd pareada por video.
3. **La media de Edge F1 se movió −3.61 pts sin ninguna intervención.** Eso es más que la
   diferencia total entre Parsimonious y Standard (−2.64 pts, §5.1). Un panel de 30 videos no
   distingue esas dos cosas.
4. Este experimento **ya está pagado**. Las llamadas se hicieron. Nadie lo interpretó como
   medición de ruido — el Registro 36 se presenta como una «re-evaluación» rutinaria.

### 3.4 Pregunta 8 — sobreajuste de selección `[VERIFICADO]`

Sí, y es demostrable con números exactos:

- El prompt de producción **v9** se adoptó en el Registro 17 mirando **`-3lnf5lzsH0`**,
  donde dio **95.7 % / 64.3 %**.
- Ese mismo video es la **fila estrella de `ara/evidence/tables/table1`**: *«MakeMyTrip …
  **95.7 %** vs 80.0 % — **Parsimonious +15.7 %**»*.
- Y en `reports/runs/2026-08-21_parsimonious_v9/results.csv` ese video sigue marcando
  **95.65 / 64.29** — los mismos valores.

El video usado para elegir el prompt es el video exhibido como prueba de que el prompt
funciona. Es el mismo error del lado Standard (panel de 14 usado para elegir y para reportar),
agravado: **aquí el panel de selección es de tamaño 1.**

Segundo canal de sobreajuste: el notebook `prompt_batch_ablation_lab_parsimonious.ipynb`
(celda 4) fija `TARGET_VIDEOS` = **5 videos** — los mismos 5 del Registro 11 — y esos 5 son
también filas de la Table 1. `[VERIFICADO]`

### 3.5 El notebook de ablación no contiene una ablación, y su «v9» no es el v9 `[VERIFICADO]`

`whiteboard_selection_lab/prompt_batch_ablation_lab_parsimonious.ipynb`, 11 celdas:

- **Un solo prompt.** `EXPERIMENT_LABEL = "Prompt_v9_Parsimonious"` (celda 4). No hay
  variantes que comparar. No es una ablación.
- **Cero salidas guardadas.** Las 11 celdas tienen `execution_count: None` y `outputs: []`.
  No queda registro de qué produjo.
- **Guarda el nombre, no el hash** — exactamente el error nº 3 del lado Standard, replicado.
- **El prompt del notebook NO es el de producción.** Celda 6 define su propia copia
  `PROMPT_V9_TEXT`:

  | | Longitud | SHA-256 |
  |---|---:|---|
  | `vision_analyzer_parsimonious.py::CLOUDSCAPE_PROMPT_TEMPLATE` | 4 481 | `a8f779627aba…` |
  | Notebook `PROMPT_V9_TEXT` | **4 475** | **`deebeebfdec7…`** |

  Difieren: el notebook usa `<ACTORS_PLACEHOLDER>` donde el módulo usa
  `<USER_ACTORS_PLACEHOLDER>`. Todo resultado del notebook etiquetado «v9» proviene de un
  texto distinto del v9 que el `run.json` certifica.
- **Usa `response_schema` Pydantic** (celda 8, `FinalArchitectureSchema`), que el módulo de
  producción **no** usa. El laboratorio y la producción no ejercitan el mismo camino.
- **Cuarto orden de preferencia del catálogo**: celda 6 prueba `graph_renderer/services.csv`
  primero. El módulo prueba `data/cloudscape_gt/services.csv`; el auditor de procedencia,
  `data/services.csv`. Tres órdenes distintos en tres archivos.

---

## Bloque 4 — El evaluador

### 4.1 Pregunta 10 — ¿miden lo mismo? Sí en el núcleo. `[VERIFICADO]`

`evaluate_parsimonious.py:34` y `evaluate_standard.py:42` **importan la misma función**
`evaluate_pair` de `scripts/utils/evaluate_graphs.py`, y el mismo
`load_services_catalog(gt_dir/"services.csv")`. Las definiciones de Service F1 y Edge F1 son
literalmente el mismo código:

- Service F1: `set_precision_recall` sobre **conjuntos únicos** de `service`
  (`evaluate_graphs.py:128-134`, invocado en `:166-168`). Idéntico en ambos lados.
- Edge F1: `edge_multiset_precision_recall` sobre multiset de pares dirigidos
  `(src_service, tgt_service)`, **ignorando el tipo** (`:137-151`, invocado en `:176-178`).
  Idéntico en ambos lados.
- Agregación: media sobre `graph_usable == True`; Edge F1 además restringido a
  `gt_edges > 0`. Standard `:123-124`; Parsimonious `:104-113`. **Misma semántica.**

**Verifiqué que las medias publicadas son reproducibles** desde los `results.csv`. No encontré
divergencia que invalide la comparación del 85.5 vs 86.7 a nivel de definición de métrica.

**Diferencias reales, todas menores pero conviene declararlas:**

| # | Diferencia | Ubicación | Impacto |
|---|---|---|---|
| 1 | Standard reporta `edge_type_accuracy`; Parsimonious no lo emite | `evaluate_standard.py:53` vs `evaluate_parsimonious.py:164-169` | Métrica ausente de un lado, no comparable |
| 2 | Standard usa `statistics.mean`; Parsimonious redondea a 4 decimales antes de multiplicar por 100 | `evaluate_standard.py:130` vs `evaluate_parsimonious.py:134-135` | ≤ 0.005 pts. Despreciable, pero es un doble redondeo innecesario |
| 3 | Standard reporta mean/median/min/max; Parsimonious solo `mean` | `:126-134` vs `:224-241` | No hay dispersión publicada del lado Parsimonious |
| 4 | Columnas del CSV distintas (`scored_for_edges`/`exclusion_reason` vs `is_zero_edge_gt`) | — | Fricción, no error |
| 5 | `gemini_model` hardcodeado vs leído de config | `:204` vs `:241` | §1.7 |

**La divergencia que sí compromete la comparación no está en el evaluador, está aguas arriba:**

- **Los prompts de los dos brazos no son simétricos.** `ara/logic/solution/constraints.md`
  lo documenta: *«Standard's Stage 2 prompt has an explicit rule to translate output fields to
  English, Parsimonious does not (verified in code, 2026-08-20)»*. Con **42 videos no-inglés**
  en el corpus (`reports/dataset_audit_2026-08-21.md:15`), es un confound declarado que ningún
  ajuste del evaluador corrige.
- **Los dos brazos usan schemas de salida distintos.** Standard fuerza `response_schema`
  Pydantic; el módulo de producción Parsimonious usa JSON libre parseado a mano
  (`vision_analyzer_parsimonious.py:223`, `:241-263`) — aunque el script que generó la mayoría
  del corpus **sí** usa Pydantic (§7.2). El brazo no es homogéneo consigo mismo.
- **Los n no coinciden entre los artefactos publicados.** El `run.json` de Parsimonious es
  n=385; el de Standard, n=370. La cifra 86.7 vs 85.5 proviene de
  `reports/dataset_audit_2026-08-21.md:28-30` (n=336, correctamente pareada) —
  **para la cual no existe ningún `run.json`.** El artefacto que respalda el número del
  artículo es un reporte de auditoría, no una corrida registrada. `[VERIFICADO]`

### 4.2 Pregunta 11 — cero aristas y `graph_usable=False` `[VERIFICADO]`

**`graph_usable`.** `evaluate_graphs.py:229-230` lee el atributo del **grafo de ground truth**
(no del generado) y normaliza el string `"false"`. Ambos lados excluyen esos videos de todas
las medias publicadas y los conservan en el CSV crudo. **Tratamiento idéntico.** En el corpus
actual son 49 de 385.

**Cero aristas en el GT.** Ambos lados los excluyen del promedio de aristas y los conservan en
el de servicios. Standard: `:101-102`, `:124`. Parsimonious: `:100`, `:107-110`.

**Una asimetría de orden, sin efecto hoy pero frágil** `[VERIFICADO]`:
`evaluate_parsimonious.py:104-110` evalúa `if not graph_usable: … else: if is_zero_edge_gt: …`.
Un video que sea **inservible y de cero aristas** entra por la primera rama y **no** aparece en
la lista `gt_has_zero_edges` del `run.json`. Standard, en cambio, acumula **ambas** razones en
`exclusion_reason` (`:104-109`). Por eso los `run.json` del 20 y 21 de agosto reportan
`gt_has_zero_edges: []` — no porque no haya, sino porque los 17 que existían están todos dentro
de los 49 inservibles (verificado: contención total). **El `run.json` de Parsimonious oculta una
categoría de exclusión que sí existe.** Hoy no cambia ninguna media; sí hace ilegible el
artefacto.

**Grafos generados con 0 aristas** (distinto de GT con 0 aristas): 4 en Parsimonious
(`BgT_bDAejSQ`, `phN08pi3YzY`, `uMX94Mn9u-4`, `zqiNLMmEeSo`) y **0 en Standard**. Son los
mismos 4 que señaló `docs/revision_parsimonious_2026-08-19.md` §4.5. No se corrigieron.

### 4.3 Pregunta 12 — normalización de nombres `[VERIFICADO]`

**Idéntica, porque es la misma función — y porque no hay normalización alguna.**

`evaluate_graphs.py` compara el atributo `service` por **igualdad exacta de string**. No hay
`.lower()`, ni tabla de alias, ni canonicalización, ni fuzzy match, en ninguna de las funciones
de extracción (`:59-90`) ni de comparación (`:110-151`). `Redshift` ≠ `redshift`;
`API Gateway` ≠ `ApiGateway`.

Ambos lados sufren esto por igual, así que **no sesga la comparación**. Pero:

- Es la razón de ser de la regla 1 del prompt parsimonioso
  (`vision_analyzer_parsimonious.py:89`, *"STRICT EXACT AWS SERVICES … STRICTLY FORBIDDEN"*):
  el prompt está compensando una limitación del evaluador. Eso vale la pena decirlo en el
  artículo, porque significa que parte del Service F1 mide adherencia tipográfica, no
  comprensión arquitectónica.
- El único evaluador permisivo (`whiteboard_selection_lab/evaluacion_permisiva.py`) se corrió
  sobre **14 videos** y **no alimenta ninguna métrica publicada**.
- El corpus tuvo históricamente 15 nodos fuera de vocabulario
  (`docs/revision_parsimonious_2026-08-19.md` §4.1). Hoy
  `reports/parsimonious_provenance.csv` reporta `unknown_services_count = 0` en las 335 filas.
  **Corregido.** ✔

---

## Bloque 5 — Lo que se puede medir hoy, sin gastar API

### 5.1 La prueba pareada que faltaba `[VERIFICADO]`

No existe en el repo ninguna prueba estadística de la diferencia Parsimonious vs Standard.
Búsqueda de `ttest|wilcoxon|scipy|paired|significan` en `scripts/`, `ara/`, `docs/` y
`reports/*.md`: los únicos aciertos son menciones en prosa en `ara/TODO_PARA_EL_ARTICULO.md`
sobre la ablación de Stage 2 de Standard. **La comparación central del artículo nunca se
testeó.**

La hice, sobre la intersección de
`reports/runs/2026-08-21_parsimonious_v9/results.csv` (385) y
`reports/runs/2026-08-20_standard_v6corrected_370v/results.csv` (370):

- Intersección: **370 videos** (los 370 de Standard son subconjunto estricto de los 385).
- Ambos `graph_usable=True`: **321**. Cero discrepancias de `graph_usable` entre lados.

| | n | Parsimonious | Standard | Δ (P−S) | sd dif | IC 95 % | t | p (t pareada) | p (Wilcoxon) |
|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| **Service F1** | 321 | 85.73 | 86.78 | **−1.05** | 8.24 | [−1.95, −0.15] | −2.29 | **0.0228** | 0.0657 |
| **Edge F1** | 321 | 57.01 | 59.65 | **−2.64** | 13.85 | [−4.15, −1.12] | −3.41 | **0.00073** | 0.00006 |

Test de signos (más robusto, ignora magnitudes):

| | Gana Pars | Gana Std | Empata | p |
|---|---:|---:|---:|---:|
| Service F1 | 68 | 94 | **159** | 0.049 |
| Edge F1 | 90 | 147 | **84** | **0.00026** |

**Lectura honesta, en tres partes:**

1. **La diferencia existe y es detectable, y va en contra de Parsimonious.** Standard gana en
   ambas métricas. El Edge F1 es sólido (p < 0.001 por dos pruebas independientes); el Service
   F1 es marginal (t pareada p = 0.023 pero Wilcoxon p = 0.066 — no coinciden, y con **159 de
   321 empates** la distribución no es normal, así que **me quedo con Wilcoxon: la diferencia
   de Service F1 no está establecida**).
2. **La magnitud es pequeña y no es «equivalencia».** Presentar 85.5 ≈ 86.7 como «rendimiento
   comparable a la mitad de coste» es defendible para Service F1; **no lo es para Edge F1**,
   donde la pérdida de 2.64 pts sí es significativa.
3. **Nada de esto es visible al tamaño de panel con el que se tomaron las decisiones.** Con el
   piso de ruido de §3.3, un panel de 30 videos tiene MDE de 4.8 / 6.1 pts. Una diferencia real
   de 1.05 / 2.64 es invisible ahí. Toda la fase de selección de prompt operó por debajo de su
   propio umbral de detección.

**Un control que refuerza la dirección:** restringiendo a los 25 videos usables con procedencia
de modelo verificable en la caché (esquema B), Δ = **−4.28 pts** (p = 0.11, n pequeño). No es
concluyente, pero **no** apunta a que la brecha se cierre al limpiar la procedencia. `[SOSPECHA]`

---

## Bloque 5b — Código

### 5.2 Pregunta 13 — código muerto y escrituras a directorios que nadie lee

**A. `scripts/utils/rebuild_parsimonious_v9.py` escribe a un directorio inexistente** `[VERIFICADO]`

`:34 output_dir = PROJECT_ROOT / "data" / "graphs_parsimonious_v9"`. **`data/graphs_parsimonious_v9/`
no existe** en el repo (`data/` contiene `graphs`, `graphs_parsimonious`, `graphs_v2_previous`,
`graphs_v6_highlighted`). El evaluador lee `data/graphs_parsimonious`. **El script que
`data/graphs_parsimonious/PROVENANCE.md` acredita como origen del corpus escribe en otra
carpeta que nadie lee.** La cadena de procedencia declarada está rota en su primer eslabón.

Agrava: `:48` acepta como objetivo tanto `v9_confirmado` como **`v9_probable`** — y los
«probable» son 280 de 335, clasificados así por un criterio que no puede dispararse (§1.8).
El script reconstruiría como v9 grafos cuya versión de prompt nadie verificó.

`PROVENANCE.md` también cita `data\_archive\2026-08-19_graphs_parsimonious_mezclada` como
destino de los experimentos v10 «contaminantes». **Ese directorio no existe en el repo**, ni
`data/graphs_parsimonious_v10/`, ni `data/batch_parsimonious_v10_progress.json`. La evidencia
central de la auditoría del 19 de agosto (v10 83.48 % vs activa 76.60 %) **ya no es
reproducible**. `[VERIFICADO]` la ausencia; `[NO PUDE VERIFICAR]` si se archivó fuera del repo.

**B. `scripts/batch_process_parsimonious_v10.py` anuncia una carpeta que no escribe** `[VERIFICADO]`

`:39-40` crea `PARSIMONIOUS_ACTIVE_DIR = data/graphs_parsimonious` y `:103` lo anuncia en el
panel de consola como directorio de destino. **Nunca escribe ahí**: `:163` exporta solo a
`PARSIMONIOUS_V10_DIR`. (La doble escritura que denunció la auditoría del 19-ago **sí se
eliminó** ✔ — pero quedó el `mkdir` y el mensaje, que ahora mienten al operador.)

Además el docstring y el nombre dicen **v10** mientras importa el prompt de
`vision_analyzer_parsimonious.py`, que hoy contiene **v9** (hash `a8f779627aba`, el mismo que
certifica el `run.json`). El nombre del script ya no describe lo que hace. Correrlo hoy
generaría grafos v9 en una carpeta llamada `graphs_parsimonious_v10`. `[VERIFICADO]`

**C. `scripts/utils/fix_parsimonious_titles.py` está roto — y menos mal** `[VERIFICADO]`

`:13 workspace = Path(__file__).resolve().parent.parent`. El archivo vive en `scripts/utils/`,
así que `parent.parent` = **`scripts/`**, y `:14 data_dir = scripts/data`, que no existe.
Todos los demás scripts usan `parent.parent.parent`. Consecuencia: `gt_dir.glob()` no devuelve
nada, `pars_dir.exists()` es `False`, y el script imprime «Loaded 0 … Updated 0» sin tocar nada.

Es una suerte, porque **si la ruta fuera correcta el script sobrescribiría `graph["name"]` de
los grafos generados con el título del ground truth** (`:69-70`, `:88-90`), destruyendo la
capacidad de auditar cómo tituló el modelo. Contaminación metodológica latente. Además usa
`nx.write_graphml` directo, sin la escritura atómica de `export_graphml`.

*(Impacto sobre métricas: ninguno. `evaluate_parsimonious.py:118-119` toma `title` y `category`
del GT, no del grafo generado.)*

**D. Rutas específicas de un sistema operativo** `[VERIFICADO]`

- `run_batch_gemini_36_multikey.py:144` —
  `node_env["PATH"] = "C:\\Users\\USUARIO\\Downloads\\PROGRAMAS\\WPy64-31040\\n;" + …`
  Ruta absoluta de una máquina Windows concreta, hardcodeada. El script falla en cualquier
  otra máquina.
- `run_batch_gemini_36_multikey.py:29` — `PROJECT_ROOT = Path('.').resolve()`. Depende del
  directorio de trabajo; todos los demás scripts usan `Path(__file__).resolve().parent…`.
- `data/graphs_parsimonious/PROVENANCE.md` usa separadores `\` de Windows.
- Todo `ara/` usa `file:///home/stemjara/Projects/AWS-Architecture/…` (Linux, otra máquina).
  **El repo contiene rutas absolutas de dos sistemas operativos distintos.**

**E. Duplicación del catálogo de servicios: cuatro rutas, tres órdenes de preferencia** `[VERIFICADO]`

| Archivo | Orden de preferencia |
|---|---|
| `scripts/core/vision_analyzer_parsimonious.py:52-55` | `data/cloudscape_gt/services.csv` → `data/services.csv` |
| `scripts/core/vision_analyzer.py:66-69` | idéntico (clon) |
| `scripts/utils/audit_parsimonious_provenance.py:19-23` | `data/services.csv` → `graph_renderer/services.csv` → `data/cloudscape_gt/services.csv` |
| `run_batch_gemini_36_multikey.py:32-34` y notebook celda 6 | `graph_renderer/services.csv` → `data/cloudscape_gt/services.csv` |
| `scripts/core/graph_builder.py::load_valid_services()` | `graph_renderer/services.csv` |

Si los tres CSV divergen alguna vez, el prompt enviado, la validación del grafo y la auditoría
de procedencia usarán vocabularios distintos, sin error visible. Hoy no hay error observable
porque coinciden, pero nada lo garantiza. `[SOSPECHA]` sobre el riesgo futuro;
`[VERIFICADO]` sobre la duplicación.

**F. Otros** `[VERIFICADO]`

- `scripts/utils/audit_dataset_coverage.py:9-11` — el docstring afirma que
  *«`evaluate_pair` never sets that key [graph_usable], so it always passes»*. **Es falso hoy:**
  `evaluate_graphs.py:237` sí devuelve `graph_usable`. Documentación obsoleta dentro de un
  script de auditoría.
- `.git/objects/pack/` contiene **~35 archivos `tmp_pack_*`** huérfanos de fetches abortados,
  cientos de MB. Higiene de repo.
- `ara/TODO_PARA_EL_ARTICULO.md` §3 tiene **todas sus líneas duplicadas** (corrupción de
  edición).

### 5.3 Pregunta 14 — divergencia silenciosa entre los dos `vision_analyzer` `[VERIFICADO]`

`scripts/core/vision_analyzer.py` (468 líneas) y `scripts/core/vision_analyzer_parsimonious.py`
(403 líneas): **similitud de secuencia 0.383**, con 167 líneas idénticas en común. No es un
fork limpio ni una jerarquía: es un copiar-pegar que divergió.

`load_services_catalog()` está **clonada literalmente** (`vision_analyzer.py:62-89` ≡
`vision_analyzer_parsimonious.py:48-76`, mismo cuerpo, misma docstring, mismo orden de rutas).

Divergencias con consecuencia:

| Aspecto | Standard | Parsimonious | Consecuencia |
|---|---|---|---|
| Salida estructurada | `response_schema` Pydantic (`vision_analyzer.py:240-244`, `:361`, `:390`) | **solo** `response_mime_type` + parseo manual (`_parsimonious.py:223`, `:241-263`) | El brazo Parsimonious puede recibir JSON malformado; Standard no |
| Reintentos | `_call_gemini_with_retry` genérico (`:223`) | solo rotación de clave en 429 (`:226-237`); **sin backoff, sin manejo de 503** | Fallos transitorios se propagan |
| Fallo de parseo | imposible (schema) | `:326-329` → `data = {"graph": {}, "nodes": [], "edges": []}` | **Un fallo de API/parseo se convierte en un grafo vacío que se evalúa como predicción legítima con F1 = 0** |
| Fusión de respuestas-lista | n/a | `:284-324` remapea `id` de nodos pero **no `flow_id`** | Dos arquitecturas fusionadas quedan con `flow_id` 0 solapados |
| Sin claves configuradas | error claro | `max_key_attempts = 0` → el bucle no corre → `:241 response.text` revienta con `AttributeError` | Mensaje de error inútil |
| Docstring de cabecera | correcto | dice `vision_analyzer.py` (`:2`) | Cosmético |

**Sobre el grafo vacío: comprobé que NO se materializó.** En
`reports/runs/2026-08-21_parsimonious_v9/results.csv` hay **0 filas con `gen_nodes == 0`** y
**0 con `svc_f1 == 0.0`**. El riesgo es real y está en el código, pero el corpus actual no está
contaminado por él. Lo digo explícitamente para no inflar el hallazgo.

*(Nota: `docs/revision_parsimonious_2026-08-19.md` §5 reportaba que los `.replace()` de
placeholders eran no-ops porque el catálogo estaba hardcodeado en la regla 1. **Eso se
corrigió**: hoy `:89` sí contiene `<AWS_SERVICES_PLACEHOLDER>` y `:132-136` sustituye de
verdad. ✔)*

---

## Bloque 6 — Balance

### 6.1 Pregunta 15 — tres cosas bien hechas, con evidencia

**1. El hash del prompt existe y es correcto.** `[VERIFICADO]`
`evaluate_parsimonious.py:48-53` calcula `sha256(CLOUDSCAPE_PROMPT_TEMPLATE)` y lo escribe en
`run.json`. **Lo verifiqué:** el SHA-256 de la plantilla en
`vision_analyzer_parsimonious.py:84-129` es
`a8f779627abaf3dc4c8d1d5d77bd1f9b8edb49c8cf6b4c5b813bfc2416930506`, exactamente el registrado en
las tres corridas. Este es precisamente el error nº 3 del lado Standard —guardar el nombre y no
el hash— **resuelto de este lado**. El defecto que le queda (hashea la plantilla, no el prompt
sustituido, §1.7) es un refinamiento, no una regresión: el esqueleto de trazabilidad está
puesto y funciona.

**2. `reports/dataset_audit_2026-08-21.md` es un análisis de sensibilidad hecho como se debe.**
`[VERIFICADO]`
Cruza los 396 GT contra cuatro criterios de exclusión (`graph_usable`, cero aristas, idioma,
pareamiento) y publica la métrica **bajo cada criterio**, en lugar de elegir uno y callar los
demás:

```
Todos los pareados        385   Std 86.2 %   Pars 85.0 %
Sin graph_usable=False    336   Std 86.7 %   Pars 85.5 %
Sin no-inglés             343   Std 85.6 %   Pars 84.3 %
Elegibles y solo inglés   301   Std 86.3 %   Pars 85.0 %
```

Comparación **pareada sobre el mismo conjunto** en cada fila, y demuestra que el resultado no
depende de a quién se incluya (±0.6 pts). Es exactamente la tabla que un revisor va a pedir, y
ya existe. `audit_dataset_coverage.py` se declara *read-only* en su docstring y lo cumple.

**3. `ara/logic/solution/constraints.md` se corrige a sí mismo y distingue hipótesis de hecho.**
`[VERIFICADO]`
Es el mejor documento del repo. §2.3 revierte explícitamente una afirmación anterior
(«requisito de ≥720p») con contraevidencia directa y fechada: *«de 17 videos nuevos … 3 fueron
aprobados a mano como pizarra válida a la misma resolución en la que otros 12 fallaron»*.
Y marca lo no probado como tal: *«**Working hypothesis, not yet validated:** el detector de
íconos … Esto necesita un test propio … antes de poder afirmarse como hecho»*. §2 corrige
también la exclusión de audio no-inglés («*that was wrong on both counts*»). Un jurado que lea
esto ve un proyecto que sabe qué sabe.

**Mención honorable:** la auditoría interna `docs/revision_parsimonious_2026-08-19.md` fue
seria y **una parte sustancial de sus hallazgos se corrigió** (§7.3). Eso es un ciclo de
mejora funcionando, y hay que contarlo.

### 6.2 Pregunta 16 — los tres problemas más graves, por riesgo de publicación

---

**#1 — `ara/evidence/` publica cifras sin fuente y una muestra que invierte el resultado.**

Es el único hallazgo que un revisor puede verificar **sin ejecutar nada**, abriendo dos
archivos. Table 2 tiene seis cifras de las que **cinco no existen en la fuente que cita**, y
una de ellas (59.7 %) es un número de otro pipeline. Table 1 recorta 16 filas de 60 de forma
que Standard 28-8 se convierte en Parsimonious 4-3, y cuatro de esas 16 filas están además
desactualizadas **todas en la misma dirección**.

Por qué es el peor: no es un error de método discutible, es una discrepancia aritmética
comprobable, y está en la capa que el ARA llama «evidencia». Encontrada por un revisor,
contamina la credibilidad de todo lo demás — incluido el trabajo bueno de §6.1.
Que `ara/TODO_PARA_EL_ARTICULO.md` §1.1-1.2 ya lo documente **agrava** el riesgo: el problema
está identificado por escrito y las tablas siguen publicadas sin corregir.

---

**#2 — Todo el prompt de producción se eligió por debajo del piso de ruido, y sobre el dato
que después se reporta.**

Nueve versiones de prompt, **16 de 18 decisiones tomadas con n = 1**. El piso de ruido medido
con los propios datos del proyecto es sd = 9.40 (Service) / 11.89 (Edge) pts por video, lo que
pone el MDE con n=1 en **26.3 / 33.3 pts**. Solo un salto de la trayectoria (v9, Registro 17)
se acerca a ese umbral, y sobre una única observación. v6→v7 y v7→v8 dieron números
literalmente idénticos.

Y el video que decidió v9 (`-3lnf5lzsH0`, 95.7 % / 64.3 %) es la fila estrella de la Table 1
del ARA y sigue con esos valores en el `results.csv` de producción. **Se eligió el prompt y se
reportó su rendimiento sobre el mismo dato.**

Es el error nº 1 del lado Standard (panel de 14 usado para elegir y reportar, ρ = −0.858 al
ampliar a 30) reproducido con **un panel de tamaño 1**. La defensa disponible es honesta pero
limitada: v9 es el prompt que se lleva al corpus completo de 385, así que el número final no
está contaminado por la selección — pero **la narrativa de «diseñamos un prompt parsimonioso
que funciona» sí lo está**, porque ninguna de las nueve iteraciones tiene evidencia que la
sostenga.

---

**#3 — La procedencia del corpus evaluado no se puede reconstruir: 87 % de los grafos no tiene
registro de modelo ni de prompt, y hay evidencia de que se mezclan cuatro modelos.**

- **86 de 385 videos (22 %) no tienen caché de análisis de ningún tipo.** Sus `.graphml` no se
  pueden regenerar ni atribuir.
- De los 299 que sí tienen caché, **280 usan un esquema que no registra `model` ni
  `prompt_version`**. Solo **51 de 385 (13 %)** tienen procedencia verificable en el artefacto.
- `prompt_ablation_detailed_report_parsimonious.html` documenta que los 250 videos que cubre se
  midieron con **cuatro modelos distintos** (145 / 79 / 19 / 7), y **53 grafos del corpus
  evaluado coinciden exactamente en nodos y aristas con corridas etiquetadas con un modelo que
  no es `gemini-3.6-flash`** — mientras `run.json` declara ese modelo para los 385 con una
  cadena **hardcodeada** (`evaluate_parsimonious.py:204`).
- Los directorios de corrida **no son inmutables** (`:182` los nombra solo por fecha), y hay
  prueba de sobrescritura: `MANIFEST.md` describe la corrida del 20-ago con métricas y commit
  que el `run.json` en disco ya no contiene.
- La cadena que `PROVENANCE.md` declara está rota: el script acreditado escribe a
  `data/graphs_parsimonious_v9/`, **que no existe**.

Por qué es grave y no simplemente desprolijo: si el corpus mezcla modelos, la comparación
Parsimonious vs Standard no compara arquitecturas de prompting, compara **una arquitectura
contra una mezcla de cuatro modelos**. Y no hay forma, con los artefactos actuales, de
demostrar que no. El punto #3 es reparable sin gastar API (§6.3-A); el #2 no.

### 6.3 Pregunta 17 — qué falta medir, y qué se puede hacer sin gastar API

**Sin una sola llamada a la API:**

| # | Medición | Cómo | Qué resuelve |
|---|---|---|---|
| **A** | **Auditar la procedencia real de los 385 grafos.** Parsear los 250 bloques de `prompt_ablation_detailed_report_parsimonious.html`, cruzar `(nodos, aristas)` y el JSON de `data/raw/` contra cada `.graphml`, y emitir un CSV `video_id → modelo, prompt, fecha, fuente`. | Ya lo hice parcialmente (§1.5). Automatizarlo y cerrarlo con los 86 sin caché. | Hallazgo #3. Es **lo primero** que hay que hacer: sin esto ninguna otra métrica es interpretable. |
| **B** | **Publicar la prueba pareada Parsimonious vs Standard** (t pareada + Wilcoxon + test de signos + IC 95 %) sobre los 336 elegibles. | §5.1, `scipy.stats`, 20 líneas. | La comparación central del artículo, hoy sin test. |
| **C** | **Publicar el test-retest del Registro 36 como medición de ruido.** | §3.3, ya está pagado. | Da el piso de significancia del lado Parsimonious y respalda que temperatura 0.0 no es determinista, con datos propios. |
| **D** | **Recalcular la curva MDE vs n y ponerla en el artículo.** | §3.2, aritmética. | Convierte «elegimos el prompt mirando 1 video» de omisión en limitación declarada. Es la diferencia entre que lo diga la autora y que lo diga el jurado. |
| **E** | **Re-generar Table 1 y Table 2 desde `reports/dataset_audit_2026-08-21.csv`**, completas y sin recortar. | Ya hay CSV. | Hallazgo #1. |
| **F** | **Re-ejecutar `audit_parsimonious_provenance.py` en esta copia de trabajo** (con `lab_workspace/` poblado) y ver cuántos «v9_probable» ascienden a «v9_confirmado». | Un comando. Verifiqué que al menos `-3lnf5lzsH0` sí casa. | Sube el 13 % de procedencia verificable sin gastar nada. |
| **G** | **Hacer inmutables los directorios de corrida:** nombrarlos `{fecha}_{modo}_{label}_{hash8}_{n}v` y hacer que el script se niegue a sobrescribir. Regenerar `MANIFEST.md`. | `evaluate_parsimonious.py:182`. | Detiene la pérdida de trazabilidad hacia adelante. |
| **H** | **Hashear el prompt sustituido, no la plantilla**, y registrar en `run.json`: `temperature`, `response_schema` usado, versión del SDK, y el modelo leído de `GEMINI_MODEL` (no hardcodeado). | `evaluate_parsimonious.py:48-53`, `:204`. | Cierra §1.7. |
| **I** | **Cuantificar el confound de idioma entre brazos:** Service/Edge F1 pareado en los 42 videos no-inglés vs los 343 restantes, por brazo, con término de interacción. | Los CSV ya lo permiten; `dataset_audit` ya trae el idioma. | La regla de traducción existe en Standard y no en Parsimonious. Hoy es un confound **declarado pero no medido**. |
| **J** | **Cuantificar el efecto del vocabulario exacto:** correr `evaluacion_permisiva.py` sobre los 385 (es offline, lee `.graphml`) y publicar estricto vs permisivo a escala. | Hoy son 14 videos. | Da la Table 2 real, y separa error tipográfico de error arquitectónico. |
| **K** | **Diagnóstico de aristas del lado Parsimonious**, análogo al §2.7 de Standard: descomponer las aristas perdidas en (retornos no dibujados / actores podados / direccionalidad invertida / servicio mal nombrado). | `edges_only_gt` / `edges_only_gen` ya salen de `evaluate_pair`. | Explica el 57 % de Edge F1 en vez de solo reportarlo. Es el hallazgo más accionable del lado Standard y no tiene equivalente aquí. |

**Lo que sí requiere API, en orden de valor por llamada:**

1. **Repetir el corpus elegible 3 veces con la configuración congelada** (336 videos × 3 ≈ 1 008
   llamadas). Da IC de la media, no solo del ruido por video, y permite reportar
   «85.5 ± x %» en vez de un puntual. Sin esto, el número del artículo no tiene barra de error.
2. **Ablación real del prompt parsimonioso** sobre ≥ 100 videos: v6, v7, v8, v9 con el mismo
   modelo y hash registrado. Hoy **no existe ninguna ablación parsimoniosa** — el archivo que
   se llama así contiene un solo prompt y cuatro modelos.
3. **La ablación solo-visión que C01 necesita** para no ser un claim sin prueba.
4. **Re-generar los 86 videos sin caché** con la configuración congelada, o excluirlos y
   declararlo.

---

## 7. Anexos

### 7.1 Cómo se verificó

- Copia de trabajo leída vía puente de dispositivo, **sin escribir en el repo**. Único archivo
  creado: este informe.
- Métricas recalculadas con `csv` + `statistics` + `scipy.stats` sobre los `results.csv`
  publicados. No se re-ejecutó `evaluate_pair` (no se movió ningún `.graphml`).
- Hashes con `hashlib.sha256` sobre el texto extraído por regex del `.py` y del `.ipynb`.
- Test-retest §3.3: parseo de las tablas markdown de los Registros 24, 26 y 36 de
  `parsimonious_prompt_history.md`, columna «Nueva Prueba», emparejado por `video_id`.
- §1.5: parseo del HTML (250 bloques), cuarta columna de cada tabla, cruzada contra
  `results.csv` por `(gen_nodes, gen_edges)`.
- Cachés de esquema B: descargadas y leídas las 55; 51 tienen campo `model`.
- MDE ≈ 2.8·sd/√n (80 % potencia, α = 0.05 bilateral), con sd tomada del test-retest propio.

### 7.2 Quién genera realmente `data/graphs_parsimonious/` `[VERIFICADO]`

No es ninguno de los scripts de `scripts/`. Es **`run_batch_gemini_36_multikey.py`**, en la raíz
del repo:

```
:43   from scripts.core.vision_analyzer_parsimonious import CLOUDSCAPE_PROMPT_TEMPLATE   ← ✔ ya no duplica el prompt
:45   prompt = TEMPLATE.replace("<USER_ACTORS_PLACEHOLDER>", lista_actores)…             ← pero con la regla is_aws (34 actores)
:184  config={"response_mime_type":…, "response_schema": FinalArchitectureSchema}        ← Pydantic (producción NO lo usa)
:238  nx.write_graphml(test_g, str(cache_graphml))                                        ← salta export_graphml (sin escritura atómica)
:239  create_graph_from_cloudscape_json(res_data)                                         ← sin video_id ni video_url
:247  shutil.copy2(cache_graphml, data/graphs_parsimonious/<vid>.graphml)                 ← ESTE es el corpus evaluado
:248  shutil.copy2(cache_json,   data/raw/<vid>_vision_analysis_parsimonious.json)        ← esquema A, sin model ni prompt_version
```

Esto explica de una sola vez: por qué 280 cachés son esquema A sin metadatos; por qué el corpus
usa Pydantic aunque la documentación diga que no; y por qué el prompt real lleva 34 actores en
vez de 28. **El artefacto que el `run.json` certifica con el hash de
`vision_analyzer_parsimonious.py` no fue generado por ese módulo.**

### 7.3 Qué se corrigió desde `docs/revision_parsimonious_2026-08-19.md`

Justicia para el trabajo hecho:

| Hallazgo del 19-ago | Estado hoy |
|---|---|
| Placeholders muertos (catálogo hardcodeado en regla 1) | ✔ **Corregido** — `:89` usa `<AWS_SERVICES_PLACEHOLDER>`, `:132-136` sustituye |
| `title`/`category` literales inventados (`Video <id>`, `Uncategorized`) | ✔ **Corregido** — `:118-119` los toma del GT |
| Unidades incompatibles (fracciones vs porcentajes) | ✔ **Corregido** — `:122-129` escribe porcentajes |
| No emite `run.json` ni queda bajo `reports/runs/` | ✔ **Corregido** — `:180-244` |
| Grafos sin GT se saltan sin contarse | ✔ **Corregido** — `skipped_no_gt` en `run.json` |
| Segunda copia del prompt en `run_batch_gemini_36_multikey.py` | ✔ **Corregido** — ahora importa la plantilla |
| Doble escritura de `batch_process_parsimonious_v10.py` | ✔ **Corregido** — solo escribe a `_v10` |
| 15 servicios fuera de vocabulario | ✔ **Corregido** — `unknown_services_count = 0` en las 335 filas |
| `data/graphs_parsimonious_v9/` no existe | ✘ **Sigue sin existir**; `rebuild_parsimonious_v9.py` sigue escribiendo ahí |
| 4 grafos con 0 aristas generadas | ✘ **Siguen** (`BgT_bDAejSQ`, `phN08pi3YzY`, `uMX94Mn9u-4`, `zqiNLMmEeSo`) |
| `fix_parsimonious_titles.py` contamina títulos | ⚠ **Inerte por un bug de ruta** (`:13`), no por diseño |
| Sin backoff exponencial ni manejo de 503 | ✘ **Sigue** |
| PATH de Windows hardcodeado | ✘ **Sigue** (`:144`) |
| `nx.write_graphml` directo saltando `export_graphml` | ✘ **Sigue** (`:238`) |
| Salto de videos sin validar tamaño ni parseo | ✘ **Sigue** (`:106`) |
| Segunda copia del prompt en el notebook de ablación | ✘ **Sigue, y con hash distinto** (`deebeebfdec7…`) |
| Artefactos v10 para reproducir la comparación | ✘ **Desaparecidos** — carpeta y progress JSON ya no están |

### 7.4 Lo que NO pude verificar

- **Los `git_commit` de los `run.json`.** Ni `932e3f9`, ni `171d123`, ni `ec35624`, ni
  `a415d5d` aparecen en `.git/logs/HEAD`. **Esto no prueba que no existan**: las dos últimas
  entradas del reflog son `pull origin main: Fast-forward`, y un fast-forward no registra los
  commits intermedios. Verificarlo requiere `git cat-file` sobre los packfiles
  (~700 MB), fuera de alcance en esta sesión. **`[NO PUDE VERIFICAR]`**
- **El contenido de los 421 `.graphml`.** Leí 3. El resto se auditó indirectamente vía
  `results.csv` y `parsimonious_provenance.csv`.
- **Si los artefactos v10 se archivaron fuera del repo.** `PROVENANCE.md` cita
  `data\_archive\…`, que no está. No hay forma de saber si existe en otra máquina.
- **La fecha real de generación de cada grafo.** Los mtimes solo dicen última escritura, y
  hubo reconstrucciones posteriores (§1.8).
- **Si la desactualización de Table 1 fue deliberada.** Los cuatro errores van en la misma
  dirección; eso es un hecho. La causa no la puedo determinar desde el repo.
- **`ara/logic/related_work.md`, `problem.md`, `architecture.md`, `algorithm.md`,
  `trace/exploration_tree.yaml`**: fuera del alcance solicitado, no auditados.

---

## 8. Tabla de cierre

| # | Hallazgo | Severidad | Qué haría falta para resolverlo |
|---:|---|---|---|
| 1 | Table 2: 5 de 6 cifras no están en la fuente citada; 59.7 % es el Edge F1 de Standard | **Bloqueante** | Regenerar desde `reports/dataset_audit_2026-08-21.csv` y `permissive_batch_evaluation.csv`. Corregir la descripción del mecanismo permisivo (superclases, no alias). ~1 h |
| 2 | Table 1: 16 filas de 60; el recorte invierte 28-8 a 4-3. 4 filas desactualizadas, las 4 a favor de Parsimonious | **Bloqueante** | Publicar la tabla completa desde el CSV, o un muestreo declarado y aleatorio. ~1 h |
| 3 | El prompt v9 se eligió sobre **1 video**, que es la fila estrella de Table 1 | **Bloqueante** | No es reparable a posteriori. Declararlo como limitación + publicar la curva MDE (§3.2) + no presentar la trayectoria de prompts como evidencia. Re-hacerlo bien cuesta ≥ 400 llamadas |
| 4 | 87 % del corpus sin registro de modelo/prompt; 86 videos sin caché; evidencia de mezcla de 4 modelos | **Bloqueante** | Auditoría de procedencia §6.3-A; re-generar o excluir-y-declarar los 86; re-ejecutar el auditor con `lab_workspace/` poblado (§6.3-F) |
| 5 | La comparación 85.5 vs 86.7 nunca se testeó; hecha la prueba, Standard gana en Edge F1 (p < 0.001) | **Alta** | Publicar §5.1 con IC y Wilcoxon. Ajustar la narrativa: la paridad es defendible en Service F1, **no** en Edge F1. ~2 h |
| 6 | Las 3 corridas de agosto son incrementales; el movimiento aparente es del evaluador, no del modelo | **Alta** | Declararlas como una sola medición sobre corpus creciente. Re-evaluar el corpus del 19-ago con el evaluador actual (§2.2) y publicar la serie homogénea. ~1 h |
| 7 | Existe un test-retest válido (Reg 24&26 → 36) sin usar: 60 %/37 % de salidas idénticas, sd 9.40/11.89, media Edge −3.61 sin cambiar nada | **Alta** *(oportunidad)* | Publicarlo como medición del piso de ruido. Ya está pagado. ~2 h |
| 8 | `run.json` insuficiente: modelo hardcodeado, sin temperatura, sin schema, commit de la evaluación; directorios sobrescribibles por fecha | **Alta** | §6.3-G y §6.3-H. Regenerar `MANIFEST.md`. ~3 h |
| 9 | El hash cubre la plantilla, no el prompt enviado; dos reglas de partición del catálogo dan prompts distintos con el mismo hash | **Alta** | Hashear el prompt sustituido; unificar la partición en una sola función compartida. ~2 h |
| 10 | `MANIFEST.md` desincronizado (85.12/55.31/`edf995f` vs 85.73/57.01/`171d123`); falta la corrida del 21; 3 de 4 enlaces rotos | **Media** | `build_manifest.py` tras arreglar #8. ~30 min |
| 11 | C01 «Validated» sin la ablación que podría falsarlo; C03 dice temp 0.1 (código: 0.0) y afirma eliminar `UserCompanyDeveloper`, que el prompt ordena generar; C02 cita una ruta inexistente | **Media** | Reescribir los cuatro claims contra evidencia existente; marcar C01 como no probado. ~3 h |
| 12 | `rebuild_parsimonious_v9.py` escribe a `data/graphs_parsimonious_v9/`, que no existe; `PROVENANCE.md` cita un archivo también inexistente | **Media** | Crear la carpeta y ejecutar de verdad, o borrar el script y reescribir `PROVENANCE.md` con lo que pasó. ~2 h |
| 13 | Asimetría de prompts entre brazos: Standard traduce al inglés, Parsimonious no, con 42 videos no-inglés | **Media** | Medir la interacción idioma×brazo (§6.3-I). Si es material, declararla como confound; si no, publicar la evidencia de que no lo es. ~2 h |
| 14 | El «reporte de ablación parsimoniosa» no contiene ablación (1 prompt) y mezcla 4 modelos | **Media** | Renombrar y re-etiquetar por modelo, o retirarlo del conjunto citable. Correr una ablación real cuesta API. ~1 h + API |
| 15 | Parseo manual sin `response_schema` en el módulo de producción: un fallo de API se convierte en grafo vacío con F1 = 0 (**no materializado hoy**) | **Media** | Adoptar `response_schema` Pydantic (ya se usa en el script que generó el corpus) y hacer que un fallo levante excepción en vez de devolver un grafo vacío. ~1 h |
| 16 | 4 grafos con 0 aristas generadas, señalados el 19-ago y sin corregir | **Media** | Diagnosticar y re-generar esos 4, o excluirlos declarándolo. Cuesta 4 llamadas |
| 17 | `run.json` de Parsimonious oculta la categoría `gt_has_zero_edges` cuando el video es además inservible | **Baja** | Acumular ambas razones como hace Standard (`evaluate_standard.py:104-109`). ~15 min |
| 18 | `fix_parsimonious_titles.py`: bug de ruta (`:13`) lo deja inerte; si funcionara, contaminaría los títulos con GT | **Baja** | Borrarlo. No arreglar la ruta. ~5 min |
| 19 | `batch_process_parsimonious_v10.py` anuncia una carpeta que no escribe; el nombre dice v10 pero usa v9 | **Baja** | Renombrar y quitar el `mkdir`/mensaje engañosos. ~15 min |
| 20 | Catálogo de servicios duplicado en 3 rutas con 3 órdenes de preferencia y 2 reglas de partición | **Baja** | Una sola función compartida, un solo CSV canónico. ~1 h |
| 21 | Rutas absolutas de dos SO distintos (`C:\Users\USUARIO\…`, `/home/stemjara/…`) | **Baja** | Rutas relativas en `ara/`; PATH de Node por variable de entorno. ~1 h |
| 22 | Numeración rota del historial (falta Reg 22; 9, 23 y 38 duplicados); `TODO_PARA_EL_ARTICULO.md` §3 con líneas duplicadas | **Baja** | Renumerar y anotar la corrección. Nada citable depende de esos IDs todavía. ~30 min |
| 23 | Los `git_commit` de los `run.json` no aparecen en el reflog | **Sin determinar** | `git cat-file -t <sha>` para los cuatro. 5 min con acceso a git |

---

*Informe generado en modo solo lectura. Ningún archivo del repositorio fue modificado, creado
ni borrado, salvo este documento.*
