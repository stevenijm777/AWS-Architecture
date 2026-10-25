# gemini-3.1-pro-preview vs gemini-3.1-pro-preview — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✓ mismo prompt Stage 2
- ✗ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.1-pro-preview | gemini-3.1-pro-preview | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 85.04 | 86.46 | +1.42 | [-1.55, +4.59] | 10 / 7 / 13 | 0.629 |
| Edge F1 | 56.07 | 59.80 | +3.73 | [-0.78, +8.53] | 14 / 10 / 6 | 0.541 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.1-pro-preview | gemini-3.1-pro-preview | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `6CgqEzyWpeA` | 74.3 | 57.1 | -17.1 | 16 | 16 | 19 |
| `-wLEkq21cvA` | 63.6 | 47.6 | -16.0 | 12 | 11 | 10 |
| `jg85DzUZ9Ac` | 72.7 | 57.1 | -15.6 | 11 | 10 | 11 |
| `1aYoIZvabbk` | 83.3 | 72.7 | -10.6 | 7 | 6 | 5 |
| `H2fOkeXxpyw` | 60.0 | 50.0 | -10.0 | 10 | 10 | 10 |
| `jV8DwutbXbg` | 70.6 | 63.2 | -7.4 | 6 | 8 | 11 |
| `Cgv0kfp_6xQ` | 83.3 | 78.3 | -5.1 | 10 | 9 | 14 |
| `u3ZwnulzLnU` | 66.7 | 64.0 | -2.7 | 11 | 12 | 13 |
| `6YkguepAQuQ` | 47.1 | 44.4 | -2.6 | 7 | 8 | 10 |
| `ww5fiygF6eg` | 54.5 | 54.1 | -0.5 | 13 | 17 | 20 |
| `2e3vOxsHekE` | 83.3 | 83.3 | +0.0 | 6 | 6 | 6 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `BlCXEMp_lqY` | 42.9 | 42.9 | +0.0 | 5 | 5 | 9 |
| `JYeXbUdFOdw` | 37.8 | 37.8 | +0.0 | 23 | 23 | 14 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `f5EJBUfGZtw` | 60.0 | 60.0 | +0.0 | 12 | 12 | 8 |
| `c-1GXhOOOww` | 26.3 | 27.0 | +0.7 | 22 | 21 | 16 |
| `hMK2NJ-q9nc` | 30.8 | 33.3 | +2.6 | 8 | 7 | 5 |
| `07lfvavMdfU` | 78.6 | 81.5 | +2.9 | 14 | 13 | 14 |
| `6EUknQqaV1w` | 78.3 | 81.8 | +3.6 | 12 | 11 | 11 |
| `-kA0ahrhX3I` | 50.0 | 61.5 | +11.5 | 8 | 5 | 8 |
| `BZ32w0SSAoY` | 61.1 | 72.7 | +11.6 | 17 | 14 | 19 |
| `wjtSHyENv0I` | 54.5 | 66.7 | +12.1 | 8 | 10 | 14 |
| `2L0m28ZLmtE` | 61.5 | 76.9 | +15.4 | 15 | 15 | 11 |
| `9qTEHITVeLE` | 37.0 | 53.3 | +16.3 | 13 | 16 | 14 |
| `2XVgpMwY5iE` | 43.5 | 60.0 | +16.5 | 11 | 8 | 12 |
| `-3lnf5lzsH0` | 60.0 | 77.4 | +17.4 | 14 | 15 | 16 |
| `7V8wTCkjOqo` | 20.0 | 38.1 | +18.1 | 13 | 14 | 7 |
| `a6kqyqTNJM4` | 15.4 | 46.2 | +30.8 | 11 | 11 | 15 |
| `FfSNnH2bbNc` | 48.3 | 88.2 | +40.0 | 10 | 15 | 19 |
