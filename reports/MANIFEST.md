# Reports index

Every row is generated from a run's `run.json`. Do not edit by hand — run
`.venv/bin/python scripts/utils/build_manifest.py` instead.

Each run directory holds `results.csv` (one row per video, unaggregated),
`run.json` (aggregates + provenance) and `report.html` (rendered from the CSV).

## Runs

| Date | Mode | Label | n | Service F1 | Edge F1 | Model | Commit |
| :--- | :--- | :--- | ---: | ---: | ---: | :--- | :--- |
| [2026-08-20](runs/2026-08-20_parsimonious_v9/report.html) | parsimonious | `v9` | 370 | 85.12% | 55.31% (n=349) | `gemini-3.6-flash` | `edf995f` |
| [2026-08-19](runs/2026-08-19_parsimonious_v9/report.html) | parsimonious | `v9` | 344 | 85.41% | 55.37% (n=327) | `gemini-3.6-flash` | `932e3f9` |
| [2026-08-16](runs/2026-08-16_standard_v6corrected_299v/report.html) | standard | `v6corrected` | 299 | 86.03% | 58.2% (n=286) | `gemini-3.6-flash` | `c047767` |

## Notes per run

### `2026-08-20_parsimonious_v9`

- Pipeline: 1-stage parsimonious v9
- Input: `data/graphs_parsimonious` vs `data/cloudscape_gt`
- Evaluated 370 · edges scored on 349 · excluded from edge averages 21 (ground truth has zero edges)
- Edge F1 averaged the old way (zero-edge GT included): 52.17%
- Excluded: `1ZLiRT0C2Yo`, `6sY0AunanlM`, `8TExnSvZqt0`, `99nNHsbwBpg`, `c8615P0yfi8`, `E68ufJOduio`, `H51Ups01ZpU`, `hEB1J9-iOqs`, `JSBB-BCvavQ`, `jzKCg9Z5_8Q`, `lA0lAgN0hTI`, `OmVQ6pNDbaY`, `phN08pi3YzY`, `QuyZHin9B70`, `r3g1Nym-ebY`, `tTQ36qQF_vA`, `u5AT15mgbHk`, `vp2Ipv2_uCg`, `W96L6ICcF3s`, `zmJ7rL1iQBY`, `zqiNLMmEeSo`

### `2026-08-19_parsimonious_v9`

- Pipeline: 1-stage parsimonious v9
- Input: `data/graphs_parsimonious` vs `data/cloudscape_gt`
- Evaluated 344 · edges scored on 327 · excluded from edge averages 17 (ground truth has zero edges)
- Edge F1 averaged the old way (zero-edge GT included): 52.63%
- Excluded: `1ZLiRT0C2Yo`, `6sY0AunanlM`, `8TExnSvZqt0`, `99nNHsbwBpg`, `c8615P0yfi8`, `E68ufJOduio`, `H51Ups01ZpU`, `JSBB-BCvavQ`, `jzKCg9Z5_8Q`, `OmVQ6pNDbaY`, `phN08pi3YzY`, `QuyZHin9B70`, `r3g1Nym-ebY`, `tTQ36qQF_vA`, `u5AT15mgbHk`, `W96L6ICcF3s`, `zqiNLMmEeSo`

### `2026-08-16_standard_v6corrected_299v`

- Pipeline: 2-stage (Stage 1 Modeler → Stage 2 Planner), Pydantic response_schema, temperature 0.0
- Input: `data/graphs` vs `data/cloudscape_gt`
- Evaluated 299 · edges scored on 286 · excluded from edge averages 13 (ground truth has zero edges)
- Edge F1 averaged the old way (zero-edge GT included): 55.67%
- Excluded: `1ZLiRT0C2Yo`, `6sY0AunanlM`, `8TExnSvZqt0`, `99nNHsbwBpg`, `E68ufJOduio`, `JSBB-BCvavQ`, `QuyZHin9B70`, `W96L6ICcF3s`, `c8615P0yfi8`, `jzKCg9Z5_8Q`, `phN08pi3YzY`, `r3g1Nym-ebY`, `zqiNLMmEeSo`
