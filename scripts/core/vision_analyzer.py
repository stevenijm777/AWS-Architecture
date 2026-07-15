"""
vision_analyzer.py — Gemini API vision analysis of architecture keyframes
                     Outputs Cloudscape-compatible schema (FAST25 paper).
"""
from __future__ import annotations

import base64
import csv
import json
import re
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
    csv_path = Path(__file__).resolve().parent.parent / "data" / "cloudscape_gt" / "services.csv"
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


# Robust JSON text cleaner to prevent syntax errors
def clean_json_text(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if "```" in text:
            text = text[:text.rfind("```")]
    text = text.strip()
    # Remove trailing commas in lists or objects
    text = re.sub(r',\s*([\]}])', r'\1', text)
    return text


MFR_STAGE_1_PROMPT_TEMPLATE = """You are an expert cloud architecture ontology modeler.
Your task is to analyze the provided whiteboard diagram and audio transcript to build a structured "World Model" representing the architecture components and their physical drawn connections.

Do NOT generate the final graph, node IDs, or edge sequences. Focus strictly on identifying the entities and the VISUAL CONNECTIONS drawn on the whiteboard.

## ENTITY IDENTIFICATION RULES:
1. Identify all active systems, databases, cloud services, and actors.
2. Use valid AWS services from this list: <AWS_SERVICES_PLACEHOLDER>.
3. Identify actors/users from this list: <USER_ACTORS_PLACEHOLDER>. Map internal operations/migration teams to "UserCompanyAgent".
4. Map on-premises/external systems to "ThirdParty" (e.g. legacy databases, Slack, or on-premises servers), unless a physically drawn corporate data center box is shown.
5. Do NOT include transient files, packages, or disk images (like AMIs, zip files, or container images) as entities. They are transition properties, not permanent nodes.

## VISUAL CONNECTION RULES:
1. Look closely at the whiteboard image. Identify every drawn connection line or arrow between the entities.
2. Note the source, target, and the direction of the arrow.
3. Only list connections that are VISUALLY represented by lines or arrows on the board. Do NOT list connections that are only mentioned in the audio but have no line drawn on the board.

## FORMAT RULES:
- Inside JSON string fields, NEVER use unescaped double quotes. Use single quotes instead (e.g. write 'AMI' instead of "AMI").

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "entities": [
    {"service": "AWS Service or Actor Name", "name": "Label on the whiteboard", "type": "AWS_Service|User|ThirdParty", "rationale": "..."}
  ],
  "visual_connections": [
    {"source_label": "Label of source box", "target_label": "Label of target box", "arrow_direction": "source_label -> target_label", "description": "What this line represents"}
  ]
}
"""

MFR_STAGE_2_PROMPT_TEMPLATE = """You are an expert AWS Solutions Architect. Your task is to compile the final cloud architecture graph from the provided World Model, whiteboard image, and audio transcript.

You must follow the structure and level of detail of the Cloudscape dataset schema.

## WORLD MODEL (IMMUTABLE INPUT):
Below is the verified World Model of the architecture. You MUST strictly adhere to this model.
<WORLD_MODEL_PLACEHOLDER>

## RULES FOR NODES:
1. Create nodes ONLY for the services and actors listed in the "entities" section of the World Model. Do NOT invent or add any other services, actors, or transient nodes (such as AMIs, packages, or config files).

## RULES FOR EDGES:
1. Create edges ONLY for the connections listed in the "visual_connections" section of the World Model.
2. Keep the exact source and target direction as specified in the "visual_connections" (arrow_direction).
3. Do NOT create return/response paths or API acknowledgments (e.g., target sending back status) unless they are physically drawn as a separate arrow on the whiteboard.
4. Set "type" to "control" for system triggers, API calls, scripts, or command invocations. Set "type" to "data" ONLY for actual block data replication, payload transmission, or database reads/writes.
5. Set the "notes" field for each edge to describe the interaction, combining the transcript details with the visual path.
6. The `flow_id` represents unique workflows. Sequential steps in the same workflow must share the same `flow_id` and have sequential `seq` numbers (0, 1, 2, 3...) based on the transcript chronology.

## FORMAT RULES:
- Inside JSON string fields, NEVER use unescaped double quotes. Use single quotes instead (e.g. write 'AMI' instead of "AMI").

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Deduce the nodes and edges from the World Model entities and visual connections, ordering them chronologically...",
  "graph": {
    "name": "<title of the architecture>",
    "link": "<youtube URL if known, else empty string>",
    "categories": "<comma-separated from: data_ingestion, interactive, compute_intensive, control, other>",
    "graph_usable": true,
    "notes": "<distilled context>"
  },
  "nodes": [
    {"id": "0", "service": "service name from entities", "name": "name from entities", "notes": "context of usage"}
  ],
  "edges": [
    {"source": "node_id", "target": "node_id", "flow_id": 0, "seq": "0", "type": "data|control", "notes": "action detail"}
  ]
}
"""

def _call_gemini_with_retry(client: genai.Client, full_prompt: str, mime: str, image_b64: str):
    import time
    max_retries = 5
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
            return response
        except Exception as e:
            err_msg = str(e)
            if attempt < max_retries - 1 and any(x in err_msg.upper() or y in err_msg for x in ["503", "429", "UNAVAILABLE", "LIMIT"] for y in ["demand", "ResourceExhausted", "quota"]):
                delay = 65 if ("429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg.upper() or "quota" in err_msg.lower()) else retry_delay
                console.print(f"  [yellow]⚠ Gemini API returned error: {err_msg}. Retrying in {delay}s... (Attempt {attempt+1}/{max_retries})[/]")
                time.sleep(delay)
                retry_delay *= 2
            else:
                raise e


# ── Public API ───────────────────────────────────────────────

def analyze_frame(
    frame_path: Path,
    transcript: str = "",
    video_url: str = "",
    detected_symbols: dict[str, list[dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """
    Send a single keyframe + transcript + detected symbols to Gemini for architecture extraction.
    Uses the Double-Model (Modeler + Planner) technique.
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

    # ── Stage 1: MODELER (Generate World Model) ──
    formatted_prompt_1 = MFR_STAGE_1_PROMPT_TEMPLATE.replace(
        "<USER_ACTORS_PLACEHOLDER>", user_actors_str
    ).replace(
        "<AWS_SERVICES_PLACEHOLDER>", aws_services_str
    )
    
    prompt_parts_1 = [formatted_prompt_1]
    if video_url:
        prompt_parts_1.append(f"\n## VIDEO URL:\n{video_url}")
    if transcript:
        prompt_parts_1.append(f"\n## FULL TRANSCRIPT:\n{transcript}")
    if detected_symbols:
        detected_parts = ["\n## DETECTED AWS SERVICE SYMBOLS (GUIDELINE):"]
        for service, occurrences in sorted(detected_symbols.items()):
            count = len(occurrences)
            box_strs = [f"box: {det['box']}" for det in occurrences]
            detected_parts.append(f"- {service}: {count} occurrences ({', '.join(box_strs)})")
        prompt_parts_1.append("\n".join(detected_parts))

    full_prompt_1 = "\n".join(prompt_parts_1)

    console.print(f"  [dim]→ [Stage 1 Modeler] Building World Model for {frame_path.name} with Gemini ({GEMINI_MODEL})…[/]")
    response_1 = _call_gemini_with_retry(client, full_prompt_1, mime, image_b64)
    world_model_text = clean_json_text(response_1.text)
    
    try:
        world_model = json.loads(world_model_text)
    except json.JSONDecodeError:
        # fallback parsing
        start = world_model_text.find("{")
        end = world_model_text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                world_model = json.loads(world_model_text[start:end])
            except json.JSONDecodeError:
                world_model = {"entities": [], "visual_connections": []}
        else:
            world_model = {"entities": [], "visual_connections": []}

    console.print(f"  [green]✓[/] World Model generated ({len(world_model.get('entities', []))} entities, {len(world_model.get('visual_connections', []))} connections)")

    # ── Stage 2: PLANNER (Compile Architecture Graph) ──
    formatted_prompt_2 = MFR_STAGE_2_PROMPT_TEMPLATE.replace(
        "<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False)
    )
    
    prompt_parts_2 = [formatted_prompt_2]
    if video_url:
        prompt_parts_2.append(f"\n## VIDEO URL:\n{video_url}")
    if transcript:
        prompt_parts_2.append(f"\n## FULL TRANSCRIPT:\n{transcript}")

    full_prompt_2 = "\n".join(prompt_parts_2)

    console.print(f"  [dim]→ [Stage 2 Planner] Compiling final architecture graph with Gemini ({GEMINI_MODEL})…[/]")
    response_2 = _call_gemini_with_retry(client, full_prompt_2, mime, image_b64)
    graph_json_text = clean_json_text(response_2.text)

    # Parse final JSON graph
    data = None
    try:
        data = json.loads(graph_json_text)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON object from mixed text
        start = graph_json_text.find("{")
        end = graph_json_text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                data = json.loads(graph_json_text[start:end])
            except json.JSONDecodeError:
                pass

    if isinstance(data, list):
        console.print("[yellow]WARNING: Gemini Planner returned a list. Using the first item...[/]")
        data = data[0] if data else {"graph": {}, "nodes": [], "edges": []}

    if data is None:
        console.print(f"[yellow]WARNING: Failed to parse Gemini Planner response as JSON[/]")
        console.print(f"[dim]{graph_json_text[:500]}[/]")
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
