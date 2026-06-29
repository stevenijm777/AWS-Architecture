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


def extract_video_id(url: str) -> str | None:
    if "v=" in url:
        part = url.split("v=")[1]
        return part.split("&")[0].split("#")[0]
    elif "youtu.be/" in url:
        part = url.split("youtu.be/")[1]
        return part.split("?")[0].split("#")[0]
    elif "embed/" in url:
        part = url.split("embed/")[1]
        return part.split("?")[0].split("#")[0]
    elif "youtube.com/v/" in url:
        part = url.split("youtube.com/v/")[1]
        return part.split("?")[0].split("#")[0]
    return None


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

    video_id = extract_video_id(url)
    if video_id:
        info_path = output_dir / f"{video_id}.info.json"
        video_path = output_dir / f"{video_id}.mp4"
        if video_path.exists():
            console.print(f"[yellow]⚠[/] Video for {video_id} already exists locally. Skipping download.")
            if info_path.exists():
                with open(info_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                dummy_info = {
                    "id": video_id,
                    "title": f"Video {video_id}",
                    "duration": 0,
                    "description": ""
                }
                with open(info_path, "w", encoding="utf-8") as f:
                    json.dump(dummy_info, f, indent=2, ensure_ascii=False)
                return dummy_info

    cookies_path = Path(__file__).resolve().parent.parent / "cookies.txt"

    ydl_opts: dict[str, Any] = {
        "format": VIDEO_FORMAT,
        "outtmpl": str(output_dir / "%(id)s.%(ext)s"),
        "merge_output_format": "mp4",
        "writeinfojson": True,          # save .info.json alongside
        "writethumbnail": False,
        "quiet": False,
        "no_warnings": False,
        "extractor_args": {"youtube": ["player_client=android"]},
        "progress_hooks": [_progress_hook],
    }

    if cookies_path.exists():
        ydl_opts["cookiefile"] = str(cookies_path)
        console.print("[green]✓[/] Using cookies from cookies.txt")

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
