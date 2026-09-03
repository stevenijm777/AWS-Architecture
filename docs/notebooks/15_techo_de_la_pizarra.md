*Fecha: 2026-09-02*
*Hash (SHA-256): 6f6c62f325585699449043142b79eb0f4907957f80c4b8a647b1a75bbc51197c*

## Propósito
Mide de forma directa el techo teórico de lo que la pizarra contiene visualmente (puntuando a humanos contra el ground truth sin pasar por la etapa 2) y cuantifica la incertidumbre de calibración de las varianzas experimentales.
**Artefacto producido:** Ninguno impreso.

## Entradas
- 30 transcripciones humanas `world_models` manuales y datos de calibración del panel.

## Compuertas
- `etiquetas de conexión sin resolver: 0/259` (`Compuerta pasada. n = 30 pizarras.`)

## Método
- Las transcripciones humanas del panel de 30, hechas sin audio ni ground truth, se evalúan contra el ground truth mediante evaluación estricta directa.
- **Incertidumbre de $\sigma_d$:** El bootstrap remuestrea las diferencias pareadas nulas.
- **Cota de la Varianza:** Revisa en los registros de corrida si la etapa 1 fue regenerada.

## Resultados

**El techo de la pizarra (contra el pipeline):**
```text
                                          Svc F1  Edge F1  aristas/arq
quién lee la pizarra                                                  
PERSONA (solo la pizarra, sin etapa 2)     87.36    57.60         8.63
pipeline · producción (4 réplicas)         87.10    58.13         9.03
brazo A · transcripción humana → etapa 2   87.82    60.40          NaN
brazo B · ground truth → etapa 2           99.57    82.17          NaN
ground truth (referencia)                 100.00   100.00        12.03

Una persona leyendo SOLO la pizarra saca 57.60 de Edge F1.
El pipeline completo saca 58.13. Diferencia: -0.54 puntos.

Y el subdibujo es el mismo: la persona anota 8.63 aristas contra 12.03 del ground truth,
un déficit de -3.40 por arquitectura — el pipeline tiene -3,38 sobre el panel de 321.
```
- "No queda margen perceptual. Una persona haciendo la percepción sin errores recupera los servicios como el pipeline y las aristas igual de mal. El techo de lo que la pizarra contiene está donde el sistema ya está. Y la persona también subdibuja, con un déficit por arquitectura casi idéntico."

**Incertidumbre de $\sigma_d$:**
```text
             n  sigma_d    IC sigma_d  MDE n=30        IC MDE
métrica                                                      
Edge F1     90     6.43  [4.73, 8.01]      3.29  [2.42, 4.09]
Service F1  90     3.45  [2.02, 4.59]      1.76  [1.03, 2.35]
El MDE de Edge F1 no es 3,29: es 3,29 con un intervalo de [2,42; 4,10].

Qué cambia en los veredictos ya publicados:
  brazo A · transcripción humana              +2.27 = 0.55x-0.94x MDE  ->  ruido en todo el IC
  brazo B · ground truth de entrada          +24.04 = 5.88x-9.95x MDE  ->  señal en todo el IC
  rango completo de las 11 variantes          +3.61 = 0.88x-1.49x MDE  ->  AMBIGUO: el IC cruza el umbral
```

**Qué etapa mide el piso:**
```text
videos con etapa 1 regenerada en los pares nulos: 0

NINGUNO. Las seis corridas reutilizaron el world model de la etapa 1.
Por lo tanto sigma_d = 6,43 es la varianza de la ETAPA 2 SOLA, y es una
COTA INFERIOR de la varianza del pipeline completo: la etapa perceptual
aporta cero por construccion en estos pares.
```
- "σ_d es una cota inferior de la variabilidad de extremo a extremo. La dirección del sesgo no es simétrica: un umbral mayor refuerza los resultados negativos —el brazo A queda más adentro del ruido y el rango de variantes cae por debajo del umbral— y deja intacto el único positivo."

## Limitaciones
- "Límites. Un solo transcriptor, que además conoce el esquema, de modo que el techo medido es si acaso generoso. Sin segundo anotador y sobre el panel de 30."
- "Medir la varianza de extremo a extremo exige una réplica que regenere la etapa 1."
