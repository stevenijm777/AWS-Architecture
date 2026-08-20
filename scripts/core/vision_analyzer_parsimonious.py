"""
vision_analyzer.py — Gemini API vision analysis of architecture keyframes
                     Outputs Cloudscape-compatible schema (FAST25 paper).
"""
from __future__ import annotations

import base64
import csv
import json
import sys
from pathlib import Path
from typing import Any

# Add project root to sys.path to support direct execution
sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai
from rich.console import Console

from config.settings import GEMINI_API_KEY, GEMINI_API_KEYS, GEMINI_MODEL

console = Console()

# ── Gemini Client (lazy init & multi-key rotation) ────────────
_current_key_idx = 0
_client: genai.Client | None = None


def _get_client(force_rotate: bool = False) -> genai.Client:
    global _client, _current_key_idx
    keys = GEMINI_API_KEYS if GEMINI_API_KEYS else ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    if not keys:
        raise ValueError("GEMINI_API_KEY or GEMINI_API_KEYS not set. Add them to your .env file.")

    if force_rotate:
        _current_key_idx = (_current_key_idx + 1) % len(keys)
        console.print(f"[yellow]🔄 Rotated Gemini API Key to key #{_current_key_idx+1}/{len(keys)}[/]")
        _client = genai.Client(api_key=keys[_current_key_idx])
    elif _client is None:
        _client = genai.Client(api_key=keys[_current_key_idx])
        console.print(f"[green]✓[/] Gemini client initialised with key #{_current_key_idx+1}/{len(keys)}")
    return _client



# ── Cloudscape-compatible Prompt ─────────────────────────────

def load_services_catalog() -> tuple[list[str], list[str]]:
    """
    Load valid AWS services and user actors from services.csv.
    """
    project_root = Path(__file__).resolve().parent.parent.parent
    csv_path = project_root / "data" / "cloudscape_gt" / "services.csv"
    if not csv_path.exists():
        csv_path = project_root / "data" / "services.csv"
    if not csv_path.exists():
        return [], []

    
    aws_services = set()
    user_actors = set()
    try:
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name", "").strip()
                capability = row.get("capability", "").strip().lower()
                if not name:
                    continue
                if capability == "user" or name.startswith("User"):
                    user_actors.add(name)
                else:
                    aws_services.add(name)
    except Exception as e:
        console.print(f"[yellow]⚠ Failed to load services catalog: {e}[/]")
    return sorted(list(aws_services)), sorted(list(user_actors))


AWS_SERVICES, USER_ACTORS = load_services_catalog()
aws_services_str = ", ".join(AWS_SERVICES)
user_actors_str = ", ".join(USER_ACTORS)


CLOUDSCAPE_PROMPT_TEMPLATE = """You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the <AWS_SERVICES_PLACEHOLDER> list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the <USER_ACTORS_PLACEHOLDER> list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes primarily on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.

4. MANDATORY DECOMPOSITION OF GROUPED BOXES: 
   - If a box on the whiteboard represents a collection of AWS services (e.g. labeled 'AWS', 'Security Sources', or 'AWS Cloud Logs') AND the transcript or presenter explicitly names the specific AWS services contained within it (such as CloudTrail, GuardDuty, SQS, SNS, S3):
   - You ARE REQUIRED to break down that single box into individual nodes for EACH explicitly named AWS service.
   - DO NOT create a single generic 'ThirdParty' or 'AWS Cloud Logs' node when specific AWS services are explicitly named in the audio/transcript.
   - If an arrow points to the boundary of the container, route connections directly to the decomposed internal service nodes.

5. STRICT VISUAL & ESSENTIAL EDGES (BALANCED CONNECTIONS): 
   - Base your connections primarily on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - Trace round-trip or return connections (<-) ONLY if they have a clear visual representation on the whiteboard (such as double arrowheads or explicit return line drawings) OR if they are indispensable to the primary synchronous execution flow drawn.
   - DO NOT mass-connect external actors or services to all components. Only draw entry and return connections that have a clear visual origin or explicit primary flow path.
   - Avoid generating speculative or decorative return paths that are not backed by visual line indicators.

6. LOGICAL SEQUENCING (FLOW FROM EXTERNAL ACTORS): When assigning `flow_id` (integer) and `seq` (string) to edges, always trace the sequence starting from external actors (UserConsumer*, UserCompany*, ThirdParty) moving progressively inwards toward the backend.

7. PARSIMONY PRINCIPLE (VISUAL DEDUPLICATION): 
   - Keep the graph structurally clean. Deduplicate multiple instances of the SAME service if they perform the exact same logical step.

8. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string.

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Briefly analyze the visual components and explicit arrows...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}
"""


CLOUDSCAPE_PROMPT = CLOUDSCAPE_PROMPT_TEMPLATE.replace(
    "<USER_ACTORS_PLACEHOLDER>", user_actors_str
).replace(
    "<AWS_SERVICES_PLACEHOLDER>", aws_services_str
)


# ── Public API ───────────────────────────────────────────────

def analyze_frame(
    frame_path: Path,
    transcript: str = "",
    video_url: str = "",
    detected_symbols: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """
    Send a single keyframe + transcript + detected symbols to Gemini for architecture extraction.

    Parameters
    ----------
    frame_path : Path
        Path to the whiteboard image.
    transcript : str
        Full transcript of the video (from Whisper).
    video_url : str
        YouTube URL for the video.
    detected_symbols : dict, optional
        AWS icons detected on the frame.

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
    if detected_symbols:
        detected_parts = ["\n## DETECTED AWS SERVICE SYMBOLS (GUIDELINE):"]
        detected_parts.append("The following AWS service symbols were detected using OpenCV template matching in this whiteboard frame:")
        for service, occurrences in sorted(detected_symbols.items()):
            count = len(occurrences)
            box_strs = [f"box: {det['box']}" for det in occurrences]
            detected_parts.append(f"- {service}: {count} occurrences ({', '.join(box_strs)})")
        detected_parts.append("\nPlease use this information to ensure the count and service types of nodes in your output graph correspond correctly to these physical icons in the diagram.")
        prompt_parts.append("\n".join(detected_parts))

    full_prompt = "\n".join(prompt_parts)

    console.print(f"  [dim]→ Analyzing {frame_path.name} with Gemini ({GEMINI_MODEL})…[/]")
    if transcript:
        console.print(f"  [dim]  Including transcript ({len(transcript)} chars)[/]")

    import time
    keys = GEMINI_API_KEYS if GEMINI_API_KEYS else ([GEMINI_API_KEY] if GEMINI_API_KEY else [])
    max_key_attempts = len(keys)
    response = None

    for key_attempt in range(max_key_attempts):
        client = _get_client()
        try:
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
                config={"response_mime_type": "application/json", "temperature": 0.0},
            )
            break
        except Exception as e:
            err_msg = str(e)
            if any(k in err_msg.upper() for k in ["429", "RESOURCE_EXHAUSTED", "QUOTA", "RATE_LIMIT"]):
                if key_attempt < max_key_attempts - 1:
                    console.print(f"  [yellow]⚠ Key #{_current_key_idx+1} quota exhausted (429). Rotating to next API key...[/]")
                    _get_client(force_rotate=True)
                    time.sleep(2)
                else:
                    console.print("  [bold red]🛑 All configured Gemini API keys have exhausted their quota.[/]")
                    raise e
            else:
                raise e


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

    if isinstance(data, list):
        console.print("[yellow]WARNING: Gemini returned a list of architectures. Merging them into a single graph...[/]")
        merged = {
            "step_by_step_reasoning": "",
            "graph": {
                "name": "",
                "link": "",
                "categories": "",
                "graph_usable": True,
                "notes": ""
            },
            "nodes": [],
            "edges": []
        }
        reasonings = []
        names = []
        notes_list = []
        categories_set = set()
        
        for idx, sub in enumerate(data):
            reasonings.append(f"--- Architecture {idx+1} ({sub.get('graph', {}).get('name', 'Unnamed')}) ---\n{sub.get('step_by_step_reasoning', '')}")
            names.append(sub.get("graph", {}).get("name", ""))
            notes_list.append(sub.get("graph", {}).get("notes", ""))
            
            # Categories
            cats = sub.get("graph", {}).get("categories", "")
            if cats:
                for c in cats.split(","):
                    c_clean = c.strip()
                    if c_clean:
                        categories_set.add(c_clean)
                        
            # Map nodes and assign unique IDs
            id_map = {}
            for node in sub.get("nodes", []):
                orig_id = str(node.get("id", ""))
                new_id = str(len(merged["nodes"]))
                id_map[orig_id] = new_id
                
                node_copy = dict(node)
                node_copy["id"] = new_id
                merged["nodes"].append(node_copy)
                
            # Map edges using the new IDs
            for edge in sub.get("edges", []):
                edge_copy = dict(edge)
                orig_src = str(edge.get("source", ""))
                orig_tgt = str(edge.get("target", ""))
                edge_copy["source"] = id_map.get(orig_src, orig_src)
                edge_copy["target"] = id_map.get(orig_tgt, orig_tgt)
                merged["edges"].append(edge_copy)
                
        # Consolidate metadata
        merged["step_by_step_reasoning"] = "\n\n".join(reasonings)
        merged["graph"]["name"] = f"Consolidated AWS Architectures ({', '.join([n for n in names if n])})"
        merged["graph"]["link"] = data[0].get("graph", {}).get("link", "") if data else ""
        merged["graph"]["categories"] = ", ".join(sorted(categories_set))
        merged["graph"]["notes"] = " ".join([n for n in notes_list if n])
        
        data = merged

    if data is None:
        console.print(f"[yellow]WARNING: Failed to parse Gemini response as JSON[/]")
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
