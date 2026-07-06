"""
extractor.py — FFmpeg-based audio & keyframe extraction
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rich.console import Console

from config.settings import AUDIO_DIR, FRAMES_DIR, FRAME_INTERVAL_SEC

console = Console()


def extract_audio(video_path: Path, output_dir: Path | None = None) -> Path:
    """
    Extract the audio track from a video as 16 kHz mono WAV
    (optimal for Whisper).

    Returns
    -------
    Path
        Path to the extracted .wav file.
    """
    output_dir = output_dir or AUDIO_DIR
    stem = video_path.stem
    audio_path = output_dir / f"{stem}.wav"

    if audio_path.exists():
        console.print(f"[yellow]⚠[/]  Audio already exists: {audio_path}")
        return audio_path

    console.print(f"[bold cyan]🔊  Extracting audio[/] → {audio_path}")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vn",                      # no video
        "-acodec", "pcm_s16le",     # 16-bit PCM
        "-ar", "16000",             # 16 kHz sample rate
        "-ac", "1",                 # mono
        str(audio_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]✗[/] FFmpeg error:\n{result.stderr}")
        raise RuntimeError(f"Audio extraction failed: {result.stderr[:500]}")

    console.print(f"[green]✓[/] Audio extracted → [bold]{audio_path}[/]")
    return audio_path

def extract_keyframes(
    video_path: Path,
    interval_sec: int | None = None,
    output_dir: Path | None = None,
) -> list[Path]:
    """
    Extract keyframes from a video using the custom density strategy:
    - First 80% of video duration: 1 frame every 10 seconds.
    - Last 20% of video duration: 1 frame every 1 second.
    - Saved as {stem}_frame_{frame_idx:05d}.jpg (using the actual raw frame index).
    """
    import cv2
    import numpy as np
    
    output_dir = output_dir or FRAMES_DIR
    stem = video_path.stem

    # Create a sub-folder per video to keep frames organized
    frames_subdir = output_dir / stem
    
    # Clean previous frames to avoid mixing naming conventions
    if frames_subdir.exists():
        for f in frames_subdir.glob("*.jpg"):
            try:
                f.unlink()
            except Exception:
                pass
    else:
        frames_subdir.mkdir(parents=True, exist_ok=True)

    console.print(
        f"[bold cyan]🖼  Extracting custom keyframes (80% @ 10s, 20% @ 1s)[/] → {frames_subdir}/"
    )

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")
        
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps if fps else 0.0

    # Calculate timestamps
    boundary = duration * 0.80
    
    timestamps = []
    # 80% every 10 seconds
    t = 0.0
    while t < boundary:
        timestamps.append(t)
        t += 10.0
        
    # Last 20% every 1 second
    t = boundary
    while t <= duration:
        timestamps.append(t)
        t += 1.0
        
    # Deduplicate and sort
    timestamps = sorted(list(set(timestamps)))

    frames = []
    for idx, t_val in enumerate(timestamps):
        frame_idx = int(round(t_val * fps))
        if frame_idx >= total_frames:
            frame_idx = total_frames - 1
            
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Name frame using its raw index to match the standard
        frame_name = f"{stem}_frame_{frame_idx:05d}.jpg"
        frame_path = frames_subdir / frame_name
        cv2.imwrite(str(frame_path), frame)
        frames.append(frame_path)
        
    cap.release()
    console.print(f"[green]✓[/] Extracted [bold]{len(frames)}[/] keyframes using raw frame indices.")
    return sorted(frames)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract audio or keyframes from video.")
    parser.add_argument("video_path", help="Path to video file")
    parser.add_argument("--audio", action="store_true", help="Extract audio only")
    parser.add_argument("--frames", action="store_true", help="Extract keyframes only")
    parser.add_argument("--interval", type=int, default=None, help="Keyframe interval in seconds")
    args = parser.parse_args()
    
    vp = Path(args.video_path)
    if args.audio or not args.frames:
        try:
            extract_audio(vp)
        except Exception as e:
            console.print(f"[red]✗[/] Audio extraction failed: {e}")
    if args.frames or not args.audio:
        try:
            extract_keyframes(vp, interval_sec=args.interval)
        except Exception as e:
            console.print(f"[red]✗[/] Frame extraction failed: {e}")
