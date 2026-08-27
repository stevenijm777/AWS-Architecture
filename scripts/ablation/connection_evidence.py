#!/usr/bin/env python3
"""
connection_evidence.py — Recover the connection evidence the detector throws away.

The whiteboard detector already computes two things: the icon boxes *and* a mask of
the connection strokes between them. Only the first survives:
`format_symbols_for_prompt` injects icon positions as text (into Stage 1 only), and
the stroke mask is merely painted yellow onto a debug image. The topology — which
icon links to which — never reaches Stage 2 in any usable form, even though Edge F1
is the pipeline's weakest metric.

Measured on the 30-video panel, that metric's deficit is a *pairing* problem, not a
direction problem: ignoring edge direction entirely lifts Edge F1 only ~2.6 points
(58.99 → 61.60), so ~38% of pairs are simply wrong or missing. This module targets
that.

Two design choices worth keeping:

  * **Numbered badges, not coordinates.** Gemini's spatial convention is normalised
    0-1000, not source pixels, and the image is rescaled internally — raw pixel
    coordinates are not a reference the model can be trusted to resolve. Instead each
    icon gets a badge drawn *on* the image and the text refers to badge numbers, so
    no spatial reasoning is required to link text to picture.
  * **No `AWS_Icon_N [C:… W:…]` stamps.** Those are what bury the handwritten service
    names in the detector's own debug render, and they duplicate numbers already sent
    as text. Badges go in the box's top-left corner; the handwritten labels sit below
    the icons, so they stay readable.

The detector is noisy — it has boxed a presenter's hand — so pairs are evidence to
corroborate, never facts, and the prompt block says so explicitly.

Usage
-----
    .venv/bin/python scripts/ablation/connection_evidence.py --videos _pXybA6832o
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "whiteboard_selection_lab"))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from rich.console import Console  # noqa: E402

from algorithms.adaptive_whiteboard_detector import (  # noqa: E402
    procesar_y_resaltar_conclusiones_pizarra,
)

console = Console()

GOOD_WB = PROJECT_ROOT / "data" / "good_whiteboard"
OUT_DIR = PROJECT_ROOT / "reports" / "connection_evidence"

MIN_SUPPORT = 3          # threshold where pair counts started matching GT edge counts
MAX_SNAP = 180           # px an endpoint may sit from an icon centre and still count
# 40 px silently dropped the short arrows between vertically adjacent icons (the gap
# between two stacked boxes is barely longer than that). 25 recovers them; going down
# to 15 changes nothing further, so the recovered strokes are real, not noise.
MIN_SEG_LEN = 25


def assign_badges(symbols: list[dict]) -> list[dict]:
    """Number icons in reading order so the badges are predictable to a human reader."""
    row_h = np.median([s["box"][3] for s in symbols]) if symbols else 1
    ordered = sorted(symbols, key=lambda s: (round(s["center"][1] / max(row_h, 1)),
                                             s["center"][0]))
    for i, s in enumerate(ordered, 1):
        s["badge"] = i
    return ordered


def stroke_mask(img: np.ndarray, symbols: list[dict]) -> np.ndarray:
    """Edges that are not part of an icon — i.e. the strokes drawn between icons."""
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Slack is measured in icon widths, not as a fraction of the diagram's span: the
    # drawing area hugs the icons, and a span-proportional margin grows until it
    # swallows whoever is standing beside the board.
    mask = np.zeros((h, w), np.uint8)
    if symbols:
        xs = [s["box"][0] for s in symbols] + [s["box"][0] + s["box"][2] for s in symbols]
        ys = [s["box"][1] for s in symbols] + [s["box"][1] + s["box"][3] for s in symbols]
        pad = int(0.6 * np.median([s["box"][2] for s in symbols]))
        mask[max(0, min(ys) - pad):min(h, max(ys) + pad),
             max(0, min(xs) - pad):min(w, max(xs) + pad)] = 255
    else:
        mask[:] = 255

    margin = 10
    for s in symbols:
        x, y, bw, bh = s["box"]
        mask[max(0, y - margin):min(h, y + bh + margin),
             max(0, x - margin):min(w, x + bw + margin)] = 0

    edges = cv2.Canny(cv2.GaussianBlur(gray, (3, 3), 0), 30, 100)
    edges = cv2.bitwise_and(edges, edges, mask=mask)
    return cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)


def candidate_pairs(symbols: list[dict], mask: np.ndarray) -> list[dict]:
    """Line segments snapped to icons → candidate links between badge numbers.

    A segment counts only if *both* endpoints land near a different icon, so strokes
    trailing into handwriting or a presenter's arm drop out on their own. `support`
    is how many segments back a pair: a real arrow usually fragments into several
    collinear pieces, a spurious link rarely repeats.
    """
    segs = cv2.HoughLinesP(mask, 1, np.pi / 180, threshold=30,
                           minLineLength=MIN_SEG_LEN, maxLineGap=12)
    if segs is None:
        return []

    centres = [s["center"] for s in symbols]

    def nearest(px, py):
        best, bd = None, float("inf")
        for i, (cx, cy) in enumerate(centres):
            d = float(np.hypot(px - cx, py - cy))
            if d < bd:
                best, bd = i, d
        return best if bd <= MAX_SNAP else None

    tally: dict[tuple[int, int], int] = {}
    for x1, y1, x2, y2 in segs[:, 0]:
        a, b = nearest(x1, y1), nearest(x2, y2)
        if a is None or b is None or a == b:
            continue
        tally[(min(a, b), max(a, b))] = tally.get((min(a, b), max(a, b)), 0) + 1

    pairs = [{"a_badge": symbols[i]["badge"], "b_badge": symbols[j]["badge"],
              "a_center": symbols[i]["center"], "b_center": symbols[j]["center"],
              "support": n}
             for (i, j), n in tally.items()]
    pairs.sort(key=lambda p: -p["support"])
    return pairs


def render_overlay(img: np.ndarray, symbols: list[dict], mask: np.ndarray) -> np.ndarray:
    """Strokes highlighted, icons boxed, each icon badged with its number.

    The badge sits in the box's top-left corner because the handwritten service name
    is written *below* the icon on these whiteboards — putting it there is what keeps
    the name legible, which the detector's own stamped render does not.
    """
    out = img.copy()
    out[mask > 0] = (0, 255, 255)
    for s in symbols:
        x, y, bw, bh = s["box"]
        cv2.rectangle(out, (x, y), (x + bw, y + bh), (255, 0, 255), 2)

        r = max(14, int(0.16 * bw))
        cx, cy = x + r, y + r
        cv2.circle(out, (cx, cy), r, (255, 0, 255), -1)
        cv2.circle(out, (cx, cy), r, (255, 255, 255), 2)
        txt = str(s["badge"])
        scale = 0.9 * r / 16
        (tw, th), _ = cv2.getTextSize(txt, cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
        cv2.putText(out, txt, (cx - tw // 2, cy + th // 2),
                    cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 2, cv2.LINE_AA)
    return out


def format_pairs_for_prompt(pairs: list[dict], min_support: int = MIN_SUPPORT) -> str:
    """Prompt block. Framed as corroborable evidence — the detector has false positives."""
    kept = [p for p in pairs if p["support"] >= min_support]
    if not kept:
        return ""
    lines = [
        "\n## CANDIDATE VISUAL CONNECTIONS (AUTOMATIC STROKE DETECTION):",
        "A second copy of the whiteboard is provided in which every detected service "
        "icon is outlined and marked with a numbered badge, and the strokes drawn "
        "between icons are highlighted. Computer vision traced those strokes and "
        "produced the candidate links below, written as badge numbers. `support` counts "
        "how many line segments back a link; higher means the stroke was longer or more "
        "clearly drawn.",
        "",
        "IMPORTANT — this detector is imprecise. It CANNOT tell arrow direction, it can "
        "join two icons that merely have a line passing between them, and it sometimes "
        "traces handwriting or a presenter's arm. Treat every entry as a HINT TO VERIFY, "
        "never as fact. Use a link only when the transcript or the image itself supports "
        "it, and do NOT create an edge purely because it is listed here. Decide direction "
        "yourself from the arrowheads and the transcript. Connections that are described "
        "in the audio but never drawn will not appear here at all — keep emitting those.",
        "",
    ]
    for p in kept:
        lines.append(f"- badge {p['a_badge']} <-> badge {p['b_badge']}   support={p['support']}")
    return "\n".join(lines)


def build_evidence(video_id: str, whiteboard: Path, workdir: Path) -> dict:
    """Entry point for the runner: returns overlay path, prompt block and raw pairs."""
    workdir.mkdir(parents=True, exist_ok=True)
    symbols, _ = procesar_y_resaltar_conclusiones_pizarra(whiteboard, workdir,
                                                          delta_contraste_min=40.0)
    symbols = assign_badges(symbols)
    img = cv2.imread(str(whiteboard))
    mask = stroke_mask(img, symbols)
    pairs = candidate_pairs(symbols, mask)

    overlay = workdir / f"{video_id}_overlay_badged.jpg"
    cv2.imwrite(str(overlay), render_overlay(img, symbols, mask))

    return {
        "video_id": video_id,
        "overlay_path": overlay,
        "prompt_block": format_pairs_for_prompt(pairs),
        "n_symbols": len(symbols),
        "pairs": pairs,
        "pairs_kept": [p for p in pairs if p["support"] >= MIN_SUPPORT],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Extrae conexiones candidatas del detector")
    ap.add_argument("--videos", nargs="+", required=True)
    args = ap.parse_args()

    for vid in args.videos:
        wb = GOOD_WB / f"{vid}.jpg"
        if not wb.exists():
            console.print(f"[red]✗ {vid}: sin pizarra[/]")
            continue
        ev = build_evidence(vid, wb, OUT_DIR / vid)
        (OUT_DIR / vid / "pairs.json").write_text(json.dumps(
            {"video_id": vid, "n_symbols": ev["n_symbols"], "pairs": ev["pairs"]},
            indent=2, ensure_ascii=False), encoding="utf-8")
        (OUT_DIR / vid / "prompt_block.txt").write_text(ev["prompt_block"], encoding="utf-8")
        console.print(f"[green]✓[/] {vid}: {ev['n_symbols']} íconos · "
                      f"{len(ev['pairs_kept'])} pares (support>={MIN_SUPPORT})")


if __name__ == "__main__":
    main()
