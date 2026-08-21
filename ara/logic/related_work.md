# 📚 Related Work & Baseline Benchmarks

## 1. The FAST25 Cloudscape Ground Truth Benchmark

The primary benchmark for evaluating cloud architecture diagram extraction is the **FAST25 Cloudscape Ground Truth** dataset (`data/cloudscape_gt/`). 

- **Structure**: Contains hand-curated GraphML representations for over 150 *AWS This is My Architecture* video presentations.
- **Node Attributes**: Each node defines standard AWS service categories (e.g., `Lambda`, `S3`, `DynamoDB`, `EC2`, `API Gateway`), specific instance names, and functional notes.
- **Edge Attributes**: Edges define directed data/control flows with `flow_id`, sequence numbers (`seq`), and flow types (`data` vs `meta`).

Prior works evaluated against Cloudscape relied on rule-based heuristic OCR or single-frame vision prompts, which struggled with presenter occlusion and arrow parsing.

## 2. Diagram & Software Architecture Extraction in Literature

1. **Heuristic OCR & Template Matching**: Early computer vision approaches matched template icons using normalized cross-correlation (NCC) or SIFT/SURF descriptors. While effective for clean static images, they fail on physical whiteboard drawings with reflections, markers, and variable lighting.
2. **Multimodal LLMs for Visual Reasoning**: Recent multimodal models (such as GPT-4V and Gemini 1.5/3.6 Vision) demonstrate strong zero-shot reasoning on visual diagrams. However, without strict epistemic guardrails and domain-specific prompting, these models frequently hallucinate non-existent connections or ungrounded actor entities.
3. **Speech-Visual Cross-Modal Grounding**: Fusing spoken narration with visual keyframes has proven successful in instructional video understanding. Our work extends this paradigm to formal software architecture extraction by integrating Whisper audio transcriptions with adaptive vision preprocessing.
