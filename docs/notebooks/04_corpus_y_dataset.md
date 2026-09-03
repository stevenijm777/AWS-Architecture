*Fecha: 2026-09-02*
*Hash (SHA-256): 809e0ca1eadfe2344c7b830d1f034652f8cd7684136e6a8a337394e252ea6dfd*

## Propósito
Filtra y define el corpus de arquitecturas usables desde las 396 iniciales de Cloudscape, y alinea el emparejamiento entre los pipelines para análisis posteriores.
**Artefacto producido:** `results/corpus.json`.

## Entradas
- Archivos leídos implícitamente por scripts: Datos del corpus Cloudscape y catálogo de videos (`videos.csv`).

## Compuertas
*(Ninguna `assert` explícita en este notebook).*

## Método
- **Criterio `graph_usable`:** Se respeta la bandera provista por el dataset original (Cloudscape).
- "Un grafo sin aristas no puede puntuar Edge F1: el denominador es 0".

## Resultados

**Filtro base del ground truth:**
```text
grafos en el ground truth : 396
  graph_usable = True     : 340
  graph_usable = False    : 56
```

**Emparejamiento entre los dos pipelines:**
```text
Standard      : 370 videos procesados · 321 con GT usable
Parsimonious  : 385 videos procesados · 336 con GT usable

videos en comun                       : 370
pareados Y usables en los dos (n=)     : 321   <- muestra de la comparacion pareada
Parsimonious usable (su propia media)  : 336

                                  n
poblacion                          
GT total                        396
GT usable                       340
Standard procesados             370
Parsimonious procesados         385
comunes a los dos               370
PAREADOS usables (comparacion)  321
```

**Calidad del catálogo de videos:**
```text
filas en videos.csv     : 570
  con video_id          : 504
  SIN video_id (vacio)  : 66

filas cuyo TITULO coincide con un episodio del GT pero cuyo video_id NO: 33
```
- "de esos IDs correctos, 32 ya estaban en videos.csv en otra fila (a menudo sin titulo)."

**Huérfanos:**
```text
huerfanos del GT sin entrada limpia en el catalogo: 72
```

## Limitaciones
- "Dos poblaciones distintas, que no hay que confundir: la muestra pareada sobre la que se comparan los brazos, y el conjunto sobre el que se reporta el desempeño de cada uno por separado."
