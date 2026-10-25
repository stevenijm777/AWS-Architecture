# claude-opus-5-5 vs gemini-3.6-flash — panel de 30 videos

Stage 2: `STAGE2_V6_CORRECTED` (sha `ed1d85054d73`), temperatura 0, mismo World Model de Stage 1 para ambos modelos.

## Controles

- ✓ mismo panel
- ✓ mismo prompt Stage 2
- ✗ mismo World Model por video
- ✓ misma pizarra por video
- ✓ panel completo en ambas

## Resultado

| métrica | gemini-3.6-flash | claude-opus-5-5 | Δ (B − A) | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---:|---:|---:|:---:|:---:|---:|
| Service F1 | 99.70 | 98.71 | -0.99 | [-1.98, -0.18] | 0 / 4 / 26 | 0.125 |
| Edge F1 | 83.18 | 82.89 | -0.30 | [-2.97, +2.28] | 11 / 8 / 11 | 0.648 |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | claude-opus-5-5 | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `a6kqyqTNJM4` | 69.2 | 50.0 | -19.2 | 11 | 13 | 15 |
| `c-1GXhOOOww` | 78.8 | 63.4 | -15.4 | 17 | 25 | 16 |
| `2L0m28ZLmtE` | 95.2 | 83.3 | -11.9 | 10 | 13 | 11 |
| `6YkguepAQuQ` | 53.3 | 42.1 | -11.2 | 5 | 9 | 10 |
| `wjtSHyENv0I` | 78.3 | 72.0 | -6.3 | 9 | 11 | 14 |
| `90rWUjKjnAE` | 100.0 | 95.2 | -4.8 | 10 | 11 | 10 |
| `Cgv0kfp_6xQ` | 81.5 | 76.9 | -4.6 | 13 | 12 | 14 |
| `-wLEkq21cvA` | 85.7 | 83.3 | -2.4 | 11 | 14 | 10 |
| `-3lnf5lzsH0` | 93.3 | 93.3 | +0.0 | 14 | 14 | 16 |
| `-kA0ahrhX3I` | 94.1 | 94.1 | +0.0 | 9 | 9 | 8 |
| `1aYoIZvabbk` | 90.9 | 90.9 | +0.0 | 6 | 6 | 5 |
| `2e3vOxsHekE` | 100.0 | 100.0 | +0.0 | 6 | 6 | 6 |
| `ww5fiygF6eg` | 75.0 | 75.0 | +0.0 | 12 | 12 | 20 |
| `BlCXEMp_lqY` | 71.4 | 71.4 | +0.0 | 5 | 5 | 9 |
| `SSWwnNVYi_Q` | 62.5 | 62.5 | +0.0 | 6 | 6 | 10 |
| `f5EJBUfGZtw` | 88.9 | 88.9 | +0.0 | 10 | 10 | 8 |
| `hMK2NJ-q9nc` | 90.9 | 90.9 | +0.0 | 6 | 6 | 5 |
| `jV8DwutbXbg` | 77.8 | 77.8 | +0.0 | 7 | 7 | 11 |
| `jg85DzUZ9Ac` | 100.0 | 100.0 | +0.0 | 11 | 11 | 11 |
| `6EUknQqaV1w` | 90.9 | 91.7 | +0.8 | 11 | 13 | 11 |
| `2XVgpMwY5iE` | 85.7 | 87.0 | +1.2 | 9 | 11 | 12 |
| `FfSNnH2bbNc` | 75.0 | 77.4 | +2.4 | 13 | 12 | 19 |
| `07lfvavMdfU` | 92.3 | 96.3 | +4.0 | 12 | 13 | 14 |
| `u3ZwnulzLnU` | 96.0 | 100.0 | +4.0 | 12 | 13 | 13 |
| `JYeXbUdFOdw` | 80.0 | 84.6 | +4.6 | 11 | 12 | 14 |
| `6CgqEzyWpeA` | 85.7 | 91.9 | +6.2 | 16 | 18 | 19 |
| `7V8wTCkjOqo` | 53.3 | 60.9 | +7.5 | 8 | 16 | 7 |
| `BZ32w0SSAoY` | 77.4 | 85.7 | +8.3 | 12 | 16 | 19 |
| `H2fOkeXxpyw` | 88.9 | 100.0 | +11.1 | 8 | 10 | 10 |
| `9qTEHITVeLE` | 83.3 | 100.0 | +16.7 | 10 | 14 | 14 |
