import os
import glob
import time
import subprocess
import json
import shutil
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
from rich.console import Console

# Parse GraphML to retrieve metadata
def parse_graphml_info(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        ns = {'': 'http://graphml.graphdrawing.org/xmlns'}
        title, link = None, None
        
        graph_elem = root.find('.//graph', ns)
        if graph_elem is not None:
            for data in graph_elem.findall('data', ns):
                key = data.get('key')
                if key == 'd0':
                    title = data.text
                elif key == 'd1':
                    link = data.text
        return title, link
    except Exception:
        return None, None

def get_candidates():
    gt_dir = "/home/stemjara/Projects/AWS-Architecture/scratch/Cloudscape/data/graphs"
    processed_dir = "/home/stemjara/Projects/AWS-Architecture/data/graphs"
    csv_path = "/home/stemjara/Projects/AWS-Architecture/videos.csv"
    
    if not os.path.exists(csv_path):
        return []
        
    df = pd.read_csv(csv_path)
    df['clean_title'] = df['title'].str.strip().str.lower()
    
    processed_ids = set()
    if os.path.exists(processed_dir):
        for f in os.listdir(processed_dir):
            if f.endswith('.graphml'):
                processed_ids.add(f[:-8])
                
    gt_files = glob.glob(os.path.join(gt_dir, "*.graphml"))
    candidates = []
    
    for gt_file in gt_files:
        video_id = os.path.basename(gt_file)[:-8]
        title, link = parse_graphml_info(gt_file)
        if not title and not link:
            continue
            
        extracted_id = video_id
        if link and "v=" in link:
            extracted_id = link.split("v=")[1].split("&")[0]
            
        if extracted_id in processed_ids or video_id in processed_ids:
            continue
            
        title_lower = title.strip().lower() if title else ""
        row = df[df['clean_title'] == title_lower]
        if row.empty and title:
            row = df[df['clean_title'].str.contains(title_lower[:20], na=False)]
            
        age = "unknown"
        if not row.empty:
            age = row.iloc[0]['age']
            
        candidates.append({
            'video_id': extracted_id,
            'title': title or (row.iloc[0]['title'] if not row.empty else "Unknown Title"),
            'url': link or f"https://www.youtube.com/watch?v={extracted_id}",
            'age': age,
            'gt_path': gt_file
        })
        
    # Keep only those > 2 years old
    valid_ages = ["hace 3 años", "hace 4 años", "hace 5 años", "hace 6 años"]
    return [c for c in candidates if c['age'] in valid_ages]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process batch to scale up to 150 videos")
    parser.add_argument(
        "--force", action="store_true",
        help="Force execution, ignoring caches"
    )
    parser.add_argument(
        "--force-vision", action="store_true",
        help="Force vision analysis, reusing transcripts"
    )
    parser.add_argument(
        "--skip-vision", action="store_true",
        help="Skip Gemini vision analysis (local processing only)"
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Limit the number of videos to process in this run"
    )
    args = parser.parse_args()

    console = Console()
    console.print("[bold green]Starting batch process to scale up to 150 videos...[/bold green]")
    
    progress_file = Path("data/batch_progress.json")
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    
    processed_in_this_run = []
    if progress_file.exists():
        try:
            with open(progress_file, "r") as f:
                processed_in_this_run = json.load(f)
            console.print(f"Resuming batch. Already processed in previous run attempt: {len(processed_in_this_run)} videos.")
        except Exception:
            pass
            
    processed_set = set(processed_in_this_run)
    
    # Check current overall count
    processed_dir = Path("data/graphs")
    total_processed = 0
    if processed_dir.exists():
        total_processed = len([f for f in os.listdir(processed_dir) if f.endswith('.graphml')])
        
    target = 150
    needed = target - total_processed
    
    if needed <= 0:
        console.print(f"[bold green]Already reached the target! Total processed: {total_processed}[/bold green]")
        return
        
    console.print(f"Total processed currently: {total_processed}. Needed to reach target: {needed}")
    
    candidates = get_candidates()
    console.print(f"Available candidates: {len(candidates)}")
    
    # Filter candidates that are not already processed in this batch
    candidates = [c for c in candidates if c['video_id'] not in processed_set]
    
    if len(candidates) < needed:
        console.print(f"[yellow]Warning: Only {len(candidates)} candidates available. Processing all of them.[/yellow]")
        needed = len(candidates)
        
    selected_candidates = candidates[:needed]
    if args.limit is not None:
        selected_candidates = selected_candidates[:args.limit]
        needed = len(selected_candidates)
        
    console.print(f"Selected {len(selected_candidates)} candidates for processing.")
    
    consecutive_failures = 0
    
    for i, video in enumerate(selected_candidates):
        video_id = video["video_id"]
        title = video["title"]
        age = video["age"]
        url = video["url"]
        gt_path = Path(video["gt_path"])
        
        console.print(f"\n[bold magenta]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold magenta]")
        console.print(f"[bold cyan][{i+1}/{needed}] Batch Progress: Processing {video_id}[/bold cyan]")
        console.print(f"Title: {title}")
        console.print(f"Age: {age} | URL: {url}")
        
        # 1. Copy Ground Truth
        dst_gt = Path(f"data/cloudscape_gt/{video_id}.graphml")
        dst_gt.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy(gt_path, dst_gt)
            console.print(f"  ✓ Ground Truth copied to {dst_gt}")
        except Exception as e:
            console.print(f"  [yellow]⚠ Failed to copy Ground Truth: {e}[/yellow]")
            
        # 2. Run pipeline with exponential backoff retry for rate limits/failures
        retries = 3
        backoff = 10
        success = False
        
        for attempt in range(retries):
            console.print(f"  Attempt {attempt+1}/{retries} running pipeline...")
            t0 = time.time()
            
            cmd = [".venv/bin/python", "main.py", "--url", url]
            if args.force:
                cmd.append("--force")
            elif args.force_vision:
                cmd.append("--force-vision")
            if args.skip_vision:
                cmd.append("--skip-vision")

            proc = subprocess.run(cmd, capture_output=True, text=True)
            elapsed = time.time() - t0
            
            if proc.returncode == 0:
                console.print(f"  [green]✓ Attempt {attempt+1} succeeded in {elapsed:.1f}s.[/green]")
                success = True
                break
            else:
                console.print(f"  [red]✗ Attempt {attempt+1} failed in {elapsed:.1f}s. Return code: {proc.returncode}[/red]")
                
                # Check for quota error in output
                output_str = proc.stdout + "\n" + proc.stderr
                if "RESOURCE_EXHAUSTED" in output_str or "429" in output_str or "quota" in output_str.lower():
                    console.print(f"  [yellow]Quota / rate limit hit. Backing off for {backoff} seconds...[/yellow]")
                else:
                    console.print(f"  [yellow]General failure. Retrying in {backoff} seconds...[/yellow]")
                    
                time.sleep(backoff)
                backoff *= 2  # Double backoff duration
                
        if success:
            processed_in_this_run.append(video_id)
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(processed_in_this_run, f, indent=2)
            consecutive_failures = 0
            
            # Copy selected best whiteboard frame to data/un_processed for manual review
            src_whiteboard = Path(f"data/frames/{video_id}_pizarra/best_whiteboard.jpg")
            if src_whiteboard.exists():
                dst_dir = Path("data/un_processed")
                dst_dir.mkdir(parents=True, exist_ok=True)
                dst_whiteboard = dst_dir / f"{video_id}.jpg"
                try:
                    shutil.copy2(src_whiteboard, dst_whiteboard)
                    console.print(f"  ✓ Copied whiteboard to {dst_whiteboard} for manual review")
                except Exception as e:
                    console.print(f"  [red]✗ Failed to copy whiteboard to unprocessed directory: {e}[/red]")
            else:
                console.print(f"  [yellow]⚠ No best_whiteboard.jpg found at {src_whiteboard}[/yellow]")
        else:
            console.print(f"  [red]✗ Failed to process {video_id} after {retries} attempts. Skipping to next video.[/red]")
            # Mark as processed so we don't get stuck on it next time
            processed_in_this_run.append(video_id)
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(processed_in_this_run, f, indent=2)
                
            consecutive_failures += 1
            if consecutive_failures >= 3:
                console.print(f"  [red]✗ {consecutive_failures} consecutive video failures. Stopping batch to prevent API blocks.[/red]")
                break
            continue
            
        # Delay between videos to avoid slamming the API
        console.print("  Waiting 5 seconds before next video...")
        time.sleep(5)
        
    # Final Summary
    final_processed = 0
    if processed_dir.exists():
        final_processed = len([f for f in os.listdir(processed_dir) if f.endswith('.graphml')])
    console.print(f"\n[bold green]Batch processing run completed. Total processed now: {final_processed} / 150[/bold green]\n")

if __name__ == "__main__":
    main()
