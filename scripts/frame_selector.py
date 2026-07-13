#!/usr/bin/env python3
"""
frame_selector.py — Intelligent frame selection for architecture whiteboard extraction.

Selects the best frame to send to Gemini by:
1. Discarding credit screens / end slides (dark + text patterns)
2. Detecting frames with colorful AWS service icons (saturated square regions)
3. Scoring occlusion (presenter blocking the whiteboard)
4. Preferring later frames (where the diagram is most complete)

This replaces the naive "use the last frame" approach and integrates the
pizarra_filter + occlusion_filter into a single, automatic step.

Usage:
    # Select best frame for a video
    python scripts/frame_selector.py VIDEO_ID

    # With debug output
    python scripts/frame_selector.py VIDEO_ID --debug
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import cv2
import numpy as np
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import FRAMES_DIR, RAW_DIR, FRAME_INTERVAL_SEC

console = Console()

# ── Credit/Outro detection ──────────────────────────────────────

# Known outro text patterns (case-insensitive substrings)
OUTRO_KEYWORDS = [
    "thank you", "for watching", "for more information",
    "this-is-my-architecture", "aws.amazon.com",
    "gracias", "merci",
]


def compute_sat_pixel_pct(img: np.ndarray) -> float:
    """
    Compute the percentage of highly-saturated, bright pixels in a frame.
    AWS service icons are colorful (high sat + decent brightness).
    Credit screens and logos have very few such pixels (< 0.05).
    Good architecture frames have many (> 0.10).
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    return np.sum(sat_mask) / (img.shape[0] * img.shape[1])


def is_credit_screen(img: np.ndarray) -> bool:
    """
    Detect credit/end screens using the key discriminator:
    saturated pixel percentage (sat_px%).
    
    Architecture frames with AWS icons: sat_px% > 0.10
    Credit screens ("Thank you", globe): sat_px% ≈ 0.03
    AWS logos: sat_px% ≈ 0.001
    """
    h, w = img.shape[:2]
    total_px = h * w
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Primary check: saturated pixel percentage
    sat_pct = compute_sat_pixel_pct(img)

    # Check 1: Nearly uniform / logo frame (very low std dev)
    if np.std(gray) < 20 and np.mean(gray) < 60:
        return True

    # Check 2: Predominantly dark AND very few saturated pixels
    # This catches "Thank you for watching" screens that have some
    # colorful elements (globe, orange text) but far fewer than real icons
    dark_pct = np.sum(gray < 50) / total_px
    if dark_pct > 0.70 and sat_pct < 0.08:
        return True

    return False


def is_blank_transition(img: np.ndarray) -> bool:
    """Detect fully black/blank transition frames."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return np.mean(gray) < 8.0


# ── Content scoring (AWS icon detection) ────────────────────────

def score_colorful_regions(img: np.ndarray) -> float:
    """
    Score a frame by how many colorful, saturated rectangular regions it has.
    AWS service icons are distinctive: bright, saturated, roughly square patches.
    
    Returns a score from 0.0 (no colorful content) to 1.0 (rich in icons).
    """
    h, w = img.shape[:2]
    total_px = h * w
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Find highly saturated pixels (S > 80) with decent brightness (V > 60)
    # This catches orange (Lambda), pink (CloudWatch), blue (Aurora), green arrows, etc.
    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    sat_pct = np.sum(sat_mask) / total_px

    # Find contours in the saturated mask to count "icon-like" rectangular blobs
    sat_uint8 = sat_mask.astype(np.uint8) * 255
    # Morphological opening (5x5) to remove thin drawings/lines
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened = cv2.morphologyEx(sat_uint8, cv2.MORPH_OPEN, kernel_open)
    # Morphological close (15x15) to connect nearby saturated pixels into blobs
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    icon_count = 0
    icon_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, cw, ch = cv2.boundingRect(cnt)

        # Filter: minimum size, roughly square-ish (aspect ratio 0.3-3.0)
        min_side = min(h, w) * 0.02  # ~2% of frame dimension
        max_side = min(h, w) * 0.25  # ~25% of frame dimension
        if cw < min_side or ch < min_side:
            continue
        if cw > max_side or ch > max_side:
            continue

        aspect = cw / ch if ch > 0 else 0
        if 0.3 < aspect < 3.0:
            icon_count += 1
            icon_area += area

    # Combine: percentage of saturated pixels + number of icon-like blobs
    # Normalize icon_count: typical architecture has 5-15 icons
    icon_score = min(icon_count / 10.0, 1.0)
    area_score = min(sat_pct * 20, 1.0)  # 5% saturated pixels → score 1.0

    # Weighted combination
    return 0.6 * icon_score + 0.4 * area_score


def score_whiteboard_content(img: np.ndarray) -> float:
    """
    Score how much "whiteboard content" (drawings, text, icons) a frame has.
    Combines:
    - Colorful icon detection (see above)
    - Edge density in the central region (drawn arrows, text)
    """
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Central ROI (skip borders where presenter stands and frame borders)
    roi_x1, roi_x2 = int(w * 0.15), int(w * 0.85)
    roi_y1, roi_y2 = int(h * 0.10), int(h * 0.90)
    roi = gray[roi_y1:roi_y2, roi_x1:roi_x2]

    # Edge density in ROI (Canny)
    edges = cv2.Canny(roi, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size

    # Color score
    color_score = score_colorful_regions(img)

    # Combine: color is more reliable than edge density
    return 0.7 * color_score + 0.3 * min(edge_density * 10, 1.0)


# ── Occlusion estimation ───────────────────────────────────────

def mask_service_icons(img: np.ndarray) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    """
    Detect highly saturated, square-like regions (AWS service icons) in the image
    and return:
      - A copy of the image with those regions blacked out.
      - A list of bounding boxes (x, y, w, h) for the detected icons.
    This prevents them from being misidentified as presenter occlusion.
    """
    masked_img = img.copy()
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Saturated pixel threshold
    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    sat_uint8 = sat_mask.astype(np.uint8) * 255
    
    # Morphological opening (5x5) to remove thin drawings/lines
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened = cv2.morphologyEx(sat_uint8, cv2.MORPH_OPEN, kernel_open)
    
    # Morphological close to group pixels into blobs
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_icons = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        
        min_side = min(h, w) * 0.015  # ~1.5% of min dimension
        max_side = min(h, w) * 0.25   # ~25% of min dimension
        
        if cw < min_side or ch < min_side:
            continue
        if cw > max_side or ch > max_side:
            continue
            
        aspect = cw / ch if ch > 0 else 0
        # AWS icons are roughly square (aspect ratio 0.6 to 1.6)
        if 0.6 < aspect < 1.6:
            # Black out this region to exclude it from occlusion estimation
            masked_img[y:y+ch, x:x+cw] = 0
            detected_icons.append((x, y, cw, ch))
            
    return masked_img, detected_icons


def estimate_occlusion_fast(img: np.ndarray, debug_save_path: Path | str | None = None) -> float:
    """
    Fast occlusion estimation without PyTorch.
    Uses skin-color detection + vertical column analysis to find presenter regions,
    while ignoring square-like highly-saturated regions (AWS service icons).
    
    Returns occlusion percentage (0-100). Lower is better.
    """
    img_masked, detected_icons = mask_service_icons(img)
    
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)

    # Central ROI where presenter typically stands
    roi_x1, roi_x2 = int(w * 0.10), int(w * 0.90)
    roi_y1 = int(h * 0.15)
    roi_y2 = int(h * 0.95)
    roi_hsv = hsv[roi_y1:roi_y2, roi_x1:roi_x2]
    roi_gray = cv2.cvtColor(img_masked[roi_y1:roi_y2, roi_x1:roi_x2], cv2.COLOR_BGR2GRAY)

    roi_w = roi_x2 - roi_x1

    # Skin-tone detection (broad range covering different skin tones)
    # HSV ranges for skin: H=0-25, S=30-170, V=60-255
    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([25, 170, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(roi_hsv, lower_skin, upper_skin)

    # Also detect clothing: medium brightness, low saturation columns
    # A presenter is a vertical band of non-whiteboard pixels
    col_skin_pct = np.mean(skin_mask > 0, axis=0)

    # A column is "occluded" if it has >15% skin-tone pixels
    # or if the column mean intensity is significantly higher than the dark whiteboard
    col_bright = np.mean(roi_gray, axis=0)
    dark_threshold = np.percentile(col_bright, 25)  # baseline darkness
    bright_cols = col_bright > (dark_threshold + 40)

    # Combine: column is occluded if has skin OR is significantly brighter
    occluded_cols = (col_skin_pct > 0.12) | (bright_cols & (col_skin_pct > 0.03))

    # Apply morphological closing to fill gaps in presenter silhouette
    occluded_uint8 = occluded_cols.astype(np.uint8)
    kernel = np.ones(int(roi_w * 0.05), dtype=np.uint8)
    occluded_closed = cv2.morphologyEx(occluded_uint8, cv2.MORPH_CLOSE, kernel)

    occlusion_pct = np.sum(occluded_closed > 0) / len(occluded_closed) * 100
    
    if debug_save_path is not None:
        debug_img = img.copy()
        
        # Draw detected service icons in green boxes
        for (ix, iy, iw, ih) in detected_icons:
            cv2.rectangle(debug_img, (ix, iy), (ix + iw, iy + ih), (0, 255, 0), 2)
            cv2.putText(debug_img, "Service", (ix, iy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
        # Draw vertical column occlusion mask in translucent red
        overlay = debug_img.copy()
        for x_idx in range(roi_w):
            if occluded_closed[x_idx] > 0:
                abs_x = roi_x1 + x_idx
                cv2.line(overlay, (abs_x, roi_y1), (abs_x, roi_y2), (0, 0, 255), 1)
        
        cv2.addWeighted(overlay, 0.4, debug_img, 0.6, 0, debug_img)
        
        # Draw ROI rectangle in yellow
        cv2.rectangle(debug_img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 2)
        
        # Write text info
        cv2.putText(
            debug_img,
            f"Occlusion: {occlusion_pct:.1f}%",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 255),
            2,
        )
        
        cv2.imwrite(str(debug_save_path), debug_img)
        
    return occlusion_pct



# ── Main frame selection logic ──────────────────────────────────

def select_best_frame(
    video_id: str,
    frames_dir: Path | None = None,
    debug: bool = False,
) -> dict:
    """
    Select the best whiteboard frame for a video following the user's updated Whisper-centric algorithm:
    1. Whisper time bounds.
    2. Focus on last 60% of frames (start_idx = 40%).
    3. Dark percentage calibration.
    4. Mask saturated icons.
    5. Calculate score = (edge_density * 50) - (occlusion * 5) where occlusion is calculated on img_masked.
    """
    frames_dir = frames_dir or FRAMES_DIR
    video_frames_dir = frames_dir / video_id

    if not video_frames_dir.exists():
        raise FileNotFoundError(f"Frames directory not found: {video_frames_dir}")

    # Get all frame files sorted by number
    all_frames = sorted(
        video_frames_dir.glob(f"{video_id}_frame_*.jpg"),
        key=lambda p: int(p.stem.split("_frame_")[-1]),
    )

    if not all_frames:
        raise FileNotFoundError(f"No frames found in {video_frames_dir}")

    total = len(all_frames)
    console.print(f"\n[bold cyan]🔍 Frame Selection for {video_id}[/] ({total} frames total)")

    # 1. INTELIGENCIA DE TIEMPO (WHISPER)
    transcript_path = RAW_DIR / f"{video_id}_transcript.json"
    ultimo_segundo_hablado = None

    if transcript_path.exists():
        try:
            with open(transcript_path, "r", encoding="utf-8") as f:
                segmentos = json.load(f)
                if segmentos:
                    ultimo_segundo_hablado = segmentos[-1].get("end")
                    console.print(f"🎙️ Whisper: Última palabra en el segundo {ultimo_segundo_hablado:.2f}s")
        except Exception as e:
            console.print(f"[yellow]⚠ Failed to load transcript for timing: {e}[/]")
    
    if ultimo_segundo_hablado is None:
        console.print(f"⚠️ No se encontró transcripción, no se aplicará corte de tiempo.")
        # Default fallback value for filter check
        filter_limit_sec = 999999.0
    else:
        filter_limit_sec = ultimo_segundo_hablado

    # Get FPS
    video_path = RAW_DIR / f"{video_id}.mp4"
    if video_path.exists():
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        cap.release()
    else:
        fps = 30.0

    # Load candidates from the last 60% of the video
    start_idx = int(total * 0.4)
    if ultimo_segundo_hablado is not None:
        # If Whisper is active, we can safely search until the very end because Whisper will cut the outro precisely
        candidates = all_frames[start_idx:]
        console.print(f"🚀 Procesando {len(candidates)} frames candidatos (Whisper activo)...")
    else:
        # Fallback: slice off the last 5% to avoid the outro screen
        end_idx = max(start_idx + 1, total - max(5, int(total * 0.05)))
        candidates = all_frames[start_idx:end_idx]
        console.print(f"🚀 Procesando {len(candidates)} frames candidatos (rango: {start_idx} a {end_idx}, fallback sin Whisper)...")

    # 2. CALIBRACIÓN DE OSCURIDAD
    max_dark_pct = 0.0
    for fp in candidates:
        img = cv2.imread(str(fp))
        if img is None:
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dark_pct = np.sum(gray < 50) / gray.size
        if dark_pct > max_dark_pct:
            max_dark_pct = dark_pct

    dynamic_threshold = max_dark_pct * 0.40
    console.print(f"🎚️ Oscuridad Máxima: {max_dark_pct:.1%}. Umbral Mínimo: {dynamic_threshold:.1%}")

    scored_frames = []
    discarded = []

    # 3. FILTRADO Y SCORING
    for fp in candidates:
        # A. FILTRO WHISPER (Con +1 de seguridad)
        try:
            frame_num = int(fp.stem.split("_frame_")[-1])
        except ValueError:
            continue

        # Calculate frame time. If frame_num is a raw index (> 1000), divide by fps.
        # If frame_num is sequential, multiply by the frame extraction interval.
        if frame_num > 1000:
            tiempo_frame_segundos = (frame_num / fps) + 1
        else:
            tiempo_frame_segundos = frame_num * FRAME_INTERVAL_SEC

        if tiempo_frame_segundos > filter_limit_sec:
            discarded.append({"name": fp.name, "reason": f"Whisper outro ({tiempo_frame_segundos:.1f}s > {filter_limit_sec:.1f}s)"})
            continue # ¡ELIMINADO POR WHISPER! (Es el outro)

        img = cv2.imread(str(fp))
        if img is None:
            continue

        # B. BLANK TRANSITION FILTER (Robustness fallback)
        if is_blank_transition(img):
            discarded.append({"name": fp.name, "reason": "Blank transition"})
            continue

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # C. SCORING DE PIZARRA
        # Enmascarar íconos cuadrados de negro para no confundir al detector de humanos
        sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
        contours, _ = cv2.findContours(sat_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_masked = img.copy()
        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)
            if 0.05 * min(h, w) < cw < 0.15 * min(h, w) and 0.85 < (cw / ch) < 1.15:
                cv2.rectangle(img_masked, (x, y), (x + cw, y + ch), (0, 0, 0), -1)

        # Canny (Densidad de Tiza) en la zona segura (28% al 72% del ancho)
        roi_gray = gray[int(h * 0.1):int(h * 0.9), int(w * 0.28):int(w * 0.72)]
        edges = cv2.Canny(cv2.medianBlur(roi_gray, 7), 80, 200)
        edge_density = np.sum(edges > 0) / edges.size

        # Oclusión (Piel humana) en la zona segura (from img_masked)
        skin_mask = cv2.inRange(cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV), (0, 30, 60), (25, 170, 255))
        roi_skin = skin_mask[int(h * 0.15):int(h * 0.95), int(w * 0.28):int(w * 0.72)]
        occlusion = np.sum(roi_skin > 0) / roi_skin.size

        # Fórmula: Premia la tiza, castiga fuerte al humano estorbando
        score = (edge_density * 50) - (occlusion * 5)
        
        scored_frames.append({
            "path": fp,
            "score": score,
            "edge_density": edge_density,
            "occlusion": occlusion,
        })

    # Robust Fallback in case Whisper cut was too aggressive or all frames filtered out
    if not scored_frames:
        console.print("[yellow]⚠ Todos los frames fueron eliminados. Usando fallback de último frame.[/]")
        fp = all_frames[-1]
        scored_frames.append({
            "path": fp,
            "score": 0.0,
            "edge_density": 0.0,
            "occlusion": 0.0,
        })

    scored_frames.sort(key=lambda x: x["score"], reverse=True)

    # Output selection details
    best = scored_frames[0]
    console.print(f"  [bold green]✓ Selected:[/] {best['path'].name} "
                  f"(score={best['score']:.3f}, edge_density={best['edge_density']:.3f}, occlusion={best['occlusion']:.1%})")

    # Save best_whiteboard.jpg
    pizarra_dir = frames_dir / f"{video_id}_pizarra"
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    dest = pizarra_dir / "best_whiteboard.jpg"
    
    import shutil
    shutil.copy(best["path"], dest)
    console.print(f"  [green]✓[/] Saved → {dest}")

    if debug:
        # Save JSON debug
        debug_data = {
            "video_id": video_id,
            "total_frames": total,
            "analyzed_from": start_idx,
            "discarded": discarded,
            "scores": [
                {
                    "frame": sf["path"].name,
                    "score": round(sf["score"], 4),
                    "edge_density": round(sf["edge_density"], 4),
                    "occlusion": round(sf["occlusion"], 4),
                }
                for sf in scored_frames[:20]
            ],
            "selected": best["path"].name,
        }
        debug_path = pizarra_dir / "frame_selection_debug.json"
        debug_path.write_text(json.dumps(debug_data, indent=2), encoding="utf-8")
        console.print(f"  [dim]Debug data saved → {debug_path}[/]")

    return {
        "best_frame": dest,
        "source_frame": best["path"],
        "final_score": best["score"],
        "content_score": best["edge_density"],
        "occlusion_pct": best["occlusion"] * 100,
        "discarded_count": len(discarded),
    }


# ── CLI ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Select best whiteboard frame for a video")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--debug", action="store_true", help="Save debug scoring data")
    args = parser.parse_args()

    try:
        result = select_best_frame(args.video_id, debug=args.debug)
        console.print(f"\n[bold green]🎉 Best frame:[/] {result['best_frame']}")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
