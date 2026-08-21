# 📊 Table 2: Strict vs. Permissive Graph Evaluation Metrics

**Source**: `[result]` [evaluacion_estricta_vs_permisiva.html](file:///home/stemjara/Projects/AWS-Architecture/evaluacion_estricta_vs_permisiva.html)

## Evaluation Protocol Comparison

| Evaluation Metric | Strict Protocol | Permissive Protocol | Delta / Impact |
| :--- | :---: | :---: | :--- |
| **Service Category Matching** | Exact string match (e.g. `Lambda` $\neq$ `Lambda Function`) | Alias dictionary mapping (`lambda_function` $\to$ `Lambda`) | Eliminates harmless naming mismatches |
| **Average Service Precision** | 78.4% | **91.2%** | **+12.8%** |
| **Average Service Recall** | 72.1% | **85.6%** | **+13.5%** |
| **Average Edge Flow F1** | 48.2% | **59.7%** | **+11.5%** |

## Summary Key Findings
1. Strict string evaluation penalizes systems for valid architectural synonyms (e.g., `Amazon S3` vs `S3 Bucket`).
2. Permissive category alignment decouples naming variations from topological graph structure, revealing true pipeline accuracy.
