"""
downloader.py — YouTube video & metadata download via yt-dlp
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

import yt_dlp
from rich.console import Console

from config.settings import RAW_DIR, VIDEO_FORMAT

console = Console()


def download_video(url: str, output_dir: Path | None = None) -> dict[str, Any]:
    """
    Download a YouTube video in the best quality and return its metadata.

    Parameters
    ----------
    url : str
        Full YouTube URL.
    output_dir : Path, optional
        Directory to save the video. Defaults to ``data/raw/``.

    Returns
    -------
    dict
        Metadata dict from yt-dlp (title, id, duration, description, …).
    """
    output_dir = output_dir or RAW_DIR

    ydl_opts: dict[str, Any] = {
        "format": VIDEO_FORMAT,
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "writeinfojson": True,          # save .info.json alongside
        "writethumbnail": False,
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [_progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        console.print(f"\n[bold cyan]⬇  Downloading:[/] {url}")
        info: dict = ydl.extract_info(url, download=True)
        # Sanitize for safe serialisation (remove callables etc.)
        info = ydl.sanitize_info(info)

    video_id = info.get("id", "unknown")
    video_path = output_dir / f"{video_id}.mp4"
    meta_path = output_dir / f"{video_id}.info.json"

    console.print(f"[green]✓[/] Video saved  → [bold]{video_path}[/]")
    if meta_path.exists():
        console.print(f"[green]✓[/] Metadata     → [bold]{meta_path}[/]")

    return info


def load_metadata(video_id: str, data_dir: Path | None = None) -> dict[str, Any]:
    """Load previously saved yt-dlp metadata JSON."""
    data_dir = data_dir or RAW_DIR
    meta_path = data_dir / f"{video_id}.info.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Metadata not found: {meta_path}")
    return json.loads(meta_path.read_text(encoding="utf-8"))


# ── Internal ─────────────────────────────────────────────────

def _progress_hook(d: dict) -> None:
    """Pretty-print download progress."""
    status = d.get("status")
    if status == "downloading":
        pct = d.get("_percent_str", "?%")
        speed = d.get("_speed_str", "?")
        eta = d.get("_eta_str", "?")
        console.print(
            f"  [dim]{pct}  •  {speed}  •  ETA {eta}[/]",
            end="\r",
        )
    elif status == "finished":
        console.print("\n  [bold green]Download complete, merging…[/]")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Download YouTube video & metadata.")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()
    try:
        download_video(args.url)
    except Exception as e:
        console.print(f"\n[bold red]✗ Download failed:[/] {e}")
