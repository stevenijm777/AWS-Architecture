import json
import os
from pathlib import Path
from config.settings import DATA_DIR

TRACKER_PATH = DATA_DIR / "processed_tracker.json"

def load_tracker():
    default_structure = {
        "version_1": [],
        "version_2": [],
        "version_3": []
    }
    
    if not TRACKER_PATH.exists():
        return default_structure
        
    try:
        with open(TRACKER_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all keys exist
            for key in default_structure:
                if key not in data:
                    data[key] = []
            return data
    except Exception as e:
        print(f"Warning: Error reading tracker JSON: {e}. Starting fresh.")
        return default_structure

def save_tracker(tracker_data):
    try:
        # Keep lists unique and sorted
        for key in tracker_data:
            tracker_data[key] = sorted(list(set(tracker_data[key])))
            
        with open(TRACKER_PATH, "w", encoding="utf-8") as f:
            json.dump(tracker_data, f, indent=2)
    except Exception as e:
        print(f"Error saving tracker JSON: {e}")

def add_to_tracker(video_id, version):
    """
    version should be "version_1", "version_2", or "version_3".
    """
    tracker = load_tracker()
    if version in tracker:
        if video_id not in tracker[version]:
            tracker[version].append(video_id)
            save_tracker(tracker)
            print(f"Registered {video_id} under {version} in tracker.")
    else:
        print(f"Error: Unknown version '{version}' for tracker.")
