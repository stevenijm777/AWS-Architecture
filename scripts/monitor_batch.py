#!/usr/bin/env python3
"""
monitor_batch.py — Quick CLI to check live progress of the v6 standard batch extraction.
"""
import json
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
GRAPHS_DIR = DATA_DIR / "graphs"
PROGRESS_FILE = DATA_DIR / "batch_v6_progress.json"
PARSIMONIOUS_DIR = DATA_DIR / "graphs_parsimonious"

def main():
    total_target = len(list(PARSIMONIOUS_DIR.glob("*.graphml"))) if PARSIMONIOUS_DIR.exists() else 118
    completed_graphs = len(list(GRAPHS_DIR.glob("*.graphml"))) if GRAPHS_DIR.exists() else 0

    progress_data = {}
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                progress_data = json.load(f)
        except Exception:
            pass

    successes = sum(1 for v in progress_data.values() if v.get("status") == "success")
    errors = sum(1 for v in progress_data.values() if v.get("status") == "error")
    pct = round((completed_graphs / total_target) * 100, 1) if total_target > 0 else 0

    table = Table(title="📊 Status of Batch Processing (v6corrected)", border_style="cyan", show_lines=True)
    table.add_column("Metric", style="bold white")
    table.add_column("Value", style="bold green")

    table.add_row("Total Target Videos", str(total_target))
    table.add_row("Completed .graphml Files", f"{completed_graphs} / {total_target} ({pct}%)")
    table.add_row("Successful API Extractions", str(successes))
    table.add_row("Failed Extractions", f"[red]{errors}[/]" if errors > 0 else "0")

    console.print()
    console.print(table)

    if progress_data:
        recent = sorted(progress_data.items(), key=lambda x: x[1].get("timestamp", 0), reverse=True)[:5]
        console.print("\n[bold cyan]Latest 5 Processed Videos:[/]")
        for vid, info in recent:
            if info.get("status") == "success":
                nodes = info.get("nodes", 0)
                edges = info.get("edges", 0)
                sec = info.get("elapsed_sec", 0)
                console.print(f"  [green]✓[/] [bold]{vid}[/]: {nodes} nodes, {edges} edges ({sec}s)")
            else:
                err = info.get("error", "Unknown error")
                console.print(f"  [red]✗[/] [bold]{vid}[/]: {err}")
    console.print()

if __name__ == "__main__":
    main()
