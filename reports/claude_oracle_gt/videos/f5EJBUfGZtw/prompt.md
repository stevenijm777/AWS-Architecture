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
      "service": "UserConsumerAPI",
      "name": "UserConsumerAPI",
      "type": "UserConsumerAPI",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3 #1",
      "type": "S3",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3 #2",
      "type": "S3",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": ""
    },
    {
      "service": "Glue",
      "name": "Glue",
      "type": "Glue",
      "rationale": ""
    },
    {
      "service": "ECS",
      "name": "ECS",
      "type": "ECS",
      "rationale": ""
    },
    {
      "service": "Aurora",
      "name": "Aurora",
      "type": "Aurora",
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "SCALE_RANGE: 5-10M events/day"
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Salesforce",
      "type": "ThirdParty",
      "rationale": "Salesforce"
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserConsumerAPI",
      "target_label": "S3 #1",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3 #1",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3 #1",
      "target_label": "Glue",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Glue",
      "target_label": "S3 #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ECS",
      "target_label": "Aurora",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Aurora",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "SQS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SQS",
      "target_label": "Salesforce",
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
https://www.youtube.com/watch?v=f5EJBUfGZtw

## FULL TRANSCRIPT:
Hi, welcome to This is My Architecture. My name is Andrea and I'm here with Sandeep from Expedia. Hi Sandeep, welcome to the show. Hi Andrea, thank you. So what do you guys do? So we are the travel technology company. We help people travel from any part of the world to anywhere in the world and by providing unique products like air, car, cruise, lodging, everything. Very cool. So today we're going to talk about a very special topic. You build a very unique pattern for integrating AWS to Salesforce. What integrations have you guys built? Yeah, sure. So we collect data from various different Expedia channels, various different Expedia platforms. Some of them are on-prem, but mostly running into the cloud right now. So we consume that data, process it through the AWS and then push the data to the Salesforce Einstein Analytics, which is a reporting engine and then provide a global unique experience to our business users. Very cool. Let's dive straight into it, shall we? Definitely. I see Expedia Group. Walk us through what apps are we talking about there? So from this Expedia different applications, we are getting data, let's say, booking, VMIN and some of our partners data. Okay. And so we see a couple of different patterns here, right? I see S3, ECS. So I can divide this architecture into two different patterns. So if I have to draw a line right there, the first part of the architecture, the top section talks about batch processing, or you can say daily processing, because this is when we get the data from Expedia applications on a daily basis. And the lower part actually talks about the real-time integration which we have built and providing this unique real-time data to our Salesforce users. I see. What do you store in S3? What components are you putting? So S3, I can call it as our data ingestion layer. Okay. Or a data lake. So we collect data from various Expedia Group applications into S3. And by the way, the data is coming into various different formats. Formats. Some of them could be Parquet, CSVs, JSON, you name it. So it's all heterogeneous sources. I see. And then what we do, we leverage the serverless architecture Glue, which is the great ETL tool. So we consume all this data, transform all this data, and then make it a unified format and push it to the S3. I see. If you could draw this out then for our viewers, what's the difference between Glue and EC2? Sure. What would the differentiation be? So when we are building this architecture, Glue, no doubt, is a great tool, but has certain limitations at that time. Like it didn't have a bookmark support for the Parquet files. So that's why we are doing that work into our EC2. Plus there's some more customization which was not done through Glue. That's why we are leveraging the EC2 over here. And then most of the data going through from here, getting transformed, comes into a common format into the S3 over here, which by the way is a CSV because the Salesforce Einstein Analytics currently has only limited to the CSV format. I see. That's a very interesting architectural pattern here to convert it to a format that is consumable by Salesforce. Now let's dive into the real-time stream. Right. ECS. Yeah. Why are you using ECS? Yeah, so ECS. So we have actually a Kafka consumer running on the ECS. Oh wow. Yeah, so Kafka consumer consumes the real-time events and then we push it to the Aurora right here and I'll come back in a moment while we are pushing to Aurora. Then we have a bunch of processing done through Lambda. We queue them up and makes a queueable message into SQS. And from the SQS, we call a bunch of other Lambdas and then call our APIs and push this data straight into the Salesforce. Okay. Makes sense. So why do you not use Kinesis Streams or manage Kafka service? Why do you use ECS? Right. I mean, Kinesis is great too, but our Kafka producer is running on an Xperia group applications. Okay. So that's why we had to consume from that same instance. I see. That's why we are using the Kafka consumer. That makes sense. And then Aurora, right? Yeah. Why not S3? So for us, the use case was more around aggregating the data, sorting the data. So for that purpose, we are leveraging the power which a MySQL engine provides and that's why there's Aurora. We actually tried it out with a few other solutions out there, but then in the end, we decided Aurora is best for our use case. Wonderful. So what are we talking about in terms of scale? How much data are you processing? Is it nightly, daily? Walk us through that. Great question. So throughout this architecture, we are actually processing 500 to 800 million rows on a daily basis from this top section right there. And then through this bottom section, we are consuming around 5 to 10 million events per day. Wow. What does the future hold? Where do you see progress? So this architecture is actually very scalable. So in future, if we want to add more sources over here, we can easily add them. If we want to consume more events, we can easily consume them. So it's a very scalable architecture. Second, we want to leverage the Fargate as well into architecture. So that's where we are heading to. Very cool. Thanks for sharing this unique architecture with integrating your core booking system and other core applications with Salesforce, but converting it into the appropriate format both on the batch layer and the streaming layer. Thank you for being here on the show. Thank you so much. And thank you for watching. This is my architecture.