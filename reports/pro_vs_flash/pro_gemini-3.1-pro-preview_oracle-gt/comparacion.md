# gemini-3.1-pro-preview vs gemini-3.6-flash — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✓ mismo prompt Stage 2
- ✗ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.6-flash | gemini-3.1-pro-preview | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 99.70 | 93.54 | -6.15 | [-8.64, -3.80] | 0 / 16 / 14 | 0.000 |
| Edge F1 | 83.18 | 71.49 | -11.70 | [-18.10, -5.83] | 7 / 21 / 2 | 0.013 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.1-pro-preview | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `hMK2NJ-q9nc` | 90.9 | 30.8 | -60.1 | 6 | 8 | 5 |
| `-kA0ahrhX3I` | 94.1 | 50.0 | -44.1 | 9 | 8 | 8 |
| `JYeXbUdFOdw` | 80.0 | 45.0 | -35.0 | 11 | 26 | 14 |
| `c-1GXhOOOww` | 78.8 | 47.6 | -31.2 | 17 | 26 | 16 |
| `wjtSHyENv0I` | 78.3 | 47.6 | -30.6 | 9 | 7 | 14 |
| `f5EJBUfGZtw` | 88.9 | 60.0 | -28.9 | 10 | 12 | 8 |
| `BlCXEMp_lqY` | 71.4 | 42.9 | -28.6 | 5 | 5 | 9 |
| `9qTEHITVeLE` | 83.3 | 60.0 | -23.3 | 10 | 16 | 14 |
| `2L0m28ZLmtE` | 95.2 | 80.0 | -15.2 | 10 | 14 | 11 |
| `u3ZwnulzLnU` | 96.0 | 82.8 | -13.2 | 12 | 16 | 13 |
| `a6kqyqTNJM4` | 69.2 | 57.1 | -12.1 | 11 | 13 | 15 |
| `6EUknQqaV1w` | 90.9 | 80.0 | -10.9 | 11 | 14 | 11 |
| `07lfvavMdfU` | 92.3 | 81.5 | -10.8 | 12 | 13 | 14 |
| `-wLEkq21cvA` | 85.7 | 75.0 | -10.7 | 11 | 14 | 10 |
| `-3lnf5lzsH0` | 93.3 | 82.8 | -10.6 | 14 | 13 | 16 |
| `jg85DzUZ9Ac` | 100.0 | 90.9 | -9.1 | 11 | 11 | 11 |
| `6YkguepAQuQ` | 53.3 | 44.4 | -8.9 | 5 | 8 | 10 |
| `jV8DwutbXbg` | 77.8 | 70.0 | -7.8 | 7 | 9 | 11 |
| `1aYoIZvabbk` | 90.9 | 83.3 | -7.6 | 6 | 7 | 5 |
| `90rWUjKjnAE` | 100.0 | 95.2 | -4.8 | 10 | 11 | 10 |
| `2XVgpMwY5iE` | 85.7 | 83.3 | -2.4 | 9 | 12 | 12 |
| `2e3vOxsHekE` | 100.0 | 100.0 | +0.0 | 6 | 6 | 6 |
| `H2fOkeXxpyw` | 88.9 | 88.9 | +0.0 | 8 | 8 | 10 |
| `BZ32w0SSAoY` | 77.4 | 78.8 | +1.4 | 12 | 14 | 19 |
| `FfSNnH2bbNc` | 75.0 | 78.8 | +3.8 | 13 | 14 | 19 |
| `6CgqEzyWpeA` | 85.7 | 91.9 | +6.2 | 16 | 18 | 19 |
| `ww5fiygF6eg` | 75.0 | 82.4 | +7.4 | 12 | 14 | 20 |
| `7V8wTCkjOqo` | 53.3 | 60.9 | +7.5 | 8 | 16 | 7 |
| `SSWwnNVYi_Q` | 62.5 | 72.7 | +10.2 | 6 | 12 | 10 |
| `Cgv0kfp_6xQ` | 81.5 | 100.0 | +18.5 | 13 | 14 | 14 |
