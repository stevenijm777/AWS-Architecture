*Fecha: 2026-09-02*
*Hash (SHA-256): 92f82b7e74b134eb0ffa7cd631240b30729b4658747d0bfb42b78b9cb02003c0*

## Propósito
Define cómo se convierte la salida del modelo en métricas (del JSON al grafo, de ahí a conjuntos de servicios y aristas, y finalmente a Precision, Recall y F1), y verifica estos cálculos contra el evaluador de producción.
**Artefacto producido:** `results/evaluacion_metricas_panel30.json`.

## Entradas
- Resultados de corridas sobre el panel de 30, extraídos para su uso como ejemplo de trabajo.

## Compuertas
- El notebook verifica todo cálculo contra el evaluador de producción (`scripts/evaluation/evaluate_graphs.evaluate_pair`); "si diverge, el notebook falla".
*(Nota: aunque no hay un `assert` explícito transcrito, la compuerta declarada es la coincidencia exacta contra `evaluate_pair`, verificada en las salidas `OK · coincide con evaluate_pair` y `OK · las medias estrictas reproducen exactamente las guardadas en run.json`).*

## Método
- **Nodos:** Identificados por su servicio, no por índice.
- **Aristas:** Representadas como pares ordenados de servicios.
- **Intersección sobre multiconjuntos:** Toma el mínimo de las multiplicidades.
- **Métrica estricta (Servicios):** F1 sobre el conjunto de servicios presentes, con coincidencia exacta de cadena contra el catálogo de Cloudscape.
- **Métrica estricta (Aristas):** F1 sobre el multiconjunto de pares dirigidos `(servicio_origen, servicio_destino)`.

## Resultados

**Datos y ejemplo de trabajo:**
```text
corrida     : 2026-08-29_0715_STAGE2_V6_CORRECTED_cell9_p30_rep4
prompt      : STAGE2_V6_CORRECTED · sha ed1d85054d73
modelo      : gemini-3.6-flash
videos      : 30
catalogo    : 169 servicios
metricas ya guardadas por la corrida: {'service_f1_mean': 86.13, 'edge_f1_mean': 57.87, 'n_success': 30}
```

**Precision, recall y F1:**
```text
                        |GEN|  aciertos  Precision  Recall     F1
escenario                                                        
perfecto                    3         3      1.000   1.000  1.000
omite 1 (falta Dynamo)      2         2      1.000   0.667  0.800
alucina 1 (agrega EC2)      4         3      0.750   1.000  0.857
alucina 3                   6         3      0.500   1.000  0.667
omite 1 y alucina 1         3         2      0.667   0.667  0.667
dispara a todo              9         3      0.333   1.000  0.500
```

**El costo de alucinar:**
```text
                      |GEN|  Precision  Recall  Service F1
servicios inventados                                      
0                         4      1.000     0.8       0.889
1                         5      0.800     0.8       0.800
2                         6      0.667     0.8       0.727
3                         7      0.571     0.8       0.667
4                         8      0.500     0.8       0.615
5                         9      0.444     0.8       0.571
6                        10      0.400     0.8       0.533
```
- "El recall es plano: alucinar no lo mueve."

**Conjunto contra multiconjunto (sobre n = 336 videos usables):**
```text
                       media
conjunto (svc_f1)      86.73
multiconjunto (ms_f1)  84.29
diferencia              2.44

nodos del GT que son instancias repetidas: 529/3478 = 15.2 %
```

**Anatomía del error de aristas:**
```text
                                     aristas     %
causa                                             
falta la arista de RETORNO                81  44.8
falta un nodo                             61  33.7
ambos nodos presentes, sin conexion       39  21.5

aristas del GT en el panel : 361
aristas del GT no generadas: 181 (50.1%)
```

**Descomposición de la ganancia (protocolo permisivo):**
```text
                          Edge F1 medio (panel 30)
estricta                                     57.87
ordenada sin dedup (ara)                     63.46
PERMISIVA 2 reglas                           74.00
3 reglas (no usar)                           76.94
Diferencia entre la 'sin regla 2' del ara y la permisiva de 2 reglas de este notebook:
   10.54 puntos

No son la misma metrica: la del ara no deduplica los bidireccionales,
asi que sigue castigando justo el error que dice perdonar.
```

**MEDIAS DEL PANEL (Salida exportada):**
```text
MEDIAS DEL PANEL
  Service F1 : estricta  86.13   permisiva  92.15   (+6.03)
  Edge F1    : estricta  57.87   permisiva  74.00   (+16.13)
```

## Limitaciones
- "Bajo la regla C un sistema que invirtiera todas las flechas obtendría F1 perfecto. El protocolo permisivo sirve para localizar el error, nunca para acreditar desempeño topológico."
