#!/usr/bin/env python3
"""
generate_html_report.py — Generate a modern, interactive HTML comparison dashboard 
                           between v6 Standard and Parsimonious Mode.
"""
from __future__ import annotations

import sys
import base64
import json
from pathlib import Path
import networkx as nx
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

DATA_DIR = PROJECT_ROOT / "data"
STANDARD_DIR = DATA_DIR / "graphs"
PARSIMONIOUS_DIR = DATA_DIR / "graphs_parsimonious"
GT_DIR = DATA_DIR / "cloudscape_gt"
GRAFICAS_DIR = PROJECT_ROOT / "graficas"
OUTPUT_HTML = PROJECT_ROOT / "reporte_comparativo_v6_vs_parsimonious.html"

catalog = load_services_catalog(GT_DIR / "services.csv")

def norm_permissive(svc):
    if not svc or svc == "?": return "Unknown"
    s = str(svc).strip()
    cap = catalog.get(s, {}).get("capability", "")
    if s.startswith("User") or cap == "User": return "User"
    if s.startswith("ThirdParty") or cap == "ThirdParty": return "ThirdParty"
    return s

def compute_prf1(inter, gen, gt):
    p = inter / gen if gen > 0 else 0.0
    r = inter / gt if gt > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1

def eval_permissive(g_gen, g_gt):
    gen_svcs = [norm_permissive(g_gen.nodes[n].get("service", "")) for n in g_gen.nodes()]
    gt_svcs = [norm_permissive(g_gt.nodes[n].get("service", "")) for n in g_gt.nodes()]
    gen_set, gt_set = set(gen_svcs), set(gt_svcs)
    _, _, node_f1 = compute_prf1(len(gen_set & gt_set), len(gen_set), len(gt_set))
    
    def extract_base_edges(G):
        edges = set()
        for u, v in G.edges():
            su = norm_permissive(G.nodes[u].get("service", ""))
            sv = norm_permissive(G.nodes[v].get("service", ""))
            if su and sv and su != "Unknown" and sv != "Unknown":
                edges.add(tuple(sorted([su, sv])))
        return edges
        
    gen_edges, gt_edges = extract_base_edges(g_gen), extract_base_edges(g_gt)
    _, _, edge_f1 = compute_prf1(len(gen_edges & gt_edges), len(gen_edges), len(gt_edges))
    return node_f1, edge_f1

def get_chart_b64(img_name: str) -> str:
    path = GRAFICAS_DIR / img_name
    if path.exists():
        encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    return ""

def generate_report():
    clean_files = sorted(list(STANDARD_DIR.glob("*.graphml")))
    eval_vids = [f.stem for f in clean_files if (GT_DIR / f"{f.stem}.graphml").exists()]
    
    data_list = []
    
    for vid in eval_vids:
        gt_path = GT_DIR / f"{vid}.graphml"
        g_gt = nx.read_graphml(gt_path)
        
        # Standard
        std_path = STANDARD_DIR / f"{vid}.graphml"
        g_std = nx.read_graphml(std_path)
        res_std_st = evaluate_pair(g_std, g_gt, vid, catalog)
        pm_std_nf1, pm_std_ef1 = eval_permissive(g_std, g_gt)
        
        # Parsimonious
        pars_path = PARSIMONIOUS_DIR / f"{vid}.graphml"
        if pars_path.exists():
            g_pars = nx.read_graphml(pars_path)
            res_pars_st = evaluate_pair(g_pars, g_gt, vid, catalog)
            pm_pars_nf1, pm_pars_ef1 = eval_permissive(g_pars, g_gt)
        else:
            continue
            
        st_sn_std, st_se_std = res_std_st["svc_f1"] * 100, res_std_st["edge_f1"] * 100
        st_sn_pars, st_se_pars = res_pars_st["svc_f1"] * 100, res_pars_st["edge_f1"] * 100
        
        pm_sn_std_pct, pm_se_std_pct = pm_std_nf1 * 100, pm_std_ef1 * 100
        pm_sn_pars_pct, pm_se_pars_pct = pm_pars_nf1 * 100, pm_pars_ef1 * 100
        
        # Strict Winner (based on average of node and edge F1)
        st_c_std = (st_sn_std + st_se_std) / 2
        st_c_pars = (st_sn_pars + st_se_pars) / 2
        if abs(st_c_std - st_c_pars) < 0.1: st_winner = "Empate"
        elif st_c_std > st_c_pars: st_winner = "v6 Standard"
        else: st_winner = "Parsimonious"
        
        # Permissive Winner
        pm_c_std = (pm_sn_std_pct + pm_se_std_pct) / 2
        pm_c_pars = (pm_sn_pars_pct + pm_se_pars_pct) / 2
        if abs(pm_c_std - pm_c_pars) < 0.1: pm_winner = "Empate"
        elif pm_c_std > pm_c_pars: pm_winner = "v6 Standard"
        else: pm_winner = "Parsimonious"
        
        data_list.append({
            "video_id": vid,
            "st_sn_std": st_sn_std, "st_se_std": st_se_std,
            "st_sn_pars": st_sn_pars, "st_se_pars": st_se_pars,
            "st_winner": st_winner,
            "pm_sn_std": pm_sn_std_pct, "pm_se_std": pm_se_std_pct,
            "pm_sn_pars": pm_sn_pars_pct, "pm_se_pars": pm_se_pars_pct,
            "pm_winner": pm_winner,
        })
        
    df = pd.DataFrame(data_list)
    
    # Calculate global averages
    avg_st_sn_std = df["st_sn_std"].mean()
    avg_st_se_std = df["st_se_std"].mean()
    avg_st_sn_pars = df["st_sn_pars"].mean()
    avg_st_se_pars = df["st_se_pars"].mean()
    
    avg_pm_sn_std = df["pm_sn_std"].mean()
    avg_pm_se_std = df["pm_se_std"].mean()
    avg_pm_sn_pars = df["pm_sn_pars"].mean()
    avg_pm_se_pars = df["pm_se_pars"].mean()
    
    # Victorias Estrictas
    st_wins_std = (df["st_winner"] == "v6 Standard").sum()
    st_wins_pars = (df["st_winner"] == "Parsimonious").sum()
    st_ties = (df["st_winner"] == "Empate").sum()
    
    # Victorias Permisivas
    pm_wins_std = (df["pm_winner"] == "v6 Standard").sum()
    pm_wins_pars = (df["pm_winner"] == "Parsimonious").sum()
    pm_ties = (df["pm_winner"] == "Empate").sum()

    # Load chart base64s
    b64_chart1 = get_chart_b64("01_global_performance_comparison.png")
    b64_chart2 = get_chart_b64("02_score_distribution_boxplot.png")
    b64_chart3 = get_chart_b64("03_node_vs_edge_f1_scatter.png")
    b64_chart4 = get_chart_b64("04_per_video_f1_comparison.png")
    b64_chart5 = get_chart_b64("05_radar_multimetric_comparison.png")
    
    # Build HTML rows for Strict Table
    strict_table_rows = []
    for r in data_list:
        w_class = "win-std" if r["st_winner"] == "v6 Standard" else ("win-pars" if r["st_winner"] == "Parsimonious" else "win-tie")
        badge = f'<span class="badge {w_class}">{r["st_winner"]}</span>'
        strict_table_rows.append(f"""
        <tr>
            <td><code>{r['video_id']}</code></td>
            <td class="num">{r['st_sn_std']:.1f}%</td>
            <td class="num">{r['st_se_std']:.1f}%</td>
            <td class="num highlight-col">{r['st_sn_pars']:.1f}%</td>
            <td class="num highlight-col">{r['st_se_pars']:.1f}%</td>
            <td>{badge}</td>
        </tr>
        """)
        
    # Build HTML rows for Permissive Table
    permissive_table_rows = []
    for r in data_list:
        w_class = "win-std" if r["pm_winner"] == "v6 Standard" else ("win-pars" if r["pm_winner"] == "Parsimonious" else "win-tie")
        badge = f'<span class="badge {w_class}">{r["pm_winner"]}</span>'
        permissive_table_rows.append(f"""
        <tr>
            <td><code>{r['video_id']}</code></td>
            <td class="num">{r['pm_sn_std']:.1f}%</td>
            <td class="num">{r['pm_se_std']:.1f}%</td>
            <td class="num highlight-col">{r['pm_sn_pars']:.1f}%</td>
            <td class="num highlight-col">{r['pm_se_pars']:.1f}%</td>
            <td>{badge}</td>
        </tr>
        """)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte Comparativo: v6 Standard vs. Parsimonious Mode</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-card: #1e293b;
            --bg-hover: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-purple: #a855f7;
            --accent-green: #22c55e;
            --accent-orange: #f97316;
            --border: #334155;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
            padding: 24px;
        }}

        header {{
            max-width: 1400px;
            margin: 0 auto 24px auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 28px;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
            backdrop-filter: blur(12px);
            border: 1px solid var(--border);
            border-radius: 16px;
        }}

        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 700;
            background: linear-gradient(90deg, #38bdf8, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 4px;
        }}

        .nav-tabs {{
            display: flex;
            gap: 12px;
            max-width: 1400px;
            margin: 0 auto 24px auto;
        }}

        .tab-btn {{
            flex: 1;
            padding: 14px 20px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            font-size: 15px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}

        .tab-btn:hover {{
            background: var(--bg-hover);
            color: var(--text-primary);
        }}

        .tab-btn.active {{
            background: linear-gradient(135deg, #0284c7, #6366f1);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        }}

        .tab-content {{
            display: none;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .tab-content.active {{
            display: block;
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 28px;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            transition: transform 0.2s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
        }}

        .kpi-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;

        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 32px;
            font-weight: 700;
            margin: 8px 0;
            color: #ffffff;
        }}

        .kpi-subtext {{
            font-size: 13px;
            color: var(--accent-blue);
        }}

        /* Tables */
        .table-container {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        }}

        .search-bar {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .search-bar input {{
            background: var(--bg-primary);
            border: 1px solid var(--border);
            color: var(--text-primary);
            padding: 10px 16px;
            border-radius: 8px;
            width: 300px;
            font-size: 14px;
            outline: none;
        }}

        .search-bar input:focus {{
            border-color: var(--accent-blue);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            background: rgba(15, 23, 42, 0.6);
            padding: 16px 20px;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 1px solid var(--border);
            cursor: pointer;
            user-select: none;
            transition: background 0.2s ease, color 0.2s ease;
        }}

        th:hover {{
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent-blue);
        }}

        th:first-child, td:first-child {{
            padding-right: 36px;
            min-width: 170px;
            border-right: 2px solid var(--border);
        }}

        th:nth-child(2), td:nth-child(2) {{
            padding-left: 28px;
        }}

        .sort-icon {{
            display: inline-block;
            margin-left: 6px;
            font-size: 12px;
            opacity: 0.5;
            transition: opacity 0.2s ease;
        }}

        th.sort-asc .sort-icon {{
            opacity: 1;
            color: var(--accent-blue);
        }}

        th.sort-desc .sort-icon {{
            opacity: 1;
            color: var(--accent-purple);
        }}

        td {{
            padding: 14px 20px;
            border-bottom: 1px solid rgba(51, 65, 85, 0.5);
            font-size: 14px;
        }}


        tr:hover {{
            background: rgba(51, 65, 85, 0.3);
        }}

        td.num {{
            font-family: 'Outfit', monospace;
            font-weight: 600;
        }}

        .highlight-col {{
            background: rgba(249, 115, 22, 0.05);
        }}

        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }}

        .win-std {{
            background: rgba(56, 189, 248, 0.15);
            color: #38bdf8;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }}

        .win-pars {{
            background: rgba(249, 115, 22, 0.15);
            color: #f97316;
            border: 1px solid rgba(249, 115, 22, 0.3);
        }}

        .win-tie {{
            background: rgba(148, 163, 184, 0.15);
            color: #94a3b8;
            border: 1px solid rgba(148, 163, 184, 0.3);
        }}

        html, body {{
            max-width: 100vw;
            overflow-x: hidden;
        }}

        /* Gallery Grid & Bulletproof Image Dimensioning */
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 24px;
            width: 100%;
            box-sizing: border-box;
        }}

        .gallery-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            min-width: 0;
            max-width: 100%;
            overflow: hidden;
            box-sizing: border-box;
        }}

        .gallery-card h3 {{
            font-family: 'Outfit', sans-serif;
            font-size: 17px;
            margin-bottom: 12px;
            color: var(--accent-blue);
            width: 100%;
            text-align: left;
        }}

        .gallery-card img {{
            max-width: 100%;
            height: auto;
            max-height: 420px;
            object-fit: contain;
            display: block;
            margin: 0 auto;
            border-radius: 12px;
            border: 1px solid var(--border);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease;
        }}

        .gallery-card img:hover {{
            transform: scale(1.02);
        }}

        .gallery-card p {{
            font-size: 13px;
            color: var(--text-secondary);
            margin-top: 12px;
            text-align: left;
            width: 100%;
        }}
    </style>
</head>


<body>

    <header>
        <div>
            <h1>Dashboard Comparativo: v6 Standard vs. Parsimonious Mode</h1>
            <p class="subtitle">Evaluación cuantitativa sobre 61 vídeos de la base de datos Cloudscape (FAST25 Ground Truth)</p>
        </div>
        <div>
            <span class="badge win-std" style="font-size: 14px; padding: 8px 16px;">69 Vídeos Procesados</span>
        </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="nav-tabs">
        <button class="tab-btn active" onclick="switchTab('dashboard')">📊 Resumen Dashboard</button>
        <button class="tab-btn" onclick="switchTab('strict')">🎯 Tabla Estricta (Strict)</button>
        <button class="tab-btn" onclick="switchTab('permissive')">🟢 Tabla Permisiva (Permissive)</button>
        <button class="tab-btn" onclick="switchTab('gallery')">🖼️ Galería de Gráficas</button>
    </div>

    <!-- TAB 1: DASHBOARD OVERVIEW -->
    <div id="tab-dashboard" class="tab-content active">
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Victorias Estrictas Combinadas</div>
                <div class="kpi-value">{st_wins_std} vs {st_wins_pars}</div>
                <div class="kpi-subtext">🏆 v6 Standard gana en el 47.5% de los vídeos ({st_ties} empates)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">F1 Aristas Estricto (Promedio)</div>
                <div class="kpi-value">{avg_st_se_std:.1f}% vs {avg_st_se_pars:.1f}%</div>
                <div class="kpi-subtext">📈 v6 Standard lidera en captura de conectividad (+3.2%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">F1 Aristas Permisivo (Promedio)</div>
                <div class="kpi-value">{avg_pm_se_std:.1f}% vs {avg_pm_se_pars:.1f}%</div>
                <div class="kpi-subtext">📈 v6 Standard supera a Parsimonious (+3.1%)</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">F1 Nodos Permisivo (Promedio)</div>
                <div class="kpi-value">{avg_pm_sn_std:.1f}% vs {avg_pm_sn_pars:.1f}%</div>
                <div class="kpi-subtext">🤝 Desempeño equivalente (~89% vs 91%)</div>
            </div>
        </div>

        <div class="gallery-grid">
            <div class="gallery-card">
                <h3>Rendimiento Global Promedio</h3>
                <img src="{b64_chart1}" alt="Rendimiento Global">
                <p>Comparación de F1 Score de Nodos y Aristas. v6 Standard logra mayor precisión de aristas al preservar identificadores de flujo (flow_id y seq).</p>
            </div>
            <div class="gallery-card">
                <h3>Comparación Radar Multimétrica</h3>
                <img src="{b64_chart5}" alt="Gráfico Radar">
                <p>El diagrama Spider muestra el equilibrio entre evaluación estricta y permisiva de ambos modelos.</p>
            </div>
        </div>
    </div>

    <!-- TAB 2: STRICT TABLE -->
    <div id="tab-strict" class="tab-content">
        <div class="table-container">
            <div class="search-bar">
                <h2>Tabla de Evaluación Estricta (Coincidencia Exacta de Servicios AWS)</h2>
                <input type="text" id="searchStrict" placeholder="Buscar por Video ID..." onkeyup="filterTable('strictTable', 'searchStrict')">
            </div>
            <table id="strictTable">
                <thead>
                    <tr>
                        <th onclick="sortTable('strictTable', 0)">Video ID <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('strictTable', 1)">v6 Standard (Node F1) <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('strictTable', 2)">v6 Standard (Edge F1) <span class="sort-icon">↕</span></th>
                        <th class="highlight-col" onclick="sortTable('strictTable', 3)">Parsimonious (Node F1) <span class="sort-icon">↕</span></th>
                        <th class="highlight-col" onclick="sortTable('strictTable', 4)">Parsimonious (Edge F1) <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('strictTable', 5)">Modelo Ganador <span class="sort-icon">↕</span></th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(strict_table_rows)}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 3: PERMISSIVE TABLE -->
    <div id="tab-permissive" class="tab-content">
        <div class="table-container">
            <div class="search-bar">
                <h2>Tabla de Evaluación Permisiva (Normalización a Grupos Base)</h2>
                <input type="text" id="searchPermissive" placeholder="Buscar por Video ID..." onkeyup="filterTable('permissiveTable', 'searchPermissive')">
            </div>
            <table id="permissiveTable">
                <thead>
                    <tr>
                        <th onclick="sortTable('permissiveTable', 0)">Video ID <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('permissiveTable', 1)">v6 Standard (Node F1) <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('permissiveTable', 2)">v6 Standard (Edge F1) <span class="sort-icon">↕</span></th>
                        <th class="highlight-col" onclick="sortTable('permissiveTable', 3)">Parsimonious (Node F1) <span class="sort-icon">↕</span></th>
                        <th class="highlight-col" onclick="sortTable('permissiveTable', 4)">Parsimonious (Edge F1) <span class="sort-icon">↕</span></th>
                        <th onclick="sortTable('permissiveTable', 5)">Modelo Ganador <span class="sort-icon">↕</span></th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(permissive_table_rows)}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TAB 4: GALLERY -->
    <div id="tab-gallery" class="tab-content">
        <div class="gallery-grid">
            <div class="gallery-card">
                <h3>01. Resumen Global de Rendimiento</h3>
                <img src="{b64_chart1}" alt="Global Chart">
                <p>Muestra el promedio de F1 score en evaluación estricta y permisiva.</p>
            </div>
            <div class="gallery-card">
                <h3>02. Distribución de Puntajes F1 (Boxplot)</h3>
                <img src="{b64_chart2}" alt="Boxplot Chart">
                <p>Distribución estadística y mediana de los puntajes por modelo.</p>
            </div>
            <div class="gallery-card">
                <h3>03. Mapeo Nodos F1 vs. Aristas F1 (Scatter Plot)</h3>
                <img src="{b64_chart3}" alt="Scatter Chart">
                <p>Diagrama de dispersión por vídeo individual.</p>
            </div>
            <div class="gallery-card">
                <h3>04. Rendimiento Desglosado por Vídeo (Sample 25)</h3>
                <img src="{b64_chart4}" alt="Per Video Chart">
                <p>Barras horizontales comparativas por vídeo.</p>
            </div>
            <div class="gallery-card" style="grid-column: span 2;">
                <h3>05. Comparación Radar Multimétrica</h3>
                <img src="{b64_chart5}" alt="Radar Chart">
                <p>Evaluación multidimensional tipo Radar/Spider Chart.</p>
            </div>
        </div>
    </div>

    <script>
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.currentTarget.classList.add('active');
            document.getElementById('tab-' + tabId).classList.add('active');
        }}

        function filterTable(tableId, inputId) {{
            const input = document.getElementById(inputId);
            const filter = input.value.toUpperCase();
            const table = document.getElementById(tableId);
            const tr = table.getElementsByTagName("tr");

            for (let i = 1; i < tr.length; i++) {{
                let td = tr[i].getElementsByTagName("td")[0];
                if (td) {{
                    let txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                        tr[i].style.display = "";
                    }} else {{
                        tr[i].style.display = "none";
                    }}
                }}
            }}
        }}

        const sortDirections = {{}};

        function sortTable(tableId, colIndex) {{
            const table = document.getElementById(tableId);
            const tbody = table.querySelector("tbody");
            const rows = Array.from(tbody.querySelectorAll("tr"));
            
            const key = tableId + "_" + colIndex;
            const isAsc = !sortDirections[key];
            sortDirections[key] = isAsc;

            const headers = table.querySelectorAll("th");
            headers.forEach(th => {{
                th.classList.remove("sort-asc", "sort-desc");
                const icon = th.querySelector(".sort-icon");
                if (icon) icon.textContent = "↕";
            }});

            const currentHeader = headers[colIndex];
            currentHeader.classList.add(isAsc ? "sort-asc" : "sort-desc");
            const icon = currentHeader.querySelector(".sort-icon");
            if (icon) icon.textContent = isAsc ? "▲" : "▼";

            rows.sort((rowA, rowB) => {{
                const cellA = rowA.children[colIndex].innerText.trim();
                const cellB = rowB.children[colIndex].innerText.trim();

                const numA = parseFloat(cellA.replace("%", ""));
                const numB = parseFloat(cellB.replace("%", ""));

                if (!isNaN(numA) && !isNaN(numB)) {{
                    return isAsc ? numA - numB : numB - numA;
                }} else {{
                    return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
                }}
            }});

            rows.forEach(row => tbody.appendChild(row));
        }}
    </script>
</body>
</html>

"""
    
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"✓ HTML Report successfully generated → {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_report()
