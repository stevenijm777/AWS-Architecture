# Graph Renderer — Headless PNG Generator

Genera imágenes PNG de alta calidad a partir de archivos `.graphml` usando Node.js Canvas y los iconos oficiales de AWS.

## Setup

```bash
cd graph_renderer
npm install
```

## Uso

### 1. Copiar todos los grafos del proyecto

```bash
node copy_all_graphs.mjs
```

Esto copia todos los `.graphml` de `cloudscape_gt/` (como `_cloud`), `graphs_parsimonious/` (como `_vision`), y `graphs/` (como `_gem`) al directorio `graphs_input/`.

### 2. Renderizar todas las imágenes

```bash
node render_graph.mjs
```

Las imágenes se generan en `graphs_output/` en formato PNG a resolución 2x.

### 3. Renderizar un archivo específico

```bash
node render_graph.mjs graphs_input/07lfvavMdfU_cloud.graphml
```

## Estructura

```
graph_renderer/
├── icons/              # 173 iconos PNG de servicios AWS (copiados de Cloudscape)
├── graphs_input/       # Archivos .graphml de entrada
├── graphs_output/      # Imágenes PNG generadas
├── services.csv        # Catálogo de servicios AWS (mapeo nombre → icono)
├── render_graph.mjs    # Script principal de renderizado
├── copy_all_graphs.mjs # Script para copiar grafos del proyecto
└── package.json        # Dependencias de Node.js
```

## Características

- **Iconos AWS oficiales**: Usa los mismos iconos que el explorador Streamlit de Cloudscape
- **Layout jerárquico**: Algoritmo topológico inspirado en Klay para posicionamiento de nodos
- **Colores por workflow**: Cada `flow_id` tiene un color distinto (negro, rojo, verde, azul, etc.)
- **Flechas y líneas punteadas**: Flechas sólidas para datos, punteadas para control/meta
- **Labels con secuencia**: Muestra el número de secuencia (`seq`) en cada arista
- **Resolución 2x**: Alta resolución para impresión y visualización detallada
- **Tags de fuente**: Añade `[Cloud GT]`, `[Parsimonious]`, o `[Standard Gemini]` al título
