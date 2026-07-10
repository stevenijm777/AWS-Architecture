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

def load_services_catalog() -> tuple[list[str], list[str]]:
    """
    Load valid AWS services and user actors from services.csv.
    """
    csv_path = Path(__file__).resolve().parent.parent / "graph_renderer" / "services.csv"
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

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.) in a way that matches the style and level of detail of the manual ground truth dataset as closely as possible.

## RULES:
1. Use SHORT AWS service names for `service` field: e.g. "S3", "Lambda", "EC2", "DynamoDB", "EKS", "CloudFront", etc.

2. USER ACTOR NORMALIZATION: Only add User nodes that are EXPLICITLY shown as icons on the whiteboard OR mentioned as main actors. Choose from this list: <USER_ACTORS_PLACEHOLDER>. To match Ground Truth style:
   - Map end-users accessing via browsers to "UserConsumerWeb", and app users to "UserConsumerMobile". Do NOT combine them into "UserConsumerWebMobile" unless a single physical box on the board is explicitly labeled for both.
   - Prefer "UserCompanyAgent" for internal operations teams, database administrators, migration teams, or backend system operators.
   - Use "UserCompanyDeveloper" ONLY when the text or diagram explicitly refers to writing application code, managing CI/CD pipelines, or software development.

3. Map rendering engine clusters/instances running on EC2 directly to service "EC2", putting "Rendering Engines" or "ASG" in the name or notes field.

4. NON-CLOUD & ON-PREMISE NORMALIZATION: Do NOT use "ThirdParty" for internal microservices. Map them to the underlying AWS compute/storage service they run on (e.g. "EKS", "Lambda").
   - However, map on-premises servers, local databases, and legacy infrastructure to "ThirdParty" (representing external resources outside AWS) to maintain consistency with Ground Truth, unless a dedicated data center icon is explicitly drawn (in which case use "OnPremDC").

5. NODE MULTIPLICITY & NO TRANSIENT ARTIFACTS: The number of nodes must match the number of physical icons (boxes) drawn on the whiteboard.
   - Do NOT create nodes for transient artifacts, machine images, config templates, or zip files (e.g., do NOT create nodes for "AMI", "Container Image", or "CloudFormation Template") even if they are described as being baked, shared, or uploaded. Instead, represent these actions as descriptions or notes on the edges (flows) connecting the permanent compute/storage components that generate or consume them.

6. Edges must have: flow_id (integer), seq (string), type ("data" or "meta"). Default to "data" for all edges.

7. EDGE DIRECTIONALITY (NO RETURN PATHS): Map ONLY active data movement or control triggers. Do NOT add return/response paths or API acknowledgments (e.g., target acknowledging source) unless they carry a distinct new payload or trigger a new asynchronous step. Orient arrows in the direction of request initiation.

8. Minimize the number of flows. Group related sequential interactions into a single flow.

9. The `notes` field for nodes should capture context from the transcript: how the service is used.

10. WHITEBOARD IMAGE IS THE PRIMARY STRUCTURE GUIDE (MATCH HUMAN DESIGN): The physical whiteboard image (icons and drawn arrows) is the primary source of truth for the structure of the graph. Do NOT add extra nodes or complex orchestration paths that are not represented by icons or arrows on the whiteboard.

## PARSIMONY PRINCIPLE:
Prefer FEWER nodes and edges over more. If you are unsure whether a service exists in the architecture, DO NOT include it. It is better to miss a real service than to hallucinate a fake one.

## VALID SERVICE NAMES:
You MUST only use names from this list of canonical services when defining the `service` field in the nodes list (do not invent names or use raw abbreviations unless listed here):
<AWS_SERVICES_PLACEHOLDER>

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Analyze the transcript chronologically...",
  "graph": {
    "name": "<title of the architecture>",
    "link": "<youtube URL if known, else empty string>",
    "categories": "<comma-separated from: data_ingestion, interactive, compute_intensive, control, other>",
    "graph_usable": true,
    "notes": "<distilled context>"
  },
  "nodes": [
    {"id": "0", "service": "...", "name": "", "notes": "..."}
  ],
  "edges": [
    {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""}
  ]
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
    max_retries = 3
    retry_delay = 10
    response = None

    for attempt in range(max_retries):
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
                config={"response_mime_type": "application/json"},
            )
            break
        except Exception as e:
            err_msg = str(e)
            if attempt < max_retries - 1 and any(x in err_msg.upper() or y in err_msg for x in ["503", "429", "UNAVAILABLE", "LIMIT"] for y in ["demand", "ResourceExhausted"]):
                console.print(f"  [yellow]⚠ Gemini API returned error: {err_msg}. Retrying in {retry_delay}s... (Attempt {attempt+1}/{max_retries})[/]")
                time.sleep(retry_delay)
                retry_delay *= 2
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
