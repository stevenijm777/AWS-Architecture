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
    Extract one frame every ``interval_sec`` seconds as JPEG.

    Returns
    -------
    list[Path]
        Sorted list of extracted frame file paths.
    """
    interval_sec = interval_sec or FRAME_INTERVAL_SEC
    output_dir = output_dir or FRAMES_DIR
    stem = video_path.stem

    # Create a sub-folder per video to keep frames organized
    frames_subdir = output_dir / stem
    frames_subdir.mkdir(parents=True, exist_ok=True)

    pattern = str(frames_subdir / f"{stem}_frame_%04d.jpg")

    console.print(
        f"[bold cyan]🖼  Extracting keyframes[/] every {interval_sec}s "
        f"→ {frames_subdir}/"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"fps=1/{interval_sec}",   # 1 frame per N seconds
        "-q:v", "2",                       # JPEG quality (2 = high)
        pattern,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        console.print(f"[red]✗[/] FFmpeg error:\n{result.stderr}")
        raise RuntimeError(f"Frame extraction failed: {result.stderr[:500]}")

    frames = sorted(frames_subdir.glob("*.jpg"))
    console.print(f"[green]✓[/] Extracted [bold]{len(frames)}[/] keyframes")
    return frames


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
