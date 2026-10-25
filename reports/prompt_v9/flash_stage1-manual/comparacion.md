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
| Service F1 | 87.82 | 87.78 | -0.04 | [-0.77, +0.66] | 1 / 1 / 28 | 1.000 |
| Edge F1 | 61.27 | 58.45 | -2.82 | [-5.53, -0.66] | 4 / 9 / 17 | 0.267 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.6-flash | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `2L0m28ZLmtE` | 90.9 | 60.6 | -30.3 | 11 | 22 | 11 |
| `H2fOkeXxpyw` | 82.4 | 70.6 | -11.8 | 7 | 7 | 10 |
| `JYeXbUdFOdw` | 53.8 | 42.1 | -11.7 | 12 | 5 | 14 |
| `BZ32w0SSAoY` | 55.2 | 44.4 | -10.7 | 10 | 8 | 19 |
| `2e3vOxsHekE` | 83.3 | 72.7 | -10.6 | 6 | 5 | 6 |
| `-3lnf5lzsH0` | 56.0 | 48.0 | -8.0 | 9 | 9 | 16 |
| `u3ZwnulzLnU` | 58.3 | 52.2 | -6.2 | 11 | 10 | 13 |
| `wjtSHyENv0I` | 69.6 | 63.6 | -5.9 | 9 | 8 | 14 |
| `6CgqEzyWpeA` | 52.9 | 51.4 | -1.5 | 15 | 16 | 19 |
| `-kA0ahrhX3I` | 66.7 | 66.7 | +0.0 | 4 | 4 | 8 |
| `-wLEkq21cvA` | 47.6 | 47.6 | +0.0 | 11 | 11 | 10 |
| `07lfvavMdfU` | 83.3 | 83.3 | +0.0 | 10 | 10 | 14 |
| `1aYoIZvabbk` | 72.7 | 72.7 | +0.0 | 6 | 6 | 5 |
| `6EUknQqaV1w` | 80.0 | 80.0 | +0.0 | 9 | 9 | 11 |
| `6YkguepAQuQ` | 53.3 | 53.3 | +0.0 | 5 | 5 | 10 |
| `Cgv0kfp_6xQ` | 78.3 | 78.3 | +0.0 | 9 | 9 | 14 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `9qTEHITVeLE` | 46.2 | 46.2 | +0.0 | 12 | 12 | 14 |
| `BlCXEMp_lqY` | 42.9 | 42.9 | +0.0 | 5 | 5 | 9 |
| `FfSNnH2bbNc` | 88.2 | 88.2 | +0.0 | 15 | 15 | 19 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `a6kqyqTNJM4` | 34.8 | 34.8 | +0.0 | 8 | 8 | 15 |
| `f5EJBUfGZtw` | 82.4 | 82.4 | +0.0 | 9 | 9 | 8 |
| `hMK2NJ-q9nc` | 36.4 | 36.4 | +0.0 | 6 | 6 | 5 |
| `jV8DwutbXbg` | 70.6 | 70.6 | +0.0 | 6 | 6 | 11 |
| `jg85DzUZ9Ac` | 57.1 | 57.1 | +0.0 | 10 | 10 | 11 |
| `c-1GXhOOOww` | 32.3 | 33.3 | +1.1 | 15 | 14 | 16 |
| `ww5fiygF6eg` | 34.5 | 35.7 | +1.2 | 9 | 8 | 20 |
| `7V8wTCkjOqo` | 57.1 | 61.5 | +4.4 | 7 | 6 | 7 |
| `2XVgpMwY5iE` | 54.5 | 60.0 | +5.5 | 10 | 8 | 12 |
