"""
pizarra_occlusion_filter.py — Secondary whiteboard filter based on presenter occlusion.
                              Generates a debug visualization and HTML report.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path
import cv2
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import FRAMES_DIR
from rich.console import Console

console = Console()

def run_occlusion_filter(video_id: str) -> dict:
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    debug_dir = pizarra_dir / "occlusion_debug"
    report_path = FRAMES_DIR / f"{video_id}_occlusion_report.html"
    
    if not pizarra_dir.exists():
        raise FileNotFoundError(f"Whiteboard directory not found: {pizarra_dir}. Please run pizarra_filter.py first.")
        
    debug_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all copied whiteboard frames
    frames = sorted(pizarra_dir.glob("*.jpg"))
    # Filter out any files inside debug directory
    frames = [f for f in frames if f.parent == pizarra_dir]
    
    if not frames:
        console.print("[yellow]⚠[/] No whiteboard frames found to analyze.")
        return {}
        
    console.print(f"\n[bold cyan]🔍 Analyzing presenter occlusion for {video_id}[/] ({len(frames)} frames)...")
    
    # 1. Determine candidates in the last 10% of the video
    # Ensure at least 3 candidates if possible
    candidate_count = max(3, int(np.ceil(len(frames) * 0.10)))
    candidate_count = min(candidate_count, len(frames))
    candidate_start_idx = len(frames) - candidate_count
    
    frame_results = []
    
    # 2. Process each frame
    for idx, fp in enumerate(frames):
        img = cv2.imread(str(fp))
        if img is None:
            continue
        h, w, c = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Central ROI coordinates (X: 25% to 75%, Y: 200 to 900)
        roi_x1, roi_x2 = int(w * 0.25), int(w * 0.75)
        roi_y1, roi_y2 = 200, 900
        
        roi = gray[roi_y1:roi_y2, roi_x1:roi_x2]
        col_means = np.mean(roi, axis=0)
        
        # Determine blocked columns (intensity > 55.0)
        occluded_cols = col_means > 55.0
        occlusion_pct = (np.sum(occluded_cols) / len(col_means)) * 100
        
        # Create debug visualization
        debug_img = img.copy()
        mask = np.zeros_like(img)
        
        for x in range(roi_x1, roi_x2):
            col_idx = x - roi_x1
            if occluded_cols[col_idx]:
                # Draw red translucent mask in the vertical range
                mask[roi_y1:roi_y2, x] = [0, 0, 255]
                
        # Apply translucent overlay
        cv2.addWeighted(mask, 0.3, debug_img, 1.0, 0, debug_img)
        # Draw yellow border around central ROI
        cv2.rectangle(debug_img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 2)
        
        # Save debug image
        debug_fp = debug_dir / fp.name
        cv2.imwrite(str(debug_fp), debug_img)
        
        is_candidate = idx >= candidate_start_idx
        
        frame_results.append({
            "name": fp.name,
            "original_path": fp,
            "debug_path": debug_fp,
            "occlusion_pct": occlusion_pct,
            "mean_intensity": np.mean(roi),
            "is_candidate": is_candidate
        })
        
    # 3. Find the best frame (candidate with MINIMUM occlusion)
    candidates = [f for f in frame_results if f["is_candidate"]]
    best_frame = min(candidates, key=lambda x: x["occlusion_pct"])
    
    # Copy best frame to a fixed name
    best_whiteboard_path = pizarra_dir / "best_whiteboard.jpg"
    shutil.copy(best_frame["original_path"], best_whiteboard_path)
    
    console.print(f"[bold green]✓[/] Best frame selected: [bold]{best_frame['name']}[/] (Occlusion: {best_frame['occlusion_pct']:.1f}%)")
    console.print(f"[green]✓[/] Copied to [bold]{best_whiteboard_path}[/]")
    
    # 4. Generate HTML Report
    generate_html_report(video_id, frame_results, best_frame, report_path)
    
    return {
        "best_frame": best_frame["name"],
        "occlusion_pct": best_frame["occlusion_pct"],
        "report_path": str(report_path)
    }

def generate_html_report(video_id: str, results: list[dict], best_frame: dict, report_path: Path) -> None:
    html = []
    html.append(f"""<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Oclusión de Presentadores - {video_id}</title>
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
        }}
        .subtitle {{
            color: #9ca3af;
            margin-top: 0;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #1f2937, #111827);
            border: 1px solid #374151;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            margin-bottom: 40px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .summary-left {{
            flex: 2;
        }}
        .summary-right {{
            flex: 1;
            text-align: right;
        }}
        .winner-badge {{
            background-color: #059669;
            color: #ffffff;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 12px;
            box-shadow: 0 0 15px rgba(5, 150, 105, 0.4);
        }}
        .winner-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0 0 10px 0;
            color: #34d399;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr));
            gap: 30px;
        }}
        .card {{
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .card:hover {{
            transform: translateY(-4px);
            border-color: #4b5563;
        }}
        .card-selected {{
            border: 2px solid #34d399;
            box-shadow: 0 0 20px rgba(52, 211, 153, 0.2);
        }}
        .img-container {{
            position: relative;
            width: 100%;
            height: 250px;
            overflow: hidden;
            background-color: #000;
        }}
        .img-container img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: opacity 0.3s;
        }}
        .img-container img.overlay-img {{
            position: absolute;
            top: 0;
            left: 0;
            opacity: 0;
        }}
        .img-container:hover img.overlay-img {{
            opacity: 1;
        }}
        .hover-hint {{
            position: absolute;
            bottom: 10px;
            right: 10px;
            background-color: rgba(0,0,0,0.7);
            color: #fff;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            pointer-events: none;
        }}
        .card-content {{
            padding: 20px;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .frame-name {{
            font-weight: 700;
            font-size: 1.1rem;
            margin: 0;
        }}
        .badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .badge-candidate {{
            background-color: #3b82f6;
            color: #ffffff;
        }}
        .badge-excluded {{
            background-color: #4b5563;
            color: #d1d5db;
        }}
        .badge-winner {{
            background-color: #10b981;
            color: #ffffff;
        }}
        .metric-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }}
        .metric-label {{
            color: #9ca3af;
        }}
        .metric-value {{
            font-weight: 600;
        }}
        .bar-container {{
            background-color: #374151;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 15px;
        }}
        .bar {{
            height: 100%;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>Reporte de Traslape y Oclusión de Presentadores</h1>
    <div class="subtitle">Video ID: <strong>{video_id}</strong> &bull; Analiza la posición de los presentadores en la zona central de la pizarra</div>
    
    <div class="summary-card">
        <div class="summary-left">
            <span class="winner-badge">Ganador Seleccionado</span>
            <h2 class="winner-title">{best_frame['name']}</h2>
            <p style="margin: 0; color: #d1d5db;">Esta imagen pertenece al último 10% del video y tiene el menor traslape con la zona de dibujo central de la pizarra.</p>
        </div>
        <div class="summary-right">
            <div style="font-size: 2.8rem; font-weight: 700; color: #34d399;">{best_frame['occlusion_pct']:.1f}%</div>
            <div style="color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Oclusión de Pizarra</div>
        </div>
    </div>

    <div class="grid">
""")

    for idx, r in enumerate(results):
        is_winner = r["name"] == best_frame["name"]
        card_class = "card card-selected" if is_winner else "card"
        
        # Badges
        if is_winner:
            badge = '<span class="badge badge-winner">Ganador</span>'
        elif r["is_candidate"]:
            badge = '<span class="badge badge-candidate">Candidato (Último 10%)</span>'
        else:
            badge = '<span class="badge badge-excluded">Excluido (Fase Inicial)</span>'
            
        # Color bar logic
        occl = r["occlusion_pct"]
        if occl < 30:
            bar_color = "#10b981" # Green
        elif occl < 60:
            bar_color = "#f59e0b" # Orange
        else:
            bar_color = "#ef4444" # Red
            
        # Paths for images inside the HTML report
        # The HTML report is in data/frames/{video_id}_occlusion_report.html
        # The images are in ./{video_id}_pizarra/{name}
        # The debug images are in ./{video_id}_pizarra/occlusion_debug/{name}
        orig_img_src = f"./{video_id}_pizarra/{r['name']}"
        debug_img_src = f"./{video_id}_pizarra/occlusion_debug/{r['name']}"
        
        html.append(f"""
        <div class="{card_class}">
            <div class="img-container">
                <img src="{orig_img_src}" alt="{r['name']}">
                <img class="overlay-img" src="{debug_img_src}" alt="Oclusión {r['name']}">
                <div class="hover-hint">Pasa el mouse para ver oclusión (en rojo)</div>
            </div>
            <div class="card-content">
                <div class="card-header">
                    <h3 class="frame-name">{r['name']}</h3>
                    {badge}
                </div>
                <div class="metric-row">
                    <span class="metric-label">Traslape de Presentadores:</span>
                    <span class="metric-value" style="color: {bar_color};">{occl:.1f}%</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Brillo Promedio Central:</span>
                    <span class="metric-value">{r['mean_intensity']:.1f}</span>
                </div>
                <div class="bar-container">
                    <div class="bar" style="width: {occl}%; background-color: {bar_color};"></div>
                </div>
            </div>
        </div>
        """)
        
    html.append("""
    </div>
</body>
</html>
""")
    
    report_path.write_text("\n".join(html), encoding="utf-8")
    console.print(f"[bold green]✓[/] Interactive HTML occlusion report saved to [bold]{report_path}[/]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run whiteboard presenter occlusion filter.")
    parser.add_argument("video_id", help="YouTube video ID")
    args = parser.parse_args()
    
    try:
        run_occlusion_filter(args.video_id)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
