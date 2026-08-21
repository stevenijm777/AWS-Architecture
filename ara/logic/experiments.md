# 🔬 Declarative Experiment Plans

---

### Experiment E01: Frame Selection and Occlusion Filter Ablation

- **Verifies**: [C01](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/claims.md#claim-c01-multimodal-audio-visual-fusion-mitigates-visual-service-omits), [C02](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/claims.md#claim-c02-morphological-opening-and-dark-pixel-ratio-isolation-eliminates-presenter-occlusion)
- **Setup**: A benchmark suite of YouTube videos from AWS *This is My Architecture*. We evaluate 4 frame selection strategies:
  1. Default last keyframe of video.
  2. Fixed dark-pixel ratio filter.
  3. Adaptive dark-pixel ratio + presenter central ROI occlusion score.
  4. Template matching combined with Whisper service transcript alignment.
- **Procedure**:
  1. Extract keyframes every 10 seconds via `ffmpeg`.
  2. Compute dark pixel area ratio and presenter body obstruction in the central 50% ROI.
  3. Apply 5x5 morphological opening filter to remove arrow connector noise.
  4. Run Gemini Vision API on the selected keyframe and compute Service Recall against Ground Truth.
- **Expected outcome**: Adaptive occlusion scoring + morphological opening isolates keyframes with minimal presenter blockage, yielding superior downstream graph extraction metrics.
- **Evidence**: [Table 1](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table1_parsimonious_vs_standard.md)

---

### Experiment E02: Prompt Parsimony vs. Standard Baseline Evaluation

- **Verifies**: [C03](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/claims.md#claim-c03-parsimonious-prompt-constraints-eliminate-spurious-user-nodes-and-over-connected-edges)
- **Setup**: Evaluated across 62+ benchmark videos using two prompt configurations:
  1. *Standard V6 Prompt*: Generates graph representation with implied return paths and unconstrained user node instantiation.
  2. *Parsimonious Prompt*: Explicitly forbids hallucinated user nodes (`UserCompanyDeveloper`, `UserConsumerWebMobile`) without direct visual/audio evidence, and enforces strict directional flow rules.
- **Procedure**:
  1. Process identical pre-selected keyframes and Whisper transcripts through Gemini Vision under both prompt variants.
  2. Convert JSON output to NetworkX MultiDiGraph and export standard GraphML.
  3. Calculate Service F1, Edge F1, and count spurious node occurrences.
- **Expected outcome**: Parsimonious prompt significantly reduces spurious node hallucinations and over-connected edges while maintaining comparable or higher Service F1 accuracy.
- **Evidence**: [Table 1](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table1_parsimonious_vs_standard.md)

---

### Experiment E03: Strict vs. Permissive Graph Alignment Evaluation

- **Verifies**: [C04](file:///home/stemjara/Projects/AWS-Architecture/ara/logic/claims.md#claim-c04-permissive-graph-alignment-metrics-decouple-nomenclature-differences-from-structural-topology)
- **Setup**: Evaluates generated GraphML representations against Cloudscape Ground Truth files using two evaluation modes:
  1. *Strict Evaluation*: Requires exact string matching for AWS service names and node attributes.
  2. *Permissive Evaluation*: Uses canonical AWS service category normalization and alias mapping tables.
- **Procedure**:
  1. Compare generated MultiDiGraph nodes and edges against Ground Truth XML structures.
  2. Compute Precision, Recall, and F1 metrics under both evaluation modes.
- **Expected outcome**: Permissive evaluation decouples harmless naming variations from true structural topology errors.
- **Evidence**: [Table 2](file:///home/stemjara/Projects/AWS-Architecture/ara/evidence/tables/table2_strict_vs_permissive.md)
