# Resumen de Estudio: Notebooks 01 y 02
**Proyecto:** AWS Architecture Extraction  
**Archivos Analizados:** [`notebooks/01_calibracion_ruido.ipynb`](file:///home/stemjara/Projects/aws-architecture-extraction/notebooks/01_calibracion_ruido.ipynb) y [`notebooks/02_evidencia_ablacion.ipynb`](file:///home/stemjara/Projects/aws-architecture-extraction/notebooks/02_evidencia_ablacion.ipynb)

---

## 📌 Contexto y Principio Metodológico

Los notebooks **01** y **02** están diseñados bajo un estricto principio de separación de responsabilidades:

> **Regla de Oro:** El notebook **01** fija el umbral de ruido (piso de ruido y MDE) ciego a las hipótesis. El notebook **02** carga esos umbrales de manera rígida y evalúa los experimentos de ablación sin recalcular el ruido.  
> *Razón:* Si un solo notebook calibrara el ruido y al mismo tiempo evaluara los efectos, se podría ajustar el umbral a conveniencia para obtener el veredicto deseado.

---

## 1. Notebook 01: Calibración del Piso de Ruido (Panel de 30)

### 🎯 Objetivo Principal
Medir **cuánto varía el pipeline por puro azar estocástico** (temperatura 0.0 del modelo Gemini 3.6 Flash) cuando no hay ninguna diferencia de código, prompt o entrada.

### 🔬 ¿Qué es una Réplica Nula?
Dos corridas son una *réplica nula* si difieren **únicamente en la llamada a la API**:
- Mismo prompt de Stage 2 (comprobado por el hash `sha256`).
- Misma imagen de la pizarra y misma transcripción de audio.
- Mismo evaluador.
- **Diferencia teórica esperada:** $d_i = A_i - B_i = 0.0$.

### 📊 Resultados Principales del Piso de Ruido

Muestra calibrada sobre **3 pares independientes** de 30 videos (**90 observaciones** en total):

| Métrica | Dispersión por video ($\sigma_d$) | **MDE ($n=30$)** | MDE ($n=14$) | MDE ($n=100$) | Muestras ($n$) para detectar 3 pts |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Edge F1 (Conexiones)** | **6.43 pts** | **3.29 pts** | 4.81 pts | 1.80 pts | 37 videos |
| **Service F1 (Nodos)** | **3.45 pts** | **1.76 pts** | 2.58 pts | 0.97 pts | 11 videos |
| **Aristas generadas** | 1.42 aristas | **0.73 aristas** | 1.06 aristas | 0.40 aristas | — |
| **Nodos generados** | 0.66 nodos | **0.34 nodos** | 0.50 nodos | 0.19 nodos | — |
| **Servicios alucinados** | 0.41 servicios | **0.21 servicios** | 0.31 servicios | 0.12 servicios | — |
| **Servicios faltantes** | 0.21 servicios | **0.11 servicios** | 0.16 servicios | 0.06 servicios | — |

*Donde MDE es el **Efecto Mínimo Detectable** con un nivel de significancia $\alpha=0.05$ y potencia $1-\beta=0.80$ ($\text{Z}_{\text{MDE}} = 2.80$).*

### 🧪 Calibración del Protocolo Permisivo (4 Niveles)
Demuestra que relajar las reglas de evaluación sube el promedio de F1, pero cada nivel modifica la varianza y requiere su propio MDE:

1. **0 · Estricto:** Svc F1 89.50% | Edge F1 66.15% | **MDE Edge: 3.29 pts**
2. **1 · + Actores agrupados:** Svc F1 94.38% | Edge F1 68.18% | **MDE Edge: 3.38 pts**
3. **2 · + Aristas sin duplicar:** Svc F1 94.38% | Edge F1 71.47% | **MDE Edge: 3.08 pts**
4. **3 · + Aristas sin dirección:** Svc F1 94.38% | Edge F1 82.44% | **MDE Edge: 2.85 pts**

### 🔮 Contraste Inicial del Oráculo (Evaluación Estricta)
Compara la ejecución de Producción contra una ejecución que recibe el World Model perfecto de referencia (*Oracle GT*):
- **Service F1:** Producción 87.43% vs Oráculo 99.57% ($\Delta = +12.14$ pts, $6.88\times \text{MDE}$, **Efecto Real**).
- **Edge F1:** Producción 58.22% vs Oráculo 82.17% ($\Delta = +23.95$ pts, $7.28\times \text{MDE}$, **Efecto Real**).

---

## 2. Notebook 02: Evidencia de la Ablación (Panel de 30)

### 🎯 Objetivo Principal
Evaluar **11 prompts distintos de la Etapa 2** sobre el mismo panel de 30 videos (**55 comparaciones pareadas por pares**) utilizando los umbrales de MDE cargados desde `results/piso_ruido_panel30.json`.

### 📊 Resultados de la Ablación entre Prompts

#### A. Rendimiento General por Prompt
Se promedian las réplicas del mismo SHA-256 (14 corridas en total para los 11 prompts puros):

- **Edge F1:** Rango de **56.49% a 60.10%** (Diferencia máxima / Rango = 3.61 pts).
- **Service F1:** Rango de **85.62% a 88.47%** (Diferencia máxima / Rango = 2.84 pts).
- **Aristas generadas:** Rango de **8.67 a 10.17 aristas**.

#### B. Pruebas Pareadas ($\hat{A}_{12}$ de Vargha & Delaney) y Significancia
Se analizan las **55 comparaciones pareadas** entre todos los pares de prompts:

- **Efecto en Edge F1:**
  - Significativas sin corregir ($\alpha=0.05$): **3 de 55** (Probabilidad de falso positivo sin corregir = 94.0%).
  - Significativas con corrección por pruebas múltiples (**Holm-Bonferroni**): **0 de 55**.
  - Significativas con **Bonferroni**: **0 de 55** ($p < 0.00091$).
  - **Magnitud del efecto ($\hat{A}_{12}$):** 55/55 comparaciones son de magnitud **insignificante** ($\hat{A}_{12} \approx 0.452 - 0.553$).
  - Todos los intervalos de confianza del 95% para $\hat{A}_{12}$ incluyen el valor 0.5 (ausencia de efecto).

> **Veredicto Clave:** **Ninguna diferencia entre prompts es estadísticamente detectable en Edge F1 ni en Service F1.** El rango entero de variación entre los 11 prompts cabe dentro del piso de ruido del sistema.

#### C. Lo que el Edge F1 Esconde (Cantidad de Aristas Dibujadas)
Aunque el Edge F1 es indistinguible entre prompts, los prompts **sí difieren de forma detectable en cuántas aristas dibujan**:
- Prompts con reglas explícitas de flujos de retorno (`STAGE2_V7_RETURN_FLOWS`) dibujan en promedio **10.17 aristas**.
- Prompts anti-alucinación (`STAGE2_V4_ANTI_HALLUCINATION`) dibujan **8.67 aristas**.
- Comparación extremo contra extremo: $\hat{A}_{12} = 0.622$ (IC 95%: $[0.558, 0.700]$) $\rightarrow$ **Efecto pequeño pero estadísticamente real**.
- *Nota:* Todos los prompts subdibujan aristas en comparación con el Ground Truth.

#### D. El Oráculo frente a Producción (Notebook 02)
Evaluación de hipótesis única preespecificada (sin penalización por comparaciones múltiples):

| Métrica | Producción | Oráculo | Diferencia ($\Delta$) | MDE ($n=30$) | $\hat{A}_{12}$ [IC 95%] | Magnitud |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Edge F1** | 58.43% | **82.17%** | **+23.75 pts** | 3.29 pts | 0.856 [0.788, 0.924] | **Grande** |
| **Service F1** | 87.55% | **99.57%** | **+12.02 pts** | 1.76 pts | 0.906 [0.829, 0.975] | **Grande** |
| **Aristas generadas** | 9.07 | 9.97 | +0.90 | 0.73 | 0.597 [0.522, 0.682] | Pequeño |
| **Nodos generados** | 8.92 | 8.73 | -0.18 | 0.34 | 0.479 [0.403, 0.552] | Insignificante |
| **Servicios alucinados** | 0.80 | **0.02** | **-0.78** | 0.21 | 0.155 [0.071, 0.241] | **Grande** (reducción) |
| **Servicios faltantes** | 1.00 | **0.03** | **-0.97** | 0.11 | 0.178 [0.092, 0.267] | **Grande** (reducción) |

---

## 💡 Conclusiones Integradas (Notebooks 01 + 02)

1. **Inestabilidad Estocástica del LLM:** Temperatura 0.0 no produce ejecuciones deterministas; variaciones azarosas entre réplicas nulas pueden alcanzar hasta 28-32 puntos de F1 en un solo video.
2. **Límite de la Ingeniería de Prompts en Etapa 2:** Modificar el texto del prompt en la Etapa 2 no genera mejoras estadísticamente detectables en la precisión del grafo de arquitectura (Edge F1 o Service F1).
3. **El Cuello de Botella es la Etapa 1 (World Model):** El salto masivo demostrado por el Oráculo (+23.75 pts en Edge F1 y erradicación casi total de alucinaciones y omisiones) prueba que las limitaciones del sistema provienen de la extracción visual y contextual de la Etapa 1, no del razonamiento o formateo del prompt en la Etapa 2.
