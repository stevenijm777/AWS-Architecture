#!/usr/bin/env python3
"""
fix_parsimonious_titles.py — Align GraphML graph['name'] attribute with canonical video titles.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import networkx as nx

def main():
    workspace = Path(__file__).resolve().parent.parent
    data_dir = workspace / "data"
    
    # 1. Build canonical title mapping from Ground Truth first (most accurate)
    gt_dir = data_dir / "cloudscape_gt"
    canonical_titles = {}
    for f in gt_dir.glob("*.graphml"):
        try:
            G = nx.read_graphml(str(f))
            name = G.graph.get("name", "").strip()
            if name:
                canonical_titles[f.stem] = name
        except Exception:
            pass
            
    # 2. Augment/backup with video_id_cache.json
    cache_path = data_dir / "video_id_cache.json"
    if cache_path.exists():
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)
            for title, vid in cache.items():
                if vid not in canonical_titles and title.strip():
                    canonical_titles[vid] = title.strip()
        except Exception:
            pass
            
    # 3. Augment with raw/*.info.json
    raw_dir = data_dir / "raw"
    if raw_dir.exists():
        for f in raw_dir.glob("*.info.json"):
            vid = f.name.replace(".info.json", "")
            if vid not in canonical_titles:
                try:
                    with open(f, "r", encoding="utf-8") as file:
                        info = json.load(file)
                    title = info.get("title", info.get("fulltitle", "")).strip()
                    if title:
                        canonical_titles[vid] = title
                except Exception:
                    pass

    print(f"Loaded {len(canonical_titles)} canonical titles from metadata sources.")

    # 4. Update Parsimonious graphs
    pars_dir = data_dir / "graphs_parsimonious"
    updated_pars = 0
    if pars_dir.exists():
        for f in pars_dir.glob("*.graphml"):
            vid = f.stem
            if vid in canonical_titles:
                try:
                    G = nx.read_graphml(str(f))
                    old_name = G.graph.get("name", "")
                    new_name = canonical_titles[vid]
                    if old_name != new_name:
                        G.graph["name"] = new_name
                        nx.write_graphml(G, str(f))
                        updated_pars += 1
                except Exception as e:
                    print(f"Error updating parsimonious graph {f.name}: {e}")
                    
    print(f"Updated {updated_pars} Parsimonious graphs with canonical titles.")

    # 5. Update Standard graphs just in case they are mismatched
    std_dir = data_dir / "graphs"
    updated_std = 0
    if std_dir.exists():
        for f in std_dir.glob("*.graphml"):
            vid = f.stem
            if vid in canonical_titles:
                try:
                    G = nx.read_graphml(str(f))
                    old_name = G.graph.get("name", "")
                    new_name = canonical_titles[vid]
                    if old_name != new_name:
                        G.graph["name"] = new_name
                        nx.write_graphml(G, str(f))
                        updated_std += 1
                except Exception as e:
                    print(f"Error updating standard graph {f.name}: {e}")
                    
    print(f"Updated {updated_std} Standard graphs with canonical titles.")

if __name__ == "__main__":
    main()
