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
      "service": "EKS",
      "name": "META MANAGER",
      "type": "AWS",
      "rationale": "EKS icon on the top left labeled META MANAGER and F.E."
    },
    {
      "service": "OpenSearch",
      "name": "ELASTICSEARCH NEO4J",
      "type": "AWS",
      "rationale": "OpenSearch search icon located below EKS, labeled ELASTICSEARCH NEO4J."
    },
    {
      "service": "S3",
      "name": "S3 DATA LAKE",
      "type": "AWS",
      "rationale": "S3 bucket icon inside the blue dashed box labeled S3 DATA LAKE."
    },
    {
      "service": "ThirdParty",
      "name": "KAFKA",
      "type": "ThirdParty",
      "rationale": "Kafka icon inside the blue dashed Data Lake box."
    },
    {
      "service": "EMR",
      "name": "EMR",
      "type": "AWS",
      "rationale": "EMR icon inside the blue dashed Data Lake box."
    },
    {
      "service": "RDS",
      "name": "RDS",
      "type": "AWS",
      "rationale": "RDS database icon at top right."
    },
    {
      "service": "ThirdParty",
      "name": "VERTICA",
      "type": "ThirdParty",
      "rationale": "Vertica icon located at middle right below RDS."
    },
    {
      "service": "RDS",
      "name": "MULTIPLE DATA SOURCES",
      "type": "OnPrem",
      "rationale": "Database cylinder icon at bottom left below the green dashed line labeled MULTIPLE DATA SOURCES."
    },
    {
      "service": "ThirdParty",
      "name": "APPLICATIONS",
      "type": "ThirdParty",
      "rationale": "Puzzle piece icon at bottom center below the green dashed line labeled APPLICATIONS."
    },
    {
      "service": "UserCompanyAnalyst",
      "name": "DA/DS",
      "type": "Actor",
      "rationale": "User icon at bottom right labeled DA/DS."
    }
  ],
  "visual_connections": [
    {
      "source_label": "META MANAGER",
      "target_label": "ELASTICSEARCH NEO4J",
      "arrow_direction": "out",
      "description": "Arrow pointing down from META MANAGER (EKS) to ELASTICSEARCH NEO4J."
    },
    {
      "source_label": "MULTIPLE DATA SOURCES",
      "target_label": "KAFKA",
      "arrow_direction": "both",
      "description": "Bidirectional arrows pointing between MULTIPLE DATA SOURCES and KAFKA across the green boundary."
    },
    {
      "source_label": "APPLICATIONS",
      "target_label": "EMR",
      "arrow_direction": "both",
      "description": "Bidirectional arrows pointing between APPLICATIONS and EMR across the green boundary."
    },
    {
      "source_label": "KAFKA",
      "target_label": "S3 DATA LAKE",
      "arrow_direction": "out",
      "description": "Arrow pointing up from KAFKA to S3 DATA LAKE."
    },
    {
      "source_label": "EMR",
      "target_label": "S3 DATA LAKE",
      "arrow_direction": "both",
      "description": "Bidirectional vertical connection arrows between EMR and S3 DATA LAKE."
    },
    {
      "source_label": "S3 DATA LAKE",
      "target_label": "RDS",
      "arrow_direction": "out",
      "description": "Arrow pointing from the S3 DATA LAKE container to RDS."
    },
    {
      "source_label": "EMR",
      "target_label": "VERTICA",
      "arrow_direction": "out",
      "description": "Arrow pointing from EMR to VERTICA."
    },
    {
      "source_label": "META MANAGER",
      "target_label": "KAFKA",
      "arrow_direction": "out",
      "description": "Pink line extending from META MANAGER downwards towards the Kafka streaming component."
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
https://www.youtube.com/watch?v=9qTEHITVeLE

## FULL TRANSCRIPT:
Welcome to This is my Architecture. Today I have here Carlos from Majid El Futame. Hi Carlos. Hi Cameron. Hi. Can you tell me a little bit more about Majid El Futame? Yeah. Majid El Futame is a multi-veilion company. We are in 14 countries and we have business like retail, real estate, we have malls and we have patient entertainment. I see that we have a very interesting architecture here today. Tell me what problem you are trying to solve. So the three pillars we want to solve is how to collect the data, how to protect the data, and how to connect the data. Okay so you have data from various sources and you want to get value out of that, extract value out of it. Exactly. So we call it the grid. So we start all of the infrastructure is defined with our DevOps team in code so we can just spin the architecture or the infrastructure from them and then you get your frontend and you connect to our MetaManager. Okay and what is the MetaManager? The manager is the brains of the grid and the main goal is to abstract you from the complexity of all this technology you need to move this data. And I see that you're running that on EKS. Yeah it's EKS microservice architecture. So that's collecting the data from the various sources. You have Elasticsearch there as well. Yes. What's happening there? So first you need to understand which data you have. So you need to discover which tables, schemas, APIs you have. Right so we get all of this data into MetaManager. We'll discover and we'll store this meta information in our MetaStore which is a combination of document and graph database. Okay so now you have indexed the data. What's next? So first step is collect as we mentioned before. Right so we need to get all of this data into our centralized data lake so we can get all the data together and we can do insights etc. Right so all of this data are in different networks, different countries, different technology. So we use a combination of Kafka and EMR to bring this data into our data lake. Okay so you're taking data from into Kafka and streaming them into S3 and EMR. What kind of scale are we talking about? Yeah so in Kafka we are talking about 600 topics, 250 gigabytes and in average we have seven days attention period. So all of the data is stored in S3. Okay and what kind of scale do we have in S3? Yeah so in S3 we have around 60 terabytes today. Sorry for my writing. No problem. Great amount of data there. All right so now you have collected the data in the data lake. What's next? How do you consume this? Yeah so first let me just explain. So we asked the data coming in and out of data lake. Right? So this data we need to protect the data. Right? So our metamani also will apply all of these data on top of this data and then we need to consume this data. So for example we have RDS and Vertica. So the data is sent to these data stores. We can publish or consume using APIs or OLTPs if we need. Okay and this is your data analyst and data scientist are going to consume this data. Exactly. So this is a traditional analytics we have in this company. You have your data analyst and your data science. They need to consume the data. They need to run models. They need to create the ask words etc. Great. So now you have consumed the data. I collected the data. How do we connect to users? That's a very good point. Data comes from different sources and applications because we also consume from APIs and then we bring this data back to our business. So we are able to connect back. One of the key components is the enterprise streaming platform that we created across all the companies in Mav. This is something that we bring to Mav. So basically I go to watch a movie at Vox Cinema and then I go to Carrefour to do shopping. What kind of experience am I getting? That's a very very good point. Mind you come to one of our iconic malls, Mall of Emirates. You come with your car. You park. So we get your plate number. We know where you park. You enter inside the mall. You connect to the wi-fi. We know how you move inside the mall. Now you are doing your groceries in Carrefour and you use our loyalty application. So we know that you've come to the cinemas before. We know you like cinema. So we can provide for you a push notification and we can offer to you a free back service. So we'll take your groceries, bring to your car and then you can come to the movies with a free popcorn pouch. I'll always love free popcorn. Great. So I know you have made this. There's a lot of complexity in our architecture and we've really simplified it. What is one thing that you're really proud of from your team that's delivered this architecture? Yeah. So we provide this DevOps approach to the company and we are able to spin up and spin down the infrastructure as we need. So for example, in our IT test, we create all the infrastructure. We run the test and then we destroy the infrastructure and we built this in six months. We put our first MVP in production. Wow. And for a non-technology company spinning it up and spinning down infrastructure as code. Yeah. That's great. So what kind of a business benefit has your company realized after this data? Yeah. So one of the first things that we provided is a 360 view of our customers. So before you were a customer in Vox and a customer in Carrefour and we couldn't relate together. Now we know you are the same customer. So we can do cross campaigns, for example, for marketing. So we can connect Carrefour and Vox with our marketing in holding and we can do these campaigns like the push notification I explained. That's good. Carlos, thank you for sharing your work with me today. Thank you for having me. And thank you for joining This is My Architecture.