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
      "service": "UserConsumerWebMobile",
      "name": "UserConsumerWebMobile",
      "type": "UserConsumerWebMobile",
      "rationale": ""
    },
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
      "name": "Lambda — WORKLOAD_PEEK: validate rendering requests",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: validate rendering requests"
    },
    {
      "service": "Lambda",
      "name": "Lambda — WORKLOAD_PEEK: react to spot instance termination events: notify to-be-stopped EC2 spot instances to stop taking requests and drain jobs",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: react to spot instance termination events: notify to-be-stopped EC2 spot instances to stop taking requests and drain jobs"
    },
    {
      "service": "Lambda",
      "name": "Lambda — WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics"
    },
    {
      "service": "SQS",
      "name": "SQS #1",
      "type": "SQS",
      "rationale": ""
    },
    {
      "service": "SQS",
      "name": "SQS #2",
      "type": "SQS",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": "SPOT: True\nWORKLOAD_PEEK: video rendering"
    },
    {
      "service": "StepFunctions",
      "name": "StepFunctions",
      "type": "StepFunctions",
      "rationale": "WORKLOAD_PEEK: handle EC2 autoscaling group to scale up/down"
    },
    {
      "service": "CloudWatch",
      "name": "CloudWatch",
      "type": "CloudWatch",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "vidoes"
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserConsumerWebMobile",
      "target_label": "ApiGateway",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserConsumerWebMobile",
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
      "target_label": "UserConsumerWebMobile",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ApiGateway",
      "target_label": "Lambda — WORKLOAD_PEEK: validate rendering requests",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: validate rendering requests",
      "target_label": "SQS #1",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: validate rendering requests",
      "target_label": "UserConsumerWebMobile",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: react to spot instance termination events: notify to-be-stopped EC2 spot instances to stop taking requests and drain jobs",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics",
      "target_label": "CloudWatch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda — WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SQS #1",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SQS #2",
      "target_label": "Lambda — WORKLOAD_PEEK: validate rendering requests",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "S3",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "SQS #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "StepFunctions",
      "target_label": "Lambda — WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudWatch",
      "target_label": "Lambda — WORKLOAD_PEEK: react to spot instance termination events: notify to-be-stopped EC2 spot instances to stop taking requests and drain jobs",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudWatch",
      "target_label": "Lambda — WORKLOAD_PEEK: scale up/down EC2 autoscaling group based on CloudWatch metrics",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3",
      "target_label": "CloudFront",
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
https://www.youtube.com/watch?v=6CgqEzyWpeA

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I'm Orit. With me today, Shai from Sunday Sky. Hi Shai, tell us about Sunday Sky. Thanks for having me, Orit. So, Sunday Sky has been around since 2007. Our customers engage with their customers using video powered experiences in which the content of the video is personalized to the viewer. What are you going to talk about today? Today I'm going to talk about our rendering ecosystem, our rendering as a service, what we call RAS. So, I imagine you get a telco bill every month. Yes, I do. And imagine that instead of getting a PDF with static data, you'll get a personalized video for Orit. So, let's say you're watching, you get a link to watch your monthly bill from your mobile device. That request arrives into our RAS ecosystem. First stop is the API Gateway, where we make use of the different capabilities of API gateway, which is a front link and we can configure usage plans and API keys for our customers to control the load on our farm. That request arrives into a Lambda function, which is our service, RAS service frontend. That Lambda function does some validations on the rendering request and eventually, pushes rendering instruction to an SQS queue where we have engine service that are part of the RAS ecosystem pulling in for rendering jobs when they have capacity to do so. Once a request arrives into the auto scaling group, then we want to have a quick response as possible from the rendering engine. So, we immediately respond to an SQS queue, which the same Lambda function invocation pulls from. And from that, a moment on, we have a link to a playlist file. That playlist file contains links to video segments that the rendering engine uploads to S3. So, when the player on the mobile device or PC device asks for this video segment to show, then the link to CloudFront actually pulls from the origin a video segment and plays it to the user. So, your video rendering is basically based on, entirely on sport instances. How do you manage high availability? So, there's two aspects to maintain this high availability of our service. First one, we're creating instances across multiple availability zones. Second thing is we try to diversify the instance types inside the auto scaling group as much as possible. So, the combination of both spreading instances across multiple availability zones and have diversified instance types provides us with high availability even when using spot instances. How do you handle the two-minute spot interruption notice while rendering video jobs? So, that's a great question. Well, we built a mechanism for spot instance interruptions where CloudWatch notifies a Lambda function via a CloudWatch event that a certain instance ID is about to be taken. That Lambda function interacts with that instance via an API call telling that instance specifically to stop pulling requests or rendering requests from the queue and kind of drain out the current jobs that it already renders. So, because our engine service is highly efficient, we have high certainty that the rendering job would finish before the two minutes timeout will exceed. So, once the API for instance to stop taking jobs from the queue is finished, we detach the instance from the auto scaling group. Makes sense. What is the scale it currently rendering as a service support? So, we generate billions of videos yearly, millions of videos daily, in order to have highly available services. We have a scaling mechanism that we built that is reliant on CloudWatch metrics that are pushed from the rendering instances and consumed by Lambda function that is triggered by a step function every 15 seconds. So, when we calculate that we don't have or we expect higher traffic coming in, the Lambda function interacts with the auto scaling group telling it to increase the amount of instances that is currently in service. Great. It looks like you build a highly available, cost efficient and scalable service. What are the next steps for you? So, we want to make use of a recent feature announced by AWS ASG where we can map specific instance types for specific weights. That way, our scaling mechanism can interact with the auto scaling group using weights, which is more suitable for representing rendering capacity that is currently required under the load of the farm. Thank you for sharing that with us. And thank you for watching. This is my architecture. Thank you for watching. See you next time. Bye. Bye. Bye. Bye. Bye. Bye. Bye. Bye.