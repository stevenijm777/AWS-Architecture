"""
bulk_preprocess_local.py — Preprocess 50 new videos locally (no API calls, no graph builds).
"""
import json
import os
import subprocess
import pandas as pd
from pathlib import Path
from rich.console import Console

console = Console()

def get_video_id(title: str) -> str | None:
    query = f"AWS Architecture {title}"
    try:
        res = subprocess.run(
            ["yt-dlp", "--get-id", f"ytsearch1:{query}"],
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.strip().split("\n")[0]
    except Exception as e:
        console.print(f"[yellow]⚠ Failed to find ID for '{title}': {e}[/]")
        return None

def main():
    df = pd.read_csv("videos.csv")
    raw_dir = Path("data/raw")
    frames_dir = Path("data/frames")

    preprocessed_count = 0
    limit = 50

    console.print(f"Starting bulk local preprocessing. Target: {limit} videos.")

    for idx, row in df.iterrows():
        if preprocessed_count >= limit:
            break

        title = row["title"]
        
        # Skip special, compilation, or long videos (> 12 minutes)
        title_lower = title.lower()
        duration_str = str(row['duration'])
        is_special = False
        if any(k in title_lower for k in ["spotlight", "greatest hits", "bloopers", "reprise", "(special)", "(special episode)"]):
            is_special = True
        else:
            try:
                parts = duration_str.strip().split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                elif len(parts) == 3:
                    minutes = int(parts[0]) * 60 + int(parts[1])
                else:
                    minutes = 0
                if minutes >= 12:
                    is_special = True
            except Exception:
                pass
                
        if is_special:
            console.print(f"[yellow]Skipping special/compilation/long video: '{title}'[/]")
            continue

        console.print(f"\n[bold]Checking video {idx+1}/{len(df)}: '{title}'[/]")

        # Get video ID from CSV or fallback to yt-dlp
        video_id = str(row["video_id"]).strip() if "video_id" in row and pd.notna(row["video_id"]) and str(row["video_id"]).strip() else None
        if not video_id:
            video_id = get_video_id(title)
            
        if not video_id:
            continue

        # Paths to check
        transcript_path = raw_dir / f"{video_id}_transcript.json"
        best_frame_path = frames_dir / f"{video_id}_pizarra" / "best_whiteboard.jpg"

        # If already preprocessed, skip
        if transcript_path.exists() and best_frame_path.exists():
            console.print(f"[dim]→ Video {video_id} is already fully preprocessed locally. Skipping.[/]")
            continue

        console.print(f"[cyan]→ Preprocessing {video_id} locally...[/]")
        url = f"https://www.youtube.com/watch?v={video_id}"
        cmd = [
            sys.executable,
            "main.py",
            "--url", url,
            "--skip-vision"
        ]

        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode == 0:
                console.print(f"[green]✓ Fully preprocessed locally: {video_id}[/]")
                preprocessed_count += 1
                console.print(f"Progress: {preprocessed_count}/{limit} completed.")
            else:
                console.print(f"[red]✗ Failed to preprocess {video_id}: {res.stderr.strip()}[/]")
        except Exception as e:
            console.print(f"[red]✗ Error executing command for {video_id}: {e}[/]")

    console.print(f"\n[bold green]✓[/] Completed local preprocessing of {preprocessed_count} videos.")

if __name__ == "__main__":
    main()
