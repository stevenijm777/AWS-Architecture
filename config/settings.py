"""
Cloud Architecture Extractor — Configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


# ── Paths ────────────────────────────────────────────────────
DATA_DIR    = _PROJECT_ROOT / "data"
RAW_DIR     = DATA_DIR / "raw"
AUDIO_DIR   = DATA_DIR / "audio"
FRAMES_DIR  = DATA_DIR / "frames"
GRAPHS_DIR  = DATA_DIR / "graphs"
LOGS_DIR    = _PROJECT_ROOT / "logs"

# Ensure all dirs exist
for d in (RAW_DIR, AUDIO_DIR, FRAMES_DIR, GRAPHS_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ── API Keys ─────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")


# ── Whisper ──────────────────────────────────────────────────
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "turbo")
WHISPER_DEVICE: str = "cuda"  # RTX 5070 Ti


# ── Frame Extraction ────────────────────────────────────────
FRAME_INTERVAL_SEC: int = int(os.getenv("FRAME_INTERVAL_SEC", "10"))


# ── yt-dlp ──────────────────────────────────────────────────
VIDEO_FORMAT: str = os.getenv(
    "VIDEO_FORMAT",
    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
)


# ── Gemini ──────────────────────────────────────────────────
# Usable Gemini Models include:
# - gemini-2.5-flash                  (Recommended default, fast, multimodal & balanced)
# - gemini-2.5-pro                    (High intelligence, complex reasoning, coding)
# - gemini-2.0-flash                  (Multimodal, high speed, bypasses daily quota of 2.5 Flash)
# - gemini-2.0-flash-lite-preview-02-05 (Extremely fast, lightweight tasks)
# - gemini-2.0-pro-exp-02-05          (Experimental high intelligence model)
# - gemini-1.5-flash                  (Standard flash model)
# - gemini-1.5-pro                    (Standard pro model, large context window)
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

