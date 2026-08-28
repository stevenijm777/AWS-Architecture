# 🔭 Evidencia — Experimento del Oráculo (E04)

Registro de la condición oráculo: alimentar Stage 2 con un World Model provisto
en vez del que genera Stage 1, para separar cuánto de la pérdida del pipeline es
de la visión y cuánto de la traducción posterior.

Ver el plan declarativo en
[`ara/logic/experiments.md` § E04](../../logic/experiments.md).

---

## Por qué existe

El Edge F1 del pipeline Standard está clavado en ~59 % y cuatro intervenciones
sobre el prompt de Stage 2 dieron resultado nulo (11 variantes, few-shot RAG,
inyección de topología por visión por computadora, correcciones dirigidas). El
piso de ruido medido — sigma_d de 8.76 puntos por video, efecto mínimo detectable
de 4.48 a n=30 — muestra que el rango entero de la tabla de ablación (3.00
puntos) cabe adentro del ruido. El prompt quedó descartado como palanca.

Queda preguntar por la **entrada**, no por el prompt.

## Los tres brazos

| Brazo | World Model que recibe Stage 2 | Qué mide |
|---|---|---|
| **Producción** | `world_model.json` — generado por Stage 1 | el pipeline tal cual |
| **A — visual** | `world_model_vision.json` — transcripción humana de la pizarra | techo de la pizarra sola |
| **B — oráculo GT** | `world_model_oracle_gt.json` — GT convertido, determinista | techo de traducción de Stage 2 |

La descomposición es el punto: **producción → A** es lo que compra mejorar
Stage 1; **A → B** es cuánto de la ground truth simplemente no está dibujado en
la pizarra, o sea la justificación cuantitativa del canal de audio.

**B va primero.** Es el control de instrumento: sin saber si Stage 2 puede
transportar una entrada perfecta, un resultado bajo en A es ininterpretable — no
se distingue si la pérdida vino de la pizarra o de Stage 2.

## Techos de pass-through (0 llamadas a la API)

Un World Model no puede producir un grafo mejor que él mismo. Si Stage 2 lo
copiara literalmente, esto es lo que daría, con la misma métrica de
`evaluate_graphs.py` (servicios en multiset; aristas en multiset sobre
`(src_service, tgt_service)`, ignorando el tipo):

| Brazo | n | Svc F1 | Edge F1 |
|---|---|---|---|
| **B — oráculo GT** | 30 | **100.00** | **100.00** |
| **A — visual** | 12 | 83.78 | **50.77** |

Reproducir:

```bash
.venv/bin/python scripts/ablation/build_oracle_world_models.py --verify
```

```bash
.venv/bin/python scripts/ablation/build_oracle_world_models.py --ceiling vision
```

### Consecuencia para el brazo A, antes de gastar una llamada

Producción sobre esos mismos 12 videos da **Edge F1 64.97**. El techo del brazo A
es **50.77**. Las 12 transcripciones, tal como están hoy, **no pueden ganarle a
producción ni con un Stage 2 perfecto**. Correr A en este estado produciría un
número negativo que se leería como "Stage 1 no es el cuello de botella" cuando en
realidad mide la calibración de la transcripción.

La firma del problema es precisión 70.0 contra recall 41.9: están
**subconectadas**. Y buena parte de la causa no es que la pizarra no tenga la
información, sino desalineación de vocabulario con el catálogo:

- `RDS` donde el GT usa `ThirdParty` — MySQL no es AWS (`-kA0ahrhX3I`, `BZ32w0SSAoY`).
- `-3lnf5lzsH0`: Apache Metron transcrito como `EC2`; el GT lo trata como `ThirdParty`.
  Ese nodo es el hub que recibe de 7 servicios: un solo error de vocabulario tira ~7 aristas.
- Actores adivinados: `UserConsumerWeb` contra `UserCompanyDeveloper` en `1aYoIZvabbk`
  (precisión 16.7 — matcheó 1 de 6 aristas).
- `6YkguepAQuQ` declara `CLOUDFRONT → VPC` pero la entidad que existe es CloudFormation:
  arista colgada por un typo, no por visión. `--ceiling` la reporta sola.

Usar el catálogo de `data/services.csv` al transcribir **no es trampa**: es el
mismo vocabulario que Stage 1 recibe en su prompt. Mirar el grafo GT sí lo sería.

## Convención de agrupación, resuelta contra el GT

La duda operativa al transcribir era qué hacer con los servicios repetidos —
`-kA0ahrhX3I` dibuja 3 cuentas AWS, cada una con su Macie y su S3.

El GT de ese video tiene **9 nodos: Macie ×2, S3 ×2**, distinguidos por `notes`
(`DATA_PEEK: Production data` contra `DATA_PEEK: Metadata of risky data`).

Tres lecturas, todas verificadas:

1. **El GT no deduplica.** Colapsar a un solo Macie cuesta recall, porque los
   servicios se cuentan en multiset.
2. **Pero tampoco replica lo dibujado**: 3 en la pizarra, 2 en el GT. Colapsa las
   dos cuentas miembro idénticas en una representante y deja la central aparte.
   **El criterio es rol, no instancia dibujada.**
3. **`flow_id`, `seq`, `type`, `notes` y `name` no puntúan** en el Edge F1 titular.
   No vale la pena transcribir secuencias.

Los servicios extra que el audio manda ignorar **se dejan** en el brazo A: se ven
en la pizarra. La penalización de precisión que generan *es* la medición de lo
que aporta el audio.

## Confounds registrados

- **Stage 2 no recibe sólo el World Model.** `run_video()` le pasa también la
  imagen de la pizarra y el transcript completo. El brazo B no es un intercambio
  limpio de entrada: mide *Stage 2 en configuración de producción, con la mejor
  entrada posible*. Es deliberado — sacarle la imagen cambiaría dos cosas a la vez
  y rompería la comparabilidad contra el 64.97. Si B no da cerca de 100, una
  explicación viable es que Stage 2 le cree más a la imagen que al World Model, y
  ahí corresponde una variante sin imagen como seguimiento.
- **Dos reglas del prompt de Stage 2 empujan en contra del oráculo.** La regla 4
  ("Dynamic Logical Fusion") le pide fusionar iconos repetidos del mismo servicio
  — exactamente el caso Macie ×2 / S3 ×2. La regla 3 ("Audio-Driven Expansion") le
  pide expandir nodos genéricos usando el audio, lo que sobre una entrada perfecta
  sólo puede agregar alucinaciones. Son los dos mecanismos candidatos si B queda
  por debajo de 100.
- **Campos sintéticos en el brazo B**: el GT no tiene geometría, así que
  `arrow_direction` va vacío y `rationale`/`description` sólo copian las notas del
  GT. El prompt de Stage 2 no menciona ninguno de los tres, pero es un cambio de
  distribución respecto de lo que produce Stage 1.
- **La referencia correcta** es producción sobre los mismos video_ids del brazo,
  nunca la tabla histórica ni el promedio del panel completo. Un cálculo previo
  sobre los 12 dio Svc 88.98 / Edge 64.97, contra 89.79 / 63.21 del panel de 14:
  usar el número del panel sobreestimaría el beneficio en ~1.8 puntos. El runner
  suprime la comparación automática en modo oráculo justamente por esto.

---

## Contenido de este directorio

| Archivo | Qué es |
|---|---|
| `manual_transcriptions_2026-07-31/` | Respaldo íntegro de las 12 transcripciones del brazo A, tal como estaban el 2026-08-27. `lab_workspace/` está en `.gitignore`, así que sin esta copia no tienen historial. |
| `manual_transcriptions_2026-07-31.sha256` | Checksums de ese respaldo. |
| `brazo_b_world_models_p30.json` | Manifiesto de los 30 World Model del brazo B: sha256 por archivo, política de etiquetas, techo verificado. |

> Las 12 transcripciones del brazo A llevan `rationale` en inglés y con prosa de
> modelo. Si alguna se sembró con salida de un LLM o mirando el GT, no son
> condición A (ciega) sino "humano con contexto", que mide otra cosa. Queda
> pendiente confirmarlo con quien las escribió; el resultado del brazo A no es
> publicable como techo visual hasta que eso esté resuelto.

## Reproducir

```bash
.venv/bin/python scripts/ablation/build_oracle_world_models.py --write
```

```bash
.venv/bin/python scripts/ablation/rerun_panel.py --prompt stage2_v6_corrected__cell9.txt --panel 30 --oracle oracle_gt
```
