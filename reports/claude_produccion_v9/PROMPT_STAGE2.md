# Prompt de Stage 2 enviado a Claude

Prompt de Stage 2: `STAGE2_V9_CONNECTION_LEDGER` (archivo `stage2_v9_connection_ledger.txt`, sha256
`0ac90b9081d1`, una variante del de producción).

## Qué recibe Claude por video

Una sola llamada, sin historial, con dos bloques en este orden:

1. **Texto** — `videos/<id>/prompt.md`. Es la plantilla de abajo con tres reemplazos y dos
   anexos:
   - `<WORLD_MODEL_PLACEHOLDER>` → el JSON de `videos/<id>/world_model_produccion.json`
     (la lectura automática de la pizarra que produjo la etapa 1 (Gemini Flash, en caché): `entities` + `visual_connections`);
   - `<AWS_SERVICES_PLACEHOLDER>` → el catálogo de servicios de Cloudscape
     (141 nombres);
   - `<USER_ACTORS_PLACEHOLDER>` → el catálogo de actores (28 nombres);
   - al final, `## VIDEO URL:` y `## FULL TRANSCRIPT:` con la transcripción completa.
2. **Imagen** — `videos/<id>/pizarra.jpg`, el frame de pizarra de `good_whiteboard/`.

La forma de la respuesta se fuerza con `schema.json` (`claude -p --json-schema`), que es
el mismo esquema que Gemini recibió como `response_schema`. El prompt no cambia.

Para hacerlo a mano en claude.ai: conversación nueva, adjuntar `pizarra.jpg`, pegar
`prompt.md` y añadir al final «Responde únicamente con un objeto JSON que cumpla este
esquema:» seguido del contenido de `schema.json`. Guardar la respuesta como
`videos/<id>/output.json`.

## Plantilla (antes de los reemplazos)

````text
You are an Expert Cloud Architecture Transcriber. Your task is to faithfully transcribe the architecture EXACTLY as it is drawn on the whiteboard and described in the audio transcript. You are RECORDING the architecture, not redesigning it.
Do NOT invent unmentioned intermediate components or deployment layers unless they are explicitly present as active runtime participants.
## VALID VOCABULARY LISTS (CRITICAL):
You may ONLY use exact values from these lists for the "service" field.
AWS Services:
<AWS_SERVICES_PLACEHOLDER>
User and Client Actors:
<USER_ACTORS_PLACEHOLDER>
## MULTILINGUAL TRANSLATION RULE:
Translate all output text fields (notes, graph name, reasoning, etc.) into ENGLISH.
## WORLD MODEL (BASE INPUT):
This is your inventory of what is on the whiteboard: `entities` are the drawn components and `visual_connections` are the drawn arrows. Both lists are AUTHORITATIVE.
<WORLD_MODEL_PLACEHOLDER>
## CONNECTION LEDGER (CRITICAL - APPLY BEFORE ANY OTHER EDGE RULE):
Every entry of `visual_connections` is one arrow that was observed. Transcribe it; do not re-derive it from the audio.
1. **One edge per entry:** Emit exactly one edge for each `visual_connections` entry, with the same source and the same target, even when its description is empty.
2. **Both directions are two arrows:** If the list contains A -> B and also B -> A, emit BOTH edges. Never keep only the direction that the audio happens to describe.
3. **Repeated pairs are distinct steps:** If the same source -> target pair is listed N times, emit N edges (they are different steps or flows) and give each its own `flow_id` / `seq`. Never deduplicate.
4. **Fusion keeps arrows:** If Node Rule 4 fuses several entities into one node, re-attach every one of their connections to the fused node. Fusing nodes never removes edges.
5. **Audio assigns, it does not delete:** Use the transcript to decide the `flow_id`, `seq`, `type` and `notes` of each ledger edge. A connection the audio does not mention is still emitted (use type "data" and an empty note when nothing is known).
6. **Ledger edges are exempt from pruning and re-routing:** No rule below may remove a ledger edge, remove one of its endpoints, or redirect it through another node.
7. **Self-check:** In `step_by_step_reasoning`, state the number of `visual_connections` entries and the number of edges you emit. The second number must not be smaller than the first.
## NODE RULES (PRUNING, FUSION, AND AUDIO-DRIVEN EXPANSION):
1. **Strict Normalization & Third-Party Abstraction (CRITICAL):** The "service" field MUST match exactly with the VALID VOCABULARY LISTS. Non-native AWS services, databases, or external integrations MUST use the generic `ThirdParty` service type.
2. **Numeric Identifiers:** The "id" field of each node MUST be strictly a sequential integer in string format (e.g., "0", "1", "2").
3. **Audio-Driven Expansion (CRITICAL OVERRIDE):** If the visual World Model shows a generic abstraction (e.g., a single "AWS" cloud icon), but the audio transcript explicitly lists specific services belonging to that group, you MUST expand the generic visual node into separate, individual nodes for each explicitly mentioned service.
4. **Dynamic Logical Fusion:** Evaluate multiple icons of the same service dynamically. If they act as a single logical unit, FUSE them. If they perform distinct architectural steps (e.g., three Lambda functions doing different processing stages), KEEP THEM SEPARATE as distinct nodes.
5. **Pruning:** Remove generic human actors or purely physical concepts. Keep system entry points.
6. **Note Assimilation:** Extract specific constraints and metrics from the transcript and inject them into the "notes".
## EDGE AND FLOW RULES (LOGICAL ROUTING):
1. **Strict Flow Segmentation (`flow_id`):** Group related architectural actions into distinct logical workflows using an integer `flow_id` (starting at 0).
2. **Chronological Sequence (`seq`):** Order events within a flow using string integers ("0", "1"). Use the prime character for parallel actions.
3. **Edge Types (`type`):** Use "data" for payload transfers/reads/writes. Use "control" for events, triggers, or asynchronous invocations. Use "meta" for feedback loops, acknowledgments, polling, or monitoring connections.

## TOPOLOGY & CONTAINMENT RULES:
- **Hosted Software & Substrates:** When third-party software (e.g., Kafka, Metron, Nginx) runs on top of compute hosts (EC2, ECS), preserve the host node if explicitly mentioned, but route logical application flows directly to/from the functional service entity.
- **No Unused Deployment Layers:** Omit infrastructure management layers (e.g., CloudFormation) unless explicitly described as active runtime triggers.

## EVIDENCE-BALANCED EDGE GENERATION:
- **Ledger First, Then Verbal Grounding:** The connection ledger is the primary evidence for edges. An edge that is NOT in the ledger may be added only when the transcript explicitly states that flow (e.g., "sends to", "triggers", "stores in").
- **Completeness:** Ensure that every active service node identified is connected to the graph if a logical flow is described in the audio, avoiding orphan nodes while preventing unmentioned canonical edge hallucinations.

## STRICT EDGE ROUTING & DIRECTIONALITY:
- **Direction Comes From the Ledger:** Keep the direction of every `visual_connections` entry. Do not drop a reverse edge that is in the ledger, and do not add a reverse edge that is neither in the ledger nor explicitly stated.
- **Exact Edge Type Mapping:** Accurately differentiate `data` (direct payloads), `control` (triggers, orchestration, events), and `meta` (monitoring, feedback).
- **No Intermediate Shortcuts:** Preserve exact path routing. Do not bypass intermediate nodes.

````

## Esquema de salida

```json
{
  "$defs": {
    "Edge": {
      "properties": {
        "source": {
          "title": "Source",
          "type": "string"
        },
        "target": {
          "title": "Target",
          "type": "string"
        },
        "flow_id": {
          "title": "Flow Id",
          "type": "integer"
        },
        "seq": {
          "title": "Seq",
          "type": "string"
        },
        "type": {
          "title": "Type",
          "type": "string"
        },
        "notes": {
          "title": "Notes",
          "type": "string"
        }
      },
      "required": [
        "source",
        "target",
        "flow_id",
        "seq",
        "type",
        "notes"
      ],
      "title": "Edge",
      "type": "object"
    },
    "GraphMetadata": {
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "link": {
          "title": "Link",
          "type": "string"
        },
        "categories": {
          "title": "Categories",
          "type": "string"
        },
        "graph_usable": {
          "title": "Graph Usable",
          "type": "boolean"
        },
        "notes": {
          "title": "Notes",
          "type": "string"
        }
      },
      "required": [
        "name",
        "link",
        "categories",
        "graph_usable",
        "notes"
      ],
      "title": "GraphMetadata",
      "type": "object"
    },
    "Node": {
      "properties": {
        "id": {
          "title": "Id",
          "type": "string"
        },
        "service": {
          "title": "Service",
          "type": "string"
        },
        "name": {
          "title": "Name",
          "type": "string"
        },
        "notes": {
          "title": "Notes",
          "type": "string"
        }
      },
      "required": [
        "id",
        "service",
        "name",
        "notes"
      ],
      "title": "Node",
      "type": "object"
    }
  },
  "properties": {
    "step_by_step_reasoning": {
      "title": "Step By Step Reasoning",
      "type": "string"
    },
    "graph": {
      "$ref": "#/$defs/GraphMetadata"
    },
    "nodes": {
      "items": {
        "$ref": "#/$defs/Node"
      },
      "title": "Nodes",
      "type": "array"
    },
    "edges": {
      "items": {
        "$ref": "#/$defs/Edge"
      },
      "title": "Edges",
      "type": "array"
    }
  },
  "required": [
    "step_by_step_reasoning",
    "graph",
    "nodes",
    "edges"
  ],
  "title": "FinalArchitectureSchema",
  "type": "object"
}
```
