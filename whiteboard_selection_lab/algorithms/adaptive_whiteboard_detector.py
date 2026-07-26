#!/usr/bin/env python3
"""
adaptive_whiteboard_detector.py — Detección Adaptativa de Pizarra (Estudio Clásico vs. Pizarra Digital)

Detecta de forma adaptativa el tipo de pizarra y extrae:
1. Tipo de entorno (Estudio Clásico con franja negra vs Pizarra Digital/Fullscreen)
2. Símbolos AWS (íconos de color + blancos/brillantes) con bounding boxes y centroides
3. Líneas de conexión entre íconos

Implementación al pie de la letra del algoritmo de detección del notebook.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from rich.console import Console

console = Console()


def procesar_y_resaltar_conclusiones_pizarra(
    ruta_imagen_input: Path,
    lab_workspace_dir: Path,
    delta_contraste_min: float = 40.0,
) -> tuple[list[dict[str, Any]], Path]:
    """
    Detecta de forma adaptativa el tipo de pizarra:
    - Si es Estudio Clásico: Encuadra la franja central negra.
    - Si es Pizarra Digital / Fullscreen: Asigna un ROI ancho de pantalla completa.

    Parameters
    ----------
    ruta_imagen_input : Path
        Ruta a la imagen de la pizarra (best_whiteboard.jpg).
    lab_workspace_dir : Path
        Directorio donde guardar los outputs (imagen procesada).
    delta_contraste_min : float
        Umbral mínimo de contraste local (anillo) para validar un ícono.

    Returns
    -------
    tuple[list[dict], Path]
        - Lista de símbolos detectados (cada uno con box, center, etc.)
        - Ruta a la imagen procesada con conexiones resaltadas.
    """
    ruta_img = Path(ruta_imagen_input)
    if not ruta_img.exists():
        raise FileNotFoundError(f"La imagen especificada no existe en: {ruta_img}")

    lab_workspace_dir.mkdir(parents=True, exist_ok=True)

    # Carga de la imagen en color, gris y HSV
    img = cv2.imread(str(ruta_img))
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # --------------------------------------------------------------------------
    # 0. DETECCIÓN ADAPTATIVA DEL ESPACIO DE TRABAJO (ROI)
    # --------------------------------------------------------------------------
    skin_mask = cv2.inRange(hsv, (0, 20, 50), (25, 180, 255))
    blue_bg_mask = cv2.inRange(hsv, (95, 40, 40), (130, 255, 255))
    exclusion_mask = cv2.bitwise_or(skin_mask, blue_bg_mask)

    # Evaluación de negro puro (V < 40) en el centro para identificar Estudio Clásico
    pure_black_pixels = (hsv[:, :, 2] < 40) & (exclusion_mask == 0)
    col_counts = np.sum(pure_black_pixels, axis=0)

    center_x = w // 2
    threshold_pixels = int(h * 0.30)

    # Probar si el centro corresponde a un panel negro físico de estudio
    is_classic_studio = False
    x_left = 0
    x_right = w

    if col_counts[center_x] >= threshold_pixels:
        x_left_temp = center_x
        while x_left_temp > 0 and col_counts[x_left_temp] >= threshold_pixels:
            x_left_temp -= 1

        x_right_temp = center_x
        while x_right_temp < w - 1 and col_counts[x_right_temp] >= threshold_pixels:
            x_right_temp += 1

        board_width = x_right_temp - x_left_temp
        # Si la franja negra tiene un ancho físico razonable (25% a 75% del frame)
        if 0.25 * w <= board_width <= 0.75 * w:
            is_classic_studio = True
            x_left = max(0, x_left_temp - 5)
            x_right = min(w, x_right_temp + 5)

    # Asignación del espacio según el tipo detectado
    if is_classic_studio:
        console.print(f"  🎯 Entorno: ESTUDIO CLÁSICO → Franja negra encuadrada: [X:{x_left} a {x_right}]")
    else:
        # Pizarra Digital / Cristal / Fullscreen → Usar el 96% del área central de la pantalla
        x_left = int(w * 0.02)
        x_right = int(w * 0.98)
        console.print(f"  🖥️ Entorno: PIZARRA DIGITAL / FULLSCREEN → Espacio ancho asignado: [X:{x_left} a {x_right}]")

    board_mask = np.zeros((h, w), dtype=np.uint8)
    board_mask[:, x_left:x_right] = 255
    x_b, y_b, w_b, h_b = x_left, 0, (x_right - x_left), h

    # --------------------------------------------------------------------------
    # 1. DETECCIÓN HÍBRIDA DE SÍMBOLOS (COLOR + BLANCOS/BRUTOS)
    # --------------------------------------------------------------------------
    symbols_list: list[dict[str, Any]] = []
    symbol_boxes: list[tuple[int, int, int, int]] = []
    symbol_id = 1

    # Vía 1: Íconos saturados de color (Pink, Green, Blue, Magenta)
    mask_color = (hsv[:, :, 1] > 35) & (hsv[:, :, 2] > 70)

    # Vía 2: Íconos blancos / alto brillo (ALB, marcos blancos)
    mask_blancos = (hsv[:, :, 2] > 180) & (hsv[:, :, 1] < 60)

    # Combinación morfológica
    candidate_mask_raw = (mask_color | mask_blancos).astype(np.uint8)
    kernel_corte = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    candidate_mask = cv2.morphologyEx(candidate_mask_raw, cv2.MORPH_OPEN, kernel_corte)

    contours, _ = cv2.findContours(candidate_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        aspect = bw / bh if bh > 0 else 0
        cx, cy = x + bw // 2, y + bh // 2

        # FILTRO CLAVE 1: Debe estar dentro del ancho X de la pizarra asignada
        if not (x_left <= cx <= x_right):
            continue

        # FILTRO CLAVE 2: Geometría de ícono (~2.5-25% del tamaño menor)
        min_dim = 0.025 * min(h, w)
        max_dim = 0.25 * min(h, w)
        if min_dim < bw < max_dim and min_dim < bh < max_dim and 0.45 < aspect < 2.2 and area > 600:
            overlap = any(abs(x - tx) < 35 and abs(y - ty) < 35 for (tx, ty, _, _) in symbol_boxes)
            if not overlap:

                # FILTRO CLAVE 3: Anillo de Contraste Local
                margen = 15
                x_out, y_out = max(0, x - margen), max(0, y - margen)
                w_out, h_out = min(w - x_out, bw + (margen * 2)), min(h - y_out, bh + (margen * 2))

                mask_anillo = np.zeros((h, w), dtype=np.uint8)
                cv2.rectangle(mask_anillo, (x_out, y_out), (x_out + w_out, y_out + h_out), 255, -1)
                cv2.rectangle(mask_anillo, (x, y), (x + bw, y + bh), 0, -1)

                brillo_icono = np.mean(gray[y:y+bh, x:x+bw])
                brillo_anillo = cv2.mean(gray, mask=mask_anillo)[0]
                delta_contraste = abs(brillo_icono - brillo_anillo)

                if delta_contraste >= delta_contraste_min:
                    symbols_list.append({
                        'symbol_id': symbol_id,
                        'label': f"AWS_Icon_{symbol_id}",
                        'confidence': 1.0,
                        'box': [x, y, bw, bh],
                        'center': [cx, cy],
                        'width': bw,
                        'height': bh,
                        'delta_contraste': round(float(delta_contraste), 2),
                        'detection_method': 'adaptive_hybrid_roi'
                    })
                    symbol_boxes.append((x, y, bw, bh))
                    symbol_id += 1

    console.print(f"  ✅ Detección completada: {len(symbols_list)} íconos válidos detectados")

    # --------------------------------------------------------------------------
    # 2. FILTRO DE LÍNEAS DE CONEXIÓN
    # --------------------------------------------------------------------------
    line_mask = board_mask.copy()

    # Excluir cajas de íconos
    margin = 10
    for (bx, by, bw_s, bh_s) in symbol_boxes:
        x1, y1 = max(0, bx - margin), max(0, by - margin)
        x2, y2 = min(w, bx + bw_s + margin), min(h, by + bh_s + margin)
        line_mask[y1:y2, x1:x2] = 0

    blur_gray = cv2.GaussianBlur(gray, (3, 3), 0)
    raw_edges = cv2.Canny(blur_gray, 30, 100)

    connection_edges = cv2.bitwise_and(raw_edges, raw_edges, mask=line_mask)

    kernel_line = np.ones((3, 3), np.uint8)
    dilated_lines = cv2.dilate(connection_edges, kernel_line, iterations=1)

    # --------------------------------------------------------------------------
    # 3. VISUALIZACIÓN (Guardar imagen procesada, sin plt.show)
    # --------------------------------------------------------------------------
    res_img = img.copy()

    # Dibujar líneas de conexión en AMARILLO brillante
    res_img[dilated_lines > 0] = (0, 255, 255)

    # Superponer íconos legítimos
    for sym in symbols_list:
        x, y, bw, bh = sym['box']
        cx, cy = sym['center']
        lbl = sym['label']

        cv2.rectangle(res_img, (x, y), (x + bw, y + bh), (255, 0, 255), 2)
        cv2.circle(res_img, (cx, cy), 5, (0, 0, 255), -1)

        tag_str = f"{lbl} [C:({cx},{cy}) W:{bw} H:{bh}]"
        cv2.putText(res_img, tag_str, (x, max(18, y - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255), 1, cv2.LINE_AA)

    # Dibujar el encuadre cian exacto del área de trabajo
    cv2.rectangle(res_img, (x_b, y_b), (x_b + w_b, y_b + h_b), (255, 255, 0), 2)

    img_output_path = lab_workspace_dir / f"{ruta_img.stem}_processed_connections.jpg"
    cv2.imwrite(str(img_output_path), res_img)
    console.print(f"  ✅ Imagen procesada guardada en: {img_output_path}")

    return symbols_list, img_output_path


def format_symbols_for_prompt(symbols_list: list[dict[str, Any]]) -> str:
    """
    Formatea la lista de símbolos detectados como texto para inyectar en el prompt de Gemini.

    Returns
    -------
    str
        Sección de texto lista para concatenar al prompt.
    """
    if not symbols_list:
        return ""

    lines = [
        "\n## DETECTED SYMBOL POSITIONS (ADAPTIVE WHITEBOARD DETECTION):",
        f"The following {len(symbols_list)} AWS service icon regions were detected on the whiteboard using adaptive computer vision analysis.",
        "Use this spatial information to accurately identify and count the services in the diagram:\n",
    ]

    for sym in symbols_list:
        cx, cy = sym['center']
        bw, bh = sym['width'], sym['height']
        lines.append(
            f"- {sym['label']}: center=({cx},{cy}), size={bw}x{bh}"
        )

    lines.append(
        "\nPlease use this information to ensure the count and spatial arrangement of nodes "
        "in your output graph correspond correctly to these physical icons in the diagram."
    )

    return "\n".join(lines)
