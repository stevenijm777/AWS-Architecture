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
import shutil
import cv2
import numpy as np
from rich.console import Console

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.settings import FRAMES_DIR, RAW_DIR, FRAME_INTERVAL_SEC

console = Console()


# ── Main frame selection logic ──────────────────────────────────

def select_best_frame(
        video_id: str,
        frames_dir: Path | None = None,
        output_dir: Path | None = None,
        debug: bool = False,
        min_area_icono: int = 2000,
        write_outputs: bool = True,
) -> dict:
    """
    Select the best whiteboard frame for a video following the final algorithm:
    1. Carga (Último 80% del video).
    2. FILTRO 1: Evaluación de piel (bandera booleana para indulto).
    3. FILTRO 2: ANOMALÍAS ESTADÍSTICAS (Purger transición al outro a brillo 30).
    4. FILTRO 3: VALIDACIÓN DE ÍCONOS AWS + Filtro Diferencial (Anillo).
    5. SCORING:
       - Mask AWS service icons directly on Grayscale.
       - Calculate capped chalk density (GaussianBlur + Canny 30,100 capped at 0.015).
       - Calculate occlusion (skin mask ROI).
       - Score equilibrado con límite en el bono de piel.
    """
    frames_dir = Path(frames_dir or FRAMES_DIR)
    video_frames_dir = frames_dir / video_id

    if not video_frames_dir.exists():
        raise FileNotFoundError(f"Frames directory not found: {video_frames_dir}")

    # Get all frame files sorted by number
    all_frames = sorted(
        video_frames_dir.glob(f"{video_id}_frame_*.jpg"),
        key=lambda p: int(p.stem.split("_frame_")[-1]),
    )
    if not all_frames:
        # Fallback to general *.jpg if needed
        all_frames = sorted(
            video_frames_dir.glob("*.jpg"),
            key=lambda p: int(p.stem.split("_frame_")[-1]) if "_frame_" in p.stem else 0,
        )

    if not all_frames:
        raise FileNotFoundError(f"No frames found in {video_frames_dir}")

    total = len(all_frames)
    console.print(f"\n[bold cyan]🔍 Frame Selection for {video_id}[/] ({total} frames total)")

    # 1. Carga el 80% del video
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

        # ---------------------------------------------------------
        # FILTRO 1: EVALUACIÓN DE PIEL (Sin descarte inmediato)
        # ---------------------------------------------------------
        skin_mask = cv2.inRange(hsv, (0, 30, 60), (25, 170, 255))
        skin_pct = np.sum(skin_mask > 0) / skin_mask.size
        tiene_piel = skin_pct >= 0.014 # Guardamos la bandera para el Indulto

        # ---------------------------------------------------------
        # FILTRO 2: FILTRADO DE ANOMALÍAS (Purger transición al outro)
        # ---------------------------------------------------------
        roi_gray_anom = gray[int(h * 0.1):int(h * 0.9), int(w * 0.28):int(w * 0.72)]
        _, roi_limpio_anom = cv2.threshold(roi_gray_anom, 30, 255, cv2.THRESH_TOZERO)
        edges_anom = cv2.Canny(cv2.medianBlur(roi_limpio_anom, 7), 80, 200)
        edge_density_anom = np.sum(edges_anom > 0) / edges_anom.size

        if edge_density_anom > 0.0495:
            discarded_count += 1
            continue

        # ---------------------------------------------------------
        # FILTRO 3: VALIDACIÓN DE ÍCONOS AWS + FILTRO DIFERENCIAL
        # ---------------------------------------------------------
        # Saturación relajada para tolerar pizarras digitales/cristal
        sat_mask_raw = (hsv[:, :, 1] > 40) & (hsv[:, :, 2] > 80)

        # Mantenemos el kernel fuerte (13x13) para la tiza
        kernel_corte = np.ones((13, 13), np.uint8)
        sat_mask = cv2.morphologyEx(sat_mask_raw.astype(np.uint8), cv2.MORPH_OPEN, kernel_corte)

        contours, _ = cv2.findContours(sat_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        iconos_validos = []
        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            
            # Geometría relajada (0.70 a 1.35)
            if 0.05 * min(h, w) < cw < 0.15 * min(h, w) and 0.70 < (cw / ch) < 1.35 and area >= min_area_icono:
                
                # --- LÓGICA DEL ANILLO (Contraste Local) ---
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

                # Si hay contraste (> 40.0), es un ícono real
                if delta_contraste >= 40.0:
                    iconos_validos.append((x, y, cw, ch))

        num_iconos = len(iconos_validos)

        # ---------------------------------------------------------
        # LÓGICA DE RECHAZO COMBINADA (El Indulto)
        # ---------------------------------------------------------
        # Si NO hay piel humana, perdonamos el frame SOLO SI tiene 2+ íconos (es un plano puro de la pizarra).
        if not tiene_piel and num_iconos < 1:
            discarded_count += 1
            continue

        # Exigimos al menos 1 ícono legítimo siempre
        if num_iconos < 1:
            discarded_count += 1
            continue

        # ---------------------------------------------------------
        # SCORING (Solo verdaderas pizarras limpias)
        # ---------------------------------------------------------
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

        # --- CÁLCULO DE PESOS REBALANCEADO ---
        puntos_iconos = num_iconos * 5
        puntos_tiza = capped_density * 50
        penalizacion_oclusion = occlusion * 700
        
        # Bono de piel capeado al 10% (Máximo 5 puntos, equivalente a 1 ícono)
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

    # Robust Fallback in case all frames filtered out
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

    # Output selection details
    best = scored_frames[0]
    console.print(f"  [bold green]✓ Selected:[/] {best['path'].name} "
                  f"(score={best['score']:.3f}, edge={best['edge_density']:.3f}, occ={best['occlusion']:.1%}, bonus={best['skin_bonus']:.2f}, iconos={best.get('num_iconos', 0)})")

    # `write_outputs=False` deja la funcion en modo consulta: devuelve la eleccion sin
    # tocar el disco. Hace falta para poder RE-EVALUAR el selector sobre videos ya
    # curados sin sobrescribir `<video>_pizarra/best_whiteboard.jpg` ni volver a sembrar
    # `bad_whiteboard/`, que es la bandeja de revision manual. El default conserva el
    # comportamiento historico intacto.
    if not write_outputs:
        return {
            "best_frame": None,
            "source_frame": best["path"],
            "final_score": best["score"],
            "content_score": best["edge_density"],
            "occlusion_pct": best["occlusion"] * 100,
            "discarded_count": discarded_count,
            "skin_bonus": best["skin_bonus"],
            # Diagnostico: `num_iconos` y `usó_fallback` distinguen una eleccion con
            # evidencia real de una que sobrevivio porque no quedaba nada mejor. El
            # fallback significa que TODOS los candidatos fueron descartados y se tomo
            # el ultimo frame del video sin puntuarlo de verdad.
            "num_iconos": best.get("num_iconos", 0),
            "candidatos_analizados": len(candidates),
            "uso_fallback": len(scored_frames) == 1 and best.get("num_iconos", 0) == 0
                            and discarded_count >= len(candidates),
            "top10_frames": [{"rank": i, "source_path": sf["path"], "score": sf["score"]}
                             for i, sf in enumerate(scored_frames[:10], start=1)],
        }

    # Determine target directory
    pizarra_dir = Path(output_dir) if output_dir else video_frames_dir.parent / f"{video_id}_pizarra"
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    dest = pizarra_dir / "best_whiteboard.jpg"

    shutil.copy(best["path"], dest)
    console.print(f"  [green]✓[/] Saved best whiteboard → {dest}")

    # Run Adaptive Whiteboard Detection & Information Highlighting
    try:
        from scripts.core.adaptive_whiteboard_detector import procesar_y_resaltar_conclusiones_pizarra
        symbols_list, proc_img_path = procesar_y_resaltar_conclusiones_pizarra(dest, pizarra_dir)
        console.print(f"  [green]✓[/] Information Highlighting applied → {proc_img_path.name}")
    except Exception as e:
        console.print(f"  [yellow]⚠ Adaptive detection on frame selection skipped: {e}[/]")

    # Save Top 10 Candidate Frames
    top10_dir = pizarra_dir / "top10"
    if top10_dir.exists():
        shutil.rmtree(top10_dir)
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
    console.print(f"  [green]✓[/] Top 10 frames saved → {top10_dir}")

    # Copy to bad_whiteboard for manual review
    bad_wb_dir = video_frames_dir.parent.parent / "bad_whiteboard"
    if bad_wb_dir.exists():
        bad_wb_dest = bad_wb_dir / f"{video_id}.jpg"
        shutil.copy(best["path"], bad_wb_dest)
        console.print(f"  [green]✓[/] Copied to bad_whiteboard → {bad_wb_dest}")

    if debug:
        # Save JSON debug
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
