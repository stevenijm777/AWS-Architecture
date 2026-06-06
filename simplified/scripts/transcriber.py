"""
transcriber.py — Local Whisper transcription (GPU-accelerated)
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

import whisper
from rich.console import Console

from config.settings import WHISPER_MODEL, WHISPER_DEVICE

console = Console()

# Module-level cache so the model is loaded only once
_model: whisper.Whisper | None = None


def _get_model() -> whisper.Whisper:
    """Lazy-load the Whisper model onto the GPU."""
    global _model
    if _model is None:
        console.print(
            f"[bold cyan]🧠  Loading Whisper model[/] "
            f"[bold]'{WHISPER_MODEL}'[/] on [bold]{WHISPER_DEVICE}[/] …"
        )
        _model = whisper.load_model(WHISPER_MODEL, device=WHISPER_DEVICE)
        console.print("[green]✓[/] Whisper model loaded")
    return _model


def transcribe(audio_path: Path, language: str | None = None) -> dict:
    """
    Transcribe an audio file using OpenAI Whisper on the local GPU.

    Parameters
    ----------
    audio_path : Path
        Path to a .wav or .mp3 file.
    language : str, optional
        ISO 639-1 code (e.g. ``"en"``). ``None`` = auto-detect.

    Returns
    -------
    dict
        Whisper result dict with keys ``text``, ``segments``, ``language``.
    """
    model = _get_model()

    console.print(f"[bold cyan]📝  Transcribing[/] {audio_path.name} …")

    opts: dict = {"fp16": True, "verbose": False}
    if language:
        opts["language"] = language

    result: dict = model.transcribe(str(audio_path), **opts)

    seg_count = len(result.get("segments", []))
    detected_lang = result.get("language", "?")
    console.print(
        f"[green]✓[/] Transcription complete — "
        f"{seg_count} segments, language: [bold]{detected_lang}[/]"
    )

    return result


def get_timestamped_segments(result: dict) -> list[dict]:
    """
    Return a clean list of segments with start/end times and text.

    Each dict: ``{"start": float, "end": float, "text": str}``
    """
    return [
        {
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        }
        for seg in result.get("segments", [])
        if seg.get("text", "").strip()
    ]


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe audio file using local Whisper.")
    parser.add_argument("audio_path", help="Path to audio file")
    parser.add_argument("--lang", default=None, help="Language hint (e.g. 'en')")
    args = parser.parse_args()
    try:
        transcribe(Path(args.audio_path), language=args.lang)
    except Exception as e:
        console.print(f"\n[bold red]✗ Transcription failed:[/] {e}")
