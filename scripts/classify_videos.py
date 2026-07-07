#!/usr/bin/env python3
"""
classify_videos.py — Classify all cached video IDs into distinct categories.
"""
from __future__ import annotations

import json
from pathlib import Path
import networkx as nx

def main():
    workspace = Path(__file__).resolve().parent.parent
    data_dir = workspace / "data"
    
    # Load all video IDs from cache
    cache_path = data_dir / "video_id_cache.json"
    if not cache_path.exists():
        print(f"Error: video_id_cache.json not found at {cache_path}")
        return
        
    with open(cache_path, "r", encoding="utf-8") as f:
        cache = json.load(f)
        
    video_ids = sorted(list(cache.values()))
    print(f"Loaded {len(video_ids)} video IDs from cache.")

    # Paths to directories
    good_wb_dir = data_dir / "good_whiteboard"
    bad_wb_dir = data_dir / "bad_whiteboard"
    special_dir = data_dir / "special_cases"
    gt_dir = data_dir / "cloudscape_gt"

    # Identify sets
    good_wb_ids = {f.stem for f in good_wb_dir.glob("*.jpg")}
    bad_wb_ids = {f.stem for f in bad_wb_dir.glob("*.jpg")}
    special_ids = {f.stem for f in special_dir.glob("*.jpg")}
    
    # Classification dict
    classification = {
        "usable_evaluation": [],
        "invalid_ground_truth": [],
        "validation_only": [],
        "bad_whiteboard": []
    }
    
    for vid in video_ids:
        # Check if the video is classified as bad or special case
        if vid in bad_wb_ids or vid in special_ids:
            classification["bad_whiteboard"].append(vid)
            continue
            
        # Check if Ground Truth exists
        gt_path = gt_dir / f"{vid}.graphml"
        if gt_path.exists():
            try:
                G = nx.read_graphml(str(gt_path))
                usable = G.graph.get("graph_usable", True)
                if usable is False or str(usable).lower() == "false":
                    classification["invalid_ground_truth"].append(vid)
                else:
                    # Valid GT, now check if we have a good whiteboard
                    if vid in good_wb_ids:
                        classification["usable_evaluation"].append(vid)
                    else:
                        # Ground Truth is valid, but no whiteboard or bad whiteboard?
                        # Since we already checked bad_wb_ids and special_ids above,
                        # this means we haven't processed/labeled the whiteboard yet.
                        # It is effectively unusable for training/evaluation until we have a good whiteboard.
                        classification["bad_whiteboard"].append(vid)
            except Exception as e:
                # If reading fails, treat Ground Truth as invalid
                classification["invalid_ground_truth"].append(vid)
        else:
            # No Ground Truth exists
            if vid in good_wb_ids:
                classification["validation_only"].append(vid)
            else:
                classification["bad_whiteboard"].append(vid)
                
    # Sort lists
    for k in classification:
        classification[k] = sorted(classification[k])
        
    # Write to video_classification.json
    output_path = data_dir / "video_classification.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(classification, f, indent=2, ensure_ascii=False)
        
    # Print summary
    print(f"\nVideo classification complete! Saved to {output_path}")
    print(f"  * Usable Evaluation (Valid GT + Good Whiteboard): {len(classification['usable_evaluation'])}")
    print(f"  * Invalid Ground Truth (graph_usable = False):    {len(classification['invalid_ground_truth'])}")
    print(f"  * Validation Only (No GT + Good Whiteboard):       {len(classification['validation_only'])}")
    print(f"  * Bad Whiteboard / Ignored:                      {len(classification['bad_whiteboard'])}")
    print(f"Total classified: {sum(len(v) for v in classification.values())}")

if __name__ == "__main__":
    main()
