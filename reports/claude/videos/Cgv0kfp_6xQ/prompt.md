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
      "service": "UserConsumerMobile",
      "name": "IOS",
      "type": "UserConsumerMobile",
      "rationale": "Cliente móvil iOS que conecta hacia el API Gateway (GW)."
    },
    {
      "service": "UserConsumerMobile",
      "name": "Android",
      "type": "UserConsumerMobile",
      "rationale": "Cliente móvil Android receptor de respuestas/notificaciones desde MCS."
    },
    {
      "service": "EKS",
      "name": "MEDIA",
      "type": "EKS",
      "rationale": "Ícono naranja de Kubernetes/EKS rotulado MEDIA, dentro del recuadro entrecortado rotulado 'EKS'. Sobre el borde superior de ese recuadro hay una caja rectangular vacía con el texto 'GW', SIN ícono de servicio: no se transcribe como entidad, y las flechas que la atraviesan se registran entre los nodos iconificados de cada extremo. Al lado del recuadro hay anotaciones manuscritas en rojo '900+EKS' y '1000+'."
    },
    {
      "service": "EKS",
      "name": "MCS",
      "type": "EKS",
      "rationale": "Ícono naranja de Kubernetes/EKS rotulado MCS, dentro del mismo recuadro entrecortado 'EKS'. Es el que más flechas concentra."
    },
    {
      "service": "EKS",
      "name": "SNAP DB",
      "type": "EKS",
      "rationale": "Microservicio de base de datos intermedia (nodo c) con ícono EKS dentro del cluster."
    },
    {
      "service": "EKS",
      "name": "FRIEND GRAPH",
      "type": "EKS",
      "rationale": "Microservicio de grafo de contactos (nodo d) con ícono EKS dentro del cluster."
    },
    {
      "service": "CloudFront",
      "name": "CloudFront",
      "type": "CloudFront",
      "rationale": "CDN CloudFront receptor desde MEDIA y emisor hacia S3."
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "Almacenamiento S3 receptor desde CloudFront."
    },
    {
      "service": "ElastiCache",
      "name": "ElastiCache",
      "type": "ElastiCache",
      "rationale": "Caché ElastiCache conectado desde MCS."
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": "Base de datos DynamoDB receptora desde SNAP DB."
    }
  ],
  "visual_connections": [
    {
      "source_label": "IOS",
      "target_label": "MEDIA",
      "arrow_direction": "down_right",
      "description": "Flecha curva desde IOS que entra en la caja 'GW' (rótulo sin ícono, sobre el borde del recuadro EKS) y sale de ella hacia abajo-izquierda con punta de flecha sobre MEDIA."
    },
    {
      "source_label": "MEDIA",
      "target_label": "CloudFront",
      "arrow_direction": "right",
      "description": "Flecha desde MEDIA hacia CloudFront."
    },
    {
      "source_label": "CloudFront",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha desde CloudFront hacia S3."
    },
    {
      "source_label": "IOS",
      "target_label": "MCS",
      "arrow_direction": "down_right",
      "description": "Segunda flecha que sale de la caja 'GW' hacia abajo-derecha con punta sobre MCS. Como 'GW' es solo un rótulo sin ícono, la flecha se registra desde IOS, el único nodo iconificado que entra a esa caja."
    },
    {
      "source_label": "MCS",
      "target_label": "Android",
      "arrow_direction": "right",
      "description": "Flecha desde MCS hacia el cliente Android."
    },
    {
      "source_label": "MCS",
      "target_label": "FRIEND GRAPH",
      "arrow_direction": "down",
      "description": "Flecha desde MCS hacia el microservicio FRIEND GRAPH."
    },
    {
      "source_label": "MCS",
      "target_label": "SNAP DB",
      "arrow_direction": "down",
      "description": "Flecha desde MCS hacia el microservicio SNAP DB."
    },
    {
      "source_label": "SNAP DB",
      "target_label": "DynamoDB",
      "arrow_direction": "right",
      "description": "Flecha desde SNAP DB hacia DynamoDB."
    },
    {
      "source_label": "MCS",
      "target_label": "ElastiCache",
      "arrow_direction": "right",
      "description": "Flecha desde MCS hacia ElastiCache."
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
https://www.youtube.com/watch?v=Cgv0kfp_6xQ

## FULL TRANSCRIPT:
Welcome to This is My Architecture. My name is Andrea, and I'm here with Saral from Snap. Hi, Saral. Welcome to the show. Thanks for having me. So what do you guys do? So Snapchat is an app that hundreds of millions of people around the world use to communicate with their close friends. Our focus is on close friendships, and we enable the fastest way to communicate by building features like AR lenses, maps, bitmoji, and spotlight. Awesome. So today we're going to talk about the platform, which resides on AWS. I'm super excited. And let's look at an end-to-end workflow, sending a snap using Snapchat. This must be massive scale. I mean, how many users do you have and how many snaps do you deal with on a daily basis? Yeah, that's a great question. So we have over 300 million daily active users on the platform. Okay, that's massive scale. Let's look at the lifecycle. You know, I'm a user. I'm using iOS, Android. What's the flow? What's the first thing that happens when I send a snap? Right. The first thing which happens is the iOS app uses our gateway, which is an EKS service which we have built, to talk to the media delivery service and send the snap to CloudFront and purchase it in S3, just so that it's closer to the recipient when they need it. I see. Okay. So we're going to go into our own database called SnapDB, which under the covers uses DynamoDB. I see. So what made you choose to create your own SnapDB as a front end to DynamoDB? Yeah. So we're talking about a lot of scale on DynamoDB, and we chose to build some higher level features ourselves, like transactions, TTL, as well as how to efficiently kind of deal with ephemeral data in our own layer. We also deal with incremental state synchronization so that we are not putting a lot of burden on DynamoDB and it keeps our costs in control. I see. So you're storing the metadata in DynamoDB, right? So what level of scale are we talking about here? So we are talking about 400 terabytes of data, which we store in DynamoDB. And interestingly, we run nightly scans on DynamoDB, which run 2 billion rows per minute to kind of do various things on DynamoDB, including looking for friend suggestions or deleting ephemeral data as well. So we are very heavy users of DynamoDB. Okay. So you do nightly scans just to make sure that it maintains the relationships and friends and everything. Right. Okay. So we talked about, you know, the send snap. What about the receiving end? What happens? Right. So the most interesting part about receiving snap is it is very latency sensitive, right? Your friend wants to get the message as soon as possible. So the first thing the messaging service does is it looks up a connection ID, a server ID from ElastiCache to get access to the persistent connection which a server has to the Android client or to any clients in the world so that we can quickly push a message to that client. So we look up the metadata from the ElastiCache. We find the server, which this client is already connected to. And through that gateway, we basically send the message to the recipient. I see. And then you retrieve the data as well, the image or video through and chat information through S3. Exactly. So that media ID was persisted all the way through to ElastiCache as well as DynamoDB. So we use that media ID to kind of get the information from CloudFront. Makes mostly sense. Now, this is massive scale. Like, can you give us some quantitative details of, like, what size cluster are you running? Just give us some numbers. Yeah. We have over 900 EKS clusters running. And many of those clusters have over 1,000 plus instances, which makes this, like, a really heavy kind of service graph, essentially. Makes perfect sense. And, I mean, how do you keep this at the low cost, high performance? I think you mentioned latency is hugely important on the receiving side, but also the cost. Yeah, for sure. Like, latency, when we moved to this architecture, we were able to reduce the P50, the median latency, of sending a snap by 24%, which is a huge business impact for us. Secondly, in terms of cost, because we use so much compute footprint, we are always looking at things like auto-scaling as well as using the right instant types like Graviton to keep our compute cost low. That's fantastic. I mean, this is interesting architecture because you're dealing with massive amount of data. And you're cleverly kind of coming up with ways, innovative ways with, for example, SnapDB to reduce latency and really make that user experience better. And then use of Graviton and others to keep the cost low. So, thanks for walking us through this architecture. Thank you so much. And thanks for watching. This is my architecture.