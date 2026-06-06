"""
pizarra_filter.py — Local whiteboard frame filtering and deduplication reporting.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
import cv2
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import FRAMES_DIR, RAW_DIR, FRAME_INTERVAL_SEC
from rich.console import Console

console = Console()

def get_video_age_from_csv(video_id: str) -> str:
    """Find the video age by matching the title in videos.csv with info.json."""
    import json
    import pandas as pd
    info_path = Path(__file__).resolve().parent.parent / "data" / "raw" / f"{video_id}.info.json"
    csv_path = Path(__file__).resolve().parent.parent / "videos.csv"
    if not info_path.exists() or not csv_path.exists():
        return "unknown"
    try:
        with open(info_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        title = info.get("title", "").strip().lower()
        if not title:
            return "unknown"
        df = pd.read_csv(csv_path)
        title_clean = title.replace(":", "").replace("-", "").replace(" ", "")
        for _, row in df.iterrows():
            row_title = str(row["title"]).strip().lower()
            row_title_clean = row_title.replace(":", "").replace("-", "").replace(" ", "")
            if title_clean in row_title_clean or row_title_clean in title_clean:
                return str(row["age"]).strip()
    except Exception:
        pass
    return "unknown"

def filter_pizarra_frames(video_id: str, dark_threshold: float | None = None) -> dict:
    """
    Scan extracted frames for a video, identify close-up whiteboard frames,
    copy them to a separate '{video_id}_pizarra' directory, and compile
    a similarity comparison report.
    """
    video_frames_dir = FRAMES_DIR / video_id
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    
    if not video_frames_dir.exists():
        raise FileNotFoundError(f"Frames directory not found: {video_frames_dir}")
        
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean up old copied frames in pizarra_dir (starting with video_id)
    if pizarra_dir.exists():
        for fp in pizarra_dir.glob(f"{video_id}_frame_*.jpg"):
            try:
                fp.unlink()
            except Exception:
                pass
                
    if dark_threshold is None:
        age = get_video_age_from_csv(video_id)
        if age == "hace 1 año" or age == "unknown":
            dark_threshold = 75.0
            console.print(f"[cyan]Video age is '{age}'. Using default dark_threshold = {dark_threshold}[/]")
        else:
            dark_threshold = 38.0
            console.print(f"[cyan]Video age is '{age}' (older). Using adaptive dark_threshold = {dark_threshold}[/]")
    else:
        console.print(f"[cyan]Forcing user-specified dark_threshold = {dark_threshold}[/]")
        
    # Load transcript speech end if available
    transcript_path = RAW_DIR / f"{video_id}_transcript.json"
    last_speech_end = None
    if transcript_path.exists():
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                segments = json.load(f)
            if segments:
                last_speech_end = segments[-1].get("end")
                console.print(f"[cyan]Loaded transcript. Last speech ends at {last_speech_end}s[/]")
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to load transcript for timing check: {e}[/]")
            
    frames = sorted(video_frames_dir.glob("*.jpg"))
    close_ups = []
    
    # 1. Identify and copy close-up blackboard frames
    for fp in frames:
        # Extract frame number to compute frame time
        try:
            frame_num_str = fp.stem.split("_frame_")[-1]
            frame_num = int(frame_num_str)
        except Exception:
            frame_num = None
            
        if last_speech_end is not None and frame_num is not None:
            frame_time = (frame_num * FRAME_INTERVAL_SEC) - (FRAME_INTERVAL_SEC / 2)
            if frame_time > last_speech_end:
                console.print(f"[yellow]Skipping frame {fp.name} (frame_time {frame_time}s > last speech end {last_speech_end}s)[/]")
                continue

        img = cv2.imread(str(fp))
        if img is None:
            continue
        h, w, c = img.shape
        total_pixels = h * w
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Calculate percentage of dark pixels (value < 45)
        dark_px_pct = (np.sum(gray < 45) / total_pixels) * 100
        mean_val = np.mean(gray)
        
        # Safety check: skip completely blank black transition screens
        if mean_val < 5.0 or dark_px_pct > 95.0:
            continue
            
        if dark_px_pct >= dark_threshold:
            dest_path = pizarra_dir / fp.name
            shutil.copy(fp, dest_path)
            close_ups.append({
                "name": fp.name,
                "path": dest_path,
                "dark_pct": dark_px_pct,
                "gray_small": cv2.resize(gray, (256, 144))
            })
            
    console.print(f"[green]✓[/] Copied [bold]{len(close_ups)}[/] close-up blackboard frames to {pizarra_dir}/")
    
    # 2. Compare consecutive close-ups to build deduplication report
    report_path = FRAMES_DIR / f"{video_id}_pizarra_report.html"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Whiteboard Similarity Report - {video_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 20px; color: #333; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ background: #fff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); margin-bottom: 20px; }}
        .pair {{ display: flex; align-items: center; background: #fff; margin-bottom: 15px; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); gap: 20px; }}
        .img-container {{ flex: 1; text-align: center; }}
        .img-container img {{ max-width: 100%; border-radius: 4px; border: 1px solid #ddd; }}
        .img-label {{ font-weight: bold; margin-top: 5px; font-size: 14px; }}
        .comparison {{ flex: 1; text-align: center; padding: 20px; border-radius: 8px; }}
        .diff-score {{ font-size: 24px; font-weight: bold; margin-bottom: 10px; }}
        .badge {{ display: inline-block; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 14px; }}
        .badge-dup {{ background: #f8d7da; color: #721c24; }}
        .badge-diff {{ background: #d4edda; color: #155724; }}
    </style>
</head>
<body>
    <h1>Whiteboard Frame Comparison Report (Video: {video_id})</h1>
    <div class="summary">
        <p><strong>Total Close-up Whiteboard Frames Copied:</strong> {len(close_ups)}</p>
        <p>This report compares each consecutive close-up whiteboard frame. The <strong>Difference Score</strong> represents the Mean Absolute Error (MAE) on a 256x144 scale. Lower scores mean more similarity.</p>
    </div>
    <div>
    """
    
    for i in range(1, len(close_ups)):
        f1 = close_ups[i-1]
        f2 = close_ups[i]
        
        diff = np.mean(cv2.absdiff(f1["gray_small"], f2["gray_small"]))
        
        # We classify based on a default safety threshold of MAE < 8.0
        is_duplicate = diff < 8.0
        badge_class = "badge-dup" if is_duplicate else "badge-diff"
        badge_text = "Highly Similar (Potential Duplicate)" if is_duplicate else "Significant Change (New Drawing/Slide)"
        
        # relative paths to the pizarra folder
        img1_path = f"./{video_id}_pizarra/{f1['name']}"
        img2_path = f"./{video_id}_pizarra/{f2['name']}"
        
        html_content += f"""
        <div class="pair">
            <div class="img-container">
                <img src="{img1_path}">
                <div class="img-label">{f1['name']} ({f1['dark_pct']:.1f}% Dark)</div>
            </div>
            <div class="comparison" style="background: {'#fdf3f3' if is_duplicate else '#f3fdf5'};">
                <div class="diff-score" style="color: {'#c0392b' if is_duplicate else '#27ae60'};">MAE: {diff:.2f}</div>
                <div class="badge {badge_class}">{badge_text}</div>
            </div>
            <div class="img-container">
                <img src="{img2_path}">
                <div class="img-label">{f2['name']} ({f2['dark_pct']:.1f}% Dark)</div>
            </div>
        </div>
        """
        
    html_content += """
    </div>
</body>
</html>
"""
    
    report_path.write_text(html_content, encoding="utf-8")
    console.print(f"[green]✓[/] Similarity comparison report saved to {report_path}")
    
    return {
        "copied_count": len(close_ups),
        "pizarra_dir": str(pizarra_dir),
        "report_path": str(report_path)
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Filter whiteboard frames.")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--threshold", type=float, default=None, help="Dark pixel percentage threshold")
    args = parser.parse_args()
    
    try:
        filter_pizarra_frames(args.video_id, dark_threshold=args.threshold)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
