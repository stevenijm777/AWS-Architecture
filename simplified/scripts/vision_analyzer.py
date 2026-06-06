"""
vision_analyzer.py — Gemini API vision analysis of architecture keyframes
                     Outputs Cloudscape-compatible schema (FAST25 paper).
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai
from rich.console import Console

from config.settings import GEMINI_API_KEY, GEMINI_MODEL

console = Console()

# ── Gemini Client (lazy init) ────────────────────────────────
_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not set. Add it to your .env file."
            )
        _client = genai.Client(api_key=GEMINI_API_KEY)
        console.print("[green]✓[/] Gemini client initialised")
    return _client


# ── Cloudscape-compatible Prompt ─────────────────────────────

CLOUDSCAPE_PROMPT = """\
You are an expert AWS Solutions Architect. You are analyzing a whiteboard \
screenshot from an AWS "This is My Architecture" YouTube video, along with \
the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the \
Cloudscape dataset schema (FAST25 paper by Satija et al.).

## RULES:
1. Use SHORT AWS service names for `service` field: e.g. "S3", "Lambda", \
"EC2", "DynamoDB", "EKS", "CloudFront", "Aurora", "ElastiCache", "MSK", \
"SQS", "SNS", "ApiGateway", "Pinpoint", "KMS", "CloudWatch", "StepFunctions", etc.
2. For end users, use: "UserConsumerWebMobile" if both mobile and web users are represented in the same flow, or "UserConsumerMobile" / "UserConsumerWeb" if distinct.
3. Map rendering engine clusters/instances running on EC2 directly to service "EC2", putting "Rendering Engines" or "ASG" in the name or notes field.
4. Do NOT use "ThirdParty" for internal microservices (e.g., "Friend Graph", "SnapDB", "Messaging Service"). Map them to the underlying AWS compute/storage service they run on (e.g. "EKS", "Lambda"), putting the microservice name in the `notes` field. Use "ThirdParty" only for external third-party software (e.g. MySQL, Nginx).
4. Each node can appear MULTIPLE times if shown multiple times in the diagram \
(keep duplicate nodes as in Cloudscape).
5. Edges must have: flow_id (integer, grouping related interactions into \
workflows), seq (string, ordering within flow), type ("data" for data \
movement, "meta" for request triggers / ack responses), and notes (CRITICAL: notes in edges MUST be completely empty, i.e. "").
6. CRITICAL RULE FOR EDGES: The notes field in the edges list MUST be completely empty (i.e. "notes": ""). Do NOT write any description sentences or texts on edges. All step descriptions must go in the node's notes or in an external document, NEVER on the graph edges.
7. The `notes` field for nodes should capture context from the transcript: \
how the service is used, data volumes, configurations mentioned. Use \
prefixes like "DATA_PEEK:" for data info and "WORKLOAD_PEEK:" for workload.
8. IMPORTANT: Use the TRANSCRIPT as the primary source of truth for \
understanding the architecture. The image shows the visual layout. When \
they conflict, prefer the transcript.

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "graph": {
    "name": "<title of the architecture>",
    "link": "<youtube URL if known, else empty string>",
    "categories": "<comma-separated from: data_ingestion, interactive, compute_intensive, control, other>",
    "graph_usable": true,
    "notes": "<distilled context: requirements, scale, key design decisions>"
  },
  "nodes": [
    {"id": "0", "service": "...", "name": "", "notes": "..."}
  ],
  "edges": [
    {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""}
  ]
}

If the image does NOT contain an AWS architecture diagram, return:
{"graph": {}, "nodes": [], "edges": []}
"""


# ── Public API ───────────────────────────────────────────────

def analyze_frame(
    frame_path: Path,
    transcript: str = "",
    video_url: str = "",
) -> dict[str, Any]:
    """
    Send a single keyframe + transcript to Gemini for architecture extraction.

    Parameters
    ----------
    frame_path : Path
        Path to the whiteboard image.
    transcript : str
        Full transcript of the video (from Whisper).
    video_url : str
        YouTube URL for the video.

    Returns
    -------
    dict
        Parsed JSON with ``graph``, ``nodes``, ``edges`` in Cloudscape schema.
    """
    client = _get_client()

    # Read and encode image
    image_bytes = frame_path.read_bytes()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    # Determine MIME type
    suffix = frame_path.suffix.lower()
    mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(
        suffix.lstrip("."), "image/jpeg"
    )

    # Build prompt with transcript context
    prompt_parts = [CLOUDSCAPE_PROMPT]
    if video_url:
        prompt_parts.append(f"\n## VIDEO URL:\n{video_url}")
    if transcript:
        prompt_parts.append(f"\n## FULL TRANSCRIPT:\n{transcript}")

    full_prompt = "\n".join(prompt_parts)

    console.print(f"  [dim]→ Analyzing {frame_path.name} with Gemini ({GEMINI_MODEL})…[/]")
    if transcript:
        console.print(f"  [dim]  Including transcript ({len(transcript)} chars)[/]")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            {
                "parts": [
                    {"text": full_prompt},
                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": image_b64,
                        }
                    },
                ]
            }
        ],
        config={"response_mime_type": "application/json"},
    )

    # Parse the JSON response
    raw_text = response.text.strip()
    console.print(f"[dim]Gemini response text: {raw_text}[/]")

    # Strip possible markdown fences (```json ... ```)
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1]
        if "```" in raw_text:
            raw_text = raw_text[: raw_text.rfind("```")]
        raw_text = raw_text.strip()

    # Try direct parse first
    data = None
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON object from mixed text
        start = raw_text.find("{")
        end = raw_text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                data = json.loads(raw_text[start:end])
            except json.JSONDecodeError:
                pass

    if data is None:
        console.print(f"[yellow]⚠[/]  Failed to parse Gemini response as JSON")
        console.print(f"[dim]{raw_text[:500]}[/]")
        data = {"graph": {}, "nodes": [], "edges": []}

    node_count = len(data.get("nodes", []))
    edge_count = len(data.get("edges", []))
    console.print(
        f"  [green]✓[/] {frame_path.name}: "
        f"{node_count} nodes, {edge_count} edges"
    )

    return data


def analyze_frames_batch(
    frame_paths: list[Path],
    transcript: str = "",
    video_url: str = "",
) -> list[dict[str, Any]]:
    """
    Analyze multiple frames sequentially (respects API rate limits).

    Returns
    -------
    list[dict]
        One result dict per frame.
    """
    console.print(
        f"\n[bold cyan]🔍  Analyzing {len(frame_paths)} frames with Gemini[/]\n"
    )
    results = []
    for i, fp in enumerate(frame_paths, 1):
        console.print(f"[bold]Frame {i}/{len(frame_paths)}[/]")
        result = analyze_frame(fp, transcript=transcript, video_url=video_url)
        result["_source_frame"] = fp.name
        results.append(result)

    total_nodes = sum(len(r.get("nodes", [])) for r in results)
    total_edges = sum(len(r.get("edges", [])) for r in results)
    console.print(
        f"\n[green]✓[/] Batch complete — "
        f"[bold]{total_nodes}[/] total nodes, "
        f"[bold]{total_edges}[/] total edges across all frames"
    )
    return results


# ── CLI ──────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze whiteboard frame with Gemini")
    parser.add_argument("frame", type=Path, help="Path to whiteboard image")
    parser.add_argument("--transcript", type=Path, help="Path to transcript JSON")
    parser.add_argument("--url", default="", help="YouTube video URL")
    parser.add_argument("--output", type=Path, help="Output JSON path")
    args = parser.parse_args()

    # Load transcript if provided
    transcript_text = ""
    if args.transcript and args.transcript.exists():
        with open(args.transcript) as f:
            segments = json.load(f)
        if isinstance(segments, list):
            transcript_text = " ".join(s.get("text", "").strip() for s in segments)
        elif isinstance(segments, dict) and "text" in segments:
            transcript_text = segments["text"]
        console.print(f"[green]✓[/] Loaded transcript: {len(transcript_text)} chars")

    result = analyze_frame(args.frame, transcript=transcript_text, video_url=args.url)

    # Save output
    out_path = args.output or args.frame.with_suffix(".cloudscape.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    console.print(f"[green]✓[/] Result saved → {out_path}")
