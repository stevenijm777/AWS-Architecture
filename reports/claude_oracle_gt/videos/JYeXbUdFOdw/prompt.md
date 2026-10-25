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
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda #1",
      "type": "Lambda",
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda #2",
      "type": "Lambda",
      "rationale": ""
    },
    {
      "service": "UserConsumerWeb",
      "name": "UserConsumerWeb",
      "type": "UserConsumerWeb",
      "rationale": ""
    },
    {
      "service": "OpenSearch",
      "name": "OpenSearch",
      "type": "OpenSearch",
      "rationale": ""
    },
    {
      "service": "RDS",
      "name": "RDS",
      "type": "RDS",
      "rationale": ""
    },
    {
      "service": "SES",
      "name": "SES",
      "type": "SES",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Novetiq backend",
      "type": "ThirdParty",
      "rationale": "Novetiq backend"
    }
  ],
  "visual_connections": [
    {
      "source_label": "S3",
      "target_label": "Lambda #1",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "Lambda #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "SES",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "UserConsumerWeb",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda #1",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda #1",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda #2",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda #2",
      "target_label": "OpenSearch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserConsumerWeb",
      "target_label": "Novetiq backend",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserConsumerWeb",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "RDS",
      "target_label": "Novetiq backend",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Novetiq backend",
      "target_label": "RDS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Novetiq backend",
      "target_label": "UserConsumerWeb",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Novetiq backend",
      "target_label": "S3",
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
https://www.youtube.com/watch?v=JYeXbUdFOdw

## FULL TRANSCRIPT:
Hi, I'm Maheen from AWS. Hi, I'm Yogesh from Novantec and this is My Architecture. So today we are going to talk about a data processing architecture pattern using AWS OpenSearch. So Yogesh, I understand you did this for Cybex. So what was the customer challenge you were trying to solve? Yeah, so Cybex is in the business to provide trade data and reports related to the export import. They had around 1.5 billion of records. Initially they used to serve their customer in offline mode. So every time customer had a new requirement whether it is related to a new product or say new country, the entire process to understand the requirement to book the order then churn the data and then serve the report. It used to take a couple of days, right? So they wanted us to provide a cloud solution which can provide flexibility to their customers to get data at any point of time from anywhere within few seconds. First of all, the raw data which is in the format of the CSV or in the Excel file, it's get uploaded into the S3 buckets. Then a Lambda get triggered to validate this data. If there is any discrepancy within the data, then it gets highlighted here. Else, copy of the validated data get uploaded into a different folder within the S3 buckets. Once we have the validated copy here, then the Lambda get triggered to process this validated data and ingest it into the OpenSearch cluster. Here we are doing few more activities like we are creating the query templates and mapping them with relevant indexes. Secondly, we are using the Amazon OpenSearch analyzer to fine-tune queries and enhance performance. And then an aggregated layer is being built on top of the process data to serve the complex reports like the trained analysis report or some other aggregation reports. So, Yagesh, I see you've used an event-driven architecture in this particular instance. So why the event-driven architecture? Yeah. So as I mentioned earlier, when we designed this architecture, at that point of time, we had around 1.5 billion number of records. But over a period of time, this number had been increased by more than 3.5 times. Now we have around 5 billion of records. But still, application is able to provide data and reports having 15 to 20 complex parameters within 2 to 4 seconds. So you can understand that there is no such latency with the huge increase of the number of records using the same architecture. Thank you for explaining how data ingestion works. Tell us how the user is able to then get access to this data. So we have designed two ways to retrieve the data, right? The user can access the data either using the web application or they can use mobile application to retrieve the data. So in case of the web application, user sends the request to the front-end application via the web browser. It has been developed using the Angular. And then the request goes back to the browser and then it's come back to the backend application, right? So this backend application we have developed using the Python. Then request goes directly to the data layer and then response sends back to the user via the backend application. While in case of the mobile apps, request goes directly to the backend application and then to the data layer and then response comes back. And early on you mentioned 5 billion records. How do you keep the costs down for that kind of volume? So you can see, right, we are using the Graviton2 instance for the Amazon OpenSearch. So it helped us really to optimize the cost, right? Initially, if I will compare from the beginning, right, we are saving something between 25 to 30 percent of the operation cost, which is roughly equivalent to the 100K dollar. And when you were explaining the challenge, you mentioned that sometimes reports can take longer to run than the normal latency. So how do you give the best customer experience using this? Yeah, it happens sometimes, right? Sometimes user requests for a report having more than 10,000 records. Then at that point of the time, we upload the report in this S3 bucket and then send an intimation to the user via SES to download this report using the pre-signed URL. That's great for security as well. Yagesh, thank you for sharing your fantastic architecture with us today. Thank you. Thank you. And thank you for watching another episode of This Is My Architecture. Thanks, everyone.