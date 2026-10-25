# Checklist de revisión del paper

Observaciones de Steven sobre la versión de 11 páginas (ahora `main_v2_marcado.tex`) y estado
en la versión 3 (`main.tex`, compilada como `main_v3.pdf`, 5 páginas).

Versiones en esta carpeta:

- `main_entregado.tex`: la versión entregada original (8 páginas).
- `main_v2_marcado.tex`: la de 11 páginas, con lo nuevo en negrita y lo quitado entre paréntesis.
- `main.tex` / `main_v3.pdf`: la versión 3, limpia, sin Parsimonious.

## Pendiente de Steven

- [ ] **Autoría.** La versión 3 mantiene "Steven Martinez, Melissa Cobos". Quitar a Melissa es
  decisión tuya; no lo toqué.
- [ ] **Qué devolver con la página que sobra.** La versión 3 ocupa 5 páginas y el límite es 6.
  Candidatos que recorté y se podrían devolver: la figura de nodos y aristas generados frente
  a la referencia; el detalle de la elección de fotograma (estaba en 5 párrafos, quedó en 1);
  la tabla de descomposición de la brecha; las lecturas de la etapa 1 con audio.
- [ ] **Gemini 4 Argon en el panel.** Una llamada sobre el video más difícil costó 0,045 USD
  (5 686 tokens de entrada, 3 312 de salida). El panel de 30 en el brazo A costaría unos
  1,3 USD. Sacó 26,3 de F1 de aristas en ese video, donde Flash, Pro y Claude sacan entre
  23,8 y 32,3. Decidir si se corre completo.
- [ ] **Repositorio.** El paper enlaza a `aws-architecture-extraction`, pero todo lo de esta
  revisión (V9, tres modelos, Stage 1, permisivo por modelo, costos, `hipotesis/`) está en
  `AWS-Architecture`. Habría que llevar a ese repositorio lo que respalda las cifras nuevas.

## Criterios generales

- [x] **G1 · Límite de 6 páginas.** Versión 3: 5 páginas.
- [x] **G2 · No contar los errores propios.** Quitado el panel de 14 a 30 y las frases del tipo
  "la versión anterior decía".
- [x] **G3 · Sin explicaciones innecesarias.** Revisado párrafo por párrafo.

## Primera parte

- [x] **1 · Frase del cambio de prompt en el resumen.** Reescrita: "Cuando la segunda etapa
  recibe la referencia como entrada y se le pide conservar sus conexiones, la reproduce
  completa: la brecha está en lo que la pizarra no contiene".
- [x] **2 · Párrafo "Qué medimos y por qué".** Reducido a tres frases dentro de la introducción.
- [x] **3 · Párrafo del panel de 14 a 30.** Quitado.
- [x] **4 · Primer párrafo de la Motivación.** Quitada la sección; los retos (oclusión,
  desconexión multimodal, anotar no es transcribir) pasan al final de la introducción.
- [x] **5 · "La etapa 1 se limita a observar".** Ahora es el objetivo: "La etapa 1 tiene como
  objetivo producir un inventario literal".
- [x] **6 · Por qué la etapa 1 recibe el texto.** Se dice que las dos etapas reciben la
  transcripción porque parte de la arquitectura solo se describe verbalmente, sin afirmar un
  efecto medido en la etapa 1. El único efecto medido es el de la etapa 2 (60,40 → 56,72), y
  está en resultados. En las pruebas de esta semana, quitarle el transcript a la etapa 1 no
  bajó el resultado.
- [x] **7 · "Lógica del negocio".** Sustituida por lo que hace la etapa 2: normalizar al
  catálogo, fusionar o separar iconos repetidos, expandir contenedores, ordenar flujos.
- [x] **8 · "Según su función".** Concretado: fusiona iconos repetidos cuando cumplen el mismo
  papel y los separa cuando hacen pasos distintos.
- [x] **9 · El motivo de dividir en etapas.** Quitada la suposición de que un solo modelo
  inventa. Queda el motivo comprobable: separar las etapas permite medir lectura e
  interpretación por separado.
- [x] **10 · El system prompt de una línea.** Quitado; queda solo que Claude no permite fijar
  la temperatura.

## Segunda parte

- [x] **11 · 370 frente a 385.** Al quitar Parsimonious ya no hace falta comparar conjuntos. El
  texto dice: el sistema procesó 370; sin las no utilizables y las que no tienen conexiones
  quedan 321. Hoy existen grafos para 385, pero las cifras salen de la corrida de 370; no se
  reevaluó.
- [x] **12 · Figura del permisivo por modelo.** Nueva Figura 3: reglas apiladas por modelo, en
  servicios y aristas, con la misma entrada (brazo A).
- [x] **13 · El ejemplo del permisivo.** Se mantiene, condensado en un párrafo.
- [x] **14 · El permisivo como calidad del grafo base.** Así se presenta.
- [x] **15 · Más protagonismo a la cifra permisiva.** Está en el resumen ("hasta 19 de sus 43
  puntos son convenciones de anotación") y en resultados, como cota superior por el límite
  de la regla de dirección.

## Tercera parte

- [x] **16 · Quitar Parsimonious.** Quitado del resumen, la introducción, la metodología, la
  Tabla I, la Figura 1 (regenerada solo con Standard) y las conclusiones.
- [ ] **17 · Números de las pruebas de la página 5.** Los de Wilcoxon y signos eran de la
  comparación con Parsimonious y salieron con ella. Los que quedan (signos, Â12, Bonferroni)
  son los del paper original; no los recalculé.
- [x] **18 · Citas de la página 6.** Verificadas contra el PDF de Arcuri y Briand: no
  recomiendan Bonferroni y recomiendan reportar el Â12 de Vargha y Delaney con su intervalo.
  Quitada la afirmación de que lo desaconsejan "por inflar el error de Tipo II", que el
  artículo no dice así.
- [x] **19 · Demasiado contenido en las páginas 7 y 8.** Recortado.
- [x] **20 · Figura 4 ilegible.** Quitada.
- [x] **21 · Demasiadas tablas.** De 15 a 7. La de tres modelos reúne etapa 1, brazo A y brazo B
  con los dos prompts.
- [x] **22 · Revisión de validez como "trabajo en curso".** Quitada, igual que la sección de
  acuerdo entre modelos.
- [x] **23 · "Localizar en qué parte se originan las fallas".** Reescrito; la cita de Liu et
  al. queda como ejemplo de evaluar una etapa suponiendo perfecta la anterior. Ese PDF no está
  en `papers referencia/`, así que no la contrasté con el texto.
- [x] **24 · "Cuya consistencia interna se desconoce".** Quitado. Queda: "todas las cifras se
  comparan contra una única anotación de referencia".

Otras citas verificadas contra los PDF: García et al. ("incluso la mejor tiene una precisión
sorprendentemente baja"), Fatemi et al. y Wang et al. (el razonamiento sobre grafos empeora con
la complejidad), Mizrahi et al. (evaluación con varias instrucciones). Quitada la cita de Luo et
al. (Alibaba), que no sostenía nada concreto. Del paper de Cloudscape se citan tres cosas que
dice textualmente: probaron modelos multimodales con baja precisión; cuando la descripción
verbal no coincide con el dibujo, siguen la verbal; y los flujos registran peticiones y
respuestas.

## Cuarta parte

- [x] **25 · Reordenar introducción, motivación y metodología.** Introducción con la pregunta,
  los aportes y los retos; metodología con sistema, conjunto, protocolo y ruido.
- [x] **26 · Trabajo relacionado.** Al final, en dos párrafos, solo con citas verificadas.

## Quinta parte

- [x] **27 · Costo en tokens.** Nueva Tabla VI: tokens y USD por video para Flash, Pro, Claude y
  Argon, y costo de las 396 arquitecturas (13 USD con Flash, 58 con Pro), con las tarifas
  oficiales de octubre de 2026. Falta el costo de la etapa 1 de Claude, que no se registró.

## Hallazgos nuevos de esta revisión

- **Exactitud de tipo de arista: 61,5 %.** El paper la definía y nunca la reportaba. Queda por
  debajo de etiquetar todo como `data` (81 % de la referencia) porque el prompt usa un tipo
  `control` que Cloudscape no tiene (30 % de las aristas generadas).
- **Corregido un error del original:** decía que ninguna intervención alcanzaba "la mitad del
  umbral", pero el *few-shot* RAG llega a 0,76 veces el MDE. Ahora dice "ninguna alcanza el
  umbral".
