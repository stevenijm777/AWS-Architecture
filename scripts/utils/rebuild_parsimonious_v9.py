#!/usr/bin/env script
"""
rebuild_parsimonious_v9.py — Rebuild clean v9 graphs from raw cache.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path
import networkx as nx

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Fix Windows console encoding issues for Unicode characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from scripts.core.graph_builder import create_graph_from_cloudscape_json, export_graphml, load_valid_services

def main():
    provenance_csv = PROJECT_ROOT / "reports" / "parsimonious_provenance.csv"
    if not provenance_csv.exists():
        print(f"❌ Provenance audit file not found: {provenance_csv}. Please run audit_parsimonious_provenance.py first.")
        sys.exit(1)
        
    raw_dir = PROJECT_ROOT / "data" / "raw"
    output_dir = PROJECT_ROOT / "data" / "graphs_parsimonious_v9"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    valid_services = load_valid_services()
    
    # Load v9 targets
    v9_ids = []
    skipped_ids = []
    
    with open(provenance_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vid = row["video_id"]
            verdict = row["verdict"]
            if verdict in ("v9_confirmado", "v9_probable"):
                v9_ids.append(vid)
            else:
                skipped_ids.append((vid, verdict))
                
    print(f"Loaded {len(v9_ids)} targets for v9 rebuild.")
    print(f"Skipping {len(skipped_ids)} targets (not marked as v9).")
    
    generated_count = 0
    failed_rebuild_count = 0
    missing_cache_count = 0
    
    rebuilt_results = []
    
    for vid in v9_ids:
        cache_path = raw_dir / f"{vid}_vision_analysis_parsimonious.json"
        if not cache_path.exists():
            print(f"⚠ Cache file missing for {vid}: {cache_path}")
            missing_cache_count += 1
            continue
            
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            url = f"https://www.youtube.com/watch?v={vid}"
            G = create_graph_from_cloudscape_json(data, video_id=vid, video_url=url)
            
            # Export using export_graphml (guarantees atomic writes)
            export_graphml(G, vid, output_dir=output_dir)
            generated_count += 1
            rebuilt_results.append((vid, True, None))
        except Exception as e:
            print(f"❌ Failed to rebuild graph for {vid}: {e}")
            failed_rebuild_count += 1
            rebuilt_results.append((vid, False, str(e)))
            
    # Verify Acceptance Criteria
    print("\n======================================================================")
    print(" VERIFYING ACCEPTANCE CRITERIA ON GENERATED GRAPHS")
    print("======================================================================")
    
    generated_files = list(output_dir.glob("*.graphml"))
    
    failures = []
    unknown_services_all = set()
    unknown_services_count = 0
    
    for gf in generated_files:
        vid = gf.stem
        size = gf.stat().st_size
        
        # 1. Check size > 0
        if size == 0:
            failures.append(f"{vid}.graphml: Size is 0 bytes")
            continue
            
        try:
            # 2. Check parsing
            G = nx.read_graphml(str(gf))
            
            # 3. Check link is correct
            link = G.graph.get("link", "")
            expected_link = f"https://www.youtube.com/watch?v={vid}"
            if link != expected_link:
                failures.append(f"{vid}.graphml: Link is '{link}' but expected '{expected_link}'")
                
            # 4. Check services outside catalog
            for node, attrs in G.nodes(data=True):
                svc = attrs.get("service", "")
                if svc:
                    svc_lower = svc.lower()
                    if svc_lower not in valid_services:
                        unknown_services_count += 1
                        unknown_services_all.add(svc)
                        failures.append(f"{vid}.graphml node [{node}]: Unknown service '{svc}'")
                    elif valid_services[svc_lower] != svc:
                        unknown_services_count += 1
                        unknown_services_all.add(f"{svc} (expected: {valid_services[svc_lower]})")
                        failures.append(f"{vid}.graphml node [{node}]: Casing mismatch for '{svc}' (expected '{valid_services[svc_lower]}')")
                    
        except Exception as e:
            failures.append(f"{vid}.graphml: Failed to parse: {e}")
            
    print(f"Total files checked in graphs_parsimonious_v9/: {len(generated_files)}")
    print(f"Files with size > 0:                         {len([f for f in generated_files if f.stat().st_size > 0])}")
    print(f"Files parsing successfully:                  {len(generated_files) - len([f for f in failures if 'parse' in f])}")
    print(f"Total unknown services instances found:      {unknown_services_count}")
    if unknown_services_all:
        print(f"Unknown services list:                       {sorted(list(unknown_services_all))}")
        
    print("\n======================================================================")
    print(" REBUILD COMPLETE SUMMARY")
    print("======================================================================")
    print(f"Rebuilt and exported successfully: {generated_count}")
    print(f"Failed during rebuild process:     {failed_rebuild_count}")
    print(f"Skipped due to missing raw cache:  {missing_cache_count}")
    print(f"Skipped because they are v10:      {len(skipped_ids)}")
    print(f"Exclusion IDs list (first 10):     {[vid for vid, _ in skipped_ids[:10]]} ...")
    print(f"Validation failures count:         {len(failures)}")
    if failures:
        print("First 5 failures:")
        for f in failures[:5]:
            print(f"  • {f}")
    else:
        print("✓ All acceptance criteria met perfectly!")
    print("======================================================================")

if __name__ == "__main__":
    main()
