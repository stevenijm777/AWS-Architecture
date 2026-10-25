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
      "name": "3rd Party",
      "type": "On-Premises / External",
      "rationale": "External software and drone system labeled 3rd Party on the left side of the diagram."
    },
    {
      "service": "CloudWatch",
      "name": "CloudWatch Event",
      "type": "AWS Service",
      "rationale": "CloudWatch Event icon triggers scheduled events for processing."
    },
    {
      "service": "StepFunctions",
      "name": "Step Functions",
      "type": "AWS Service",
      "rationale": "Step Functions orchestrates execution of Lambda functions."
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "AWS Service",
      "rationale": "AWS Lambda icon processing image files, calling 3rd party API, and creating raster proxies."
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "AWS Service",
      "rationale": "S3 bucket icon used for storing processed drone imagery."
    },
    {
      "service": "StorageGateway",
      "name": "Storage Gateway",
      "type": "AWS Service",
      "rationale": "Storage Gateway icon enabling on-premises server access to S3 storage."
    },
    {
      "service": "OnPremDC",
      "name": "Server",
      "type": "On-Premises",
      "rationale": "On-premises server icon located inside the on-premise container box on the right."
    },
    {
      "service": "OnPremDC",
      "name": "Database",
      "type": "On-Premises",
      "rationale": "On-premises database icon located inside the on-premise container box on the right below the server."
    }
  ],
  "visual_connections": [
    {
      "source_label": "3rd Party",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Curved green arrow showing imagery data transfer from 3rd Party to S3."
    },
    {
      "source_label": "CloudWatch Event",
      "target_label": "Step Functions",
      "arrow_direction": "down",
      "description": "Green arrow from CloudWatch Event triggering Step Functions."
    },
    {
      "source_label": "Step Functions",
      "target_label": "Lambda",
      "arrow_direction": "down_right",
      "description": "Green arrow from Step Functions triggering Lambda execution."
    },
    {
      "source_label": "Lambda",
      "target_label": "3rd Party",
      "arrow_direction": "left",
      "description": "Green arrow labeled API pointing from Lambda to 3rd Party."
    },
    {
      "source_label": "Lambda",
      "target_label": "S3",
      "arrow_direction": "up",
      "description": "Green arrow from Lambda pointing up to S3 bucket."
    },
    {
      "source_label": "Lambda",
      "target_label": "Database",
      "arrow_direction": "right",
      "description": "Green arrow from Lambda pointing to on-premises Database."
    },
    {
      "source_label": "Server",
      "target_label": "Storage Gateway",
      "arrow_direction": "up_left",
      "description": "Green arrow from Server pointing to Storage Gateway."
    },
    {
      "source_label": "Storage Gateway",
      "target_label": "S3",
      "arrow_direction": "left",
      "description": "Green arrow pointing from Storage Gateway to S3."
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
https://www.youtube.com/watch?v=ww5fiygF6eg

## FULL TRANSCRIPT:
Hi, welcome to This is Mar Architecture. I'm Jennifer and I'm here with Mark from Marathon Oil. Hi Mark, thanks for joining us today. Hi Jennifer, pleasure to be here. Could you tell us a little bit about Marathon Oil? Yeah, we're a responsible independent exploration and production company with deep roots in American energy. Great, I see a drone here. Could you walk us through this architecture and how it's used to solve your business problem? Yeah, so we routinely monitor our well pads. In the past we were doing that via people and now we've moved to drones. So these drones are being flown by third-party pilots who are licensed who go to every one of our well pads on a routine basis. Once they take that imagery, they're loading that imagery into a third-party software which is actually processing all of the imagery and creating three separate files per well pad. So those three image files, one is an ortho mosaic which is a high resolution top-down view of the well pad. We also get a digital terrain model and a digital elevation model. So what happens when the drones capture these images? Yeah, so once the images are created and stored on that third-party server, this is where the AWS architecture takes over. So the first event that we have is actually a cloud watch event which is running on a scheduled basis. This cloud watch event is calling a step function, and that step function consists of three separate Lambda functions. The first Lambda function actually goes to this third-party software via an API and determines if there's new images and new flights available. If it does find a new flight or a new image, it will call a second Lambda function which actually takes those images from this third party and stores them in an S3 bucket in our environment. So what happens after these images are in S3? Yeah, so we need to get them into our on-prem mapping software. Now the on-prem mapping software cannot read directly from S3. So we need to call a separate Lambda function which is actually taking these S3 images and creating what's called a raster proxy. This raster proxy serves as kind of a URL for this server to understand how to go out and actually get those images. So these raster proxies are stored in the local servers database. And from there, if I'm a user, I want to go out and actually view these images, I hit the mapping software, which via a storage gateway will come out, find those image files and display them for our end user. Okay. So for your on-premise servers, do you have to change the application in order to leverage storage gateway? No. So that third Lambda function that we're using is actually what is doing that for us. So it's creating the URL that the server can make sense of, which is called a raster proxy, which allows the on-premise software to actually read directly from the S3 bucket via storage gateway. So what happens after these index files are in S3? How do your internal end users leverage these files? Yep. So we have a maintenance team and various other operations teams that leverage these images for a variety of reasons. Really, it's to identify any issues with equipment or see if we need to do preventative maintenance and just get an overall health check of the well pad itself. Thank you, Mark, for walking us through this architecture. It's been really interesting to learn how Marathon Oil uses the serverless architecture to process your drone images and also be able to provide automatic monitoring of your health equipment. And thank you for watching. This is my architecture. Thank you.