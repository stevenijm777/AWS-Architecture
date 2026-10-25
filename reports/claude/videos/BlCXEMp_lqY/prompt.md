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
      "service": "UserConsumerTV",
      "name": "USER CONSUMER TV",
      "type": "UserConsumerTV",
      "rationale": "Smart TV / Consumer TV client device streaming telemetry data."
    },
    {
      "service": "KinesisDataStream",
      "name": "KINESIS DATA STREAMS",
      "type": "KinesisDataStream",
      "rationale": "Amazon Kinesis Data Streams ingesting real-time video/telemetry streams from Consumer TV."
    },
    {
      "service": "Firehose",
      "name": "KINESIS FIREHOSE",
      "type": "Firehose",
      "rationale": "Amazon Kinesis Data Firehose delivering streaming data to S3 and Redshift."
    },
    {
      "service": "S3",
      "name": "AMAZON S3",
      "type": "S3",
      "rationale": "Amazon S3 bucket receiving raw data stream from Kinesis Firehose."
    },
    {
      "service": "RedShift",
      "name": "AMAZON REDSHIFT",
      "type": "RedShift",
      "rationale": "Amazon Redshift data warehouse receiving loaded data from Kinesis Firehose and feeding QuickSight."
    },
    {
      "service": "QuickSight",
      "name": "AMAZON QUICKSIGHT",
      "type": "QuickSight",
      "rationale": "Amazon QuickSight business intelligence tool visualizing analytics from Redshift."
    }
  ],
  "visual_connections": [
    {
      "source_label": "USER CONSUMER TV",
      "target_label": "KINESIS DATA STREAMS",
      "arrow_direction": "right",
      "description": "User Consumer TV streams data to Amazon Kinesis Data Streams."
    },
    {
      "source_label": "KINESIS DATA STREAMS",
      "target_label": "KINESIS FIREHOSE",
      "arrow_direction": "right",
      "description": "Kinesis Data Streams passes stream records to Kinesis Firehose."
    },
    {
      "source_label": "KINESIS FIREHOSE",
      "target_label": "AMAZON S3",
      "arrow_direction": "up_right",
      "description": "Kinesis Firehose delivers data to Amazon S3 bucket."
    },
    {
      "source_label": "KINESIS FIREHOSE",
      "target_label": "AMAZON REDSHIFT",
      "arrow_direction": "down_right",
      "description": "Kinesis Firehose loads streaming data into Amazon Redshift."
    },
    {
      "source_label": "AMAZON REDSHIFT",
      "target_label": "AMAZON QUICKSIGHT",
      "arrow_direction": "right",
      "description": "Amazon Redshift feeds analytical datasets into Amazon QuickSight."
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
https://www.youtube.com/watch?v=BlCXEMp_lqY

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I'm Matt from AWS. Today I'm joined by Abhishek from Vizio. Thanks for joining. Thanks Matt. So tell us about Vizio. Vizio is one of the largest TV and sound bar makers in America and our focus is on making the smart TVs and bringing you a better experience for our customers. Great. So these TVs are not the TVs that our parents had. They're smart like you said they have a lot of data, a lot of telemetry. So I see we have a TV over here. Tell us about how you're using that TV data with AWS. So TVs do generate a lot of data for us and that data could be logs. Yeah. Right. And we do post a lot of performance telemetry. Sure. For and whatever is happening on the TV. And then there is also some user data where we do want to know how our application is being used to bring even better experience for our users. Yeah. Sure. So you can do better things for customers with this data. So the raw data doesn't tell you much. You have to process it, ingest it. Yeah. So I see you have Kinesis. Is that kind of your front door to the cloud? It is true. The Kinesis data streams are our front door and everything is being piped through Kinesis. And we do run an eight shard Kinesis pipeline, which we have not yet needed to scale it up. Okay. So these TVs are talking directly to Kinesis to ingest or to send their data up to the cloud? Yeah. And you could, but you haven't had to scale the Kinesis by adding or removing shards? Not yet. No. Okay. Great. So data gets to Kinesis from the TVs, different streams, I imagine different types of data, logs, performance user. Do these have different characteristics? Are they in different formats? They are all different formats and different columns, if you will. Yeah. And the best part here is that we are not sticking to any particular schema yet. So we are free to send any, anything we want in any format. And then we will pipe it through Firehose. Kinesis Firehose takes the data as is and dumps it into Redshift. So you're using Redshift as a data warehouse. So you collect the data, it goes through Kinesis, you use Firehose to ingest it into Redshift. I see S3 down here. Does that mean you're using Redshift Spectrum or how are you using S3? S3 is just our data store and we, data is cheap, so we just keep it there forever for future use. We do not necessarily import all the columns we send out here to Redshift. Okay. So the raw data sort of finds its long-term home in S3. Yeah. And then a subset of that gets ingested into the data warehouse. That's correct. Okay. Have you always used Redshift or have you experimented with different types of databases? We did start experimenting with AWS Aurora. Yeah. And we figured out that billions of rows do not aggregate well in Aurora and that was just not the right use case for it. Okay. Yeah. I mean, that's why we have different types of data stores and databases in AWS for different purposes. And certainly for the scale maybe you're talking with all the TVs out there. How much are you talking? What kind of scale are we talking about? We are talking about millions of connected devices and billions of events per month. Okay. So billions of events per month that you want to aggregate. Yeah. It's definitely an analytics use case. Great case for Redshift. So the data, I understand so far you persist in an S3 long-term. I guess you could reload it if you ever need to replace the database or data warehouse. That is true. And we did that when we experimented with Aurora. Yeah. We had to quickly migrate to using Redshift. And at that time we had everything in S3 and in the data streams. We were able to just reload everything in Redshift without any data loss. Okay. And then how do you actually visualize the data? How do your users make use of it? For that we use Amazon QuickSight. And QuickSight is a great tool for visualizing aggregation. And we do use the in-built in-memory database called Spice. Yeah. Where we write custom SQL or custom queries to download the data from Redshift to the Spice data sets. From where it's snappy. It's very snappy to create, slice and dice the data and create the reports you want. Great. So you take subsets of data using custom SQL. You put it into the in-memory Spice database for QuickSight. So your users can visualize it quickly and generate the reports. Yeah. Okay. That's very cool. I love the scale that you're operating at. How long did it take you to build this whole thing? So we started this project with Amazon Professional Services help. Yeah. And I think within a few weeks span we had the first prototype and we were like fourth or fifth week we were in the production. Wow. So from zero to users being able to use QuickSight and run reports on it, this was like maybe six weeks. It's great to hear you're having success with professional services in like six weeks to production for an analytics, you know, where we're talking billions of messages is pretty amazing. It is pretty amazing. Yeah. Yeah. And Redshift by the nature of it, it is great with running large aggregation because it fetches columns. So the IO is very optimized and we could see the results right away in the throughput. Absolutely. The benefits of a column in your database like Redshift for large scale analytics. Very cool to see. Well, I like it sort of an elegant solution to a scale problem to make use of all of this data that our smart TVs are able to produce these days. Thanks for sharing with us. It's very interesting. Thanks, Matt. Thanks for watching. This is my architecture.