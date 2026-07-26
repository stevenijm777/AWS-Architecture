# 🧪 Whiteboard Selection Lab

Sandbox de experimentación para desarrollar, probar y evaluar algoritmos de selección de pizarra y generación de grafos de arquitectura AWS sin afectar el pipeline de producción (`main.py` / `process_batch.py`).

> **Principio fundamental:** Todo el trabajo se realiza **localmente dentro de esta carpeta**. Los archivos necesarios (frames, transcripciones, audio, grafos previos) se **copian** desde `data/` al workspace local del video. Los resultados experimentales **nunca** se escriben directamente en `data/graphs/`.

---

## 📂 Estructura de Directorios

```
whiteboard_selection_lab/
│
├── README.md                       ← Este archivo
├── lab_notebook_guide.py           ← Guía rápida de importaciones para notebooks
│
├── 📓 NOTEBOOKS ─────────────────────────────────────────────────
│   ├── spanish_videos_lab.ipynb    ← Lab para videos en español (pipeline completo)
│   ├── prompt_evaluation_lab.ipynb ← Lab para probar prompts personalizados
│   ├── evaluacion_avanzada.ipynb   ← Evaluación masiva de carpetas de grafos vs GT
│   ├── process_video.ipynb         ← Experimentación con filtros de selección de frames
│   ├── video_Analyze.ipynb         ← Análisis visual detallado de frames
│   ├── Final_Visualization.ipynb   ← Visualización final de resultados
│   ├── Final_selection_v2.ipynb    ← Selección final de best_whiteboard (v2)
│   ├── creating_rules.ipynb        ← Creación/refinamiento de reglas de filtrado
│   ├── graficas.ipynb              ← Gráficas comparativas de métricas
│   ├── visualize_graphs.ipynb      ← Visualización de grafos individuales
│   └── preuba.ipynb                ← Notebook de pruebas rápidas
│
├── 📁 lab_workspace/               ← 🔑 WORKSPACE PRINCIPAL (por video)
│   ├── .gitkeep
│   └── {VIDEO_ID}/                 ← Carpeta aislada por video
│       ├── audio/                  ← Audio WAV copiado del video
│       ├── best_whiteboard.jpg     ← Mejor frame de pizarra seleccionado
│       ├── world_model.json        ← [Cache] Modelo del Mundo (Fase 1)
│       ├── test_analysis.json      ← [Cache] Análisis final del modelo (Fase 2)
│       ├── test_graph.graphml      ← Grafo experimental generado
│       ├── evaluation.json         ← [Evaluador] Resultado de evaluación con LLM
│       └── discrepancies.json      ← [Evaluador] Discrepancias detalladas
│
├── 📁 frames_new/                  ← Frames extraídos por video
│   ├── {VIDEO_ID}/                 ← Todos los keyframes del video
│   │   ├── frame_0000.jpg
│   │   ├── frame_0001.jpg
│   │   └── ...
│   └── {VIDEO_ID}_pizarra/         ← Frames filtrados como "pizarra"
│       ├── best_whiteboard.jpg     ← Mejor pizarra seleccionada
│       └── frame_selection_debug.json
│
├── 📁 transcriptions/              ← Transcripciones JSON (Whisper)
│   └── {VIDEO_ID}_transcript.json  ← Segmentos con timestamps
│
├── 📁 templates/                   ← Templates de iconos AWS para matching
│   ├── lambda.png
│   ├── s3.png
│   ├── ec2.png
│   └── ...                         ← ~29 templates de servicios AWS
│
├── 📁 algorithms/                  ← Algoritmos de selección/filtrado
│   ├── frame_selector.py           ← Selector principal de frames
│   ├── pizarra_filter.py           ← Filtro básico de pizarra
│   ├── pizarra_occlusion_filter.py ← Filtro de oclusión
│   ├── pizarra_outro_filter.py     ← Filtro de outro/cierre
│   ├── pizarra_compare_methods.py  ← Comparación de métodos
│   ├── pizarra_template_matching.py         ← Template matching
│   ├── pizarra_template_matching_transcript.py ← Template matching + transcript
│   └── symbol_detector.py          ← Detector de símbolos AWS
│
├── 📁 analisis_ground_truth/       ← Análisis estadístico del dataset GT
│   ├── 1_frecuencia_servicios.csv
│   ├── 2_frecuencia_flujos_edges.csv
│   └── 3_mapeo_textos_humanos.csv
│
├── 📁 bad_whiteboard/              ← Ejemplos de pizarras problemáticas (~93 imgs)
│   └── {VIDEO_ID}.jpg
│
├── 📁 frames/                      ← Frames legados (directorio vacío)
│
├── 📊 ARCHIVOS DE RESULTADOS ────────────────────────────────────
│   ├── evaluation_per_video.csv         ← Métricas por video (multi-modelo)
│   ├── detailed_model_comparison.csv    ← Comparación detallada entre modelos
│   └── three_graphs_comparison.csv      ← Comparación triple (GT vs Std vs Parsimonious)
```

---

## 🔄 Patrón de Trabajo en Notebooks

Todos los notebooks siguen un patrón consistente de **sandbox aislado**:

### 1. Configuración (Celda 1)

```python
VIDEO_ID = "6CgqEzyWpeA"

PROJECT_ROOT = Path('/home/stemjara/Projects/AWS-Architecture')
LAB_DIR = PROJECT_ROOT / 'whiteboard_selection_lab'

# Carpetas de trabajo locales
FRAMES_NEW_DIR = LAB_DIR / 'frames_new' / VIDEO_ID
TRANSCRIPTIONS_DIR = LAB_DIR / 'transcriptions'
LAB_WORKSPACE = LAB_DIR / 'lab_workspace' / VIDEO_ID
AUDIO_DIR = LAB_WORKSPACE / 'audio'

for d in (FRAMES_NEW_DIR, TRANSCRIPTIONS_DIR, LAB_WORKSPACE, AUDIO_DIR):
    d.mkdir(parents=True, exist_ok=True)
```

### 2. Copiado de Recursos (Celdas 2–5)

Los notebooks copian lo necesario desde `data/` al workspace local:

| Recurso | Origen | Destino |
|---------|--------|---------|
| Video MP4 | `data/raw/{VIDEO_ID}.mp4` | Se procesa en sitio |
| Audio WAV | Se extrae del MP4 | `lab_workspace/{VIDEO_ID}/audio/` |
| Transcripción | Se genera con Whisper | `transcriptions/{VIDEO_ID}_transcript.json` |
| Keyframes | Se extraen del video | `frames_new/{VIDEO_ID}/` |
| Best whiteboard | Se selecciona de frames | `lab_workspace/{VIDEO_ID}/best_whiteboard.jpg` |

### 3. Experimentación (Celdas 6–7)

Se definen prompts y se llaman a la API de Gemini:

- Los resultados se guardan **localmente** en `lab_workspace/{VIDEO_ID}/`
- Se implementa **caching**: si el archivo JSON ya existe, se carga sin consumir tokens
- Para re-ejecutar, eliminar los archivos cache manualmente

### 4. Evaluación (Celdas 8–9)

Se comparan los resultados experimentales contra:

- **Ground Truth** → `data/cloudscape_gt/{VIDEO_ID}.graphml`
- **Modelo Estándar** → `data/graphs/{VIDEO_ID}.graphml`
- **Modelo Parsimonioso** → `data/graphs_parsimonious/{VIDEO_ID}.graphml`

Usando `scripts/utils/evaluate_graphs.py` → `evaluate_pair()` que calcula:
- Service F1 (unique set y multiset)
- Edge F1 (por pares de servicio)
- Servicios faltantes y alucinados

---

## 🧪 Notebooks Disponibles

| Notebook | Propósito | Cuándo Usar |
|----------|-----------|-------------|
| `spanish_videos_lab.ipynb` | Pipeline completo para videos en español | Probar un video nuevo desde cero |
| `prompt_evaluation_lab.ipynb` | Probar prompts personalizados rápidamente | Iterar sobre redacción de prompts |
| `evaluacion_avanzada.ipynb` | Evaluación masiva de una carpeta completa | Benchmark de un modelo contra todo el GT |
| `process_video.ipynb` | Experimentar con filtros de selección de frames | Mejorar algoritmos de whiteboard selection |
| `graficas.ipynb` | Generar gráficas comparativas | Visualizar métricas entre modelos |

---

## 💡 Convenciones Importantes

1. **Nunca escribir en `data/graphs/` directamente** — Los grafos experimentales se guardan en `lab_workspace/`
2. **Caching por defecto** — Los notebooks verifican si el archivo ya existe antes de llamar a la API
3. **Para re-ejecutar**: Borrar los archivos de cache:
   ```bash
   rm lab_workspace/{VIDEO_ID}/world_model.json
   rm lab_workspace/{VIDEO_ID}/test_analysis.json
   rm lab_workspace/{VIDEO_ID}/evaluation.json
   ```
4. **Ground Truth como referencia** — Siempre se lee de `data/cloudscape_gt/` (solo lectura)
5. **Un `VIDEO_ID` por ejecución** — Cambiar la variable en la celda de configuración para analizar otro video
