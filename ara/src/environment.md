# ⚙️ Physical Layer: Environment & Dependencies

## 1. Hardware & Operating System

- **OS**: Linux (Ubuntu 22.04 / Debian GNU/Linux)
- **GPU**: NVIDIA GPU with CUDA support ($\ge 6\text{ GB}$ VRAM) for local OpenAI Whisper inference
- **Python Version**: Python 3.10+

## 2. Core Python Dependencies (`requirements.txt`)

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `openai-whisper` | Latest / PyTorch CUDA | Local GPU speech recognition |
| `google-genai` | Latest | Multimodal Gemini Vision API client |
| `opencv-python` (`cv2`) | 4.x | Image processing, morphological filtering, dark pixel ratio, template matching |
| `networkx` | 3.x | Graph data structure (`MultiDiGraph`) and GraphML export |
| `yt-dlp` | Latest | Downloading YouTube videos and metadata |
| `pandas` | 2.x | Benchmark CSV parsing and metrics summary |
| `rich` | Latest | CLI logging, tables, and progress display |

## 3. System Tools

- **FFmpeg**: Required for audio extraction (16 kHz mono WAV) and video keyframe extraction (`fps=1/10`).

## 4. Pipeline Execution Commands

```bash
# Run local processing pipeline (download, audio extract, Whisper transcript, whiteboard selection)
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --skip-vision

# Run complete multimodal pipeline including Gemini Vision API
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```
