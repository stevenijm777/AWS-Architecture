*Fecha: 2026-09-02*
*Hash (SHA-256): 724981b32797488697bb968a3fc85de00cd5a2c6964daa2586946efbb83b6c47*

## Propósito
Mide si los errores de la extracción automática se propagan lo suficiente como para alterar las conclusiones publicadas por la tarea downstream de Santillán y Abad (clasificación en HPC/Edge).
**Artefacto producido:** `results/rq5_tarea_downstream.json`.

## Entradas
- Clasificaciones generadas por el script downstream sobre los corpus: `run_local`, `run_gt385`, `run_extracted385`, `run_extended`.

## Compuertas
- El notebook verifica que la ejecución local sobre el dataset original reproduzca la Tabla I del paper publicado:
  `OK · la corrida base reproduce la Tabla I del paper exacto.`
  `Cualquier diferencia de aca en adelante es atribuible al cambio de corpus, no a la ejecucion.`

## Método
- Se ejecuta la misma lógica de clasificación sobre la anotación humana (`run_gt385`) y sobre la extracción automática (`run_extracted385`).

## Resultados

**Compuerta de reproducción:**
```text
          nuestra corrida  Tabla I publicada  coincide
None                  280                280      True
Edge                  101                101      True
HPC                    11                 11      True
Edge+HPC                4                  4      True
```

**Coincidencia de clasificación:**
```text
arquitecturas pareadas : 385
misma clasificacion    : 365  (94.8 %)
desacuerdos            : 20

          anotacion humana  extraccion automatica  Δ  % humano
tipo                                                          
HPC                     11                     12  1       2.9
Edge                    98                     89 -9      25.5
Edge+HPC                 4                      3 -1       1.0
None                   272                    281  9      70.6
```

**Dirección de los desacuerdos:**
```text
Desacuerdos por direccion:

      Edge  →  None      14
      None  →  Edge      5
  Edge+HPC  →  HPC       1

El pipeline pierde la etiqueta Edge en 14 casos
y la agrega de mas en 5: el sesgo es hacia SUB-clasificar.
```
- "Coherente con el subdibujado de aristas del notebook 05: si faltan servicios o conexiones, faltan tambien las señales que disparan la etiqueta Edge."

**Ranking de servicios:**
```text
======================================================================

          top-10 en comun                                     solo humano                solo automatico
grupo                                                                                                   
HPC                     7  UserCompanyAnalyst, UserCompanyDataStream, Use  CloudFormation, DynamoDB, ECR
Edge                    8               UserConsumerEdge, UserConsumerWeb     RDS, UserConsumerWebMobile
Edge+HPC                8                                     Aurora, EC2               AutoScaling, RDS
None                    9                                 UserConsumerWeb                            ECS
```
- "El ranking se preserva en la mayoría de las posiciones de los cuatro grupos. Es lo que un lector se lleva del artículo, y sobrevive a la sustitución."

**Servicios por arquitectura:**
```text
          humano  automatico     Δ
tipo                              
HPC         8.09        7.67 -0.42
Edge        8.43        8.38 -0.05
Edge+HPC    7.75        8.33  0.58
None        7.13        7.07 -0.06

Desviacion maxima: 0.58 servicios por arquitectura.
La conclusion cualitativa del paper —que los cuatro grupos rondan los 7-8 servicios—
se mantiene con cualquiera de los dos corpus.
```

**Arquitecturas que el pipeline agrega:**
```text
arquitecturas nuevas: 61

             nuevas
anio_video        
2020.0           9
2021.0           6
2022.0          11
2023.0           2
2024.0          33

Las 33 de 2024 son el hueco temporal que el dataset original no cubre:
un corpus curado a mano queda desactualizado, uno extraido automaticamente se re-corre.

          396 publicado  457 actualizado  Δ puntos %
tipo                                                
HPC                  11               12        -0.2
Edge                101              125         1.8
Edge+HPC              4                4        -0.1
None                280              316        -1.6
```

## Limitaciones
- "Solo lo que depende del conjunto de servicios. Su análisis de workflows depende de aristas, y se mide aparte en el notebook 13."
- "El clasificador es una compuerta de presencia simple: perder un solo servicio disparador voltea la etiqueta. La coincidencia se mide bajo ese peor caso, no bajo uno benigno."
