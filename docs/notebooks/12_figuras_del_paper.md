*Fecha: 2026-09-02*
*Hash (SHA-256): 6a01fb9d8a2791fe59c50917ccd8a837538e273daabefa2ba8a3bc5c797f6fbf*

## Propósito
Genera las seis figuras del paper en formato vectorial y rasterizado (PDF, SVG y PNG), leyendo resultados precalculados sin consumir cuota de API.
**Artefacto producido:** Múltiples imágenes guardadas en `results/figuras_paper/`.

## Entradas
- Archivos `.json` de resultados computados por los notebooks 03, 05, 08 y 10.

## Compuertas
- Verificación del recálculo del F1 permisivo de dos reglas contra el original:
  `OK · misma definicion que el notebook 03.`
  (`permisivo 2 reglas recalculado : svc 92.15 · edge 74.00` vs `notebook 03 dice               : svc 92.15 · edge 74.00`)

## Método
- Lee métricas guardadas y dibuja los gráficos de barras, diagramas de dispersión, y gráficos de distribución usando las variables globales de calibración de ruido (`MDE`).

## Resultados

**Constantes de ruido usadas:**
```text
MDE n=30 — Edge 3.29 pts · Service 1.76 pts
```

**Inventario de figuras generadas:**
```text
                                figura         RQ   pdf   svg
0  fig1_asimetria_servicios_vs_aristas        RQ1  True  True
1                     fig2_subdibujado        RQ1  True  True
2           fig3_invarianza_de_prompts        RQ2  True  True
3             fig4_tres_brazos_oraculo        RQ3  True  True
4   fig5_estricto_vs_permisivo_2reglas  protocolo  True  True
5                fig6_tarea_downstream        RQ5  True  True

6 figuras en ../results/figuras_paper
```

**Detalle del Evaluador Permisivo de Figura 5:**
```text
IMPORTANTE — el permisivo de 3 reglas daria edge 76.94 en vez de 74.00.
La diferencia es la regla que colapsa duplicados, que el prompt implementa a proposito.
```

**Detalle Figura 1 (La asimetría):**
```text
Standard     : svc 86.78 · edge 59.65 · brecha 27.1 pts
Parsimonious : svc 85.73 · edge 57.01 · brecha 28.7 pts
```

**Detalle Figura 6 (La tarea downstream):**
```text
Direcciones del desacuerdo: {'Edge->None': 14, 'None->Edge': 5, 'Edge+HPC->HPC': 1}
```

## Limitaciones
- "Las figuras descartadas y el motivo: en cada caso, o el dato ya estaba en una tabla, o la figura mostraba una diferencia que no supera el umbral de detección y presentarla visualmente sugeriría un efecto que las pruebas no sostienen."
