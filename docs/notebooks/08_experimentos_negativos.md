*Fecha: 2026-09-02*
*Hash (SHA-256): 39dcd8d279a935048bd5937e4c5aeebb27a25784a8b2446780dbc42cfb9e294b*

## Propósito
Evalúa cuatro intervenciones dirigidas diseñadas para mitigar causas específicas de pérdida de aristas, verificando si sus mecanismos funcionaron y su impacto final medible en el Edge F1.
**Artefacto producido:** `results/experimentos_negativos.json`.

## Entradas
- Salidas de los experimentos puntuales (Evidencia visual / Hough, V8 actores y retornos, Auditoría de retornos).

## Compuertas
*(Ninguna `assert` explícita en este notebook).*

## Método
- Cada experimento se compara contra **su propia base** (la corrida que le corresponde por configuración) para calcular el diferencial ($\Delta$) y la prueba de signos, y no contra un promedio global.

## Resultados

**Resultado sobre el panel de 30:**
```text
MDE n=30 · Edge 3.29 pts · Service 1.76 pts

base (produccion, panel 30) : Svc 88.07  Edge 58.99
base rep4 (para la auditoria): Svc 86.13  Edge 57.87

                           n  Svc base  Svc exp  Edge base  Edge exp  delta Edge  x MDE  gana  pierde  empata  p (signos)   veredicto
intervencion                                                                                                                         
Evidencia visual (Hough)  30     88.07    86.31      58.99     57.39       -1.60  0.487     4       7      19       0.549  sin efecto
V8 · actores y retornos   30     88.07    86.21      58.99     58.40       -0.59  0.179     6       9      15       0.607  sin efecto
Auditoria de retornos     30     86.13    86.13      57.87     59.07        1.20  0.365     4       3      23       1.000  sin efecto
```
- "Las tres caen por debajo del MDE y ninguna alcanza significancia. Los empates son la categoría dominante: en la mayoría de los videos el resultado no cambia."

**Los mecanismos funcionaron; el F1 no se movió:**
```text
                                                   antes  despues  objetivo
intervencion            mecanismo                                          
V8 · actores y retornos actores User* recuperados   20.0     29.0      34.0
                        % pares bidireccionales     12.4     17.9      46.7
                        aristas generadas (total)  269.0    299.0     361.0

Auditoria de retornos — propuestas del modelo: 25
   aceptadas por el validador : 25 (100%)
   rechazadas                 : 0
   Service F1: 86.13 -> 86.13  (identico por construccion: nodos congelados)

   prueba pareada: 4 gana / 3 pierde / 23 empata · p = 1.0000
```
- "Las intervenciones hicieron lo que prometían —recuperaron actores, subieron la bidireccionalidad, generaron propuestas válidas— y el F1 de aristas quedó igual. Eso es lo que descarta que la brecha sea un problema de instrucción."

## Limitaciones
- "Cada intervención tiene una sola corrida contra su base. Con el MDE medido, un efecto menor al umbral no es distinguible del ruido, de modo que la afirmación es *no detectable*, no *nulo*."
