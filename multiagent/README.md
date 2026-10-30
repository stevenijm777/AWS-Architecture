# Sistema multiagente

Reconstruye una arquitectura Cloudscape separando las fuentes: un agente lee la pizarra, otro
la narración, un tercero las reconcilia, y lo determinista va en código. No toca el pipeline
Standard ni sus resultados.

```
pizarra (k fotogramas) ─► A1 lector visual ─┐
                                             ├─► C1 normalizador ─► A3 reconciliador ─► C2 reglas ─► C3 validación ─┬─► .graphml + procedencia
transcripción con tiempos ─► A2 narración ──┘       (código)            (LLM)            (código)      (código)      │
                                                                                                                  └─► A4 crítico (si C3/C2 avisan, 1 vuelta) ─► C3
```

| Archivo | Qué hace |
|---|---|
| `config.yaml` | modelo (`gemini-3.8-flash`), temperatura, k, rutas, flags de A2/C2/A4, tope de llamadas |
| `esquemas.py` | contratos Pydantic de A1–A4 (`response_schema`) |
| `llm.py` | llamada con caché `reports/multiagente/cache/<video>/<agente>/<hash>.json`, log por llamada y tope de llamadas nuevas; reutiliza `call_gemini` y `KeyRotator` de rerun_panel |
| `prompts/` | un prompt versionado por agente; la versión (`archivo@sha12`) queda en el log y en cada fila de run.json |
| `construir_datos.py` | congela `datos/alias.json` (C1) y `datos/reglas_c2.json` (C2) desde la partición de `reports/reglas_convencion/`, y verifica que ningún grafo del panel entra |
| `c1_normalizador.py`, `c2_reglas.py`, `c3_validacion.py` | pasos en código |
| `agentes.py` | insumos y armado de prompts de A1, A2, A3, A4 y la llamada única |
| `orquestador.py` | corre una configuración sobre videos o el panel |
| `evaluar.py` | `evaluate_pair` del repo, más precisión por procedencia, llamadas, tokens y costo |
| `estadistica.py` | signos y bootstrap (de compare_models), Wilcoxon exacto, Â12, MDE 3,29 |

## Configuraciones

| # | `--config` | Qué cambia |
|---|---|---|
| 1 | — | Standard (línea base): `rerun_panel.py` |
| 2 | `unica` | una sola llamada con pizarra y transcripción; C2 y C3 en código |
| 3 | `completo` | todo |
| 4 | `sin_a2` | sin narración |
| 5 | `sin_c2` | sin reglas |
| 6 | `sin_a4` | sin crítico (sale de la caché de `completo`) |
| 7 | `brazo_b` / `brazo_b_sin_c2` | el GT reemplaza a A1, con y sin C2 |

```bash
.venv/Scripts/python -m multiagent.orquestador --config completo --videos fRv8sOUyhZw 7LziNjUTo7w
.venv/Scripts/python -m multiagent.orquestador --config completo --panel --max-llamadas 130
.venv/Scripts/python -m multiagent.orquestador --config completo --panel --replica 1 --max-llamadas 130
.venv/Scripts/python -m multiagent.estadistica --a <run línea base> --b reports/multiagente/completo_k1_p30
```

## Reglas de C2 y el panel

Las reglas se estimaron solo con los 218 grafos de inducción y se eligieron con los 73 de
validación (`reports/reglas_convencion/particion.json`, semilla 42). Los 30 del panel quedaron
fuera de ambos conjuntos. `construir_datos.verificar` lo comprueba al construir los datos y otra
vez cada vez que C1 o C2 los cargan. Quedan dos familias:
- `actor_subtipo`, +0,90 en validación;
- `ida_y_vuelta` en 7 pares, +0,24.

`invertir` se descartó porque empeora en validación.
