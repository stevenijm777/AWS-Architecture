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
      "service": "CloudFront",
      "name": "CloudFront",
      "type": "CloudFront",
      "rationale": ""
    },
    {
      "service": "ApiGateway",
      "name": "ApiGateway",
      "type": "ApiGateway",
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda — NOTES: separate lambda for ACL",
      "type": "Lambda",
      "rationale": "NOTES: separate lambda for ACL"
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": "AUTOSCALE: False\nSPOT: False"
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": ""
    },
    {
      "service": "UserConsumerWeb",
      "name": "UserConsumerWeb",
      "type": "UserConsumerWeb",
      "rationale": ""
    }
  ],
  "visual_connections": [
    {
      "source_label": "CloudFront",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudFront",
      "target_label": "UserConsumerWeb",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ApiGateway",
      "target_label": "Lambda — NOTES: separate lambda for ACL",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ApiGateway",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ApiGateway",
      "target_label": "UserConsumerWeb",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — NOTES: separate lambda for ACL",
      "target_label": "ApiGateway",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "DynamoDB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "ApiGateway",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "CloudFront",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "DynamoDB",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserConsumerWeb",
      "target_label": "CloudFront",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserConsumerWeb",
      "target_label": "ApiGateway",
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
https://www.youtube.com/watch?v=wjtSHyENv0I

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I am Gerardo and I'm joined today by Gerald from American Family Group. Welcome Gerald. Thank you for having me sir. So Gerald, what is American Family Group? American Family Group is a parent company of several insurance companies, one of which is Main Street America. I work for American Family Group and the architecture that we're talking about is for Main Street America. It's for independent agents. Okay, great. So I hear that you are in the middle of migration and transformation of a legacy application and it's happening as we speak. Yes, we're modernizing this application as we speak. That's good. Can you run me through some of the components and what you've modernized so far? Sure. As I go through, I'll talk about which ones. Well, the agents come in and they request the single page application. We've modernized that. It used to be on an Apache. Now it's served up from an S3 bucket through a CloudFront to the application. Great. Then, when they're making calls to the back end, they come into, it used to be on some load balanced on-prem timecat servers running Java script. Now they come into an API gateway. The first thing that API gateway is use a modern Lambda authorizer to validate that they do have access. Then, it makes the calls to this Lambda here, which is a serverless Python Lambda, so it can scale up and down easily. That particular Lambda then decides we've modernized by moving in some of the functions into the Lambdas in the serverless stack, but we still haven't moved the whole application. So, for some things, it calls up to here, who calls back down there. Okay. So, some of the functionality is still sitting in the Tomcat application? Yes, it is, sir. Can you give me some examples of the functionality that's still there and what's been moved to the serverless world? Well, some things like how user management are still there because we haven't had to move it yet. When we're moving stuff is when either there's a new feature change, okay, so anything new is being implemented in the serverless stack. If there's enhancements, significant enhancements to a function, they're also being then migrated and moved into a more modern serverless Python stack. And lastly, of course, the dreaded bugs. If there's a significant bug, not a one-liner or a two-liner, but something significant, that piece of code is modernized. So, we're slowly strangling this timecat. Oh, that's awesome. That's awesome. So, out of these components, we still need to talk about this. Oh, yeah. So, what's this DynamoDB timeout? Well, the DynamoDB is used for storing, caching the user information. So, when a user comes in, we cache it. And we do it in DynamoDB for a couple reasons. One, the Lambda, you can hit another instance of the Lambda next time you make an API call. So, we can't cache it on the machine there. This DynamoDB is a regional one. So, everything in the region. So, if one of these Lambdas is running in Availability Zone A and others in B, they can both access that cache of information. Then, lastly, of course, if, I know it doesn't ever happen, but if Availability Zone A would go down, then, you know, the ones running in B can access it without a pause. Yeah, that makes sense. That makes sense. So, have you started realizing some of the benefits of the modernization that you're going through? Actually, we have. Yeah. First off, we've been able to shut down 25 on-prem servers. We've also seen our user satisfaction increase by 25% of what it used to be. And because of that user satisfaction, the agents are excited about this. And they will talk to their fellow agents saying, you know, you've got to go give that application a new chance. So, we've actually seen 10% new users coming in, which is selling more policies for us. And lastly, of course, using Lambdas and all are much cheaper than running a bunch of, you know, on-prem servers. Thank you so much for sharing this great modernization story with us. Thank you for having me and allowing me to present it. And thank you for watching. This is Markitecture. See you next time. We'll see you next time.