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
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "stores all master files"
    },
    {
      "service": "CloudFormation",
      "name": "CloudFormation",
      "type": "CloudFormation",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": "AUTOSCALE: true\nWORKLOAD_PEEK: running Evertz ORT software"
    },
    {
      "service": "DirectConnect",
      "name": "DirectConnect",
      "type": "DirectConnect",
      "rationale": ""
    },
    {
      "service": "UserCompanyDataStream",
      "name": "UserCompanyDataStream",
      "type": "UserCompanyDataStream",
      "rationale": ""
    },
    {
      "service": "UserCompanyEdge",
      "name": "UserCompanyEdge",
      "type": "UserCompanyEdge",
      "rationale": ""
    }
  ],
  "visual_connections": [
    {
      "source_label": "S3",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "DirectConnect",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "DirectConnect",
      "target_label": "UserCompanyDataStream",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserCompanyDataStream",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserCompanyDataStream",
      "target_label": "UserCompanyEdge",
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
https://www.youtube.com/watch?v=hMK2NJ-q9nc

## FULL TRANSCRIPT:
Hello and welcome to This is My Architecture. My name is Amir. I'm here with Matt from WarnerMedia HBO. Matt, why don't you tell us what HBO does? So HBO is a content provider. We are now part of WarnerMedia and we have a number of brands that we are currently supporting. We're here today to talk about your cloud linear play out that you guys are running currently through New York and Atlanta. So why don't you tell us a little about what business problem that was trying to solve? Sure. The business problem is actually two-fold. Initially it was a BCP solution, so business continuity. That morphed over time with the business to support 30 channels out of our AWS US East 1 region. And I see we have that drawn up here on the board. So why don't you walk us through how files get moved up into the cloud process and then sent back out for play out. Sure. So today Linear Ops QCs the master files in Atlanta. Those get taken via Spera up to S3 where they are stored with all of the brands. We store all of our master files there. Once they are registered in Eberts Mediator, they then get transferred to the local EC2, which is running Eberts' ORT software. Within each AZ in US East 1, we have 10 channels running. Each channel has a primary and backup. The primary and backup and the EC2 instances are supported also with auto scaling groups. Those files are played out using Eberts playtime. That play out goes via direct connect back to prem as a unicast signal. Then that gets taken and compressed and brought to the uplink for distribution to affiliates. So this path here, which I just drew, is what we call the X chain. I'll just put an X there. That is a tertiary path to air. We use an auto changeover switch on site to switch between a Techwood playout, a CNN center playout, and a cloud playout. For the BCP solution, we go direct connect to Hudson Yards, and that is eight channels, and that also gets fed to an uplink. Now, I've noticed you've got CloudFormation here. What was that used to deploy the solution here? Good question. So we took the CloudFormation templates. We actually scrubbed them all. Our internal cloud team worked with AWS and Eberts to essentially edit those YAML files and create what is a repeatable process so we can now expand the deployment if we'd like. We went through about 40 YAMLs to deploy the system. And I see that since they're in different AZs, if one goes down, the other AZs are still up and the solution is still running, right? Absolutely. Redundancy was a key part of this. We want to try to reach the five nines availability that you would expect from an on-prem system. And to handle any sort of latency or any problems with the connection, what kind of protocol are you using to run from the EC2s to your on-prem? Good question. Today we're using Eberts' CloudBridge to take us from the EC2, the ORT, back to site. And we basically bookend that connection. There's CloudBridge in New York, there's CloudBridge in Atlanta, and there's CloudBridge in AWS. What's your future plans for this solution going forward? So there are a couple things on the plate right now. We're looking at live. How can we take a venue signal and essentially switch between a live input on the ORT and switch between live and pre-recorded content? We're also looking at taking these signals from the ORTs out and muxing them together, creating a multiplex that we can then hand off direct to an MVPD. So essentially doing the compression that you would do today at Atlanta and do that in the cloud. Thanks, Matt. It was great learning how you're able to use the cloud to speed up your deployment for your cloud linear play out to your affiliates. Thanks, my pleasure. And thanks for watching. This is my architecture.