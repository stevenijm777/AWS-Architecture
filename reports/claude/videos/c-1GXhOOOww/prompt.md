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
      "service": "UserConsumerWeb",
      "name": "User (1)",
      "type": "UserConsumerWeb",
      "rationale": "Primer actor de usuario con flechas bidireccionales hacia la zona CDN."
    },
    {
      "service": "UserConsumerWeb",
      "name": "User (2)",
      "type": "UserConsumerWeb",
      "rationale": "Segundo actor de usuario con flecha unidireccional hacia la zona CDN."
    },
    {
      "service": "CloudFront",
      "name": "CDN (CloudFront)",
      "type": "CloudFront",
      "rationale": "Zona entre líneas entrecortadas etiquetada como CDN, mapeada a CloudFront."
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "Ícono de S3 a la derecha con conexión bidireccional hacia CDN."
    },
    {
      "service": "ThirdParty",
      "name": "AppSync",
      "type": "ThirdParty",
      "rationale": "AWS AppSync (mapeado a ThirdParty por no estar en el catálogo cerrado)."
    },
    {
      "service": "Lambda",
      "name": "AWS Lambda (1)",
      "type": "Lambda",
      "rationale": "Ícono de Lambda en la ruta de AppSync hacia DynamoDB."
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": "Base de datos DynamoDB que recibe conexiones de AppSync y AWS Lambda (1)."
    },
    {
      "service": "ApiGateway",
      "name": "API Gateway",
      "type": "ApiGateway",
      "rationale": "Ícono de API Gateway conectado desde CDN hacia AWS Lambda (2)."
    },
    {
      "service": "Lambda",
      "name": "AWS Lambda (2)",
      "type": "Lambda",
      "rationale": "Ícono de Lambda en la ruta de API Gateway hacia SQS."
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": "Cola SQS con conexión bidireccional desde AWS Lambda (2)."
    }
  ],
  "visual_connections": [
    {
      "source_label": "User (1)",
      "target_label": "CDN (CloudFront)",
      "arrow_direction": "right",
      "description": "Flecha saliente desde User (1) hacia CDN."
    },
    {
      "source_label": "CDN (CloudFront)",
      "target_label": "User (1)",
      "arrow_direction": "left",
      "description": "Flecha entrante hacia User (1) desde CDN."
    },
    {
      "source_label": "User (2)",
      "target_label": "CDN (CloudFront)",
      "arrow_direction": "right",
      "description": "Flecha desde User (2) hacia CDN."
    },
    {
      "source_label": "S3",
      "target_label": "CDN (CloudFront)",
      "arrow_direction": "left",
      "description": "Flecha desde S3 hacia CDN."
    },
    {
      "source_label": "CDN (CloudFront)",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha desde CDN hacia S3."
    },
    {
      "source_label": "CDN (CloudFront)",
      "target_label": "AppSync",
      "arrow_direction": "right",
      "description": "Flecha desde CDN hacia AppSync."
    },
    {
      "source_label": "AppSync",
      "target_label": "AWS Lambda (1)",
      "arrow_direction": "right",
      "description": "Flecha desde AppSync hacia AWS Lambda (1)."
    },
    {
      "source_label": "AWS Lambda (1)",
      "target_label": "DynamoDB",
      "arrow_direction": "right",
      "description": "Flecha ida desde AWS Lambda (1) hacia DynamoDB."
    },
    {
      "source_label": "DynamoDB",
      "target_label": "AWS Lambda (1)",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde DynamoDB hacia AWS Lambda (1)."
    },
    {
      "source_label": "AppSync",
      "target_label": "DynamoDB",
      "arrow_direction": "right",
      "description": "Flecha directa desde AppSync hacia DynamoDB."
    },
    {
      "source_label": "CDN (CloudFront)",
      "target_label": "API Gateway",
      "arrow_direction": "right",
      "description": "Flecha desde CDN hacia API Gateway."
    },
    {
      "source_label": "API Gateway",
      "target_label": "AWS Lambda (2)",
      "arrow_direction": "right",
      "description": "Flecha desde API Gateway hacia AWS Lambda (2)."
    },
    {
      "source_label": "AWS Lambda (2)",
      "target_label": "SQS",
      "arrow_direction": "right",
      "description": "Flecha ida desde AWS Lambda (2) hacia SQS."
    },
    {
      "source_label": "SQS",
      "target_label": "AWS Lambda (2)",
      "arrow_direction": "left",
      "description": "Flecha vuelta desde SQS hacia AWS Lambda (2)."
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
https://www.youtube.com/watch?v=c-1GXhOOOww

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I am Han and today I'm joined by Gabriel from Anchor. Welcome. Thank you for having us. Before we get started, tell us a little bit about Anchor. Yes, of course. Anchor is a ticketing platform. Today we have more than 40 tenants on the platform. We actually serve tickets for daytime experiences, including, for example, the Statue of Liberty cruises that take you to the island. Naiara Falls, of course, you see the falls in Canada, Alcatraz Island, and we also have some ferry systems like the NYC ferry. Pretty cool. So let's say I'm one of those tenants on your platform. How do I create an event? Yes, of course. So, I mean, in the last six months we actually onboarded more than 20 new tenants into the platform. So nowadays we use a wizard that walks you through the different steps that you have to go through to select the different options that you want as a new tenant, right? So that first, I mean, of course, it's a web application that, you know, the first thing we hit is the CDN. So the CDN, because it's our code, it hits the AppSync that is our GraphQL gateway, you know? So it goes through here. And then we have some resolvers that basically tell Lambda that it needs to go and fan out to different subroutines, right? So then Lambda sets a bunch of SQS messages that later will get reprocessed by Lambda, right? And then there's an interaction that happens between Lambda and DynamoDB just to finish the setting of the whole tenancy. Gotcha. So how do you enable the multi-tenancy here? Yes. Okay. So DynamoDB, because of the nature of the partitions and everything, we use partition keys for each of the tenants. So we share the same tables, but everything is partitioned by the tenant. Yeah. That's awesome. So let's say I'm a customer. I would like to say to go to the Statue of Liberty, et cetera, right? So how does that work? Yeah, of course. So we have another of the clients of the system is going to be the customer, right? At the same time, the customer can come from multiple different channels. So we have the Omni channel that can be you're purchasing from the mobile app or the website or a third-party reseller. When you look up for a Statue of Liberty, you're probably going to find one of the resellers like Expedia, Viator, or Get Your Guide making one of our offerings, right? Trying to sell one of the offerings. So if that's the case, depending on where your channel you're trying to sell, the request is going to first hit the CDN, right, from the client. And then, for example, if it is a reseller, an OTA, they will go through most likely a third-party API that we implemented for them. That is a regular REST endpoint, right? So it will go to API Gateway, and then it's going to hit the same lambdas that the other channels, mobile apps, and websites that we own are going to go through, right? So if you have a website, for example, if you start your customer journey hitting one of our websites and not going through the OTAs, because we like the whole serverless infrastructure, what we want is just to first show you what is the offering of a ticket, right? Like the description of the event and some nice pictures and descriptions, et cetera. So that's all going to be hosted on the S3 bucket serving as an HTTP server, right? So then it hits the CDN, the CDN returns back that to the client, and the client will be able to browse, go navigate, et cetera. When it's time to service the dynamic content, then the CDN knows now it's time to hit AppSync, right? So it goes through GraphQL, it takes a node of the graph, and it processes that using lambda. We sometimes use also straight Dynamo resolvers, right, that can be later mapped and reused using the pipeline resolvers that are built into AppSync. Gotcha. So you're capturing the booking experience, but also the experience itself, right? Yes. Yeah. So when it's time to actually borrow the experience, right, the customer, so the first thing we do is just check them in, right? So check them in. We also have a mobile application that is the checking application. So they go, we look at the booking, or we scan the ticket, et cetera, et cetera, and it goes through, again, the same flow, AppSync, Lambda. It goes, makes a dance with DynamoDB, and SQS puts some messages that will be processed later, right? Customer service, post experience, or anything that needs to happen after the checking process, it puts a message in SQS, and then later gets processed by Lambda. Gotcha. So they're able to do the booking and also capture the experience and also potentially get a feedback from the property. Yes, of course. Yes, it is. So after the check-in, right, we put messages in SQS, and later an email gets sent to the customer so they can reply back and, you know, remind them to go and write a review on the experience. Awesome. Well, that's a really awesome architecture at SCALE, so thank you so much for sharing. Thank you. And thank you for watching This Is My Architecture. .