# Reporte de Benchmarking y Estimación de Capacidad (Cloudscape Dataset)

Este reporte evalúa la velocidad de procesamiento del pipeline de extracción de arquitecturas en la nube y proyecta el tiempo necesario para alcanzar el objetivo de 150 videos procesados.

## 1. Configuración del Experimento
Se seleccionaron al azar 4 videos con antigüedad superior a 2 años de la base de datos de Cloudscape, distribuidos por cohortes de edad para garantizar la variabilidad de la calidad de imagen y los formatos de pizarra:
* **3 años**: `gpWR5JBC64A` (FoodHub)
* **4 años**: `A4Lfk1Zz1dE` (Spot.io)
* **5 años**: `07lfvavMdfU` (Levels Beyond)
* **6 años**: `Yju3yReAQtc` (Fortinet)

Cada video se procesó a través del pipeline completo en un entorno local (descarga de video, extracción de keyframes, transcripción con Whisper en GPU y análisis de visión estructurada con Gemini 3.5 Flash).

## 2. Resultados Obtenidos

| Video ID | Título | Antigüedad | Tiempo (s) | Precisión Servicios | Recall Servicios | Nodos/Arcos | Estado |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `gpWR5JBC64A` | FoodHub: Enabling Massive Scale Order Processing with Serverless Architecture | hace 3 años | 3.0 | 75.0% | 75.0% | 8/12 | ✅ Success |
| `A4Lfk1Zz1dE` | Spot.io: Optimizing Cloud Infrastructure Through Secure Cost Aware Automation | hace 4 años | 47.7 | 85.7% | 100.0% | 9/10 | ✅ Success |
| `07lfvavMdfU` | Levels Beyond: Digital Content Orchestration | hace 5 años | 50.2 | 90.9% | 100.0% | 11/15 | ✅ Success |
| `Yju3yReAQtc` | Fortinet Uses AWS Serverless to Provide a Highly Available ControlPlane for their FortiWeb CloudWAF | hace 6 años | 60.9 | 62.5% | 71.4% | 13/18 | ✅ Success |

## 3. Métricas de Rendimiento Promedio
* **Tiempo promedio por video:** 40.45 segundos (~0.67 minutos).
* **Rendimiento diario estimado (procesamiento continuo):** 2135.9 videos al día.

## 4. Estimación para alcanzar 150 videos

* **Videos ya procesados previamente (en `data/graphs/`):** 27
* **Videos restantes necesarios para el objetivo:** 123
* **Tiempo estimado necesario para el objetivo:** **0.06 días** (1.4 horas) de ejecución continua.

---
*Reporte generado automáticamente el 2026-06-15 20:46:57 (Hora local).*
