---
title: "Multimodal AI Agent Framework for Automated Extraction and Verification of Cloud Architecture Graphs from Video Demonstrations"
authors:
  - "Steven Jara"
year: 2026
domain: "Multimodal AI, Software Architecture Extraction, Graph Neural Networks, Agentic Workflows"
keywords:
  - "Cloud Architecture Extraction"
  - "Multimodal LLMs"
  - "AWS This is My Architecture"
  - "GraphML"
  - "Whisper Speech Recognition"
  - "Keyframe Occlusion Filtering"
  - "Agentic Research Artifact"
claims_summary:
  C01: "Multimodal fusion of Whisper transcriptions and adaptive keyframes outperforms vision-only extraction by reducing service hallucination by 24%."
  C02: "Adaptive dark-pixel thresholding and morphological opening effectively eliminate presenter occlusion and connection arrow noise for AWS icon isolation."
  C03: "Parsimonious prompt engineering prevents spurious edge over-connection and ghost user node creation while maintaining equal or higher Service F1 scores."
  C04: "Permissive graph evaluation accurately decouples nomenclature variance from structural topology mismatches against the FAST25 Ground Truth benchmark."
abstract: |
  Extracting software architecture diagrams from unstructured technical video demonstrations—such as AWS's "This is My Architecture" series—presents a major challenge due to presenter occlusion, drawing noise, speech-visual mismatch, and ambiguous edge flows. Traditional OCR and heuristics fail under real-world video dynamics. In this work, we present an end-to-end autonomous agentic framework that extracts structured yEd-compatible GraphML diagrams directly from video URLs. Our framework combines local GPU-accelerated OpenAI Whisper audio transcription with an adaptive vision pre-processing pipeline (incorporating dark-pixel ratio thresholding and morphological opening) to isolate optimal whiteboard frames. We feed these fused representations into a multimodal agent powered by Gemini Vision with parsimonious prompting constraints. Evaluated against the FAST25 Ground Truth benchmark (Cloudscape dataset), our system demonstrates high Precision and Recall across service nodes and connectivity flows, significantly mitigating node hallucination and edge over-connection.
---

# 🔬 Agent-Native Research Artifact: Cloud Architecture Extractor

> **Artifact Root Manifest & Layer Index**  
> *This artifact provides complete epistemic traceability, linking every scientific claim to declarative experiment plans, raw empirical evidence, physical environment specifications, and exploration DAGs.*

---

## 🗂️ Layer Index

### 🧠 1. Cognitive Layer (`logic/`)
- [**Problem Formulation**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/problem.md) — *Research gap, task definition, and epistemic motivation.*
- [**Falsifiable Claims (`claims.md`)**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/claims.md) — *Rigorous, testable assertions (C01–C04) with proof pointers.*
- [**Declarative Experiments (`experiments.md`)**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/experiments.md) — *Experimental setups and verification procedures (E01–E03).*
- [**Solution Architecture**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/solution/architecture.md) — *7-stage agent pipeline DAG and system design.*
- [**Algorithms & Mathematical Formulations**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/solution/algorithm.md) — *Adaptive occlusion scoring and morphological opening math.*
- [**Boundary Constraints**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/solution/constraints.md) — *System limitations, resolution boundaries, and exclusion rules.*
- [**Related Work & Baseline**](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/related_work.md) — *FAST25 Cloudscape GT dataset and prior diagram extraction methods.*

### ⚙️ 2. Physical Layer (`src/`)
- [**Environment Specification (`environment.md`)**](file:///home/stemjara/Projects/AWS-Architecture/ara/src/environment.md) — *Hardware (CUDA, GPU), dependencies (Whisper, OpenCV, Gemini API, NetworkX).*

### 🌳 3. Exploration Graph (`trace/`)
- [**Exploration DAG (`exploration_tree.yaml`)**](file:///home/stemjara/Projects/AWS-Architecture/ara/trace/exploration_tree.yaml) — *Complete research trajectory including dead-end nodes, rejected hypotheses, and parameter iterations.*

### 📊 4. Evidence Layer (`evidence/`)
- [**Evidence Ledger & Overview (`README.md`)**](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/README.md) — *Complete index of quantitative evaluation tables and visual comparison reports.*
- [**Parsimonious vs. Standard Evaluation Table**](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table1_parsimonious_vs_standard.md) — *F1 performance across 62+ video evaluations.*
- [**Strict vs. Permissive Graph Metrics**](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table2_strict_vs_permissive.md) — *Service Precision, Recall, and Edge alignment metrics.*
