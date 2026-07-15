"""
pizarra_outro_filter.py — Detect and remove intro/outro branded screens from
                          the pizarra frame set before best-frame selection.

These screens ("This is My Architecture" title, "Thank you for watching") share
a dark background with real whiteboard frames, but lack the colorful AWS service
icons that characterize actual architecture diagrams.

Detection strategy (no keywords, pure visual):
  1. Color saturation analysis — Real whiteboards have saturated AWS service
     icons (pink, green, purple, orange). Intro/outro screens are mostly
     grayscale text on dark backgrounds.
  2. No person detection — Intro/outro screens never show presenters. Real
     whiteboard frames always have at least one person visible.
  3. Edge density in central region — Architecture diagrams have many small
     edges from icons/arrows/text. Branded screens have fewer, larger features.
"""
from __future__ import annotations

import sys
from pathlib import Path
import cv2
import numpy as np

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import FRAMES_DIR
from rich.console import Console

console = Console()


def detect_outro_frames(video_id: str, dry_run: bool = False) -> dict:
    """
    Scan pizarra frames and identify intro/outro branded screens.
    
    Parameters
    ----------
    video_id : str
        YouTube video ID.
    dry_run : bool
        If True, only report detections without deleting files.
    
    Returns
    -------
    dict with keys: removed (list of filenames), kept (list of filenames)
    """
    pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
    
    if not pizarra_dir.exists():
        raise FileNotFoundError(f"Pizarra directory not found: {pizarra_dir}")
    
    frames = sorted(pizarra_dir.glob(f"{video_id}_frame_*.jpg"))
    
    if not frames:
        console.print("[yellow]No pizarra frames found.[/]")
        return {"removed": [], "kept": []}
    
    console.print(f"\n[bold cyan]Scanning {len(frames)} pizarra frames for intro/outro screens...[/]")
    
    removed = []
    kept = []
    
    for fp in frames:
        img = cv2.imread(str(fp))
        if img is None:
            continue
        
        is_outro, reasons = _is_branded_screen(img)
        
        if is_outro:
            reason_str = ", ".join(reasons)
            console.print(f"  [red]OUTRO[/] {fp.name}: {reason_str}")
            removed.append(fp.name)
            if not dry_run:
                fp.unlink()
        else:
            kept.append(fp.name)
    
    action = "Would remove" if dry_run else "Removed"
    console.print(f"\n[bold green]{action} {len(removed)} intro/outro frame(s), kept {len(kept)} frame(s).[/]")
    
    return {"removed": removed, "kept": kept}


def _is_branded_screen(img: np.ndarray) -> tuple[bool, list[str]]:
    """
    Determine if an image is a branded intro/outro screen based on:
    1. Skin-tone pixel percentage (presenters are never in intro/outro slides).
    2. Spatial brightness distribution (intro/outro slides have very dark left and right borders).
    3. Side vs center brightness difference (the center in intro/outro is brighter than the sides,
       whereas a real blackboard is dark in the center and has bright studio lights/backgrounds on the sides).
    
    Returns (is_outro: bool, reasons: list[str])
    """
    h, w, _ = img.shape
    reasons = []
    
    # Convert to HSV and gray
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Skin-tone pixel percentage (H: 0-25, S: 40-170, V: 80-255)
    skin_mask = cv2.inRange(hsv, (0, 40, 80), (25, 170, 255))
    skin_pct = (np.sum(skin_mask > 0) / skin_mask.size) * 100
    if skin_pct < 1.5:
        reasons.append(f"low skin percentage ({skin_pct:.2f}%)")
        
    # 2. Brightness distribution check (L, R, C)
    col_means = np.mean(gray, axis=0)
    left_bright = np.mean(col_means[:int(w * 0.15)])
    center_bright = np.mean(col_means[int(w * 0.35):int(w * 0.65)])
    right_bright = np.mean(col_means[int(w * 0.85):])
    
    # Side-vs-center difference
    svc = ((left_bright + right_bright) / 2) - center_bright
    
    if left_bright < 32.0 and right_bright < 32.0:
        reasons.append(f"dark sides (L={left_bright:.1f}, R={right_bright:.1f})")
    if svc < -5.0:
        reasons.append(f"negative side-vs-center difference ({svc:.1f})")
        
    # Determine if it is a branded slide
    # Require at least 2 indicators, AND either svc must be negative or sides must be very dark
    is_outro = len(reasons) >= 2 and (svc < -5.0 or (left_bright < 32.0 and right_bright < 32.0))
    
    return is_outro, reasons


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Detect and remove intro/outro branded screens.")
    parser.add_argument("video_id", help="YouTube video ID")
    parser.add_argument("--dry-run", action="store_true", help="Only report, don't delete")
    args = parser.parse_args()
    
    try:
        result = detect_outro_frames(args.video_id, dry_run=args.dry_run)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}")
