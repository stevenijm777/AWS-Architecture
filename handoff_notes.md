# Handoff Notes: AWS Architecture Extraction Pipeline

Hola, en esta nota se resumen los avances logrados, los cambios en los algoritmos y la estructura de archivos del proyecto, junto con los pasos y tareas pendientes para continuar el trabajo.

---

## 1. Contexto de los Cambios Recientes

Hemos optimizado el pipeline local para resolver problemas de selección de fotogramas y escalabilidad:

### A. Mejoras en la Selección de Pizarra (`scripts/frame_selector.py`)
1.  **Filtro Adaptativo de Oclusión (Presentadores):**
    *   **Problema:** En vídeos con pizarras negras (de cristal), el selector a veces elegía rostros o primeros planos del presentador por tener alta cantidad de píxeles oscuros.
    *   **Solución:** Se calcula el máximo porcentaje de píxeles oscuros (`max_dark_pct`) de todo el vídeo. Los fotogramas que bajen del `75%` de este valor (lo que indica que el presentador está bloqueando la pizarra o hay un zoom de su cara) son descartados de manera adaptativa.
2.  **Segmentación de Iconos (Morphological Opening):**
    *   **Problema:** Las flechas de conexión gruesas y los dibujos unían todos los iconos en un contorno gigante al aplicar la clausura morfológica (15x15), arruinando la puntuación del contenido.
    *   **Solución:** Se añadió una **apertura morfológica (5x5)** con kernel rectangular *antes* de la clausura. Esto "borra" las líneas de conexión delgadas y mantiene los iconos de AWS como contornos individuales y bien definidos, mejorando drásticamente el scoring de diagramas finales.

### B. Ejecución en Modo Local y Escalado a 150 Vídeos
*   Para evitar chocar con límites de cuota (TPM/RPM) de la API de Gemini, modificamos `main.py` y `scratch/process_to_150.py` para soportar la bandera `--skip-vision`.
*   Esta bandera ejecuta todo el procesamiento pesado (descarga, Whisper local en GPU y selección de pizarra) localmente sin llamar a Gemini.
*   **Logro:** Procesamos de manera local los **62 vídeos restantes** que hacían falta para llegar a la meta. El pipeline local corre de forma muy eficiente.

---

## 2. Nueva Estructura de Directorios

Hemos introducido carpetas en `data/` para la validación visual manual de las pizarras:

*   📂 **`data/un_processed/`**:
    *   Aquí se guardan las pizarras autoseleccionadas (`{video_id}.jpg`) de todos los nuevos vídeos procesados localmente en esta tanda.
    *   También se han movido a esta carpeta los 6 vídeos con problemas previos de pizarra (`_cca2eNePC4`, `-yCol_7qH2U`, `1SwHH7qQ6Pc`, `1VcpCVe3tLQ`, `6CgqEzyWpeA`, `6uEX5RKd0Bk`) para su revisión.
*   📂 **`data/procesados/`**:
    *   Contiene las imágenes de pizarra que ya han sido revisadas y confirmadas como correctas/de buena calidad.

> [!IMPORTANT]
> **Ignorado de Archivos Grandes (.gitignore):**
> Las carpetas `data/raw/` (videos mp4 y transcripciones json), `data/audio/` (archivos wav de audio) y `data/frames/` (todos los keyframes extraídos) ya están configuradas en `.gitignore`. No se subirán a Git ni llenarán tu espacio en disco. Solo se subirán los scripts, las pizarras seleccionadas en `.jpg` y los grafos finales en `.graphml`.

---

## 3. Tareas Pendientes y Pasos a Seguir

### Tarea 1: Revisión y Aprobación de Pizarras (Control de Calidad)
1.  Abre la carpeta `data/un_processed/` y revisa visualmente las imágenes de pizarra generadas.
2.  Si una imagen muestra la pizarra completa de forma clara, **muévela** a `data/procesados/`.
3.  Si notas algún vídeo que eligió un fotograma incorrecto, puedes depurarlo ejecutando individualmente el selector para ese vídeo:
    ```bash
    .venv/bin/python scripts/frame_selector.py VIDEO_ID --debug
    ```

### Tarea 2: Reprocesamiento de los 6 Vídeos con Ajustes de Pizarra
Hemos quitado los grafos y movido a `data/un_processed/` los siguientes 6 vídeos para reprocesarlos usando el nuevo algoritmo:
*   `_cca2eNePC4` (SoftChef AWS IoT)
*   `-yCol_7qH2U` (Talabat Migration)
*   `1SwHH7qQ6Pc` (Toyota Motor Lake House)
*   `1VcpCVe3tLQ` (Astana stock exchange)
*   `6CgqEzyWpeA` (Define Media Low Latency ML)
*   `6uEX5RKd0Bk` (HeyJobs Serverless)

Para procesarlos localmente con el nuevo algoritmo de selección:
```bash
.venv/bin/python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --skip-vision --force
```

### Tarea 3: Ejecución de la API de Visión en Bloque (Generación de Grafos)
Una vez que todas las pizarras en `data/un_processed/` hayan sido aprobadas y movidas a `data/procesados/`, puedes lanzar el análisis de visión masivo para generar los archivos de grafos definitivos `.graphml` sin gastar tiempo en re-descargas.
Ejecuta el script de lotes **sin** la bandera `--skip-vision`:
```bash
.venv/bin/python scratch/process_to_150.py
```
*Esto utilizará las transcripciones locales y los fotogramas seleccionados existentes, enviándolos en bloque a Gemini Vision de forma limpia.*

🟡 Problema #2: Prompt genera User nodes incorrectos y sobre-conecta edges
UserCompanyDeveloper alucinado 15 veces, UserConsumerWebMobile 13 veces
La regla 7 "return paths obligatorios" genera edges que el GT no tiene
ALB/ELB se confunden mutuamente


🟠 Problema #3: 92 carpetas processed_filters idénticas
Son los mismos 30 templates grises copiados a cada directorio de video
~35MB desperdiciados, se crean en symbol_detector.py
El plan detalla las s