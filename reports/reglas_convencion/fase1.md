# Fase 1 · Reglas firmes y debate sobre retornos

Scripts:
- `scripts/reglas/fase1a_huella_y_reglas.py` (sin API)
- `scripts/reglas/fase1b_debate_retornos.py` (gemini-3.8-flash)
- prompts en `scripts/reglas/prompts/`

Datos:
- `fase1a_resumen.json`
- `fase1b/` (reparto, rondas, final)
- `llamadas.jsonl`

## 1a · Reglas firmes por par (código)

Las reglas se estiman en inducción con soporte ≥ 5 grafos y proporción ≥ 0,8, y se aplican a los grafos de producción:
- **Invertir:** 19 pares.
- **Ida y vuelta:** 7 pares, por ejemplo Aurora–Lambda, EC2–ElastiCache y EMR–S3.
- **Actor:** 1 cambio (UserConsumerWebMobile → UserConsumerMobile).

| Reglas | Inducción (218) | Validación (73) |
|---|---|---|
| Ninguna | 60,58 | 58,10 |
| Actor | 60,87 | 59,00 |
| Invertir | 60,41 | 57,64 |
| Ida y vuelta | 61,10 | 58,34 |
| Actor + ida y vuelta + invertir | 61,23 | 58,79 |

Todas juntas aportan **+0,7**, muy por debajo del MDE de 3,29. Invertir empeora.

**Huella de anotación.** Ningún rasgo del GT separa los grafos con retornos de los sin retornos. Los rasgos probados fueron las primas en `seq`, las notas en aristas, las notas del grafo y el formato de `seq`. Además, las primas no marcan retornos: solo el 51,9 % de las aristas primadas tiene la inversa.

**Señales disponibles al inferir.** Ninguna pasa de ρ = 0,23 con la fracción bidireccional del GT. Las probadas fueron el largo de la transcripción, los nodos, aristas y almacenes generados, y la fracción bidireccional del propio grafo generado.

## 1b · Debate proponente–escéptico

| Ronda | Hipótesis | Exactitud balanceada | Mejor F1 con la política | F1 sin agregar | Oráculo de estilo |
|---|---|---|---|---|---|
| 1 (proponente, lote de 100) | 5 | 48,9–59,6 % | 61,46 | 61,30 | 65,65 |
| 2 (escéptico, lote de 102) | 4 | 46,8–54,0 % | 60,33 | 60,13 | 63,69 |
| Validación (la mejor de la ronda 2) | 1 | 50,9 % | 59,83 | 59,01 | 63,37 |

La hipótesis elegida dice que la narración describe un servicio interno que consulta a otro antes de seguir.
- En validación solo dijo "sí" en 4 de 63 videos (el clasificador omitió 10 de los 73).
- Su exactitud es la del azar, así que el +0,8 viene de esos 4 videos y no es señal.

17 llamadas: 365 mil tokens de entrada y 367 mil de salida más thinking, **$1,65**.

## Conclusión

Decidir si un grafo lleva retornos vale hasta +4 puntos con un oráculo, pero no se puede predecir con ninguna de estas fuentes:
- el par de servicios,
- la huella de anotación,
- rasgos del grafo generado,
- preguntas sobre la narración que el propio LLM formuló y refinó.

Sale cerca del azar en todos los casos. La evidencia apunta a una **variación de anotación** que el video no determina. Esa parte de la brecha de aristas es techo del ground truth, no error del modelo.

Las convenciones que sí son firmes (dirección por par y subtipo de actor) suman menos de un punto. Las clases de error que quedan con margen grande son de contenido, no de convención:
- servicio no detectado: +10,3,
- conexión omitida entre nodos presentes: +5,9.
