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
      "service": "UserConsumerSatellite",
      "name": "Satellite",
      "type": "UserConsumerSatellite",
      "rationale": "Ícono de satélite dibujado a mano al inicio del flujo."
    },
    {
      "service": "EC2",
      "name": "EC2 Spot",
      "type": "EC2",
      "rationale": "Instancia EC2 Spot que recibe del satélite y conecta hacia S3 y RDS."
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "Ícono de S3 con conexiones bidireccionales hacia AWS Fargate y Lambda."
    },
    {
      "service": "Fargate",
      "name": "AWS Fargate",
      "type": "Fargate",
      "rationale": "Contenedor AWS Fargate con conexiones bidireccionales hacia S3, User, ElastiCache y RDS."
    },
    {
      "service": "UserConsumerWeb",
      "name": "User",
      "type": "UserConsumerWeb",
      "rationale": "Actor de usuario con conexión bidireccional hacia AWS Fargate."
    },
    {
      "service": "ElastiCache",
      "name": "ElastiCache",
      "type": "ElastiCache",
      "rationale": "Ícono de ElastiCache con conexión bidireccional hacia AWS Fargate."
    },
    {
      "service": "RDS",
      "name": "Amazon RDS",
      "type": "RDS",
      "rationale": "Base de datos RDS que recibe de EC2 Spot, con conexiones hacia AWS Fargate y Lambda."
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "Ícono de Lambda con conexiones bidireccionales hacia RDS y S3."
    }
  ],
  "visual_connections": [
    {
      "source_label": "Satellite",
      "target_label": "EC2 Spot",
      "arrow_direction": "right",
      "description": "Flecha desde el satélite hacia EC2 Spot."
    },
    {
      "source_label": "EC2 Spot",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha desde EC2 Spot hacia S3."
    },
    {
      "source_label": "S3",
      "target_label": "AWS Fargate",
      "arrow_direction": "right",
      "description": "Flecha ida desde S3 hacia AWS Fargate."
    },
    {
      "source_label": "AWS Fargate",
      "target_label": "S3",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde AWS Fargate hacia S3."
    },
    {
      "source_label": "AWS Fargate",
      "target_label": "User",
      "arrow_direction": "right",
      "description": "Flecha ida desde AWS Fargate hacia User."
    },
    {
      "source_label": "User",
      "target_label": "AWS Fargate",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde User hacia AWS Fargate."
    },
    {
      "source_label": "AWS Fargate",
      "target_label": "ElastiCache",
      "arrow_direction": "right",
      "description": "Flecha ida desde AWS Fargate hacia ElastiCache."
    },
    {
      "source_label": "ElastiCache",
      "target_label": "AWS Fargate",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde ElastiCache hacia AWS Fargate."
    },
    {
      "source_label": "EC2 Spot",
      "target_label": "Amazon RDS",
      "arrow_direction": "right",
      "description": "Flecha desde EC2 Spot hacia Amazon RDS."
    },
    {
      "source_label": "Amazon RDS",
      "target_label": "AWS Fargate",
      "arrow_direction": "right",
      "description": "Flecha ida desde Amazon RDS hacia AWS Fargate."
    },
    {
      "source_label": "AWS Fargate",
      "target_label": "Amazon RDS",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde AWS Fargate hacia Amazon RDS."
    },
    {
      "source_label": "Lambda",
      "target_label": "Amazon RDS",
      "arrow_direction": "right",
      "description": "Flecha ida desde Lambda hacia Amazon RDS."
    },
    {
      "source_label": "Amazon RDS",
      "target_label": "Lambda",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde Amazon RDS hacia Lambda."
    },
    {
      "source_label": "Lambda",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha ida desde Lambda hacia S3."
    },
    {
      "source_label": "S3",
      "target_label": "Lambda",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde S3 hacia Lambda."
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
https://www.youtube.com/watch?v=FfSNnH2bbNc

## FULL TRANSCRIPT:
Hi, and welcome to This is My Architecture. I'm Andy, and I'm here with Jacob from Indigo Carbon. Hi, Jacob. Hey, Andy. So, Jacob, can you tell me about Indigo Carbon? Yeah. Indigo is working with individual farmers to help them transition to regenerative agriculture, which is a system of practices to kind of enrich their soil and get paid to do it by people that are emitting CO2 and want to buy offsets for that. So, how do you actually help farmers with this architecture? Yeah. So, there's a lot of different data that needs to be collected in order to actually produce carbon credits. We're able to leverage existing satellites from organizations like NASA to infer a lot of things about the operation on an individual field. It all kind of starts there. Every day throughout the day, we get a series of tiles from them that are kind of modestly processed and corrected for a bunch of things. And we get them in, but we need to do some post-processing both to correct some more and to get it into different formats that are more accessible for stuff downstream. So, we spin up a big kind of cluster of spot instances as quickly as possible, process all this data as it comes in, and spin it back down. We store those outputs in a combination of S3 and RDS. RDS has the metadata in it, and S3 actually has like the big bulk data itself. Can you give me a sense of how much data we're actually talking about here? Yeah. So, our catalog spans back actually like 30 years. Most of our data is kind of in like the 10-year time frame. All of that surprises about five petabytes or so, give or take. And every day that grows as we get new imagery in. And that's like 100 gigabytes a day. And that rate increases as we add more data sources that we're doing kind of continuously. Wow. So, after you've ingested this data, what happens next? Yeah. So, we access it in two kind of pretty different ways. One is from direct kind of like user access, and the other is to drive stuff in our models that we ultimately use to generate the carbon credits. We can talk about the user flow first. When they log into our app, one of the first things we show is this map of the United States, and we show some imagery on top of that. And we want it to be like our most up-to-date imagery. We give them the option to select what kind of layer they want from here and which time frame they're talking about. But ultimately, it gets served up as web tiles that come from this Fargate cluster. When you load a map, it gets sliced into 16 or so different tiles, and those come as individual requests to Fargate. Fargate then looks up in RDS which source imagery actually corresponds to that tile. And then it pulls that data from S3. S3 has relatively large compressed chunks of data. And we only need like a small subsection of that for each one of these like source tiles. We actually use one of the kind of main features in S3 that's useful is HTTP range requests. We can read a part of an object in S3 instead of reading the entire thing. We then take all those different little parts of images, and we stitch them back together into a kind of bigger image. We down sample it to the right resolution, and then we'd either do color correction if we're talking about an RGB image, or we do color mapping if we're talking about just like an intensity value. So if you want to show like greenness of your field, that'll be like a zero to one value. We need to map that into like an RGB space. We have a color map for that. And then we serve it back as a tile. So I'm seeing a few other components on here. How does ElastiCache fit into this solution? Yeah, it's pretty simple. We just use Redis in ElastiCache as a kind of central cache for the tiles we've already generated. A lot of the tiles in our system are pretty common. Like I said, when we first load the app for most users, it shows the entire US. Those tiles are seen by everybody. So instead of recomputing those on the fly every time, we compute them on the fly once and store them in ElastiCache here, and read and write from that as needed, and serve back tiles to the user. Okay, excellent. And then so there's one last one other component to this. I'm seeing a lambda over here. Can you tell me what this lambda is actually doing? Yeah, so this is actually a series of lambda functions in here. What is ultimately there to do is try to compute a time series of data from this kind of source data cube. Taking back to the example of like the average greenness on your field, over the course of a year, say it's like 2019, and that goes to 2020, for corn, somewhere in August is kind of your peak greenness, and it'll end up looking in a curve like this. And this can tell you things about like the health of your corn and that kind of thing. You can imagine there's a lot more complex stuff you can do with it. But in order to compute that from this raw imagery, we need to take the area that we're interested in. In this case, it's something that a farmer told us, which is like their field somewhere in there in the grid of Iowa. And there's a little cutout here. So this is custom, this is what the grower is actually farming. So we don't know this ahead of time. So they tell us this, we only need to take it, pass it to this series of lambda functions. And what this does is pretty similar to what the Fargate service does here. Initially, it pulls the imagery that it needs from by looking it up in RDS and then reading stuff from S3. It turns that into kind of the tile of interest that we're doing. And then we clip it to this area of interest, and then can be a summary on it. In this case, we're talking about like the mean of the greenness. That's what it would do, take the average of all the pixels that fall in that field. And then it does that 1000 times over to get that time series. I'm seeing a lot of serverless components on here. Why'd you choose to go with that for this particular architecture? Yeah, so we have we have thousands of input variables here, and all kinds of different locations in the country. We just talked about how like we don't actually know the area that we're really interested in until the farmer tells us. And we have time as well as another component of this. So there's millions of combinations that we could cut this data cube. We get it to a point where it's kind of minimally processed and to do all the other processing on the fly. And it saves us orders of magnitude of cost. Excellent. Jacob, thank you very much for sharing this. It's great to hear how Indigo Carbon is using a largely serverless architecture to help individual farmers with regenerative agriculture. And thank you for watching. This is my architecture.