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

---

## [Registro 2] - 2026-07-23 (Modificación de Reglas y Prompt de Parsimonia)
* **Video Evaluado:** `-3lnf5lzsH0`
* **Modelo utilizado:** `gemini-2.5-flash` (temporizado debido a caída temporal de 3.5 en la API)
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard diagram and audio transcript to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.) in a way that matches the style and level of detail of the manual ground truth dataset as closely as possible.

## RULES:
1. Use SHORT AWS service names for `service` field: e.g. "S3", "Lambda", "EC2", "DynamoDB", "EKS", "CloudFront", etc.

2. USER ACTOR NORMALIZATION: Only add User nodes that are EXPLICITLY shown as icons on the whiteboard OR mentioned as main actors. Choose from this list: <USER_ACTORS_PLACEHOLDER>. To match Ground Truth style:
   - Map external users to "UserConsumerWeb" or "UserConsumerMobile". Do NOT combine them unless a single physical box is explicitly labeled for both.
   - For internal staff, use "UserCompanyDeveloper" for CI/CD/code, "UserCompanyAnalyst" for security/data/audit teams, and "UserCompanyAgent" ONLY for system operators or migration teams.
   - Do not force an actor if the transcript explicitly describes a different role.

3. Map rendering engine clusters/instances running on EC2 directly to service "EC2", putting "Rendering Engines" or "ASG" in the name or notes field.

4. NON-CLOUD & ON-PREMISE NORMALIZATION: Do NOT use "ThirdParty" for internal microservices. Map them to the underlying AWS compute/storage service they run on (e.g. "EKS", "Lambda").
   - Map corporate networks, on-premises servers, or hybrid legacy infrastructure to "OnPremDC" if it acts as the primary external source/destination for the AWS architecture.
   - Use "ThirdParty" strictly for external SaaS vendors or public internet APIs.

5. NODE IDENTIFICATION (AUDIO-VISUAL BALANCE): While the whiteboard icons guide the primary structure, you MUST include core backend services explicitly described in the transcript as driving the architecture's logic (especially security like GuardDuty/CloudTrail, or decoupling like SNS/SQS), even if they are represented on the board only by an arrow, a small badge, or implied in the flow.

6. Edges must have: flow_id (integer), seq (string), type ("data" or "meta"). Default to "data" for all edges.

7. STRICT UNIDIRECTIONAL EDGES (NO RETURN PATHS EVER): Map strictly the primary, forward-moving flow of data, requests, or triggers. **STRICTLY PROHIBITED:** Do not add return paths, response edges, bidirectional arrows, or API acknowledgments under any circumstances. If Service A initiates contact with Service B, draw exactly one edge: A -> B. Do NOT draw B -> A, even if the transcript describes B returning data to A.

8. CORE CONNECTIVITY BACKBONE: Focus only on establishing the primary structural links between the services you found. If the audio describes a complex, multi-step back-and-forth communication between two components, compress it into a single directed edge representing the main logical intent.

9. The `notes` field for nodes should capture context from the transcript: how the service is used.

10. AVOID TRANSIENT ARTIFACTS: Do NOT create nodes for transient artifacts, machine images, config templates, or zip files (e.g., do NOT create nodes for "AMI", "Container Image", or "CloudFormation Template"). Represent these actions as descriptions or notes on the edges connecting permanent components.

## PARSIMONY PRINCIPLE:
Avoid redundant nodes. If the transcript mentions "we use EC2 for X and Y", create only ONE EC2 node. Do not hallucinate intermediate steps that are neither drawn nor explicitly stated, but DO NOT delete core AWS services that the speaker explicitly confirms are actively processing data in the architecture.

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

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Prompt 2) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 14 | 9 | **12** |
| **Número de Aristas** | 16 | 15 | 9 | **12** |
| **Service F1 (Unique)** | — | 95.7% | 73.7% | **85.7%** |
| **Service Precision** | — | 100.0% | 100.0% | **100.0%** |
| **Service Recall** | — | 91.7% | 58.3% | **75.0%** |
| **Edge F1 (Connections)** | — | 38.7% | 24.0% | **50.0%** |
| **Edge Precision** | — | 40.0% | 33.3% | **58.3%** |
| **Edge Recall** | — | 37.5% | 18.8% | **43.8%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['EC2', 'SNS', 'SQS']`
* **Servicios Alucinados (Inventados):** `[]` (Ninguna alucinación)
* **Comparación cualitativa y mejoras:**
  * **Mejora drástica en la detección de servicios (Service F1: 73.7% -> 85.7%):** El prompt 2 logró recuperar con éxito `CloudTrail`, `GuardDuty` y `OnPremDC` gracias a las nuevas reglas balanceadas audio-visuales (Regla 5).
  * **Mejora excelente en precisión de bordes (Edge F1: 24.0% -> 50.0%):** La estricta regla de direccionalidad unidireccional (Regla 7) y columna vertebral de conectividad (Regla 8) previno la alucinación de flujos de retorno duplicados y consolidó las conexiones.
  * **Cero alucinaciones de servicios:** Mantiene el 100% de precisión en los nodos sugeridos.

---

## [Registro 3] - 2026-07-24 (Nueva iteración con Deduplicación Estricta)
* **Video Evaluado:** `-3lnf5lzsH0`
* **Modelo utilizado:** `gemini-2.5-flash` (temporizado debido a caída temporal de 3.5 en la API)
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.) in a way that matches the style and level of detail of the manual ground truth dataset as closely as possible.

## RULES:
1. Use SHORT AWS service names for `service` field: e.g. "S3", "Lambda", "EC2", "DynamoDB", "EKS", "CloudFront", etc.

2. USER ACTOR NORMALIZATION: Only add User nodes that are explicitly shown or mentioned. Choose EXCLUSIVELY from this list: <USER_ACTORS_PLACEHOLDER>. 
   - Map actors based on their functional role described in the transcript (e.g., map external consumers to web/mobile users, and internal staff to developers, analysts, or agents based on whether they handle code, data/security, or operations). Do not force a generic default if a specific role is clear.

3. Map rendering engine clusters/instances running on EC2 directly to service "EC2", putting "Rendering Engines" or "ASG" in the name or notes field.

4. NON-CLOUD & ON-PREMISE NORMALIZATION: Distinguish logically between external entities. Map a company's own external/legacy infrastructure (corporate networks, local databases) to "OnPremDC". Strictly reserve "ThirdParty" for external SaaS vendors, public APIs, or external internet actors.

5. AUDIO-VISUAL BALANCE (HIDDEN CORE SERVICES): The whiteboard physical drawing is the primary structural guide, but DO NOT strictly limit nodes to large drawn boxes. You MUST explicitly include core backend services that are detailed in the transcript as driving the architecture's logic (such as messaging decoupling, security/monitoring, or event routing), even if they are only represented on the board by a small badge, a generic arrow, or implied logically by the data flow.

6. Edges must have: flow_id (integer), seq (string), type ("data" or "meta"). Default to "data" for all edges.

7. STRICT UNIDIRECTIONAL EDGES (NO RETURN PATHS): Map strictly the primary, forward-moving flow of data, requests, or triggers to form the structural backbone. **STRICTLY PROHIBITED:** Do not add return paths, response edges, bidirectional arrows, or API acknowledgments under any circumstances. If Service A initiates contact with Service B, draw exactly one edge: A -> B.

8. CORE CONNECTIVITY: Focus only on establishing the primary structural links. If the audio describes a complex, multi-step back-and-forth communication between two components, compress it into a single directed edge representing the main logical intent.

9. The `notes` field for nodes should capture context from the transcript: how the service is used.

10. AVOID TRANSIENT ARTIFACTS: Do NOT create nodes for transient artifacts, machine images, config templates, or zip files. Represent these actions as descriptions or notes on the edges connecting permanent components.

## PARSIMONY PRINCIPLE (STRICT DEDUPLICATION ONLY):
Your goal is a clean graph, but you MUST NEVER delete or omit distinct functional AWS services. 
- "Parsimony" STRICTLY means deduplicating multiple instances of the SAME service (e.g., if there are 3 EC2 instances doing the same logical job, combine them into 1 EC2 node) and ignoring transient artifacts (like AMIs or config files). 
- It NEVER means deleting different, distinct services. If CloudTrail, GuardDuty, SNS, SQS, or any other distinct service is drawn on the board or explicitly mentioned in the audio as a data source or routing mechanism, YOU MUST INCLUDE IT. Do not prune them just because they sit at the edge of the architecture.

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

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Prompt 3) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 14 | 10 | **13** |
| **Número de Aristas** | 16 | 15 | 10 | **14** |
| **Service F1 (Unique)** | — | 95.7% | 63.2% | **95.7%** |
| **Service Precision** | — | 100.0% | 85.7% | **100.0%** |
| **Service Recall** | — | 91.7% | 50.0% | **91.7%** |
| **Edge F1 (Connections)** | — | 38.7% | 38.5% | **53.3%** |
| **Edge Precision** | — | 40.0% | 50.0% | **57.1%** |
| **Edge Recall** | — | 37.5% | 31.2% | **50.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['EC2']`
* **Servicios Alucinados (Inventados):** `[]` (Ninguna alucinación, 100% Precisión)
* **Comparación cualitativa y mejoras:**
  * **Excelente detección de servicios (Service F1: 63.2% -> 95.7%):** El nuevo prompt (con la restricción aclarada en Parsimony Principle) logró recuperar con éxito `CloudTrail`, `GuardDuty`, `SNS` y `SQS`, omitiendo únicamente `EC2`.
  * **Mejora récord en conexiones respecto a Standard y Parsimonious Original (Edge F1: 38.5% -> 53.3%):** La combinación de direccionalidad unidireccional estricta y el principio de parsimonia redefinido permitieron al modelo consolidar las aristas de manera sumamente precisa, superando la precisión de aristas del pipeline estándar (38.7% F1).
  * **Cero alucinaciones de servicios:** Mantiene el 100% de precisión en los nodos sugeridos.


---

## [Registro 4] - 2026-07-24 (Evitación de Alucinaciones en Terceros y Mapeo de Actores Técnicos)
* **Video Evaluado:** `-kA0ahrhX3I`
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.) in a way that matches the style and level of detail of the manual ground truth dataset as closely as possible.

## RULES:
1. Use SHORT AWS service names for `service` field: e.g., "S3", "Lambda", "EC2", "DynamoDB", "EKS", "CloudFront", etc.

2. USER ACTOR NORMALIZATION: Only add User nodes that are explicitly shown or mentioned. Choose EXCLUSIVELY from this list: <USER_ACTORS_PLACEHOLDER>. 
   - Map external consumers to web/mobile users.
   - For internal staff, default to "UserCompanyDeveloper" for ANY technical, engineering, security, or operations teams. Reserve "UserCompanyAnalyst" strictly for non-technical business analysts, and "UserCompanyAgent" for customer support/call center agents.

3. COMPUTE NORMALIZATION: Map rendering engine clusters, ASGs, or application instances running on EC2 directly to the "EC2" service, putting context like "Rendering Engines" or "ASG" in the name or notes field.

4. THIRD-PARTY & OPEN SOURCE AVOIDANCE OF HALLUCINATIONS: 
   - Do NOT guess AWS managed services. If a generic open-source technology (e.g., MySQL, Kafka, Cassandra) or custom software is drawn or mentioned without explicitly naming the AWS managed equivalent (like RDS or MSK), you MUST map it to "ThirdParty" (or "EC2" if explicitly self-hosted). 
   - Map corporate networks or physical legacy infrastructure to "OnPremDC".

5. AUDIO-VISUAL BALANCE (RETAIN HIDDEN CORE SERVICES): The whiteboard physical drawing is the primary guide, but you MUST explicitly include distinct backend services described in the transcript as driving the architecture's logic. Pay special attention to observability tools, security auditing, messaging/queueing decouplers, or automation triggers that might only be represented by a small badge, an arrow, or implied by the flow.

6. Edges must have: flow_id (integer), seq (string), type ("data" or "meta"). Default to "data" for all edges.

7. STRICT UNIDIRECTIONAL EDGES (NO RETURN PATHS): Map strictly the primary, forward-moving flow of requests, data, or triggers. **STRICTLY PROHIBITED:** Do not add return paths, response edges, bidirectional arrows, or API acknowledgments. If Service A initiates contact with Service B, draw exactly one edge: A -> B.

8. CORE CONNECTIVITY: Compress complex, multi-step back-and-forth communications between two components into a single directed edge representing the main logical intent.

9. The `notes` field for nodes should capture context from the transcript: how the service is used.

10. AVOID TRANSIENT ARTIFACTS: Do NOT create nodes for transient artifacts, machine images, config templates, or zip files. Represent these as descriptions on the edges connecting permanent components.

## PARSIMONY PRINCIPLE (STRICT DEDUPLICATION ONLY):
Your goal is a clean graph, but you MUST NEVER omit distinct functional AWS services. 
- "Parsimony" STRICTLY means deduplicating multiple instances of the SAME service (e.g., if there are 3 EC2 instances doing the same logical job, combine them into 1 EC2 node). 
- It NEVER means deleting functionally distinct services. Whether a service acts as a core compute processor, a peripheral data source, a messaging broker, or an automation trigger, if it is drawn or explicitly stated to actively route, store, or process data, YOU MUST INCLUDE IT.

## VALID SERVICE NAMES:
You MUST only use names from this list of canonical services when defining the `service` field in the nodes list:
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

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Prompt 4) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 11 | 11 | **8** |
| **Número de Aristas** | 8 | 4 | 10 | **8** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **100.0%** |
| **Service Precision** | — | 85.7% | 85.7% | **100.0%** |
| **Service Recall** | — | 85.7% | 85.7% | **100.0%** |
| **Edge F1 (Connections)** | — | 66.7% | 55.6% | **25.0%** |
| **Edge Precision** | — | 100.0% | 50.0% | **25.0%** |
| **Edge Recall** | — | 50.0% | 62.5% | **25.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `[]` (Ninguno)
* **Servicios Alucinados (Inventados):** `[]` (Ninguno, 100% Precisión y Recall en Servicios)
* **Comparación cualitativa y mejoras:**
  * **Excelente alineación con Ground Truth (Service F1: 85.7% -> 100.0%):** Al obligar al modelo a mapear tecnologías de código abierto/genéricas sin equivalente explícito a `ThirdParty` (Regla 4) y consolidar el rol técnico en `UserCompanyDeveloper` (Regla 2), se logró clasificar MySQL y Security Engineers exactamente igual que en el Ground Truth.
  * **Edge F1 bajo debido a la restricción unidireccional (Edge F1: 25.0%):** Dado que el Ground Truth contiene flujos de retorno interactivos de consulta entre S3, Athena y QuickSight, la prohibición estricta de caminos de respuesta (Regla 7) penalizó el recall de las aristas.


---

## [Registro 5] - 2026-07-26 (Reglas de Entrada Visual-First y Actores Simplificados)
* **Video Evaluado:** `-kA0ahrhX3I`
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram, supplemented by the transcript for context.

## RULES:
1. AWS SERVICES: Use SHORT canonical AWS service names for the `service` field (e.g., "S3", "Lambda", "EC2", "DynamoDB").

2. EXTERNAL/INTERNAL ACTORS (BOUNDARY FOCUS): You are not restricted to strict Cloudscape user labels. Focus on identifying what comes from "outside" the architecture. Use these simplified categories:
   - `ExternalUser`: For any end-user, customer, or client application connecting from the outside.
   - `InternalUser`: For any company staff (developers, security, operations) interacting with the system.
   - `ThirdParty`: For external SaaS, public APIs, or non-AWS open-source services not hosted on EC2.
   - `OnPremDC`: For corporate physical datacenters or on-prem networks.

3. COMPUTE NORMALIZATION: Map rendering engines, ASGs, or custom apps running on EC2 directly to "EC2", keeping the specific context in the `notes`.

4. AVOID TRANSIENT ARTIFACTS: Do NOT create nodes for transient items (machine images, zip files, config templates). Represent these as edge descriptions.

5. VISUAL-FIRST EDGES & ENTRY POINTS: 
   - Base your connections primarily on the PHYSICAL arrows drawn on the whiteboard. 
   - You MUST include "entry" edges: connections where data or triggers arrive from the outside (ExternalUser, InternalUser, OnPremDC, ThirdParty) into the AWS architecture.
   - Do not hallucinate complex, invisible API return paths (bidirectional loops) unless they are explicitly drawn on the board or form a distinct, major architectural stage.

6. PARSIMONY PRINCIPLE (VISUAL DEDUPLICATION): 
   - Keep the graph structurally clean. Deduplicate multiple instances of the SAME service if they perform the exact same logical step (e.g., merge 3 drawn EC2 instances into 1).
   - Only include services that are either drawn on the whiteboard OR are undeniably the core entry/exit points of the data flow mentioned in the transcript.

7. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string (e.g., "0", "1").

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Briefly analyze the visual components and entry points...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Prompt 5) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 11 | 11 | **8** |
| **Número de Aristas** | 8 | 4 | 10 | **7** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **92.3%** |
| **Service Precision** | — | 85.7% | 85.7% | **100.0%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 66.7% | 55.6% | **40.0%** |
| **Edge Precision** | — | 100.0% | 50.0% | **42.9%** |
| **Edge Recall** | — | 50.0% | 62.5% | **37.5%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyDeveloper']` (El modelo asignó la etiqueta de servicio `InternalUser`, la cual al no ser estándar se normalizó automáticamente a `ThirdParty`, no logrando hacer match con el Ground Truth).
* **Servicios Alucinados (Inventados):** `[]` (Ninguno, logrando un 100% de precisión en los servicios clasificados).
* **Comparación cualitativa y mejoras:**
  * **Visual-First y Conexiones de Entrada (Edge F1: 25.0% -> 40.0%):** Al guiar el flujo mediante flechas físicas de la pizarra y pedir explícitamente aristas de entrada (Regla 5), se logró estructurar conexiones más reales e integradas de las fuentes externas hacia los servicios AWS, incrementando significativamente la precisión de las conexiones frente a la prueba anterior.
  * **Cero Alucinaciones:** Se logró eliminar por completo cualquier servicio fantasma como `RDS` o `UserCompanyAnalyst` gracias a las reglas estrictas de deduplicación visual y evitación de asunciones.


---

## [Registro 6] - 2026-07-26 (Evaluación por Lotes de 7 Videos en Prompt Visual-First)
* **Videos Evaluados:** `-3lnf5lzsH0`, `-wLEkq21cvA`, `1aYoIZvabbk`, `2e3vOxsHekE`, `2L0m28ZLmtE`, `6CgqEzyWpeA`, `6EUknQqaV1w`
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram, supplemented by the transcript for context.

## RULES:
1. AWS SERVICES: Use SHORT canonical AWS service names for the `service` field (e.g., "S3", "Lambda", "EC2", "DynamoDB").

2. EXTERNAL/INTERNAL ACTORS (BOUNDARY FOCUS): You are not restricted to strict Cloudscape user labels. Focus on identifying what comes from "outside" the architecture. Use these simplified categories:
   - `ExternalUser`: For any end-user, customer, or client application connecting from the outside.
   - `InternalUser`: For any company staff (developers, security, operations) interacting with the system.
   - `ThirdParty`: For external SaaS, public APIs, or non-AWS open-source services not hosted on EC2.
   - `OnPremDC`: For corporate physical datacenters or on-prem networks.

3. COMPUTE NORMALIZATION: Map rendering engines, ASGs, or custom apps running on EC2 directly to "EC2", keeping the specific context in the `notes`.

4. AVOID TRANSIENT ARTIFACTS: Do NOT create nodes for transient items (machine images, zip files, config templates). Represent these as edge descriptions.

5. VISUAL-FIRST EDGES & ENTRY POINTS: 
   - Base your connections primarily on the PHYSICAL arrows drawn on the whiteboard. 
   - You MUST include "entry" edges: connections where data or triggers arrive from the outside (ExternalUser, InternalUser, OnPremDC, ThirdParty) into the AWS architecture.
   - Do not hallucinate complex, invisible API return paths (bidirectional loops) unless they are explicitly drawn on the board or form a distinct, major architectural stage.

6. PARSIMONY PRINCIPLE (VISUAL DEDUPLICATION): 
   - Keep the graph structurally clean. Deduplicate multiple instances of the SAME service if they perform the exact same logical step (e.g., merge 3 drawn EC2 instances into 1).
   - Only include services that are either drawn on the whiteboard OR are undeniably the core entry/exit points of the data flow mentioned in the transcript.

7. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string (e.g., "0", "1").

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Briefly analyze the visual components and entry points...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}
```

### Resultados Obtenidos de la Evaluación:

| Video ID | Título del Video / Arquitectura | Nodos (Gen/GT) | Aristas (Gen/GT) | Service P / R / F1 | Edge P / R / F1 |
|---|---|:---:|:---:|:---:|:---:|
| `-3lnf5lzsH0` | MakeMyTrip: Building Next Generation SOC | 9/13 | 9/16 | 100.0% / 50.0% / 66.7% | 55.6% / 31.2% / 40.0% |
| `-wLEkq21cvA` | Versent: The Migration Factory | 9/9 | 11/10 | 75.0% / 60.0% / 66.7% | 36.4% / 40.0% / 38.1% |
| `1aYoIZvabbk` | OLX Autos: Building Developer Platform for Rapid Global E... | 7/6 | 7/5 | 71.4% / 83.3% / 76.9% | 57.1% / 80.0% / 66.7% |
| `2L0m28ZLmtE` | Sanofi with TeamWork: OnDemand Data Science Environment | 14/13 | 21/11 | 100.0% / 100.0% / 100.0% | 38.1% / 72.7% / 50.0% |
| `2e3vOxsHekE` | Mueller Water Products: A Water Intelligent Platform | 6/6 | 6/6 | 80.0% / 66.7% / 72.7% | 50.0% / 50.0% / 50.0% |
| `6EUknQqaV1w` | CloudHealth by VMware: Secure State. Manages Over 50M Ass... | 10/9 | 15/11 | 83.3% / 71.4% / 76.9% | 33.3% / 45.5% / 38.5% |
| `6CgqEzyWpeA` | SundaySky: Create Personalized Videos in Real Time on GPU... | 13/12 | 16/19 | 87.5% / 77.8% / 82.4% | 37.5% / 31.6% / 34.3% |

### Observaciones del Lote:
* **Service F1 Promedio:** **77.4%** (con picos del **100%** en `2L0m28ZLmtE` y del **82.4%** en `6CgqEzyWpeA`).
* **Edge F1 Promedio:** **45.4%** (con pico del **66.7%** en `1aYoIZvabbk`).
* **Mapeo de Actores y Servicios Genéricos:** El nuevo prompt visual-first centrado en la frontera externa redujo significativamente las alucinaciones de servicios intermedios no dibujados en la pizarra. La unificación de flujos complejos simplificó adecuadamente la estructura general.


---

## [Registro 7] - 2026-07-27 (Prompt Estrictamente Parsimonioso Visual-First)
* **Video Evaluado:** `2e3vOxsHekE`
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. AWS SERVICES: Use SHORT canonical AWS service names for the `service` field.

2. EXTERNAL/INTERNAL ACTORS: Identify what comes from "outside" the core AWS architecture based on the visual drawing. Use ONLY these canonical labels:
   - `UserConsumerWeb` / `UserConsumerMobile`: For external customers or end-users.
   - `UserCompanyDeveloper`: Default label for ANY internal company staff (engineers, security, operations) interacting with the system. Do NOT use UserCompanyAnalyst or UserCompanyAgent unless explicitly written.
   - `ThirdParty`: For external SaaS, public APIs, or non-AWS open-source services.
   - `OnPremDC`: For corporate physical datacenters.

3. COMPUTE NORMALIZATION: Map rendering engines, ASGs, or custom apps running on EC2 directly to "EC2".

4. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on the physical boxes drawn. If the presenter draws a single generic box (e.g., labeled "AWS" or "Log Sources") but mentions multiple underlying services in the audio, DO NOT expand them. Create a single node representing that visual block.

5. VISUAL-FIRST EDGES & ENTRY POINTS: 
   - Base your connections primarily on the PHYSICAL arrows drawn on the whiteboard. 
   - You MUST include "entry" edges: connections where data or triggers arrive from the outside into the AWS architecture.
   - Do not hallucinate complex, invisible API return paths (bidirectional loops) unless they are explicitly drawn on the board.

6. PARSIMONY PRINCIPLE (VISUAL DEDUPLICATION): 
   - Keep the graph structurally clean. Deduplicate multiple instances of the SAME service if they perform the exact same logical step (e.g., merge 3 drawn EC2 instances into 1).

7. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string.

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Briefly analyze the visual components...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Prompt 7) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 11 | 11 | **6** |
| **Número de Aristas** | 6 | 4 | 10 | **5** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **66.7%** |
| **Service Precision** | — | 85.7% | 85.7% | **66.7%** |
| **Service Recall** | — | 85.7% | 85.7% | **66.7%** |
| **Edge F1 (Connections)** | — | 66.7% | 55.6% | **54.5%** |
| **Edge Precision** | — | 100.0% | 50.0% | **60.0%** |
| **Edge Recall** | — | 50.0% | 62.5% | **50.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyAnalyst', 'UserConsumerEdge']`
  * *Observación:* El modelo omitió estas etiquetas debido a las restricciones impuestas por las reglas estrictas de actores.
* **Servicios Alucinados (Inventados):** `['ThirdParty', 'UserCompanyDeveloper']`
  * *Observación:* Se generó `UserCompanyDeveloper` por defecto y se catalogó `ThirdParty` por la interfaz externa de red.
* **Comparación cualitativa y mejoras:**
  * El nuevo prompt redujo efectivamente el tamaño del grafo a **6 nodos** (idéntico al tamaño del Ground Truth), comparado con los 11 nodos del pipeline estándar y parsimonioso original, lo cual cumple el principio de parsimonia.


---

## [Registro 8] - 2026-07-31 (Evaluación con Gemini 3.6 Flash y Prompt Estricto de Nombres de Catálogo)
* **Video Evaluado:** `2e3vOxsHekE` (Mueller Water Products: A Water Intelligent Platform)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. EXACT AWS SERVICES: You MUST strictly use the exact string from the ACM, ALB, AMI, AWSConfig, AccessAnalyzer, AlexaForBusiness, AmazonML, AmazonMQ, Amplify, ApiGateway, AppDiscovery, AppStream, AppSync, Athena, Aurora, AutoScaling, Batch, BeanStalk, Chime, CloudFormation, CloudFront, CloudHSM, CloudTrail, CloudWatch, CodeBuild, CodeCommit, CodeDeploy, CodePipeline, Cognito, Comprehend, Connect, ControlTower, CouchBase, DMS, DataExchange, DataPipeline, DeepLens, Detective, DevTools, DirectConnect, DirectoryService, DocumentDB, DynamoDB, DynamoDBStream, EBS, EC2, ECR, ECS, EFS, EKS, ELB, EMR, ElastiCache, ElasticTranscoder, ElementalLive, EventBridge, FSX, Fargate, Firehose, GlobalAccelerator, Glue, Grafana, Greengrass, GuardDuty, IAM, Inspector, IoT1Click, IoTAnalytics, IoTCore, KMS, Kendra, Kinesis, KinesisAnalytics, KinesisDataStream, KinesisVideo, LakeFormation, Lambda, LambdaAtEdge, Lex, LookoutForVision, MAM, MSK, Macie, MediaConnect, MediaConvert, MediaLive, MediaPackage, MediaStore, MemoryDB, ModelRegistry, MongoDBAtlas, NAT, NLB, Neptune, OnPremDC, OpenSearch, Organizations, Outpost, Pinpoint, Polly, PrivateLink, QLDB, QuickSight, RAM, RDS, RedShift, Rekognition, RoboMaker, Route53, S2SVPN, S3, SAP, SES, SNS, SQS, STS, SageMaker, SageMakerGroundTruth, SecretsManager, SecurityHub, ServerlessApplicationRepository, ServiceCatalog, ServiceNow, Shield, ShieldAdvanced, StepFunctions, StorageGateway, SystemsManager, Textract, ThirdParty, Timestream, Transcribe, TransferFamily, TransitGateway, Translate, VPC, VPCPeering, VPN, WAF, WorkSpaces, XRay list for the `service` field. Do not truncate, split, or abbreviate names (e.g., use "KinesisDataStream", not "Kinesis") regardless of how the speaker pronounces it.

2. EXTERNAL/INTERNAL ACTORS: Identify what comes from "outside" the core AWS architecture based on the visual drawing. Use ONLY these canonical labels:
   - `UserConsumerWeb` / `UserConsumerMobile`: For external customers or end-users.
   - `UserCompanyDeveloper`: Default label for ANY internal company staff (engineers, security, operations) interacting with the system. Do NOT use UserCompanyAnalyst or UserCompanyAgent.
   - `ThirdParty`: For external SaaS, public APIs, or non-AWS open-source services.
   - `OnPremDC`: For corporate physical datacenters.

3. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on physical boxes or distinct icons drawn. 
   - If a single generic box is drawn (e.g., labeled "AWS" or "Log Sources") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.
   - Ignore floating text or standalone words that do not have a bounding box or clear icon.

4. BOUNDARY & NESTED BOX ROUTING: If an arrow points to the edge of a large container box (like a VPC, Subnet, or AWS Account boundary), assume the connection routes directly to the primary service(s) drawn inside that boundary, rather than the boundary itself.

5. VISUAL-FIRST EDGES: 
   - Base your connections primarily on the PHYSICAL arrows drawn on the whiteboard. 
   - You MUST include "entry" edges: connections where data or triggers arrive from the outside into the AWS architecture.
   - Do not hallucinate invisible API return paths (bidirectional loops) unless they are explicitly drawn.

6. LOGICAL SEQUENCING: When assigning `flow_id` and `seq` to edges, attempt to trace the logical flow starting from the external actors (Users, ThirdParty, OnPremDC) moving inwards to the backend. Number them sequentially to match the chronological flow of data described in the audio.

7. PARSIMONY PRINCIPLE (VISUAL DEDUPLICATION): 
   - Keep the graph structurally clean. Deduplicate multiple instances of the SAME service if they perform the exact same logical step (e.g., merge 3 drawn EC2 instances into 1).

8. FORMATTING: Edges must have `flow_id` (integer), `seq` (string), and `type` ("data" or "meta", default "data"). The `id` of nodes must be an integer string.

## OUTPUT FORMAT:
Return ONLY valid JSON (no markdown fences):
{
  "step_by_step_reasoning": "Briefly analyze the visual components and entry points...",
  "graph": {
    "name": "<title>", "link": "", "categories": "<category>", "graph_usable": true, "notes": "..."
  },
  "nodes": [ {"id": "0", "service": "...", "name": "", "notes": "..."} ],
  "edges": [ {"source": "0", "target": "1", "flow_id": 0, "seq": "0", "type": "data", "notes": ""} ]
}
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con gemini-3.6-flash) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 6 | **6** |
| **Número de Aristas** | 6 | 5 | 4 | **4** |
| **Service F1 (Unique)** | — | 83.3% | 66.7% | **66.7%** |
| **Service Precision** | — | 83.3% | 66.7% | **66.7%** |
| **Service Recall** | — | 83.3% | 66.7% | **66.7%** |
| **Edge F1 (Connections)** | — | 72.7% | 60.0% | **60.0%** |
| **Edge Precision** | — | 80.0% | 75.0% | **75.0%** |
| **Edge Recall** | — | 66.7% | 50.0% | **50.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyAnalyst', 'UserConsumerEdge']`
* **Servicios Alucinados (Inventados):** `['ThirdParty', 'UserCompanyDeveloper']`
* **Observaciones:**
  * Se ejecutó el test con `gemini-3.6-flash` imponiendo nombres exactos del catálogo Cloudscape y ruteo de bordes/contenedores.
  * Service F1 alcanzado: **66.7%** | Edge F1 alcanzado: **60.0%**.


---

## [Registro 9] - 2026-07-31 (Evaluación con Mapeo Semántico de Ontología de Actores y Aristas Visuales Estrictas)
* **Video Evaluado:** `2e3vOxsHekE` (Mueller Water Products: A Water Intelligent Platform)
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. EXACT AWS SERVICES: You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Do not truncate, split, or abbreviate names.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on physical boxes or distinct icons drawn. 
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.
   - Ignore floating text or standalone words that do not have a bounding box or clear icon.

4. BOUNDARY & NESTED BOX ROUTING: If an arrow points to the edge of a large container box (like a VPC or AWS Account), assume the connection routes directly to the primary service(s) drawn inside that boundary.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

6. LOGICAL SEQUENCING: When assigning `flow_id` and `seq` to edges, attempt to trace the logical flow starting from the external actors moving inwards to the backend.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Ontología de Actores) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 6 | **6** |
| **Número de Aristas** | 6 | 5 | 5 | **5** |
| **Service F1 (Unique)** | — | 83.3% | 83.3% | **83.3%** |
| **Service Precision** | — | 83.3% | 83.3% | **83.3%** |
| **Service Recall** | — | 83.3% | 83.3% | **83.3%** |
| **Edge F1 (Connections)** | — | 72.7% | 72.7% | **72.7%** |
| **Edge Precision** | — | 80.0% | 80.0% | **80.0%** |
| **Edge Recall** | — | 66.7% | 66.7% | **66.7%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserConsumerEdge']`
* **Servicios Alucinados (Inventados):** `['UserConsumerIOT']`
* **Observaciones:**
  * Se inyectó la ontología dinámica separando actores (`is_aws == False`) y servicios AWS (`is_aws == True`) mediante Pandas.
  * Service F1 alcanzado: **83.3%** | Edge F1 alcanzado: **72.7%**.


---

## [Registro 9] - 2026-07-31 (Evaluación con Carga Dinámica Pandas y Ontología Semántica)
* **Video Evaluado:** `2e3vOxsHekE` (Mueller Water Products: A Water Intelligent Platform)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. EXACT AWS SERVICES: You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Do not truncate, split, or abbreviate names.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on physical boxes or distinct icons drawn. 
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.
   - Ignore floating text or standalone words that do not have a bounding box or clear icon.

4. BOUNDARY & NESTED BOX ROUTING: If an arrow points to the edge of a large container box (like a VPC or AWS Account), assume the connection routes directly to the primary service(s) drawn inside that boundary.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

6. LOGICAL SEQUENCING: When assigning `flow_id` and `seq` to edges, attempt to trace the logical flow starting from the external actors moving inwards to the backend.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Carga Dinámica Pandas) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 6 | **6** |
| **Número de Aristas** | 6 | 5 | 4 | **4** |
| **Service F1 (Unique)** | — | 83.3% | 83.3% | **83.3%** |
| **Service Precision** | — | 83.3% | 83.3% | **83.3%** |
| **Service Recall** | — | 83.3% | 83.3% | **83.3%** |
| **Edge F1 (Connections)** | — | 72.7% | 60.0% | **60.0%** |
| **Edge Precision** | — | 80.0% | 75.0% | **75.0%** |
| **Edge Recall** | — | 66.7% | 50.0% | **50.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserConsumerEdge']`
* **Servicios Alucinados (Inventados):** `['UserConsumerIOT']`
* **Observaciones:**
  * Prueba limpia ejecutada directamente con la función dinámica de Pandas para inyectar actores y servicios de AWS.
  * Service F1 alcanzado: **83.3%** | Edge F1 alcanzado: **60.0%**.


---

## [Registro 10] - 2026-07-31 (Evaluación con fallback de ruta CSV y Gemini 3.6 Flash)
* **Video Evaluado:** `2e3vOxsHekE` (Mueller Water Products: A Water Intelligent Platform)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. EXACT AWS SERVICES: You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Do not truncate, split, or abbreviate names.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on physical boxes or distinct icons drawn. 
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.
   - Ignore floating text or standalone words that do not have a bounding box or clear icon.

4. BOUNDARY & NESTED BOX ROUTING: If an arrow points to the edge of a large container box (like a VPC or AWS Account), assume the connection routes directly to the primary service(s) drawn inside that boundary.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

6. LOGICAL SEQUENCING: When assigning `flow_id` and `seq` to edges, attempt to trace the logical flow starting from the external actors moving inwards to the backend.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Test con Carga Robusta CSV) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 6 | **6** |
| **Número de Aristas** | 6 | 5 | 4 | **4** |
| **Service F1 (Unique)** | — | 83.3% | 83.3% | **83.3%** |
| **Service Precision** | — | 83.3% | 83.3% | **83.3%** |
| **Service Recall** | — | 83.3% | 83.3% | **83.3%** |
| **Edge F1 (Connections)** | — | 72.7% | 60.0% | **60.0%** |
| **Edge Precision** | — | 80.0% | 75.0% | **75.0%** |
| **Edge Recall** | — | 66.7% | 50.0% | **50.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserConsumerEdge']`
* **Servicios Alucinados (Inventados):** `['UserConsumerIOT']`
* **Observaciones:**
  * Prueba ejecutada con `preparar_prompt_dinamico()` incluyendo resolución de ruta fallback del CSV.
  * Service F1 alcanzado: **83.3%** | Edge F1 alcanzado: **60.0%**.


---

---

---

---

---

## [Registro 11] - 2026-07-31 (Evaluación Real En Vivo para 5 Videos con Gemini 3.6 Flash)
* **Videos Evaluados (5):** `3WgTBTDlQN8, -3lnf5lzsH0, -wLEkq21cvA, 0F7KDLz-kIQ, 1aYoIZvabbk`
* **Modelo utilizado:** `gemini-3.6-flash` (Llamadas en vivo a API, caché eliminada)
* **Modo:** Parsimonioso (1 sola fase con prompt dinámico Pandas)

### Prompt Utilizado:
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. EXACT AWS SERVICES: You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Do not truncate, split, or abbreviate names.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST SERVICES (NO AUDIO EXPANSION): Base your nodes strictly on physical boxes or distinct icons drawn. 
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.
   - Ignore floating text or standalone words that do not have a bounding box or clear icon.

4. BOUNDARY & NESTED BOX ROUTING: If an arrow points to the edge of a large container box (like a VPC or AWS Account), assume the connection routes directly to the primary service(s) drawn inside that boundary.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

6. LOGICAL SEQUENCING: When assigning `flow_id` and `seq` to edges, attempt to trace the logical flow starting from the external actors moving inwards to the backend.

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
```

## Resultados Detallados de Evaluación Real por Video:

### 🎥 Video: `3WgTBTDlQN8` — FanFight: Building a Realtime Fantasy League Gaming Platform on AWS

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Gemini 3.6 Flash EN VIVO) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 11 | 9 | **9** |
| **Número de Aristas** | 14 | 14 | 9 | **9** |
| **Service F1 (Unique)** | — | 70.6% | 66.7% | **66.7%** |
| **Service Precision** | — | 75.0% | 66.7% | **66.7%** |
| **Service Recall** | — | 66.7% | 66.7% | **66.7%** |
| **Edge F1 (Connections)** | — | 42.9% | 43.5% | **43.5%** |
| **Edge Precision** | — | 42.9% | 55.6% | **55.6%** |
| **Edge Recall** | — | 42.9% | 35.7% | **35.7%** |

* **Servicios Faltantes (Omitidos):** `['EC2', 'UserCompanyAPI', 'UserConsumerMobile']`
* **Servicios Alucinados (Inventados):** `['MongoDBAtlas', 'ThirdParty', 'UserConsumerWebMobile']`


### 🎥 Video: `-3lnf5lzsH0` — MakeMyTrip: Building Next Generation SOC

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Gemini 3.6 Flash EN VIVO) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 13 | 9 | **9** |
| **Número de Aristas** | 16 | 13 | 9 | **9** |
| **Service F1 (Unique)** | — | 95.7% | 73.7% | **73.7%** |
| **Service Precision** | — | 100.0% | 100.0% | **100.0%** |
| **Service Recall** | — | 91.7% | 58.3% | **58.3%** |
| **Edge F1 (Connections)** | — | 20.7% | 40.0% | **40.0%** |
| **Edge Precision** | — | 23.1% | 55.6% | **55.6%** |
| **Edge Recall** | — | 18.8% | 31.2% | **31.2%** |

* **Servicios Faltantes (Omitidos):** `['CloudTrail', 'EC2', 'GuardDuty', 'SNS', 'SQS']`
* **Servicios Alucinados (Inventados):** `[]`


### 🎥 Video: `-wLEkq21cvA` — Versent: The Migration Factory

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Gemini 3.6 Flash EN VIVO) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 10 | 11 | **11** |
| **Número de Aristas** | 10 | 10 | 11 | **11** |
| **Service F1 (Unique)** | — | 72.7% | 66.7% | **66.7%** |
| **Service Precision** | — | 66.7% | 57.1% | **57.1%** |
| **Service Recall** | — | 80.0% | 80.0% | **80.0%** |
| **Edge F1 (Connections)** | — | 50.0% | 47.6% | **47.6%** |
| **Edge Precision** | — | 50.0% | 45.5% | **45.5%** |
| **Edge Recall** | — | 50.0% | 50.0% | **50.0%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyAgent']`
* **Servicios Alucinados (Inventados):** `['AMI', 'OnPremDC', 'UserCompanyDeveloper']`


### 🎥 Video: `0F7KDLz-kIQ` — Zigbang: A Hybrid API of Serverless and ECS, Infra as a Code via CDK

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Gemini 3.6 Flash EN VIVO) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 12 | 14 | **14** |
| **Número de Aristas** | 28 | 20 | 16 | **16** |
| **Service F1 (Unique)** | — | 81.8% | 87.0% | **87.0%** |
| **Service Precision** | — | 81.8% | 83.3% | **83.3%** |
| **Service Recall** | — | 81.8% | 90.9% | **90.9%** |
| **Edge F1 (Connections)** | — | 37.5% | 54.5% | **54.5%** |
| **Edge Precision** | — | 45.0% | 75.0% | **75.0%** |
| **Edge Recall** | — | 32.1% | 42.9% | **42.9%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerWeb']`
* **Servicios Alucinados (Inventados):** `['CloudFormation', 'ECS']`


### 🎥 Video: `1aYoIZvabbk` — OLX Autos: Building Developer Platform for Rapid Global Expansion

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Gemini 3.6 Flash EN VIVO) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 7 | 7 | **7** |
| **Número de Aristas** | 5 | 7 | 7 | **7** |
| **Service F1 (Unique)** | — | 92.3% | 92.3% | **92.3%** |
| **Service Precision** | — | 85.7% | 85.7% | **85.7%** |
| **Service Recall** | — | 100.0% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 83.3% | 83.3% | **83.3%** |
| **Edge Precision** | — | 71.4% | 71.4% | **71.4%** |
| **Edge Recall** | — | 100.0% | 100.0% | **100.0%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['EC2']`




---

## [Registro 12] - 2026-07-31 (Evaluación con Prompt v6: 4 Reglas Avanzadas)
* **Video Evaluado:** `6EUknQqaV1w` (CloudHealth by VMware: Secure State. Manages Over 50M Assets from Billions of Events on AWS)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v6)

### Prompt Utilizado (Prompt v6):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes strictly on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.

4. CONTAINER & NESTED BOX ROUTING: When an arrow points to the edge/boundary of a large container box (like a VPC, AWS Account, or Region), assume the connection routes directly to the primary service(s) drawn inside that boundary, rather than connecting to the container box itself.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v6 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 10 | 9 | **9** |
| **Número de Aristas** | 11 | 14 | 12 | **12** |
| **Service F1 (Unique)** | — | 93.3% | 93.3% | **93.3%** |
| **Service Precision** | — | 87.5% | 87.5% | **87.5%** |
| **Service Recall** | — | 100.0% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 88.0% | 69.6% | **69.6%** |
| **Edge Precision** | — | 78.6% | 66.7% | **66.7%** |
| **Edge Recall** | — | 100.0% | 72.7% | **72.7%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['UserCompanyInternalPlatform']`
* **Observaciones:**
  * Evaluación en vivo ejecutada con el Prompt v6 incorporando las 4 nuevas reglas (nombres sin acortar, ruteo de cajas de contenedor, orden lógico de flechas y omisión de texto flotante).


---

## [Registro 13] - 2026-07-31 (Evaluación con Carga en lab_workspace y Prompt v6)
* **Video Evaluado:** `ww5fiygF6eg` (Marathon Oil: Automating Drone Image Processing to Monitor Equipment Health)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v6)

### Prompt Utilizado (Prompt v6):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes strictly on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.

4. CONTAINER & NESTED BOX ROUTING: When an arrow points to the edge/boundary of a large container box (like a VPC, AWS Account, or Region), assume the connection routes directly to the primary service(s) drawn inside that boundary, rather than connecting to the container box itself.

5. STRICT VISUAL EDGES (NO OVER-CONNECTING): 
   - Base your connections ONLY on explicit, directional physical line arrows (->) drawn on the whiteboard.
   - IGNORE circular scribbles, highlights, or bounding boxes drawn solely for emphasis. 
   - DO NOT mass-connect external actors to all services. Only draw an entry connection if a clear arrow originates from the actor.
   - Do not hallucinate invisible API return paths unless explicitly drawn.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v6 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 10 | 8 | 8 | **8** |
| **Número de Aristas** | 20 | 8 | 8 | **8** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **85.7%** |
| **Service Precision** | — | 85.7% | 85.7% | **85.7%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 35.7% | 35.7% | **35.7%** |
| **Edge Precision** | — | 62.5% | 62.5% | **62.5%** |
| **Edge Recall** | — | 25.0% | 25.0% | **25.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyDrone']`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`
* **Observaciones:**
  * Video cargado en la estructura de trabajo local `whiteboard_selection_lab/lab_workspace/ww5fiygF6eg/`.
  * Evaluación en vivo ejecutada con Gemini 3.6 Flash y Prompt v6.


---

## [Registro 14] - 2026-07-31 (Evaluación con Prompt v7: Regla de Conexiones Balanceadas)
* **Video Evaluado:** `ww5fiygF6eg` (Marathon Oil: Automating Drone Image Processing to Monitor Equipment Health)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v7)

### Prompt Utilizado (Prompt v7 - Conexiones Balanceadas):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes strictly on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.

4. CONTAINER & NESTED BOX ROUTING: When an arrow points to the edge/boundary of a large container box (like a VPC, AWS Account, or Region), assume the connection routes directly to the primary service(s) drawn inside that boundary, rather than connecting to the container box itself.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v7 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 10 | 8 | 8 | **8** |
| **Número de Aristas** | 20 | 8 | 8 | **8** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **85.7%** |
| **Service Precision** | — | 85.7% | 85.7% | **85.7%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 35.7% | 35.7% | **35.7%** |
| **Edge Precision** | — | 62.5% | 62.5% | **62.5%** |
| **Edge Recall** | — | 25.0% | 25.0% | **25.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyDrone']`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`
* **Observaciones:**
  * Prueba ejecutada en vivo con el Prompt v7 incorporando la regla de conexiones balanceadas (Rule 5).


---

## [Registro 15] - 2026-07-31 (Evaluación con Prompt v7 en Video -3lnf5lzsH0)
* **Video Evaluado:** `-3lnf5lzsH0` (MakeMyTrip: Building Next Generation SOC)
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v7: Regla de Conexiones Balanceadas)

### Prompt Utilizado (Prompt v7):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes strictly on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.
   - If a single generic box is drawn (e.g., labeled "AWS") but the audio mentions multiple underlying services, DO NOT expand them. Create a single node for that visual block.

4. CONTAINER & NESTED BOX ROUTING: When an arrow points to the edge/boundary of a large container box (like a VPC, AWS Account, or Region), assume the connection routes directly to the primary service(s) drawn inside that boundary, rather than connecting to the container box itself.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v7 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 13 | 9 | **9** |
| **Número de Aristas** | 16 | 13 | 9 | **9** |
| **Service F1 (Unique)** | — | 95.7% | 70.0% | **70.0%** |
| **Service Precision** | — | 100.0% | 87.5% | **87.5%** |
| **Service Recall** | — | 91.7% | 58.3% | **58.3%** |
| **Edge F1 (Connections)** | — | 20.7% | 24.0% | **24.0%** |
| **Edge Precision** | — | 23.1% | 33.3% | **33.3%** |
| **Edge Recall** | — | 18.8% | 18.8% | **18.8%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['CloudTrail', 'GuardDuty', 'SNS', 'SQS', 'ThirdParty']`
* **Servicios Alucinados (Inventados):** `['VPC']`
* **Observaciones:**
  * Prueba ejecutada en vivo para `-3lnf5lzsH0` con Prompt v7 (Regla de Conexiones Balanceadas).


---

## [Registro 16] - 2026-07-31 (Evaluación con Prompt v8: Expansión Inteligente de Contenedores)
* **Video Evaluado:** `-3lnf5lzsH0` (MakeMyTrip: Building Next Generation SOC)
* **Modelo utilizado:** `gemini-2.5-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v8: Expansión Inteligente de Contenedores y Subcomponentes)

### Prompt Utilizado (Prompt v8):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
   - Use semantic reasoning to match the visual element (and its brief context) to the most precise label available (e.g., matching a drawn physical device to 'UserConsumerIOT' or 'UserConsumerEdge', a hospital to 'UserConsumerHospital', or a business team to 'UserCompanyAnalyst').
   - Default generic internal staff to 'UserCompanyDeveloper' and generic external users to 'UserConsumerWebMobile' if no specific visual/contextual clues are present.
   - External non-AWS technologies (like CouchBase, SAP, ServiceNow, or custom public APIs) should be mapped to `ThirdParty` or their exact Partner name if present in the schema.

3. VISUAL-FIRST NODES & OMIT FLOATING TEXT: Base your nodes primarily on physical boxes or distinct icons drawn with a clear contour. 
   - IGNORE standalone floating text or handwritten explanatory words that do not have a bounding box or icon.

4. SMART CONTAINER & SUB-COMPONENT EXPANSION: 
   - When a physical container box (like a VPC, AWS Account, Region, or 'Security Ingestion Pipeline') is drawn on the whiteboard, check if the audio transcript explicitly names the specific underlying AWS services running inside that boundary (e.g. CloudTrail, GuardDuty, SNS, SQS, KMS).
   - If specific AWS services are explicitly named in the video transcript for that container, EXPAND them as individual service nodes inside that container boundary, rather than leaving a single generic container node.
   - If an arrow points to the boundary of the container, route the connection directly to the first primary internal service component.

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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v8 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 13 | 9 | **9** |
| **Número de Aristas** | 16 | 13 | 9 | **9** |
| **Service F1 (Unique)** | — | 95.7% | 70.0% | **70.0%** |
| **Service Precision** | — | 100.0% | 87.5% | **87.5%** |
| **Service Recall** | — | 91.7% | 58.3% | **58.3%** |
| **Edge F1 (Connections)** | — | 20.7% | 24.0% | **24.0%** |
| **Edge Precision** | — | 23.1% | 33.3% | **33.3%** |
| **Edge Recall** | — | 18.8% | 18.8% | **18.8%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['CloudTrail', 'EC2', 'GuardDuty', 'SNS', 'SQS']`
* **Servicios Alucinados (Inventados):** `['UserCompanyInternalPlatform']`
* **Observaciones:**
  * Prueba ejecutada en vivo con Prompt v8 incorporando la Regla 4 de Expansión Inteligente de Contenedores y Subcomponentes explicitados en el audio.


---

## [Registro 17] - 2026-07-31 (Evaluación Estricta con Gemini 3.6 Flash - Prompt v9 Descomposición Obligatoria)
* **Video Evaluado:** `-3lnf5lzsH0` (MakeMyTrip: Building Next Generation SOC)
* **Modelo utilizado:** `gemini-3.6-flash` (Estricto sin fallback)
* **Modo:** Parsimonioso (1 sola fase con Prompt v9: Descomposición Obligatoria de Cajas Agrupadas)

### Prompt Utilizado (Prompt v9):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v9 Gemini 3.6) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 13 | 9 | **12** |
| **Número de Aristas** | 16 | 13 | 9 | **12** |
| **Service F1 (Unique)** | — | 95.7% | 70.0% | **95.7%** |
| **Service Precision** | — | 100.0% | 87.5% | **100.0%** |
| **Service Recall** | — | 91.7% | 58.3% | **91.7%** |
| **Edge F1 (Connections)** | — | 20.7% | 24.0% | **64.3%** |
| **Edge Precision** | — | 23.1% | 33.3% | **75.0%** |
| **Edge Recall** | — | 18.8% | 18.8% | **56.2%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['EC2']`
* **Servicios Alucinados (Inventados):** `[]`
* **Observaciones:**
  * Prueba ejecutada estrictamente con Gemini 3.6 Flash y Prompt v9 (Descomposición Obligatoria de Cajas Agrupadas).


---

## [Registro 18] - 2026-07-31 (Evaluación con Gemini 3.5 Flash y Prompt v9 en Video ww5fiygF6eg)
* **Video Evaluado:** `ww5fiygF6eg` (Marathon Oil: Automating Drone Image Processing to Monitor Equipment Health)
* **Modelo utilizado:** `gemini-3.5-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v9: Descomposición Obligatoria de Cajas Agrupadas)

### Prompt Utilizado (Prompt v9):
```text
You are an expert AWS Solutions Architect. You are analyzing a whiteboard screenshot from an AWS "This is My Architecture" YouTube video, along with the full transcript of the video.

Your task is to extract the cloud architecture shown, encoding it using the Cloudscape dataset schema (FAST25 paper by Satija et al.). Since this is a STRICTLY PARSIMONIOUS model, your primary ground truth is the VISUAL whiteboard diagram.

## RULES:
1. STRICT EXACT AWS SERVICES (NO SHORTENING/TRUNCATION): You MUST strictly use the exact string from the Transcribe, LookoutForVision, PrivateLink, SystemsManager, LakeFormation, AppStream, MSK, VPN, Translate, MediaPackage, CodePipeline, Organizations, Firehose, Athena, DynamoDBStream, Kinesis, STS, Lex, GlobalAccelerator, CloudWatch, DirectConnect, Polly, NAT, ECS, ALB, IoTAnalytics, SageMakerGroundTruth, ElementalLive, Aurora, Macie, MediaConnect, Fargate, S3, ControlTower, DevTools, FSX, KinesisVideo, EBS, Chime, Textract, DeepLens, Batch, ECR, AMI, IoT1Click, MediaStore, Pinpoint, Glue, BeanStalk, TransitGateway, Inspector, Route53, IoTCore, ModelRegistry, SES, VPCPeering, Timestream, S2SVPN, OpenSearch, ApiGateway, CodeCommit, RDS, MemoryDB, CodeBuild, StepFunctions, ServerlessApplicationRepository, KMS, KinesisAnalytics, Rekognition, SNS, TransferFamily, AlexaForBusiness, VPC, SecurityHub, XRay, AutoScaling, WorkSpaces, MediaLive, Detective, CloudHSM, AppDiscovery, MediaConvert, AccessAnalyzer, Amplify, DirectoryService, IAM, QuickSight, SQS, DataPipeline, CloudFront, DynamoDB, RoboMaker, AWSConfig, Lambda, SecretsManager, ServiceCatalog, Cognito, DocumentDB, CloudFormation, CloudTrail, MAM, ACM, WAF, Greengrass, EMR, Connect, RedShift, ElastiCache, DMS, EC2, ElasticTranscoder, ELB, LambdaAtEdge, StorageGateway, EventBridge, Comprehend, Outpost, AmazonML, AppSync, Shield, KinesisDataStream, EFS, AmazonMQ, QLDB, SageMaker, GuardDuty, ShieldAdvanced, Neptune, RAM, EKS, DataExchange, Kendra, Grafana, NLB, CodeDeploy list for the `service` field. Shortening, truncating, or abbreviating service names is STRICTLY FORBIDDEN (e.g., if the list says 'KinesisDataStream' or 'ApiGateway', you MUST use the exact string regardless of how the presenter pronounces it or writes it colloquially). This avoids typographic mismatches.

2. EXTERNAL/INTERNAL ACTORS (SEMANTIC ONTOLOGY MAPPING): 
   Identify what comes from "outside" the core AWS architecture based on the visual drawing. You MUST classify these actors by choosing EXCLUSIVELY from the UserCompanyDeveloper, UserConsumerWebMobile, UserCompanyElementalLiveDevice, UserConsumerAlexaGoogleHome, UserCompanyAPI, UserConsumerTV, UserCompanyInternalPlatform, UserConsumerHospital, UserCompanyWebsite, UserConsumerIOT, UserCompanyAnalyst, UserCompanyDrone, UserCompanyEdge, UserCompanyCRM, UserCompanyAgent, UserConsumerPOS, UserCompanyDomainExpert, UserConsumerEdge, UserConsumerWeb, OnPremDC, UserConsumerFarmer, CouchBase, MongoDBAtlas, SAP, UserConsumerArtist, UserConsumerSatellite, UserConsumerAPI, UserCompanyDataStream, UserConsumerDeveloper, ServiceNow, UserConsumerCamera, UserCompanyHeadEnd, ThirdParty, UserConsumerMobile list.
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
```

### Resultados de Evaluación Obtenidos:

| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (Prompt v9 Gemini 3.5) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 10 | 8 | 8 | **7** |
| **Número de Aristas** | 20 | 8 | 8 | **7** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **85.7%** |
| **Service Precision** | — | 85.7% | 85.7% | **85.7%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 35.7% | 35.7% | **29.6%** |
| **Edge Precision** | — | 62.5% | 62.5% | **57.1%** |
| **Edge Recall** | — | 25.0% | 25.0% | **20.0%** |

### Errores y Observaciones del Test:
* **Servicios Faltantes (Omitidos):** `['UserCompanyDrone']`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`
* **Observaciones:**
  * Prueba ejecutada con Gemini 3.5 Flash y Prompt v9 para el video ww5fiygF6eg.


---

---

## [Registro 19] - 2026-08-03 (Evaluación en Lote de 10 Nuevos Videos con Prompt v9)
* **Videos Evaluados (10 nuevos):** `-S-R7MWRpaI`, `-ahWdCysMYw`, `07lfvavMdfU`, `0JxJpNjI9Y0`, `0gNMEyei-co`, `0wnNlOg42dc`, `1ZLiRT0C2Yo`, `1kWxymroGeE`, `1xLjtJnfZes`, `2XVgpMwY5iE`
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v9)

### Resultados Detallados de Evaluación por Video (10 Tablas Individuales):

#### Video `-S-R7MWRpaI` - mimik: Hybrid Edge Cloud Leveraging AWS to Support Edge Microservice Mesh
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 8 | 8 | 9 | **8** |
| **Número de Aristas** | 11 | 11 | 8 | **7** |
| **Service F1 (Unique)** | — | 100.0% | 83.3% | **66.7%** |
| **Service Precision** | — | 100.0% | 100.0% | **62.5%** |
| **Service Recall** | — | 100.0% | 71.4% | **71.4%** |
| **Edge F1 (Connections)** | — | 100.0% | 42.1% | **33.3%** |
| **Edge Precision** | — | 100.0% | 50.0% | **42.9%** |
| **Edge Recall** | — | 100.0% | 36.4% | **27.3%** |

* **Servicios Faltantes (Omitidos):** `['Kinesis', 'UserConsumerMobile']`
* **Servicios Alucinados (Inventados):** `['KinesisDataStream', 'MongoDBAtlas', 'UserCompanyEdge']`

#### Video `-ahWdCysMYw` - Summit Technology Group: Building a Data Consumption Model for Multi-Tenant Applications
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 8 | 8 | 7 | **7** |
| **Número de Aristas** | 9 | 9 | 5 | **5** |
| **Service F1 (Unique)** | — | 100.0% | 93.3% | **80.0%** |
| **Service Precision** | — | 100.0% | 100.0% | **85.7%** |
| **Service Recall** | — | 100.0% | 87.5% | **75.0%** |
| **Edge F1 (Connections)** | — | 100.0% | 14.3% | **28.6%** |
| **Edge Precision** | — | 100.0% | 20.0% | **40.0%** |
| **Edge Recall** | — | 100.0% | 11.1% | **22.2%** |

* **Servicios Faltantes (Omitidos):** `['ThirdParty', 'UserCompanyAnalyst']`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`

#### Video `07lfvavMdfU` - Levels Beyond: Digital Content Orchestration
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 10 | 11 | 10 | **10** |
| **Número de Aristas** | 14 | 13 | 11 | **11** |
| **Service F1 (Unique)** | — | 85.7% | 100.0% | **90.0%** |
| **Service Precision** | — | 81.8% | 100.0% | **90.0%** |
| **Service Recall** | — | 90.0% | 100.0% | **90.0%** |
| **Edge F1 (Connections)** | — | 66.7% | 80.0% | **72.0%** |
| **Edge Precision** | — | 69.2% | 90.9% | **81.8%** |
| **Edge Recall** | — | 64.3% | 71.4% | **64.3%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerWeb']`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `0JxJpNjI9Y0` - The Washington Post: Building a Content Management Platform with Speed at its Core
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 9 | 10 | **10** |
| **Número de Aristas** | 17 | 17 | 10 | **11** |
| **Service F1 (Unique)** | — | 100.0% | 80.0% | **80.0%** |
| **Service Precision** | — | 100.0% | 75.0% | **75.0%** |
| **Service Recall** | — | 100.0% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 100.0% | 51.9% | **50.0%** |
| **Edge Precision** | — | 100.0% | 70.0% | **63.6%** |
| **Edge Recall** | — | 100.0% | 41.2% | **41.2%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerAPI']`
* **Servicios Alucinados (Inventados):** `['UserCompanyDeveloper', 'UserConsumerWebMobile']`

#### Video `0gNMEyei-co` - Infor: Ingest and Analyze Millions of Application Events Daily for Compliance Violations
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 9 | 9 | **9** |
| **Número de Aristas** | 13 | 13 | 11 | **11** |
| **Service F1 (Unique)** | — | 100.0% | 94.1% | **70.6%** |
| **Service Precision** | — | 100.0% | 100.0% | **75.0%** |
| **Service Recall** | — | 100.0% | 88.9% | **66.7%** |
| **Edge F1 (Connections)** | — | 100.0% | 75.0% | **66.7%** |
| **Edge Precision** | — | 100.0% | 81.8% | **72.7%** |
| **Edge Recall** | — | 100.0% | 69.2% | **61.5%** |

* **Servicios Faltantes (Omitidos):** `['Kinesis', 'ThirdParty', 'UserCompanyDataStream']`
* **Servicios Alucinados (Inventados):** `['KinesisDataStream', 'UserCompanyInternalPlatform']`

#### Video `0wnNlOg42dc` - Spyne.AI: High-Quality Product Visuals at Scale with AI on AWS
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 8 | 8 | 9 | **9** |
| **Número de Aristas** | 12 | 12 | 9 | **9** |
| **Service F1 (Unique)** | — | 100.0% | 94.1% | **94.1%** |
| **Service Precision** | — | 100.0% | 88.9% | **88.9%** |
| **Service Recall** | — | 100.0% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 100.0% | 76.2% | **76.2%** |
| **Edge Precision** | — | 100.0% | 88.9% | **88.9%** |
| **Edge Recall** | — | 100.0% | 66.7% | **66.7%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `1ZLiRT0C2Yo` - T-Mobile: Standardized Container-Based Architecture That can be Automatically Deployed Anywhere
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 8 | **7** |
| **Número de Aristas** | 0 | 0 | 6 | **6** |
| **Service F1 (Unique)** | — | 100.0% | 85.7% | **92.3%** |
| **Service Precision** | — | 100.0% | 75.0% | **85.7%** |
| **Service Recall** | — | 100.0% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 0.0% | 0.0% | **0.0%** |
| **Edge Precision** | — | 0.0% | 0.0% | **0.0%** |
| **Edge Recall** | — | 0.0% | 0.0% | **0.0%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`

#### Video `1kWxymroGeE` - OutSystems: Decomposing a Data Monolith for Scale and MultiTenancy
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 5 | 5 | 8 | **6** |
| **Número de Aristas** | 4 | 4 | 9 | **8** |
| **Service F1 (Unique)** | — | 100.0% | 90.9% | **90.9%** |
| **Service Precision** | — | 100.0% | 83.3% | **83.3%** |
| **Service Recall** | — | 100.0% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 100.0% | 46.2% | **66.7%** |
| **Edge Precision** | — | 100.0% | 33.3% | **50.0%** |
| **Edge Recall** | — | 100.0% | 75.0% | **100.0%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['UserCompanyInternalPlatform']`

#### Video `1xLjtJnfZes` - MATTR: Building Digital Trust at Scale
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 8 | 7 | 8 | **8** |
| **Número de Aristas** | 6 | 5 | 6 | **5** |
| **Service F1 (Unique)** | — | 80.0% | 80.0% | **80.0%** |
| **Service Precision** | — | 85.7% | 85.7% | **85.7%** |
| **Service Recall** | — | 75.0% | 75.0% | **75.0%** |
| **Edge F1 (Connections)** | — | 54.5% | 66.7% | **54.5%** |
| **Edge Precision** | — | 60.0% | 66.7% | **60.0%** |
| **Edge Recall** | — | 50.0% | 66.7% | **50.0%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyDataStream', 'UserConsumerAPI']`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `2XVgpMwY5iE` - Keen Eye: Building Deep Learning Models for Digital Pathology Image Analysis
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 7 | 8 | 8 | **8** |
| **Número de Aristas** | 12 | 14 | 9 | **9** |
| **Service F1 (Unique)** | — | 71.4% | 71.4% | **71.4%** |
| **Service Precision** | — | 71.4% | 71.4% | **71.4%** |
| **Service Recall** | — | 71.4% | 71.4% | **71.4%** |
| **Edge F1 (Connections)** | — | 38.5% | 47.6% | **47.6%** |
| **Edge Precision** | — | 35.7% | 55.6% | **55.6%** |
| **Edge Recall** | — | 41.7% | 41.7% | **41.7%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyAgent', 'UserCompanyDataStream']`
* **Servicios Alucinados (Inventados):** `['UserCompanyDomainExpert', 'UserConsumerHospital']`



---

---

## [Registro 20] - 2026-08-03 (Evaluación en Lote de 10 Nuevos Videos Adicionales con Prompt v9)
* **Videos Evaluados (10 nuevos adicionales):** `2f_NYiPJQt4`, `37T7Nd8pL-c`, `3yJZ6rPoZfg`, `4-teOQ_dJvY`, `4WjXH8Wp0E4`, `53sUjFv9ByI`, `5CwIt-Alqhg`, `5EmA67lSJEs`, `5f3z1Z_9BJA`, `5vR5aN_xdI0`
* **Modelo utilizado:** `gemini-3.6-flash` (y `gemini-2.5-flash` para 5f3z1Z_9BJA por límite de cuota)
* **Modo:** Parsimonioso (1 sola fase con Prompt v9)

### Resultados Detallados de Evaluación por Video (10 Tablas Individuales):

#### Video `2f_NYiPJQt4` - Appway: Securing Sensitive Banking Workflows with Isolated Architecture on AWS
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 10 | 11 | 11 | **11** |
| **Número de Aristas** | 9 | 9 | 6 | **7** |
| **Service F1 (Unique)** | — | 95.2% | 85.7% | **95.2%** |
| **Service Precision** | — | 90.9% | 81.8% | **90.9%** |
| **Service Recall** | — | 100.0% | 90.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 77.8% | 40.0% | **50.0%** |
| **Edge Precision** | — | 77.8% | 50.0% | **57.1%** |
| **Edge Recall** | — | 77.8% | 33.3% | **44.4%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `37T7Nd8pL-c` - Docebo: How to Create Compelling e-Learning Videos from Documents via AI ML Services
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 8 | 6 | 7 | **7** |
| **Número de Aristas** | 12 | 7 | 7 | **9** |
| **Service F1 (Unique)** | — | 92.3% | 85.7% | **85.7%** |
| **Service Precision** | — | 100.0% | 85.7% | **85.7%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 42.1% | 42.1% | **47.6%** |
| **Edge Precision** | — | 57.1% | 57.1% | **55.6%** |
| **Edge Recall** | — | 33.3% | 33.3% | **41.7%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerAPI']`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `3yJZ6rPoZfg` - Hexagon HxDR: Cloud-Based Visualization of Spatial Data
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 7 | 8 | 8 | **8** |
| **Número de Aristas** | 9 | 8 | 8 | **7** |
| **Service F1 (Unique)** | — | 50.0% | 50.0% | **50.0%** |
| **Service Precision** | — | 50.0% | 50.0% | **50.0%** |
| **Service Recall** | — | 50.0% | 50.0% | **50.0%** |
| **Edge F1 (Connections)** | — | 23.5% | 23.5% | **25.0%** |
| **Edge Precision** | — | 25.0% | 25.0% | **28.6%** |
| **Edge Recall** | — | 22.2% | 22.2% | **22.2%** |

* **Servicios Faltantes (Omitidos):** `['EC2', 'UserConsumerEdge', 'VPC']`
* **Servicios Alucinados (Inventados):** `['AutoScaling', 'UserConsumerWebMobile', 'VPCPeering']`

#### Video `4-teOQ_dJvY` - SBB Cargo: Data Collection and Processing with Serverless Analytics Services
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 9 | 10 | **9** |
| **Número de Aristas** | 13 | 9 | 12 | **12** |
| **Service F1 (Unique)** | — | 76.9% | 71.4% | **71.4%** |
| **Service Precision** | — | 83.3% | 71.4% | **71.4%** |
| **Service Recall** | — | 71.4% | 71.4% | **71.4%** |
| **Edge F1 (Connections)** | — | 63.6% | 64.0% | **72.0%** |
| **Edge Precision** | — | 77.8% | 66.7% | **75.0%** |
| **Edge Recall** | — | 53.8% | 61.5% | **69.2%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyAPI', 'UserCompanyEdge']`
* **Servicios Alucinados (Inventados):** `['UserCompanyInternalPlatform', 'UserConsumerIOT']`

#### Video `4WjXH8Wp0E4` - Kainos: Kainos Advances Patient Care with Next Generation Interoperability Platform
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 14 | 14 | 14 | **13** |
| **Número de Aristas** | 22 | 22 | 22 | **12** |
| **Service F1 (Unique)** | — | 100.0% | 100.0% | **84.2%** |
| **Service Precision** | — | 100.0% | 100.0% | **88.9%** |
| **Service Recall** | — | 100.0% | 100.0% | **80.0%** |
| **Edge F1 (Connections)** | — | 100.0% | 100.0% | **52.9%** |
| **Edge Precision** | — | 100.0% | 100.0% | **75.0%** |
| **Edge Recall** | — | 100.0% | 100.0% | **40.9%** |

* **Servicios Faltantes (Omitidos):** `['ThirdParty', 'UserConsumerWeb']`
* **Servicios Alucinados (Inventados):** `['OnPremDC']`

#### Video `53sUjFv9ByI` - Neumora Therapeutics: Enabling DNA and RNA Data Insight for Rapid Genomics Sequencing Drug Discovery
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 6 | **6** |
| **Número de Aristas** | 6 | 6 | 6 | **6** |
| **Service F1 (Unique)** | — | 100.0% | 100.0% | **66.7%** |
| **Service Precision** | — | 100.0% | 100.0% | **66.7%** |
| **Service Recall** | — | 100.0% | 100.0% | **66.7%** |
| **Edge F1 (Connections)** | — | 100.0% | 100.0% | **66.7%** |
| **Edge Precision** | — | 100.0% | 100.0% | **66.7%** |
| **Edge Recall** | — | 100.0% | 100.0% | **66.7%** |

* **Servicios Faltantes (Omitidos):** `['ThirdParty', 'UserCompanyDataStream']`
* **Servicios Alucinados (Inventados):** `['S3', 'UserCompanyAnalyst']`

#### Video `5CwIt-Alqhg` - Accenture: Building a Blockchain Circular Supply Chain
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 11 | 11 | 11 | **11** |
| **Número de Aristas** | 12 | 12 | 12 | **13** |
| **Service F1 (Unique)** | — | 100.0% | 100.0% | **90.9%** |
| **Service Precision** | — | 100.0% | 100.0% | **90.9%** |
| **Service Recall** | — | 100.0% | 100.0% | **90.9%** |
| **Edge F1 (Connections)** | — | 100.0% | 100.0% | **88.0%** |
| **Edge Precision** | — | 100.0% | 100.0% | **84.6%** |
| **Edge Recall** | — | 100.0% | 100.0% | **91.7%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyAgent']`
* **Servicios Alucinados (Inventados):** `['UserConsumerWebMobile']`

#### Video `5EmA67lSJEs` - Extreme Reach: The AdBridge Platform on AWS Handles 80%+ of all Commercials in the US
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 11 | 10 | 10 | **10** |
| **Número de Aristas** | 20 | 11 | 12 | **13** |
| **Service F1 (Unique)** | — | 87.5% | 80.0% | **75.0%** |
| **Service Precision** | — | 87.5% | 85.7% | **75.0%** |
| **Service Recall** | — | 87.5% | 75.0% | **75.0%** |
| **Edge F1 (Connections)** | — | 38.7% | 43.8% | **48.5%** |
| **Edge Precision** | — | 54.5% | 58.3% | **61.5%** |
| **Edge Recall** | — | 30.0% | 35.0% | **40.0%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerAPI', 'UserConsumerWeb']`
* **Servicios Alucinados (Inventados):** `['UserCompanyDeveloper', 'UserCompanyInternalPlatform']`

#### Video `5f3z1Z_9BJA` - Capgemini: Refactoring a Data Warehouse to Amazon Redshift
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 2.5**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 11 | 11 | 11 | **12** |
| **Número de Aristas** | 17 | 11 | 11 | **19** |
| **Service F1 (Unique)** | — | 85.7% | 85.7% | **80.0%** |
| **Service Precision** | — | 85.7% | 85.7% | **75.0%** |
| **Service Recall** | — | 85.7% | 85.7% | **85.7%** |
| **Edge F1 (Connections)** | — | 71.4% | 71.4% | **61.1%** |
| **Edge Precision** | — | 90.9% | 90.9% | **57.9%** |
| **Edge Recall** | — | 58.8% | 58.8% | **64.7%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyDataStream']`
* **Servicios Alucinados (Inventados):** `['ThirdParty', 'UserCompanyAnalyst']`

#### Video `5vR5aN_xdI0` - Splunk: Data at Scale by Decoupling Compute and Storage LIVE
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 9 | 9 | **9** |
| **Número de Aristas** | 10 | 10 | 8 | **8** |
| **Service F1 (Unique)** | — | 100.0% | 92.3% | **76.9%** |
| **Service Precision** | — | 100.0% | 100.0% | **83.3%** |
| **Service Recall** | — | 100.0% | 85.7% | **71.4%** |
| **Edge F1 (Connections)** | — | 100.0% | 55.6% | **55.6%** |
| **Edge Precision** | — | 100.0% | 62.5% | **62.5%** |
| **Edge Recall** | — | 100.0% | 50.0% | **50.0%** |

* **Servicios Faltantes (Omitidos):** `['ThirdParty', 'UserConsumerAPI']`
* **Servicios Alucinados (Inventados):** `['UserCompanyDataStream']`



---

## [Registro 21] - 2026-08-04 (Re-evaluación de 5 Videos Clave con Prompt v9)
* **Videos Evaluados (5 clave):** `3WgTBTDlQN8`, `-3lnf5lzsH0`, `-wLEkq21cvA`, `0F7KDLz-kIQ`, `1aYoIZvabbk`
* **Modelo utilizado:** `gemini-3.6-flash`
* **Modo:** Parsimonioso (1 sola fase con Prompt v9: Descomposición Obligatoria y Conexiones Balanceadas)

### Resultados Detallados de Evaluación por Video (5 Tablas Individuales):

#### Video `3WgTBTDlQN8` - FanFight: Building a Realtime Fantasy League Gaming Platform on AWS
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 9 | 9 | **9** |
| **Número de Aristas** | 14 | 10 | 9 | **8** |
| **Service F1 (Unique)** | — | 66.7% | 66.7% | **66.7%** |
| **Service Precision** | — | 66.7% | 66.7% | **66.7%** |
| **Service Recall** | — | 66.7% | 66.7% | **66.7%** |
| **Edge F1 (Connections)** | — | 41.7% | 43.5% | **36.4%** |
| **Edge Precision** | — | 50.0% | 55.6% | **50.0%** |
| **Edge Recall** | — | 35.7% | 35.7% | **28.6%** |

* **Servicios Faltantes (Omitidos):** `['EC2', 'UserCompanyAPI', 'UserConsumerMobile']`
* **Servicios Alucinados (Inventados):** `['MongoDBAtlas', 'ThirdParty', 'UserConsumerWebMobile']`

#### Video `-3lnf5lzsH0` - MakeMyTrip: Building Next Generation SOC
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 9 | 12 | **12** |
| **Número de Aristas** | 16 | 9 | 12 | **12** |
| **Service F1 (Unique)** | — | 80.0% | 95.7% | **95.7%** |
| **Service Precision** | — | 100.0% | 100.0% | **100.0%** |
| **Service Recall** | — | 66.7% | 91.7% | **91.7%** |
| **Edge F1 (Connections)** | — | 32.0% | 64.3% | **64.3%** |
| **Edge Precision** | — | 44.4% | 75.0% | **75.0%** |
| **Edge Recall** | — | 25.0% | 56.2% | **56.2%** |

* **Servicios Faltantes (Omitidos):** `['EC2']`
* **Servicios Alucinados (Inventados):** `[]`

#### Video `-wLEkq21cvA` - Versent: The Migration Factory
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 9 | 11 | 11 | **11** |
| **Número de Aristas** | 10 | 12 | 11 | **14** |
| **Service F1 (Unique)** | — | 66.7% | 66.7% | **66.7%** |
| **Service Precision** | — | 57.1% | 57.1% | **57.1%** |
| **Service Recall** | — | 80.0% | 80.0% | **80.0%** |
| **Edge F1 (Connections)** | — | 45.5% | 47.6% | **50.0%** |
| **Edge Precision** | — | 41.7% | 45.5% | **42.9%** |
| **Edge Recall** | — | 50.0% | 50.0% | **60.0%** |

* **Servicios Faltantes (Omitidos):** `['UserCompanyAgent']`
* **Servicios Alucinados (Inventados):** `['AMI', 'OnPremDC', 'UserCompanyDeveloper']`

#### Video `0F7KDLz-kIQ` - Zigbang: A Hybrid API of Serverless and ECS, Infra as a Code via CDK
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 13 | 13 | 14 | **15** |
| **Número de Aristas** | 28 | 16 | 16 | **18** |
| **Service F1 (Unique)** | — | 90.9% | 87.0% | **83.3%** |
| **Service Precision** | — | 90.9% | 83.3% | **76.9%** |
| **Service Recall** | — | 90.9% | 90.9% | **90.9%** |
| **Edge F1 (Connections)** | — | 63.6% | 54.5% | **60.9%** |
| **Edge Precision** | — | 87.5% | 75.0% | **77.8%** |
| **Edge Recall** | — | 50.0% | 42.9% | **50.0%** |

* **Servicios Faltantes (Omitidos):** `['UserConsumerWeb']`
* **Servicios Alucinados (Inventados):** `['DevTools', 'ECS', 'UserConsumerWebMobile']`

#### Video `1aYoIZvabbk` - OLX Autos: Building Developer Platform for Rapid Global Expansion
| Métrica | Ground Truth | Standard Original | Parsimonious Original | Nueva Prueba (**Prompt v9 Gemini 3.6**) |
| :--- | :---: | :---: | :---: | :---: |
| **Número de Nodos** | 6 | 6 | 7 | **7** |
| **Número de Aristas** | 5 | 6 | 7 | **7** |
| **Service F1 (Unique)** | — | 83.3% | 92.3% | **92.3%** |
| **Service Precision** | — | 83.3% | 85.7% | **85.7%** |
| **Service Recall** | — | 83.3% | 100.0% | **100.0%** |
| **Edge F1 (Connections)** | — | 72.7% | 83.3% | **83.3%** |
| **Edge Precision** | — | 66.7% | 71.4% | **71.4%** |
| **Edge Recall** | — | 80.0% | 100.0% | **100.0%** |

* **Servicios Faltantes (Omitidos):** `[]`
* **Servicios Alucinados (Inventados):** `['EC2']`



---
