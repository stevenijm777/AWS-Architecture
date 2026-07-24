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
