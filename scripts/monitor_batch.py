#!/usr/bin/env python3
"""
monitor_batch.py — Live CLI monitor for Standard and Parsimonious batch extractions.
"""
import json
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GT_DIR = DATA_DIR / "cloudscape_gt"
STD_DIR = DATA_DIR / "graphs"
PARS_DIR = DATA_DIR / "graphs_parsimonious"
PARS_V10_DIR = DATA_DIR / "graphs_parsimonious_v10"

PROGRESS_STD = DATA_DIR / "batch_standard_missing_progress.json"
PROGRESS_PARS_V10 = DATA_DIR / "batch_parsimonious_v10_progress.json"
PROGRESS_V6_LEGACY = DATA_DIR / "batch_v6_progress.json"


def load_progress(file_path: Path) -> dict:
    if file_path.exists():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def main():
    gt_vids = set([f.stem for f in GT_DIR.glob("*.graphml")]) if GT_DIR.exists() else set()
    std_vids = set([f.stem for f in STD_DIR.glob("*.graphml")]) if STD_DIR.exists() else set()
    pars_vids = set([f.stem for f in PARS_DIR.glob("*.graphml")]) if PARS_DIR.exists() else set()
    pars_v10_vids = set([f.stem for f in PARS_V10_DIR.glob("*.graphml")]) if PARS_V10_DIR.exists() else set()

    intersection_vids = std_vids & pars_vids & gt_vids

    prog_std = load_progress(PROGRESS_STD)
    prog_v10 = load_progress(PROGRESS_PARS_V10)

    std_success = sum(1 for v in prog_std.values() if v.get("status") == "success")
    std_errors = sum(1 for v in prog_std.values() if v.get("status") == "error")

    v10_success = sum(1 for v in prog_v10.values() if v.get("status") == "success")
    v10_errors = sum(1 for v in prog_v10.values() if v.get("status") == "error")

    table = Table(title="📊 Live Status of Cloudscape Architecture Batch Processing", border_style="cyan", show_lines=True)
    table.add_column("Categoría / Métrica", style="bold white")
    table.add_column("Valor Actual", style="bold green")

    table.add_row("Cloudscape GT Dataset Total", f"{len(gt_vids)} vídeos Ground Truth")
    table.add_row("Standard Mode (.graphml en data/graphs)", f"{len(std_vids)} vídeos ({len(std_vids & gt_vids)} en GT)")
    table.add_row("Parsimonious Mode (.graphml en data/graphs_parsimonious)", f"{len(pars_vids)} vídeos ({len(pars_vids & gt_vids)} en GT)")
    table.add_row("Parsimonious v10 Refinado (.graphml en v10)", f"{len(pars_v10_vids)} vídeos")
    table.add_row("🎯 Evaluables Lado a Lado (Standard & Parsimonious & GT)", f"[bold cyan]{len(intersection_vids)} vídeos[/]")
    table.add_row("Batch Standard Reciente", f"Exitosos: {std_success} | Fallos: {std_errors}")
    table.add_row("Batch Parsimonious v10 Reciente", f"Exitosos: {v10_success} | Fallos: {v10_errors}")

    console.print()
    console.print(table)

    # Merge recent logs across progress files
    all_recent = []
    for vid, info in prog_std.items():
        all_recent.append((vid, info, "Standard"))
    for vid, info in prog_v10.items():
        all_recent.append((vid, info, "Parsimonious v10"))

    if all_recent:
        sorted_recent = sorted(all_recent, key=lambda x: x[1].get("timestamp", 0), reverse=True)[:8]
        console.print("\n[bold cyan]⏱️ Últimos 8 Vídeos Procesados en Vivo:[/]")
        for vid, info, mode in sorted_recent:
            if info.get("status") == "success":
                nodes = info.get("nodes", 0)
                edges = info.get("edges", 0)
                sec = info.get("elapsed_sec", 0)
                console.print(f"  [green]✓[/] [bold]{vid}[/] ({mode}): {nodes} nodos, {edges} aristas ({sec}s)")
            else:
                err = info.get("error", "Error desconocido")
                console.print(f"  [red]✗[/] [bold]{vid}[/] ({mode}): {err}")
    console.print()


if __name__ == "__main__":
    main()

