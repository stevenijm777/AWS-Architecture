*Fecha: 2026-09-02*
*Hash (SHA-256): 1f5949165f2e327b838fd1145a7a8e90a3752a6152db98770da6ea7cc1b91bdc*

## Propósito
Verifica el linaje exacto de cada prompt de Stage 2, comprobando que cada corrida grabada se origine en un texto materializado idéntico al que figura en el manifiesto, usando sus hashes SHA-256 en lugar de sus nombres de archivo.
**Artefacto producido:** Ninguno impreso.

## Entradas
- Manifiesto de prompts e historial de corridas en `run.json`. Textos materializados de los prompts de Stage 2.

## Compuertas
- Verificación cruzada entre los archivos `.txt` materializados y los hashes del manifiesto:
  `OK · los textos materializados son los que el manifiesto declara.`
  (`variantes verificadas: 18 · discrepancias: 0`)
- Verificación cruzada de todas las corridas contra un prompt registrado verificable:
  `OK · toda corrida guardada es atribuible a un texto de prompt verificable.`
- Verificación del prompt de producción contra el manifiesto:
  `OK · .txt ↔ manifiesto verificado. El eslabon contra el codigo de produccion en vivo se verifica en el repo de trabajo.`

## Método
- Compara los hashes SHA-256 de los prompts grabados en cada corrida contra los manifiestos, ya que "dos archivos con el mismo nombre contienen textos distintos".

## Resultados

**Re-extracción y verificación contra el manifiesto:**
```text
manifiesto generado: 2026-08-19
variantes registradas: 18

sha de produccion · Stage 2: ed1d85054d73
sha de produccion · Stage 1: 497d30164f48

Re-extraccion no disponible en este repo (falta el notebook de laboratorio).
Verificando en su lugar: .txt materializado ↔ hash del manifiesto.

variantes verificadas: 18 · discrepancias: 0
```

**Las celdas no recuperables:**
```text
Celdas no recuperables declaradas en el manifiesto:

  celda 11 · STAGE2_V7_RETURN_FLOWS
    NameError: name 'STAGE2_V4_ANTI_HALLUCINATION' is not defined
```

**Inventario (resumen de inconsistencia de nombres):**
```text
Nombres que corresponden a mas de un texto:
  V0_BASELINE: 2 textos distintos — celdas [7.0, 8.0], [2375, 2513] chars
  V4_ANTI_HALLUCINATION: 2 textos distintos — celdas [7.0, 8.0], [2904, 3422] chars
  V5_STRICT_ROUTING: 2 textos distintos — celdas [7.0, 8.0], [3256, 3737] chars
  V6_CORRECTED: 3 textos distintos — celdas [7.0, 9.0, 10.0], [3835, 3887, 3974] chars
```
- "Por qué importa. El nombre de una variante no la identifica; el hash sí. Toda cifra de ablación del proyecto se atribuye por SHA, no por nombre."

**Cada corrida apunta a un prompt que existe:**
```text
corridas con prompt registrado : 35
con hash RECONOCIDO            : 35
con hash huerfano              : 0
```

**El prompt de producción:**
```text
stage2_v6_corrected__cell9.txt  : ed1d85054d73c153
manifiesto dice produccion      : ed1d85054d73c153
vision_analyzer.py              : no disponible en este repo
```

**Cómo se arma el prompt final:**
```text
Placeholders de la plantilla:
  <AWS_SERVICES_PLACEHOLDER>
  <USER_ACTORS_PLACEHOLDER>
  <WORLD_MODEL_PLACEHOLDER>

Lo que se agrega despues de la plantilla, en orden (rerun_panel.run_video):
  1. la plantilla con los placeholders ya sustituidos
  2. ## VIDEO URL:  (el enlace de YouTube)
  3. ## FULL TRANSCRIPT:  (el audio transcripto — ausente con --no-transcript)
  4. [imagen] la pizarra aprobada, adjunta como inline_data

plantilla: 3978 chars
El texto ENSAMBLADO no se guarda; se reconstruye desde plantilla + catalogo +
World Model + transcript, todos con procedencia registrada en el run.json.
```

## Limitaciones
- "Re-extraccion no disponible en este repo (falta el notebook de laboratorio)."
- "El texto ENSAMBLADO no se guarda; se reconstruye desde plantilla + catalogo + World Model + transcript, todos con procedencia registrada en el run.json."
