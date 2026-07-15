#!/usr/bin/env python3
"""
process_15_parsimonious.py — Processes exactly 15 missing parsimonious graphs
                             using subprocess with a safety timeout.
"""
import json
import time
import sys
import subprocess
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def main():
    tracker_path = project_root / "data" / "processed_tracker.json"
    if not tracker_path.exists():
        print("Error: processed_tracker.json not found!")
        return

    with open(tracker_path, "r", encoding="utf-8") as f:
        tracker = json.load(f)

    v3_processed = set(tracker.get("version_3", []))

    good_whiteboard_dir = project_root / "data" / "good_whiteboard"
    good_ids = {p.stem for p in good_whiteboard_dir.glob("*.jpg")}

    raw_dir = project_root / "data" / "raw"
    
    # Filter videos that have a transcript and a good whiteboard but are not processed yet
    missing_videos = []
    for video_id in sorted(list(good_ids - v3_processed)):
        transcript_path = raw_dir / f"{video_id}_transcript.json"
        if transcript_path.exists():
            missing_videos.append(video_id)

    print(f"Total missing videos with transcript and good whiteboard: {len(missing_videos)}")
    
    # Take the first 15 (next ones in line)
    target_videos = missing_videos[:15]
    if not target_videos:
        print("No missing videos to process!")
        return

    print(f"Selected 15 videos to process: {target_videos}")
    print("Starting batch execution with subprocess timeouts...")
    
    start_time = time.time()
    successful = 0
    failed = 0
    max_success = 15
    max_failures = 3

    import os
    env = dict(os.environ)
    env["NO_GT_COMPARE"] = "true"
    env["GEMINI_MAX_RETRIES"] = "1"  # Disable retries inside vision_analyzer_parsimonious
    env["PYTHONIOENCODING"] = "utf-8"

    for idx, video_id in enumerate(target_videos, 1):
        if successful >= max_success:
            print(f"\nReached target of {max_success} successful graphs. Stopping.")
            break
        if failed >= max_failures:
            print(f"\nReached {max_failures} failures. Stopping early to prevent token/quota waste.")
            break

        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"\n==================================================")
        print(f"[Success: {successful}/{max_success}, Failures: {failed}/{max_failures}]")
        print(f"Processing video: {video_id} ({idx}/{len(target_videos)})...")
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
    # Evaluation is skipped to avoid using the Ground Truth or original Cloudscape files.
    pass

if __name__ == "__main__":
    main()
