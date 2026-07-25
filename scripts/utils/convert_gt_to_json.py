"""
convert_gt_to_json.py — Utility to parse all Ground Truth .graphml files
                      and export them into clean JSON files in data/cloudscape_gt_json/
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "whiteboard_selection_lab" / "algorithms"))

from dynamic_rag_matcher import parse_graphml_file


def convert_all_ground_truths(gt_dir: Path, output_dir: Path):
    """Parse all .graphml files in gt_dir and export them as JSON to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    graphml_files = list(gt_dir.glob("*.graphml"))
    
    print(f"🔄 Converting {len(graphml_files)} Ground Truth .graphml files to JSON...")
    
    count = 0
    for p in graphml_files:
        try:
            gt_obj = parse_graphml_file(p)
            json_data = gt_obj.to_json()
            
            # Save JSON
            out_file = output_dir / f"{p.stem}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            count += 1
        except Exception as e:
            print(f"  [yellow]⚠ Error converting {p.name}: {e}[/]")
            
    print(f"✅ Successfully exported {count} Ground Truth JSON files to: {output_dir}")


if __name__ == "__main__":
    gt_dir = PROJECT_ROOT / "data" / "cloudscape_gt"
    output_dir = PROJECT_ROOT / "data" / "cloudscape_gt_json"
    convert_all_ground_truths(gt_dir, output_dir)
