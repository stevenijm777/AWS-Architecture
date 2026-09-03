*Fecha: 2026-09-02*
*Hash (SHA-256): 36d3b3dc53ff1cc685b700c462e1aa1e1b4aab65ce32116652ed2c2d3a98e182*

## Propósito
Analiza el mecanismo subyacente detrás de los desacuerdos de clasificación aguas abajo (identificando nodos faltantes específicos) y mide el efecto de la propagación del error topológico en el análisis de secuencias de workflows.
**Artefacto producido:** Ninguno explícitamente escrito en la salida.

## Entradas
- Datos del pipeline y etiquetas manuales (Overrides) de la clasificación downstream. Listas estáticas de disparadores del paper de Santillán y Abad.

## Compuertas
- Verificación de la identidad de las listas discriminadoras HPC y Edge contra el estudio de origen:
  `Compuerta pasada: las listas discriminadoras son las de los autores, sin cambios.`
- Reimplementación y aislamiento de overrides manuales:
  `Compuerta pasada: la regla reimplementada es la suya, y los overrides manuales quedan identificados y aislados.`

## Método
- Un desacuerdo de clasificación se atribuye al "disparador faltante o agregado".
- Se extrae la media y mediana de los *workflows* (secuencias de aristas síncronas partiendo desde un disparador) para comparar entre Ground Truth y Extracción sobre el mismo conjunto.

## Resultados

**Los servicios disparadores:**
```text
                               grupo  dispositivo  en el GT  en nuestra extracción   Δ
disparador                                                                            
cloudfront                      edge        False        43                     47   4
userconsumeredge                edge         True        21                      2 -19
...
userconsumerfarmer              edge         True         1                      1   0

edge: GT 121 apariciones · nosotros 110 · recall bruto 90.9 %
HPC: GT 10 apariciones · nosotros 11 · recall bruto 110.0 %

Sólo los 10 nodos de DISPOSITIVO (cámaras, drones, TVs, POS):
  GT 48 · nosotros 30 · recall 62.5 %
Son la clase de nodo que no es un servicio de AWS sino un actor físico del mundo.
```

**Atribuir cada desacuerdo a un servicio:**
```text
Dirección: **Edge → None** 14 · **None → Edge** 5 · **Edge+HPC → HPC** 1

Desacuerdos con un disparador perdido identificable: 15/20
  ... de los cuales el faltante es SÓLO un nodo de dispositivo: 15

Servicios que más desacuerdos causan al faltar:
   8 × userconsumeredge  (dispositivo)
   3 × usercompanyedge  (dispositivo)
   3 × userconsumertv  (dispositivo)
   1 × userconsumerpos  (dispositivo)
```

**RQ7 · Workflows:**
```text
                   n (GT)  media (GT)  mediana (GT)  n (nuestro)  media (nuestro)  mediana (nuestro)  Δ media
tipo_arquitectura                                                                                            
HPC                    11        4.00           3.0           12             2.50                2.0    -1.50
Edge                   98        3.28           3.0           89             2.60                2.0    -0.68
Edge+HPC                4        4.50           4.0            3             3.00                3.0    -1.50
None                  272        3.15           3.0          281             2.59                2.0    -0.57
Publicado en su Fig. 9: HPC 4.0 · Edge 3.3 · Edge+HPC 4.5 · None 3.1
Reproducido sobre el GT : HPC 4.0 · Edge 3.3 · Edge+HPC 4.5 · None 3.2
Sobre nuestra extracción: HPC 2.5 · Edge 2.6 · Edge+HPC 3.0 · None 2.6

Insight 8 de los autores: «la diferencia entre grupos no es alta, todos entre 3.1 y 4.5».
  rango de medias en el GT        : 3.2 – 4.5  (amplitud 1.3)
  rango con nuestra extracción    : 2.5 – 3.0  (amplitud 0.5)
```
- "La conclusión CUALITATIVA sobrevive —los grupos siguen sin separarse—, pero los valores absolutos caen 28 % en promedio: subcontamos workflows igual que subdibujamos aristas."

## Limitaciones
- "Qué no se puede afirmar: que el pipeline «no vea» los dispositivos por una limitación perceptual. El prompt de producción también poda actores, de modo que causa perceptual y decisión de diseño están confundidas y este notebook no las separa."
- "Tampoco nada cuantitativo sobre el grupo HPC, demasiado chico según sus propios autores."
