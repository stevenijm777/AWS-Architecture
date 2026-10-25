# gemini-3.6-flash vs gemini-3.6-flash — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✓ mismo prompt Stage 2
- ✗ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.6-flash | gemini-3.6-flash | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 85.90 | 87.82 | +1.91 | [-1.08, +5.19] | 10 / 8 / 12 | 0.815 |
| Edge F1 | 57.12 | 61.27 | +4.15 | [-0.75, +9.22] | 16 / 9 / 5 | 0.230 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.6-flash | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `BlCXEMp_lqY` | 71.4 | 42.9 | -28.6 | 5 | 5 | 9 |
| `6CgqEzyWpeA` | 74.3 | 52.9 | -21.3 | 16 | 15 | 19 |
| `jg85DzUZ9Ac` | 72.7 | 57.1 | -15.6 | 11 | 10 | 11 |
| `1aYoIZvabbk` | 83.3 | 72.7 | -10.6 | 7 | 6 | 5 |
| `u3ZwnulzLnU` | 66.7 | 58.3 | -8.3 | 11 | 11 | 13 |
| `Cgv0kfp_6xQ` | 83.3 | 78.3 | -5.1 | 10 | 9 | 14 |
| `6YkguepAQuQ` | 57.1 | 53.3 | -3.8 | 4 | 5 | 10 |
| `-wLEkq21cvA` | 50.0 | 47.6 | -2.4 | 10 | 11 | 10 |
| `ww5fiygF6eg` | 35.7 | 34.5 | -1.2 | 8 | 9 | 20 |
| `2e3vOxsHekE` | 83.3 | 83.3 | +0.0 | 6 | 6 | 6 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `H2fOkeXxpyw` | 82.4 | 82.4 | +0.0 | 7 | 7 | 10 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `jV8DwutbXbg` | 70.6 | 70.6 | +0.0 | 6 | 6 | 11 |
| `c-1GXhOOOww` | 30.8 | 32.3 | +1.5 | 10 | 15 | 16 |
| `6EUknQqaV1w` | 78.3 | 80.0 | +1.7 | 12 | 9 | 11 |
| `f5EJBUfGZtw` | 77.8 | 82.4 | +4.6 | 10 | 9 | 8 |
| `9qTEHITVeLE` | 40.0 | 46.2 | +6.2 | 11 | 12 | 14 |
| `07lfvavMdfU` | 75.0 | 83.3 | +8.3 | 10 | 10 | 14 |
| `2XVgpMwY5iE` | 45.5 | 54.5 | +9.1 | 10 | 10 | 12 |
| `JYeXbUdFOdw` | 44.4 | 53.8 | +9.4 | 13 | 12 | 14 |
| `a6kqyqTNJM4` | 25.0 | 34.8 | +9.8 | 9 | 8 | 15 |
| `hMK2NJ-q9nc` | 25.0 | 36.4 | +11.4 | 11 | 6 | 5 |
| `wjtSHyENv0I` | 54.5 | 69.6 | +15.0 | 8 | 9 | 14 |
| `BZ32w0SSAoY` | 40.0 | 55.2 | +15.2 | 6 | 10 | 19 |
| `-kA0ahrhX3I` | 50.0 | 66.7 | +16.7 | 8 | 4 | 8 |
| `2L0m28ZLmtE` | 72.7 | 90.9 | +18.2 | 11 | 11 | 11 |
| `-3lnf5lzsH0` | 32.0 | 56.0 | +24.0 | 9 | 9 | 16 |
| `7V8wTCkjOqo` | 26.7 | 57.1 | +30.5 | 8 | 7 | 7 |
| `FfSNnH2bbNc` | 48.3 | 88.2 | +40.0 | 10 | 15 | 19 |
