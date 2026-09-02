/**
 * render_graph.mjs — Headless Cytoscape.js renderer for AWS architecture graphs
 * 
 * Reads .graphml files, builds Cytoscape elements with AWS service icons,
 * renders with klay layout, and exports to high-quality PNG.
 * 
 * Usage:
 *   node render_graph.mjs                        # Render all in graphs_input/
 *   node render_graph.mjs graphs_input/file.graphml  # Render single file
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { createCanvas, loadImage } from 'canvas';
import { XMLParser } from 'fast-xml-parser';
import { parse as csvParse } from 'csv-parse/sync';

// ─── Configuration ───────────────────────────────────────────────────────────
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ICONS_DIR = path.join(__dirname, 'icons');
const INPUT_DIR = path.join(__dirname, 'graphs_input');
const OUTPUT_DIR = path.join(__dirname, 'graphs_output');
const SERVICES_CSV = path.join(__dirname, 'services.csv');

const NODE_SIZE = 64;
const NODE_BG_RADIUS = NODE_SIZE / 2 + 6; // white knockout circle behind icon
const LABEL_FONT = '13px "Segoe UI", Arial, sans-serif';
const LABEL_FONT_BOLD = 'bold 13px "Segoe UI", Arial, sans-serif';
const EDGE_LABEL_FONT = '11px "Segoe UI", Arial, sans-serif';
const PADDING = 80;
const DPI_SCALE = 2; // 2x resolution for crisp output

const FLOW_COLORS = [
  '#1a1a1a', '#e53935', '#43a047', '#1e88e5', '#8e24aa',
  '#f4511e', '#00897b', '#d81b60', '#fdd835', '#00acc1',
  '#757575', '#795548', '#546e7a', '#9e9d24', '#6d4c41',
];

// ─── Load service catalog ────────────────────────────────────────────────────
function loadServiceCatalog() {
  const csvContent = fs.readFileSync(SERVICES_CSV, 'utf-8');
  const records = csvParse(csvContent, { columns: true, skip_empty_lines: true });
  const catalog = {};
  for (const row of records) {
    catalog[row.name] = {
      image_url: row.image_url,
      capability: row.capability,
      is_aws: row.is_aws === 'True',
    };
  }
  return catalog;
}

// ─── Parse GraphML ───────────────────────────────────────────────────────────
function parseGraphML(filePath) {
  const xml = fs.readFileSync(filePath, 'utf-8');
  const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: '@_',
    isArray: (name) => ['node', 'edge', 'data', 'key'].includes(name),
  });
  const doc = parser.parse(xml);
  const graphml = doc.graphml;

  // Build key mapping (id → attr.name)
  const keys = {};
  if (graphml.key) {
    for (const k of graphml.key) {
      keys[k['@_id']] = k['@_attr.name'];
    }
  }

  const graph = graphml.graph;
  const nodes = [];
  const edges = [];
  const graphAttrs = {};

  // Parse graph-level data
  if (graph.data) {
    for (const d of Array.isArray(graph.data) ? graph.data : [graph.data]) {
      const attrName = keys[d['@_key']];
      if (attrName) graphAttrs[attrName] = d['#text'] ?? '';
    }
  }

  // Parse nodes
  if (graph.node) {
    for (const n of graph.node) {
      const nodeData = { id: String(n['@_id']) };
      if (n.data) {
        for (const d of Array.isArray(n.data) ? n.data : [n.data]) {
          const attrName = keys[d['@_key']];
          if (attrName) nodeData[attrName] = d['#text'] ?? '';
        }
      }
      nodes.push(nodeData);
    }
  }

  // Parse edges
  if (graph.edge) {
    for (const e of graph.edge) {
      const edgeData = {
        source: String(e['@_source']),
        target: String(e['@_target']),
      };
      if (e.data) {
        for (const d of Array.isArray(e.data) ? e.data : [e.data]) {
          const attrName = keys[d['@_key']];
          if (attrName) {
            const val = d['#text'] ?? '';
            edgeData[attrName] = attrName === 'flow_id' ? parseInt(val) || 0 : val;
          }
        }
      }
      edges.push(edgeData);
    }
  }

  return { graphAttrs, nodes, edges };
}

// ─── Klay-inspired hierarchical layout ───────────────────────────────────────
function computeLayout(nodes, edges) {
  // Identify which nodes have at least one edge (source or target)
  const connectedIds = new Set();
  for (const e of edges) {
    connectedIds.add(e.source);
    connectedIds.add(e.target);
  }

  // Separate orphan nodes (no edges at all) from connected nodes
  const connectedNodes = nodes.filter(n => connectedIds.has(n.id));
  const orphanNodes = nodes.filter(n => !connectedIds.has(n.id));

  // Build adjacency for topological sort (only connected nodes)
  const adj = {};
  const inDeg = {};
  for (const n of connectedNodes) {
    adj[n.id] = [];
    inDeg[n.id] = 0;
  }
  for (const e of edges) {
    if (adj[e.source] && inDeg[e.target] !== undefined) {
      adj[e.source].push(e.target);
      inDeg[e.target]++;
    }
  }

  // Topological layering via BFS (Kahn's algorithm)
  const queue = [];
  const layer = {};
  for (const n of connectedNodes) {
    if (inDeg[n.id] === 0) {
      queue.push(n.id);
      layer[n.id] = 0;
    }
  }

  let maxLayer = 0;
  while (queue.length > 0) {
    const curr = queue.shift();
    for (const next of adj[curr]) {
      const newLayer = layer[curr] + 1;
      if (layer[next] === undefined || newLayer > layer[next]) {
        layer[next] = newLayer;
      }
      inDeg[next]--;
      if (inDeg[next] === 0) {
        queue.push(next);
        maxLayer = Math.max(maxLayer, layer[next]);
      }
    }
  }

  // Assign remaining unvisited connected nodes (cycles) to layer 0
  for (const n of connectedNodes) {
    if (layer[n.id] === undefined) {
      layer[n.id] = 0;
    }
  }

  // Group connected nodes by layer
  const layers = {};
  for (const n of connectedNodes) {
    const l = layer[n.id];
    if (!layers[l]) layers[l] = [];
    layers[l].push(n.id);
  }

  // Compute positions
  const hSpacing = NODE_SIZE * 3.8;
  const vSpacing = NODE_SIZE * 3.2;
  const positions = {};

  const sortedLayerKeys = Object.keys(layers).map(Number).sort((a, b) => a - b);

  if (process.env.RG_COMPACT === '1') {
    const perCol = Math.max(3, Math.ceil(Math.sqrt(connectedNodes.length)));
    let xCursor = 0;
    for (const l of sortedLayerKeys) {
      const inLayer = layers[l];
      const nCols = Math.ceil(inLayer.length / perCol);
      const colH = Math.ceil(inLayer.length / nCols);
      for (let i = 0; i < inLayer.length; i++) {
        const col = Math.floor(i / colH), row = i % colH;
        const thisColCount = Math.min(colH, inLayer.length - col * colH);
        positions[inLayer[i]] = {
          x: xCursor + col * hSpacing,
          y: -(thisColCount - 1) * hSpacing / 2 + row * hSpacing,
        };
      }
      xCursor += nCols * hSpacing + vSpacing;
    }
  } else {
    for (const l of sortedLayerKeys) {
      const nodesInLayer = layers[l];
      const layerWidth = nodesInLayer.length * hSpacing;
      const startY = -(layerWidth / 2) + hSpacing / 2;

      for (let i = 0; i < nodesInLayer.length; i++) {
        positions[nodesInLayer[i]] = {
          x: l * vSpacing,
          y: startY + i * hSpacing,
        };
      }
    }
  }

  // Place orphan nodes in a separate row below the main graph
  if (orphanNodes.length > 0) {
    const allYValues = Object.values(positions).map(p => p.y);
    const maxY = allYValues.length > 0 ? Math.max(...allYValues) : 0;
    const orphanY = maxY + hSpacing * 1.5; // well below the connected graph
    const orphanWidth = orphanNodes.length * hSpacing;
    const orphanStartX = -(orphanWidth / 2) + hSpacing / 2;

    for (let i = 0; i < orphanNodes.length; i++) {
      positions[orphanNodes[i].id] = {
        x: orphanStartX + i * hSpacing,
        y: orphanY,
      };
    }
  }

  return positions;
}

// ─── Draw arrow head ─────────────────────────────────────────────────────────
function drawArrowHead(ctx, fromX, fromY, toX, toY, color, size = 10) {
  const angle = Math.atan2(toY - fromY, toX - fromX);
  ctx.save();
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.moveTo(toX, toY);
  ctx.lineTo(
    toX - size * Math.cos(angle - Math.PI / 6),
    toY - size * Math.sin(angle - Math.PI / 6)
  );
  ctx.lineTo(
    toX - size * Math.cos(angle + Math.PI / 6),
    toY - size * Math.sin(angle + Math.PI / 6)
  );
  ctx.closePath();
  ctx.fill();
  ctx.restore();
}

// ─── Clip edge to node circle boundary ───────────────────────────────────────
function clipToCircle(cx, cy, tx, ty, radius) {
  const dx = tx - cx;
  const dy = ty - cy;
  const dist = Math.sqrt(dx * dx + dy * dy);
  if (dist === 0) return { x: cx, y: cy };
  return {
    x: cx + (dx / dist) * radius,
    y: cy + (dy / dist) * radius,
  };
}

// ─── Build node label for display ────────────────────────────────────────────
function getNodeLabel(node) {
  const service = node.service || 'ThirdParty';
  let label = service;
  if (service === 'ThirdParty' && node.name) {
    const name = node.name;
    label = name.length > 20 ? name.substring(0, 18) + '...' : name;
  }
  if (label.length > 24) label = label.substring(0, 22) + '..';
  return `${label} (${node.id})`;
}

// ─── Main render function ────────────────────────────────────────────────────
async function renderGraph(graphmlPath, outputPath, serviceCatalog) {
  const { graphAttrs, nodes, edges } = parseGraphML(graphmlPath);
  
  if (nodes.length === 0) {
    console.log(`  ⚠ Skipping ${path.basename(graphmlPath)}: no nodes`);
    return;
  }

  const positions = computeLayout(nodes, edges);

  // Build node lookup by id for connection table
  const nodeById = {};
  for (const n of nodes) nodeById[n.id] = n;

  // ── Pre-measure connection table to reserve space ──
  const TABLE_FONT = '12px "Segoe UI", Arial, sans-serif';
  const TABLE_FONT_BOLD = 'bold 12px "Segoe UI", Arial, sans-serif';
  const TABLE_LINE_H = 18;
  const TABLE_PADDING = 16;

  // Build connection table lines
  const tableLines = [];
  if (edges.length > 0) {
    tableLines.push({ text: 'CONNECTIONS', bold: true });
    tableLines.push({ text: '─────────────────────────', bold: false });
    for (const edge of edges) {
      const srcNode = nodeById[edge.source];
      const tgtNode = nodeById[edge.target];
      if (!srcNode || !tgtNode) continue;
      const srcLabel = getNodeLabel(srcNode);
      const tgtLabel = getNodeLabel(tgtNode);
      tableLines.push({ text: `${srcLabel}  →  ${tgtLabel}`, bold: false });
    }
  }

  // Measure max table text width using a temp canvas
  let tableWidth = 0;
  if (tableLines.length > 0) {
    const tmpCanvas = createCanvas(10, 10);
    const tmpCtx = tmpCanvas.getContext('2d');
    tmpCtx.font = TABLE_FONT;
    for (const line of tableLines) {
      if (line.bold) tmpCtx.font = TABLE_FONT_BOLD;
      else tmpCtx.font = TABLE_FONT;
      const w = tmpCtx.measureText(line.text).width;
      if (w > tableWidth) tableWidth = w;
    }
    tableWidth += TABLE_PADDING * 2 + 20; // extra margin
  }

  // Compute bounding box for graph area
  const allX = Object.values(positions).map(p => p.x);
  const allY = Object.values(positions).map(p => p.y);
  const minX = Math.min(...allX) - PADDING;
  const maxX = Math.max(...allX) + PADDING;
  const minY = Math.min(...allY) - PADDING;
  const maxY = Math.max(...allY) + PADDING;

  const graphWidth = Math.max(maxX - minX + NODE_SIZE * 2, 400);
  const graphHeight = Math.max(maxY - minY + NODE_SIZE * 2, 300);

  // Total canvas = graph + connection table on the right
  const tableColumnWidth = tableLines.length > 0 ? tableWidth + 20 : 0;
  const width = graphWidth + tableColumnWidth;
  const tableHeight = tableLines.length * TABLE_LINE_H + TABLE_PADDING * 2;
  const height = Math.max(graphHeight, tableHeight + 40);

  // Create canvas
  const canvas = createCanvas(width * DPI_SCALE, height * DPI_SCALE);
  const ctx = canvas.getContext('2d');
  ctx.scale(DPI_SCALE, DPI_SCALE);

  // White background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, width, height);

  // Offset to center graph in its area
  const offsetX = -minX + NODE_SIZE;
  const offsetY = -minY + NODE_SIZE;

  // ── Draw title ──
  let rawTitle = graphAttrs.name || path.basename(graphmlPath, '.graphml');
  const maxTitleChars = Math.floor(graphWidth / 10);
  if (rawTitle.length > maxTitleChars) {
    rawTitle = rawTitle.substring(0, maxTitleChars - 3) + '...';
  }
  const baseName = path.basename(graphmlPath, '.graphml');
  let sourceTag = '';
  if (baseName.endsWith('_cloud')) sourceTag = ' [Cloud GT]';
  else if (baseName.endsWith('_vision')) sourceTag = ' [Parsimonious]';
  else if (baseName.endsWith('_gem')) sourceTag = ' [Standard Gemini]';
  const title = rawTitle + sourceTag;
  ctx.fillStyle = '#1a1a1a';
  ctx.font = 'bold 15px "Segoe UI", Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(title, graphWidth / 2, 22);

  // Helper: check if a straight line passes too close to any intermediate node
  const nodePositions = nodes.map(n => {
    const p = positions[n.id];
    return p ? { id: n.id, x: p.x + offsetX, y: p.y + offsetY } : null;
  }).filter(Boolean);

  function findBlockingNodes(sx, sy, tx, ty, srcId, tgtId) {
    const blocking = [];
    const clearance = NODE_SIZE * 0.7;
    for (const np of nodePositions) {
      if (np.id === srcId || np.id === tgtId) continue;
      const dx = tx - sx, dy = ty - sy;
      const len2 = dx * dx + dy * dy;
      if (len2 === 0) continue;
      let t = ((np.x - sx) * dx + (np.y - sy) * dy) / len2;
      t = Math.max(0, Math.min(1, t));
      const px = sx + t * dx, py = sy + t * dy;
      const dist = Math.sqrt((np.x - px) ** 2 + (np.y - py) ** 2);
      if (dist < clearance) blocking.push(np);
    }
    return blocking;
  }

  // ── Draw edges ──
  for (const edge of edges) {
    const srcPos = positions[edge.source];
    const tgtPos = positions[edge.target];
    if (!srcPos || !tgtPos) continue;

    const sx = srcPos.x + offsetX;
    const sy = srcPos.y + offsetY;
    const tx = tgtPos.x + offsetX;
    const ty = tgtPos.y + offsetY;

    const flowId = edge.flow_id || 0;
    const color = FLOW_COLORS[flowId % FLOW_COLORS.length];
    const edgeType = edge.type || 'data';

    const from = clipToCircle(sx, sy, tx, ty, NODE_BG_RADIUS);
    const to = clipToCircle(tx, ty, sx, sy, NODE_BG_RADIUS + 4);

    const blockers = findBlockingNodes(sx, sy, tx, ty, edge.source, edge.target);

    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    if (edgeType !== 'data') {
      ctx.setLineDash([6, 4]);
    }

    if (blockers.length > 0) {
      // Curve smoothly around blocking nodes using quadratic Bezier curve
      const midX = (from.x + to.x) / 2;
      const midY = (from.y + to.y) / 2;
      const dx = to.x - from.x;
      const dy = to.y - from.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;

      // Perpendicular normal vector
      const nx = -dy / dist;
      const ny = dx / dist;

      // Offset control point perpendicular to line
      const offset = NODE_SIZE * 0.85;
      const ctrlX = midX + nx * offset;
      const ctrlY = midY + ny * offset;

      const fromClip = clipToCircle(sx, sy, ctrlX, ctrlY, NODE_BG_RADIUS);
      const toClip = clipToCircle(tx, ty, ctrlX, ctrlY, NODE_BG_RADIUS + 4);

      ctx.beginPath();
      ctx.moveTo(fromClip.x, fromClip.y);
      ctx.quadraticCurveTo(ctrlX, ctrlY, toClip.x, toClip.y);
      ctx.stroke();
      ctx.restore();

      // Arrow head at endpoint tangent from control point
      drawArrowHead(ctx, ctrlX, ctrlY, toClip.x, toClip.y, color, 10);
    } else {
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.lineTo(to.x, to.y);
      ctx.stroke();
      ctx.restore();
      drawArrowHead(ctx, from.x, from.y, to.x, to.y, color, 10);
    }

    // Edge label (seq number)
    const seq = edge.seq ?? '';
    if (seq !== '') {
      const mx = (from.x + to.x) / 2;
      const my = (from.y + to.y) / 2;
      ctx.save();
      ctx.font = EDGE_LABEL_FONT;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      const textW = ctx.measureText(seq).width + 6;
      ctx.fillStyle = 'rgba(255,255,255,0.9)';
      ctx.fillRect(mx - textW / 2, my - 8, textW, 16);
      ctx.fillStyle = color;
      ctx.fillText(seq, mx, my);
      ctx.restore();
    }
  }

  // ── Draw nodes ──
  for (const node of nodes) {
    const pos = positions[node.id];
    if (!pos) continue;

    const x = pos.x + offsetX;
    const y = pos.y + offsetY;
    const service = node.service || 'ThirdParty';
    const svcInfo = serviceCatalog[service];
    const iconFile = svcInfo ? `${svcInfo.image_url}.png` : 'user.png';
    const iconPath = path.join(ICONS_DIR, iconFile);

    // White knockout circle behind icon
    ctx.save();
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(x, y, NODE_BG_RADIUS, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Draw icon
    if (fs.existsSync(iconPath)) {
      try {
        const img = await loadImage(iconPath);
        const imgSize = NODE_SIZE - 4;
        ctx.drawImage(img, x - imgSize / 2, y - imgSize / 2, imgSize, imgSize);
      } catch {
        ctx.fillStyle = '#e0e0e0';
        ctx.beginPath();
        ctx.arc(x, y, NODE_SIZE / 2 - 2, 0, Math.PI * 2);
        ctx.fill();
      }
    } else {
      ctx.fillStyle = '#e0e0e0';
      ctx.beginPath();
      ctx.arc(x, y, NODE_SIZE / 2 - 2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#333';
      ctx.font = '10px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(service.substring(0, 6), x, y);
    }

    // Draw label below icon
    const labelText = getNodeLabel(node);
    ctx.save();
    ctx.font = LABEL_FONT_BOLD;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    const tw = ctx.measureText(labelText).width + 8;
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    ctx.fillRect(x - tw / 2, y + NODE_SIZE / 2 + 1, tw, 18);
    ctx.fillStyle = '#1a1a1a';
    ctx.fillText(labelText, x, y + NODE_SIZE / 2 + 3);
    ctx.restore();
  }

  // ── Draw connection table on the right ──
  if (tableLines.length > 0) {
    const tableX = graphWidth + 10;
    const tableY = 36;

    // Table background
    ctx.save();
    ctx.fillStyle = '#f7f8fa';
    ctx.strokeStyle = '#dde2ea';
    ctx.lineWidth = 1;
    const tblW = tableColumnWidth - 20;
    const tblH = tableLines.length * TABLE_LINE_H + TABLE_PADDING * 2;
    ctx.beginPath();
    ctx.roundRect(tableX, tableY, tblW, tblH, 6);
    ctx.fill();
    ctx.stroke();
    ctx.restore();

    // Table text
    let curY = tableY + TABLE_PADDING + 12;
    for (const line of tableLines) {
      ctx.save();
      ctx.font = line.bold ? TABLE_FONT_BOLD : TABLE_FONT;
      ctx.fillStyle = line.bold ? '#1a1a1a' : '#333';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(line.text, tableX + TABLE_PADDING, curY);
      ctx.restore();
      curY += TABLE_LINE_H;
    }
  }

  // Export to PNG
  const buffer = canvas.toBuffer('image/png');
  fs.writeFileSync(outputPath, buffer);
}

// ─── Main ────────────────────────────────────────────────────────────────────
async function main() {
  const serviceCatalog = loadServiceCatalog();
  console.log(`✓ Loaded ${Object.keys(serviceCatalog).length} services from catalog`);

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });

  const args = process.argv.slice(2);
  let files;

  if (args.length > 0) {
    files = args.filter(f => f.endsWith('.graphml'));
  } else {
    files = fs.readdirSync(INPUT_DIR)
      .filter(f => f.endsWith('.graphml'))
      .map(f => path.join(INPUT_DIR, f));
  }

  console.log(`\nRendering ${files.length} graphs...\n`);

  let count = 0;
  for (const file of files) {
    const fullPath = path.isAbsolute(file) ? file : path.join(INPUT_DIR, file);
    const basename = path.basename(file, '.graphml');
    const outputPath = path.join(OUTPUT_DIR, `${basename}.png`);

    process.stdout.write(`  [${++count}/${files.length}] ${basename}...`);
    try {
      await renderGraph(fullPath, outputPath, serviceCatalog);
      console.log(' ✓');
    } catch (err) {
      console.log(` ✗ ${err.message}`);
    }
  }

  console.log(`\n✓ Done! ${count} images saved to ${OUTPUT_DIR}/`);
}

main().catch(console.error);
