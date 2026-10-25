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
      "service": "UserCompanyDeveloper",
      "name": "Developer (Casco)",
      "type": "UserCompanyDeveloper",
      "rationale": "Persona con casco de constructor."
    },
    {
      "service": "UserCompanyAnalyst",
      "name": "Analyst (Monopoly)",
      "type": "UserCompanyAnalyst",
      "rationale": "Persona de enmedio con sombrero tipo Monopoly."
    },
    {
      "service": "UserConsumerWeb",
      "name": "User (Niño)",
      "type": "UserConsumerWeb",
      "rationale": "Tercera persona (niño)."
    },
    {
      "service": "EC2",
      "name": "EC2 (1)",
      "type": "EC2",
      "rationale": "Primer ícono de EC2 al que conecta la persona de enmedio."
    },
    {
      "service": "DirectoryService",
      "name": "Active Directory",
      "type": "DirectoryService",
      "rationale": "Servicio Active Directory (AD) conectado con EC2 (1)."
    },
    {
      "service": "EC2",
      "name": "EC2 (2)",
      "type": "EC2",
      "rationale": "Segundo ícono de EC2 al otro lado del divisor."
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "Ícono de S3 receptor de EC2 (2) y EMR."
    },
    {
      "service": "EMR",
      "name": "EMR",
      "type": "EMR",
      "rationale": "Ícono de EMR que conecta hacia S3."
    },
    {
      "service": "KMS",
      "name": "KMS",
      "type": "KMS",
      "rationale": "Ícono de KMS entre S3 y RDS."
    },
    {
      "service": "RDS",
      "name": "Amazon RDS",
      "type": "RDS",
      "rationale": "Base de datos RDS destino de KMS."
    }
  ],
  "visual_connections": [
    {
      "source_label": "Analyst (Monopoly)",
      "target_label": "EC2 (1)",
      "arrow_direction": "right",
      "description": "Flecha desde la persona de enmedio hacia EC2 (1)."
    },
    {
      "source_label": "EC2 (1)",
      "target_label": "Active Directory",
      "arrow_direction": "right",
      "description": "Flecha entre EC2 (1) y Active Directory."
    },
    {
      "source_label": "EC2 (2)",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha desde EC2 (2) hacia S3."
    },
    {
      "source_label": "EMR",
      "target_label": "S3",
      "arrow_direction": "right",
      "description": "Flecha desde EMR hacia S3."
    },
    {
      "source_label": "S3",
      "target_label": "KMS",
      "arrow_direction": "right",
      "description": "Flecha desde S3 hacia KMS."
    },
    {
      "source_label": "KMS",
      "target_label": "Amazon RDS",
      "arrow_direction": "right",
      "description": "Flecha desde KMS hacia Amazon RDS."
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
https://www.youtube.com/watch?v=SSWwnNVYi_Q

## FULL TRANSCRIPT:
Hi, I'm Simon from AWS and this is This is My Architecture. I'm joined today by Ed from NHS Digital. Hello. Let's start by telling me a little bit about NHS Digital. What do you guys do? So we're the information and technology partner for the NHS. Okay, and before we get into the architecture, let's talk a little bit about the scenario behind the architecture. What is this doing and how does it help? So what we're looking at here is the architecture behind the data access environment, which we're putting on AWS to start to move away from some of our legacy systems that we currently run within NHS Digital. Okay, so let's get into the architecture itself. Let's start going from left to right. We've got a number of users on the left-hand side. Who do they represent? So these represent internal teams within NHS Digital. Okay, and the EC2 instance on this side of the dotted line? So this side is effectively a public gateway and users can log into something called Guacamole here and from there they're effectively in a sandbox, which is on the right-hand side of this drawing, where they can look at and analyse data, but they can't get any of that data out of the system. So it's very important. This side is very secure to us. And the users ultimately, they authenticate via directory services so that we know who they are. And their role as a user is also used within the data processing tools to give them access to the right data. So we use something called Apache Ranger to make sure that users only see what they're meant to see. And yeah, we can control access that way. Okay, and I noticed you've got S3 on the right-hand side here. Presumably you're storing data there? That's right. So we are moving existing data sets and converting them to Parquet format and we're putting them into S3 here. Okay. And what are you doing to secure this data? Presumably it's confidential data you're storing? That's right. So we are using KMS to provide a key to encrypt that data. It's all encrypted in transit. And any other information within the system is also encrypted. Okay. And are you encrypting that data at rest as well? That's right. Yes. Yeah. It's encrypted always. Okay. So we've talked about the security. Talk to me a little bit more about what you're using EMR for and what's it doing? Yeah. So EMR is running the analytics jobs we want to run and it's providing a consistent compute layer for our data. So EMR reads the data from S3 and then we're able to form those analytics jobs for people. Okay. And let's take a step back. So how did you arrive at this architecture? Presumably you've gone through a number of steps to get there. Tell me about that journey. Sure. We were looking at, so we've got a drive towards moving toward cloud infrastructures and we looked at various options. So we looked at Cloudera, EMR and various others. We also looked on-prem type solutions. And ultimately we found that the flexibility of running something on EMR and the scale was kind of fit our use case quite well. Okay. And from producing this architecture, what have been the benefits? What have NHS Digital seen as a result of this? So the key benefits of moving to this architecture are in the performance of those analytics jobs. So what previously may have taken hours can now take minutes or seconds. We're also able to give much more fine-grained control over what people can and can't see and a stronger audit within the infrastructure as well. We're also able to, from a functional perspective, put in a broader range of tooling than we're used to using today. So things like RStudio, Jupiter Hub, Hue, various others. Because ultimately NHS Digital wants to move in the direction more towards machine learning and getting more value from the data that it holds and not just necessarily doing what it does today. And is that the long-term aspiration then to try and get more value out of that data? That's right. Some of the processing that we try and do today is hamstrung by the technical limitations, what we have and the kind of scale. So moving to this architecture allows us to do those things. OK, so if I were to summarise what you've created here is a highly secure environment, which has allowed you to process data faster than you have done previously. But it sounds like you're still evolving that and you're looking to improve it in the future. Yeah, that's right. This is an evolving service and we're expanding out to more and more teams that want to use it. And they are moving away from their existing tools. And ultimately, we hope to turn off the existing estate so that that's when we'll see the real value benefits of doing this. Well, thank you, Ed, for joining us today. And thank you very much for joining us on This Is My Architecture.