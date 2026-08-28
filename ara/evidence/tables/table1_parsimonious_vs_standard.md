# Tabla 1 · Parsimonious vs Standard — comparación pareada

**Fuente:** `reports/runs/2026-08-21_parsimonious_v9/results.csv` y `reports/runs/2026-08-20_standard_v6corrected_370v/results.csv`.
**Reproducir:** `.venv/bin/python scripts/ablation/build_evidence_tables.py`

Parsimonious evaluó 385 videos y Standard 370; comparten **370**. De esos, **321** produjeron un grafo utilizable en los dos pipelines y forman la muestra pareada. Cada video aporta una diferencia, así que la comparación controla por dificultad del video: no se comparan dos promedios sobre corpus distintos.

## Resultado principal

| Métrica | n | Parsimonious | Standard | Δ (P − S) | sd de la dif. | IC 95 % | t | p (t) |
| :--- | ---: | ---: | ---: | ---: | ---: | :---: | ---: | ---: |
| F1 de servicios | 321 | 85.73 % | 86.78 % | **-1.05** | 8.24 | [-1.95, -0.15] | -2.29 | 0.0221 |
| F1 de aristas | 321 | 57.01 % | 59.65 % | **-2.64** | 13.85 | [-4.15, -1.12] | -3.41 | 0.0006 |

| Métrica | gana Parsimonious | gana Standard | empata | p signos | p Wilcoxon |
| :--- | ---: | ---: | ---: | ---: | ---: |
| F1 de servicios | 68 | 94 | 159 | 0.04917 | 0.06606 |
| F1 de aristas | 90 | 147 | 84 | 0.00026 | 0.00006 |

## Lectura

1. **En servicios los dos pipelines son equivalentes.** La diferencia es de -1.05 puntos y las dos pruebas no paramétricas divergen (signos p = 0.049, Wilcoxon p = 0.066). Con 159 empates de 321 la distribución de diferencias está lejos de la normal, así que la t pareada no es la prueba que gobierna: **la diferencia en servicios no queda establecida**.
2. **En aristas gana Standard, y eso sí es sólido.** -2.64 puntos, IC 95 % [-4.15, -1.12], con signos p = 0.00026 y Wilcoxon p = 0.00006. Las dos pruebas coinciden y el intervalo no toca el cero.
3. **La afirmación defendible es partida, no una paridad.** «Parsimonious rinde igual a la mitad del costo» vale para servicios y **no** vale para topología.

### El punto metodológico

Esos 2.64 puntos de aristas son **reales a n = 321 e invisibles a n ≤ 30**. Con el piso de ruido medido del proyecto (`reports/noise_floor.json`, σ_d = 8.76 puntos de Edge F1 por video) el efecto mínimo detectable con 30 videos es de 4.48 puntos y con 14 videos de 6.56. Toda la fase de selección de prompts, en los dos brazos, operó por debajo de su propio umbral de detección: la comparación central del proyecto es ella misma un caso del problema metodológico que este trabajo reporta.

## Muestra por video

15 videos tomados al azar de los 321 con `random.Random(20260827).sample(...)` — semilla fija y declarada, para que cualquiera reproduzca exactamente estas filas. **No es una selección hecha a mano.** El detalle completo de los 321 está en los dos `results.csv` citados arriba.

| Video ID | Svc F1 Parsimonious | Svc F1 Standard | Edge F1 Parsimonious | Edge F1 Standard |
| :--- | ---: | ---: | ---: | ---: |
| `-3lnf5lzsH0` | 95.7 % | 80.0 % | 64.3 % | 32.0 % |
| `4zVB5RbSTCo` | 100.0 % | 94.1 % | 72.7 % | 60.0 % |
| `Eoq7E6jMtBs` | 94.7 % | 94.7 % | 45.2 % | 54.5 % |
| `HcmEFZukA-Y` | 100.0 % | 100.0 % | 66.7 % | 88.9 % |
| `Ly_UhX3LCCs` | 100.0 % | 88.9 % | 47.1 % | 42.9 % |
| `MbkLJ62jtMc` | 71.4 % | 76.9 % | 54.5 % | 60.0 % |
| `OrC9cLYMbas` | 83.3 % | 90.9 % | 18.2 % | 36.4 % |
| `aY-wF9g0qkM` | 76.9 % | 76.9 % | 43.5 % | 52.2 % |
| `cZuoiXQ0xUk` | 85.7 % | 85.7 % | 47.6 % | 47.6 % |
| `ccPhkyPm_3w` | 83.3 % | 83.3 % | 33.3 % | 57.1 % |
| `lkDq9g43djw` | 100.0 % | 100.0 % | 50.0 % | 75.0 % |
| `mq3XuoN0rUM` | 94.1 % | 82.3 % | 47.6 % | 43.5 % |
| `nflGdpwbf54` | 87.5 % | 87.5 % | 66.7 % | 66.7 % |
| `sSa4ikC8-Jc` | 80.0 % | 100.0 % | 42.4 % | 55.6 % |
| `yPJf85tjv6M` | 94.1 % | 94.1 % | 69.6 % | 60.9 % |

## Nota de corrección

Una versión anterior de esta tabla publicaba **16 filas de las 60** de `reporte_comparacion_detallada.md`, elegidas sin criterio declarado. El recorte invertía el signo del resultado: en las 60 filas de la fuente Standard ganaba 28 a 8, mientras que en las 16 publicadas ganaba Parsimonious 4 a 3. Además 4 de esas 16 filas ya no coincidían con el corpus vigente y **las cuatro discrepaban a favor de Parsimonious** (`-kA0ahrhX3I` 100 → 71.43, `6EUknQqaV1w` 100 → 92.31, `AzM_d7ZvzUE` 100 → 87.50, `BlCXEMp_lqY` 100 → 83.33). El archivo fuente describe un corpus que ya no existe: 27 de sus 60 filas difieren del `results.csv` actual en al menos una columna.

Esta versión se calcula sobre la población completa de videos comparables y reporta la prueba pareada, que es lo que la afirmación necesitaba desde el principio.

### Limitación que no se puede reparar hacia atrás

El prompt de producción de Parsimonious (v9) se adoptó mirando **un solo video** (`-3lnf5lzsH0`, Registro 17 de la bitácora), que además era la fila estrella de la versión anterior de esta tabla («Parsimonious +15.7 %»). Con el piso de ruido medido, el efecto mínimo detectable con n = 1 es de 26.3 puntos de Service F1 y 33.3 de Edge F1: esa decisión no fue medible. El prompt se eligió y se reportó su rendimiento sobre el mismo dato. No es corregible retroactivamente sin volver a correr la selección, y queda declarado como limitación.
