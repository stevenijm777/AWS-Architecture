#!/usr/bin/env python3
"""
generate_comparison_plots.py — Generate comprehensive comparison plots between
                               Standard Mode (v6corrected) and Parsimonious Mode
                               evaluated against Cloudscape Ground Truth.

Videos Cloudscape marks graph_usable=False are excluded from every plot, same
criterion as evaluate_standard.py / evaluate_parsimonious.py.
"""
from __future__ import annotations

import sys
import json
from collections import Counter
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

def permissive_missing_hallucinated(g_gen, g_gt):
    """Same set-diff methodology as evaluate_pair's services_missing/hallucinated,
    but on actor-superclass-normalized labels (User*, ThirdParty* collapsed)."""
    gen_set = {norm_permissive(g_gen.nodes[n].get("service", "")) for n in g_gen.nodes()}
    gt_set = {norm_permissive(g_gt.nodes[n].get("service", "")) for n in g_gt.nodes()}
    gen_set.discard("Unknown")
    gt_set.discard("Unknown")
    missing = sorted(gt_set - gen_set)
    hallucinated = sorted(gen_set - gt_set)
    return missing, hallucinated

def is_actor_label(svc: str) -> bool:
    """True for actor-superclass labels (User*/ThirdParty*), false for real AWS services."""
    s = str(svc).strip()
    cap = catalog.get(s, {}).get("capability", "")
    return s.startswith("User") or s.startswith("ThirdParty") or cap in ("User", "ThirdParty")

def collect_evaluation_data():
    """Returns (df, full_results). df has one row per (video, model) with the flat
    metrics used by most plots. full_results carries the complete evaluate_pair()
    dicts per model (incl. capability_breakdown), which don't fit cleanly in a
    DataFrame cell."""
    clean_files = sorted(list(STANDARD_DIR.glob("*.graphml")))
    eval_vids = [f.stem for f in clean_files if (GT_DIR / f"{f.stem}.graphml").exists()]

    records = []
    full_results = {"v6 Standard": [], "Parsimonious": []}
    for vid in eval_vids:
        gt_path = GT_DIR / f"{vid}.graphml"
        g_gt = nx.read_graphml(gt_path)

        # Standard
        std_path = STANDARD_DIR / f"{vid}.graphml"
        g_std = nx.read_graphml(std_path)
        res_std_st = evaluate_pair(g_std, g_gt, vid, catalog)

        # Cloudscape flags 56/396 of its own ground truths as unusable.
        if not res_std_st["graph_usable"]:
            continue

        pm_std_nf1, pm_std_ef1 = eval_permissive(g_std, g_gt)
        pm_std_missing, pm_std_halluc = permissive_missing_hallucinated(g_std, g_gt)

        records.append({
            "video_id": vid,
            "model": "v6 Standard",
            "strict_node_f1": res_std_st["svc_f1"] * 100,
            "strict_ms_f1": res_std_st["ms_f1"] * 100,
            "strict_edge_f1": res_std_st["edge_f1"] * 100,
            "permissive_node_f1": pm_std_nf1 * 100,
            "permissive_edge_f1": pm_std_ef1 * 100,
            "services_missing": res_std_st["services_missing"],
            "services_hallucinated": res_std_st["services_hallucinated"],
            "services_missing_permissive": pm_std_missing,
            "services_hallucinated_permissive": pm_std_halluc,
        })
        full_results["v6 Standard"].append(res_std_st)

        # Parsimonious
        pars_path = PARSIMONIOUS_DIR / f"{vid}.graphml"
        if pars_path.exists():
            g_pars = nx.read_graphml(pars_path)
            res_pars_st = evaluate_pair(g_pars, g_gt, vid, catalog)
            pm_pars_nf1, pm_pars_ef1 = eval_permissive(g_pars, g_gt)
            pm_pars_missing, pm_pars_halluc = permissive_missing_hallucinated(g_pars, g_gt)

            records.append({
                "video_id": vid,
                "model": "Parsimonious",
                "strict_node_f1": res_pars_st["svc_f1"] * 100,
                "strict_ms_f1": res_pars_st["ms_f1"] * 100,
                "strict_edge_f1": res_pars_st["edge_f1"] * 100,
                "permissive_node_f1": pm_pars_nf1 * 100,
                "permissive_edge_f1": pm_pars_ef1 * 100,
                "services_missing": res_pars_st["services_missing"],
                "services_hallucinated": res_pars_st["services_hallucinated"],
                "services_missing_permissive": pm_pars_missing,
                "services_hallucinated_permissive": pm_pars_halluc,
            })
            full_results["Parsimonious"].append(res_pars_st)

    return pd.DataFrame(records), full_results

def plot_all():
    df, full_results = collect_evaluation_data()
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
    fig, ax = plt.subplots(figsize=(7.5, 7))

    
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
    plt.savefig(p1, dpi=140)
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
    plt.savefig(p2, dpi=140)
    plt.close()
    print(f"✓ Saved {p2.name}")

    # ── PLOT 3: Scatter Plot Node F1 vs Edge F1 ──
    fig, ax = plt.subplots(figsize=(7.5, 7))

    
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
    plt.savefig(p3, dpi=140)
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
    plt.savefig(p4, dpi=140)
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
    plt.savefig(p5, dpi=140)
    plt.close()
    print(f"✓ Saved {p5.name}")

    # ── PLOT 6 & 7: Top Hallucinated / Missing Services (Standard vs Parsimonious) ──
    def top_service_counts(col: str, top_n: int = 10) -> pd.DataFrame:
        counts = {}
        for model_name in ["v6 Standard", "Parsimonious"]:
            services = [s for row in df.loc[df["model"] == model_name, col] for s in row]
            counts[model_name] = Counter(services)
        all_services = set(counts["v6 Standard"]) | set(counts["Parsimonious"])
        rows = [
            {"service": s, "v6 Standard": counts["v6 Standard"].get(s, 0),
             "Parsimonious": counts["Parsimonious"].get(s, 0)}
            for s in all_services
        ]
        ranked = pd.DataFrame(rows)
        ranked["total"] = ranked["v6 Standard"] + ranked["Parsimonious"]
        return ranked.sort_values("total", ascending=False).head(top_n)

    def plot_service_errors(col: str, title: str, filename: str) -> None:
        top = top_service_counts(col)
        if top.empty:
            print(f"  (sin datos para {filename}, se omite)")
            return
        melted = top.melt(id_vars="service", value_vars=["v6 Standard", "Parsimonious"],
                           var_name="model", value_name="Frecuencia")
        fig, ax = plt.subplots(figsize=(11, max(4, 0.5 * len(top))))
        sns.barplot(data=melted, y="service", x="Frecuencia", hue="model", palette=colors, ax=ax)
        ax.set_title(title, fontsize=13, wrap=True)
        ax.set_xlabel("Vídeos en los que ocurre")
        ax.set_ylabel("")
        ax.legend(title="Modelo")
        plt.tight_layout()
        p = OUTPUT_DIR / filename
        plt.savefig(p, dpi=140)
        plt.close()
        print(f"✓ Saved {p.name}")

    plot_service_errors(
        "services_hallucinated",
        "Top Servicios Alucinados por Modelo — Evaluación Estricta (inventados, no están en el GT)",
        "06_hallucinated_services.png",
    )
    plot_service_errors(
        "services_missing",
        "Top Servicios Faltantes por Modelo — Evaluación Estricta (presentes en el GT, no detectados)",
        "07_missing_services.png",
    )
    plot_service_errors(
        "services_hallucinated_permissive",
        "Top Servicios Alucinados por Modelo — Evaluación Permisiva (User*/ThirdParty* colapsados)",
        "08_hallucinated_services_permissive.png",
    )
    plot_service_errors(
        "services_missing_permissive",
        "Top Servicios Faltantes por Modelo — Evaluación Permisiva (User*/ThirdParty* colapsados)",
        "09_missing_services_permissive.png",
    )

    # ── PLOT 8: Total Error Volume — Strict vs Permissive ──
    # Does collapsing User*/ThirdParty* actor variants into two buckets actually
    # reduce the error count, and by how much, per model?
    totals = []
    for model_name in ["v6 Standard", "Parsimonious"]:
        sub = df[df["model"] == model_name]
        totals.append({"model": model_name, "modo": "Estricto", "tipo": "Alucinados",
                        "total": sum(len(x) for x in sub["services_hallucinated"])})
        totals.append({"model": model_name, "modo": "Permisivo", "tipo": "Alucinados",
                        "total": sum(len(x) for x in sub["services_hallucinated_permissive"])})
        totals.append({"model": model_name, "modo": "Estricto", "tipo": "Faltantes",
                        "total": sum(len(x) for x in sub["services_missing"])})
        totals.append({"model": model_name, "modo": "Permisivo", "tipo": "Faltantes",
                        "total": sum(len(x) for x in sub["services_missing_permissive"])})
    totals_df = pd.DataFrame(totals)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    mode_colors = {"Estricto": "#c0392b", "Permisivo": "#27ae60"}
    for ax, tipo in zip(axes, ["Alucinados", "Faltantes"]):
        sub = totals_df[totals_df["tipo"] == tipo]
        sns.barplot(data=sub, x="model", y="total", hue="modo", palette=mode_colors, ax=ax)
        ax.set_title(f"Total de Servicios {tipo}\n(suma de ocurrencias sobre {df['video_id'].nunique()} vídeos)")
        ax.set_xlabel("")
        ax.set_ylabel("Cantidad total de ocurrencias" if tipo == "Alucinados" else "")
        for p in ax.patches:
            h = p.get_height()
            if h > 0:
                ax.annotate(f"{int(h)}", (p.get_x() + p.get_width() / 2, h),
                            ha="center", va="bottom", fontsize=10, fontweight="bold",
                            xytext=(0, 3), textcoords="offset points")
        ax.legend(title="Evaluación")
    plt.suptitle("Efecto de la Evaluación Permisiva en el Volumen de Errores", fontweight="bold")
    plt.tight_layout()
    p10 = OUTPUT_DIR / "10_strict_vs_permissive_error_volume.png"
    plt.savefig(p10, dpi=140)
    plt.close()
    print(f"✓ Saved {p10.name}")

    # ── PLOT 9: Share of strict errors that are actor-label disagreements ──
    # Of everything counted as "hallucinated"/"missing" under strict evaluation,
    # how much is really an AWS service miss vs. just a User*/ThirdParty* actor
    # sub-type disagreement (which permissive evaluation absorbs)?
    breakdown = []
    for model_name in ["v6 Standard", "Parsimonious"]:
        sub = df[df["model"] == model_name]
        for tipo, col in [("Alucinados", "services_hallucinated"), ("Faltantes", "services_missing")]:
            all_items = [s for row in sub[col] for s in row]
            n_actor = sum(1 for s in all_items if is_actor_label(s))
            n_service = len(all_items) - n_actor
            breakdown.append({"model": model_name, "tipo": tipo, "categoria": "Etiqueta de actor (User*/ThirdParty*)", "total": n_actor})
            breakdown.append({"model": model_name, "tipo": tipo, "categoria": "Servicio AWS real", "total": n_service})
    breakdown_df = pd.DataFrame(breakdown)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
    cat_colors = {"Etiqueta de actor (User*/ThirdParty*)": "#8e44ad", "Servicio AWS real": "#2980b9"}
    for ax, tipo in zip(axes, ["Alucinados", "Faltantes"]):
        sub = breakdown_df[breakdown_df["tipo"] == tipo]
        pivot = sub.pivot(index="model", columns="categoria", values="total").reindex(["v6 Standard", "Parsimonious"])
        pivot = pivot[["Servicio AWS real", "Etiqueta de actor (User*/ThirdParty*)"]]
        pivot.plot(kind="bar", stacked=True, ax=ax, color=[cat_colors[c] for c in pivot.columns], legend=(tipo == "Alucinados"))
        ax.set_title(f"Composición de Errores Estrictos: {tipo}")
        ax.set_xlabel("")
        ax.set_ylabel("Cantidad total de ocurrencias" if tipo == "Alucinados" else "")
        ax.tick_params(axis="x", rotation=0)
        for i, model_name in enumerate(pivot.index):
            total = pivot.loc[model_name].sum()
            actor_pct = 100 * pivot.loc[model_name, "Etiqueta de actor (User*/ThirdParty*)"] / total if total else 0
            ax.annotate(f"{actor_pct:.0f}% actor", (i, total), ha="center", va="bottom", fontsize=10, fontweight="bold")
    plt.suptitle("¿De qué están hechos los errores estrictos? Actor vs. Servicio AWS real", fontweight="bold")
    plt.tight_layout()
    p11 = OUTPUT_DIR / "11_strict_error_composition.png"
    plt.savefig(p11, dpi=140)
    plt.close()
    print(f"✓ Saved {p11.name}")

    # ── PLOT 12 & 13: Recall + Error Distribution by Capability (per model) ──
    # Design lifted from whiteboard_selection_lab/evaluacion_avanzada.ipynb.
    def plot_capability_breakdown(results: list[dict], model_name: str, filename: str) -> None:
        cap_data: dict[str, dict[str, int]] = {}
        for r in results:
            for cap, vals in r.get("capability_breakdown", {}).items():
                a = cap_data.setdefault(cap, {"gt": 0, "correct": 0, "missed": 0, "hallucinated": 0})
                a["gt"] += vals.get("gt", 0)
                a["correct"] += vals.get("correct", 0)
                a["missed"] += vals.get("missed", 0)
                a["hallucinated"] += vals.get("hallucinated", 0)

        rows = []
        for cap, v in cap_data.items():
            gt, correct, missed, halluc = v["gt"], v["correct"], v["missed"], v["hallucinated"]
            recall = correct / gt if gt > 0 else 0.0
            precision = correct / (correct + halluc) if (correct + halluc) > 0 else 0.0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
            rows.append({"capability": cap, "gt": gt, "correct": correct, "missed": missed,
                         "hallucinated": halluc, "recall": recall, "f1": f1})
        dfc = pd.DataFrame(rows).sort_values("f1")
        if dfc.empty:
            print(f"  (sin datos de capability para {filename}, se omite)")
            return

        fig, axes = plt.subplots(1, 2, figsize=(15, max(5, 0.55 * len(dfc))))

        bar_colors = ["#e74c3c" if r < 0.5 else "#f39c12" if r < 0.8 else "#27ae60" for r in dfc["recall"]]
        axes[0].barh(dfc["capability"], dfc["recall"], color=bar_colors)
        axes[0].set_xlim(0, 1.08)
        axes[0].set_xlabel("Recall")
        axes[0].set_title(f"Recall por Capability — {model_name}\n(¿Qué tan bien encuentra cada tipo de servicio?)")
        for i, r in enumerate(dfc["recall"]):
            axes[0].text(r + 0.02, i, f"{r:.0%}", va="center", fontsize=10)

        axes[1].barh(dfc["capability"], dfc["correct"], color="#27ae60", label="Correct")
        axes[1].barh(dfc["capability"], dfc["missed"], left=dfc["correct"], color="#e74c3c", label="Missed")
        axes[1].barh(dfc["capability"], dfc["hallucinated"],
                      left=dfc["correct"] + dfc["missed"], color="#f39c12", label="Hallucinated")
        axes[1].set_xlabel("Count")
        axes[1].set_title(f"Distribución de Errores por Capability — {model_name}")
        axes[1].legend()

        plt.tight_layout()
        p = OUTPUT_DIR / filename
        plt.savefig(p, dpi=140)
        plt.close()
        print(f"✓ Saved {p.name}")

    plot_capability_breakdown(full_results["v6 Standard"], "v6 Standard", "12_capability_breakdown_standard.png")
    plot_capability_breakdown(full_results["Parsimonious"], "Parsimonious", "13_capability_breakdown_parsimonious.png")

    # ── PLOT 14 & 15: "Salud General" Boxplot (per model) ──
    # Same design/palette as graficas.ipynb's graficar_salud_general — Set2 palette
    # + stripplot overlay, the style explicitly preferred over the default one above.
    def plot_health_boxplot(sub_df: pd.DataFrame, model_name: str, filename: str) -> None:
        cols = {"strict_node_f1": "F1 Servicios\n(Básico)",
                "strict_ms_f1": "F1 Nodos\n(Multiset)",
                "strict_edge_f1": "F1 Aristas\n(Conexiones)"}
        order = list(cols.values())
        melted = sub_df[list(cols.keys())].rename(columns=cols).melt(var_name="Métrica", value_name="F1 Score (%)")

        fig, ax = plt.subplots(figsize=(9, 6.5))
        sns.boxplot(x="Métrica", y="F1 Score (%)", hue="Métrica", data=melted, order=order,
                    palette="Set2", width=0.5, legend=False, ax=ax)
        sns.stripplot(x="Métrica", y="F1 Score (%)", data=melted, order=order,
                      color=".25", size=5, alpha=0.5, ax=ax)
        ax.set_title(f"Salud General del Pipeline — {model_name}\nDistribución de F1-Scores (n={len(sub_df)})",
                     fontweight="bold")
        ax.set_ylim(-5, 105)
        ax.set_ylabel("Score (100 = Perfecto)")
        ax.set_xlabel("")

        plt.tight_layout()
        p = OUTPUT_DIR / filename
        plt.savefig(p, dpi=140)
        plt.close()
        print(f"✓ Saved {p.name}")

    plot_health_boxplot(df[df["model"] == "v6 Standard"], "v6 Standard", "14_health_boxplot_standard.png")
    plot_health_boxplot(df[df["model"] == "Parsimonious"], "Parsimonious", "15_health_boxplot_parsimonious.png")

    # ── PLOT 16 & 17: F1 Range Distribution Pie (per model) ──
    # Same buckets/colors as graficas.ipynb's graficar_distribucion_parsimonioso,
    # redesigned so labels don't overlap: no inline text on thin wedges, all
    # counts/percentages moved to an external legend instead.
    def plot_f1_distribution_pie(sub_df: pd.DataFrame, model_name: str, filename: str) -> None:
        def clasificar(score: float) -> str:
            if score >= 90: return "Excelente (≥90%)"
            elif score >= 70: return "Bueno (70-89%)"
            elif score >= 50: return "Aceptable (50-69%)"
            else: return "Bajo (<50%)"

        orden = ["Excelente (≥90%)", "Bueno (70-89%)", "Aceptable (50-69%)", "Bajo (<50%)"]
        colores = {"Excelente (≥90%)": "#2ecc71", "Bueno (70-89%)": "#f1c40f",
                   "Aceptable (50-69%)": "#e67e22", "Bajo (<50%)": "#e74c3c"}

        fig, axes = plt.subplots(1, 2, figsize=(15, 7))
        for ax, col, label in zip(axes, ["strict_node_f1", "strict_edge_f1"], ["Servicios", "Conexiones"]):
            counts = sub_df[col].apply(clasificar).value_counts().reindex(orden).fillna(0).astype(int)
            counts = counts[counts > 0]
            n = int(counts.sum())

            wedges, _, autotexts = ax.pie(
                counts, colors=[colores[c] for c in counts.index],
                autopct=lambda pct: f"{pct:.1f}%" if pct >= 3 else "",
                pctdistance=0.75, startangle=90, counterclock=False,
                wedgeprops=dict(edgecolor="white", linewidth=2),
            )
            for t in autotexts:
                t.set_fontweight("bold")
                t.set_fontsize(11)
                t.set_color("white")

            legend_labels = [f"{c} — {counts[c]} vídeos" for c in counts.index]
            ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5),
                       fontsize=10, frameon=False)
            ax.set_title(f"F1 {label} — {model_name} (N={n})", fontweight="bold")

        plt.tight_layout()
        p = OUTPUT_DIR / filename
        plt.savefig(p, dpi=140, bbox_inches="tight")
        plt.close()
        print(f"✓ Saved {p.name}")

    plot_f1_distribution_pie(df[df["model"] == "v6 Standard"], "v6 Standard", "16_f1_distribution_pie_standard.png")
    plot_f1_distribution_pie(df[df["model"] == "Parsimonious"], "Parsimonious", "17_f1_distribution_pie_parsimonious.png")


if __name__ == "__main__":
    plot_all()
