#!/usr/bin/env python3
"""
generate_comparison_plots.py — Generate comprehensive comparison plots between 
                               Standard Mode (v6corrected) and Parsimonious Mode
                               evaluated against Cloudscape Ground Truth (61 GT videos).
"""
from __future__ import annotations

import sys
import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

DATA_DIR = PROJECT_ROOT / "data"
STANDARD_DIR = DATA_DIR / "graphs"
PARSIMONIOUS_DIR = DATA_DIR / "graphs_parsimonious"
GT_DIR = DATA_DIR / "cloudscape_gt"
OUTPUT_DIR = PROJECT_ROOT / "graficas"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Catalog
catalog = load_services_catalog(GT_DIR / "services.csv")

def norm_permissive(svc):
    if not svc or svc == "?": return "Unknown"
    s = str(svc).strip()
    cap = catalog.get(s, {}).get("capability", "")
    if s.startswith("User") or cap == "User": return "User"
    if s.startswith("ThirdParty") or cap == "ThirdParty": return "ThirdParty"
    return s

def compute_prf1(inter, gen, gt):
    p = inter / gen if gen > 0 else 0.0
    r = inter / gt if gt > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1

def eval_permissive(g_gen, g_gt):
    gen_svcs = [norm_permissive(g_gen.nodes[n].get("service", "")) for n in g_gen.nodes()]
    gt_svcs = [norm_permissive(g_gt.nodes[n].get("service", "")) for n in g_gt.nodes()]
    gen_set, gt_set = set(gen_svcs), set(gt_svcs)
    _, _, node_f1 = compute_prf1(len(gen_set & gt_set), len(gen_set), len(gt_set))
    
    def extract_base_edges(G):
        edges = set()
        for u, v in G.edges():
            su = norm_permissive(G.nodes[u].get("service", ""))
            sv = norm_permissive(G.nodes[v].get("service", ""))
            if su and sv and su != "Unknown" and sv != "Unknown":
                edges.add(tuple(sorted([su, sv])))
        return edges
        
    gen_edges, gt_edges = extract_base_edges(g_gen), extract_base_edges(g_gt)
    _, _, edge_f1 = compute_prf1(len(gen_edges & gt_edges), len(gen_edges), len(gt_edges))
    return node_f1, edge_f1

def collect_evaluation_data():
    clean_files = sorted(list(STANDARD_DIR.glob("*.graphml")))
    eval_vids = [f.stem for f in clean_files if (GT_DIR / f"{f.stem}.graphml").exists()]
    
    records = []
    for vid in eval_vids:
        gt_path = GT_DIR / f"{vid}.graphml"
        g_gt = nx.read_graphml(gt_path)
        
        # Standard
        std_path = STANDARD_DIR / f"{vid}.graphml"
        g_std = nx.read_graphml(std_path)
        res_std_st = evaluate_pair(g_std, g_gt, vid, catalog)
        pm_std_nf1, pm_std_ef1 = eval_permissive(g_std, g_gt)
        
        records.append({
            "video_id": vid,
            "model": "v6 Standard",
            "strict_node_f1": res_std_st["svc_f1"] * 100,
            "strict_edge_f1": res_std_st["edge_f1"] * 100,
            "permissive_node_f1": pm_std_nf1 * 100,
            "permissive_edge_f1": pm_std_ef1 * 100,
        })
        
        # Parsimonious
        pars_path = PARSIMONIOUS_DIR / f"{vid}.graphml"
        if pars_path.exists():
            g_pars = nx.read_graphml(pars_path)
            res_pars_st = evaluate_pair(g_pars, g_gt, vid, catalog)
            pm_pars_nf1, pm_pars_ef1 = eval_permissive(g_pars, g_gt)
            
            records.append({
                "video_id": vid,
                "model": "Parsimonious",
                "strict_node_f1": res_pars_st["svc_f1"] * 100,
                "strict_edge_f1": res_pars_st["edge_f1"] * 100,
                "permissive_node_f1": pm_pars_nf1 * 100,
                "permissive_edge_f1": pm_pars_ef1 * 100,
            })
            
    return pd.DataFrame(records)

def plot_all():
    df = collect_evaluation_data()
    print(f"Collected data for {len(df['video_id'].unique())} GT videos ({len(df)} rows).")
    
    # Custom styling
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 14,
        "figure.titlesize": 16,
        "font.family": "DejaVu Sans",
    })
    
    colors = {"v6 Standard": "#1f77b4", "Parsimonious": "#ff7f0e"}
    
    # ── PLOT 1: Global Performance Summary (Bar Chart) ──
    fig, ax = plt.subplots(figsize=(10, 6))
    
    avg_df = df.groupby("model")[["strict_node_f1", "strict_edge_f1", "permissive_node_f1", "permissive_edge_f1"]].mean().reset_index()
    melted = avg_df.melt(id_vars="model", var_name="Metric", value_name="F1 Score (%)")
    
    metric_labels = {
        "strict_node_f1": "Strict Node F1",
        "strict_edge_f1": "Strict Edge F1",
        "permissive_node_f1": "Permissive Node F1",
        "permissive_edge_f1": "Permissive Edge F1",
    }
    melted["Metric"] = melted["Metric"].map(metric_labels)
    
    sns.barplot(data=melted, x="Metric", y="F1 Score (%)", hue="model", palette=colors, ax=ax)
    ax.set_title("Overall Performance Comparison (Standard vs. Parsimonious)")
    ax.set_ylim(0, 105)
    ax.set_ylabel("Average F1 Score (%)")
    ax.set_xlabel("")
    
    # Annotate bars with exact percentages
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f"{height:.1f}%",
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=10, fontweight='bold',
                        xytext=(0, 3), textcoords='offset points')
                        
    plt.tight_layout()
    p1 = OUTPUT_DIR / "01_global_performance_comparison.png"
    plt.savefig(p1, dpi=300)
    plt.close()
    print(f"✓ Saved {p1.name}")
    
    # ── PLOT 2: Box Plot Distributions ──
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Nodes boxplot
    melted_nodes = df.melt(id_vars=["video_id", "model"], value_vars=["strict_node_f1", "permissive_node_f1"],
                           var_name="Metric", value_name="F1 Score (%)")
    melted_nodes["Metric"] = melted_nodes["Metric"].map({"strict_node_f1": "Strict Node F1", "permissive_node_f1": "Permissive Node F1"})
    sns.boxplot(data=melted_nodes, x="Metric", y="F1 Score (%)", hue="model", palette=colors, ax=axes[0], showmeans=True)
    axes[0].set_title("Node F1 Score Distribution")
    axes[0].set_ylim(0, 105)
    
    # Edges boxplot
    melted_edges = df.melt(id_vars=["video_id", "model"], value_vars=["strict_edge_f1", "permissive_edge_f1"],
                           var_name="Metric", value_name="F1 Score (%)")
    melted_edges["Metric"] = melted_edges["Metric"].map({"strict_edge_f1": "Strict Edge F1", "permissive_edge_f1": "Permissive Edge F1"})
    sns.boxplot(data=melted_edges, x="Metric", y="F1 Score (%)", hue="model", palette=colors, ax=axes[1], showmeans=True)
    axes[1].set_title("Edge F1 Score Distribution")
    axes[1].set_ylim(0, 105)
    
    plt.tight_layout()
    p2 = OUTPUT_DIR / "02_score_distribution_boxplot.png"
    plt.savefig(p2, dpi=300)
    plt.close()
    print(f"✓ Saved {p2.name}")

    # ── PLOT 3: Scatter Plot Node F1 vs Edge F1 ──
    fig, ax = plt.subplots(figsize=(9, 7))
    
    sns.scatterplot(
        data=df,
        x="strict_node_f1",
        y="strict_edge_f1",
        hue="model",
        style="model",
        s=90,
        alpha=0.8,
        palette=colors,
        ax=ax
    )
    
    # Diagonal reference line
    ax.plot([0, 100], [0, 100], "--", color="gray", alpha=0.5, label="1:1 Ratio")
    ax.set_title("Node F1 vs. Edge F1 Score (Per-Video Mapping)")
    ax.set_xlabel("Strict Node F1 Score (%)")
    ax.set_ylabel("Strict Edge F1 Score (%)")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 105)
    ax.legend(title="Model / Approach")
    
    plt.tight_layout()
    p3 = OUTPUT_DIR / "03_node_vs_edge_f1_scatter.png"
    plt.savefig(p3, dpi=300)
    plt.close()
    print(f"✓ Saved {p3.name}")

    # ── PLOT 4: Per-video Node & Edge F1 Comparison (Top 25 Videos Horizontal Bar Chart) ──
    pivot_df = df.pivot(index="video_id", columns="model", values=["strict_node_f1", "strict_edge_f1", "permissive_node_f1", "permissive_edge_f1"])
    pivot_df.columns = ['_'.join(c) for c in pivot_df.columns]
    
    # Filter top 25 GT videos for clean visualization
    sample_vids = pivot_df.head(25).index
    sub_df = df[df["video_id"].isin(sample_vids)]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 10), sharey=True)
    
    sns.barplot(data=sub_df, y="video_id", x="strict_node_f1", hue="model", palette=colors, ax=axes[0])
    axes[0].set_title("Strict Node F1 Score by Video (Sample 25 Videos)")
    axes[0].set_xlabel("Strict Node F1 (%)")
    axes[0].set_ylabel("Video ID")
    
    sns.barplot(data=sub_df, y="video_id", x="strict_edge_f1", hue="model", palette=colors, ax=axes[1])
    axes[1].set_title("Strict Edge F1 Score by Video (Sample 25 Videos)")
    axes[1].set_xlabel("Strict Edge F1 (%)")
    axes[1].set_ylabel("")
    
    plt.tight_layout()
    p4 = OUTPUT_DIR / "04_per_video_f1_comparison.png"
    plt.savefig(p4, dpi=300)
    plt.close()
    print(f"✓ Saved {p4.name}")

    # ── PLOT 5: Radar Chart for Multi-Metric Evaluation ──
    labels = ["Strict Node F1", "Strict Edge F1", "Permissive Node F1", "Permissive Edge F1"]
    num_vars = len(labels)
    
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    
    for model_name in ["v6 Standard", "Parsimonious"]:
        m_data = avg_df[avg_df["model"] == model_name].iloc[0]
        stats = [
            m_data["strict_node_f1"],
            m_data["strict_edge_f1"],
            m_data["permissive_node_f1"],
            m_data["permissive_edge_f1"],
        ]
        stats += stats[:1]
        
        ax.plot(angles, stats, color=colors[model_name], linewidth=2, label=model_name)
        ax.fill(angles, stats, color=colors[model_name], alpha=0.15)
        
    ax.set_yticklabels(["20%", "40%", "60%", "80%", "100%"], color="grey", size=9)
    ax.set_ylim(0, 100)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=11, fontweight="bold")
    ax.set_title("Multi-Metric Radar Comparison", y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
    
    plt.tight_layout()
    p5 = OUTPUT_DIR / "05_radar_multimetric_comparison.png"
    plt.savefig(p5, dpi=300)
    plt.close()
    print(f"✓ Saved {p5.name}")

if __name__ == "__main__":
    plot_all()
