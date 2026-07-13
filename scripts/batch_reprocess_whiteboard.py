#!/usr/bin/env python3
import cv2
import numpy as np
import shutil
from pathlib import Path

# Configuración
PROJECT_ROOT = Path('/home/stemjara/Projects/AWS-Architecture')
DATA_DIR = PROJECT_ROOT / 'data'
FRAMES_BASE_DIR = DATA_DIR / 'frames'
BAD_WB_DIR = DATA_DIR / 'bad_whiteboard'
GOOD_WB_DIR = DATA_DIR / 'good_whiteboard'

VIDEO_IDS = [
    "1ZLiRT0C2Yo", "2f_NYiPJQt4", "4WjXH8Wp0E4", "6sY0AunanlM", "9-a9Y5THTYo",
    "9qTEHITVeLE", "37T7Nd8pL-c", "53sUjFv9ByI", "90rWUjKjnAE", "A4Lfk1Zz1dE",
    "AzM_d7ZvzUE", "BX1K8x1lVLc", "CTG23wd9H74", "Cw26CrJUqv8", "E8BGpIxzYc4",
    "eFQNwelGLhA", "FfSNnH2bbNc", "GxjMSvwcgvw", "hrhBOOrR5v0", "JSBB-BCvavQ",
    "JVcKidzqpYY", "k8nhRJTQ15I", "KgRib8AM0fs", "Kp51k6LY-2c", "PBa68gCG0Uk",
    "QJZHs1CSxu0"
]

def clean_old_data(video_id):
    """
    Deletes previously selected/copied files for a video ID.
    """
    print(f"🧹 Limpiando datos antiguos para {video_id}...")
    
    # 1. Delete bad_whiteboard entry
    bad_wb_file = BAD_WB_DIR / f"{video_id}.jpg"
    if bad_wb_file.exists():
        bad_wb_file.unlink()
        print(f"  - Eliminado: {bad_wb_file.relative_to(PROJECT_ROOT)}")

    # 2. Delete good_whiteboard entry (just in case)
    good_wb_file = GOOD_WB_DIR / f"{video_id}.jpg"
    if good_wb_file.exists():
        good_wb_file.unlink()
        print(f"  - Eliminado: {good_wb_file.relative_to(PROJECT_ROOT)}")

    # 3. Delete _pizarra folder
    pizarra_dir = FRAMES_BASE_DIR / f"{video_id}_pizarra"
    if pizarra_dir.exists():
        shutil.rmtree(pizarra_dir)
        print(f"  - Eliminado directorio: {pizarra_dir.relative_to(PROJECT_ROOT)}")

    # 4. Delete _FINAL_SELECTION folder
    final_sel_dir = FRAMES_BASE_DIR / f"{video_id}_FINAL_SELECTION"
    if final_sel_dir.exists():
        shutil.rmtree(final_sel_dir)
        print(f"  - Eliminado directorio: {final_sel_dir.relative_to(PROJECT_ROOT)}")

def process_video(video_id):
    frames_dir = FRAMES_BASE_DIR / video_id
    if not frames_dir.exists():
        print(f"⚠️ Directorio de frames no existe: {frames_dir}. Saltando...")
        return False

    output_dir = FRAMES_BASE_DIR / f"{video_id}_FINAL_SELECTION"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Carga (Solo el último 40% del video)
    all_frames = sorted(frames_dir.glob("*.jpg"), key=lambda p: int(p.stem.split("_frame_")[-1]))
    if not all_frames:
        print(f"⚠️ No se encontraron frames *.jpg en {frames_dir}. Saltando...")
        return False

    start_idx = int(len(all_frames) * 0.6) # Empezar en el 60%, analizar hasta el final
    candidates = all_frames[start_idx:]

    scored_frames = []
    print(f"🚀 Procesando {len(candidates)} frames para {video_id} (Último 40% del video)...")

    for fp in candidates:
        img = cv2.imread(str(fp))
        if img is None:
            continue

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # ---------------------------------------------------------
        # FILTRO 1: ELIMINACIÓN DE PANTALLAS CLARAS
        # ---------------------------------------------------------
        dark_px_pct = np.sum(gray < 45) / (h * w)
        if dark_px_pct < 0.20:
            continue # ¡ELIMINADO! Ni siquiera lo guardamos.

        # ---------------------------------------------------------
        # FILTRO 2: ELIMINACIÓN DE OUTROS / LOGOS (Falta de piel)
        # ---------------------------------------------------------
        skin_mask = cv2.inRange(hsv, (0, 30, 60), (25, 170, 255))
        skin_pct = np.sum(skin_mask > 0) / skin_mask.size

        # Si no hay ni un 1.5% de piel humana, es un logo o texto 100% seguro.
        if skin_pct < 0.015:
            continue # ¡ELIMINADO!

        # ---------------------------------------------------------
        # SCORING (Solo llegan las verdaderas pizarras con humanos)
        # ---------------------------------------------------------
        # 1. Pintar íconos cuadrados de negro
        sat_mask = (hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 60)
        contours, _ = cv2.findContours(sat_mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img_masked = img.copy()
        for cnt in contours:
            x, y, cw, ch = cv2.boundingRect(cnt)
            if 0.05*min(h,w) < cw < 0.15*min(h,w) and 0.85 < (cw/ch) < 1.15:
                cv2.rectangle(img_masked, (x, y), (x+cw, y+ch), (0,0,0), -1)

        # 2. Densidad de Tiza (Centro)
        roi_gray = gray[int(h*0.1):int(h*0.9), int(w*0.28):int(w*0.72)]
        edges = cv2.Canny(cv2.medianBlur(roi_gray, 7), 80, 200)
        edge_density = np.sum(edges > 0) / edges.size

        # 3. Penalización por Oclusión (Centro) - ¡BUG ARREGLADO!
        roi_skin = skin_mask[int(h*0.15):int(h*0.95), int(w*0.28):int(w*0.72)]
        # Ahora da un porcentaje real de 0.0 a 1.0 (en lugar de sumar 255s)
        occlusion = np.sum(roi_skin > 0) / roi_skin.size

        # Cálculo final
        score = (edge_density * 50) - (occlusion * 5)
        scored_frames.append({"path": fp, "score": score})

    # 3. Selección Final
    if not scored_frames:
        print(f"⚠️ Todos los frames fueron eliminados para {video_id}. Ninguno cumplió los requisitos.")
        return False

    scored_frames.sort(key=lambda x: x['score'], reverse=True)

    # Copiar Top 10 seleccionados
    print(f"✅ Top 10 seleccionados de las pizarras sobrevivientes para {video_id}:")
    for i, item in enumerate(scored_frames[:10]):
        rank = i + 1
        shutil.copy(item['path'], output_dir / f"Rank{rank}_{item['path'].name}")
        print(f"  Rank {rank}: {item['path'].name} (Score: {item['score']:.4f})")

    # Copiar Rank 1 a bad_whiteboard
    best_frame_path = scored_frames[0]['path']
    bad_wb_dest = BAD_WB_DIR / f"{video_id}.jpg"
    BAD_WB_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(best_frame_path, bad_wb_dest)
    print(f"📌 Rank 1 copiado a: {bad_wb_dest.relative_to(PROJECT_ROOT)}")

    # Copiar Rank 1 a _pizarra/best_whiteboard.jpg
    pizarra_dir = FRAMES_BASE_DIR / f"{video_id}_pizarra"
    pizarra_dir.mkdir(parents=True, exist_ok=True)
    pizarra_dest = pizarra_dir / "best_whiteboard.jpg"
    shutil.copy(best_frame_path, pizarra_dest)
    print(f"📌 Rank 1 copiado a: {pizarra_dest.relative_to(PROJECT_ROOT)}")

    return True

def main():
    print(f"🚀 Iniciando procesamiento por lotes para {len(VIDEO_IDS)} videos...")
    success_count = 0
    failed_count = 0

    for idx, vid in enumerate(VIDEO_IDS):
        print(f"\n==================================================")
        print(f"[{idx+1}/{len(VIDEO_IDS)}] Procesando Video: {vid}")
        print(f"==================================================")
        
        try:
            clean_old_data(vid)
            success = process_video(vid)
            if success:
                success_count += 1
                print(f"🎉 Éxito procesando {vid}")
            else:
                failed_count += 1
                print(f"❌ Fallo al procesar {vid}")
        except Exception as e:
            failed_count += 1
            print(f"💥 Error inesperado al procesar {vid}: {e}")

    print(f"\n==================================================")
    print(f"Resumen de Procesamiento:")
    print(f"  - Total procesados con éxito: {success_count}")
    print(f"  - Total fallidos: {failed_count}")
    print(f"==================================================")

if __name__ == "__main__":
    main()
