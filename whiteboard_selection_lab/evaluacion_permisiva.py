#!/usr/bin/env python3
"""
evaluacion_permisiva.py — Evaluador Permisivo para el whiteboard_selection_lab.

Realiza una evaluación permisiva de grafos generados contra Ground Truth:
1. Normalización Permisiva de Nodos:
   - Cualquier tipo de actor usuario (UserConsumerWeb, UserCompanyAgent, UserConsumerMobile, etc.)
     o servicio con capability 'User' se mapea genéricamente a 'User'.
   - Cualquier sistema externo/on-prem (ThirdParty, etc.) o capability 'ThirdParty' se mapea a 'ThirdParty'.
   - Los servicios AWS se mantienen exactos (ej. S3, EC2, Lambda).
2. Conectividad Base No Dirigida (Aristas Permisivas):
   - Evalúa si existe estructuralmente una conexión base no dirigida entre los servicios normalizados:
     (min(service_a, service_b), max(service_a, service_b)).
"""

import argparse
import csv
import json
import pandas as pd
import networkx as nx
from pathlib import Path
from collections import Counter
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LAB_DIR = Path(__file__).resolve().parent
GOOD_GT_DIR = PROJECT_ROOT / "data" / "cloudscape_gt"
SERVICES_CSV = GOOD_GT_DIR / "services.csv"
if not SERVICES_CSV.exists():
    SERVICES_CSV = PROJECT_ROOT / "data" / "services.csv"

BATCH_VIDEOS = [
    "-3lnf5lzsH0", "-kA0ahrhX3I", "-wLEkq21cvA", "07lfvavMdfU",
    "1aYoIZvabbk", "2L0m28ZLmtE", "2e3vOxsHekE", "6CgqEzyWpeA",
    "6EUknQqaV1w", "6YkguepAQuQ", "BZ32w0SSAoY", "Cgv0kfp_6xQ",
    "wjtSHyENv0I", "ww5fiygF6eg"
]


def load_services_catalog(csv_path: Path = SERVICES_CSV) -> dict[str, dict]:
    """Carga el catálogo de servicios AWS y actores desde services.csv."""
    catalog = {}
    if not csv_path.exists():
        return catalog
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                catalog[name] = {
                    "capability": row.get("capability", "").strip(),
                    "is_aws": row.get("is_aws", "").strip() == "True",
                }
    return catalog


CATALOG = load_services_catalog()


def normalize_service_permissive(svc: str) -> str:
    """
    Normaliza el nombre de un servicio para la evaluación permisiva:
    - Todos los actores 'User*' o capability 'User' -> 'User'
    - Todos los actores 'ThirdParty*' o capability 'ThirdParty' -> 'ThirdParty'
    - Otros servicios -> mantener su nombre real.
    """
    if not svc or svc == "?":
        return "Unknown"
    svc_str = str(svc).strip()
    cap = CATALOG.get(svc_str, {}).get("capability", "")
    
    if svc_str.startswith("User") or cap == "User":
        return "User"
    if svc_str.startswith("ThirdParty") or cap == "ThirdParty":
        return "ThirdParty"
    return svc_str


def compute_p_r_f1(inter_count: int, gen_count: int, gt_count: int) -> tuple[float, float, float]:
    p = inter_count / gen_count if gen_count > 0 else 0.0
    r = inter_count / gt_count if gt_count > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1


def evaluate_ultra_permissive_pair(gen_graph: nx.MultiDiGraph, gt_graph: nx.MultiDiGraph, video_id: str) -> dict[str, Any]:
    """
    Evalúa de forma permisiva un par (Grafo Generado, Grafo Ground Truth):
    - Permissive Node Matching (User / ThirdParty agrupados)
    - Permissive Base Connection Matching (Aristas no dirigidas entre servicios normalizados)
    """
    # Extraer nombres de servicios raw
    gen_raw_nodes = [gen_graph.nodes[n].get("service", "") for n in gen_graph.nodes()]
    gt_raw_nodes = [gt_graph.nodes[n].get("service", "") for n in gt_graph.nodes()]
    
    # Nodos normalizados permisivos
    gen_norm_nodes = [normalize_service_permissive(s) for s in gen_raw_nodes if s]
    gt_norm_nodes = [normalize_service_permissive(s) for s in gt_raw_nodes if s]
    
    # 1. Servicios Únicos Permisivos
    gen_norm_set = set(gen_norm_nodes)
    gt_norm_set = set(gt_norm_nodes)
    inter_set = gen_norm_set & gt_norm_set
    svc_p, svc_r, svc_f1 = compute_p_r_f1(len(inter_set), len(gen_norm_set), len(gt_norm_set))
    
    # 2. Servicios Multiset Permisivos
    c_gen = Counter(gen_norm_nodes)
    c_gt = Counter(gt_norm_nodes)
    inter_ms = sum((c_gen & c_gt).values())
    ms_p, ms_r, ms_f1 = compute_p_r_f1(inter_ms, len(gen_norm_nodes), len(gt_norm_nodes))
    
    # 3. Conexiones Base No Dirigidas Permisivas
    def extract_perm_base_edges(G: nx.MultiDiGraph) -> set[tuple[str, str]]:
        edges = set()
        for u, v in G.edges():
            su = normalize_service_permissive(G.nodes[u].get("service", ""))
            sv = normalize_service_permissive(G.nodes[v].get("service", ""))
            if su and sv and su != "Unknown" and sv != "Unknown":
                pair = tuple(sorted([su, sv]))
                edges.add(pair)
        return edges
        
    gen_base_edges = extract_perm_base_edges(gen_graph)
    gt_base_edges = extract_perm_base_edges(gt_graph)
    
    inter_edge = len(gen_base_edges & gt_base_edges)
    edge_p, edge_r, edge_f1 = compute_p_r_f1(inter_edge, len(gen_base_edges), len(gt_base_edges))
    
    return {
        "video_id": video_id,
        "gt_name": gt_graph.graph.get("name", f"Video {video_id}"),
        "gen_nodes": len(gen_raw_nodes),
        "gt_nodes": len(gt_raw_nodes),
        "perm_svc_precision": svc_p,
        "perm_svc_recall": svc_r,
        "perm_svc_f1": svc_f1,
        "perm_ms_f1": ms_f1,
        "perm_edge_precision": edge_p,
        "perm_edge_recall": edge_r,
        "perm_edge_f1": edge_f1,
        "gen_base_edges_count": len(gen_base_edges),
        "gt_base_edges_count": len(gt_base_edges),
        "services_correct": sorted(list(inter_set)),
        "services_missing": sorted(list(gt_norm_set - gen_norm_set)),
        "services_hallucinated": sorted(list(gen_norm_set - gt_norm_set)),
        "base_edges_correct": sorted([f"{a}<->{b}" for a, b in (gen_base_edges & gt_base_edges)]),
        "base_edges_missing": sorted([f"{a}<->{b}" for a, b in (gt_base_edges - gen_base_edges)]),
        "base_edges_hallucinated": sorted([f"{a}<->{b}" for a, b in (gen_base_edges - gt_base_edges)]),
    }


def run_evaluation(video_ids: list[str] = None) -> pd.DataFrame:
    if video_ids is None:
        video_ids = BATCH_VIDEOS
        
    results = []
    for vid in video_ids:
        gt_path = GOOD_GT_DIR / f"{vid}.graphml"
        gen_path = LAB_DIR / "lab_workspace" / vid / "test_graph.graphml"
        if not gen_path.exists():
            gen_path = PROJECT_ROOT / "data" / "graphs" / f"{vid}.graphml"
            
        if not gt_path.exists() or not gen_path.exists():
            print(f"⚠ Omitiendo {vid}: Falta GT o Grafo generado")
            continue
            
        g_gt = nx.read_graphml(str(gt_path))
        g_gen = nx.read_graphml(str(gen_path))
        
        res = evaluate_ultra_permissive_pair(g_gen, g_gt, vid)
        results.append(res)
        
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluador Permisivo de Grafos de Arquitectura")
    parser.add_argument("video_ids", nargs="*", default=[], help="IDs de videos a evaluar")
    args = parser.parse_args()
    
    vids = args.video_ids if args.video_ids else BATCH_VIDEOS
    print(f"🧪 Ejecutando Evaluación Permisiva sobre {len(vids)} videos...")
    
    df_res = run_evaluation(vids)
    
    print("\n" + "=" * 70)
    print("📊 RESULTADOS DE LA EVALUACIÓN PERMISIVA:")
    print("=" * 70)
    
    df_show = df_res.copy()
    for col in ["perm_svc_f1", "perm_ms_f1", "perm_edge_f1"]:
        df_show[col] = df_show[col].apply(lambda x: f"{x:.1%}")
        
    cols_to_print = ["video_id", "gen_nodes", "gt_nodes", "perm_svc_f1", "perm_ms_f1", "perm_edge_f1"]
    print(df_show[cols_to_print].to_string(index=False))
    
    print("\n" + "-" * 70)
    print(f"  • Promedio F1 Servicios Únicos Permisivos (perm_svc_f1):  {df_res['perm_svc_f1'].mean():.1%}")
    print(f"  • Promedio F1 Nodos Multiset Permisivos (perm_ms_f1):     {df_res['perm_ms_f1'].mean():.1%}")
    print(f"  • Promedio F1 Conectividad Base (perm_edge_f1):          {df_res['perm_edge_f1'].mean():.1%}")
    print("=" * 70)
    
    out_csv = LAB_DIR / "permissive_evaluation_summary.csv"
    df_res.to_csv(out_csv, index=False)
    print(f"\n✓ Resumen guardado en: {out_csv}")
