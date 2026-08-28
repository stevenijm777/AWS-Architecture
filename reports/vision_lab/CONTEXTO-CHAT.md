# Contexto para el chat del experimento de visión (oráculo de Stage 1)

Pegá este archivo entero al abrir el chat nuevo. Está pensado para que alguien que
arranca en frío pueda trabajar sin el historial previo.

---

## Qué se está intentando

El pipeline **Standard** tiene dos etapas: Stage 1 (*Modeler*) mira el frame de la
pizarra y produce un **World Model** (`entities` + `visual_connections`); Stage 2
(*Planner*) lo convierte en el grafo final (`nodes` + `edges`).

El Edge F1 del pipeline está clavado en ~59 % y **cuatro intervenciones distintas
sobre el prompt de Stage 2 dieron resultado nulo** (11 variantes de prompt,
few-shot RAG, inyección de topología detectada por visión por computadora, y
correcciones dirigidas a los errores más frecuentes).

El **experimento del oráculo** responde la pregunta que queda: *si Stage 1 fuera
perfecto, ¿cuánto mejora Stage 2?* Se le pasa a Stage 2 un World Model
**transcrito a mano por un humano** desde la pizarra — la "trampa" — en lugar del
que genera el modelo.

- Si la mejora es **poca** → el techo es de la tarea o del ground truth.
- Si es **mucha** → hay que invertir en Stage 1.

Cuesta 12 llamadas a la API (o más, si se completan las trampas que faltan).

---

## La herramienta

```bash
.venv/bin/python scripts/ablation/vision_lab.py
# abre http://localhost:8765
```

Fuente: `scripts/ablation/vision_lab.py`. Es un servidor local con `http.server`
(sin dependencias extra), no un HTML suelto.

**Por qué servidor y no archivo estático:** el renderizador de grafos es Node
(`graph_renderer/render_graph.mjs`) y necesita disco, así que un HTML suelto no
puede llamarlo. Una primera versión dibujaba los grafos en el navegador con un
layout propio y se veía mal.

### Qué hace

1. Genera las imágenes que falten (GT, Standard, Parsimonious, trampa) para los
   30 videos del panel. Saltea las que ya existen. `--rerender` fuerza todo.
2. Sirve la página de comparación: por video, la pizarra a ancho completo y
   debajo cuatro grafos en fila. Clic para ampliar.
3. `POST /render` — recibe un JSON, lo pasa a graphml, lo renderiza con el mismo
   motor y devuelve el PNG. Es el renderizador único al final de la página.
4. Guarda las anotaciones en `reports/vision_lab/annotations.json` (en disco, no
   en el navegador).

### Formatos que acepta el renderizador

Detecta los dos solo:

**World Model** (el que recibe Stage 2 — es el que hay que escribir):
```json
{
  "entities": [
    {"service":"S3","name":"S3","type":"S3","rationale":"bucket arriba a la izquierda"}
  ],
  "visual_connections": [
    {"source_label":"S3","target_label":"STEP FUNCTIONS",
     "arrow_direction":"right","description":"flecha sólida"}
  ]
}
```
Las conexiones referencian entidades por `name` o `service`, **no por índice**.

**Grafo Cloudscape** (el del ground truth y la salida de Stage 2):
```json
{"nodes":[{"id":"0","service":"S3","name":"","notes":""}],
 "edges":[{"source":"0","target":"1","flow_id":0,"seq":"1","type":"data","notes":""}]}
```

Avisa automáticamente de tres cosas: etiquetas que no resuelven, entidades sin
ninguna conexión, y servicios fuera del catálogo de Cloudscape.

---

## Un cambio que toca infraestructura compartida

`graph_renderer/render_graph.mjs` apila **una capa entera sobre el eje Y**:

```js
x: l * vSpacing,            // la capa va al eje X
y: startY + i * hSpacing,   // la posición dentro de la capa va al eje Y
```

El ground truth de Cloudscape tiene casi todos los nodos con grado de entrada 0,
o sea **todos en la misma capa**, y salía como una tira de 857×4518 px ilegible.

Se le agregó un modo compacto que parte las capas grandes en varias columnas,
**detrás de `RG_COMPACT=1` y apagado por defecto**. Es opt-in a propósito: ese
renderizador también alimenta el pipeline **Parsimonious de Melissa**, y no
corresponde cambiarle la salida sin avisarle.

Resultado: `-3lnf5lzsH0` pasó de 857×4518 a 1932×1651. Relación alto/ancho del
ground truth: de 3.07 de mediana a 0.84.

> **Regla del proyecto:** nunca modificar `data/graphs_parsimonious*` ni
> `vision_analyzer_parsimonious.py` sin preguntar. Son archivos de Melissa.

---

## Estado actual

**12 de 30 trampas hechas**, en
`whiteboard_selection_lab/lab_workspace/<vid>/world_model_vision.json`:

```
-3lnf5lzsH0  -kA0ahrhX3I  -wLEkq21cvA  07lfvavMdfU  1aYoIZvabbk  2e3vOxsHekE
6CgqEzyWpeA  6EUknQqaV1w  6YkguepAQuQ  BZ32w0SSAoY  Cgv0kfp_6xQ  wjtSHyENv0I
```

**18 faltan.** Dos son del panel de 14 (`2L0m28ZLmtE`, `ww5fiygF6eg`) y 16 son
del ensanche. En la página se aíslan con el filtro *"Sin trampa — por hacer"*.

Total en las 12 hechas: 103 entidades, 91 conexiones. Todos los servicios están
en el catálogo, así que todos los iconos renderizan.

### Defecto conocido, sin corregir a propósito

`6YkguepAQuQ` declara `CLOUDFRONT → VPC`, pero **no existe una entidad CloudFront**
en ese archivo — hay **CloudFormation**. Es un typo de transcripción que deja la
arista colgando. No se tocó: es la lectura humana de la pizarra, la corrección le
corresponde a quien la escribió.

Además hay entidades huérfanas (sin ninguna conexión) en 7 de los 12. Pueden ser
legítimas si se dibujó una caja sin flechas, pero vale revisarlas.

### Advertencia al revisar

**Verificar contra el JSON antes de marcar algo como mal transcrito.** En
`07lfvavMdfU` parecía haber un `Rekognition → Comprehend` y en realidad el JSON
dice `REKOGNITION → DYNAMODB`, que es correcto: el layout alinea nodos en columnas
y una arista larga *parece* pasar por un nodo intermedio.

---

## Lo que falta para correr el experimento

1. **Revisión visual de las 12** — confirmar que cada JSON representa fielmente su
   pizarra. Es el paso que habilita interpretar el resultado.
2. **Completar las trampas que se quieran** — más videos, más potencia.
3. **Agregar modo oráculo a `scripts/ablation/rerun_panel.py`** — hoy **no existe**.
   Hace falta que lea `world_model_vision.json` en lugar de `world_model.json`,
   se restrinja a los videos que tengan trampa, y use un tag de checkpoint y un
   sufijo de salida propios para no colisionar con las corridas normales.
   El runner ya tiene `--replicate N`, que es el patrón a imitar.
4. **Correr** con `src/configs/prompts/stage2_v6_corrected__cell9.txt`
   (sha `ed1d85054d73`, es byte-idéntico al de producción).

### La trampa de la comparación — no equivocarse acá

El resultado del oráculo **no se compara** contra las cifras del panel de 14 ni
del de 30. Hay 12 trampas, así que la referencia es **producción sobre esos mismos
12 videos**. Un cálculo previo dio **Svc 88.98 · Edge 64.97**, más alto que el
panel completo de 14 (89.79 / 63.21) — usar el número del panel de 14
sobreestimaría el beneficio del oráculo en ~1.8 puntos.

**Recalcular esa referencia antes de usarla**, porque ahora existen dos corridas
completas de producción sobre el panel de 30
(`2026-08-25_1637_..._p30` y `2026-08-27_1640_..._p30_rep2`) y conviene promediar
o reportar ambas.

---

## Restricción de API que condiciona todo

El tier gratuito da **20 requests por día, por proyecto, por modelo**:

```
id    : GenerateRequestsPerDayPerProjectPerModel-FreeTier
valor : 20
```

Hay **12 llaves configuradas pero solo 8 vivas** — 3 devuelven 401 (revocadas) y
1 tiene un carácter no-ASCII (mal pegada en el `.env`). Techo real: **~160
llamadas diarias**.

El `retryDelay: 39s` que devuelve la API es engañoso: es un tope diario, no se
despeja esperando. `rerun_panel.py` ya distingue los dos casos (retira la llave
si el error dice `PerDay`, rota si es por minuto) y guarda checkpoint después de
cada video, así que cortar y retomar no re-paga nada.

---

## Contexto de por qué esto importa

Se midió el piso de ruido del proyecto y el resultado reencuadra todo:

- Temperatura 0.0 **no es determinista**: 0 de 170 salidas byte-idénticas.
- sigma_d por video: **8.76 puntos** de Edge F1.
- Efecto mínimo detectable a n=30: **4.48 puntos**.
- El rango completo de las 10 variantes de prompt en el panel de 30 es **3.00
  puntos** — la tabla de ablación entera cabe adentro del ruido.
- sigma_d entre prompts *distintos* 8.54 vs 8.76 entre réplicas del *mismo*
  prompt: razón **0.99**.

Por eso el oráculo es el experimento que queda: no pregunta por el prompt, que ya
se descartó como palanca, sino por la calidad de la entrada.

Script del análisis: `scripts/ablation/measure_noise_floor.py` (cero API, lee los
`run.json` existentes). Salida en `reports/noise_floor.json`.
