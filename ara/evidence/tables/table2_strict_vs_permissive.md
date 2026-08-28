# Tabla 2 · Evaluación estricta vs permisiva

**Fuente:** `reports/ablation/2026-08-25_1637_STAGE2_V6_CORRECTED_cell9_p30/run.json` — corrida de producción sobre el panel de 30 videos (`STAGE2_V6_CORRECTED`, celda 9, sha `ed1d85054d73`), n = 30.
**Reproducir:** `.venv/bin/python scripts/ablation/build_evidence_tables.py`

Los dos protocolos puntúan **los mismos grafos generados**. No hay una segunda corrida ni una segunda llamada a la API: cambia el evaluador, no la salida del modelo. Toda diferencia de esta tabla es diferencia de criterio de medición.

## Qué relaja exactamente el protocolo permisivo

Tres cosas a la vez, no una. Conviene enumerarlas porque la ganancia se suele atribuir entera a la primera:

1. **Colapso de subtipos de actor** — todo `User*` cuenta como `User` y todo `ThirdParty*` como `ThirdParty`.
2. **Aristas como conjunto** — las instancias duplicadas del mismo par de servicios dejan de contarse por separado.
3. **Aristas no dirigidas** — `A → B` y `B → A` pasan a ser la misma arista, así que **los errores de dirección dejan de penalizar**.

Implementación: `scripts/ablation/build_evidence_tables.py:norm_permissive`, copia fiel de `generate_comparison_plots.py`. El estricto es `scripts/utils/evaluate_graphs.py:evaluate_pair` — servicios por conjunto con coincidencia exacta de cadena, aristas por multiconjunto dirigido.

## Resultados

| Métrica (media por video) | Estricto | Permisivo | Δ |
| :--- | ---: | ---: | ---: |
| Precisión de servicios | 89.99 % | 93.12 % | +3.13 |
| Recall de servicios | 86.86 % | 91.72 % | +4.86 |
| **F1 de servicios** | 88.07 % | 92.07 % | +4.00 |
| Precisión de aristas | 69.64 % | 76.88 % | +7.24 |
| Recall de aristas | 53.75 % | 77.89 % | +24.14 |
| **F1 de aristas** | 58.99 % | 76.88 % | +17.89 |

Distribución de la ganancia video por video:

| Ganancia permisivo − estricto | media | IC 95 % | mejora | empata | empeora |
| :--- | ---: | :---: | ---: | ---: | ---: |
| F1 de servicios | +4.00 | [+1.41, +6.60] | 9 | 21 | 0 |
| F1 de aristas | +17.89 | [+13.30, +22.49] | 28 | 1 | 1 |

*No se reporta una prueba de significancia sobre esta diferencia, y es a propósito.* El signo lo fija el diseño del evaluador, no el desempeño del modelo: relajar el criterio agrega coincidencias en casi todos los videos, así que contrastar contra «la ganancia es cero» sería contrastar una hipótesis que nadie sostiene. Lo informativo es la magnitud y su dispersión.

El signo tampoco está garantizado video a video, y conviene no afirmarlo: en `-wLEkq21cvA` el F1 de aristas **baja** de 77.78 a 72.73. Colapsar los subtipos de actor y volver las aristas no dirigidas también fusiona nodos y aristas del ground truth, así que los denominadores de las dos partes se achican de forma despareja y el F1 puede caer.

## Lectura

1. La ganancia en aristas (+17.89 puntos) es grande, pero **no mide una mejora del pipeline**: el pipeline no cambió. Mide cuánto del error estricto dependía de exigir la dirección de la flecha y de contar las instancias duplicadas. El protocolo permisivo responde una pregunta más fácil, y responderla mejor no es un hallazgo.
2. Por eso la cifra que se reporta como resultado del sistema es la **estricta**. La permisiva sirve para localizar dónde está el error, no para acreditar el desempeño.
3. **La subida del recall no significa que se encuentren más conexiones.** Es la lectura intuitiva y es falsa. Los conteos brutos sobre los 30 videos:

   | | aristas en el GT | aristas generadas | aciertos |
   | :--- | ---: | ---: | ---: |
   | Estricto (dirigido, multiconjunto) | 361 | 269 | 183 |
   | Permisivo (no dirigido, conjunto) | 212 | 216 | 163 |

   Los **aciertos bajan** de 183 a 163. Lo que sube el recall es que la referencia se achica 41.3 % (361 → 212 aristas): colapsar actores y quitar la dirección fusiona aristas **del ground truth también**, no sólo de la salida del modelo. El permisivo no acredita más aciertos; mide contra una referencia más chica.
4. En servicios la ganancia es chica (+4.00 puntos): la identificación de servicios casi no depende del criterio de medición, mientras que la topología depende muchísimo. Es la misma asimetría que aparece en la Tabla 1.

## Nota de corrección

Una versión anterior de esta tabla publicaba seis cifras (78.4 / 91.2 / 72.1 / 85.6 / 48.2 / 59.7 %) atribuidas a `evaluacion_estricta_vs_permisiva.html`. **Ninguna de las seis aparece en ese archivo**, y 59.7 coincide con el Edge F1 *estricto* del pipeline Standard sobre otro corpus (n=321) — una cifra de otra corrida colocada en la celda «Edge F1 permisiva». Aquella versión también describía el mecanismo como un diccionario de alias de servicios (`lambda_function → Lambda`), que no es lo que hace el evaluador. Ambas cosas quedan corregidas acá.
