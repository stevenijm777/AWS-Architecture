#!/usr/bin/env python3
"""
build_report_data.py — Consolidate every ablation run into one JSON for the report.

Each run directory holds its own `run.json`; nothing aggregates them, so answering
"how did variant X do on the 16 new videos" meant re-deriving it by hand every time.
This walks all of them once and emits `reports/ablation_report_data.json` with the
per-variant metrics, the 14/16/30 split, the edge-volume figures the panel is
actually diagnosed by, and the per-video detail.

Usage
-----
    .venv/bin/python scripts/ablation/build_report_data.py
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

import networkx as nx  # noqa: E402

from scripts.core.graph_builder import create_graph_from_cloudscape_json  # noqa: E402

GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
OUT = PROJECT_ROOT / "reports" / "ablation_report_data.json"


def mean(rows, key):
    return round(100 * sum(r[key] for r in rows) / len(rows), 2) if rows else None


def graph_stats(rows):
    """Edge volume, bidirectionality and actor count — the diagnostics the F1 hides."""
    pairs = bidi = actors = 0
    for r in rows:
        G = create_graph_from_cloudscape_json(r["analysis"], video_id=r["video_id"])
        und = {}
        for u, v in G.edges():
            a = G.nodes[u].get("service", "?")
            b = G.nodes[v].get("service", "?")
            und.setdefault(tuple(sorted((a, b))), set()).add((a, b))
        pairs += len(und)
        bidi += sum(1 for s in und.values() if len(s) == 2)
        actors += sum(1 for _, at in G.nodes(data=True)
                      if at.get("service", "").startswith("User"))
    return {
        "gen_edges": sum(r["gen_edges"] for r in rows),
        "gt_edges": sum(r["gt_edges"] for r in rows),
        "connected_pairs": pairs,
        "bidirectional_pairs": bidi,
        "pct_bidirectional": round(100 * bidi / pairs, 1) if pairs else 0.0,
        "user_actors": actors,
    }


def main() -> None:
    variants, panel14, panel16 = [], None, None

    for rj in sorted(glob.glob(str(PROJECT_ROOT / "reports/ablation/*/run.json"))):
        d = json.load(open(rj))
        if "panel30" in rj:                      # the hybrid, superseded by the clean run
            continue
        sp, m = d["stage2_prompt"], d["metrics"]
        ok = [r for r in d["results"] if r["status"] == "success"]
        n = len(ok)
        if n not in (14, 30):
            continue

        vids = d["video_ids"]
        if n == 30 and panel14 is None:
            panel14, panel16 = vids[:14], vids[14:]

        connev = bool(d.get("connection_evidence_enabled"))
        entry = {
            "name": sp["name"].replace("STAGE2_", ""),
            "cell": sp.get("source_cell"),
            "sha": sp["sha256"][:12],
            "file": sp["file"],
            "is_production": bool(sp.get("matches_production")) and not connev,
            "connection_evidence": connev,
            "panel": n,
            "dir": str(Path(rj).parent.relative_to(PROJECT_ROOT)),
            "svc_f1": m["service_f1_mean"],
            "edge_f1": m["edge_f1_mean"],
        }

        if n == 30:
            first14 = [r for r in ok if r["video_id"] in vids[:14]]
            last16 = [r for r in ok if r["video_id"] in vids[14:]]
            entry["split"] = {
                "p14": {"svc_f1": mean(first14, "svc_f1"), "edge_f1": mean(first14, "edge_f1"),
                        **graph_stats(first14)},
                "p16": {"svc_f1": mean(last16, "svc_f1"), "edge_f1": mean(last16, "edge_f1"),
                        **graph_stats(last16)},
                "p30": {"svc_f1": m["service_f1_mean"], "edge_f1": m["edge_f1_mean"],
                        **graph_stats(ok)},
            }
            entry["videos"] = [{
                "video_id": r["video_id"],
                "svc_f1": round(100 * r["svc_f1"], 1),
                "edge_f1": round(100 * r["edge_f1"], 1),
                "gen_nodes": r["gen_nodes"], "gt_nodes": r["gt_nodes"],
                "gen_edges": r["gen_edges"], "gt_edges": r["gt_edges"],
            } for r in ok]

        variants.append(entry)

    # ground truth reference for the two sub-panels
    def gt_ref(vids):
        n_nodes = n_edges = n_actors = pairs = bidi = 0
        for v in vids:
            g = nx.read_graphml(str(GT_DIR / f"{v}.graphml"))
            n_nodes += g.number_of_nodes()
            n_edges += g.number_of_edges()
            n_actors += sum(1 for _, a in g.nodes(data=True)
                            if a.get("service", "").startswith("User"))
            und = {}
            for u, w in g.edges():
                a = g.nodes[u].get("service", "?")
                b = g.nodes[w].get("service", "?")
                und.setdefault(tuple(sorted((a, b))), set()).add((a, b))
            pairs += len(und)
            bidi += sum(1 for s in und.values() if len(s) == 2)
        return {"nodes": n_nodes, "edges": n_edges, "user_actors": n_actors,
                "connected_pairs": pairs, "bidirectional_pairs": bidi,
                "pct_bidirectional": round(100 * bidi / pairs, 1) if pairs else 0.0}

    def video_meta(vids):
        out = []
        for v in vids:
            g = nx.read_graphml(str(GT_DIR / f"{v}.graphml"))
            out.append({"video_id": v, "gt_nodes": g.number_of_nodes(),
                        "gt_edges": g.number_of_edges(),
                        "name": g.graph.get("name", "")[:70]})
        return out

    payload = {
        "panel14": video_meta(panel14),
        "panel16": video_meta(panel16),
        "gt": {"p14": gt_ref(panel14), "p16": gt_ref(panel16),
               "p30": gt_ref(panel14 + panel16)},
        "variants": variants,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    n30 = sum(1 for v in variants if v["panel"] == 30)
    print(f"✓ {OUT.relative_to(PROJECT_ROOT)} — {n30} variantes a 30, "
          f"{sum(1 for v in variants if v['panel'] == 14)} a 14")


if __name__ == "__main__":
    main()
