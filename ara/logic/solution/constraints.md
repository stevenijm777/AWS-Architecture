# 🚧 System Constraints & Operational Boundaries

## 1. Supported Input Regime

- **Video Format**: Standard MP4 videos from YouTube (*AWS This is My Architecture* series).
- **Resolution**: Minimum 720p (1280x720) for clear icon recognition.
- **Language**: Presentations in English (Whisper speech recognition tuned for English terms).
- **Video Duration**: Technical presentations between 2 minutes and 12 minutes.

## 2. Explicit Exclusion Criteria & Manual Overrides

The pipeline automatically skips or flags videos under the following conditions:
1. **Non-English Audio**: Videos spoken in Spanish, French, Italian, or Japanese (e.g. `CsD5bmM6mpY`, `7dtomip_VXc`) are excluded to avoid transcript misalignment.
2. **Compilation / Spotlight Episodes**: Videos exceeding 12 minutes or containing keywords like *"spotlight"*, *"greatest hits"*, *"bloopers"*, or *"reprise"* are excluded because they aggregate multiple separate architectures rather than a single diagram.
3. **Severe Permanent Occlusion & Manual Whiteboard Curation**: If a presenter never steps away from the whiteboard throughout the entire video ($O(f_t) > 50\%$ for all keyframes), or if keyframes were part of hidden/edge-case batches during initial selector calibration, the best frame is manually curated and placed directly into `data/good_whiteboard/`.
   - **Rationale & Future Work**: To prevent modifying or overfitting the calibrated automatic selector algorithm (`scripts/pizarra_filter.py` / `frame_selector.py`)—which could distort previously benchmarked results—these 51 manually curated whiteboards are registered as manual overrides. Enhancing the automatic selector to handle these edge cases without manual intervention is designated as Future Work.

## 3. Hardware & API Quotas

- **GPU Memory**: Local Whisper transcription requires CUDA GPU with $\ge 6\text{ GB}$ VRAM.
- **Gemini API Limits**: API calls must observe TPM/RPM rate limits; local keyframe pre-processing `--skip-vision` is supported to run offline stages prior to batch vision evaluation.
