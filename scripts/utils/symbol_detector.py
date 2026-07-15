"""
symbol_detector.py — Detect AWS service icons in a whiteboard frame using template matching
"""
from __future__ import annotations

import json
from pathlib import Path
import cv2
import numpy as np
from rich.console import Console

console = Console()

# Denser, wider set of scales to handle different template sizes and whiteboard resolutions
SCALES_TO_TEST = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]

# Keyword mapping to detect mentioned services from the transcript
SERVICE_KEYWORDS = {
    "apigateway": ["api gateway", "apigateway", "gateway"],
    "autoscaling": ["auto scaling", "autoscaling", "asg"],
    "cloudfront": ["cloudfront", "cloud front"],
    "cloudwatch": ["cloudwatch", "cloud watch"],
    "lambda": ["lambda"],
    "s3": ["s3", "simple storage", "bucket"],
    "spotinstance": ["spot instance", "spotinstance", "spot", "sport instance", "sport"],
    "sqs": ["sqs", "simple queue"],
    "stepfunctions": ["step function", "stepfunctions", "step-function"],
    "phone": ["mobile", "phone", "device"],
    "machine": ["pc", "computer", "machine", "desktop"],
    "cloudsearch": ["cloudsearch", "cloud search", "search"],
    "elasticache": ["elasticache", "cache", "redis", "memcached"],
    "dynamodb": ["dynamodb", "dynamo"],
    "ec2": ["ec2", "virtual machine", "instance"],
    "eks": ["eks", "kubernetes", "k8s"],
    "rds": ["rds", "relational database", "database", "postgres", "mysql"],
    "kinesis": ["kinesis", "stream", "data stream"],
    "greengrass": ["greengrass", "iot greengrass"],
    "documentdb": ["documentdb", "document db", "mongodb"],
    "userconsumermobile": ["mobile app", "ios", "android", "user app"]
}

def non_max_suppression(boxes: list[tuple[int, int, int, int, float]], overlap_thresh: float = 0.3) -> list[tuple[int, int, int, int, float]]:
    """
    Perform Non-Maximum Suppression (NMS) on boxes.
    Each box is (x1, y1, x2, y2, score).
    """
    if not boxes:
        return []
    
    # Convert to numpy array
    boxes_arr = np.array(boxes, dtype=np.float32)
    x1 = boxes_arr[:, 0]
    y1 = boxes_arr[:, 1]
    x2 = boxes_arr[:, 2]
    y2 = boxes_arr[:, 3]
    scores = boxes_arr[:, 4]
    
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        
        denom = (areas[i] + areas[order[1:]] - inter)
        iou = np.zeros_like(inter)
        valid = denom > 0
        iou[valid] = inter[valid] / denom[valid]
        
        inds = np.where(iou <= overlap_thresh)[0]
        order = order[inds + 1]
        
    return [boxes[i] for i in keep]

def get_services_from_transcript_text(transcript_text: str) -> list[str]:
    """Identify mentioned AWS services based on keywords in transcript text."""
    if not transcript_text:
        return []
    
    full_text = transcript_text.lower()
    mentioned = []
    for service, keywords in SERVICE_KEYWORDS.items():
        for kw in keywords:
            if kw in full_text:
                mentioned.append(service)
                break
    return mentioned

def detect_symbols(
    image_path: Path,
    templates_dir: Path,
    transcript_text: str = "",
    threshold: float = 0.75
) -> dict[str, list[dict[str, Any]]]:
    """
    Detect AWS service icons in a single image.
    
    Returns:
        dict: mapping base service name to a list of detections (box, confidence).
    """
    if not image_path.exists():
        console.print(f"[red]Error: Image {image_path} does not exist.[/]")
        return {}
        
    img_color = cv2.imread(str(image_path))
    if img_color is None:
        console.print(f"[red]Error: Failed to read image {image_path}.[/]")
        return {}
        
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    # 1. Load available templates
    available_templates = {}
    if templates_dir.exists():
        for p in templates_dir.glob("*"):
            if p.suffix.lower() not in [".png", ".jpg"]:
                continue
            if p.name in ["verify_crops.jpg", "verify_crops.png"]:
                continue
            
            stem_lower = p.stem.lower()
            base_service = stem_lower.split("_")[0]
            
            t_img_gray = cv2.imread(str(p), cv2.IMREAD_GRAYSCALE)
            available_templates[p.stem] = {
                "stem": p.stem,
                "base_service": base_service,
                "img": t_img_gray
            }
            
    if not available_templates:
        console.print(f"[yellow]Warning: No templates found in {templates_dir}[/]")
        return {}
        
    # 2. Use all available templates (transcript filtering disabled by default)
    templates = available_templates
    console.print(f"[dim]Using all {len(templates)} available templates (transcript filtering is disabled).[/]")
        
    # Group boxes by base service
    service_boxes = {}
    
    for t_name, t_data in templates.items():
        t_img = t_data["img"]
        base_service = t_data["base_service"]
        
        template_boxes = []
        for scale in SCALES_TO_TEST:
            w = int(t_img.shape[1] * scale)
            h = int(t_img.shape[0] * scale)
            if w > img_gray.shape[1] or h > img_gray.shape[0]:
                continue
            
            resized_t = cv2.resize(t_img, (w, h))
            res = cv2.matchTemplate(img_gray, resized_t, cv2.TM_CCOEFF_NORMED)
            
            # Local maxima
            res_dilated = cv2.dilate(res, np.ones((5, 5)))
            local_max = (res == res_dilated) & (res >= threshold)
            y_coords, x_coords = np.where(local_max)
            
            for y, x in zip(y_coords, x_coords):
                score = float(res[y, x])
                template_boxes.append((x, y, x + w, y + h, score))
                
        # NMS per template
        keep_boxes = non_max_suppression(template_boxes, overlap_thresh=0.3)
        if keep_boxes:
            if base_service not in service_boxes:
                service_boxes[base_service] = []
            for bx1, by1, bx2, by2, score in keep_boxes:
                service_boxes[base_service].append({
                    "box": (int(bx1), int(by1), int(bx2), int(by2)),
                    "confidence": score
                })
                
    # Apply NMS across the same service category to avoid double-counting different template shapes of the same service
    final_detections = {}
    for service, detections in service_boxes.items():
        raw_boxes = []
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            raw_boxes.append((x1, y1, x2, y2, det["confidence"]))
            
        keep_boxes = non_max_suppression(raw_boxes, overlap_thresh=0.4)
        final_detections[service] = []
        for bx1, by1, bx2, by2, score in keep_boxes:
            final_detections[service].append({
                "box": (int(bx1), int(by1), int(bx2), int(by2)),
                "confidence": score
            })
            
    return final_detections
