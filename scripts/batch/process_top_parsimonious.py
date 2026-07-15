import subprocess
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent

# Top best video IDs according to the evaluation report
top_videos = [
    "BlCXEMp_lqY",
    "Cgv0kfp_6xQ",
    "8TExnSvZqt0",
    "-3lnf5lzsH0",
    "07lfvavMdfU",
    "4WjXH8Wp0E4",
    "6YkguepAQuQ",
    "7LziNjUTo7w",
    "AzM_d7ZvzUE"
]

print(f"Starting parsimonious batch processing for {len(top_videos)} top videos...")

for idx, video_id in enumerate(top_videos, 1):
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n==================================================")
    print(f"[{idx}/{len(top_videos)}] Processing: {video_id}")
    print(f"==================================================")
    
    cmd = [sys.executable, str(project_root / "main.py"), "--url", url, "--force-vision", "--mode", "parsimonious"]
    result = subprocess.run(cmd)
    
    if result.returncode != 0:
        print(f"Warning: Pipeline execution failed for {video_id}")
    else:
        print(f"Success: Processed {video_id}")

print("\nBatch processing finished!")
