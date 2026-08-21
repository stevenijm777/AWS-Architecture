# 🎯 Problem Formulation

## 1. Context & Motivation

AWS's *"This is My Architecture"* video series contains hundreds of technical presentations where cloud architects draw real-world system designs on physical glass whiteboards. These diagrams represent valuable, unstructured architectural knowledge. 

Manually converting these video demonstrations into formal, machine-readable software architecture representations (such as `.graphml` files for yEd or NetworkX) is labor-intensive and error-prone. The **FAST25 Cloudscape Ground Truth** dataset provided a human-curated benchmark of reference graphs for these videos, highlighting the urgent need for reliable, automated extraction pipelines.

## 2. Identified Research Gaps

Prior attempts to automate diagram extraction from technical video presentations faced critical challenges:

1. **Presenter Visual Occlusion**: Presenters continuously block icons, arrows, and text while drawing or speaking, leading vision algorithms to pick frames with partially drawn diagrams or heavy body obstruction.
2. **Visual Noise vs. Architectural Semantics**: Drawing lines, hand-written labels, and optical reflections on glass whiteboards cause standard OCR/object detection models to mistake connector lines for icons or create fragmented service nodes.
3. **Hallucination of Spurious Nodes and Over-Connection**: Unconstrained multimodal LLM prompts tend to infer "ghost" actor nodes (e.g., repeating `UserCompanyDeveloper` or `UserConsumerWebMobile` up to 15 times per graph) and create bidirectionally over-connected edges not supported by the video content.
4. **Speech-Vision Disconnect**: Relying solely on keyframes misses contextual cues spoken by architects during the video, while relying solely on audio lacks spatial topology.

## 3. Formal Problem Statement

Let $V$ be a technical video presentation of duration $T$, comprising visual frames $\{f_t\}_{t=0}^T$ and an audio stream $A$. 

Our goal is to construct an autonomous agent system $F(V, A) \to \hat{G}$ that produces a directed multi-graph $\hat{G} = (\hat{V}_G, \hat{E}_G)$ where:
- $\hat{V}_G$ is the set of extracted cloud service nodes $v_i = (\text{service\_type}, \text{custom\_label})$.
- $\hat{E}_G$ is the set of directed data flow or control edges $e_{ij} = (v_i, v_j, \text{flow\_id}, \text{sequence\_id}, \text{type})$.

The extracted graph $\hat{G}$ must be evaluated against the Ground Truth graph $G_{GT} = (V_{GT}, E_{GT})$ across **Service Precision/Recall/F1** and **Flow Precision/Recall/F1** under both strict and parsimonious matching protocols.
