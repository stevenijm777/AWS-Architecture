# 🧪 Falsifiable Claims

---

### Claim C01: Multimodal Audio-Visual Fusion Mitigates Visual Service Omits

- **Statement**: Fusing timestamped speech transcriptions with selected visual keyframes reduces service node omission by providing linguistic context for partially obscured or stylized architectural icons.
- **Conditions**: Applies to technical presentation videos in English where speakers explicitly mention service names; invalid if audio is silent or unaligned.
- **Status**: Validated
- **Falsification criteria**: Fails if vision-only keyframe analysis yields higher or equal Service Recall compared to fused audio-visual analysis across a benchmark set of videos.
- **Proof**: Verified by Experiment [E01](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/experiments.md#e01) and recorded in [Table 1](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table1_parsimonious_vs_standard.md).
- **Sources**:
  - `data/` metrics report: `[result]` [reporte_comparacion_detallada.md](file:///home/stemjara/Projects/AWS-Architecture/reporte_comparacion_detallada.md#L4) «Parsimonious supera a Standard por 15.7%»

---

### Claim C02: Morphological Opening and Dark-Pixel Ratio Isolation Eliminates Presenter Occlusion

- **Statement**: Combining an adaptive dark-pixel ratio threshold (75% of max dark pixels) with a 5x5 rectangular morphological opening pre-processing filter isolates discrete AWS service icon contours while removing thin drawing lines and presenter body occlusions.
- **Conditions**: Evaluated on glass whiteboard recordings with dark backgrounds; uncalibrated on light magnetic whiteboards or digital slides.
- **Status**: Validated
- **Falsification criteria**: Fails if standard fixed-threshold contour extraction selects keyframes with >25% presenter body occlusion area in the central ROI.
- **Proof**: Verified by Experiment [E01](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/experiments.md#e01) and implementation in [pizarra_occlusion_filter.py](file:///home/stemjara/Projects/AWS-Architecture/scripts/pizarra_occlusion_filter.py#L20-L40).
- **Sources**:
  - Code reference: `[input]` [pizarra_occlusion_filter.py](file:///home/stemjara/Projects/AWS-Architecture/scripts/pizarra_occlusion_filter.py#L55) «columnas_bloqueadas = media_columnas > 55.0»

---

### Claim C03: Parsimonious Prompt Constraints Eliminate Spurious User Nodes and Over-connected Edges

- **Statement**: Constraining the vision-language prompt to require explicit visual evidence for actor/user nodes and prohibiting assumed bidirectional return paths eliminates recurring "ghost" actor nodes and spurious edge over-connection without sacrificing overall Service F1 accuracy.
- **Conditions**: Tested on Gemini Vision API (temperature 0.1); applicable to structured JSON generation schemas.
- **Status**: Validated
- **Falsification criteria**: Fails if parsimonious prompting drops Service F1 score by more than 5% on average compared to unconstrained baseline prompts.
- **Proof**: Verified by Experiment [E02](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/experiments.md#e02) and documented in [Table 1](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table1_parsimonious_vs_standard.md).
- **Sources**:
  - Handoff analysis: `[result]` [handoff_notes.md](file:///home/stemjara/Projects/AWS-Architecture/handoff_notes.md#L74) «UserCompanyDeveloper alucinado 15 veces»

---

### Claim C04: Permissive Graph Alignment Metrics Decouple Nomenclature Differences from Structural Topology

- **Statement**: Evaluating extracted graphs using permissive service category matching (e.g. mapping `Lambda` vs `Lambda Function`) isolates true graph topological errors from harmless naming discrepancies, providing a realistic assessment of pipeline performance against Ground Truth.
- **Conditions**: Ground truth comparison requires canonical AWS service category mappings.
- **Status**: Validated
- **Falsification criteria**: Fails if strict vs. permissive evaluation metrics diverge unpredictably without strong correlation to node category alias mappings.
- **Proof**: Verified by Experiment [E03](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/experiments.md#e03) and recorded in [Table 2](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table2_strict_vs_permissive.md).
- **Sources**:
  - Analysis HTML: `[result]` [evaluacion_estricta_vs_permisiva.html](file:///home/stemjara/Projects/AWS-Architecture/evaluacion_estricta_vs_permisiva.html)
