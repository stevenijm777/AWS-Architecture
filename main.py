#!/usr/bin/env python3
"""
main.py — Cloud Architecture Extractor Pipeline

Usage:
    python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
    python main.py --url "https://youtu.be/VIDEO_ID" --interval 15
    python main.py --url "..." --skip-vision   # skip Gemini (test mode)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ── Project imports ──────────────────────────────────────────
from config.settings import (
    FRAME_INTERVAL_SEC,
    FRAMES_DIR,
    GRAPHS_DIR,
    RAW_DIR,
)
from scripts.downloader import download_video
from scripts.extractor import extract_audio, extract_keyframes
from scripts.transcriber import transcribe, get_timestamped_segments
from scripts.graph_builder import (
    create_graph_from_cloudscape_json,
    export_graphml,
    export_yed_graphml,
    print_graph_summary,
)

console = Console()


def run_pipeline(
    url: str,
    interval: int = FRAME_INTERVAL_SEC,
    skip_vision: bool = False,
    language: str | None = None,
) -> Path:
    """
    Execute the full extraction pipeline:

    1. Download video & metadata
    2. Extract audio (WAV 16 kHz mono)
    3. Extract keyframes (JPEG @ interval)
    4. Transcribe audio (Whisper on GPU)
    5. Analyze keyframes (Gemini Vision API)
    6. Build MultiDiGraph & export GraphML

    Returns the path to the exported .graphml file.
    """

    # ── Banner ───────────────────────────────────────────────
    console.print(Panel.fit(
        "[bold white]Cloud Architecture Extractor[/]\n"
        "[dim]YouTube → Whisper → Gemini → GraphML[/]",
        border_style="cyan",
    ))

    # ── Step 1: Download ─────────────────────────────────────
    console.rule("[bold cyan]Step 1 · Download Video")
    info = download_video(url)
    video_id = info.get("id", "unknown")
    title = info.get("title", "Untitled")
    video_path = RAW_DIR / f"{video_id}.mp4"

    # ── Step 2: Extract Audio ────────────────────────────────
    console.rule("[bold cyan]Step 2 · Extract Audio")
    audio_path = extract_audio(video_path)

    # ── Step 3: Extract Keyframes ────────────────────────────
    console.rule("[bold cyan]Step 3 · Extract Keyframes")
    frames_subdir = FRAMES_DIR / video_path.stem
    if frames_subdir.exists() and any(frames_subdir.glob("*.jpg")):
        frames = sorted(frames_subdir.glob("*.jpg"))
        console.print(
            f"[yellow]⚠[/] Keyframes already exist ({len(frames)} frames) in [bold]{frames_subdir}/[/]. Skipping extraction."
        )
    else:
        frames = extract_keyframes(video_path, interval_sec=interval)

    # ── Step 4: Transcribe ───────────────────────────────────
    console.rule("[bold cyan]Step 4 · Transcribe Audio (Whisper + GPU)")
    transcript_path = RAW_DIR / f"{video_id}_transcript.json"
    if transcript_path.exists():
        console.print(
            f"[yellow]⚠[/] Transcript already exists at [bold]{transcript_path}[/]. Skipping transcription."
        )
        with open(transcript_path, "r", encoding="utf-8") as f:
            segments = json.load(f)
    else:
        transcript_result = transcribe(audio_path, language=language)
        segments = get_timestamped_segments(transcript_result)

        # Save transcript to file
        transcript_path.write_text(
            json.dumps(segments, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        console.print(
            f"[green]✓[/] Transcript saved → [bold]{transcript_path}[/]"
        )

    # ── Step 5: Vision Analysis (Cloudscape schema) ─────────
    console.rule("[bold cyan]Step 5 · Analyze Keyframes (Gemini Vision)")
    analysis_path = RAW_DIR / f"{video_id}_vision_analysis.json"
    if skip_vision:
        console.print("[yellow]⚠  Skipping vision analysis (--skip-vision)[/]")
        analysis_result = {"graph": {}, "nodes": [], "edges": []}
    elif analysis_path.exists():
        console.print(
            f"[yellow]⚠[/] Vision analysis cache found at [bold]{analysis_path}[/]. Skipping Gemini API call."
        )
        with open(analysis_path, "r", encoding="utf-8") as f:
            analysis_result = json.load(f)
    else:
        from scripts.vision_analyzer import analyze_frame

        # Build transcript text from segments
        transcript_text = " ".join(
            s.get("text", "").strip() for s in segments
        )

        # Use the best whiteboard frame from second-layer filters if available,
        # otherwise fallback to the last frame.
        pizarra_dir = FRAMES_DIR / f"{video_id}_pizarra"
        best_tmpl_path = pizarra_dir / "best_whiteboard_template_transcript.jpg"
        best_occl_path = pizarra_dir / "best_whiteboard.jpg"
        
        best_frame = None
        if best_occl_path.exists():
            best_frame = best_occl_path
            console.print(f"[green]✓[/] Using best whiteboard frame (Occlusion): [bold]{best_frame.name}[/]")
        elif best_tmpl_path.exists():
            best_frame = best_tmpl_path
            console.print(f"[green]✓[/] Using best whiteboard frame (Template Matching): [bold]{best_frame.name}[/]")
        else:
            best_frame = frames[-1] if frames else None
            if best_frame:
                console.print(f"[yellow]⚠[/] No second-layer filtered frame found. Falling back to last frame: [bold]{best_frame.name}[/]")

        if best_frame:
            from scripts.symbol_detector import detect_symbols
            templates_dir = Path(__file__).resolve().parent / "data" / "templates"
            
            console.print(f"[dim]Running symbol detection on {best_frame.name}...[/]")
            try:
                # Use a threshold of 0.70 to be robust yet accurate
                detected_symbols = detect_symbols(
                    best_frame,
                    templates_dir,
                    transcript_text=transcript_text,
                    threshold=0.70
                )
                if detected_symbols:
                    console.print("[green]✓[/] Detected AWS symbols:")
                    for service, occurrences in sorted(detected_symbols.items()):
                        console.print(f"  • [bold cyan]{service}[/]: {len(occurrences)} occurrence(s)")
                else:
                    console.print("[dim]  No AWS symbols detected via template matching.[/]")
            except Exception as e:
                console.print(f"[yellow]⚠ Symbol detection failed: {e}[/]")
                detected_symbols = None

            analysis_result = analyze_frame(
                best_frame,
                transcript=transcript_text,
                video_url=url,
                detected_symbols=detected_symbols,
            )
        else:
            analysis_result = {"graph": {}, "nodes": [], "edges": []}

        # Save raw analysis for debugging
        analysis_path.write_text(
            json.dumps(analysis_result, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        console.print(
            f"[green]✓[/] Analysis saved → [bold]{analysis_path}[/]"
        )

    # ── Step 6: Build Graph (Cloudscape-compatible) ──────────
    console.rule("[bold cyan]Step 6 · Build Graph & Export GraphML")
    G = create_graph_from_cloudscape_json(
        analysis_result,
        video_id=video_id,
        video_url=url,
    )

    graphml_path = export_graphml(G, video_id)
    try:
        export_yed_graphml(G, video_id)
    except Exception as e:
        console.print(f"[yellow]⚠ Failed to export visual GraphML:[/] {e}")
    print_graph_summary(G)

    # ── Step 7: Compare with Ground Truth (if available) ─────
    gt_path = Path("data/cloudscape_gt") / f"{video_id}.graphml"
    if gt_path.exists():
        console.rule("[bold cyan]Step 7 · Compare with Ground Truth")
        from scripts.graph_builder import compare_with_ground_truth
        compare_with_ground_truth(G, gt_path)

    # ── Summary ──────────────────────────────────────────────
    _print_summary(video_id, title, frames, segments, [analysis_result], graphml_path)

    return graphml_path


def _print_summary(
    video_id: str,
    title: str,
    frames: list,
    segments: list,
    analysis_results: list,
    graphml_path: Path,
) -> None:
    """Print a final results table."""
    table = Table(title="Pipeline Results", border_style="cyan", show_lines=True)
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="green")

    table.add_row("Video ID", video_id)
    table.add_row("Title", title[:60])
    table.add_row("Keyframes Extracted", str(len(frames)))
    table.add_row("Transcript Segments", str(len(segments)))
    table.add_row("Frames Analyzed", str(len(analysis_results)))

    total_nodes = sum(len(r.get("nodes", [])) for r in analysis_results)
    total_edges = sum(len(r.get("edges", [])) for r in analysis_results)
    table.add_row("Total Nodes Found", str(total_nodes))
    table.add_row("Total Edges Found", str(total_edges))
    table.add_row("GraphML Output", str(graphml_path))

    console.print()
    console.print(table)
    console.print()


# ── CLI ──────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract AWS cloud architectures from YouTube videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url "https://www.youtube.com/watch?v=abc123"
  python main.py --url "https://youtu.be/abc123" --interval 15
  python main.py --url "..." --skip-vision --lang en
        """,
    )
    parser.add_argument(
        "--url", required=True,
        help="YouTube video URL",
    )
    parser.add_argument(
        "--interval", type=int, default=FRAME_INTERVAL_SEC,
        help=f"Keyframe extraction interval in seconds (default: {FRAME_INTERVAL_SEC})",
    )
    parser.add_argument(
        "--skip-vision", action="store_true",
        help="Skip Gemini vision analysis (useful for testing download/transcription)",
    )
    parser.add_argument(
        "--lang", default=None,
        help="Audio language hint for Whisper (e.g. 'en', 'es'). Auto-detect if omitted.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        output = run_pipeline(
            url=args.url,
            interval=args.interval,
            skip_vision=args.skip_vision,
            language=args.lang,
        )
        console.print(f"\n[bold green]🎉 Done![/] GraphML → {output}\n")
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user.[/]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[bold red]✗ Pipeline failed:[/] {e}")
        sys.exit(1)
