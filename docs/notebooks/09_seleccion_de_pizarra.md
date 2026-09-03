*Fecha: 2026-09-02*
*Hash (SHA-256): eec14faa7fd79083076e7937c6960c1e60081590beeb14af3bdaf99a9cde7946*

## Propósito
Documenta la etapa visual previa al agente: la selección de fotogramas candidatos, los filtros que los descartan y el registro (manifiesto) de la imagen exacta que se usó en cada extracción para asegurar reproducibilidad.
**Artefacto producido:** Ninguno impreso (`resultados/` en disco implícito, pero no escribe archivo desde la celda de salida).

## Entradas
- Manifiesto e historial de corridas en `run.json`.

## Compuertas
- El script comprueba que el SHA-256 registrado coincida de manera exacta:
  `OK · el manifiesto identifica exactamente las imagenes con las que se llamo a la API.`
  (`comprobaciones manifiesto vs run.json : 600 | coinciden : 600 | distintos : 0`).

## Método
- **Filtro Piel:** Requiere $>1.4\%$ de densidad de piel detectada.
- **Filtro Anomalía Estadística:** Compara densidad contra el umbral del fotograma.
- **Validación de Íconos AWS:** Descarta por contraste excesivo que corrompa la lectura.
- **Puntuación Oclusión:** Combinación lineal de íconos encontrados, tiza detectada, oclusión penalizada y bono por presencia humana (piel).

## Resultados

**El pipeline de la etapa visual:**
```text
pizarras registradas en el manifiesto: 446
Counter({'frame_extraido': 380, 'reemplazo_manual': 66})

imagen de ejemplo: -3lnf5lzsH0.jpg  (1920x1012)
```

**Los filtros y Puntuación:**
```text
piel = 9.38%  ->  tiene_piel = True  (umbral 1.4%)
densidad 0.0276 vs umbral 0.0495  ->  pasa el filtro
iconos validos: 8   descartados por contraste: 1
  deltas rechazados: ['7.2'] (umbral 40.0)

  iconos (5 x n)                +40.000
  tiza (50 x densidad tope)      +0.750
  oclusion (-700 x pct)         -13.901
  bono piel (50 x tope)          +4.689
  TOTAL                         +31.538
```

**El manifiesto:**
```text
      video_id                                             sha256   bytes  \
0  -3lnf5lzsH0  4a068bb5c768ae47b547cbd5fcfc3db184437a77f53d99...  309961   
1  -S-R7MWRpaI  6e65fc1a7096c3c25417abd562548abc6b059a3136b54b...  387453   
2  -ahWdCysMYw  2b4c310a27310d2fedfc67c3a09ef7e636e8e8697cefc4...  348080   

           origen                frame_archivo frame_numero frames_extraidos  
0  frame_extraido  -3lnf5lzsH0_frame_13230.jpg        13230              174  
1  frame_extraido  -S-R7MWRpaI_frame_04795.jpg        04795               76  
2  frame_extraido  -ahWdCysMYw_frame_04769.jpg        04769               51  

origen de las 446 imagenes del estudio:
  frame_extraido      380  (85.2 %)
  reemplazo_manual     66  (14.8 %)
```

**Copyright y validación del manifiesto:**
```text
comprobaciones manifiesto vs run.json : 600
  coinciden : 600
  distintos : 0

OK · el manifiesto identifica exactamente las imagenes con las que se llamo a la API.
```

## Limitaciones
- "El código del selector cambió después de generar las imágenes con las que se corrieron los experimentos. Las imágenes están fijadas por hash en el manifiesto, así que los resultados son reproducibles; lo que no es reproducible es regenerar esas mismas imágenes desde el video con el código de hoy."
