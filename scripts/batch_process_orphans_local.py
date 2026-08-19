#!/usr/bin/env python3
"""
batch_process_orphans_local.py — Local-only preprocessing for a specific ID list.

Runs main.py --skip-vision (download, audio extraction, Whisper transcription,
whiteboard frame selection) for a fixed list of video IDs, never calling Gemini.
Unlike bulk_preprocess_local.py, this does not scan all of videos.csv — it only
touches the IDs passed on the command line, so it can't accidentally reprocess
or skip unrelated rows.

Checkpointed per video: safe to interrupt and rerun.

Usage:
    .venv/bin/python scripts/batch_process_orphans_local.py --ids-file path/to/ids.txt
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from rich.console import Console
from rich.panel import Panel

from config.settings import DATA_DIR, FRAMES_DIR, RAW_DIR

console = Console()
PROGRESS_FILE = DATA_DIR / "batch_orphans_local_progress.json"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, ensure_ascii=False), encoding="utf-8")


def already_done(vid: str) -> bool:
    transcript = RAW_DIR / f"{vid}_transcript.json"
    frame = FRAMES_DIR / f"{vid}_pizarra" / "best_whiteboard.jpg"
    return transcript.exists() and frame.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description="Local-only preprocessing for a fixed video ID list")
    parser.add_argument("--ids-file", required=True, help="Text file, one video_id per line")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ids = [l.strip() for l in Path(args.ids_file).read_text(encoding="utf-8").splitlines() if l.strip()]
    progress = load_progress()

    console.print(Panel.fit(
        f"[bold cyan]Local preprocessing (no Gemini calls)[/]\n"
        f"Videos: [bold green]{len(ids)}[/]",
        border_style="cyan",
    ))

    ok, skipped, failed = 0, 0, 0

    for idx, vid in enumerate(ids, 1):
        console.rule(f"[bold cyan][{idx}/{len(ids)}] {vid}")

        if not args.force and already_done(vid):
            console.print("[green]✓[/] Already preprocessed locally. Skipping.")
            skipped += 1
            progress[vid] = {"status": "skipped_already_done", "timestamp": time.time()}
            save_progress(progress)
            continue

        url = f"https://www.youtube.com/watch?v={vid}"
        cmd = [sys.executable, "main.py", "--url", url, "--skip-vision"]
        if args.force:
            cmd.append("--force")

        start = time.time()
        res = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
        elapsed = round(time.time() - start, 1)

        if res.returncode == 0:
            console.print(f"[bold green]✓ {vid} done in {elapsed}s[/]")
            ok += 1
            progress[vid] = {"status": "success", "elapsed_sec": elapsed, "timestamp": time.time()}
        else:
            tail = "\n".join(res.stderr.strip().splitlines()[-5:])
            console.print(f"[bold red]✗ {vid} failed:[/]\n{tail}")
            failed += 1
            progress[vid] = {"status": "error", "error": tail, "timestamp": time.time()}
        save_progress(progress)

    console.print(f"\n[bold green]Done.[/] ok={ok} skipped={skipped} failed={failed}\n")


if __name__ == "__main__":
    main()
