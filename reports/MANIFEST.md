# Reports index

Every row is generated from a run's `run.json`. Do not edit by hand — run
`.venv/bin/python scripts/utils/build_manifest.py` instead.

Each run directory holds `results.csv` (one row per video, unaggregated),
`run.json` (aggregates + provenance) and `report.html` (rendered from the CSV).

## Runs

| Date | Mode | Label | n | Service F1 | Edge F1 | Model | Commit |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- | :--- |
| [2026-08-16](runs/2026-08-16_standard_v6corrected_299v/report.html) | standard | `v6corrected` | 299 | 86.03% | 58.2% (n=286) | `gemini-3.6-flash` | `c047767` |

## Notes per run

### `2026-08-16_standard_v6corrected_299v`

- Pipeline: 2-stage (Stage 1 Modeler → Stage 2 Planner), Pydantic response_schema, temperature 0.0
- Input: `data/graphs` vs `data/cloudscape_gt`
- Evaluated 299 · edges scored on 286 · excluded from edge averages 13 (ground truth has zero edges)
- Edge F1 averaged the old way (zero-edge GT included): 55.67%
- Excluded: `1ZLiRT0C2Yo`, `6sY0AunanlM`, `8TExnSvZqt0`, `99nNHsbwBpg`, `E68ufJOduio`, `JSBB-BCvavQ`, `QuyZHin9B70`, `W96L6ICcF3s`, `c8615P0yfi8`, `jzKCg9Z5_8Q`, `phN08pi3YzY`, `r3g1Nym-ebY`, `zqiNLMmEeSo`
