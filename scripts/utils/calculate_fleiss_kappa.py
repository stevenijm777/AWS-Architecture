#!/usr/bin/env python3
"""
calculate_fleiss_kappa.py - Calculates Fleiss's Kappa coefficient to measure
agreement between human annotations (ground truth) and different AI pipelines.
"""

import sys
from pathlib import Path
import networkx as nx

# Add project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def compute_fleiss_kappa(matrix):
    """
    Computes Fleiss's Kappa for an agreement matrix.
    Each row in matrix represents a subject, and each column represents a category.
    The elements are counts of raters who assigned the subject to the category.
    """
    N = len(matrix)
    if N == 0:
        return 0.0
    m = sum(matrix[0])
    k = len(matrix[0])
    
    # 1. Compute p_j (proportion of all ratings assigned to category j)
    p = [0.0] * k
    for j in range(k):
        p[j] = sum(row[j] for row in matrix) / (N * m)
        
    # 2. Compute P_i (extent to which raters agree for subject i)
    P = [0.0] * N
    for i in range(N):
        numerator = sum(matrix[i][j]**2 for j in range(k)) - m
        P[i] = numerator / (m * (m - 1))
        
    # 3. Compute overall P and Pe
    P_mean = sum(P) / N
    Pe = sum(pj**2 for pj in p)
    
    if Pe >= 1.0:
        return 1.0
    return (P_mean - Pe) / (1.0 - Pe)

def get_video_services(folder_path: Path, video_id: str) -> set[str]:
    """Reads graphml and extracts unique AWS services."""
    path = folder_path / f"{video_id}.graphml"
    if not path.exists():
        return set()
    try:
        g = nx.read_graphml(str(path))
        return {g.nodes[n].get('service') for n in g.nodes() if g.nodes[n].get('service')}
    except Exception:
        return set()

def run_evaluation():
    # Identify video IDs present in all three directories
    gt_dir = project_root / "data" / "cloudscape_gt"
    std_dir = project_root / "data" / "graphs"
    pars_dir = project_root / "data" / "graphs_parsimonious"
    
    if not gt_dir.exists() or not std_dir.exists() or not pars_dir.exists():
        print("Error: One or more data directories (cloudscape_gt, graphs, graphs_parsimonious) do not exist.")
        return
        
    vids = sorted(
        set(f.stem for f in gt_dir.glob("*.graphml")) &
        set(f.stem for f in std_dir.glob("*.graphml")) &
        set(f.stem for f in pars_dir.glob("*.graphml"))
    )
    
    if not vids:
        print("No matching videos found across all three directories.")
        return
        
    # Load services catalog from graph_renderer/services.csv
    services_csv = project_root / "graph_renderer" / "services.csv"
    if not services_csv.exists():
        # fallback
        services_csv = project_root / "data" / "cloudscape_gt" / "services.csv"
        
    if not services_csv.exists():
        print(f"Error: services.csv not found at {services_csv}")
        return
        
    catalog = set()
    with open(services_csv, "r", encoding="utf-8") as f:
        # Simple parsing skipping header
        for line in f:
            line = line.strip()
            if not line:
                continue
            service = line.split(",")[0].strip()
            if service and service != "name":
                catalog.add(service)
                
    catalog = sorted(list(catalog))
    
    matrix = []
    for vid in vids:
        gt = get_video_services(gt_dir, vid)
        std = get_video_services(std_dir, vid)
        pars = get_video_services(pars_dir, vid)
        
        for s in catalog:
            ratings = [0, 0]  # [Absent, Present]
            for annotator in [gt, std, pars]:
                if s in annotator:
                    ratings[1] += 1
                else:
                    ratings[0] += 1
            matrix.append(ratings)
            
    kappa = compute_fleiss_kappa(matrix)
    
    # Interpretation
    if kappa > 0.80:
        interpretation = "Acuerdo casi perfecto (Altamente confiable)"
    elif kappa > 0.60:
        interpretation = "Acuerdo sustancial"
    elif kappa > 0.40:
        interpretation = "Acuerdo moderado"
    else:
        interpretation = "Acuerdo débil o pobre"
        
    print(f"\n================ Fleiss's Kappa Evaluation ================")
    print(f"Videos evaluados (intersección triple): {len(vids)}")
    print(f"Servicios evaluados del catálogo:       {len(catalog)}")
    print(f"Evaluadores (3):                        1. Ground Truth (Cloudscape)")
    print(f"                                        2. Gemini 2.5 Estándar")
    print(f"                                        3. Gemini 3.5 Parsimonioso")
    print(f"-----------------------------------------------------------")
    print(f"Fleiss's Kappa (K):                     {kappa:.4f}")
    print(f"Interpretación:                        {interpretation}")
    print(f"===========================================================\n")

if __name__ == "__main__":
    run_evaluation()
