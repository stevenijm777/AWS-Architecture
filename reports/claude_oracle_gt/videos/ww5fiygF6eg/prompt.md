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
Use this as your visual inventory.
{
  "entities": [
    {
      "service": "UserCompanyDrone",
      "name": "UserCompanyDrone",
      "type": "UserCompanyDrone",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Imagery process (into three files per well pad)",
      "type": "ThirdParty",
      "rationale": "Imagery process (into three files per well pad)"
    },
    {
      "service": "ThirdParty",
      "name": "on-premises database & server",
      "type": "ThirdParty",
      "rationale": "NOTES: the database storing raster proxies; the server handles user queries. the server cannot directly imagery data read from S3 without raster proxies\nNAME: on-premises database & server"
    },
    {
      "service": "CloudWatch",
      "name": "CloudWatch",
      "type": "CloudWatch",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "processed imagery data"
    },
    {
      "service": "StorageGateway",
      "name": "StorageGateway",
      "type": "StorageGateway",
      "rationale": ""
    },
    {
      "service": "StepFunctions",
      "name": "StepFunctions",
      "type": "StepFunctions",
      "rationale": "N_STEPS: 3\nWORKLOAD_PEEK: test if new imagery data are available; pull images from third party to S3; process images"
    },
    {
      "service": "Lambda",
      "name": "Lambda — WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available"
    },
    {
      "service": "Lambda",
      "name": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: pull data from third-party to S3"
    },
    {
      "service": "Lambda",
      "name": "Lambda — WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)"
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserCompanyDrone",
      "target_label": "Imagery process (into three files per well pad)",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Imagery process (into three files per well pad)",
      "target_label": "Lambda — WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Imagery process (into three files per well pad)",
      "target_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "on-premises database & server",
      "target_label": "StorageGateway",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudWatch",
      "target_label": "StepFunctions",
      "arrow_direction": "",
      "description": "scheduled basis"
    },
    {
      "source_label": "S3",
      "target_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "Lambda — WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "StorageGateway",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StorageGateway",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StorageGateway",
      "target_label": "on-premises database & server",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StepFunctions",
      "target_label": "Lambda — WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StepFunctions",
      "target_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StepFunctions",
      "target_label": "Lambda — WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available",
      "target_label": "Imagery process (into three files per well pad)",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: call APIs to the third-party see if new imagery data are available",
      "target_label": "StepFunctions",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "target_label": "Imagery process (into three files per well pad)",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: pull data from third-party to S3",
      "target_label": "StepFunctions",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: transfer images into raster proxies, which serve like URLs for the on-prem server to get data (the on-prem software cannot directly reads from S3)",
      "target_label": "on-premises database & server",
      "arrow_direction": "",
      "description": ""
    }
  ]
}
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
- **Visual & Verbal Grounding:** Primary evidence for edges must come from visual arrows or explicit verbal flow statements in the transcript (e.g., "sends to", "triggers", "stores in").
- **Completeness:** Ensure that every active service node identified is connected to the graph if a logical flow is described in the audio, avoiding orphan nodes while preventing unmentioned canonical edge hallucinations.

## STRICT EDGE ROUTING & DIRECTIONALITY:
- **Unidirectional Default:** Treat data and control flows as strictly unidirectional unless a reverse flow is explicitly shown or stated.
- **Exact Edge Type Mapping:** Accurately differentiate `data` (direct payloads), `control` (triggers, orchestration, events), and `meta` (monitoring, feedback).
- **No Intermediate Shortcuts:** Preserve exact path routing. Do not bypass intermediate nodes.


## VIDEO URL:
https://www.youtube.com/watch?v=ww5fiygF6eg

## FULL TRANSCRIPT:
Hi, welcome to This is Mar Architecture. I'm Jennifer and I'm here with Mark from Marathon Oil. Hi Mark, thanks for joining us today. Hi Jennifer, pleasure to be here. Could you tell us a little bit about Marathon Oil? Yeah, we're a responsible independent exploration and production company with deep roots in American energy. Great, I see a drone here. Could you walk us through this architecture and how it's used to solve your business problem? Yeah, so we routinely monitor our well pads. In the past we were doing that via people and now we've moved to drones. So these drones are being flown by third-party pilots who are licensed who go to every one of our well pads on a routine basis. Once they take that imagery, they're loading that imagery into a third-party software which is actually processing all of the imagery and creating three separate files per well pad. So those three image files, one is an ortho mosaic which is a high resolution top-down view of the well pad. We also get a digital terrain model and a digital elevation model. So what happens when the drones capture these images? Yeah, so once the images are created and stored on that third-party server, this is where the AWS architecture takes over. So the first event that we have is actually a cloud watch event which is running on a scheduled basis. This cloud watch event is calling a step function, and that step function consists of three separate Lambda functions. The first Lambda function actually goes to this third-party software via an API and determines if there's new images and new flights available. If it does find a new flight or a new image, it will call a second Lambda function which actually takes those images from this third party and stores them in an S3 bucket in our environment. So what happens after these images are in S3? Yeah, so we need to get them into our on-prem mapping software. Now the on-prem mapping software cannot read directly from S3. So we need to call a separate Lambda function which is actually taking these S3 images and creating what's called a raster proxy. This raster proxy serves as kind of a URL for this server to understand how to go out and actually get those images. So these raster proxies are stored in the local servers database. And from there, if I'm a user, I want to go out and actually view these images, I hit the mapping software, which via a storage gateway will come out, find those image files and display them for our end user. Okay. So for your on-premise servers, do you have to change the application in order to leverage storage gateway? No. So that third Lambda function that we're using is actually what is doing that for us. So it's creating the URL that the server can make sense of, which is called a raster proxy, which allows the on-premise software to actually read directly from the S3 bucket via storage gateway. So what happens after these index files are in S3? How do your internal end users leverage these files? Yep. So we have a maintenance team and various other operations teams that leverage these images for a variety of reasons. Really, it's to identify any issues with equipment or see if we need to do preventative maintenance and just get an overall health check of the well pad itself. Thank you, Mark, for walking us through this architecture. It's been really interesting to learn how Marathon Oil uses the serverless architecture to process your drone images and also be able to provide automatic monitoring of your health equipment. And thank you for watching. This is my architecture. Thank you.