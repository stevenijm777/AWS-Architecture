# gemini-3.6-flash vs gemini-3.6-flash — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✗ mismo prompt Stage 2
- ✓ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.6-flash | gemini-3.6-flash | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 85.90 | 85.65 | -0.25 | [-1.74, +1.05] | 3 / 3 / 24 | 1.000 |
| Edge F1 | 57.12 | 57.55 | +0.43 | [-1.88, +2.98] | 6 / 7 / 17 | 1.000 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.6-flash | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `1aYoIZvabbk` | 83.3 | 66.7 | -16.7 | 7 | 7 | 5 |
| `2e3vOxsHekE` | 83.3 | 72.7 | -10.6 | 6 | 5 | 6 |
| `u3ZwnulzLnU` | 66.7 | 60.9 | -5.8 | 11 | 10 | 13 |
| `07lfvavMdfU` | 75.0 | 69.6 | -5.4 | 10 | 9 | 14 |
| `2L0m28ZLmtE` | 72.7 | 69.6 | -3.2 | 11 | 12 | 11 |
| `JYeXbUdFOdw` | 44.4 | 42.9 | -1.6 | 13 | 14 | 14 |
| `c-1GXhOOOww` | 30.8 | 29.6 | -1.1 | 10 | 11 | 16 |
| `-3lnf5lzsH0` | 32.0 | 32.0 | +0.0 | 9 | 9 | 16 |
| `6CgqEzyWpeA` | 74.3 | 74.3 | +0.0 | 16 | 16 | 19 |
| `6YkguepAQuQ` | 57.1 | 57.1 | +0.0 | 4 | 4 | 10 |
| `BZ32w0SSAoY` | 40.0 | 40.0 | +0.0 | 6 | 6 | 19 |
| `Cgv0kfp_6xQ` | 83.3 | 83.3 | +0.0 | 10 | 10 | 14 |
| `wjtSHyENv0I` | 54.5 | 54.5 | +0.0 | 8 | 8 | 14 |
| `ww5fiygF6eg` | 35.7 | 35.7 | +0.0 | 8 | 8 | 20 |
| `2XVgpMwY5iE` | 45.5 | 45.5 | +0.0 | 10 | 10 | 12 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `9qTEHITVeLE` | 40.0 | 40.0 | +0.0 | 11 | 11 | 14 |
| `BlCXEMp_lqY` | 71.4 | 71.4 | +0.0 | 5 | 5 | 9 |
| `H2fOkeXxpyw` | 82.4 | 82.4 | +0.0 | 7 | 7 | 10 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `f5EJBUfGZtw` | 77.8 | 77.8 | +0.0 | 10 | 10 | 8 |
| `hMK2NJ-q9nc` | 25.0 | 25.0 | +0.0 | 11 | 11 | 5 |
| `jV8DwutbXbg` | 70.6 | 70.6 | +0.0 | 6 | 6 | 11 |
| `jg85DzUZ9Ac` | 72.7 | 72.7 | +0.0 | 11 | 11 | 11 |
| `FfSNnH2bbNc` | 48.3 | 50.0 | +1.7 | 10 | 9 | 19 |
| `7V8wTCkjOqo` | 26.7 | 28.6 | +1.9 | 8 | 7 | 7 |
| `6EUknQqaV1w` | 78.3 | 83.3 | +5.1 | 12 | 13 | 11 |
| `a6kqyqTNJM4` | 25.0 | 33.3 | +8.3 | 9 | 9 | 15 |
| `-kA0ahrhX3I` | 50.0 | 66.7 | +16.7 | 8 | 4 | 8 |
| `-wLEkq21cvA` | 50.0 | 73.7 | +23.7 | 10 | 9 | 10 |
