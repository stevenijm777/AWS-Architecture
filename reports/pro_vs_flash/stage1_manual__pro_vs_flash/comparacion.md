# gemini-3.1-pro-preview vs gemini-3.6-flash — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✓ mismo prompt Stage 2
- ✓ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.6-flash | gemini-3.1-pro-preview | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 87.82 | 86.46 | -1.36 | [-3.84, +1.21] | 3 / 6 / 21 | 0.508 |
| Edge F1 | 61.27 | 59.80 | -1.47 | [-5.63, +2.60] | 9 / 12 / 9 | 0.664 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.1-pro-preview | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `H2fOkeXxpyw` | 82.4 | 50.0 | -32.4 | 7 | 10 | 10 |
| `f5EJBUfGZtw` | 82.4 | 60.0 | -22.4 | 9 | 12 | 8 |
| `7V8wTCkjOqo` | 57.1 | 38.1 | -19.0 | 7 | 14 | 7 |
| `JYeXbUdFOdw` | 53.8 | 37.8 | -16.0 | 12 | 23 | 14 |
| `2L0m28ZLmtE` | 90.9 | 76.9 | -14.0 | 11 | 15 | 11 |
| `6YkguepAQuQ` | 53.3 | 44.4 | -8.9 | 5 | 8 | 10 |
| `jV8DwutbXbg` | 70.6 | 63.2 | -7.4 | 6 | 8 | 11 |
| `c-1GXhOOOww` | 32.3 | 27.0 | -5.2 | 15 | 21 | 16 |
| `-kA0ahrhX3I` | 66.7 | 61.5 | -5.1 | 4 | 5 | 8 |
| `hMK2NJ-q9nc` | 36.4 | 33.3 | -3.0 | 6 | 7 | 5 |
| `wjtSHyENv0I` | 69.6 | 66.7 | -2.9 | 9 | 10 | 14 |
| `07lfvavMdfU` | 83.3 | 81.5 | -1.9 | 10 | 13 | 14 |
| `-wLEkq21cvA` | 47.6 | 47.6 | +0.0 | 11 | 11 | 10 |
| `1aYoIZvabbk` | 72.7 | 72.7 | +0.0 | 6 | 6 | 5 |
| `2e3vOxsHekE` | 83.3 | 83.3 | +0.0 | 6 | 6 | 6 |
| `Cgv0kfp_6xQ` | 78.3 | 78.3 | +0.0 | 9 | 9 | 14 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `BlCXEMp_lqY` | 42.9 | 42.9 | +0.0 | 5 | 5 | 9 |
| `FfSNnH2bbNc` | 88.2 | 88.2 | +0.0 | 15 | 15 | 19 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `jg85DzUZ9Ac` | 57.1 | 57.1 | +0.0 | 10 | 10 | 11 |
| `6EUknQqaV1w` | 80.0 | 81.8 | +1.8 | 9 | 11 | 11 |
| `6CgqEzyWpeA` | 52.9 | 57.1 | +4.2 | 15 | 16 | 19 |
| `2XVgpMwY5iE` | 54.5 | 60.0 | +5.5 | 10 | 8 | 12 |
| `u3ZwnulzLnU` | 58.3 | 64.0 | +5.7 | 11 | 12 | 13 |
| `9qTEHITVeLE` | 46.2 | 53.3 | +7.2 | 12 | 16 | 14 |
| `a6kqyqTNJM4` | 34.8 | 46.2 | +11.4 | 8 | 11 | 15 |
| `BZ32w0SSAoY` | 55.2 | 72.7 | +17.6 | 10 | 14 | 19 |
| `ww5fiygF6eg` | 34.5 | 54.1 | +19.6 | 9 | 17 | 20 |
| `-3lnf5lzsH0` | 56.0 | 77.4 | +21.4 | 9 | 15 | 16 |
