# Fase 0 · Diagnóstico sin API

Script: `scripts/reglas/fase0_diagnostico.py` · datos: `fase0_resumen.json`, `fase0_errores_por_video.csv`, `particion.json`.

## Partición

Los 321 grafos puntuables del paper, menos los 30 del panel, se reparten con semilla 42:

| Conjunto | Videos | Uso |
|---|---|---|
| Inducción | 218 | lo único que miran esta fase y los agentes |
| Validación | 73 | decidir qué reglas se quedan |
| Prueba | 30 (panel) | una sola evaluación al final |

El F1 de aristas recalculado coincide con `results.csv` en los 218 videos. En inducción, la producción (V6, Flash) da **60,58**.

## Errores de producción en inducción

Cada arista que falta (FN) o sobra (FP) cae en una sola clase. La última columna es el F1 si solo esa clase se corrigiera entera. Es el techo de una regla dirigida a ella; las ganancias no se suman.

| Clase | FN | FP | Videos | F1 si se corrige | Ganancia |
|---|---|---|---|---|---|
| Nodo faltante (el servicio no está) | 382 | — | 130 | 70,83 | +10,25 |
| **Retorno omitido** (está la ida, falta la vuelta) | 414 | — | 144 | 70,29 | **+9,72** |
| Subtipo de actor (UserConsumerWeb vs UserCompanyAgent…) | 134 | 134 | 89 | 66,57 | +5,99 |
| Conexión omitida (ambos nodos están, sin arista) | 199 | — | 86 | 66,49 | +5,91 |
| Nodo alucinado | — | 200 | 86 | 63,14 | +2,56 |
| Repetición omitida (par repetido colapsado) | 106 | — | 60 | 63,07 | +2,49 |
| Conexión extra | — | 139 | 87 | 62,55 | +1,98 |
| Dirección invertida | 31 | 31 | 23 | 61,90 | +1,32 |
| Repetición extra | — | 32 | 17 | 61,14 | +0,56 |
| Retorno extra | — | 16 | 13 | 60,83 | +0,25 |

La dirección casi nunca está mal (+1,32). Lo que falta es la vuelta.

## Consistencia del ground truth (inducción)

**Retornos.** El 40,7 % de los pares conectados tiene ida y vuelta, pero varía mucho entre grafos: 35 grafos no tienen ninguno y 66 tienen más de la mitad.

Para predecir si un par concreto lleva vuelta, dejándolo fuera de los datos de referencia:

| Predictor | Exactitud |
|---|---|
| La tasa global | 53,3 % |
| El mismo par de servicios en los otros grafos | 58,7 % |
| **Los otros pares del mismo grafo** | **69,5 %** |

La vuelta es sobre todo un **estilo del grafo** (de quien anotó o del video), no una propiedad del par de servicios.

**¿Qué rinde aplicar una regla de retornos a la producción?**

| Política | F1 de aristas |
|---|---|
| Nunca agregar la vuelta (producción) | 60,58 |
| Siempre agregarla | 58,60 |
| Agregarla solo en los grafos mayormente bidireccionales (oráculo de estilo) | 64,77 |

Una regla uniforme empeora el resultado. Saber el estilo de cada grafo vale hasta +4,2.

**Dirección.** Cuando una arista va en un solo sentido, el 80,6 % de las veces sigue la dirección mayoritaria de ese par en los demás grafos. Algunos pares no se invierten nunca: ApiGateway→Lambda, SNS→SQS, Firehose→S3 y DynamoDB→Lambda (el dato sale de la tabla hacia la función).

**Presencia.** Para pares de servicios que aparecen juntos en 3 o más grafos, la convención predice si están conectados con un 76,5 % de exactitud. Recupera solo el 36,8 % de las aristas reales, con precisión de 67,4 %. El resto de la topología depende del video.

**Señal hablada.** Correlación de Spearman entre la fracción bidireccional del grafo y la frecuencia de verbos en la transcripción:

| Verbos | ρ |
|---|---|
| De respuesta ("returns", "responds", "back to") | 0,06 |
| De lectura ("reads", "queries", "fetches") | 0,21 |

Los verbos de respuesta no predicen el estilo. Los de lectura, apenas.

**Otros datos:**
- 200 de 218 grafos tienen al menos un actor.
- Tipos de arista: 81 % data y 19 % meta.
- Mediana de 11 aristas y 3 flujos por grafo.

## Qué implica para la fase 1

1. Hay **convenciones firmes** que se pueden escribir como código:
   - la dirección por par cuando la arista es de un solo sentido,
   - el subtipo de actor,
   - los pares que nunca se invierten.
2. El **retorno**, que es la clase de error más grande, no es una regla fija. Es una decisión por grafo. Los agentes deben buscar qué señal del video la predice (techo: +4,2), y aplicarla sin esa señal empeora el resultado.
3. El "100 %" no es alcanzable por convención:
   - la dirección es consistente en un 80 %,
   - la decisión de retorno en un 70 %,
   - la presencia de aristas depende del video en dos tercios.

   Esos son los techos contra los que hay que leer cualquier mejora.
