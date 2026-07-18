"""
vision_analyzer.py — Gemini API vision analysis of architecture keyframes
                     Outputs Cloudscape-compatible schema (FAST25 paper).
                     Uses Pydantic schemas for guaranteed JSON structure.
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
from pydantic import BaseModel
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


# ── Services Catalog ─────────────────────────────────────────

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


# ══════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — Phase 1 (World Model)
# ══════════════════════════════════════════════════════════════

class Entity(BaseModel):
    service: str
    name: str
    type: str
    rationale: str


class VisualConnection(BaseModel):
    source_label: str
    target_label: str
    arrow_direction: str
    description: str


class WorldModelSchema(BaseModel):
    entities: list[Entity]
    visual_connections: list[VisualConnection]


# ══════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS — Phase 2 (Final Architecture Graph)
# ══════════════════════════════════════════════════════════════

class GraphMetadata(BaseModel):
    name: str
    link: str
    categories: str
    graph_usable: bool
    notes: str


class Node(BaseModel):
    id: str
    service: str
    name: str
    notes: str


class Edge(BaseModel):
    source: str
    target: str
    flow_id: int
    seq: str
    type: str
    notes: str


class FinalArchitectureSchema(BaseModel):
    step_by_step_reasoning: str
    graph: GraphMetadata
    nodes: list[Node]
    edges: list[Edge]


# ══════════════════════════════════════════════════════════════
# PROMPTS
# ══════════════════════════════════════════════════════════════

MFR_STAGE_1_PROMPT_TEMPLATE = """You are an expert in visual extraction of cloud architectures. Your task is to analyze the provided whiteboard diagram and audio transcript to build a structured "World Model" representing the components and their visual groupings.

Do NOT generate the final graph. Focus strictly on identifying the present entities, how they are visually grouped, and what lines connect them.

## ENTITY IDENTIFICATION AND GROUPING RULES:
1. Identify all active systems, databases, cloud services, and actors VISIBLE on the whiteboard.
2. Identify BOXES or dashed containers. If a service (e.g., SAP) is drawn inside another service or box (e.g., EC2), register both and strictly note this containment in the "rationale".
3. Use valid AWS services from this list: <AWS_SERVICES_PLACEHOLDER>.
4. Identify actors/users from this list: <USER_ACTORS_PLACEHOLDER>. Map on-premises/external systems to "ThirdParty" and actors to "User".
5. Do NOT include transient files, packages, or disk images (like AMIs) as entities.

## VISUAL CONNECTION RULES:
1. Register ALL lines or arrows explicitly drawn between entities on the whiteboard.
2. Note the source, target, and the direction of the arrow.
"""

MFR_STAGE_2_PROMPT_TEMPLATE = """
You are an expert AWS Solutions Architect. Your task is to compile the final logical cloud architecture graph from the provided World Model and audio transcript.

You must generalize your reasoning to deduce the true logical "Ground Truth" architecture based on standard AWS patterns, ignoring visual drawing errors but respecting the core system design.

## VALID VOCABULARY LISTS (CRITICAL):
You may ONLY use exact values from these lists for the "service" field.

AWS Services:
<AWS_SERVICES_PLACEHOLDER>

User and Client Actors:
<USER_ACTORS_PLACEHOLDER>

## MULTILINGUAL TRANSLATION RULE:
Translate all output text fields (notes, graph name, reasoning, etc.) into ENGLISH.

## WORLD MODEL (BASE INPUT):
Use this as your visual inventory.
<WORLD_MODEL_PLACEHOLDER>

## NODE RULES (PRUNING, FUSION, AND ROLE SEPARATION):
1. **Strict Normalization (CRITICAL):** The "service" field MUST match exactly with an element from the VALID VOCABULARY LISTS. NEVER invent or hallucinate a name.
   - Map Auto Scaling Groups (ASG) or compute clusters directly to "EC2". DO NOT use "AutoScaling".
   - **Client Abstraction:** Map ALL external client entities (e.g., users, browsers, publisher websites, mobile devices) into a SINGLE combined node using the most appropriate actor from the list (e.g., "UserConsumerWeb"). DO NOT split the user and the website into two nodes.
2. **Numeric Identifiers:** The "id" field of each node MUST be strictly a sequential integer in string format (e.g., "0", "1", "2").
3. **Logical Fusion vs. Separation (HEURISTIC):**
   - **FUSE** related microservices (like multiple Lambda functions handling different triggers) into a single representative service node to keep the graph highly abstracted.
   - **SEPARATE** massive compute infrastructure (like EC2 fleets) ONLY if they serve entirely distinct architectural roles (e.g., a "Bidding" EC2 cluster vs. a "Tracking" EC2 cluster).
4. **Pruning:** Remove generic human actors or purely physical concepts. Keep system entry points.
5. **Note Assimilation:** Extract specific constraints and metrics from the transcript (e.g., "1 million requests per second", "Spot instances") and inject them into the "notes" of the relevant nodes.

## EDGE AND FLOW RULES (LOGICAL ROUTING):
1. **Strict Flow Segmentation (`flow_id`):** Group related architectural actions into distinct logical workflows using an integer `flow_id` (starting at 0).
   - `0`: Usually the primary baseline, ingestion, or synchronous workflow.
   - `1`, `2`, `3`, etc.: Subsequent, decoupled, or asynchronous workflows.
2. **Chronological Sequence (`seq`):**
   - Order events within a flow using string integers ("0", "1", "2").
   - **Parallel Actions:** If a single component triggers MULTIPLE downstream actions simultaneously, use the prime character (e.g., "1" and "1'").
   - **Bidirectionality:** Request/response cycles must be modeled as two edges (e.g., Request is "0", Response is "1").
3. **Edge Types (`type`):**
   - Use "data" for payload transfers, database reads/writes, or heavy data movement.
   - Use "control" for events, triggers, or asynchronous invocations.
"""


# ── Retry Logic ──────────────────────────────────────────────

def _call_gemini_with_retry(
    client: genai.Client,
    full_prompt: str,
    mime: str,
    image_b64: str,
    response_schema=None,
):
    """Call Gemini with retry logic for transient API errors.
    
    When response_schema is provided, uses Pydantic-enforced structured output.
    """
    import time
    max_retries = 5
    retry_delay = 10
    response = None

    config = {"response_mime_type": "application/json"}
    if response_schema is not None:
        config["response_schema"] = response_schema

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
                config=config,
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
    Uses the Double-Model (Modeler + Planner) technique with Pydantic schemas
    for guaranteed JSON structure.
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

    # ══════════════════════════════════════════════════════════
    # PHASE 1: MODELER — Build the World Model
    # ══════════════════════════════════════════════════════════
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

    console.print(f"  [dim]→ [Stage 1 Modeler] Building World Model for {frame_path.name} with Gemini ({GEMINI_MODEL}) + Pydantic…[/]")
    response_1 = _call_gemini_with_retry(
        client, full_prompt_1, mime, image_b64,
        response_schema=WorldModelSchema,
    )

    # Pydantic guarantees valid JSON — direct parse
    world_model = json.loads(response_1.text)
    console.print(f"  [green]✓[/] World Model generated ({len(world_model.get('entities', []))} entities, {len(world_model.get('visual_connections', []))} connections)")

    # ══════════════════════════════════════════════════════════
    # PHASE 2: PLANNER — Compile Final Architecture Graph
    # ══════════════════════════════════════════════════════════
    formatted_prompt_2 = MFR_STAGE_2_PROMPT_TEMPLATE.replace(
        "<WORLD_MODEL_PLACEHOLDER>", json.dumps(world_model, indent=2, ensure_ascii=False)
    ).replace(
        "<AWS_SERVICES_PLACEHOLDER>", aws_services_str
    ).replace(
        "<USER_ACTORS_PLACEHOLDER>", user_actors_str
    )

    prompt_parts_2 = [formatted_prompt_2]
    if video_url:
        prompt_parts_2.append(f"\n## VIDEO URL:\n{video_url}")
    if transcript:
        prompt_parts_2.append(f"\n## FULL TRANSCRIPT:\n{transcript}")

    full_prompt_2 = "\n".join(prompt_parts_2)

    console.print(f"  [dim]→ [Stage 2 Planner] Compiling final architecture graph with Gemini ({GEMINI_MODEL}) + Pydantic…[/]")
    response_2 = _call_gemini_with_retry(
        client, full_prompt_2, mime, image_b64,
        response_schema=FinalArchitectureSchema,
    )

    # Pydantic guarantees valid JSON — direct parse
    data = json.loads(response_2.text)

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
