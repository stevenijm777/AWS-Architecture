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
| Service F1 | 85.90 | 85.04 | -0.86 | [-2.88, +1.52] | 2 / 7 / 21 | 0.180 |
| Edge F1 | 57.12 | 56.07 | -1.04 | [-5.09, +3.05] | 6 / 11 / 13 | 0.332 |

## Piso de ruido (4 réplicas de gemini-3.6-flash, mismo prompt, sin ww5fiygF6eg)

Cuánto difiere Flash de sí mismo entre corridas, sobre los mismos videos. La diferencia entre modelos solo cuenta como efecto si sale de este rango.

| métrica | medias de las réplicas | réplica − A (rango) | B − A en esos videos | ¿|B − A| supera al mayor |réplica − A|? |
|---|---|:---:|---:|:---:|
| Service F1 | 87.88, 86.82, 86.98, 85.88 | [-0.03, +1.98] | -0.69 | no |
| Edge F1 | 59.79, 58.63, 58.62, 58.63 | [+0.76, +1.93] | -1.73 | no |

## Por video (Edge F1, ordenado por diferencia)

| video | gemini-3.6-flash | gemini-3.1-pro-preview | Δ | aristas A | aristas B | aristas GT |
|---|---:|---:|---:|---:|---:|---:|
| `BlCXEMp_lqY` | 71.4 | 42.9 | -28.6 | 5 | 5 | 9 |
| `H2fOkeXxpyw` | 82.4 | 60.0 | -22.4 | 7 | 10 | 10 |
| `f5EJBUfGZtw` | 77.8 | 60.0 | -17.8 | 10 | 12 | 8 |
| `2L0m28ZLmtE` | 72.7 | 61.5 | -11.2 | 11 | 15 | 11 |
| `6YkguepAQuQ` | 57.1 | 47.1 | -10.1 | 4 | 7 | 10 |
| `a6kqyqTNJM4` | 25.0 | 15.4 | -9.6 | 9 | 11 | 15 |
| `7V8wTCkjOqo` | 26.7 | 20.0 | -6.7 | 8 | 13 | 7 |
| `JYeXbUdFOdw` | 44.4 | 37.8 | -6.6 | 13 | 23 | 14 |
| `c-1GXhOOOww` | 30.8 | 26.3 | -4.5 | 10 | 22 | 16 |
| `9qTEHITVeLE` | 40.0 | 37.0 | -3.0 | 11 | 13 | 14 |
| `2XVgpMwY5iE` | 45.5 | 43.5 | -2.0 | 10 | 11 | 12 |
| `-kA0ahrhX3I` | 50.0 | 50.0 | +0.0 | 8 | 8 | 8 |
| `1aYoIZvabbk` | 83.3 | 83.3 | +0.0 | 7 | 7 | 5 |
| `2e3vOxsHekE` | 83.3 | 83.3 | +0.0 | 6 | 6 | 6 |
| `6CgqEzyWpeA` | 74.3 | 74.3 | +0.0 | 16 | 16 | 19 |
| `6EUknQqaV1w` | 78.3 | 78.3 | +0.0 | 12 | 12 | 11 |
| `Cgv0kfp_6xQ` | 83.3 | 83.3 | +0.0 | 10 | 10 | 14 |
| `wjtSHyENv0I` | 54.5 | 54.5 | +0.0 | 8 | 8 | 14 |
| `90rWUjKjnAE` | 66.7 | 66.7 | +0.0 | 8 | 8 | 10 |
| `FfSNnH2bbNc` | 48.3 | 48.3 | +0.0 | 10 | 10 | 19 |
| `SSWwnNVYi_Q` | 50.0 | 50.0 | +0.0 | 6 | 6 | 10 |
| `jV8DwutbXbg` | 70.6 | 70.6 | +0.0 | 6 | 6 | 11 |
| `jg85DzUZ9Ac` | 72.7 | 72.7 | +0.0 | 11 | 11 | 11 |
| `u3ZwnulzLnU` | 66.7 | 66.7 | +0.0 | 11 | 11 | 13 |
| `07lfvavMdfU` | 75.0 | 78.6 | +3.6 | 10 | 14 | 14 |
| `hMK2NJ-q9nc` | 25.0 | 30.8 | +5.8 | 11 | 8 | 5 |
| `-wLEkq21cvA` | 50.0 | 63.6 | +13.6 | 10 | 12 | 10 |
| `ww5fiygF6eg` | 35.7 | 54.5 | +18.8 | 8 | 13 | 20 |
| `BZ32w0SSAoY` | 40.0 | 61.1 | +21.1 | 6 | 17 | 19 |
| `-3lnf5lzsH0` | 32.0 | 60.0 | +28.0 | 9 | 14 | 16 |
