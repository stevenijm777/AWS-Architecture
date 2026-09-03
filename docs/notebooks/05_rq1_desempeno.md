*Fecha: 2026-09-02*
*Hash (SHA-256): ceb687573a787daf258166f6434a7630a5e93d21eadd92868356cceeb3ec18a6*

## Propósito
Cuantifica la asimetría de precisión en la recuperación de servicios versus topología (aristas), analizando el error y comparando el desempeño pareado entre Standard y Parsimonious.
**Artefacto producido:** `results/rq1_desempeno.json`.

## Entradas
- Archivos de resultados de las corridas de los pipelines Standard y Parsimonious.

## Compuertas
*(Ninguna `assert` explícita en este notebook).*

## Método
- **Métrica Tamaño de efecto (Â₁₂):** "probabilidad de que un video puntúe mejor con un brazo que con el otro; 0.5 es ausencia de efecto".
- **Remuestreo:** "El bootstrap remuestrea videos completos: el diseño es pareado y remuestrear cada brazo por separado rompería el apareamiento."

## Resultados

**Muestra pareada:** `n = 321`

**La asimetría:**
```text
            Standard  Parsimonious  brecha
Service F1     86.78         85.73    1.05
Edge F1        59.65         57.01    2.64

Asimetria dentro de Standard    : 27.13 puntos
Asimetria dentro de Parsimonious: 28.72 puntos
```

**Precision y recall:**
```text
           Standard  Parsimonious
Service P     88.61         85.82
Service R     85.70         86.21
Edge P        70.36         68.27
Edge R        53.99         51.44

En aristas la precision supera claramente al recall en los dos pipelines:
  Standard       P = 70.36   R = 53.99   P - R = +16.37
  Parsimonious   P = 68.27   R = 51.44   P - R = +16.83
```
- "Lo que produce tiende a ser correcto; el problema es lo que NO produce."

**Subdibujado:**
```text
         generadas Standard  generadas Parsimonious  ground truth  ratio S/GT
nodos                  9.15                    9.33          9.11        1.01
aristas                9.04                    8.83         12.42        0.73

diferencia media por video (Standard - GT):
  nodos   : +0.05   (MDE 0.34)  -> dentro del ruido
  aristas : -3.38   (MDE 0.73)  -> SENAL
```

**Comparación pareada Standard contra Parsimonious:**
```text
            Standard  Parsimonious  delta (P-S)  IC95 +-  gana P  gana S  empata  p (signos)
metrica                                                                                     
Service F1   86.7796       85.7278      -1.0518   0.9009      68      94     159      0.0492
Edge F1      59.6483       57.0092      -2.6391   1.5156      90     147      84      0.0003
```

**Tamaño de efecto (Â₁₂):**
```text
            Â₁₂ (Standard > Parsimonious)          IC 95%        magnitud  IC incluye 0.5
métrica                                                                                  
Service F1                          0.524  [0.499, 0.549]  insignificante            True
Edge F1                             0.536  [0.513, 0.559]  insignificante           False
```
- "Las dos magnitudes son insignificantes. En servicios el IC incluye 0.5, asi que no hay efecto establecido; en aristas lo excluye, pero Â₁₂ = 0.536 significa que Standard gana en el 53.6 % de los videos: detectable y practicamente irrelevante."
- "Es exactamente el caso que Arcuri advierte cuando se reporta un p sin tamaño de efecto — y el que sostiene que la afirmacion de RQ1 sea partida y no una paridad."

## Limitaciones
- "Los dos brazos difieren en arquitectura de sistema, no solo en el texto del prompt: dos llamadas con esquema forzado y reintentos contra una llamada con JSON parseado a mano. Ese confound se declara y no se corrige."
