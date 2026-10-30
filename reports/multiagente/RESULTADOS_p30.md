# Multiagente en el panel de 30 (gemini-3.8-flash, k=1, réplica 0)

Comparación pareada con `multiagent/estadistica.py`. Δ = B − A, IC95 por bootstrap. MDE = 3,29.

## Línea base

| Corrida | svc F1 | edge F1 | llamadas | USD |
|---|---|---|---|---|
| Standard V6, gemini-3.6-flash (producción, paper) | 88,07 | 58,99 | — | — |
| Standard V6, gemini-3.8-flash, ambas etapas (`standard_v6_gemini-3.8-flash_p30`) | 85,72 | 56,91 | 60 | 1,35 |

Pasar de 3.6 a 3.8: edge Δ −2,07, IC95 [−6,85, +2,78], Wilcoxon p = 0,415. Queda por debajo del MDE, así que el cambio de modelo no mueve el resultado de forma detectable.

## Configuraciones contra Standard 3.8

| # | Config | svc F1 | edge F1 | Δ edge | IC95 | signos (+/−/=) | Wilcoxon p | Â12 | llamadas nuevas | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Standard 3.8 | 85,72 | 56,91 | — | — | — | — | — | 60 | 1,35 |
| 3 | completo | 83,31 | 52,59 | −4,32 | [−11,28, +2,47] | 11/16/3 | 0,194 | 0,44 | 114 | 2,28 |
| 6 | sin_a4 | 83,31 | 52,59 | −4,32 | igual a completo | | | | 0 (caché) | — |
| 5 | sin_c2 | 83,28 | 52,26 | −4,66 | [−10,93, +1,55] | 9/15/6 | 0,143 | 0,44 | 4 | 0,04 |

- **C2 en el panel**: completo − sin_c2 = +0,34, IC95 [−1,15, +1,86], 4/4/22. Coincide con lo que dio en validación (+0,7): el efecto es real pero chico.
- **A4**: corrió en 24 de 30 videos (46 avisos `par_ambiguo` y 9 `nodo_huerfano`) y devolvió 0 correcciones las 24 veces. Cuesta unos $0,02 por video y no aporta.

## Precisión de las aristas según su procedencia (completo)

| Procedencia | aristas | % | precisión |
|---|---|---|---|
| ambas (dibujada y hablada) | 202 | 66 | 64,9 |
| solo dibujada | 75 | 24 | 44,9 |
| solo hablada | 23 | 7 | 48,6 |
| regla C2 (`ida_y_vuelta`) | 8 | 3 | 37,5 |

Una arista que aparece en las dos fuentes acierta unos 20 puntos más que una que viene de una sola.

## De dónde sale la caída (peores videos)

- **6CgqEzyWpeA** (−45,7):
  - C2 `actor_subtipo` cambió UserConsumerWebMobile a UserConsumerMobile, pero el GT de este video conserva WebMobile. Esa sola regla rompe 4 aristas.
  - Además, A3 invierte flujos de disparo: escribe Lambda→SQS donde el GT tiene SQS→Lambda, y lo mismo con StepFunctions→Lambda y CloudWatch→Lambda. En el agregado esto no explica la brecha: ver la evaluación permisiva más abajo, donde la regla N no la achica.
- **u3ZwnulzLnU** (−41,7): leyó Fargate como ECS. A3 no ve la pizarra, solo el texto de A1, y "ES"/"ECS" en una caja no alcanza para distinguirlos. Ese error se arrastra a 6 aristas.
- **1aYoIZvabbk** (−38,9): sobregenera, con 13 aristas contra 5 del GT. Los EKS→SQS×3 y EKS→ThirdParty×3 salen de la regla de mantener interacciones distintas por workflow.

En lo agregado, el sistema completo genera 308 aristas contra 291 de Standard (el GT tiene 361), con la misma cobertura de servicios.

## Evaluación permisiva con las reglas por separado (`multiagent/permisivo.py`, 0 llamadas)

Reglas: **A**, colapsar subtipos de actor; **C**, contar las aristas como conjunto; **N**, tratarlas como no dirigidas. Con ninguna se reproduce el estricto de run.json, y con A+C+N el permisivo del paper (producción 3.6 da 76,88, igual que la Tabla 2). Detalle en `permisivo_por_regla.json`.

| Reglas | Std 3.6 | Std 3.8 | completo | Δ completo − Std 3.8 | IC95 | Wilcoxon p |
|---|---|---|---|---|---|---|
| estricto | 58,99 | 56,91 | 52,59 | −4,32 | [−11,3, +2,5] | 0,19 |
| A | 61,74 | 62,39 | 58,71 | −3,68 | [−10,4, +3,1] | 0,27 |
| C | 62,23 | 60,24 | 56,12 | −4,12 | [−10,9, +2,8] | 0,19 |
| N | 61,60 | 60,01 | 55,24 | −4,76 | [−11,9, +2,1] | 0,24 |
| A+C | 65,27 | 66,53 | 63,21 | −3,32 | [−9,6, +3,3] | 0,24 |
| A+N | 64,35 | 65,78 | 61,36 | −4,42 | [−11,4, +2,4] | 0,25 |
| C+N | 73,40 | 70,41 | 65,87 | −4,54 | [−11,5, +2,4] | 0,18 |
| A+C+N | 76,88 | 77,70 | 73,48 | −4,22 | [−10,6, +2,4] | 0,10 |
| svc estricto | 88,07 | 85,72 | 83,31 | −2,40 | [−5,9, +1,2] | 0,20 |
| svc con A | 92,07 | 93,05 | 92,33 | −0,71 | [−3,7, +2,4] | 0,57 |

### Lectura

1. **El hueco del multiagente no se mueve con ninguna regla.** Va de −3,3 a −4,8 en las 8 combinaciones. No viene de nombres de actor, de duplicados ni de dirección: el sistema conecta **pares de servicios equivocados**. En A+C+N acierta 162 pares contra 171 de Standard, con 226 y 231 generados. La pérdida está sobre todo en el recall: 75,9 contra 82,1 en A+C+N, y la precisión cae menos (72,7 contra 75,2). Esto descarta la hipótesis de que A3 invertía flujos de disparo: bajo N la diferencia no se achica.
2. **En servicios, la desventaja del multiagente es casi toda de nombres de actor.** Pasa de −2,40 a −0,71 con A. Es el terreno de C1 y de `actor_subtipo`.
3. **3.6 contra 3.8 es solo el subtipo de actor.** La ventaja de 3.6 (+2,07 en aristas y +2,35 en servicios) desaparece con A: queda en −0,65 y −0,98. El cambio de modelo no altera la topología, solo cómo se nombra al actor.
4. **C y N interactúan.** En Std 3.8, C suma +3,3 y N +3,1 por separado, pero juntas suman +13,5, unos 7 puntos más que la suma. El GT dibuja muchas idas y vueltas como dos aristas (A→B y B→A). En multiconjunto no dirigido cuentan doble y con conjunto se funden. Es la misma convención que encontró el experimento de reglas.
   Aportes de Shapley sobre +20,8 (Std 3.8): A 6,3, C 7,5, N 7,0. En completo: A 6,8, C 7,7, N 6,4.

## Configuraciones 2 y 7 (unica, brazo_b_sin_a4), 60 llamadas, unos $2,4

| Reglas | Std 3.8 | completo | unica | brazo_b sin A4 |
|---|---|---|---|---|
| estricto | 56,91 | 52,59 | 55,03 | 93,08 |
| A+C+N | 77,70 | 73,48 | 75,52 | 95,54 |
| svc | 85,72 | 83,31 | 84,94 | 96,81 |

- **unica contra Std 3.8**: edge Δ −1,89, IC95 [−6,3, +2,4], p = 0,54, por debajo del MDE. Empata.
- **unica contra completo**: Δ +2,43, IC95 [−3,0, +7,9], p = 0,33. Separar en agentes no suma, y la tendencia es a restar.
- **brazo_b**: con la lectura perfecta, A3 + C2 llegan a 93,1 en estricto. Las reglas permisivas casi no le suman (95,5), así que el reconciliador no es el cuello de botella; lo es la lectura de la pizarra. Es un techo, no comparable con el oráculo de Standard (83,18, con 3.6 y otro formato de entrada).
- Salida completa del análisis: `post_corrida.txt`, `estadistica_vs_base38_v2.json`, `permisivo_por_regla_v2.json`.
