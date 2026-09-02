# ¿Cuánto distorsiona nuestro error de extracción las conclusiones?

Hay **385 arquitecturas** donde existen las dos versiones: la anotada a mano por UW–Madison y la que extrajo nuestro pipeline. Se corrió el análisis de Santillán y Abad sobre cada una por separado.

Mismos videos, mismo código, misma clasificación automática. Lo único que cambia es **quién leyó la pizarra**. Toda diferencia de este documento es error de extracción propagado a las conclusiones — no es un F1, es el efecto de ese F1 sobre lo que un investigador publicaría.

**Reproducir:** `python scripts/santillan_abad/error_propagation.py`

## Clasificación HPC / edge

| Grupo | anotación humana | extracción automática | Δ |
| :--- | ---: | ---: | ---: |
| HPC | 11 (2.9 %) | 12 (3.1 %) | +1 |
| Edge | 98 (25.5 %) | 89 (23.1 %) | -9 |
| Edge+HPC | 4 (1.0 %) | 3 (0.8 %) | -1 |
| None | 272 (70.6 %) | 281 (73.0 %) | +9 |

**Coincidencia arquitectura por arquitectura: 365/385 (94.8 %).** Es el número que importa: no que los totales se parezcan, sino que cada arquitectura caiga en el mismo grupo.

Las 20 que no coinciden:

| Video | humano | automático |
| :--- | :--- | :--- |
| `2e3vOxsHekE` | Edge | None |
| `3yJZ6rPoZfg` | Edge | None |
| `4-teOQ_dJvY` | Edge | None |
| `6iK4WNj6QqI` | None | Edge |
| `PoYiSKUy8sE` | Edge | None |
| `QnwfcDZkwh8` | Edge | None |
| `QuyZHin9B70` | None | Edge |
| `TTlyNWh0gjM` | None | Edge |
| `XGVWdSnml6A` | Edge+HPC | HPC |
| `_vjB_vF4Uec` | Edge | None |
| `aOZ4H98XROc` | Edge | None |
| `c-1GXhOOOww` | None | Edge |
| `c863uNkF0w4` | Edge | None |
| `dWCQw_KvlYQ` | Edge | None |
| `hMK2NJ-q9nc` | Edge | None |
| `lTSZT10JMQA` | Edge | None |
| `lcLw-Le_tXQ` | None | Edge |
| `mKZw29_UtoU` | Edge | None |
| `mmM_JnYygZM` | Edge | None |
| `wtl7CrSQnHA` | Edge | None |

Direcciones del desacuerdo: **Edge → None** 14 · **None → Edge** 5 · **Edge+HPC → HPC** 1.

## Servicios más frecuentes (RQ1–RQ2)

Lo que un lector se lleva del paper es el ranking, no el conteo exacto. La pregunta útil es si el ranking sobrevive.

### HPC — 7/10 servicios en común en el top 10

| # | humano | | automático | |
| ---: | :--- | ---: | :--- | ---: |
| 1 | EC2 | 9 | S3 | 11 |
| 2 | S3 | 8 | EC2 | 10 |
| 3 | ThirdParty | 7 | FSX | 7 |
| 4 | FSX | 5 | Lambda | 5 |
| 5 | Lambda | 5 | ThirdParty | 5 |
| 6 | EKS | 4 | EKS | 4 |
| 7 | Batch | 4 | Batch | 4 |
| 8 | UserCompanyDataStream | 3 | CloudFormation ⚠ | 3 |
| 9 | UserConsumerWeb | 3 | DynamoDB ⚠ | 3 |
| 10 | UserCompanyAnalyst | 3 | ECR ⚠ | 2 |

### Edge — 8/10 servicios en común en el top 10

| # | humano | | automático | |
| ---: | :--- | ---: | :--- | ---: |
| 1 | S3 | 76 | S3 | 69 |
| 2 | Lambda | 58 | Lambda | 53 |
| 3 | CloudFront | 39 | CloudFront | 43 |
| 4 | DynamoDB | 38 | DynamoDB | 35 |
| 5 | ApiGateway | 32 | ThirdParty | 33 |
| 6 | EC2 | 32 | EC2 | 29 |
| 7 | ThirdParty | 31 | ApiGateway | 26 |
| 8 | UserConsumerWeb | 26 | RDS ⚠ | 21 |
| 9 | UserConsumerMobile | 24 | UserConsumerMobile | 18 |
| 10 | UserConsumerEdge | 20 | UserConsumerWebMobile ⚠ | 17 |

### Edge+HPC — 8/10 servicios en común en el top 10

| # | humano | | automático | |
| ---: | :--- | ---: | :--- | ---: |
| 1 | CloudFront | 3 | CloudFront | 3 |
| 2 | S3 | 3 | Lambda | 3 |
| 3 | Lambda | 3 | S3 | 2 |
| 4 | EC2 | 2 | UserConsumerWebMobile | 1 |
| 5 | Aurora | 2 | StepFunctions | 1 |
| 6 | StepFunctions | 1 | AutoScaling ⚠ | 1 |
| 7 | UserConsumerWebMobile | 1 | ApiGateway | 1 |
| 8 | SQS | 1 | CloudWatch | 1 |
| 9 | ApiGateway | 1 | SQS | 1 |
| 10 | CloudWatch | 1 | RDS ⚠ | 1 |

### None — 9/10 servicios en común en el top 10

| # | humano | | automático | |
| ---: | :--- | ---: | :--- | ---: |
| 1 | S3 | 164 | S3 | 171 |
| 2 | Lambda | 149 | Lambda | 155 |
| 3 | ThirdParty | 112 | ThirdParty | 140 |
| 4 | EC2 | 106 | EC2 | 108 |
| 5 | DynamoDB | 79 | DynamoDB | 81 |
| 6 | ApiGateway | 61 | ApiGateway | 67 |
| 7 | UserConsumerWeb | 56 | RDS | 60 |
| 8 | RDS | 56 | SQS | 51 |
| 9 | SQS | 51 | EKS | 45 |
| 10 | EKS | 45 | ECS ⚠ | 43 |

## Servicios por arquitectura (Fig. 5)

| Grupo | media humana | media automática | Δ |
| :--- | ---: | ---: | ---: |
| HPC | 8.09 | 7.67 | -0.42 |
| Edge | 8.43 | 8.38 | -0.05 |
| Edge+HPC | 7.75 | 8.33 | +0.58 |
| None | 7.13 | 7.07 | -0.06 |

## Almacenamiento (RQ3)

| | Block | File | Hybrid | NoSQL | Object | SQL | Specialized |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Edge | 0.0 → 1.1 | 1.0 → 0.0 | 3.1 → 3.4 | 49.0 → 50.6 | 77.5 → 77.5 | 27.6 → 31.5 | 7.1 → 7.9 |
| HPC | 0.0 → 0.0 | 54.5 → 66.7 | 0.0 → 0.0 | 36.4 → 33.3 | 72.7 → 91.7 | 27.3 → 25.0 | 9.1 → 8.3 |
| Edge+HPC | 0.0 → 0.0 | 25.0 → 0.0 | 0.0 → 0.0 | 25.0 → 33.3 | 75.0 → 66.7 | 50.0 → 66.7 | 0.0 → 0.0 |
| None | 2.9 → 2.5 | 1.5 → 1.4 | 0.0 → 0.0 | 36.0 → 36.6 | 60.3 → 60.9 | 31.6 → 32.7 | 12.5 → 12.1 |

## Machine learning (RQ4)

| | con_ML | total | porcentaje |
| :--- | ---: | ---: | ---: |
| Edge | 19.0 → 15.0 | 98.0 → 89.0 | 19.4 → 16.9 |
| Edge+HPC | 1.0 → 1.0 | 4.0 → 3.0 | 25.0 → 33.3 |
| HPC | 2.0 → 2.0 | 11.0 → 12.0 | 18.2 → 16.7 |
| None | 45.0 → 49.0 | 272.0 → 281.0 | 16.5 → 17.4 |

## Cómo leer esto

Este documento **no valida el pipeline** — para eso está el F1 contra el ground truth. Valida algo distinto y más útil para el artículo: si los errores del pipeline **cambian las conclusiones** que se publicarían.

Un pipeline puede tener 86 % de F1 y aun así reproducir el ranking de servicios entero, si los errores se reparten en la cola. O puede tener el mismo 86 % y romper el ranking, si se concentran en los servicios frecuentes. La diferencia importa y el F1 solo no la distingue.

Límite de este análisis: cubre lo que depende del **conjunto de servicios**. No cubre workflows (RQ7), que dependen de las aristas, donde el pipeline mide 59.7 % de F1 contra 86.8 % en servicios.
