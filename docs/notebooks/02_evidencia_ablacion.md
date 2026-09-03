*Fecha: 2026-09-02*
*Hash (SHA-256): 3c6744a30c07c3d3bc68c149330c213d152402769507dfeee526e6f0fa697e33*

## Propósito
Compara 11 prompts distintos sobre el mismo panel mediante 55 comparaciones pareadas, utilizando los umbrales del notebook 01 para decidir qué diferencias son detectables.
**Artefacto producido:** Ninguno.

## Entradas
- Archivos leídos: `results/piso_ruido_panel30.json` (constantes base) y las corridas de la ablación en `results/ablation/*/run.json`.

## Compuertas
*(Ningún `assert` fue utilizado en este notebook)*.

## Método
- **Métrica Rango:** Definida operativamente como la amplitud total entre el mejor y el peor prompt para una misma métrica ($Rango = Max - Min$). "El veredicto es sobre el RANGO, no sobre ninguna comparacion en particular: dice si el diseno tiene resolucion suficiente para que valga la pena mirar, no si hay una diferencia real."
- **Métrica $\hat{A}_{12}$ de Vargha y Delaney:** "la probabilidad de que un video puntúe mejor con el prompt A que con el B, contando empates como medio". 
- **Intervalo de Confianza (IC) del $\hat{A}_{12}$:** "El intervalo de confianza es lo que distingue no hay efecto de no hay potencia: un IC angosto centrado en 0.5 es evidencia de ausencia."

## Resultados

**Umbrales cargados de `piso_ruido_panel30.json` (generado 2026-09-03T03:49:26):**
```text
                   sigma_d  MDE n=30
Edge F1               6.43      3.29
Service F1            3.45      1.76
aristas generadas     1.42      0.73
nodos generados       0.66      0.34
svc alucinados        0.41      0.21
svc faltantes         0.21      0.11
```

**11 prompts distintos (SHA-256), 14 corridas sobre los 30 videos (comparaciones por pares: 55):**
```text
                                         réplicas  Edge F1  Service F1  aristas generadas  nodos generados  svc alucinados  svc faltantes
condicion                                                                                                                                
STAGE2_V7_RETURN_FLOWS_V6 · 7ad8d936            1    60.10       88.07               9.73             8.90            0.73           1.00
STAGE2_V6_OPTIMIZED · 079b0aa8                  1    59.14       86.75               8.97             9.00            0.87           1.03
STAGE2_V7_RETURN_FLOWS · 1ed4ebf9               1    58.65       86.91              10.17             9.23            0.93           0.90
STAGE2_V5_STRICT_ROUTING · a792c132             1    58.45       86.78               8.70             8.97            0.87           1.03
STAGE2_V8_ACTORS_AND_RETURNS · 277020ba         1    58.40       86.21               9.97             9.07            0.97           1.07
STAGE2_V6_CORRECTED · ed1d8505                  4    58.13       87.10               9.03             8.89            0.82           1.03
STAGE2_V6_CORRECTED · dbddf1f3                  1    58.10       88.47               9.47             9.10            0.77           0.87
STAGE2_V5_STRICT_ROUTING · 53f8d912             1    58.08       86.65               9.37             9.07            0.90           0.97
STAGE2_V6_CORRECTED · 7228956f                  1    57.52       85.92               9.37             8.97            0.93           1.07
STAGE2_V4_ANTI_HALLUCINATION · cdb8998f         1    57.10       85.62               8.67             9.07            1.03           1.07
STAGE2_V4_DYNAMIC_FEW_SHOT · 45da674e           1    56.49       88.03               9.33             8.83            0.77           0.90
```

**¿El rango cabe dentro del ruido?**
```text
                   mejor   peor  rango  MDE n=30  rango / MDE                  veredicto
metrica                                                                                 
Edge F1            60.10  56.49   3.61      3.29         1.10  el rango excede el umbral
Service F1         88.47  85.62   2.84      1.76         1.61  el rango excede el umbral
aristas generadas  10.17   8.67   1.50      0.73         2.07  el rango excede el umbral
nodos generados     9.23   8.83   0.40      0.34         1.18  el rango excede el umbral
svc alucinados      1.03   0.73   0.30      0.21         1.42  el rango excede el umbral
svc faltantes       1.07   0.87   0.20      0.11         1.86  el rango excede el umbral
```

**Comparaciones por pares (métrica Edge F1):**
```text
— lo que Arcuri y Briand piden que se reporte primero —
  significativas SIN corregir       : 3/55
  Â₁₂ rango                          : 0.452 – 0.553
  magnitudes de efecto              : {'insignificante': 55}
  IC de Â₁₂ que incluye 0.5          : 55/55
  ancho medio del IC                : 0.110

— control de robustez, no el argumento —
  P(al menos un falso positivo sin corregir) = 94.0%
  significativas con Bonferroni     : 0   (umbral p < 0.00091)
  significativas con Holm           : 0

                         A                       B  dif medias  gana A  gana B  empata  p crudo     Â₁₂  IC bajo  IC alto        magnitud  IC incluye 0.5  signif. sin corregir  signif. Holm
46     STAGE2_V6_OPTIMIZED     STAGE2_V6_CORRECTED      1.6211      13       2      15   0.0074  0.5239   0.4950   0.5633  insignificante            True                  True         False
49  STAGE2_V7_RETURN_FLOWS     STAGE2_V6_CORRECTED      2.5844      15       3      12   0.0075  0.5456   0.4994   0.6061  insignificante            True                  True         False
6   STAGE2_V4_ANTI_HALLUCI  STAGE2_V7_RETURN_FLOWS     -2.9997       3      13      14   0.0213  0.4517   0.3772   0.5150  insignificante            True                  True         False
5   STAGE2_V4_ANTI_HALLUCI     STAGE2_V6_OPTIMIZED     -2.0363       3      11      16   0.0574  0.4728   0.4244   0.5133  insignificante            True                 False         False
42  STAGE2_V5_STRICT_ROUTI     STAGE2_V6_CORRECTED      0.9392      10       3      17   0.0923  0.5228   0.4889   0.5672  insignificante            True                 False         False
23  STAGE2_V5_STRICT_ROUTI  STAGE2_V7_RETURN_FLOWS     -2.0188       5      13      12   0.0963  0.4667   0.4044   0.5256  insignificante            True                 False         False
50  STAGE2_V7_RETURN_FLOWS     STAGE2_V6_CORRECTED      2.0010      11       4      15   0.1185  0.5272   0.4911   0.5700  insignificante            True                 False         False
3   STAGE2_V4_ANTI_HALLUCI  STAGE2_V8_ACTORS_AND_R     -1.3025       4      10      16   0.1796  0.4794   0.4161   0.5333  insignificante            True                 False         False
4   STAGE2_V4_ANTI_HALLUCI  STAGE2_V5_STRICT_ROUTI     -1.3544       2       7      21   0.1797  0.4767   0.4311   0.5122  insignificante            True                 False         False
22  STAGE2_V5_STRICT_ROUTI     STAGE2_V6_OPTIMIZED     -1.0555       5      11      14   0.2101  0.4894   0.4350   0.5417  insignificante            True                 False         False
47     STAGE2_V6_OPTIMIZED     STAGE2_V6_CORRECTED      1.0377      11       5      14   0.2101  0.5061   0.4628   0.5500  insignificante            True                 False         False
37  STAGE2_V8_ACTORS_AND_R     STAGE2_V6_CORRECTED      0.8873      11       5      14   0.2101  0.5217   0.4744   0.5761  insignificante            True                 False         False
```
*(Nota: la salida impresa por la celda limitaba la visualización a las top 12 comparaciones)*.

**Lo que el Edge F1 esconde:**
```text
Edge F1          : rango 3.61  vs MDE 3.29  -> 1.10x el umbral
aristas generadas: rango 1.50  vs MDE 0.73  -> 2.07x el umbral

aristas, extremo vs extremo: Â₁₂ = 0.622 [0.558, 0.700] · pequeño
```

**El oráculo contra producción (Produccion promedia 2 replicas, oraculo 2):**
```text
                   produccion  oraculo   delta  MDE n=30  veces el MDE    Â₁₂          IC 95%        magnitud
metrica                                                                                                      
Edge F1                58.425   82.172  23.747     3.288         7.223  0.856  [0.788, 0.924]          grande
Service F1             87.549   99.569  12.020     1.764         6.813  0.906  [0.829, 0.975]          grande
aristas generadas       9.067    9.967   0.900     0.726         1.239  0.597  [0.522, 0.682]         pequeño
nodos generados         8.917    8.733  -0.183     0.339        -0.541  0.479  [0.403, 0.552]  insignificante
svc alucinados          0.800    0.017  -0.783     0.212        -3.697  0.155  [0.071, 0.241]          grande
svc faltantes           1.000    0.033  -0.967     0.108        -8.970  0.178  [0.092, 0.267]          grande
```

**Qué se puede afirmar:** *(Conclusiones declaradas explícitamente e impresas por la celda 12 de texto)*
- "Ninguna diferencia entre prompts es detectable. Los 55 tamaños de efecto son insignificantes y sus intervalos, angostos, contienen el 0.5."
- "El oráculo mejora muy por encima del MDE, con el test de signos y el tamaño de efecto coincidiendo."
- "Los prompts difieren de forma detectable en cuántas aristas dibujan, no en Edge F1."
- "Todos subdibujan aristas respecto del ground truth."

**Qué no se puede afirmar:**
- "que un prompt sea mejor que otro, ni que las variantes sean equivalentes. El IC acota cuánto podría estar escondido sin llevarlo a cero."

## Limitaciones
- "De los 11 prompts, sólo uno tiene réplicas. Arcuri y Briand recomiendan del orden de 1000 corridas por condición y GenProg reporta 100; acá hay entre 1 y 4, y la diferencia es de costo: cada corrida son 30 llamadas a una API con cuota de 20 por día."
