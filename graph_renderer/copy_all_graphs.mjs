#!/usr/bin/env node
/**
 * render_all_project_graphs.mjs — Bulk render all available graphs from the project
 * 
 * Copies all .graphml files from:
 *   - data/cloudscape_gt/  → {id}_cloud.graphml
 *   - data/graphs_parsimonious/ → {id}_vision.graphml
 *   - data/graphs/ → {id}_gem.graphml
 * 
 * Then renders them all to graphs_output/
 * 
 * Usage:
 *   node render_all_project_graphs.mjs
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, '..');
const INPUT_DIR = path.join(__dirname, 'graphs_input');
const RENDER_SCRIPT = path.join(__dirname, 'render_graph.mjs');

const SOURCES = [
  { dir: path.join(PROJECT_ROOT, 'data/cloudscape_gt'), suffix: '_cloud' },
  { dir: path.join(PROJECT_ROOT, 'data/graphs_parsimonious'), suffix: '_vision' },
  { dir: path.join(PROJECT_ROOT, 'data/graphs'), suffix: '_gem' },
];

// Clear input dir
fs.mkdirSync(INPUT_DIR, { recursive: true });
for (const f of fs.readdirSync(INPUT_DIR)) {
  if (f.endsWith('.graphml')) fs.unlinkSync(path.join(INPUT_DIR, f));
}

let totalCopied = 0;
for (const { dir, suffix } of SOURCES) {
  if (!fs.existsSync(dir)) {
    console.log(`⚠ Directory ${dir} does not exist, skipping.`);
    continue;
  }
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.graphml') && !f.includes('_visual'));
  for (const f of files) {
    const id = f.replace('.graphml', '');
    const dest = path.join(INPUT_DIR, `${id}${suffix}.graphml`);
    fs.copyFileSync(path.join(dir, f), dest);
    totalCopied++;
  }
  console.log(`✓ Copied ${files.length} files from ${path.basename(dir)} as *${suffix}.graphml`);
}

console.log(`\n✓ Total: ${totalCopied} graphml files copied to graphs_input/`);
console.log(`\nNow run: node render_graph.mjs\n`);
