# Historial de Prompts y Rendimiento - Modelo Parsimonioso

Este documento actúa como un registro histórico de los prompts de parsimonia y el rendimiento de las evaluaciones en el laboratorio. Su propósito es trackear los experimentos y modificaciones del prompt parsimonioso para optimizar las métricas (Service F1, Edge F1, etc.) frente al Ground Truth.

---

## [Registro 1] - 2026-07-23
* **Video Evaluado:** `-3lnf5lzsH0`
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 14 | 9 | **9** |
| **Número de Aristas** | 16 | 15 | 9 | **9** |
| **Service F1 (Unique)** | — | 95.7% | 73.7% | **63.2%** |
| **Service Precision** | — | 100.0% | 100.0% | **85.7%** |
| **Service Recall** | — | 91.7% | 58.3% | **50.0%** |
| **Edge F1 (Connections)** | — | 38.7% | 24.0% | **24.0%** |
| **Edge Precision** | — | 40.0% | 33.3% | **33.3%** |
| **Edge Recall** | — | 37.5% | 18.8% | **18.8%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['CloudTrail', 'GuardDuty', 'OnPremDC', 'SNS', 'SQS', 'UserCompanyAnalyst']`
* **Servicios Alucinados (Inventados):** `['UserCompanyAgent']`
* **Comparación cualitativa:** 
  * El modelo mantiene exactamente el mismo tamaño simplificado del original parsimonioso (9 nodos y 9 aristas).
  * Sin embargo, omitió `OnPremDC` y `UserCompanyAnalyst` que sí detectó el parsimonioso original, e introdujo un actor alucinado `UserCompanyAgent`.
  * La precisión de bordes (aristas) se mantiene idéntica en 24.0% F1.
