*Fecha: 2026-09-02*
*Hash (SHA-256): 83daca2a3dfbf808c8e5bae2f87136d7cd79e2cdf76b1c96f6ec2f806509a3c1*

## Propósito
Parte el error de aristas utilizando el tipo de anotación del ground truth de Cloudscape (`data` vs `meta`) para identificar si el déficit recae desproporcionadamente en las interacciones y *acks* enunciados verbalmente.
**Artefacto producido:** Ninguno explícitamente nombrado por la celda.

## Entradas
- `.graphml` en disco de Standard y Parsimonious sobre la muestra pareada (n=321).

## Compuertas
- Se verifica el F1 recalculado desde disco contra el valor previamente publicado:
  `Compuerta pasada: los graphml en disco son los que produjeron el paper.`
  (`Standard Service F1 (conjunto) = 86.78 esperado 86.78 OK`)

## Método
- Las aristas del ground truth se agrupan por su etiqueta `type`. El pipeline es evaluado en el Recall sobre esos subgrupos.
- **Métrica Recall por tipo:** "Toma las aristas del ground truth, las parte por *su* tipo, y pregunta si produjimos ese par de servicios. Por eso reporta recall y no F1".
- Ambigüedad de asignación resuelta mediante "reparto en proporción a los conteos".
- **Prueba Pareada por Video:** Prueba de signos no paramétrica.

## Resultados

**Los vocabularios de `type` no coinciden:**
```text
                   aristas                                  %                      
              Ground truth Standard Parsimonious Ground truth Standard Parsimonious
data                  3223     1910         2563         80.8     65.8         90.5
meta                   764      130           73         19.2      4.5          2.6
control                  0      861            0          0.0     29.7          0.0

Etiquetas que el ground truth NUNCA usa: ['authenticates', 'control', 'data_flow', 'network', 'reads_from', 'triggers', 'writes_to']
  Standard         861 aristas con etiqueta ajena (29.7 % de las suyas)
  Parsimonious     197 aristas con etiqueta ajena (7.0 % de las suyas)
```
- "El pipeline emite etiquetas que el ground truth nunca usa. [...] de acá en adelante ese campo no se vuelve a leer."

**Recall por tipo del ground truth:**
```text
              aristas data (GT)  recall data  aristas meta (GT)  recall meta  brecha  ambiguas
brazo                                                                                         
Standard                   3223        56.73                764        29.29   27.44       129
Parsimonious               3223        54.17                764        26.73   27.43       124

Las aristas ambiguas (mismo par como data y meta) son a lo sumo 3.2 % del total del GT:
el reparto proporcional no puede explicar una brecha de 27 puntos.
```

**Prueba pareada por video:**
```text
Standard       videos con ambos tipos: 196 | data > meta 150 / data < meta  46 / empates 0
               mediana de la diferencia: +34.58 pts | test de signos p = 4.6e-14

Parsimonious   videos con ambos tipos: 196 | data > meta 150 / data < meta  44 / empates 2
               mediana de la diferencia: +35.67 pts | test de signos p = 9.79e-15
```

**Por qué `edge_type_accuracy` no es interpretable:**
```text
              % etiquetado 'data'  etiquetas distintas  edge_type_accuracy
brazo                                                                     
Standard                     65.8                    3               61.51
Parsimonious                 90.5                    8               83.59
tasa base del ground truth ('data'): 80.8 %
```
- "La métrica no es interpretable como acierto de tipo: hay que sacarla o redefinirla contra un vocabulario mapeado."

**Nodos duplicados:**
```text
              Service F1 (conjunto)  Service F1 (multiconjunto)     Δ
brazo                                                                
Standard                      86.78                       84.50 -2.28
Parsimonious                  85.73                       83.85 -1.88
```

## Limitaciones
- "Cloudscape no publica reglas de decisión ni acuerdo entre anotadores para `data`/`meta`. La confiabilidad de la etiqueta es desconocida."
- "El confound que sí existe: si el anotador tendió a marcar `meta` justamente cuando la arista solo se mencionaba de palabra, etiqueta y fallo comparten causa y la brecha estaría inflada."
