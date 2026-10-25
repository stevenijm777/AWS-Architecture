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
      "service": "UserCompanyDataStream",
      "name": "UserCompanyDataStream",
      "type": "UserCompanyDataStream",
      "rationale": ""
    },
    {
      "service": "KinesisDataStream",
      "name": "KinesisDataStream #1",
      "type": "KinesisDataStream",
      "rationale": ""
    },
    {
      "service": "KinesisDataStream",
      "name": "KinesisDataStream #2",
      "type": "KinesisDataStream",
      "rationale": ""
    },
    {
      "service": "Neptune",
      "name": "Neptune",
      "type": "Neptune",
      "rationale": ""
    },
    {
      "service": "OpenSearch",
      "name": "OpenSearch",
      "type": "OpenSearch",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Shard Service",
      "type": "ThirdParty",
      "rationale": "Shard Service"
    },
    {
      "service": "ThirdParty",
      "name": "Slack, email, splunk",
      "type": "ThirdParty",
      "rationale": "Slack, email, splunk"
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": ""
    },
    {
      "service": "CloudWatch",
      "name": "CloudWatch",
      "type": "CloudWatch",
      "rationale": ""
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserCompanyDataStream",
      "target_label": "KinesisDataStream #1",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "KinesisDataStream #1",
      "target_label": "Neptune",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "KinesisDataStream #1",
      "target_label": "KinesisDataStream #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "KinesisDataStream #2",
      "target_label": "DynamoDB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "KinesisDataStream #2",
      "target_label": "Slack, email, splunk",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Neptune",
      "target_label": "OpenSearch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Neptune",
      "target_label": "DynamoDB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Neptune",
      "target_label": "CloudWatch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Neptune",
      "target_label": "KinesisDataStream #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "OpenSearch",
      "target_label": "CloudWatch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudWatch",
      "target_label": "Shard Service",
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
https://www.youtube.com/watch?v=6EUknQqaV1w

## FULL TRANSCRIPT:
Hello and welcome to This Is My Architecture. I'm here with Shrapria from Cloud Health by VMware. Hi, Shrapria. Hi, thanks for having me here. Yeah, we're happy to have you. Can you tell me a little bit about Cloud Health by VMware? Sure. So Cloud Health Secure State is a cloud security and monitoring platform. We help our customers mitigate security and compliance risks through our intelligent real-time insights. That's great. I'm really looking forward to diving in and learning a little bit more. So can you start where we would do the collection piece? Sure. So we have primarily two modes of collection. The main aspect, like I mentioned, is the real-time detection of security violations. So for that, we leverage the cloud providers' native security event streams, which is like CloudWatch or activity log in case of Azure. And once the events are coming into our system, we have a collection framework which evaluates those events and determines the current state of the resource and publishes those resources into a Kinesis data stream. Awesome. So as an architect, what challenges would you face in this architecture? Right. So one of the main challenges, as with any data pipeline, is the scale that we have to handle, right? So we are supporting three major cloud providers today. And each of these cloud providers have a lot of services that we also support. So given that, we are talking about billions of events per day. And that scale is pretty huge to handle. And with that, topped by the number of resources we collect and monitor. And to provide real-time insights, we have to exercise a graph-based exploration on those resources. So those are the primary challenges we have in our system. Yeah. No, that's great. So you mentioned the graph-based piece. I'm curious to hear how Neptune plays in. Sure. So once the cloud resources are ingested into our data stream, we have the consumer, which publishes those resources into Amazon Neptune, right? So the primary usage of Amazon Neptune is a graph database, like we all know. And the cloud uses data is a highly interconnected data set. And we wanted to provide our customers graph-based exploration capabilities. Neptune allows us to do that efficiently. And on top of that, it also provides a read scale-out that we require for executing a lot of rules on them, on the cloud resources. And we also chose Neptune because it's schema-less. So one of the key considerations in our system is as we onboard more cloud providers, support more resource type, each of them have varied configurations. And we want our data layer to be agnostic of those representations. And that is another reason that we had to choose Neptune. Yeah. No, that makes sense. How many assets are we talking about here? Yeah. I think in terms of, like I said, we are handling billions of events, which amounts to about 50 million-plus resources that we collect and monitor in our pipeline. And this number is an ever-growing number. Yeah. Wow. That's a lot. That's a lot of assets to process. So after the data goes into Neptune, what happens next? Right. So I think we also wanted to provide our customers capability to slice and dice this cloud resources data in various forms and shape. We want them to have reporting analytical capabilities, search aggregations. And also we want them to visualize how the resource configurations have changed over time. So one thing we found out is there is no one database that can perform all these more efficiently. So apart from Neptune, which is our primary persistence, we do have Elasticsearch and DynamoDB as our backing stores to power some of the other use cases. Yeah. No, that makes sense. Those are great to use to process that. But I am very curious to hear more about this area over here. Why are we using sharding? Sure. So I think Neptune provides the read scale out that we require to exercise and execute the rules. We also wanted a strategy to scale our writes out. And the way we do that is with our sharder service. So sharder service basically provides us a logical grouping of data that we want to store in our provision Neptune clusters. And the sharder service is intelligent in itself that it uses this CloudWatch metrics from Neptune and Elasticsearch to kind of determine the shard capacity of these provision Neptune clusters. So it uses CPU memory and few other parameters to determine, OK, given Neptune is full or not. And that allows us to efficiently load balance our customers' data in the provision Neptune clusters. So that information kind of flows back, which allows us to make decisions at this front. Yeah. No, that's really smart use. So once that data is sharded and put back into Neptune, where does it go? Sure. So once the data is all persisted, the next thing in our pipeline is the rule executions, right? So the incoming event along with the resource changes are then propagated to our rule execution pipeline. The rule engine that we have is smart enough to determine what rules needs to be executed for a given event and the resource changes. And this could be like thousands of rules, right, that gets executed. So we fronted with the Kinesis data stream. And we exercise this over the Neptune graph database to perform those security checks. And if it detects any security violations, those are again persisted in our DynamoDB. And also we provide real-time notifications to our customers through various channels. We have support for Slack, email, Splunk, and the like. That's awesome. That's really great for your customers. Shafriya, thank you so much for joining us today. I've learned a lot about CloudHealth SecureState. Thank you. And thank you for watching This Is My Architecture.