# AWS Architecture Extractor 🚀
### Pipeline Multimodal de YouTube a GraphML (FAST25 Cloudscape Schema)

Este repositorio contiene un pipeline multimodal avanzado desarrollado en Python para extraer automáticamente diagramas de arquitectura en la nube (en formato GraphML) a partir de los vídeos de la serie de YouTube *"This is My Architecture"* de AWS. 

El pipeline procesa los vídeos descargando su contenido, extrayendo audio y keyframes, transcribiendo con Whisper GPU, seleccionando el fotograma de pizarra óptimo y utilizando la API de visión de Google Gemini para construir el grafo de red final bajo el estándar oficial de Cloudscape.

---

## 📋 Tabla de Contenidos
1. [Estructura del Repositorio](#-estructura-del-repositorio)
2. [Requisitos e Instalación](#-requisitos-e-instalación)
3. [Configuración de Entorno (.env)](#-configuración-de-entorno-env)
4. [Instrucciones de Ejecución](#-instrucciones-de-ejecución)
5. [Visualizadores Streamlit (Explorador Interactivo)](#-visualizadores-streamlit-explorador-interactivo)
6. [Laboratorio de Jupyter Notebooks](#-laboratorio-de-jupyter-notebooks)
7. [Consideraciones Especiales y Limitaciones](#-consideraciones-especiales-y-limitaciones)

---

## 📂 Estructura del Repositorio

El código ha sido modularizado y estructurado limpiamente en las siguientes carpetas:

```text
├── main.py                    # Punto de entrada unificado por CLI (soporta standard y parsimonious)
├── config/
│   └── settings.py            # Configuración global y rutas del sistema
├── scripts/
│   ├── core/                  # Módulos core del pipeline
│   │   ├── downloader.py      # Descarga de videos y metadatos con yt-dlp
│   │   ├── extractor.py       # Conversión de audio (WAV) y fotogramas (Keyframes) con FFmpeg
│   │   ├── transcriber.py     # Transcripción con OpenAI Whisper acelerada por GPU
│   │   ├── frame_selector.py  # Algoritmo de visión local para seleccionar la mejor pizarra
│   │   ├── vision_analyzer.py # Agente de Visión Gemini (Standard Mode)
│   │   ├── vision_analyzer_parsimonious.py # Agente de Visión Gemini (Parsimonious Mode)
│   │   ├── graph_builder.py   # Construcción y serialización del archivo GraphML
│   │   └── tracker.py         # Registro de control de videos procesados
│   ├── batch/                 # Ejecutores en lote y procesamiento por lotes
│   └── utils/                 # Herramientas de evaluación y métricas de grafos
├── cloudscape_explorer/       # Servidores visualizadores Streamlit interactivos
├── whiteboard_selection_lab/  # Laboratorio de notebooks Jupyter para pruebas locales
├── run_explorers.sh           # Script bash para levantar los 3 servidores Streamlit a la vez
├── requirements.txt           # Dependencias oficiales de Python
└── videos.csv                 # Base de datos local de videos de la serie
```

---

## 🛠 Requisitos e Instalación

### **Requisitos de Sistema**
* **Python 3.10 o superior**
* **FFmpeg** instalado en el sistema (necesario para el procesamiento de audio/video con OpenCV/FFmpeg).
* GPU con soporte **CUDA** (Altamente recomendado para Whisper. Si no hay GPU, transcribirá usando CPU de forma más lenta).

### **Instalación Paso a Paso**
1. Clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/stevenijm777/AWS-Architecture.git
   cd AWS-Architecture
   ```

2. Crea y activa un entorno virtual de Python:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Instala las dependencias del proyecto:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuración de Entorno (.env)

El pipeline requiere una API Key de Google Gemini para ejecutar el análisis de visión. Crea un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
# Google Gemini API Key (Requerido para el paso de visión)
GEMINI_API_KEY=Tu_API_Key_Aqui

# Modelo de Gemini a usar (Se recomienda gemini-3.5-flash)
GEMINI_MODEL=gemini-3.5-flash

# Tamaño del modelo Whisper: tiny, base, small, medium, large, turbo
WHISPER_MODEL=turbo

# Intervalo en segundos para la extracción de keyframes
FRAME_INTERVAL_SEC=10
```

---

## 🚀 Instrucciones de Ejecución

### **1. Procesar un único Video por URL**

Puedes procesar cualquier video interactivo pasando su URL de YouTube. El pipeline soporta dos modalidades de abstracción:

#### **Modo Standard (Clásico)**
Analiza el video de manera integral, extrayendo todos los servicios mencionados tanto visual como conversacionalmente:
```bash
python main.py --url "https://www.youtube.com/watch?v=5hjkSczrke4" --mode standard
```

#### **Modo Parsimonious (Simplificado)**
Es un enfoque estricto y conservador. Genera grafos muy limpios limitados exclusivamente a lo que se dibuja de forma nítida en la pizarra (ideal para reducir alucinaciones):
```bash
python main.py --url "https://www.youtube.com/watch?v=5hjkSczrke4" --mode parsimonious
```

### **Flags Adicionales del CLI:**
* `--skip-vision`: Ejecuta localmente todo el pipeline (descarga, audio, keyframes, Whisper, frame_selector) pero **salta las llamadas de pago a Gemini**. Excelente para pruebas de dry-run.
* `--force-vision`: Fuerza a Gemini a volver a realizar el análisis cognitivo de la imagen, sobreescribiendo el caché guardado en `data/raw/`.
* `--force`: Fuerza la ejecución de todos los pasos locales desde cero (descarga y keyframes), ignorando el almacenamiento local.

---

## 📊 Visualizadores Streamlit (Explorador Interactivo)

El proyecto incluye una suite interactiva de exploradores en [cloudscape_explorer/](file:///home/stemjara/Projects/AWS-Architecture/cloudscape_explorer) para navegar visualmente por las arquitecturas generadas y compararlas contra las referencias manuales.

Hemos unificado el arranque en el script unificado [run_explorers.sh](file:///home/stemjara/Projects/AWS-Architecture/run_explorers.sh). Solo debes ejecutar:

```bash
./run_explorers.sh
```

Esto levantará **tres servidores Streamlit concurrentes** en los siguientes puertos locales:
1. **Gemini Standard (Estilo Clásico):** [http://localhost:8501](http://localhost:8501) (Carga desde `data/graphs/`)
2. **Gemini Parsimonious (Estilo Simplificado):** [http://localhost:8502](http://localhost:8502) (Carga desde `data/graphs_parsimonious/`)
3. **Ground Truth (Manual de Referencia):** [http://localhost:8503](http://localhost:8503) (Carga desde `data/cloudscape_gt/`)

*Para apagar los tres servidores a la vez, simplemente presiona `Ctrl + C` en la terminal.*

---

## 🧪 Laboratorio de Jupyter Notebooks

Para pruebas y análisis locales, Melissa y el equipo pueden abrir los cuadernos de experimentos en [whiteboard_selection_lab/](file:///home/stemjara/Projects/AWS-Architecture/whiteboard_selection_lab).

La estructura de carpetas de almacenamiento pesado (`bad_whiteboard/`, `frames/`, etc.) ya está integrada mediante archivos de control de Git (`.gitkeep`). Solo deben levantar Jupyter:
```bash
jupyter notebook
```
Y abrir archivos como `Final_Visualization.ipynb` o `graficas.ipynb` para analizar visualmente la precisión de las máscaras de color, oclusión de siluetas de presentadores y correlación de texto.

---

## ⚠️ Consideraciones Especiales y Limitaciones

El pipeline cuenta con reglas automáticas de exclusión para evitar tokens desperdiciados o fallos del modelo:
1. **Vídeos Especiales y Recopilaciones:** Los videos que contienen palabras clave en su título como *"spotlight"*, *"greatest hits"*, *"bloopers"*, o *"reprise"* se omiten de manera segura.
2. **Idioma:** Solo se procesan videos en **inglés**. Los videos en español, francés, italiano, japonés o alemán se excluyen ya que Whisper en otro idioma desalinea las etiquetas de los servicios de AWS mapeados en inglés.
3. **Duración:** Vídeos de **12 minutos o más** son omitidos por el pipeline de lotes para evitar transcripciones sobredimensionadas que generen alucinación de aristas.

---

## ❓ Preguntas y Decisiones de Diseño (Para la Profesora)

Hemos recopilado las siguientes dudas arquitectónicas y metodológicas clave basadas en las métricas obtenidas y los casos particulares del dataset:

1. **Grafo Objetivo por Video:**
   * ¿Se espera que al final del proyecto contemos con un grafo para cada uno de los videos válidos del dataset? En aquellos casos especiales donde el modelo cometa imprecisiones debido a una pizarra con mala iluminación o diagramación no estándar, ¿debemos construir/corregir dichos grafos manualmente para asegurar un dataset de referencia completo?

2. **Umbral de Calidad Aceptable:**
   * ¿Cuál es el umbral de precisión y exhaustividad (*F1-Score*) que se consideraría satisfactorio para validar la efectividad de nuestro pipeline automático? Actualmente, el modo unificado estándar obtiene un **91.92% en F1 de Servicios (Nodos)** y un **67.78% en F1 de Conexiones (Aristas)** sobre el benchmark core.

3. **Nivel de Detalle en la Dirección de Flujos (Conexiones):**
   * ¿Qué tan detallados debemos ser con la dirección de las aristas? Específicamente, ¿debemos contemplar flujos bidireccionales (peticiones de ida y vuelta) o relaciones entrecortadas (mensajes de control/confirmación)? Actualmente, la lógica del pipeline prioriza el flujo principal de datos y no considera exhaustivamente las flechas de regreso.

4. **Flexibilidad en la Evaluación de Componentes Equivalentes:**
   * Detectamos discrepancias entre lo extraído por el modelo y el Ground Truth manual (por ejemplo, clasificar un nodo genérico como `ThirdParty` frente a usar nombres específicos como `REST API` o `Salesforce`). ¿Sería viable modificar la evaluación para que no penalice al modelo si selecciona un sinónimo funcional o un equivalente semántico aceptable?

5. **Discrepancia Visual/Conversacional y Nodos Duplicados:**
   * Hay videos donde los presentadores duplican visualmente el mismo servicio en la pizarra por estética de diseño (e.g., video `3yJZ6rPoZfg`), o donde mencionan servicios que no se dibujan (y viceversa). ¿Cómo se sugiere ponderar o resolver esta falta de consistencia entre la información del canal de audio (Whisper) y la imagen (Gemini Vision)?

