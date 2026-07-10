#!/usr/bin/env python3
"""
process_10_parsimonious.py — Processes up to 10 successful parsimonious graphs from a custom list.
                             Stops immediately on the 3rd failure to prevent token wasting.
"""
import json
import time
import sys
import os
import subprocess
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def main():
    # Load user provided list of videos
    target_list = [
        "KywvGM6HVXI", "KzJKdUZ3Ba4", "L8a6qI14MwA", "LD5ksgnu8r8", "LPZlrX2cNjo", 
        "LYP98nPBj2A", "LxeSC3-xMlk", "Ly_UhX3LCCs", "M_hqigB9C4I", "MbkLJ62jtMc", 
        "NfUwtK8ALtw", "O11BgSm7V14", "O3s3MWD-UUA", "O5Sn5QCEAzE", "OQKOHNtyz3E", 
        "OTPyxlTjWp0", "OWLGK-eVrTw", "OYHSkwt31Vc", "OrC9cLYMbas", "Pc7_uOdlGKo", 
        "PgeQufaQy7I", "PoYiSKUy8sE", "RU__HBEMDvQ", "S85DeDgWQSc", "SC6n6J8Bi58", 
        "V6rYfjJG3BE", "W4QzOaKCX2Y", "WojdRyYDvDM", "X3mC6Yfd138", "XCnul-AjrNU", 
        "YV8e36ZywLk", "Yju3yReAQtc", "_cca2eNePC4", "aovXn5QDEzU", "c6yBZBMwtLk", 
        "cZuoiXQ0xUk", "cczJb4heExQ", "cmYI6axlicc", "ebngmAqbe-k", "ec6j-MaOSUc", 
        "fbzeoxxyzIw", "gcgtLDB0cKA", "gpWR5JBC64A", "hlVnmCfydIs", "hnMQFnTGr3I", 
        "i4ueYgjVDCw", "iI0OQtXnWrs", "irpARK1Tdo4"
    ]

    tracker_path = project_root / "data" / "processed_tracker.json"
    if not tracker_path.exists():
        print("Error: processed_tracker.json not found!")
        return

    with open(tracker_path, "r", encoding="utf-8") as f:
        tracker = json.load(f)

    v3_processed = set(tracker.get("version_3", []))

    # Filter out videos that already have their parsimonious graphml on disk
    good_whiteboard_dir = project_root / "data" / "good_whiteboard"
    graphs_pars_dir = project_root / "data" / "graphs_parsimonious"
    
    missing_videos = []
    for vid in target_list:
        # Check if the graphml file already exists physically
        graphml_path = graphs_pars_dir / f"{vid}.graphml"
        if not graphml_path.exists():
            missing_videos.append(vid)

    print(f"Total videos from custom list that are missing graphs: {len(missing_videos)}")
    
    if not missing_videos:
        print("No missing videos to process from the provided list!")
        return

    print("Starting batch execution...")
    
    start_time = time.time()
    successful = 0
    failed = 0
    max_success = 2
    max_failures = 2

    env = dict(os.environ)
    env["NO_GT_COMPARE"] = "true"
    env["GEMINI_MAX_RETRIES"] = "1"  # Disable retries inside vision_analyzer_parsimonious
    env["PYTHONIOENCODING"] = "utf-8"

    for idx, video_id in enumerate(missing_videos, 1):
        if successful >= max_success:
            print(f"\nReached target of {max_success} successful graphs. Stopping.")
            break
        if failed >= max_failures:
            print(f"\nReached {max_failures} failures. Stopping early to prevent token/quota waste.")
            break

        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\n==================================================")
        print(f"[Success: {successful}/{max_success}, Failures: {failed}/{max_failures}]")
        print(f"Processing video: {video_id} ({idx}/{len(missing_videos)} in queue)...")
        print(f"==================================================")
        
        single_start = time.time()
        try:
            cmd = [
                sys.executable,
                str(project_root / "main_parsimonious.py"),
                "--url", url
            ]
            # Run with a 90-second timeout, set UTF-8 encoding
            res = subprocess.run(cmd, timeout=90, capture_output=True, text=True, encoding="utf-8", env=env, check=True)
            duration = time.time() - single_start
            print(res.stdout)
            print(f"✓ Finished {video_id} successfully in {duration:.2f}s")
            successful += 1
        except subprocess.TimeoutExpired as e:
            duration = time.time() - single_start
            print(f"✗ Timeout: processing {video_id} hung for more than 90 seconds. Skipped.")
            failed += 1
        except subprocess.CalledProcessError as e:
            duration = time.time() - single_start
            print(f"✗ Failed: processing {video_id} returned exit code {e.returncode} after {duration:.2f}s.")
            print(f"Stdout:\n{e.stdout}")
            print(f"Stderr:\n{e.stderr}")
            failed += 1
        except Exception as e:
            duration = time.time() - single_start
            print(f"✗ Error: unexpected issue processing {video_id} after {duration:.2f}s: {e}")
            failed += 1
            
        # Optional: Sleep briefly between calls to prevent rate limits
        time.sleep(2)

    total_duration = time.time() - start_time
    print("\n==================================================")
    print("Batch processing complete!")
    print(f"  * Successful: {successful}/{max_success}")
    print(f"  * Failed:     {failed}/{max_failures}")
    print(f"  * Total Time:  {total_duration:.2f} seconds ({total_duration/60:.2f} minutes)")
    print("==================================================")

if __name__ == "__main__":
    main()
