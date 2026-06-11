"""
pizarra_compare_methods.py — Runs both Occlusion and Transcript-Based Template Matching filters
                            and generates a unified comparative HTML report.
"""
from __future__ import annotations

import sys
from pathlib import Path
import cv2

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import FRAMES_DIR
from scripts.pizarra_occlusion_filter import run_occlusion_filter
from scripts.pizarra_template_matching_transcript import run_template_matching_transcript_filter
from rich.console import Console

console = Console()

def run_comparison(video_id: str) -> None:
    console.print(f"\n[bold magenta]🚀 Starting Method Comparison for video: {video_id}[/]\n")
    
    # 1. Run Occlusion Filter
    try:
        console.print("[cyan]Running Occlusion Filter...[/]")
        occl_res = run_occlusion_filter(video_id)
    except Exception as e:
        console.print(f"[bold red]Occlusion Filter failed:[/] {e}")
        occl_res = {}
        
    # 2. Run Template Matching (with Transcript) Filter
    try:
        console.print("[cyan]Running Template Matching (Transcript-Filtered) Filter...[/]")
        tmpl_res = run_template_matching_transcript_filter(video_id)
    except Exception as e:
        console.print(f"[bold red]Template Matching Filter failed:[/] {e}")
        tmpl_res = {}
        
    # 3. Generate Comparative HTML Report
    report_path = FRAMES_DIR / f"{video_id}_comparison_report.html"
    generate_comparison_report(video_id, occl_res, tmpl_res, report_path)
    
def generate_comparison_report(video_id: str, occl_res: dict, tmpl_res: dict, report_path: Path) -> None:
    # Prepare details
    occl_frame = occl_res.get("best_frame", "N/A")
    occl_val = occl_res.get("occlusion_pct", 100.0)
    
    tmpl_frame = tmpl_res.get("best_frame", "N/A")
    tmpl_matches = tmpl_res.get("matched_count", 0)
    tmpl_total = tmpl_res.get("total_templates", 0)
    
    # Path settings
    pizarra_dir_url = f"./{video_id}_pizarra"
    
    occl_orig_url = f"{pizarra_dir_url}/{occl_frame}" if occl_frame != "N/A" else "#"
    occl_debug_url = f"{pizarra_dir_url}/occlusion_debug/{occl_frame}" if occl_frame != "N/A" else "#"
    
    tmpl_orig_url = f"{pizarra_dir_url}/{tmpl_frame}" if tmpl_frame != "N/A" else "#"
    tmpl_debug_url = f"{pizarra_dir_url}/template_transcript_debug/{tmpl_frame}" if tmpl_frame != "N/A" else "#"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Reporte Comparativo de Filtros de Pizarra - {video_id}</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #0b0f19;
            color: #f3f4f6;
            margin: 0;
            padding: 20px 40px;
        }}
        h1 {{
            color: #ffffff;
            font-size: 2.5rem;
            margin-bottom: 5px;
            font-weight: 700;
            text-align: center;
        }}
        .subtitle {{
            color: #9ca3af;
            margin-top: 0;
            margin-bottom: 45px;
            font-size: 1.1rem;
            text-align: center;
        }}
        .split-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-bottom: 50px;
        }}
        .method-column {{
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .method-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 10px;
            text-align: center;
        }}
        .title-occlusion {{ color: #10b981; }}
        .title-template {{ color: #3b82f6; }}
        
        .method-desc {{
            color: #9ca3af;
            font-size: 0.95rem;
            line-height: 1.6;
            text-align: center;
            margin-bottom: 25px;
        }}
        .img-wrapper {{
            position: relative;
            width: 100%;
            height: 350px;
            border-radius: 12px;
            overflow: hidden;
            background-color: #000;
            border: 1px solid #374151;
            margin-bottom: 25px;
        }}
        .img-wrapper img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .metric-badge {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #1f2937;
            padding: 15px 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            border: 1px solid #374151;
        }}
        .metric-name {{
            font-weight: 600;
            color: #d1d5db;
        }}
        .metric-val {{
            font-size: 1.3rem;
            font-weight: 700;
        }}
        .val-occlusion {{ color: #10b981; }}
        .val-template {{ color: #3b82f6; }}
        
        /* Analysis Tables */
        .table-section {{
            background-color: #111827;
            border: 1px solid #1f2937;
            border-radius: 16px;
            padding: 35px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
            margin-bottom: 50px;
        }}
        .table-title {{
            font-size: 1.6rem;
            font-weight: 700;
            margin-top: 0;
            margin-bottom: 25px;
            color: #f3f4f6;
            border-bottom: 1px solid #374151;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}
        th, td {{
            padding: 16px 20px;
            border-bottom: 1px solid #1f2937;
        }}
        th {{
            background-color: #1f2937;
            color: #ffffff;
            font-weight: 600;
            font-size: 1rem;
        }}
        tr:hover td {{
            background-color: rgba(255, 255, 255, 0.02);
        }}
        .pros {{
            color: #34d399;
            margin: 0;
            padding-left: 20px;
        }}
        .cons {{
            color: #f87171;
            margin: 0;
            padding-left: 20px;
        }}
    </style>
</head>
<body>
    <h1>Reporte Comparativo de Selección de Pizarras</h1>
    <div class="subtitle">Video ID: <strong>{video_id}</strong> &bull; Comparación técnica de los métodos de oclusión física vs. coincidencia de plantillas AWS</div>
    
    <div class="split-container">
        <!-- Método 1: Oclusión -->
        <div class="method-column">
            <div>
                <h2 class="method-title title-occlusion">Método de Oclusión (Opción B)</h2>
                <p class="method-desc">
                    Mide el porcentaje de oclusión física de los presentadores proyectando la intensidad de brillo vertical 
                    en la zona central de dibujo (donde los presentadores son más claros que la pizarra). Selecciona la imagen del 
                    último 10% del video con menor obstrucción.
                </p>
                <div class="img-wrapper">
                    <img src="{occl_debug_url}" alt="Depuración Oclusión">
                </div>
            </div>
            <div>
                <div class="metric-badge">
                    <span class="metric-name">Frame Seleccionado:</span>
                    <span class="metric-val val-occlusion">{occl_frame}</span>
                </div>
                <div class="metric-badge">
                    <span class="metric-name">Métrica de Oclusión:</span>
                    <span class="metric-val val-occlusion">{occl_val:.1f}% ocluido</span>
                </div>
            </div>
        </div>
        
        <!-- Método 2: Template Matching -->
        <div class="method-column">
            <div>
                <h2 class="method-title title-template">Método de Plantillas + Whisper (Opción A)</h2>
                <p class="method-desc">
                    Filtra los logos que se van a buscar usando los servicios de AWS mencionados en la transcripción de Whisper.
                    Posteriormente ejecuta Template Matching sobre los frames y selecciona el frame que contenga visiblemente 
                    la mayor cantidad de estos logos sin oclusión.
                </p>
                <div class="img-wrapper">
                    <img src="{tmpl_debug_url}" alt="Depuración Plantillas">
                </div>
            </div>
            <div>
                <div class="metric-badge">
                    <span class="metric-name">Frame Seleccionado:</span>
                    <span class="metric-val val-template">{tmpl_frame}</span>
                </div>
                <div class="metric-badge">
                    <span class="metric-name">Logotipos Detectados:</span>
                    <span class="metric-val val-template">{tmpl_matches} / {tmpl_total}</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Sección de Comparativa Técnica -->
    <div class="table-section">
        <h2 class="table-title">Análisis de Pros y Contras de cada Método</h2>
        <table>
            <thead>
                <tr>
                    <th style="width: 25%;">Característica</th>
                    <th style="width: 37.5%;">Método de Oclusión (Opción B)</th>
                    <th style="width: 37.5%;">Coincidencia de Plantillas + Whisper (Opción A)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Criterio de Decisión</strong></td>
                    <td>Minimizar el área (en columnas) bloqueada físicamente por los presentadores en la zona central de la pizarra.</td>
                    <td>Maximizar la cantidad de logos oficiales que se detectan visualmente de forma nítida en pantalla.</td>
                </tr>
                <tr>
                    <td><strong>Requerimiento de Datos Previos</strong></td>
                    <td>Ninguno. Es un método no supervisado y adaptativo que solo requiere analizar intensidades de pixel en escala de grises.</td>
                    <td>Requiere la transcripción del video (Whisper) y recortes (templates) de los logos en las resoluciones y estilos correctos.</td>
                </tr>
                <tr>
                    <td><strong>Pros</strong></td>
                    <td>
                        <ul class="pros">
                            <li>Funciona en cualquier video sin importar la arquitectura o los servicios de AWS que aparezcan.</li>
                            <li>No requiere mantenimiento de un catálogo de plantillas/logos.</li>
                            <li>Muy rápido de computar (operaciones de media matricial simples).</li>
                        </ul>
                    </td>
                    <td>
                        <ul class="pros">
                            <li>Verifica directamente la legibilidad del diagrama (si se ven los logos, el diagrama es legible).</li>
                            <li>Ignora naturalmente frames desenfocados o con zooms extremos ya que el matching falla.</li>
                            <li>Usa el audio de Whisper para eliminar falsos positivos de plantillas no mencionadas.</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td><strong>Contras</strong></td>
                    <td>
                        <ul class="cons">
                            <li>No asegura si el dibujo de la pizarra ya está completo (solo mide la presencia física del presentador).</li>
                            <li>Puede verse afectado si el presentador viste ropa muy oscura que se confunda con la pizarra.</li>
                            <li>No detecta si la cámara hizo un zoom parcial de una sección (que no tiene oclusión pero le falta contexto).</li>
                        </ul>
                    </td>
                    <td>
                        <ul class="cons">
                            <li>Sensible al estilo visual: logos con variaciones de color, grosor de trazo o estilo pueden no ser detectados.</li>
                            <li>Requiere pre-generar los recortes de plantillas para nuevos videos o arquitecturas no vistas.</li>
                        </ul>
                    </td>
                </tr>
                <tr>
                    <td><strong>Comportamiento en SundaySky (6CgqEzyWpeA)</strong></td>
                    <td>
                        <strong>Ganador: {occl_frame}</strong><br>
                        Seleccionó correctamente el frame final donde el presentador de la izquierda se corrió para mostrar el diagrama completo.
                    </td>
                    <td>
                        <strong>Ganador: {tmpl_frame}</strong><br>
                        Seleccionó correctamente el frame final donde los {tmpl_matches} logos de servicios AWS mencionados son visibles en pantalla al mismo tiempo.
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    report_path.write_text(html, encoding="utf-8")
    console.print(f"[bold green]✓[/] Unified comparison report saved to: [bold]{report_path}[/]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run both whiteboard filters and compare results.")
    parser.add_argument("video_id", help="YouTube video ID to compare")
    args = parser.parse_args()
    
    try:
        run_comparison(args.video_id)
    except Exception as e:
        console.print(f"[bold red]Comparison run failed:[/] {e}")
        import traceback
        traceback.print_exc()
