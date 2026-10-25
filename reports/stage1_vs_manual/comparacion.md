# Stage 1 contra la transcripción manual — panel de 30

Cada World Model se reduce a servicios y pares de servicio, igual que el evaluador. «vs manual» mide cuánto coincide con lo que una persona leyó en la pizarra; «vs GT» es el techo que tendría Stage 2 si copiara ese World Model sin tocarlo.

| World Model | entidades | conexiones | sin resolver | servicios F1 vs manual | conexiones P / R / F1 vs manual | servicios F1 vs GT | conexiones F1 vs GT |
|---|---:|---:|---:|---:|:---:|---:|---:|
| `s1-flash` | 9.03 | 8.27 | 0 | 86.93 | 65.0 / 63.0 / 63.07 | 84.52 | 52.40 |
| `s1-pro` | 9.67 | 8.90 | 0 | 86.39 | 62.4 / 63.2 / 61.64 | 83.18 | 50.59 |
| `s1-claude` | 9.40 | 8.73 | 4 | 84.36 | 67.7 / 68.7 / 66.99 | 81.02 | 52.81 |
| `s1-flash-img` | 8.83 | 8.17 | 0 | 89.49 | 69.3 / 66.4 / 66.75 | 85.74 | 53.34 |
| `s1-pro-img` | 9.40 | 8.37 | 0 | 91.79 | 71.1 / 70.6 / 69.87 | 83.24 | 52.72 |
| `s1-claude-img` | 9.33 | 8.57 | 6 | 86.24 | 69.7 / 69.2 / 68.47 | 82.73 | 52.31 |
| `vision` | 9.00 | 8.63 | 0 | 100.00 | 100.0 / 100.0 / 100.00 | 87.36 | 57.60 |

Ground truth: 8.73 nodos y 12.03 aristas por arquitectura.

## Diferencias pareadas (B − A)

| A | B | métrica | Δ | IC 95 % | gana B / gana A / empate | p (signos) |
|---|---|---|---:|:---:|:---:|---:|
| `s1-flash` | `s1-pro` | conexiones F1 vs manual | -1.43 | [-11.45, +7.95] | 11 / 13 / 6 | 0.839 |
| `s1-flash` | `s1-pro` | servicios F1 vs manual | -0.55 | [-7.29, +4.76] | 9 / 10 / 11 | 1.000 |
| `s1-flash` | `s1-pro` | conexiones F1 vs GT | -1.80 | [-9.99, +5.32] | 10 / 13 / 7 | 0.678 |
| `s1-flash` | `s1-pro` | servicios F1 vs GT | -1.34 | [-7.25, +2.95] | 9 / 10 / 11 | 1.000 |
| `s1-flash` | `s1-claude` | conexiones F1 vs manual | +3.91 | [-3.61, +12.01] | 16 / 12 / 2 | 0.572 |
| `s1-flash` | `s1-claude` | servicios F1 vs manual | -2.58 | [-7.02, +1.70] | 9 / 12 / 9 | 0.664 |
| `s1-flash` | `s1-claude` | conexiones F1 vs GT | +0.41 | [-4.92, +5.82] | 11 / 12 / 7 | 1.000 |
| `s1-flash` | `s1-claude` | servicios F1 vs GT | -3.50 | [-7.79, +0.56] | 8 / 11 / 11 | 0.648 |
| `s1-flash` | `s1-flash-img` | conexiones F1 vs manual | +3.67 | [-4.86, +12.38] | 14 / 11 / 5 | 0.690 |
| `s1-flash` | `s1-flash-img` | servicios F1 vs manual | +2.55 | [-1.44, +6.72] | 9 / 6 / 15 | 0.607 |
| `s1-flash` | `s1-flash-img` | conexiones F1 vs GT | +0.94 | [-5.65, +7.26] | 15 / 11 / 4 | 0.557 |
| `s1-flash` | `s1-flash-img` | servicios F1 vs GT | +1.22 | [-2.11, +4.46] | 9 / 5 / 16 | 0.424 |
| `s1-flash` | `s1-pro-img` | conexiones F1 vs manual | +6.79 | [-2.81, +16.83] | 14 / 10 / 6 | 0.541 |
| `s1-flash` | `s1-pro-img` | servicios F1 vs manual | +4.86 | [+0.30, +9.62] | 11 / 7 / 12 | 0.481 |
| `s1-flash` | `s1-pro-img` | conexiones F1 vs GT | +0.32 | [-4.78, +5.49] | 11 / 10 / 9 | 1.000 |
| `s1-flash` | `s1-pro-img` | servicios F1 vs GT | -1.28 | [-4.84, +2.29] | 5 / 9 / 16 | 0.424 |
| `s1-flash` | `s1-claude-img` | conexiones F1 vs manual | +5.40 | [-2.23, +13.79] | 13 / 12 / 5 | 1.000 |
| `s1-flash` | `s1-claude-img` | servicios F1 vs manual | -0.69 | [-5.03, +3.74] | 9 / 11 / 10 | 0.824 |
| `s1-flash` | `s1-claude-img` | conexiones F1 vs GT | -0.09 | [-4.94, +5.01] | 10 / 11 / 9 | 1.000 |
| `s1-flash` | `s1-claude-img` | servicios F1 vs GT | -1.80 | [-5.59, +2.00] | 8 / 11 / 11 | 0.648 |
| `s1-flash` | `vision` | conexiones F1 vs GT | +5.20 | [+0.36, +10.56] | 14 / 9 / 7 | 0.405 |
| `s1-flash` | `vision` | servicios F1 vs GT | +2.84 | [+0.56, +5.45] | 11 / 5 / 14 | 0.210 |
| `s1-pro` | `s1-claude` | conexiones F1 vs manual | +5.34 | [-2.45, +14.26] | 15 / 11 / 4 | 0.557 |
| `s1-pro` | `s1-claude` | servicios F1 vs manual | -2.03 | [-7.25, +4.52] | 10 / 14 / 6 | 0.541 |
| `s1-pro` | `s1-claude` | conexiones F1 vs GT | +2.22 | [-5.48, +11.38] | 12 / 11 / 7 | 1.000 |
| `s1-pro` | `s1-claude` | servicios F1 vs GT | -2.16 | [-8.08, +5.17] | 9 / 14 / 7 | 0.405 |
| `s1-pro` | `s1-flash-img` | conexiones F1 vs manual | +5.10 | [-4.21, +15.20] | 19 / 7 / 4 | 0.029 |
| `s1-pro` | `s1-flash-img` | servicios F1 vs manual | +3.10 | [-1.85, +9.59] | 13 / 7 / 10 | 0.263 |
| `s1-pro` | `s1-flash-img` | conexiones F1 vs GT | +2.75 | [-4.82, +10.93] | 13 / 10 / 7 | 0.678 |
| `s1-pro` | `s1-flash-img` | servicios F1 vs GT | +2.56 | [-2.07, +8.60] | 11 / 7 / 12 | 0.481 |
| `s1-pro` | `s1-pro-img` | conexiones F1 vs manual | +8.22 | [+0.36, +16.98] | 15 / 7 / 8 | 0.134 |
| `s1-pro` | `s1-pro-img` | servicios F1 vs manual | +5.40 | [+0.99, +11.16] | 12 / 4 / 14 | 0.077 |
| `s1-pro` | `s1-pro-img` | conexiones F1 vs GT | +2.13 | [-4.07, +8.95] | 12 / 10 / 8 | 0.832 |
| `s1-pro` | `s1-pro-img` | servicios F1 vs GT | +0.06 | [-4.56, +5.94] | 6 / 9 / 15 | 0.607 |
| `s1-pro` | `s1-claude-img` | conexiones F1 vs manual | +6.83 | [-0.17, +14.97] | 16 / 8 / 6 | 0.152 |
| `s1-pro` | `s1-claude-img` | servicios F1 vs manual | -0.14 | [-5.50, +6.42] | 11 / 11 / 8 | 1.000 |
| `s1-pro` | `s1-claude-img` | conexiones F1 vs GT | +1.71 | [-5.00, +9.69] | 10 / 12 / 8 | 0.832 |
| `s1-pro` | `s1-claude-img` | servicios F1 vs GT | -0.45 | [-5.78, +5.72] | 9 / 11 / 10 | 0.824 |
| `s1-pro` | `vision` | conexiones F1 vs GT | +7.00 | [-0.41, +15.76] | 13 / 13 / 4 | 1.000 |
| `s1-pro` | `vision` | servicios F1 vs GT | +4.18 | [-0.18, +10.08] | 12 / 7 / 11 | 0.359 |
| `s1-claude` | `s1-flash-img` | conexiones F1 vs manual | -0.24 | [-7.46, +6.69] | 12 / 14 / 4 | 0.845 |
| `s1-claude` | `s1-flash-img` | servicios F1 vs manual | +5.13 | [+0.98, +9.23] | 16 / 5 / 9 | 0.027 |
| `s1-claude` | `s1-flash-img` | conexiones F1 vs GT | +0.53 | [-4.25, +5.29] | 13 / 12 / 5 | 1.000 |
| `s1-claude` | `s1-flash-img` | servicios F1 vs GT | +4.72 | [+1.06, +8.66] | 12 / 4 / 14 | 0.077 |
| `s1-claude` | `s1-pro-img` | conexiones F1 vs manual | +2.88 | [-3.93, +9.05] | 14 / 10 / 6 | 0.541 |
| `s1-claude` | `s1-pro-img` | servicios F1 vs manual | +7.43 | [+3.69, +11.15] | 17 / 4 / 9 | 0.007 |
| `s1-claude` | `s1-pro-img` | conexiones F1 vs GT | -0.09 | [-5.39, +5.23] | 10 / 9 / 11 | 1.000 |
| `s1-claude` | `s1-pro-img` | servicios F1 vs GT | +2.22 | [-1.43, +6.04] | 9 / 8 / 13 | 1.000 |
| `s1-claude` | `s1-claude-img` | conexiones F1 vs manual | +1.48 | [-4.10, +7.25] | 8 / 5 / 17 | 0.581 |
| `s1-claude` | `s1-claude-img` | servicios F1 vs manual | +1.89 | [-1.62, +5.57] | 6 / 3 / 21 | 0.508 |
| `s1-claude` | `s1-claude-img` | conexiones F1 vs GT | -0.51 | [-4.61, +3.49] | 7 / 6 / 17 | 1.000 |
| `s1-claude` | `s1-claude-img` | servicios F1 vs GT | +1.71 | [-1.20, +5.04] | 6 / 4 / 20 | 0.754 |
| `s1-claude` | `vision` | conexiones F1 vs GT | +4.79 | [+0.18, +9.37] | 16 / 7 / 7 | 0.093 |
| `s1-claude` | `vision` | servicios F1 vs GT | +6.34 | [+2.86, +10.05] | 16 / 6 / 8 | 0.052 |
| `s1-flash-img` | `s1-pro-img` | conexiones F1 vs manual | +3.12 | [-2.36, +9.09] | 11 / 11 / 8 | 1.000 |
| `s1-flash-img` | `s1-pro-img` | servicios F1 vs manual | +2.30 | [-1.21, +5.95] | 10 / 10 / 10 | 1.000 |
| `s1-flash-img` | `s1-pro-img` | conexiones F1 vs GT | -0.62 | [-6.26, +5.77] | 10 / 13 / 7 | 0.678 |
| `s1-flash-img` | `s1-pro-img` | servicios F1 vs GT | -2.50 | [-5.40, +0.44] | 4 / 13 / 13 | 0.049 |
| `s1-flash-img` | `s1-claude-img` | conexiones F1 vs manual | +1.72 | [-5.15, +8.65] | 14 / 12 / 4 | 0.845 |
| `s1-flash-img` | `s1-claude-img` | servicios F1 vs manual | -3.24 | [-6.74, +0.44] | 6 / 14 / 10 | 0.115 |
| `s1-flash-img` | `s1-claude-img` | conexiones F1 vs GT | -1.04 | [-6.58, +4.50] | 13 / 13 / 4 | 1.000 |
| `s1-flash-img` | `s1-claude-img` | servicios F1 vs GT | -3.01 | [-6.51, +0.35] | 4 / 12 / 14 | 0.077 |
| `s1-flash-img` | `vision` | conexiones F1 vs GT | +4.26 | [-1.65, +10.29] | 15 / 11 / 4 | 0.557 |
| `s1-flash-img` | `vision` | servicios F1 vs GT | +1.62 | [-1.24, +4.60] | 9 / 9 / 12 | 1.000 |
| `s1-pro-img` | `s1-claude-img` | conexiones F1 vs manual | -1.40 | [-6.82, +3.94] | 13 / 12 / 5 | 1.000 |
| `s1-pro-img` | `s1-claude-img` | servicios F1 vs manual | -5.55 | [-8.92, -2.12] | 4 / 15 / 11 | 0.019 |
| `s1-pro-img` | `s1-claude-img` | conexiones F1 vs GT | -0.42 | [-5.01, +4.03] | 10 / 10 / 10 | 1.000 |
| `s1-pro-img` | `s1-claude-img` | servicios F1 vs GT | -0.51 | [-3.83, +2.77] | 7 / 6 / 17 | 1.000 |
| `s1-pro-img` | `vision` | conexiones F1 vs GT | +4.88 | [+0.78, +9.23] | 15 / 9 / 6 | 0.307 |
| `s1-pro-img` | `vision` | servicios F1 vs GT | +4.12 | [+1.94, +6.41] | 15 / 3 / 12 | 0.008 |
| `s1-claude-img` | `vision` | conexiones F1 vs GT | +5.29 | [+0.74, +9.83] | 18 / 6 / 6 | 0.023 |
| `s1-claude-img` | `vision` | servicios F1 vs GT | +4.63 | [+1.68, +7.75] | 15 / 4 / 11 | 0.019 |
