"""
bulk_preprocess_local.py — Preprocess 50 new videos locally (no API calls, no graph builds).
"""
import json
import os
import subprocess
import sys
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

def count_remaining_to_preprocess(df: pd.DataFrame, raw_dir: Path, frames_dir: Path) -> tuple[int, int]:
    total_valid = 0
    preprocessed_count = 0
    for idx, row in df.iterrows():
        title = str(row["title"])
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
            continue

        total_valid += 1
        video_id = str(row["video_id"]).strip() if "video_id" in row and pd.notna(row["video_id"]) and str(row["video_id"]).strip() else None
        if not video_id:
            continue

        transcript_path = raw_dir / f"{video_id}_transcript.json"
        best_frame_path = frames_dir / f"{video_id}_pizarra" / "best_whiteboard.jpg"
        if transcript_path.exists() and best_frame_path.exists():
            preprocessed_count += 1

    remaining = total_valid - preprocessed_count
    return remaining, preprocessed_count

def main():
    df = pd.read_csv("videos.csv")
    raw_dir = Path("data/raw")
    frames_dir = Path("data/frames")

    preprocessed_count = 0
    limit = 1000

    rem_before, prev_done = count_remaining_to_preprocess(df, raw_dir, frames_dir)
    console.print(f"Iniciando procesamiento local masivo. Meta: {limit} videos (o todos los pendientes).")


    console.print(f"Videos procesados previamente: {prev_done} | Pendientes antes de iniciar: {rem_before}")

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
            console.print(f"[yellow]Saltando video especial/recopilación/largo: '{title}'[/]")
            continue

        console.print(f"\n[bold]Revisando video {idx+1}/{len(df)}: '{title}'[/]")

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
            console.print(f"[dim]→ El video {video_id} ya fue procesado localmente. Saltando.[/]")
            continue

        console.print(f"[cyan]→ Procesando {video_id} localmente (sin API)...[/]")
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
                console.print(f"[green]✓ Procesado localmente con éxito: {video_id}[/]")
                preprocessed_count += 1
                console.print(f"Progreso en este lote: {preprocessed_count}/{limit} completados.")
            else:
                console.print(f"[red]✗ Error al procesar {video_id}: {res.stderr.strip()}[/]")
        except Exception as e:
            console.print(f"[red]✗ Error al ejecutar comando para {video_id}: {e}[/]")

    rem_after, total_done = count_remaining_to_preprocess(df, raw_dir, frames_dir)
    console.print(f"\n[bold green]✓ Procesamiento por lote finalizado![/]")
    console.print(f"Videos procesados en este lote: {preprocessed_count}")
    console.print(f"Total de videos procesados localmente: {total_done}")
    console.print(f"[bold yellow]Faltan {rem_after} videos por procesar de esta manera.[/]")

if __name__ == "__main__":
    main()

