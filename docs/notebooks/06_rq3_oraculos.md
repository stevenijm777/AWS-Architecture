*Fecha: 2026-09-02*
*Hash (SHA-256): e1c93242c6f9fddb888b8e3d25d8ecf6cf7a08a5085464a1d09a53fdf0a29fd9*

## Propósito
Determina dónde está el cuello de botella del sistema aislando la etapa 1 mediante tres brazos (Producción, transcripción humana a ciegas, y ground truth) para evaluar si la lectura de la pizarra es el límite.
**Artefacto producido:** `results/rq3_oraculos.json`.

## Entradas
- Archivos de resultados correspondientes a los tres brazos (Producción, visión/transcripción humana, oráculo/ground truth).
- Umbrales calculados del notebook de calibración de ruido.

## Compuertas
*(Ninguna `assert` explícita en este notebook).*

## Método
- **Brazo A (transcripción humana):** Una persona transcribió la pizarra a ciegas (sin audio y sin ver el ground truth).
- **Brazo B (ground truth):** La etapa 2 recibe la respuesta directa como ground truth.
- Se compara el desempeño de los brazos A y B contra Producción calculando el diferencial ($\Delta$) y expresándolo como múltiplo del MDE.
- **Prueba pareada por video:** Prueba de signos no paramétrica.

## Resultados

**Carga de las tres condiciones:**
```text
                                                                  Service F1  Edge F1  n_videos
brazo         corrida                                                                          
produccion    2026-08-25_1637_STAGE2_V6_CORRECTED_cell9_p30            88.07    58.99        30
              2026-08-27_1640_STAGE2_V6_CORRECTED_cell9_p30_rep2       87.03    57.86        30
              2026-08-29_0442_STAGE2_V6_CORRECTED_cell9_p30_rep3       87.19    57.81        30
              2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4       86.13    57.87        30
A · vision    2026-08-29_0725_STAGE2_V6_CORRECTED_cell9_p30_o...       87.82    60.40        30
B · oracle_gt 2026-08-28_0315_STAGE2_V6_CORRECTED_cell9_p30_o...       99.70    83.18        30
              2026-08-28_2211_STAGE2_V6_CORRECTED_cell9_p30_o...       99.44    81.16        30
MDE n=30 (de 01_calibracion_ruido): Edge 3.29 pts · Service 1.76 pts
```

**El resultado central:**
```text
               corridas  Service F1  Edge F1
brazo                                       
produccion            4       87.10    58.13
A · vision            1       87.82    60.40
B · oracle_gt         2       99.57    82.17

Contra produccion (Edge F1 = 58.13, MDE = 3.29 pts):

  A · vision        +2.27 pts = 0.69x MDE   dentro del ruido
  B · oracle_gt    +24.04 pts = 7.31x MDE   *** SENAL ***

  B - A            +21.77 pts = 6.62x MDE
```
- "El brazo A no se despega de producción: su diferencia queda por debajo del umbral. El brazo B lo supera por un múltiplo grande. Ni la etapa 2 ni la calidad de lectura de la etapa 1 son el factor limitante."

**Distancia al techo, repartida:**
```text
                                            puntos                                       atribuible a  % de la brecha
tramo                                                                                                                
Stage 1 automatico -> transcripcion humana    2.27                   calidad de lectura de la pizarra            5.42
transcripcion humana -> ground truth         21.77              informacion que NO esta en la pizarra           52.00
ground truth -> 100                          17.83  perdida propia de Stage 2 (con la respuesta en...           42.59
```

**Prueba pareada por video:**
```text
                           n  gana  pierde  empata  dif media  p (signos)         veredicto
brazo         metrica                                                                      
A · vision    Edge F1     30    17       7       6     2.5279      0.0639  no significativo
              Service F1  30    11       8      11     1.6875      0.6476  no significativo
B · oracle_gt Edge F1     30    27       1       2    25.3154      0.0000     significativo
              Service F1  30    26       0       4    13.5692      0.0000     significativo
```

**Service F1:**
```text
Service F1 — brazo A vs produccion: +0.72 pts (0.41x MDE)
```
- "En Service F1 el brazo A tampoco se despega. Identificar qué servicios hay en la pizarra no es donde el sistema pierde."

**Qué autoriza a afirmar este notebook:**
- "Dar el ground truth como entrada produce un efecto muy por encima del umbral."
- "Sustituir la etapa perceptual por una transcripción humana no produce mejora detectable."
- "De ahí se sigue que el límite no está en la fidelidad con que se lee la pizarra."

**Qué no autoriza a afirmar:**
- "que las dos condiciones sean equivalentes: el brazo A tiene una sola corrida."

## Limitaciones
- "Producción tiene 4 réplicas y el oráculo 2; el brazo A tiene una sola corrida. Por eso su afirmación es *no distinguible del ruido*, que es más débil que *igual*."
