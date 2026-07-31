---
name: aws-architecture-pipeline
description: Standard operating procedures and rules for processing videos, running batch extractions, and evaluating AWS cloud architecture graphs without creating unnecessary scripts.
---

# AWS Architecture Extractor — Agent Operational Guide

This skill defines the mandatory workflow for AI agents when asked to process videos, run batch extractions, or evaluate architecture graphs in this repository.

> **CRITICAL RULE FOR AGENTS:**
> **DO NOT create temporary Python scripts, scratch batch files, or redefine pipeline code.**
> Use the official commands and scripts documented below.

---

## 1. Single Video Processing

To process a single YouTube video using Gemini Vision API:

```bash
# Standard Mode (data/graphs/<VIDEO_ID>.graphml)
GEMINI_MODEL=gemini-3-flash-preview .venv/bin/python main.py --url "https://www.youtube.com/watch?v=<VIDEO_ID>" --mode standard

# Parsimonious Mode (data/graphs_parsimonious/<VIDEO_ID>.graphml)
GEMINI_MODEL=gemini-3-flash-preview .venv/bin/python main.py --url "https://www.youtube.com/watch?v=<VIDEO_ID>" --mode parsimonious
```

*Flags:*
- `--skip-vision`: Runs local download, audio extraction, keyframe extraction, and frame selection without calling Gemini API.
- `--force-vision`: Forces Gemini to re-analyze the whiteboard image even if cached in `data/raw/`.

---

## 2. Batch Processing

Use the official batch runners located in `scripts/batch/`.

### A. Local Preprocessing (No API calls)
Preprocesses new videos locally (downloads audio/frames, transcribes with Whisper, and selects best whiteboard frame):
```bash
.venv/bin/python scripts/batch/bulk_preprocess_local.py
```

### B. Gemini Vision API Batch Processing
Processes missing videos using Gemini Vision API and exports GraphML files:

```bash
# Process 10 missing videos in Standard mode (default)
GEMINI_MODEL=gemini-3-flash-preview .venv/bin/python scripts/batch/process_batch_vision.py --mode standard --limit 10

# Process 10 missing videos in Parsimonious mode
GEMINI_MODEL=gemini-3-flash-preview .venv/bin/python scripts/batch/process_batch_vision.py --mode parsimonious --limit 10

# Continuous processing until all videos complete or API quota is exhausted
GEMINI_MODEL=gemini-3-flash-preview .venv/bin/python scripts/batch/process_batch_vision.py --mode standard --until-quota
```

---

## 3. Graph Evaluation

To evaluate generated graphs against Cloudscape ground truth:
```bash
.venv/bin/python scripts/utils/evaluate_graphs.py
```
*Reports are saved automatically to `data/reports/` and `data/reports/csv/`.*

---

## 4. Output Storage Locations

- Standard GraphML: `data/graphs/<VIDEO_ID>.graphml`
- Parsimonious GraphML: `data/graphs_parsimonious/<VIDEO_ID>.graphml`
- Raw Vision JSON: `data/raw/<VIDEO_ID>_vision_analysis.json`
- Reports & CSVs: `data/reports/` and `data/reports/csv/`

*Never save production outputs inside `whiteboard_selection_lab/`.*
