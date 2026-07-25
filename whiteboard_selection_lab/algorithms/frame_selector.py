#!/usr/bin/env python3
"""
frame_selector.py — Intelligent frame selection for architecture whiteboard extraction.

Selects the best frame to send to Gemini by:
1. Discarding credit screens / end slides (dark + text patterns)
2. Detecting frames with colorful AWS service icons (saturated square regions)
3. Scoring occlusion (presenter blocking the whiteboard)
4. Preferring later frames (where the diagram is most complete)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
import shutil
import cv2
import numpy as np
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import FRAMES_DIR, RAW_DIR, FRAME_INTERVAL_SEC

console = Console()

# ── Credit/Outro detection ──────────────────────────────────────

OUTRO_KEYWORDS = [
    "thank you", "for watching", "for more information",
    "this-is-my-architecture", "aws.amazon.com",
    "gracias", "merci",
]


def compute_sat_pixel_pct(img: np.ndarray) -> float:
    """
    Compute the percentage of highly-saturated, bright pixels in a frame.
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    return np.sum(sat_mask) / (img.shape[0] * img.shape[1])


def is_credit_screen(img: np.ndarray) -> bool:
    """Detect credit/end screens."""
    h, w = img.shape[:2]
    total_px = h * w
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    sat_pct = compute_sat_pixel_pct(img)

    if np.std(gray) < 20 and np.mean(gray) < 60:
        return True

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
    """Score a frame by how many colorful, saturated rectangular regions it has."""
    h, w = img.shape[:2]
    total_px = h * w
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    sat_pct = np.sum(sat_mask) / total_px

    sat_uint8 = sat_mask.astype(np.uint8) * 255
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened = cv2.morphologyEx(sat_uint8, cv2.MORPH_OPEN, kernel_open)
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)

    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    icon_count = 0
    icon_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, cw, ch = cv2.boundingRect(cnt)

        min_side = min(h, w) * 0.02
        max_side = min(h, w) * 0.25
        if cw < min_side or ch < min_side:
            continue
        if cw > max_side or ch > max_side:
            continue

        aspect = cw / ch if ch > 0 else 0
        if 0.3 < aspect < 3.0:
            icon_count += 1
            icon_area += area

    icon_score = min(icon_count / 10.0, 1.0)
    area_score = min(sat_pct * 20, 1.0)

    return 0.6 * icon_score + 0.4 * area_score


def score_whiteboard_content(img: np.ndarray) -> float:
    """Score how much whiteboard content a frame has."""
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    roi_x1, roi_x2 = int(w * 0.15), int(w * 0.85)
    roi_y1, roi_y2 = int(h * 0.10), int(h * 0.90)
    roi = gray[roi_y1:roi_y2, roi_x1:roi_x2]

    edges = cv2.Canny(roi, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size

    color_score = score_colorful_regions(img)

    return 0.7 * color_score + 0.3 * min(edge_density * 10, 1.0)


# ── Occlusion estimation ───────────────────────────────────────

def mask_service_icons(img: np.ndarray) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    """Detect highly saturated, square-like regions (AWS service icons)."""
    masked_img = img.copy()
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
    sat_uint8 = sat_mask.astype(np.uint8) * 255
    
    kernel_open = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opened = cv2.morphologyEx(sat_uint8, cv2.MORPH_OPEN, kernel_open)
    
    kernel_close = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close)
    
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    detected_icons = []
    for cnt in contours:
        x, y, cw, ch = cv2.boundingRect(cnt)
        
        min_side = min(h, w) * 0.015
        max_side = min(h, w) * 0.25
        
        if cw < min_side or ch < min_side:
            continue
        if cw > max_side or ch > max_side:
            continue
            
        aspect = cw / ch if ch > 0 else 0
        if 0.6 < aspect < 1.6:
            masked_img[y:y+ch, x:x+cw] = 0
            detected_icons.append((x, y, cw, ch))
            
    return masked_img, detected_icons


def estimate_occlusion_fast(img: np.ndarray, debug_save_path: Path | str | None = None) -> float:
    """Fast occlusion estimation using skin-color detection + vertical column analysis."""
    img_masked, detected_icons = mask_service_icons(img)
    
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)

    roi_x1, roi_x2 = int(w * 0.10), int(w * 0.90)
    roi_y1 = int(h * 0.15)
    roi_y2 = int(h * 0.95)
    roi_hsv = hsv[roi_y1:roi_y2, roi_x1:roi_x2]
    roi_gray = cv2.cvtColor(img_masked[roi_y1:roi_y2, roi_x1:roi_x2], cv2.COLOR_BGR2GRAY)

    roi_w = roi_x2 - roi_x1

    lower_skin = np.array([0, 30, 60], dtype=np.uint8)
    upper_skin = np.array([25, 170, 255], dtype=np.uint8)
    skin_mask = cv2.inRange(roi_hsv, lower_skin, upper_skin)

    col_skin_pct = np.mean(skin_mask > 0, axis=0)
    col_bright = np.mean(roi_gray, axis=0)
    dark_threshold = np.percentile(col_bright, 25)
    bright_cols = col_bright > (dark_threshold + 40)

    occluded_cols = (col_skin_pct > 0.12) | (bright_cols & (col_skin_pct > 0.03))

    occluded_uint8 = occluded_cols.astype(np.uint8)
    kernel = np.ones(int(roi_w * 0.05), dtype=np.uint8)
    occluded_closed = cv2.morphologyEx(occluded_uint8, cv2.MORPH_CLOSE, kernel)

    occlusion_pct = np.sum(occluded_closed > 0) / len(occluded_closed) * 100
    
    if debug_save_path is not None:
        debug_img = img.copy()
        
        for (ix, iy, iw, ih) in detected_icons:
            cv2.rectangle(debug_img, (ix, iy), (ix + iw, iy + ih), (0, 255, 0), 2)
            cv2.putText(debug_img, "Service", (ix, iy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
        overlay = debug_img.copy()
        for x_idx in range(roi_w):
            if occluded_closed[x_idx] > 0:
                abs_x = roi_x1 + x_idx
                cv2.line(overlay, (abs_x, roi_y1), (abs_x, roi_y2), (0, 0, 255), 1)
        
        cv2.addWeighted(overlay, 0.4, debug_img, 0.6, 0, debug_img)
        cv2.rectangle(debug_img, (roi_x1, roi_y1), (roi_x2, roi_y2), (0, 255, 255), 2)
        
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
        min_area_icono: int = 2000,
) -> dict:
    """
    Select the best whiteboard frame for a video.
    """
    frames_dir = Path(frames_dir or FRAMES_DIR)
    video_frames_dir = frames_dir / video_id

    if not video_frames_dir.exists():
        raise FileNotFoundError(f"Frames directory not found: {video_frames_dir}")

    all_frames = sorted(
        video_frames_dir.glob(f"{video_id}_frame_*.jpg"),
        key=lambda p: int(p.stem.split("_frame_")[-1]),
    )
    if not all_frames:
        all_frames = sorted(
            video_frames_dir.glob("*.jpg"),
            key=lambda p: int(p.stem.split("_frame_")[-1]) if "_frame_" in p.stem else 0,
        )

    if not all_frames:
        raise FileNotFoundError(f"No frames found in {video_frames_dir}")

    total = len(all_frames)
    console.print(f"\n[bold cyan]🔍 Frame Selection for {video_id}[/] ({total} frames total)")

    start_idx = int(total * 0.2)  
    candidates = all_frames[start_idx:]
    console.print(f"🚀 Procesando {len(candidates)} frames (Último 80% del video)...")

    scored_frames = []
    discarded_count = 0

    for fp in candidates:
        img = cv2.imread(str(fp))
        if img is None:
            continue

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        skin_mask = cv2.inRange(hsv, (0, 30, 60), (25, 170, 255))
        skin_pct = np.sum(skin_mask > 0) / skin_mask.size
        tiene_piel = skin_pct >= 0.014

        roi_gray_anom = gray[int(h * 0.1):int(h * 0.9), int(w * 0.28):int(w * 0.72)]
        _, roi_limpio_anom = cv2.threshold(roi_gray_anom, 30, 255, cv2.THRESH_TOZERO)
        edges_anom = cv2.Canny(cv2.medianBlur(roi_limpio_anom, 7), 80, 200)
        edge_density_anom = np.sum(edges_anom > 0) / edges_anom.size

        if edge_density_anom > 0.0495:
            discarded_count += 1
            continue

        sat_mask_raw = (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 80)
        kernel_corte = np.ones((13, 13), np.uint8)
        sat_mask = cv2.morphologyEx(sat_mask_raw.astype(np.uint8), cv2.MORPH_OPEN, kernel_corte)

        contours, _ = cv2.findContours(sat_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        iconos_validos = []
        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            
            if 0.05 * min(h, w) < cw < 0.15 * min(h, w) and 0.70 < (cw / ch) < 1.35 and area >= min_area_icono:
                margen = 20
                x_out = max(0, x - margen)
                y_out = max(0, y - margen)
                w_out = min(w - x_out, cw + (margen * 2))
                h_out = min(h - y_out, ch + (margen * 2))

                mask_anillo = np.zeros((h, w), dtype=np.uint8)
                cv2.rectangle(mask_anillo, (x_out, y_out), (x_out+w_out, y_out+h_out), 255, -1)
                cv2.rectangle(mask_anillo, (x, y), (x+cw, y+ch), 0, -1)

                brillo_icono = np.mean(gray[y:y+ch, x:x+cw])
                brillo_anillo = cv2.mean(gray, mask=mask_anillo)[0]

                delta_contraste = abs(brillo_icono - brillo_anillo)

                if delta_contraste >= 40.0:
                    iconos_validos.append((x, y, cw, ch))

        num_iconos = len(iconos_validos)

        if not tiene_piel and num_iconos < 1:
            discarded_count += 1
            continue

        if num_iconos < 1:
            discarded_count += 1
            continue

        gray_masked = gray.copy()
        for (x, y, cw, ch) in iconos_validos:
            cv2.rectangle(gray_masked, (x, y), (x + cw, y + ch), (0, 0, 0), -1)

        roi_gray = gray_masked[int(h * 0.1):int(h * 0.9), int(w * 0.28):int(w * 0.72)]
        roi_blur = cv2.GaussianBlur(roi_gray, (3, 3), 0)
        edges = cv2.Canny(roi_blur, 30, 100)
        edge_density = np.sum(edges > 0) / edges.size

        capped_density = min(edge_density, 0.015)

        roi_skin = skin_mask[int(h * 0.15):int(h * 0.95), int(w * 0.28):int(w * 0.72)]
        occlusion = np.sum(roi_skin > 0) / roi_skin.size

        puntos_iconos = num_iconos * 5
        puntos_tiza = capped_density * 50
        penalizacion_oclusion = occlusion * 300
        bono_piel = min(skin_pct, 0.10) * 50 

        score = puntos_iconos + puntos_tiza - penalizacion_oclusion + bono_piel

        scored_frames.append({
            "path": fp,
            "score": score,
            "edge_density": edge_density,
            "capped_density": capped_density,
            "occlusion": occlusion,
            "skin_bonus": bono_piel,
            "num_iconos": num_iconos
        })

    if not scored_frames:
        console.print("[yellow]⚠ Todos los frames fueron eliminados. Usando fallback de último frame.[/]")
        fp = all_frames[-1]
        img = cv2.imread(str(fp))
        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi_gray = gray[int(h * 0.1):int(h * 0.9), int(w * 0.28):int(w * 0.72)]
        roi_blur = cv2.GaussianBlur(roi_gray, (3, 3), 0)
        edges = cv2.Canny(roi_blur, 30, 100)
        edge_density = np.sum(edges > 0) / edges.size
        capped_density = min(edge_density, 0.015)
        score = (capped_density * 50)
        scored_frames.append({
            "path": fp,
            "score": score,
            "edge_density": edge_density,
            "capped_density": capped_density,
            "occlusion": 0.0,
            "skin_bonus": 0.0,
            "num_iconos": 0
        })

    scored_frames.sort(key=lambda x: x["score"], reverse=True)

    best = scored_frames[0]
    console.print(f"  [bold green]✓ Selected:[/] {best['path'].name} "
                  f"(score={best['score']:.3f}, edge={best['edge_density']:.3f}, occ={best['occlusion']:.1%}, bonus={best['skin_bonus']:.2f}, iconos={best.get('num_iconos', 0)})")

    pizarra_dir = video_frames_dir.parent / f"{video_id}_pizarra"
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    dest = pizarra_dir / "best_whiteboard.jpg"
    shutil.copy(best["path"], dest)
    console.print(f"  [green]✓[/] Saved → {dest}")

    top10_dir = pizarra_dir / "top10"
    top10_dir.mkdir(parents=True, exist_ok=True)

    top10_info = []
    for rank, sf in enumerate(scored_frames[:10], start=1):
        top10_dest = top10_dir / f"rank_{rank:02d}_{sf['path'].name}"
        shutil.copy(sf["path"], top10_dest)
        top10_info.append({
            "rank": rank,
            "path": top10_dest,
            "source_path": sf["path"],
            "score": sf["score"]
        })
    console.print(f"  [green]✓[/] Top 10 frames guardados en → {top10_dir}")

    bad_wb_dir = video_frames_dir.parent.parent / "bad_whiteboard"
    if bad_wb_dir.exists():
        bad_wb_dest = bad_wb_dir / f"{video_id}.jpg"
        shutil.copy(best["path"], bad_wb_dest)
        console.print(f"  [green]✓[/] Copied to bad_whiteboard → {bad_wb_dest}")

    if debug:
        debug_data = {
            "video_id": video_id,
            "total_frames": total,
            "analyzed_from": start_idx,
            "scores": [
                {
                    "frame": sf["path"].name,
                    "score": round(sf["score"], 4),
                    "edge_density": round(sf["edge_density"], 4),
                    "capped_density": round(sf.get("capped_density", 0.0), 4),
                    "occlusion": round(sf["occlusion"], 4),
                    "skin_bonus": round(sf["skin_bonus"], 4),
                    "num_iconos": sf.get("num_iconos", 0)
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
        "discarded_count": discarded_count,
        "skin_bonus": best["skin_bonus"],
        "top10_frames": top10_info
    }

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
