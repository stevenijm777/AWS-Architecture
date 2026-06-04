"""
pizarra_fine_extractor.py — Extract high-resolution temporal frames (fine interval) 
                            only from time segments where close-up whiteboard diagrams are active,
                            and generate a similarity report.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
import cv2
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import RAW_DIR, FRAMES_DIR, FRAME_INTERVAL_SEC
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

def extract_fine_pizarra_frames(
    video_id: str, 
    coarse_interval: int = FRAME_INTERVAL_SEC,
    fine_interval: int = 2,
    dark_threshold: float | None = None
) -> None:
    """
    1. Scan 'data/frames/{video_id}_pizarra' to find which coarse frames were close-up whiteboards.
    2. Convert those frame indexes into active time segments.
    3. Merge contiguous/overlapping segments.
    4. Run FFmpeg to extract frames at a smaller interval (fine_interval) only during those segments.
    5. Filter the newly extracted fine frames to keep only close-up whiteboards.
    6. Generate a similarity comparison report to let the user review frame changes.
    """
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    fine_dir = FRAMES_DIR / f"{video_id}_pizarra_fine"
    video_path = RAW_DIR / f"{video_id}.mp4"
    
    if not pizarra_dir.exists():
        raise FileNotFoundError(f"Coarse whiteboard directory not found: {pizarra_dir}. Please run pizarra_filter.py first.")
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    if dark_threshold is None:
        age = get_video_age_from_csv(video_id)
        if age == "hace 1 año" or age == "unknown":
            dark_threshold = 75.0
            console.print(f"[cyan]Video age is '{age}'. Using default dark_threshold = {dark_threshold}[/]")
        else:
            dark_threshold = 45.0
            console.print(f"[cyan]Video age is '{age}' (older). Using adaptive dark_threshold = {dark_threshold}[/]")
    else:
        console.print(f"[cyan]Forcing user-specified dark_threshold = {dark_threshold}[/]")
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    fine_dir = FRAMES_DIR / f"{video_id}_pizarra_fine"
    video_path = RAW_DIR / f"{video_id}.mp4"
    
    if not pizarra_dir.exists():
        raise FileNotFoundError(f"Coarse whiteboard directory not found: {pizarra_dir}. Please run pizarra_filter.py first.")
    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")
        
    # Clean and recreate fine directory
    if fine_dir.exists():
        shutil.rmtree(fine_dir)
    fine_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Parse frame numbers from pizarra_dir
    coarse_frames = sorted(pizarra_dir.glob("*.jpg"))
    if not coarse_frames:
        console.print("[yellow]⚠[/] No whiteboard frames found in coarse directory.")
        return
        
    frame_indices = []
    for fp in coarse_frames:
        try:
            num = int(fp.stem.split("_frame_")[-1])
            frame_indices.append(num)
        except (ValueError, IndexError):
            continue
            
    if not frame_indices:
        console.print("[yellow]⚠[/] Could not parse frame indices from filenames.")
        return
        
    # 2. Convert to time segments [start, end]
    segments = []
    for idx in sorted(frame_indices):
        start = (idx - 1) * coarse_interval
        end = idx * coarse_interval
        segments.append([start, end])
        
    # 3. Merge overlapping or adjacent segments
    merged_segments = []
    for seg in sorted(segments, key=lambda x: x[0]):
        if not merged_segments:
            merged_segments.append(seg)
        else:
            prev = merged_segments[-1]
            if seg[0] <= prev[1]:  # overlapping or adjacent
                prev[1] = max(prev[1], seg[1])
            else:
                merged_segments.append(seg)
                
    console.print(f"[cyan]Active whiteboard time ranges detected ({len(merged_segments)} segments):[/]")
    for seg in merged_segments:
        console.print(f"  • {seg[0]}s to {seg[1]}s")
        
    # 4. Extract frames with fine_interval only during those segments
    temp_dir = FRAMES_DIR / f"{video_id}_pizarra_fine_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean temp dir if it exists
    for f in temp_dir.glob("*.jpg"):
        f.unlink()
        
    console.print(f"\n[bold cyan]🖼  Extracting fine-interval keyframes[/] every {fine_interval}s from active segments...")
    
    for idx, (start, end) in enumerate(merged_segments, 1):
        duration = end - start
        pattern = str(temp_dir / f"seg_{idx:02d}_frame_%04d.jpg")
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start),
            "-t", str(duration),
            "-i", str(video_path),
            "-vf", f"fps=1/{fine_interval}",
            "-q:v", "2",
            pattern
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[red]✗[/] FFmpeg error on segment {idx}: {result.stderr[:200]}")
            continue
            
    # 5. Filter and copy only close-ups to fine_dir
    temp_frames = sorted(temp_dir.glob("*.jpg"))
    console.print(f"Extracted {len(temp_frames)} raw fine-interval frames. Filtering close-ups...")
    
    close_ups = []
    copied_count = 0
    for fp in temp_frames:
        img = cv2.imread(str(fp))
        if img is None:
            continue
        h, w, c = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dark_px_pct = (np.sum(gray < 45) / (h * w)) * 100
        mean_val = np.mean(gray)
        
        # Safety check: skip completely blank black transition screens
        if mean_val < 5.0 or dark_px_pct > 95.0:
            continue
            
        if dark_px_pct >= dark_threshold:
            dest_name = f"{video_id}_fine_{copied_count+1:04d}.jpg"
            dest_path = fine_dir / dest_name
            shutil.copy(fp, dest_path)
            close_ups.append({
                "name": dest_name,
                "path": dest_path,
                "dark_pct": dark_px_pct,
                "gray_small": cv2.resize(gray, (256, 144))
            })
            copied_count += 1
            
    # Clean up temp dir
    shutil.rmtree(temp_dir)
    
    console.print(f"[bold green]✓[/] Successfully saved [bold]{copied_count}[/] filtered fine-interval whiteboard frames to {fine_dir}/")
    
    # 6. Generate similarity comparison report
    report_path = FRAMES_DIR / f"{video_id}_pizarra_fine_report.html"
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Fine-Interval Whiteboard Similarity Report - {video_id}</title>
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
    <h1>Fine-Interval Whiteboard Frame Comparison Report (Video: {video_id})</h1>
    <div class="summary">
        <p><strong>Total Fine-Interval Whiteboard Frames Saved:</strong> {len(close_ups)} (extracted every {fine_interval}s)</p>
        <p>This report compares each consecutive close-up whiteboard frame. The <strong>Difference Score</strong> represents the Mean Absolute Error (MAE) on a 256x144 scale. Lower scores mean more similarity.</p>
    </div>
    <div>
    """
    
    for i in range(1, len(close_ups)):
        f1 = close_ups[i-1]
        f2 = close_ups[i]
        
        diff = np.mean(cv2.absdiff(f1["gray_small"], f2["gray_small"]))
        
        # We classify based on a default safety threshold of MAE < 6.0
        is_duplicate = diff < 6.0
        badge_class = "badge-dup" if is_duplicate else "badge-diff"
        badge_text = "Highly Similar (Potential Duplicate)" if is_duplicate else "Significant Change (New Drawing/Slide)"
        
        img1_path = f"./{video_id}_pizarra_fine/{f1['name']}"
        img2_path = f"./{video_id}_pizarra_fine/{f2['name']}"
        
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract fine-interval whiteboard frames.")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--coarse", type=int, default=FRAME_INTERVAL_SEC, help="Coarse frame interval in seconds")
    parser.add_argument("--fine", type=int, default=2, help="Fine frame interval in seconds")
    parser.add_argument("--threshold", type=float, default=None, help="Dark pixel percentage threshold")
    args = parser.parse_args()
    
    try:
        extract_fine_pizarra_frames(
            args.video_id,
            coarse_interval=args.coarse,
            fine_interval=args.fine,
            dark_threshold=args.threshold
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
