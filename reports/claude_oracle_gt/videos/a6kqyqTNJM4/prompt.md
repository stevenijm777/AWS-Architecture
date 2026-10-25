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
      "name": "UserConsumerWeb",
      "type": "UserConsumerWeb",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "media"
    },
    {
      "service": "CloudFront",
      "name": "CloudFront",
      "type": "CloudFront",
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: request routing"
    },
    {
      "service": "ThirdParty",
      "name": "Load Balancer",
      "type": "ThirdParty",
      "rationale": "Load Balancer"
    },
    {
      "service": "ThirdParty",
      "name": "Mongo DB",
      "type": "ThirdParty",
      "rationale": "Mongo DB"
    },
    {
      "service": "EKS",
      "name": "EKS",
      "type": "EKS",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2 — WORKLOAD_PEEK: Hosting legacy application",
      "type": "EC2",
      "rationale": "WORKLOAD_PEEK: Hosting legacy application"
    },
    {
      "service": "EC2",
      "name": "EC2 — WORKLOAD_PEEK: Hosting tools like prometheus for monitoring",
      "type": "EC2",
      "rationale": "WORKLOAD_PEEK: Hosting tools like prometheus for monitoring"
    },
    {
      "service": "RDS",
      "name": "RDS",
      "type": "RDS",
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
      "source_label": "UserConsumerWeb",
      "target_label": "CloudFront",
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
      "source_label": "CloudFront",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudFront",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudFront",
      "target_label": "Load Balancer",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "CloudFront",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Load Balancer",
      "target_label": "EC2 — WORKLOAD_PEEK: Hosting legacy application",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Load Balancer",
      "target_label": "CloudFront",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Load Balancer",
      "target_label": "EKS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Mongo DB",
      "target_label": "EKS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EKS",
      "target_label": "Load Balancer",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EKS",
      "target_label": "Mongo DB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EKS",
      "target_label": "RDS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2 — WORKLOAD_PEEK: Hosting legacy application",
      "target_label": "Load Balancer",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "RDS",
      "target_label": "EKS",
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
https://www.youtube.com/watch?v=a6kqyqTNJM4

## FULL TRANSCRIPT:
Hello and welcome to This is My Architecture. Today I'm joined by Kays from Syrah Group. Welcome Kays. Hey Mo, happy to be here. Before we start, can you tell us a bit more about Syrah Group? Yeah, sure. Syrah Group is the leading travel group in the region represented by a lot of big brands like Al Musafir, Ila, Tajawal, Lumi, Discover Saudi and Hajjan Umrah for Mawasim. Excellent. Who doesn't like traveling, yeah? Yeah. Amazing. So can you tell us a bit more about the challenges or the problems that you faced and you build the architecture to solve it? Yeah, sure. Being the leading group in the travel sector, you need to be extremely effective in scaling and responding quickly to the market changes. That's from one point. And on the other side, we as a full brands, we want to be a very much customer centric, delivering things that's very relevant to our customers. On top of all of this, having a very proper, agile and speed delivery. Interesting. So let's dive deep into the architecture and walk us through how it works. Sure. Happy to do so. So let's take Al Musafir as an example. Al Musafir receives on an average around 300k requests per minute. This traffic goes through CloudFront. And CloudFront as a CDN helps us to serve our customers in a better way. We are utilizing a very effective and cost efficient storage place like S3 to serve our content, to serve our images. Al Musafir is a very heavy load content platform. On top of all of this, we are utilizing Lambda to decide this traffic coming from which region, this traffic comes from which device, allowing us to serve our customers better and providing the system with the first layer of scaling and resiliency. Amazing. So you use a simple storage service to help you with the static contents on a cost efficient way. And you use Lambda for intelligent at the edge and deciding where to route the traffic. Exactly. Amazing. Okay. So what about the load balancer? What do you do in the architecture? Yeah. When the traffic goes through to our load balancer, at that stage, we want to decide if this is a backend service traffic or if it's a web traffic. Actually, we have here roughly around 60 load balancers to take care of, shall I route this traffic to our backend or to our frontend? And when we discussed the backend, we mentioned earlier, we went through a lot of transformation. Having said that, we have a lot of monolithic systems that change to a proper microservices systems. Our load balancer does not only do load balancing. Actually, it does routing between the legacy and the new. So I see that it can help you with gradually migrating from legacy systems that still hosted in EC2 and bring them into microservices that are hosted in EKS Elastic Kubernetes Service. Right? Yeah. Can you tell us a bit more about the containers and EKS size and what they do? So we actually were successfully migrating around 80% of our services to EKS. EKS here is being used as the core for all of our services, either backend and frontend. Actually, even our frontend is a micro frontend architecture. So we are utilizing EKS here. Roughly we have more than 250 microservices deployed over 1400 bots and production, allowing the system to scale and to adapt to the load and to allow us also to have a proper resilience inside our systems. Oh, amazing. Cool. And then about the data layer, what we have here? So one of the advantages of having a proper microservices systems, allowing you to adapt the data storage and layer to the needs of your service. Yes. Most of our services need no SQL databases. Here we are utilizing a self-managed Mongo instances using EC2. Some of other services are using our RDS capabilities, which is some of the function needs a proper transaction at SQL databases. Yeah. In top of all of that, you are talking about a microservices system and a big part of it is event driven. And here Kafka plays a major role in that. Interesting. So I can see that you have a choice of going with a third party software of your choice on EC2. Yeah. Self-managed or you can go with a initial database service and then use a managed service from AWS. Yeah. So question, how do you ensure that this architecture actually working and you're providing the expected customer experience? We always speak about the benefits of microservices, but actually having a proper monitoring system on top of your services is one of the key things. And I always tell the team, keep monitoring or die trying. Yeah. And in here we are utilizing a lot of services. Some of them are self-managed services. For example, this system allowing us to have an internal look on every single service. We are using CloudWatch to make sure that our both hills are properly shaped. We are using a lot of internal tools like Prometheus, our ELK stack to make sure that we also have an eye on the logs, monitoring the logs. And all of this ties to our alarming system, which we are utilizing Slack and PagerTuty to make sure that the team is on top of everything that's happening inside. Excellent. So I can see again, the choice of going with your own tools on top of EC2 or you use AWS native tools like CloudWatch and have end-to-end view of what's going on. Yeah. Amazing. So what's next? What is your future plans and ideas to improve, you know, the architecture in the future? When you have a microservices system like this, it allows you to innovate, allow you to give more to your customers. We were the first actually to respond to a COVID situation by having bots automated in WhatsApp, and that would be impossible by this. Currently, we are focusing on providing more variety to our customers of selection of travel, focusing more on to building systems, allowing the customer to have a different experience than our competitors. I see. Without the right architecture, you couldn't respond to the market and situations like COVID. Definitely. I'd like to thank you, Qais, for sharing this architecture with us today. Thank you, Mo, for having me. And I would like to thank Sira Technology team who are behind all of that. It's been fascinating listening to you. Great work we see here. And thank you for watching us today.