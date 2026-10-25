You are an Expert Cloud Architecture Transcriber. Your task is to faithfully transcribe the architecture EXACTLY as it is drawn on the whiteboard and described in the audio transcript. You are RECORDING the architecture, not redesigning it.
Do NOT invent unmentioned intermediate components or deployment layers unless they are explicitly present as active runtime participants.
## VALID VOCABULARY LISTS (CRITICAL):
You may ONLY use exact values from these lists for the "service" field.
AWS Services:
ACM, ALB, AMI, AWSConfig, AccessAnalyzer, AlexaForBusiness, AmazonML, AmazonMQ, Amplify, ApiGateway, AppDiscovery, AppStream, AppSync, Athena, Aurora, AutoScaling, Batch, BeanStalk, Chime, CloudFormation, CloudFront, CloudHSM, CloudTrail, CloudWatch, CodeBuild, CodeCommit, CodeDeploy, CodePipeline, Cognito, Comprehend, Connect, ControlTower, CouchBase, DMS, DataExchange, DataPipeline, DeepLens, Detective, DevTools, DirectConnect, DirectoryService, DocumentDB, DynamoDB, DynamoDBStream, EBS, EC2, ECR, ECS, EFS, EKS, ELB, EMR, ElastiCache, ElasticTranscoder, ElementalLive, EventBridge, FSX, Fargate, Firehose, GlobalAccelerator, Glue, Grafana, Greengrass, GuardDuty, IAM, Inspector, IoT1Click, IoTAnalytics, IoTCore, KMS, Kendra, Kinesis, KinesisAnalytics, KinesisDataStream, KinesisVideo, LakeFormation, Lambda, LambdaAtEdge, Lex, LookoutForVision, MAM, MSK, Macie, MediaConnect, MediaConvert, MediaLive, MediaPackage, MediaStore, MemoryDB, ModelRegistry, MongoDBAtlas, NAT, NLB, Neptune, OnPremDC, OpenSearch, Organizations, Outpost, Pinpoint, Polly, PrivateLink, QLDB, QuickSight, RAM, RDS, RedShift, Rekognition, RoboMaker, Route53, S2SVPN, S3, SAP, SES, SNS, SQS, STS, SageMaker, SageMakerGroundTruth, SecretsManager, SecurityHub, ServerlessApplicationRepository, ServiceCatalog, ServiceNow, Shield, ShieldAdvanced, StepFunctions, StorageGateway, SystemsManager, Textract, ThirdParty, Timestream, Transcribe, TransferFamily, TransitGateway, Translate, VPC, VPCPeering, VPN, WAF, WorkSpaces, XRay
User and Client Actors:
UserCompanyAPI, UserCompanyAgent, UserCompanyAnalyst, UserCompanyCRM, UserCompanyDataStream, UserCompanyDeveloper, UserCompanyDomainExpert, UserCompanyDrone, UserCompanyEdge, UserCompanyElementalLiveDevice, UserCompanyHeadEnd, UserCompanyInternalPlatform, UserCompanyWebsite, UserConsumerAPI, UserConsumerAlexaGoogleHome, UserConsumerArtist, UserConsumerCamera, UserConsumerDeveloper, UserConsumerEdge, UserConsumerFarmer, UserConsumerHospital, UserConsumerIOT, UserConsumerMobile, UserConsumerPOS, UserConsumerSatellite, UserConsumerTV, UserConsumerWeb, UserConsumerWebMobile
## MULTILINGUAL TRANSLATION RULE:
Translate all output text fields (notes, graph name, reasoning, etc.) into ENGLISH.
## WORLD MODEL (BASE INPUT):
This is your inventory of what is on the whiteboard: `entities` are the drawn components and `visual_connections` are the drawn arrows. Both lists are AUTHORITATIVE.
{
  "entities": [
    {
      "service": "ThirdParty",
      "name": "CSV & XL",
      "type": "resource",
      "rationale": "Hand-drawn box on the left representing incoming CSV and Excel source data files"
    },
    {
      "service": "S3",
      "name": "Amazon S3 (Raw Data)",
      "type": "service",
      "rationale": "S3 bucket in the Data Ingestion container holding raw uploaded files"
    },
    {
      "service": "Lambda",
      "name": "AWS Lambda (Validation)",
      "type": "service",
      "rationale": "Lambda function in the Data Ingestion container triggered to validate raw CSV/Excel data"
    },
    {
      "service": "S3",
      "name": "Amazon S3 (Validated Data)",
      "type": "service",
      "rationale": "S3 bucket in the Data Ingestion container storing validated data files"
    },
    {
      "service": "Lambda",
      "name": "AWS Lambda (Processing)",
      "type": "service",
      "rationale": "Lambda function in the Data Ingestion container processing validated data and loading into OpenSearch"
    },
    {
      "service": "OpenSearch",
      "name": "AWS OpenSearch (Ingestion)",
      "type": "service",
      "rationale": "OpenSearch cluster in the Data Ingestion container with Graviton2 processor icon"
    },
    {
      "service": "User",
      "name": "User",
      "type": "actor",
      "rationale": "User stick figure representing web browser and mobile app consumers"
    },
    {
      "service": "ThirdParty",
      "name": "Front End",
      "type": "component",
      "rationale": "Hand-drawn box labeled FE in the Data Retrieval container representing the Angular web front-end application"
    },
    {
      "service": "ThirdParty",
      "name": "Back End",
      "type": "component",
      "rationale": "Hand-drawn box labeled BE in the Data Retrieval container representing the Python back-end application"
    },
    {
      "service": "OpenSearch",
      "name": "AWS OpenSearch (Retrieval)",
      "type": "service",
      "rationale": "OpenSearch cluster in the Data Retrieval container serving queries for reports and search"
    },
    {
      "service": "RDS",
      "name": "Amazon RDS",
      "type": "service",
      "rationale": "RDS database in the Data Retrieval container providing structured relational data access"
    },
    {
      "service": "S3",
      "name": "Amazon S3 (Reports)",
      "type": "service",
      "rationale": "S3 bucket in the Data Retrieval container storing generated report files (>10,000 records)"
    },
    {
      "service": "SES",
      "name": "Amazon SES",
      "type": "service",
      "rationale": "SES service icon in the Data Retrieval container used for sending download link emails to users"
    }
  ],
  "visual_connections": [
    {
      "source_label": "CSV & XL",
      "target_label": "Amazon S3 (Raw Data)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing raw data upload into the raw S3 bucket"
    },
    {
      "source_label": "Amazon S3 (Raw Data)",
      "target_label": "AWS Lambda (Validation)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow indicating S3 event trigger calling the validation Lambda"
    },
    {
      "source_label": "AWS Lambda (Validation)",
      "target_label": "Amazon S3 (Validated Data)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing validated copy uploaded to the validated S3 bucket"
    },
    {
      "source_label": "Amazon S3 (Validated Data)",
      "target_label": "AWS Lambda (Processing)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow indicating trigger from validated S3 bucket to processing Lambda"
    },
    {
      "source_label": "AWS Lambda (Processing)",
      "target_label": "AWS OpenSearch (Ingestion)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing data ingestion into the OpenSearch cluster"
    },
    {
      "source_label": "User",
      "target_label": "Front End",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow representing user web request to Angular Front End"
    },
    {
      "source_label": "Front End",
      "target_label": "User",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow representing response back from Angular Front End to User browser"
    },
    {
      "source_label": "User",
      "target_label": "Back End",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow representing direct request from mobile user or web client to Python Back End"
    },
    {
      "source_label": "Back End",
      "target_label": "User",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow representing data response back from Python Back End to User"
    },
    {
      "source_label": "Back End",
      "target_label": "AWS OpenSearch (Retrieval)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing Back End querying the OpenSearch data layer"
    },
    {
      "source_label": "Back End",
      "target_label": "Amazon RDS",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing Back End querying the RDS database"
    },
    {
      "source_label": "Back End",
      "target_label": "Amazon S3 (Reports)",
      "arrow_direction": "pointing_to_target",
      "description": "Arrow showing Back End uploading generated large reports to S3 bucket"
    }
  ]
}
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


## VIDEO URL:
https://www.youtube.com/watch?v=JYeXbUdFOdw

## FULL TRANSCRIPT:
Hi, I'm Maheen from AWS. Hi, I'm Yogesh from Novantec and this is My Architecture. So today we are going to talk about a data processing architecture pattern using AWS OpenSearch. So Yogesh, I understand you did this for Cybex. So what was the customer challenge you were trying to solve? Yeah, so Cybex is in the business to provide trade data and reports related to the export import. They had around 1.5 billion of records. Initially they used to serve their customer in offline mode. So every time customer had a new requirement whether it is related to a new product or say new country, the entire process to understand the requirement to book the order then churn the data and then serve the report. It used to take a couple of days, right? So they wanted us to provide a cloud solution which can provide flexibility to their customers to get data at any point of time from anywhere within few seconds. First of all, the raw data which is in the format of the CSV or in the Excel file, it's get uploaded into the S3 buckets. Then a Lambda get triggered to validate this data. If there is any discrepancy within the data, then it gets highlighted here. Else, copy of the validated data get uploaded into a different folder within the S3 buckets. Once we have the validated copy here, then the Lambda get triggered to process this validated data and ingest it into the OpenSearch cluster. Here we are doing few more activities like we are creating the query templates and mapping them with relevant indexes. Secondly, we are using the Amazon OpenSearch analyzer to fine-tune queries and enhance performance. And then an aggregated layer is being built on top of the process data to serve the complex reports like the trained analysis report or some other aggregation reports. So, Yagesh, I see you've used an event-driven architecture in this particular instance. So why the event-driven architecture? Yeah. So as I mentioned earlier, when we designed this architecture, at that point of time, we had around 1.5 billion number of records. But over a period of time, this number had been increased by more than 3.5 times. Now we have around 5 billion of records. But still, application is able to provide data and reports having 15 to 20 complex parameters within 2 to 4 seconds. So you can understand that there is no such latency with the huge increase of the number of records using the same architecture. Thank you for explaining how data ingestion works. Tell us how the user is able to then get access to this data. So we have designed two ways to retrieve the data, right? The user can access the data either using the web application or they can use mobile application to retrieve the data. So in case of the web application, user sends the request to the front-end application via the web browser. It has been developed using the Angular. And then the request goes back to the browser and then it's come back to the backend application, right? So this backend application we have developed using the Python. Then request goes directly to the data layer and then response sends back to the user via the backend application. While in case of the mobile apps, request goes directly to the backend application and then to the data layer and then response comes back. And early on you mentioned 5 billion records. How do you keep the costs down for that kind of volume? So you can see, right, we are using the Graviton2 instance for the Amazon OpenSearch. So it helped us really to optimize the cost, right? Initially, if I will compare from the beginning, right, we are saving something between 25 to 30 percent of the operation cost, which is roughly equivalent to the 100K dollar. And when you were explaining the challenge, you mentioned that sometimes reports can take longer to run than the normal latency. So how do you give the best customer experience using this? Yeah, it happens sometimes, right? Sometimes user requests for a report having more than 10,000 records. Then at that point of the time, we upload the report in this S3 bucket and then send an intimation to the user via SES to download this report using the pre-signed URL. That's great for security as well. Yagesh, thank you for sharing your fantastic architecture with us today. Thank you. Thank you. And thank you for watching another episode of This Is My Architecture. Thanks, everyone.