"""
pizarra_template_matching.py — Whiteboard frame selection using AWS service icon template matching.
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

def run_template_matching_filter(video_id: str, threshold: float = 0.90) -> dict:
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    templates_dir = Path(__file__).resolve().parent.parent / "data" / "templates"
    debug_dir = pizarra_dir / "template_debug"
    report_path = FRAMES_DIR / f"{video_id}_template_report.html"
    
    if not pizarra_dir.exists():
        raise FileNotFoundError(f"Whiteboard directory not found: {pizarra_dir}. Please run pizarra_filter.py first.")
    if not templates_dir.exists() or not list(templates_dir.glob("*.jpg")):
        raise FileNotFoundError(f"Template directory or icons not found in: {templates_dir}")
        
    debug_dir.mkdir(parents=True, exist_ok=True)
    
    # Load all template images in grayscale
    templates = {}
    for p in templates_dir.glob("*.jpg"):
        if p.name == "verify_crops.jpg":
            continue
        templates[p.stem] = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
        
    # Get all copied whiteboard frames
    frames = sorted(pizarra_dir.glob("*.jpg"))
    # Filter out debug folders and best_ copies
    frames = [f for f in frames if f.parent == pizarra_dir and f.name.startswith(video_id)]
    
    if not frames:
        console.print("[yellow]⚠[/] No whiteboard frames found to analyze.")
        return {}
        
    console.print(f"\n[bold cyan]🔍 Running Template Matching analysis for {video_id}[/] ({len(frames)} frames)...")
    
    frame_results = []
    
    # Process each frame
    for idx, fp in enumerate(frames):
        img_color = cv2.imread(str(fp))
        if img_color is None:
            continue
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        
        debug_img = img_color.copy()
        matched_services = {}
        blocked_services = []
        
        # Match each template
        for t_name, t_img in templates.items():
            res = cv2.matchTemplate(img_gray, t_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= threshold:
                h_t, w_t = t_img.shape
                x1, y1 = max_loc
                x2, y2 = x1 + w_t, y1 + h_t
                matched_services[t_name] = {
                    "confidence": max_val,
                    "box": (x1, y1, x2, y2)
                }
                # Draw green bounding box for matches
                cv2.rectangle(debug_img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(debug_img, f"{t_name} ({max_val:.2f})", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                blocked_services.append(t_name)
                
        # Save debug visualization
        debug_fp = debug_dir / fp.name
        cv2.imwrite(str(debug_fp), debug_img)
        
        frame_results.append({
            "name": fp.name,
            "original_path": fp,
            "debug_path": debug_fp,
            "matched_count": len(matched_services),
            "matched_services": matched_services,
            "blocked_services": sorted(blocked_services),
            "index": idx
        })
        
    # Find the best frame
    # Selection rule:
    # 1. Maximize number of matched services.
    # 2. Tie-breaker: choose the LATEST frame (highest index) because it has the most complete drawings.
    best_score = max(f["matched_count"] for f in frame_results)
    candidates = [f for f in frame_results if f["matched_count"] == best_score]
    best_frame = max(candidates, key=lambda x: x["index"])
    
    # Copy best frame to a fixed name
    best_whiteboard_path = pizarra_dir / "best_whiteboard_template.jpg"
    shutil.copy(best_frame["original_path"], best_whiteboard_path)
    
    console.print(f"[bold green]✓[/] Best frame selected: [bold]{best_frame['name']}[/] (Matched: {best_frame['matched_count']}/{len(templates)})")
    console.print(f"[green]✓[/] Copied to [bold]{best_whiteboard_path}[/]")
    
    # Generate HTML Report
    generate_html_report(video_id, frame_results, best_frame, len(templates), report_path)
    
    return {
        "best_frame": best_frame["name"],
        "matched_count": best_frame["matched_count"],
        "total_templates": len(templates),
        "report_path": str(report_path)
    }

def generate_html_report(video_id: str, results: list[dict], best_frame: dict, total_templates: int, report_path: Path) -> None:
    html = []
    html.append(f"""<!DOCTYPE html>
<html>
<head>
    <title>Reporte de Coincidencia de Plantillas - {video_id}</title>
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
            background: linear-gradient(135deg, #1f2937, #1e3a8a);
            border: 1px solid #3b82f6;
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
            background-color: #3b82f6;
            color: #ffffff;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 12px;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
        }}
        .winner-title {{
            font-size: 1.8rem;
            font-weight: 700;
            margin: 0 0 10px 0;
            color: #60a5fa;
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
            border: 2px solid #60a5fa;
            box-shadow: 0 0 20px rgba(96, 165, 250, 0.2);
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
        .badge-winner {{
            background-color: #2563eb;
            color: #ffffff;
        }}
        .badge-candidate {{
            background-color: #4b5563;
            color: #d1d5db;
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
        .services-list {{
            margin-top: 10px;
            font-size: 0.85rem;
            color: #d1d5db;
        }}
        .service-tag {{
            display: inline-block;
            padding: 2px 6px;
            margin: 2px;
            border-radius: 4px;
            font-weight: 500;
        }}
        .service-tag-match {{
            background-color: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}
        .service-tag-block {{
            background-color: rgba(239, 68, 68, 0.2);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
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
    <h1>Reporte de Coincidencia de Plantillas (Template Matching)</h1>
    <div class="subtitle">Video ID: <strong>{video_id}</strong> &bull; Evalúa la visibilidad de los logotipos de AWS sobre la pizarra</div>
    
    <div class="summary-card">
        <div class="summary-left">
            <span class="winner-badge">Ganador Seleccionado</span>
            <h2 class="winner-title">{best_frame['name']}</h2>
            <p style="margin: 0; color: #d1d5db;">Esta imagen contiene el número máximo de servicios de AWS detectados sin obstrucción por los presentadores.</p>
        </div>
        <div class="summary-right">
            <div style="font-size: 2.8rem; font-weight: 700; color: #60a5fa;">{best_frame['matched_count']} / {total_templates}</div>
            <div style="color: #9ca3af; font-size: 0.9rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Logotipos Visibles</div>
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
        else:
            badge = '<span class="badge badge-candidate">Analizado</span>'
            
        score_pct = (r["matched_count"] / total_templates) * 100
        if score_pct >= 80:
            bar_color = "#10b981" # Green
        elif score_pct >= 40:
            bar_color = "#f59e0b" # Orange
        else:
            bar_color = "#ef4444" # Red
            
        orig_img_src = f"./{video_id}_pizarra/{r['name']}"
        debug_img_src = f"./{video_id}_pizarra/template_debug/{r['name']}"
        
        # Render service tags
        tags = []
        for name in sorted(best_frame["matched_services"].keys()):
            if name in r["matched_services"]:
                conf = r["matched_services"][name]["confidence"]
                tags.append(f'<span class="service-tag service-tag-match">✓ {name} ({conf:.2f})</span>')
            else:
                tags.append(f'<span class="service-tag service-tag-block">✗ {name}</span>')
                
        html.append(f"""
        <div class="{card_class}">
            <div class="img-container">
                <img src="{orig_img_src}" alt="{r['name']}">
                <img class="overlay-img" src="{debug_img_src}" alt="Depuración {r['name']}">
                <div class="hover-hint">Pasa el mouse para ver bounding boxes (en verde)</div>
            </div>
            <div class="card-content">
                <div class="card-header">
                    <h3 class="frame-name">{r['name']}</h3>
                    {badge}
                </div>
                <div class="metric-row">
                    <span class="metric-label">Logotipos Detectados:</span>
                    <span class="metric-value" style="color: {bar_color};">{r['matched_count']} / {total_templates}</span>
                </div>
                <div class="bar-container">
                    <div class="bar" style="width: {score_pct}%; background-color: {bar_color};"></div>
                </div>
                <div class="services-list">
                    <strong>Servicios:</strong><br>
                    {"".join(tags)}
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
    console.print(f"[bold green]✓[/] Interactive HTML template matching report saved to [bold]{report_path}[/]")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run whiteboard template matching filter.")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--threshold", type=float, default=0.90, help="Matching confidence threshold")
    args = parser.parse_args()
    
    try:
        run_template_matching_filter(args.video_id, threshold=args.threshold)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
