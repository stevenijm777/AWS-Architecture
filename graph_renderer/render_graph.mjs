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
import { createCanvas, loadImage } from 'canvas';
import { XMLParser } from 'fast-xml-parser';
import { parse as csvParse } from 'csv-parse/sync';

// ─── Configuration ───────────────────────────────────────────────────────────
const __dirname = path.dirname(new URL(import.meta.url).pathname);
const ICONS_DIR = path.join(__dirname, 'icons');
const INPUT_DIR = path.join(__dirname, 'graphs_input');
const OUTPUT_DIR = path.join(__dirname, 'graphs_output');
const SERVICES_CSV = path.join(__dirname, 'services.csv');

const NODE_SIZE = 64;
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
  // Build adjacency for topological sort
  const adj = {};
  const inDeg = {};
  for (const n of nodes) {
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
  for (const n of nodes) {
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

  // Assign remaining unvisited nodes (cycles) to layer 0
  for (const n of nodes) {
    if (layer[n.id] === undefined) {
      layer[n.id] = 0;
    }
  }

  // Group nodes by layer
  const layers = {};
  for (const n of nodes) {
    const l = layer[n.id];
    if (!layers[l]) layers[l] = [];
    layers[l].push(n.id);
  }

  // Compute positions
  const hSpacing = NODE_SIZE * 2.8;
  const vSpacing = NODE_SIZE * 2.2;
  const positions = {};

  const sortedLayerKeys = Object.keys(layers).map(Number).sort((a, b) => a - b);
  
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

// ─── Main render function ────────────────────────────────────────────────────
async function renderGraph(graphmlPath, outputPath, serviceCatalog) {
  const { graphAttrs, nodes, edges } = parseGraphML(graphmlPath);
  
  if (nodes.length === 0) {
    console.log(`  ⚠ Skipping ${path.basename(graphmlPath)}: no nodes`);
    return;
  }

  const positions = computeLayout(nodes, edges);

  // Compute bounding box
  const allX = Object.values(positions).map(p => p.x);
  const allY = Object.values(positions).map(p => p.y);
  const minX = Math.min(...allX) - PADDING;
  const maxX = Math.max(...allX) + PADDING;
  const minY = Math.min(...allY) - PADDING;
  const maxY = Math.max(...allY) + PADDING;

  const width = Math.max(maxX - minX + NODE_SIZE * 2, 400);
  const height = Math.max(maxY - minY + NODE_SIZE * 2, 300);

  // Create canvas
  const canvas = createCanvas(width * DPI_SCALE, height * DPI_SCALE);
  const ctx = canvas.getContext('2d');
  ctx.scale(DPI_SCALE, DPI_SCALE);

  // White background
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, width, height);

  // Offset to center
  const offsetX = -minX + NODE_SIZE;
  const offsetY = -minY + NODE_SIZE;

  // ── Draw title ──
  let rawTitle = graphAttrs.name || path.basename(graphmlPath, '.graphml');
  // Truncate to fit canvas width
  const maxTitleChars = Math.floor(width / 10);
  if (rawTitle.length > maxTitleChars) {
    rawTitle = rawTitle.substring(0, maxTitleChars - 3) + '...';
  }
  // Add source suffix from filename (_cloud, _vision, _gem)
  const baseName = path.basename(graphmlPath, '.graphml');
  let sourceTag = '';
  if (baseName.endsWith('_cloud')) sourceTag = ' [Cloud GT]';
  else if (baseName.endsWith('_vision')) sourceTag = ' [Parsimonious]';
  else if (baseName.endsWith('_gem')) sourceTag = ' [Standard Gemini]';
  const title = rawTitle + sourceTag;
  ctx.fillStyle = '#1a1a1a';
  ctx.font = 'bold 15px "Segoe UI", Arial, sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText(title, width / 2, 22);

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

    // Clip to node boundary
    const from = clipToCircle(sx, sy, tx, ty, NODE_SIZE / 2 + 2);
    const to = clipToCircle(tx, ty, sx, sy, NODE_SIZE / 2 + 6);

    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    if (edgeType !== 'data') {
      ctx.setLineDash([6, 4]);
    }
    ctx.beginPath();
    ctx.moveTo(from.x, from.y);
    ctx.lineTo(to.x, to.y);
    ctx.stroke();
    ctx.restore();

    // Arrow head
    drawArrowHead(ctx, from.x, from.y, to.x, to.y, color, 10);

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

    // Draw icon
    if (fs.existsSync(iconPath)) {
      try {
        const img = await loadImage(iconPath);
        const imgSize = NODE_SIZE - 4;
        ctx.drawImage(img, x - imgSize / 2, y - imgSize / 2, imgSize, imgSize);
      } catch {
        // Fallback: colored circle
        ctx.fillStyle = '#e0e0e0';
        ctx.beginPath();
        ctx.arc(x, y, NODE_SIZE / 2 - 2, 0, Math.PI * 2);
        ctx.fill();
      }
    } else {
      // Fallback: colored circle with text
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
    let label = service;
    if (service === 'ThirdParty' && node.name) {
      // Abbreviate ThirdParty names to keep labels readable
      const name = node.name;
      label = name.length > 20 ? name.substring(0, 18) + '...' : name;
    }
    // Truncate long labels
    if (label.length > 24) label = label.substring(0, 22) + '..';
    const labelText = `${label} (${node.id})`;

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
