*Fecha: 2026-09-02*
*Hash (SHA-256): 69a1af0a29184494be712c3388c66d7b47f3326f2fb58997c9c21be8301ca3f6*

## Propósito
Descompone cada arista perdida en su causa raíz para identificar y medir los fenómenos estructurales que dominan el subdibujado de la topología.
**Artefacto producido:** `results/anatomia_aristas.json`.

## Entradas
- Corrida `2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4`.

## Compuertas
*(Ninguna `assert` explícita en este notebook).*

## Método
- Para cada arista del ground truth no producida, se asigna una causa excluyente:
  - **Falta un nodo:** el servicio no está en el grafo.
  - **Falta el retorno:** el modelo produjo `a→b` y el ground truth tiene también `b→a`.
  - **Sin conexión:** los dos nodos están presentes pero no se conectaron.

## Resultados

**Por qué se pierde cada arista:**
```text
corrida: 2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4
videos : 30
aristas generadas: 271 · en el GT: 361

                                     aristas     %
causa                                             
falta la arista de RETORNO                81  44.8
falta un nodo                             61  33.7
ambos nodos presentes, sin conexion       39  21.5

aristas del GT     : 361
aristas perdidas   : 181 (50.1%)
```
- "La causa dominante es la arista de retorno: el modelo conecta `a→b` correctamente y no produce `b→a`, que el ground truth sí tiene."

**Qué nodos ausentes cuestan más aristas:**
```text
                       aristas que arrastra
extremo_ausente                            
UserConsumerWeb                          22
ThirdParty                               10
UserCompanyDataStream                     6
UserCompanyAgent                          5
MSK                                       3
UserCompanyDeveloper                      3
UserConsumerAPI                           2
UserConsumerMobile                        2
SNS                                       1
SQS                                       1
GuardDuty                                 1
OnPremDC                                  1

aristas perdidas por nodo ausente         : 61
  ... cuyo extremo ausente es User*/ThirdParty: 53 (87%)

Los actores humanos y sistemas externos son los nodos que mas aristas cuestan
cuando faltan. El prompt de produccion los PODA explicitamente (regla 5).
```

**La brecha de bidireccionalidad:**
```text
% medio de pares bidireccionales
  ground truth : 52.6%
  produccion   : 15.1%
  brecha       : 37.5 puntos
```

**Cuánto valdría acertar la dirección:**
```text
Edge F1 dirigido (estricto) : 57.87
Edge F1 no dirigido (techo) : 69.58
la direccion cuesta          : 11.72 puntos
```

## Limitaciones
- Ninguna declarada explícitamente en el output computado como sección formal. El texto sí señala como precisión analítica que "Las dos primeras causas [falta el retorno y la ausencia de actores] son ontológicas y no perceptuales: dependen de convenciones de anotación, no de lo que se ve en la pizarra".
