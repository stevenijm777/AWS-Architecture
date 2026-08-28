# Actualización del análisis de Santillán y Abad (2025)

Santillán, S. y Abad, C. L. (2025). *An Analysis of HPC and Edge Architectures in the Cloud*. IC2E 2025, pp. 259–266. DOI [10.1109/IC2E65552.2025.00043](https://doi.org/10.1109/IC2E65552.2025.00043). Paquete de reproducibilidad bajo licencia MIT.

El paper analiza las **396 arquitecturas** de Cloudscape, que cubren videos de marzo 2019 a diciembre 2023. Nuestro pipeline extrajo **61 arquitecturas** que ese dataset no tiene. Este documento reporta el análisis de los autores corrido sobre las **457**.

**Método.** Se ejecutó el notebook de los autores sin modificar su lógica. Las dos corridas usan el mismo código; lo único que cambia es el directorio de graphml que leen. Antes de actualizar nada se verificó que la corrida base reproduce el paper publicado: la Tabla I (280/101/11/4) y las medias de workflows de la Fig. 9 (4.0 / 3.3 / 4.5 / 3.1) salen exactas, y los archivos que el notebook regenera coinciden 396/396 con los que los autores publicaron.

**Reproducir:**

```bash
# entorno con versiones fijadas: ver scripts/santillan_abad/requirements.txt
python scripts/santillan_abad/build_extended_corpus.py
python scripts/santillan_abad/make_analysis_notebook.py
python scripts/santillan_abad/run_notebooks.py       # ejecuta las dos variantes
python scripts/santillan_abad/compare_update.py
```

## Qué agregan las arquitecturas nuevas

| Año | Arquitecturas nuevas |
| :--- | ---: |
| 2020 | 9 |
| 2021 | 6 |
| 2022 | 11 |
| 2023 | 2 |
| 2024 | 33 |
| **Total** | **61** |

Las **33 de 2024** son el hueco que el dataset original no cubre. Las de 2020–2023 son videos que la curación manual de Cloudscape no incluyó.

## Prevalencia por tipo (Tabla I y RQ6)

| Grupo | 396 arq. (publicado) | | 457 arq. (actualizado) | | Δ puntos |
| :--- | ---: | ---: | ---: | ---: | ---: |
| HPC | 11 | 2.8 % | 12 | 2.6 % | -0.2 |
| Edge | 101 | 25.5 % | 125 | 27.4 % | +1.8 |
| Edge+HPC | 4 | 1.0 % | 4 | 0.9 % | -0.1 |
| None | 280 | 70.7 % | 316 | 69.1 % | -1.6 |

Sólo entre las nuevas: **HPC** 1 · **Edge** 24 · **Edge+HPC** 0 · **None** 36.

### Conteo absoluto por año

| Año | HPC base → ext | Edge base → ext | Edge+HPC base → ext | None base → ext |
| :--- | ---: | ---: | ---: | ---: |
| 2019 | 1 | 30 | 0 | 78 |
| 2020 | 3 → 4 | 30 → 36 | 2 | 60 → 62 |
| 2021 | 3 | 13 → 14 | 0 | 53 → 58 |
| 2022 | 4 | 19 → 26 | 0 | 58 → 62 |
| 2023 | 0 | 9 → 10 | 2 | 31 → 32 |
| 2024 | 0 | 0 → 9 | 0 | 0 → 24 |

2024 no existe en el análisis publicado. Es la fila que este trabajo agrega.

## Servicios más frecuentes (RQ1–RQ2)

Cuenta en cuántas arquitecturas del grupo aparece cada servicio.

### HPC (11 → 12 arquitecturas)

| # | Publicado | | Actualizado | | Movimiento |
| ---: | :--- | ---: | :--- | ---: | :--- |
| 1 | EC2 | 9 (82 %) | S3 | 9 (75 %) | sube 1 |
| 2 | S3 | 8 (73 %) | EC2 | 9 (75 %) | = |
| 3 | ThirdParty | 7 (64 %) | ThirdParty | 7 (58 %) | = |
| 4 | FSX | 5 (45 %) | Lambda | 6 (50 %) | = |
| 5 | Lambda | 5 (45 %) | FSX | 5 (42 %) | baja 1 |
| 6 | EKS | 4 (36 %) | Batch | 5 (42 %) | sube 1 |
| 7 | Batch | 4 (36 %) | EKS | 4 (33 %) | baja 1 |
| 8 | UserCompanyDataStream | 3 (27 %) | DynamoDB | 4 (33 %) | sube 1 |
| 9 | UserConsumerWeb | 3 (27 %) | UserCompanyDataStream | 3 (25 %) | baja 1 |
| 10 | UserCompanyAnalyst | 3 (27 %) | UserConsumerWeb | 3 (25 %) | baja 1 |

Sale del top 10: UserCompanyAnalyst.

### Edge (101 → 125 arquitecturas)

| # | Publicado | | Actualizado | | Movimiento |
| ---: | :--- | ---: | :--- | ---: | :--- |
| 1 | S3 | 77 (76 %) | S3 | 93 (74 %) | = |
| 2 | Lambda | 61 (60 %) | Lambda | 77 (62 %) | = |
| 3 | CloudFront | 41 (41 %) | CloudFront | 52 (42 %) | = |
| 4 | DynamoDB | 40 (40 %) | ThirdParty | 50 (40 %) | sube 2 |
| 5 | EC2 | 34 (34 %) | DynamoDB | 47 (38 %) | baja 1 |
| 6 | ThirdParty | 33 (33 %) | EC2 | 43 (34 %) | baja 1 |
| 7 | ApiGateway | 32 (32 %) | ApiGateway | 42 (34 %) | = |
| 8 | UserConsumerWeb | 27 (27 %) | UserConsumerWeb | 31 (25 %) | = |
| 9 | UserConsumerMobile | 25 (25 %) | RDS | 30 (24 %) | sube 1 |
| 10 | RDS | 21 (21 %) | UserConsumerMobile | 25 (20 %) | baja 1 |

### Edge+HPC (4 → 4 arquitecturas)

| # | Publicado | | Actualizado | | Movimiento |
| ---: | :--- | ---: | :--- | ---: | :--- |
| 1 | Lambda | 3 (75 %) | CloudFront | 3 (75 %) | = |
| 2 | CloudFront | 3 (75 %) | S3 | 3 (75 %) | = |
| 3 | S3 | 3 (75 %) | Lambda | 3 (75 %) | = |
| 4 | EC2 | 2 (50 %) | EC2 | 2 (50 %) | = |
| 5 | Aurora | 2 (50 %) | Aurora | 2 (50 %) | = |
| 6 | ApiGateway | 1 (25 %) | CloudWatch | 1 (25 %) | = |
| 7 | CloudWatch | 1 (25 %) | ApiGateway | 1 (25 %) | = |
| 8 | StepFunctions | 1 (25 %) | SQS | 1 (25 %) | = |
| 9 | SQS | 1 (25 %) | UserConsumerWebMobile | 1 (25 %) | = |
| 10 | UserConsumerWebMobile | 1 (25 %) | StepFunctions | 1 (25 %) | = |

### None (280 → 316 arquitecturas)

| # | Publicado | | Actualizado | | Movimiento |
| ---: | :--- | ---: | :--- | ---: | :--- |
| 1 | S3 | 165 (59 %) | S3 | 186 (59 %) | = |
| 2 | Lambda | 151 (54 %) | Lambda | 169 (53 %) | = |
| 3 | ThirdParty | 113 (40 %) | ThirdParty | 136 (43 %) | = |
| 4 | EC2 | 107 (38 %) | EC2 | 112 (35 %) | = |
| 5 | DynamoDB | 79 (28 %) | DynamoDB | 92 (29 %) | = |
| 6 | ApiGateway | 62 (22 %) | ApiGateway | 72 (23 %) | = |
| 7 | UserConsumerWeb | 56 (20 %) | RDS | 62 (20 %) | = |
| 8 | RDS | 56 (20 %) | UserConsumerWeb | 58 (18 %) | baja 1 |
| 9 | SQS | 51 (18 %) | EKS | 55 (17 %) | sube 1 |
| 10 | EKS | 45 (16 %) | SQS | 54 (17 %) | baja 1 |

## Servicios por arquitectura (Fig. 5)

| Grupo | media base | media ext | mediana base | mediana ext |
| :--- | ---: | ---: | ---: | ---: |
| HPC | 8.09 | 8.08 | 8.0 | 8.0 |
| Edge | 8.50 | 8.62 | 9.0 | 9.0 |
| Edge+HPC | 7.75 | 7.75 | 8.0 | 8.0 |
| None | 7.04 | 7.04 | 7.0 | 7.0 |

## Almacenamiento (RQ3)

Porcentaje de arquitecturas del grupo que usan cada servicio de almacenamiento.

| | Block | File | Hybrid | NoSQL | Object | SQL | Specialized |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Edge | 0.0 → 0.0 | 1.0 → 1.6 | 3.0 → 2.4 | 49.5 → 48.0 | 76.2 → 74.4 | 28.7 → 32.0 | 6.9 → 7.2 |
| HPC | 0.0 → 0.0 | 54.5 → 50.0 | 0.0 → 0.0 | 36.4 → 41.7 | 72.7 → 75.0 | 27.3 → 25.0 | 9.1 → 8.3 |
| Edge+HPC | 0.0 → 0.0 | 25.0 → 25.0 | 0.0 → 0.0 | 25.0 → 25.0 | 75.0 → 75.0 | 50.0 → 50.0 | 0.0 → 0.0 |
| None | 2.9 → 2.5 | 1.4 → 1.3 | 0.0 → 0.0 | 35.0 → 35.8 | 58.9 → 58.9 | 31.1 → 30.4 | 12.1 → 12.7 |

## Machine learning (RQ4)

Arquitecturas con al menos un servicio de ML.

| | con_ML | total | porcentaje |
| :--- | ---: | ---: | ---: |
| Edge | 19.0 → 24.0 | 101.0 → 125.0 | 18.8 → 19.2 |
| Edge+HPC | 1.0 → 1.0 | 4.0 → 4.0 | 25.0 → 25.0 |
| HPC | 2.0 → 2.0 | 11.0 → 12.0 | 18.2 → 16.7 |
| None | 46.0 → 58.0 | 280.0 → 316.0 | 16.4 → 18.4 |

## Qué NO se actualizó, y por qué

| Análisis | Estado | Razón |
| :--- | :--- | :--- |
| RQ5 — objetivos funcionales | **fuera** | Cloudscape usa un vocabulario controlado (`data_ingestion`, `interactive`, `control`, `compute_intensive`, `other`) y nuestro pipeline genera texto libre. Requiere etiquetar a mano las 61 nuevas. |
| RQ7 — workflows | **fuera** | Depende de las aristas y de `flow_id`. Nuestro pipeline mide 59.7 % de F1 en aristas contra 86.8 % en servicios: publicar una distribución de workflows construida sobre eso sería publicar ruido. |
| Fig. 2 — industrias | **fuera** | El dato de industria no está en el paquete de reproducibilidad de los autores; lo hicieron a mano y no lo publicaron. La celda falla con su propio `assert len(df_meta) == 396`. |
| §III-G — clustering k-means | **fuera** | No es reproducible: da resultados distintos entre dos corridas consecutivas en la misma máquina, porque el orden de entrada no está fijado. |

## Limitaciones de esta actualización

1. **Las arquitecturas nuevas no recibieron curación manual.** Los autores clasifican por lista de servicios y después corrigen a mano: sobre las 396, el clasificador automático da HPC 8, Edge 100, Edge+HPC 1, y la curación manual lo lleva a 11 / 101 / 4. Las 61 nuevas sólo pasaron por el clasificador automático, así que es esperable que estén **sub-clasificadas** como HPC y Edge+HPC respecto de las originales.
2. **Las arquitecturas nuevas son extracción automática, no anotación humana.** Las 396 originales las anotó a mano un equipo de UW–Madison; las 61 nuevas salen de nuestro pipeline, con F1 de servicios de 86.8 % medido contra ese mismo ground truth. Todo número de este documento mezcla 396 filas curadas a mano con 61 filas extraídas automáticamente, y el error de extracción afecta a esas últimas.
3. **Ningún servicio de las nuevas cae fuera del catálogo de Cloudscape**, lo cual acota el punto anterior en la dimensión que más importa acá: no hay nombres inventados contaminando los conteos de frecuencia.
