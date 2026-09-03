*Fecha: 2026-09-02*
*Hash (SHA-256): 7687d19b746cd2d1d0da1ce052a4fd034d8230335606cb4b1db234deaa718a30*

## Propósito
Calibra cuánto se mueve el sistema cuando no se cambia nada, para usar como umbral base en toda comparación posterior.
**Artefacto producido:** `results/piso_ruido_panel30.json`

## Entradas
- Archivos de corridas leídos: `results/ablation/*/run.json`

## Compuertas
- `assert len(usadas) == len(set(usadas))`
  Verifica que las corridas emparejadas como réplicas nulas sean independientes (es decir, que ninguna corrida individual se reutilice cruzada entre dos pares).

## Método
- **Métrica `|dif|`:** Diferencia absoluta pareada por video, definida operativamente en la Celda 6 como "cuánto se mueve un video entre dos corridas idénticas".
- **Métrica MDE (Efecto Mínimo Detectable):** Diferencia más chica que un panel de tamaño $n$ puede detectar, calculada en la Celda 9 con la fórmula:
  $$\text{MDE} = (z_{1-\alpha/2} + z_{1-\beta})\,\frac{\sigma_d}{\sqrt{n}} = 2{,}80\,\frac{\sigma_d}{\sqrt{n}}$$
  (con $\alpha = 0.05$ a dos colas y potencia $0.80$).

## Resultados

**sigma_d por par, antes de juntar:**
```text
    condicion   n  sigma_svc  sigma_edge
0     oraculo  30       2.77        6.31
1  produccion  30       4.06        7.84
2  produccion  30       3.46        4.84
```

**POOL de 3 pares independientes (90 observaciones)**
```text
            n observaciones  sigma_d por video  MDE n=14  MDE n=30  MDE n=100  n para 3 pts
metrica                                                                                    
Service F1               90               3.45      2.58      1.76       0.97            11
Edge F1                  90               6.43      4.81      3.29       1.80            37
```

**Piso de ruido por metrica — pool de los pares nulos del panel de 30**
```text
                   n obs  sigma_d  MDE n=14  MDE n=30  media |dif|  max |dif|
metrica                                                                      
Edge F1               90     6.43      4.81      3.29         3.73      27.78
Service F1            90     3.45      2.58      1.76         1.13      16.67
aristas generadas     90     1.42      1.06      0.73         0.82       6.00
nodos generados       90     0.66      0.50      0.34         0.21       4.00
svc alucinados        90     0.41      0.31      0.21         0.13       2.00
svc faltantes         90     0.21      0.16      0.11         0.04       1.00
```

**Calibrado sobre los mismos 3 pares nulos (90 diferencias por nivel, protocolo permisivo)**
```text
                             Svc F1 medio  sigma_d Svc  MDE Svc n=30  Edge F1 medio  sigma_d Edge  MDE Edge n=30
nivel                                                                                                           
0 · estricto                        89.50         3.58          1.83          66.15          6.43           3.29
1 · + actores agrupados             94.38         3.51          1.79          68.18          6.61           3.38
2 · + aristas sin duplicar          94.38         3.51          1.79          71.47          6.03           3.08
3 · + aristas sin dirección         94.38         3.51          1.79          82.44          5.57           2.85
```

**Aporte incremental de cada relajación (protocolo permisivo):**
```text
                         Svc F1 medio  Edge F1 medio  MDE Svc n=30  MDE Edge n=30
+ agrupar actores                4.88           2.04         -0.04           0.09
+ aristas sin duplicar           0.00           3.29          0.00          -0.29
+ aristas sin dirección          0.00          10.97          0.00          -0.24

Estricto  -> permisivo completo:
  Edge F1 medio : 66.15 -> 82.44 (+16.30)
  MDE Edge      : 3.29 -> 2.85 (-0.44)

  Puntos de F1 ganados por cada punto de MDE reducido: 37.1
```

**Efecto del oráculo (Produccion promedia 3 replicas, oraculo 2; ambas sobre los mismos 30 videos)**
```text
            produccion  oraculo  delta  MDE n=30  veces el MDE veredicto
metrica                                                                 
Service F1       87.43    99.57  12.14      1.76          6.88      REAL
Edge F1          58.22    82.17  23.95      3.29          7.28      REAL

Service F1: oraculo gana en 25, pierde en 0, empata en 5 (de 30)  ->  p = 0.00000
Edge F1: oraculo gana en 28, pierde en 1, empata en 1 (de 30)  ->  p = 0.00000
```

## Limitaciones
- "Las réplicas nulas reutilizaron la salida de la etapa 1 desde caché, así que la varianza perceptual es cero por construcción: σ_d cuantifica la variabilidad del compilador de grafos y es una cota inferior de la del sistema completo."
- "La dirección del sesgo favorece a los resultados negativos —un umbral mayor los refuerza— y deja intacto el positivo. Medir la varianza de extremo a extremo exige una réplica que regenere la etapa 1."
