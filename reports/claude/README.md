# Panel de 30 con Claude en Stage 2

Misma condición que `reports/pro_vs_flash/*_stage1-manual`: Stage 1 es la transcripción
manual de la pizarra y solo cambia el modelo de Stage 2. Se corre con `claude -p`
(Claude Code con la suscripción), una llamada sin historial por video.

## Contenido

| archivo | qué es |
|---|---|
| `PROMPT_STAGE2.md` | el prompt de Stage 2, qué se reemplaza en él y el esquema de salida |
| `schema.json` | esquema JSON de la respuesta (el mismo `response_schema` de Gemini) |
| `videos/<id>/prompt.md` | texto exacto enviado para ese video (prompt + World Model manual + transcript) |
| `videos/<id>/world_model_manual.json` | Stage 1 manual de ese video |
| `videos/<id>/pizarra.jpg` | copia del frame de pizarra |
| `videos/<id>/output.json` | respuesta de Claude (aparece al correr) |
| `videos/<id>/meta.json` | modelo usado, effort, tokens, segundos |
| `videos/<id>/claude_raw.jsonl` | eventos crudos de `claude -p` |
| `videos/<id>/grafo.graphml`, `evaluacion.json` | grafo construido y sus métricas (tras `evaluate`) |
| `run.json`, `results.csv` | resultado del panel, comparable con `compare_models.py` |

## Pasos

```powershell
# 0. una sola vez: iniciar sesión en el CLI (abre el navegador)
& "$env:APPDATA\Claude\claude-code\2.1.293\83cb0bd7fed4\claude.exe" auth login

# 1. exportar (ya hecho; se puede repetir)
.venv\Scripts\python scripts\ablation\claude_panel.py export

# 2. prueba con 2 videos, luego el resto (retoma solo los que faltan)
.venv\Scripts\python scripts\ablation\claude_panel.py run --limit 2
.venv\Scripts\python scripts\ablation\claude_panel.py run

# 3. evaluar y comparar contra Flash con el mismo Stage 1
.venv\Scripts\python scripts\ablation\claude_panel.py evaluate
.venv\Scripts\python scripts\ablation\compare_models.py --a reports\pro_vs_flash\flash_gemini-3.6-flash_stage1-manual --b reports\claude --out reports\claude
```

Modelo por defecto `claude-opus-5-5` con effort `high`; se cambian con `--model` y `--effort`.

## Diferencias con las corridas de Gemini

- La temperatura no se puede fijar (Gemini corrió a 0.0).
- Claude Code exige un system prompt; se reemplaza el suyo por una línea neutra (está en
  `run.json`). Gemini no recibió ninguno.
- Sin herramientas, sin memoria de proyecto y en un directorio vacío, para que cada video
  llegue con contexto limpio.
