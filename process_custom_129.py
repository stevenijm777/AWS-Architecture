#!/usr/bin/env python3
import sys
import json
import shutil
import os
import time
from pathlib import Path

# Reconfigure stdout/stderr for Unicode support on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import cv2
import numpy as np
from rich.console import Console

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from config.settings import FRAMES_DIR, RAW_DIR, GRAPHS_DIR
from scripts.transcriber import get_timestamped_segments
from scripts.graph_builder import (
    create_graph_from_cloudscape_json,
    export_graphml,
    print_graph_summary,
)
from scripts.vision_analyzer import analyze_frame
from scripts.symbol_detector import detect_symbols

console = Console(force_terminal=True, legacy_windows=False)

def main():
    video_id = "iKYvG5aiIn8"
    video_path = RAW_DIR / f"{video_id}.mp4"
    transcript_path = RAW_DIR / f"{video_id}_transcript.json"

    if not video_path.exists():
        console.print(f"[bold red]Error: Video file not found:[/] {video_path}")
        sys.exit(1)

    # 1. Video Info
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        console.print(f"[bold red]Error: Failed to open video file:[/] {video_path}")
        sys.exit(1)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps else 0.0
    cap.release()

    console.print(f"[bold cyan]Video Details:[/]")
    console.print(f"  * Video Path: {video_path.name}")
    console.print(f"  * FPS: {fps:.3f}")
    console.print(f"  * Total Frames: {total_frames}")
    console.print(f"  * Duration: {duration:.2f}s")

    # Middle of video duration
    mid_time = duration / 2.0
    console.print(f"  * Middle of Video Time: {mid_time:.2f}s")
    
    # Last 15 seconds
    last_15s_start = duration - 15.0
    console.print(f"  * Last 15 seconds start: {last_15s_start:.2f}s")

    # 2. Compute custom timestamps
    # - Standard 10s interval from middle (mid_time) to last_15s_start
    # - High-frequency 1s interval from last_15s_start to end (duration)
    standard_times = []
    t = mid_time
    while t < last_15s_start:
        standard_times.append(t)
        t += 10.0
        
    last_15s_times = []
    t = last_15s_start
    while t <= duration:
        last_15s_times.append(t)
        t += 1.0

    timestamps = sorted(list(set(standard_times + last_15s_times)))
    console.print(f"[cyan]Custom timestamps generated ({len(timestamps)} frames total):[/]")
    console.print(f"  * Standard (10s intervals): {len(standard_times)} frames from {standard_times[0]:.1f}s to {standard_times[-1]:.1f}s")
    console.print(f"  * High-frequency (1s intervals): {len(last_15s_times)} frames from {last_15s_times[0]:.1f}s to {last_15s_times[-1]:.1f}s")

    # 3. Extract keyframes
    video_frames_dir = FRAMES_DIR / video_id
    video_frames_dir.mkdir(parents=True, exist_ok=True)
    # clean frames dir
    for f in video_frames_dir.glob("*.jpg"):
        f.unlink()

    console.print(f"\n[bold cyan]Extracting custom keyframes...[/]")
    cap = cv2.VideoCapture(str(video_path))
    extracted_frames = []
    for idx, t in enumerate(timestamps):
        frame_idx = int(round(t * fps))
        if frame_idx >= total_frames:
            frame_idx = total_frames - 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            console.print(f"[yellow]Warning: Failed to read frame at {t:.2f}s (index {frame_idx})[/]")
            continue
        
        # Name frames sequentially starting at 0001
        frame_name = f"{video_id}_frame_{idx + 1:04d}.jpg"
        frame_file = video_frames_dir / frame_name
        cv2.imwrite(str(frame_file), frame)
        extracted_frames.append({
            "name": frame_name,
            "path": frame_file,
            "time": t
        })
    cap.release()
    console.print(f"[green]Success:[/] Extracted [bold]{len(extracted_frames)}[/] frames to {video_frames_dir}/")

    # 4. Whiteboard filtering (pizarra_filter)
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    for f in pizarra_dir.glob("*.jpg"):
        try:
            f.unlink()
        except:
            pass
            
    # For video 129, since age is 'hace 4 años' (older), standard dark_threshold is 38.0
    dark_threshold = 38.0
    console.print(f"\n[bold cyan]Filtering whiteboard frames (threshold = {dark_threshold})...[/]")
    
    close_ups = []
    for item in extracted_frames:
        fp = item["path"]
        img = cv2.imread(str(fp))
        if img is None:
            continue
        h, w, c = img.shape
        total_pixels = h * w
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        dark_px_pct = (np.sum(gray < 45) / total_pixels) * 100
        mean_val = np.mean(gray)
        
        # Skip completely blank transition screens
        if mean_val < 5.0 or dark_px_pct > 95.0:
            console.print(f"  * Skipping blank/dark frame {fp.name}: mean {mean_val:.1f}, dark {dark_px_pct:.1f}%")
            continue
            
        if dark_px_pct >= dark_threshold:
            dest_path = pizarra_dir / fp.name
            shutil.copy(fp, dest_path)
            close_ups.append({
                "name": fp.name,
                "path": dest_path,
                "dark_pct": dark_px_pct,
                "gray_small": cv2.resize(gray, (256, 144)),
                "time": item["time"]
            })
            console.print(f"  * Kept whiteboard frame {fp.name} (dark_pct: {dark_px_pct:.1f}%)")

    console.print(f"[green]Success:[/] Filtered [bold]{len(close_ups)}[/] whiteboard frames into {pizarra_dir}/")
    if not close_ups:
        console.print("[bold red]Error: No whiteboard frames found after filtering.[/]")
        sys.exit(1)

    # 5. Occlusion Detection on all frames
    console.print(f"\n[bold cyan]Running presenter occlusion detection...[/]")
    
    # Initialize SSD-Lite person detector if available
    has_detector = False
    try:
        import torch
        import torchvision
        from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights

        device = "cuda" if torch.cuda.is_available() else "cpu"
        console.print(f"  * Initializing SSD-Lite person detector on [bold]{device}[/]...")
        weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
        model = ssdlite320_mobilenet_v3_large(weights=weights)
        model.to(device)
        model.eval()
        has_detector = True
    except ImportError:
        console.print("[yellow]Warning: torchvision is not installed. Using intensity-based occlusion detection fallback.[/]")

    debug_dir = pizarra_dir / "occlusion_debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    
    frame_results = []
    for idx, item in enumerate(close_ups):
        fp = item["path"]
        img = cv2.imread(str(fp))
        h, w, c = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Central ROI coordinates (X: 25% to 75%, Y: 200 to 900)
        roi_x1, roi_x2 = int(w * 0.25), int(w * 0.75)
        roi_y1, roi_y2 = 200, 900
        roi = gray[roi_y1:roi_y2, roi_x1:roi_x2]
        
        # Fast intensity-based occlusion as default/fallback
        col_means = np.mean(roi, axis=0)
        original_occluded_cols = col_means > 55.0
        occluded_cols = np.zeros_like(original_occluded_cols, dtype=bool)
        
        use_fallback = True
        if has_detector:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_tensor = torchvision.transforms.functional.to_tensor(img_rgb).to(device)
                
                with torch.no_grad():
                    predictions = model([img_tensor])
                    
                pred = predictions[0]
                boxes = pred["boxes"].cpu().numpy()
                labels = pred["labels"].cpu().numpy()
                scores = pred["scores"].cpu().numpy()
                
                person_detected = False
                for i in range(len(boxes)):
                    # Class 1 is 'person' in COCO
                    if labels[i] == 1 and scores[i] > 0.3:
                        person_detected = True
                        px1, py1, px2, py2 = boxes[i]
                        if py1 <= roi_y2 and py2 >= roi_y1:
                            x_start = max(int(px1), roi_x1)
                            x_end = min(int(px2), roi_x2)
                            if x_start < x_end:
                                occluded_cols[x_start - roi_x1 : x_end - roi_x1] = True
                
                if person_detected:
                    use_fallback = False
                else:
                    use_fallback = True
            except Exception as e:
                console.print(f"    [yellow]Warning: PyTorch failed on {fp.name}: {e}. Fallback to intensity.[/]")
                use_fallback = True

        if use_fallback:
            occluded_cols = original_occluded_cols

        occlusion_pct = (np.sum(occluded_cols) / len(occluded_cols)) * 100

        # Save debug visualization
        debug_img = img.copy()
        mask = np.zeros_like(img)
        for x in range(roi_x1, roi_x2):
            col_idx = x - roi_x1
            if occluded_cols[col_idx]:
                mask[roi_y1:roi_y2, x] = [0, 0, 255]
        cv2.addWeighted(mask, 0.3, debug_img, 1.0, 0, debug_img)
        cv2.rectangle(debug_img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 2)
        cv2.imwrite(str(debug_dir / fp.name), debug_img)

        frame_results.append({
            "name": fp.name,
            "path": fp,
            "occlusion_pct": occlusion_pct,
            "time": item["time"]
        })
        console.print(f"  * Frame {fp.name} at {item['time']:.1f}s: Occlusion = {occlusion_pct:.1f}%")

    # Select best frame (MINIMUM occlusion across ALL evaluated frames)
    best_frame = min(frame_results, key=lambda x: x["occlusion_pct"])
    best_whiteboard_path = pizarra_dir / "best_whiteboard.jpg"
    shutil.copy(best_frame["path"], best_whiteboard_path)

    console.print(f"[bold green]Success:[/] Best frame selected: [bold]{best_frame['name']}[/] at {best_frame['time']:.2f}s (Occlusion: {best_frame['occlusion_pct']:.1f}%)")
    console.print(f"[green]Success:[/] Saved best whiteboard to: {best_whiteboard_path}")

    # 6. Load full transcript
    if not transcript_path.exists():
        console.print(f"[bold red]Error: Transcript not found:[/] {transcript_path}")
        sys.exit(1)
        
    with open(transcript_path, "r", encoding="utf-8") as f:
        segments = json.load(f)
    
    transcript_text = " ".join(s.get("text", "").strip() for s in segments)
    console.print(f"\n[bold cyan]Transcript loaded:[/] {len(segments)} segments, {len(transcript_text)} characters")

    # 7. Symbol detection
    templates_dir = Path(__file__).resolve().parent / "data" / "templates"
    console.print(f"\n[bold cyan]Running symbol detection on best whiteboard...[/]")
    try:
        detected_symbols = detect_symbols(
            best_whiteboard_path,
            templates_dir,
            transcript_text=transcript_text,
            threshold=0.70
        )
        if detected_symbols:
            console.print("[green]Success:[/] Detected AWS symbols:")
            for service, occurrences in sorted(detected_symbols.items()):
                console.print(f"  * [bold cyan]{service}[/]: {len(occurrences)} occurrence(s)")
        else:
            console.print("  No AWS symbols detected.")
    except Exception as e:
        console.print(f"[yellow]Warning: Symbol detection failed: {e}[/]")
        detected_symbols = None

    # 8. Gemini Vision Analysis
    console.print(f"\n[bold cyan]Running Gemini Vision Analysis...[/]")
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    max_retries = 3
    retry_delay = 5
    analysis_result = None
    
    # List of models to try in order
    models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    
    for model_name in models_to_try:
        import scripts.vision_analyzer
        scripts.vision_analyzer.GEMINI_MODEL = model_name
        console.print(f"  * Using model: [bold]{model_name}[/]")
        
        success = False
        for attempt in range(1, max_retries + 1):
            try:
                analysis_result = analyze_frame(
                    best_whiteboard_path,
                    transcript=transcript_text,
                    video_url=url,
                    detected_symbols=detected_symbols,
                )
                success = True
                break
            except Exception as e:
                console.print(f"    [yellow]Warning: Attempt {attempt} failed with error: {e}[/]")
                if attempt < max_retries:
                    console.print(f"    Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                else:
                    console.print(f"    [red]All {max_retries} attempts failed for model {model_name}.[/]")
        
        if success and analysis_result:
            break
            
    if not analysis_result:
        console.print("[bold red]Error: Gemini Vision Analysis failed on all models and attempts.[/]")
        sys.exit(1)
        
    analysis_path = RAW_DIR / f"{video_id}_vision_analysis.json"
    analysis_path.write_text(
        json.dumps(analysis_result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    console.print(f"[green]Success:[/] Analysis saved to: {analysis_path}")

    # 9. Build Graph and Export GraphML locally
    console.print(f"\n[bold cyan]Building Graph...[/]")
    G = create_graph_from_cloudscape_json(
        analysis_result,
        video_id=video_id,
        video_url=url,
    )

    # Export to standard graphs folder
    graphml_path = export_graphml(G, video_id)
    print_graph_summary(G)

    # Copy GraphML files to cloudscape_gt folder
    gt_dir = Path("data/cloudscape_gt")
    gt_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(graphml_path, gt_dir / f"{video_id}.graphml")
    console.print(f"[green]Success:[/] GraphML copied to local: {gt_dir / f'{video_id}.graphml'}")

    # 10. Copy best whiteboard to best_whiteboard/iKYvG5aiIn8/best_whiteboard.png
    best_wb_out_dir = Path("best_whiteboard") / video_id
    best_wb_out_dir.mkdir(parents=True, exist_ok=True)
    best_wb_out_path = best_wb_out_dir / "best_whiteboard.png"
    shutil.copy(best_whiteboard_path, best_wb_out_path)
    console.print(f"[green]Success:[/] Best whiteboard image saved locally to: {best_wb_out_path}")
    
    console.print("\n[bold green]Finished successfully! (All files saved locally)[/]\n")

if __name__ == "__main__":
    main()

