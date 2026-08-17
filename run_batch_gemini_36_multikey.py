"""
Multi-Key Batch Processor for Gemini 3.6 Flash (Prompt v9 Parsimonious)

Usage:
  python run_batch_gemini_36_multikey.py

Features:
  - Reads `GEMINI_API_KEYS` list from `.env` (via config.settings).
  - Automatically rotates to the next API key when 429 Quota/Limit is reached.
  - Automatically updates history markdown, viewer HTML, and ablation reports when done.
"""

import os
import sys
import base64
import json
import shutil
import re
import time
import subprocess
import pandas as pd
import networkx as nx
from pathlib import Path
from pydantic import BaseModel
from google import genai

MODEL_NAME = "gemini-3.6-flash"

PROJECT_ROOT = Path('.').resolve()
sys.path.append(str(PROJECT_ROOT))

LAB_DIR = PROJECT_ROOT / "whiteboard_selection_lab"
services_csv = PROJECT_ROOT / "graph_renderer" / "services.csv"
if not services_csv.exists():
    services_csv = PROJECT_ROOT / "data" / "cloudscape_gt" / "services.csv"

df_services = pd.read_csv(services_csv)
df_actores = df_services[df_services['is_aws'] == False]
df_aws = df_services[df_services['is_aws'] == True]

lista_actores = ", ".join(df_actores['name'].dropna().astype(str).unique())
lista_aws = ", ".join(df_aws['name'].dropna().astype(str).unique())

PROMPT_BASE = """You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES (STRICT PARSIMONIOUS MODEL - PROMPT V9):
1. AWS SERVICES: You MUST strictly use the exact string from the <AWS_SERVICES_PLACEHOLDER> list for the `service` field. Shortening or truncating service names is strictly forbidden (e.g. use 'KinesisDataStream' instead of 'Kinesis').

2. ACTORS / USERS: Use 'UserConsumerWeb', 'UserConsumerMobile', 'UserCompanyDeveloper', 'UserCompanyAgent', or 'ThirdParty' from <ACTORS_PLACEHOLDER>.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes primarily on physical boxes or distinct icons drawn with a clear contour on the whiteboard. Ignore standalone floating text or handwritten explanatory words without a bounding box or icon.

4. DECOMPOSITION OF GROUPED BOXES:
   - If a box on the whiteboard represents a collection of AWS services (e.g. labeled 'AWS', 'Security Sources', or 'AWS Cloud Logs') AND the transcript explicitly names specific AWS services contained within it (such as CloudTrail, GuardDuty, SQS, SNS, S3):
   - You ARE REQUIRED to break down that single box into individual nodes for EACH explicitly named AWS service.

5. ARROW-DRIVEN EDGES & NO SPECULATIVE RETURNS:
   - Extract edges ONLY when there is a visible line or arrow physically drawn on the whiteboard canvas.
   - Do NOT generate speculative return paths or implicit responses unless a double-headed arrow (<->) or a second return line is explicitly drawn on screen.

6. LOGICAL SEQUENCING: Assign `flow_id` (integer) and `seq` (string) starting from external actors moving progressively towards backend data stores.

7. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string.

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Analyze visual components and physical lines...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}"""

prompt = PROMPT_BASE.replace("<ACTORS_PLACEHOLDER>", lista_actores).replace("<AWS_SERVICES_PLACEHOLDER>", lista_aws)

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

def main():
    import importlib
    import config.settings
    importlib.reload(config.settings)

    api_keys_pool = config.settings.GEMINI_API_KEYS
    if not api_keys_pool:
        print("❌ Error: GEMINI_API_KEYS no contiene llaves API válidas en .env")
        sys.exit(1)

    current_key_idx = 0
    client = genai.Client(api_key=api_keys_pool[current_key_idx])

    print(f"==================================================")
    print(f"🔑 Pool de {len(api_keys_pool)} Llaves API cargado para rotación automática.")
    print(f"==================================================")

    from scripts.core.graph_builder import create_graph_from_cloudscape_json
    from scripts.utils.evaluate_graphs import evaluate_pair, load_services_catalog

    catalog_dict = load_services_catalog(services_csv)

    gt_dir = PROJECT_ROOT / "data" / "cloudscape_gt"
    all_gt_videos = [p.stem for p in gt_dir.glob("*.graphml")]

    unprocessed_candidates = []

    for vid in all_gt_videos:
        lab_ws = LAB_DIR / "lab_workspace" / vid
        json_cache = PROJECT_ROOT / "data" / "raw" / f"{vid}_vision_analysis_parsimonious.json"

        if (lab_ws / "test_graph.graphml").exists() or json_cache.exists():
            continue

        p1 = PROJECT_ROOT / "data" / "good_whiteboard" / f"{vid}.jpg"
        p2 = PROJECT_ROOT / "cloudscape_reports" / vid / "best_whiteboard.jpg"
        p3 = LAB_DIR / "frames_new" / f"{vid}_pizarra" / "best_whiteboard.jpg"
        p4 = PROJECT_ROOT / "data" / "pizarras_buenas" / f"{vid}.jpg"
        p5 = PROJECT_ROOT / "data" / "pizarras" / f"{vid}.jpg"

        whiteboard_found = None
        for p in [p1, p2, p3, p4, p5]:
            if p.exists():
                whiteboard_found = p
                break

        t1 = PROJECT_ROOT / "data" / "raw" / f"{vid}_transcript.json"
        t2 = LAB_DIR / "transcriptions" / f"{vid}_transcript.json"

        transcript_found = None
        for t in [t1, t2]:
            if t.exists():
                transcript_found = t
                break

        if whiteboard_found and transcript_found:
            unprocessed_candidates.append({
                "video_id": vid,
                "whiteboard_path": whiteboard_found,
                "transcript_path": transcript_found
            })

    print(f"🚀 Se encontraron {len(unprocessed_candidates)} videos candidatos no procesados listos para evaluar en {MODEL_NAME}.")

    if not unprocessed_candidates:
        print("🎉 ¡Todos los videos candidatos ya han sido procesados!")
        return

    node_env = os.environ.copy()
    node_env["PATH"] = "C:\\Users\\USUARIO\\Downloads\\PROGRAMAS\\WPy64-31040\\n;" + node_env.get("PATH", "")

    batch_results = []
    pool_exhausted = False

    for idx, candidate in enumerate(unprocessed_candidates, 1):
        video_id = candidate["video_id"]
        wb_path = candidate["whiteboard_path"]
        tr_path = candidate["transcript_path"]

        print(f"\n[{idx}/{len(unprocessed_candidates)}] Procesando Video {video_id} con Prompt v9 ({MODEL_NAME}) [Llave API #{current_key_idx+1}/{len(api_keys_pool)}]...")

        lab_workspace = LAB_DIR / "lab_workspace" / video_id
        lab_workspace.mkdir(parents=True, exist_ok=True)

        cache_json = lab_workspace / "test_analysis.json"
        cache_graphml = lab_workspace / "test_graph.graphml"

        gt_graph_path = gt_dir / f"{video_id}.graphml"
        gt_g = nx.read_graphml(str(gt_graph_path))

        ws_whiteboard = lab_workspace / "best_whiteboard.jpg"
        ws_transcript = LAB_DIR / "transcriptions" / f"{video_id}_transcript.json"

        shutil.copy2(wb_path, ws_whiteboard)
        LAB_DIR.joinpath("transcriptions").mkdir(parents=True, exist_ok=True)
        shutil.copy2(tr_path, ws_transcript)

        image_bytes = ws_whiteboard.read_bytes()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        with open(ws_transcript, "r", encoding="utf-8") as f:
            segments = json.load(f)
        transcript_text = " ".join(s.get("text", "").strip() for s in segments)

        full_prompt = f"{prompt}\n\n## FULL TRANSCRIPT:\n{transcript_text}"

        res_data = None

        while current_key_idx < len(api_keys_pool):
            key_changed = False
            for attempt in range(1, 4):
                try:
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[
                            {
                                "parts": [
                                    {"text": full_prompt},
                                    {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}}
                                ]
                            }
                        ],
                        config={
                            "response_mime_type": "application/json",
                            "response_schema": FinalArchitectureSchema
                        }
                    )
                    res_data = json.loads(response.text)
                    break
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "QuotaExceeded" in err_str:
                        print(f"⛔ Límite de cuota alcanzado en la Llave API #{current_key_idx+1}.")
                        current_key_idx += 1
                        if current_key_idx < len(api_keys_pool):
                            print(f"🔄 Rotando automáticamente a la Llave API #{current_key_idx+1} de {len(api_keys_pool)}...")
                            client = genai.Client(api_key=api_keys_pool[current_key_idx])
                            key_changed = True
                            break
                        else:
                            print(f"🛑 Se agotaron las {len(api_keys_pool)} llaves API del pool.")
                            pool_exhausted = True
                            break
                    else:
                        print(f"  ⚠ Intento {attempt}/3 falló en {video_id}: {e}")
                        time.sleep(3)

            if res_data or pool_exhausted:
                break
            if key_changed:
                continue

        if pool_exhausted:
            break

        if not res_data:
            print(f"❌ Error al procesar {video_id}")
            continue

        with open(cache_json, "w", encoding="utf-8") as f:
            json.dump(res_data, f, indent=2, ensure_ascii=False)

        test_g = create_graph_from_cloudscape_json(res_data)
        nx.write_graphml(test_g, str(cache_graphml))

        shutil.copy2(cache_graphml, PROJECT_ROOT / "data" / "graphs_parsimonious" / f"{video_id}.graphml")
        shutil.copy2(cache_json, PROJECT_ROOT / "data" / "raw" / f"{video_id}_vision_analysis_parsimonious.json")

        shutil.copy2(cache_graphml, PROJECT_ROOT / "graph_renderer" / "graphs_input" / f"{video_id}_vision.graphml")
        subprocess.run(
            ["node", "render_graph.mjs", f".\\{video_id}_vision.graphml"],
            cwd=str(PROJECT_ROOT / "graph_renderer"),
            env=node_env,
            shell=True,
            check=True
        )
        shutil.copy2(PROJECT_ROOT / "graph_renderer" / "graphs_output" / f"{video_id}_vision.png", PROJECT_ROOT / "Graphs" / f"{video_id}_vision.png")

        test_eval = evaluate_pair(test_g, gt_g, video_id, catalog_dict)

        batch_results.append({
            "video_id": video_id,
            "title": gt_g.graph.get('name', f"Video {video_id}"),
            "test_eval": test_eval
        })

        print(f"✓ Video {video_id}: Service F1={test_eval['svc_f1']*100:.1f}%, Edge F1={test_eval['edge_f1']*100:.1f}%")

    print(f"\n==================================================")
    print(f"🎉 Se completó el procesamiento de {len(batch_results)} videos con rotación de llaves API.")
    if pool_exhausted:
        print(f"🛑 El procesamiento se detuvo al agotar las {len(api_keys_pool)} llaves API.")
    print(f"==================================================")

if __name__ == "__main__":
    main()
