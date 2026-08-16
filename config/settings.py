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
DATA_DIR            = _PROJECT_ROOT / "data"
RAW_DIR             = DATA_DIR / "raw"
AUDIO_DIR           = DATA_DIR / "audio"
FRAMES_DIR          = DATA_DIR / "frames"
GRAPHS_DIR          = DATA_DIR / "graphs"
GOOD_WHITEBOARD_DIR = DATA_DIR / "good_whiteboard"
BAD_WHITEBOARD_DIR  = DATA_DIR / "bad_whiteboard"
UNPROCESSED_DIR     = DATA_DIR / "un_processed"
PROCESADOS_DIR      = DATA_DIR / "procesados"
LOGS_DIR            = _PROJECT_ROOT / "logs"

# Ensure all dirs exist
for d in (RAW_DIR, AUDIO_DIR, FRAMES_DIR, GRAPHS_DIR, GOOD_WHITEBOARD_DIR, BAD_WHITEBOARD_DIR, UNPROCESSED_DIR, PROCESADOS_DIR, LOGS_DIR):
    d.mkdir(parents=True, exist_ok=True)


# ── API Keys ─────────────────────────────────────────────────
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
raw_keys = os.getenv("GEMINI_API_KEYS", GEMINI_API_KEY)
GEMINI_API_KEYS: list[str] = [k.strip() for k in raw_keys.split(",") if k.strip()]
if not GEMINI_API_KEYS and GEMINI_API_KEY:
    GEMINI_API_KEYS = [GEMINI_API_KEY]



# ── Whisper ──────────────────────────────────────────────────
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "turbo")
import torch
WHISPER_DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"


# ── Frame Extraction ────────────────────────────────────────
FRAME_INTERVAL_SEC: int = int(os.getenv("FRAME_INTERVAL_SEC", "10"))


# ── yt-dlp ──────────────────────────────────────────────────
VIDEO_FORMAT: str = os.getenv(
    "VIDEO_FORMAT",
    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
)


# ── Gemini ──────────────────────────────────────────────────
# The default must match what .env actually sets, otherwise anyone running
# without a .env silently evaluates on a different model than the reports claim.
# Usable Gemini models include:
# - gemini-3.6-flash                  (current default: fast, multimodal, used for all runs since Aug 2026)
# - gemini-3.5-flash                  (previous default)
# - gemini-2.5-flash / gemini-2.5-pro (older generation, higher latency on vision)
# - gemini-2.0-flash                  (multimodal, high speed, separate daily quota)
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

