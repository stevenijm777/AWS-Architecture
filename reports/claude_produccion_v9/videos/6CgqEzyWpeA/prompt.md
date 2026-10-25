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
This is your inventory of what is on the whiteboard: `entities` are the drawn components and `visual_connections` are the drawn arrows. Both lists are AUTHORITATIVE.
{
  "entities": [
    {
      "service": "UserConsumerWebMobile",
      "name": "Client Devices",
      "type": "UserConsumerWebMobile",
      "rationale": "Client mobile and web devices requesting and streaming the personalized videos."
    },
    {
      "service": "CloudFront",
      "name": "CloudFront",
      "type": "CloudFront",
      "rationale": "CloudFront CDN used to deliver personalized video segments efficiently to the client devices."
    },
    {
      "service": "ApiGateway",
      "name": "API Gateway",
      "type": "ApiGateway",
      "rationale": "API Gateway serving as the frontend entry point managing usage plans and API keys to control load."
    },
    {
      "service": "Lambda",
      "name": "RAS Frontend Lambda",
      "type": "Lambda",
      "rationale": "Lambda function serving as the RAS frontend to validate rendering requests and manage SQS workflows."
    },
    {
      "service": "SQS",
      "name": "SQS Jobs Queue",
      "type": "SQS",
      "rationale": "SQS queue storing rendering tasks and instructions for the rendering engine."
    },
    {
      "service": "SQS",
      "name": "SQS Responses Queue",
      "type": "SQS",
      "rationale": "SQS queue holding status responses and playlist links that the frontend pulls from."
    },
    {
      "service": "EC2",
      "name": "Rendering EC2 Instances",
      "type": "EC2",
      "rationale": "EC2 Spot instances used to render video segments under the Auto Scaling group. Visually grouped inside the EC2 Auto Scaling box."
    },
    {
      "service": "AutoScaling",
      "name": "Auto Scaling Group",
      "type": "AutoScaling",
      "rationale": "Auto Scaling group managing the pool of rendering spot instances. Visually grouped inside the EC2 Auto Scaling box."
    },
    {
      "service": "S3",
      "name": "S3 Bucket",
      "type": "S3",
      "rationale": "S3 bucket storing the rendered personalized video segments."
    },
    {
      "service": "StepFunctions",
      "name": "Step Functions",
      "type": "StepFunctions",
      "rationale": "Step Functions used to trigger the custom scaling Lambda function every 15 seconds."
    },
    {
      "service": "Lambda",
      "name": "Scaling Lambda",
      "type": "Lambda",
      "rationale": "Lambda function evaluating capacity based on CloudWatch metrics and instructing the Auto Scaling group to scale."
    },
    {
      "service": "CloudWatch",
      "name": "CloudWatch",
      "type": "CloudWatch",
      "rationale": "CloudWatch collecting performance metrics and dispatching spot instance interruption events."
    },
    {
      "service": "Lambda",
      "name": "Interruption Handler Lambda",
      "type": "Lambda",
      "rationale": "Lambda function reacting to Spot Interruption Events to safely drain and detach instances from the Auto Scaling Group."
    }
  ],
  "visual_connections": [
    {
      "source_label": "Client Devices",
      "target_label": "API Gateway",
      "arrow_direction": "right",
      "description": "Users request monthly video bill through API Gateway."
    },
    {
      "source_label": "API Gateway",
      "target_label": "RAS Frontend Lambda",
      "arrow_direction": "right",
      "description": "API Gateway routes requests to frontend validation Lambda."
    },
    {
      "source_label": "RAS Frontend Lambda",
      "target_label": "SQS Jobs Queue",
      "arrow_direction": "up_right",
      "description": "Lambda pushes rendering instructions to SQS queue."
    },
    {
      "source_label": "SQS Jobs Queue",
      "target_label": "Rendering EC2 Instances",
      "arrow_direction": "right",
      "description": "EC2 spot instances pull jobs from SQS when they have capacity."
    },
    {
      "source_label": "Rendering EC2 Instances",
      "target_label": "SQS Responses Queue",
      "arrow_direction": "left",
      "description": "Engine immediately responds back to the response SQS queue."
    },
    {
      "source_label": "SQS Responses Queue",
      "target_label": "RAS Frontend Lambda",
      "arrow_direction": "left",
      "description": "Frontend Lambda polls SQS for the playlist information."
    },
    {
      "source_label": "RAS Frontend Lambda",
      "target_label": "Client Devices",
      "arrow_direction": "left",
      "description": "Provides the playlist file link back to the player on the client device."
    },
    {
      "source_label": "Rendering EC2 Instances",
      "target_label": "S3 Bucket",
      "arrow_direction": "up_right",
      "description": "EC2 rendering engine uploads finished video segments to S3."
    },
    {
      "source_label": "Client Devices",
      "target_label": "CloudFront",
      "arrow_direction": "up_left",
      "description": "Client device requests video playback through CloudFront."
    },
    {
      "source_label": "CloudFront",
      "target_label": "S3 Bucket",
      "arrow_direction": "right",
      "description": "CloudFront pulls video segments from the S3 origin."
    },
    {
      "source_label": "CloudWatch",
      "target_label": "Interruption Handler Lambda",
      "arrow_direction": "up",
      "description": "CloudWatch Events triggers Lambda on spot interruption notice."
    },
    {
      "source_label": "Interruption Handler Lambda",
      "target_label": "Rendering EC2 Instances",
      "arrow_direction": "left",
      "description": "Lambda calls API on EC2 to stop pulling new jobs and drain current ones."
    },
    {
      "source_label": "Interruption Handler Lambda",
      "target_label": "Auto Scaling Group",
      "arrow_direction": "right",
      "description": "Lambda detaches the interrupted instance from the ASG."
    },
    {
      "source_label": "Step Functions",
      "target_label": "Scaling Lambda",
      "arrow_direction": "up",
      "description": "Step Functions trigger the custom scaling calculation every 15 seconds."
    },
    {
      "source_label": "Scaling Lambda",
      "target_label": "Auto Scaling Group",
      "arrow_direction": "right",
      "description": "Scaling Lambda instructs ASG to scale up or down based on metrics."
    },
    {
      "source_label": "Rendering EC2 Instances",
      "target_label": "CloudWatch",
      "arrow_direction": "down_right",
      "description": "Rendering instances publish custom performance metrics to CloudWatch."
    }
  ]
}
## CONNECTION LEDGER (CRITICAL - APPLY BEFORE ANY OTHER EDGE RULE):
Every entry of `visual_connections` is one arrow that was observed. Transcribe it; do not re-derive it from the audio.
1. **One edge per entry:** Emit exactly one edge for each `visual_connections` entry, with the same source and the same target, even when its description is empty.
2. **Both directions are two arrows:** If the list contains A -> B and also B -> A, emit BOTH edges. Never keep only the direction that the audio happens to describe.
3. **Repeated pairs are distinct steps:** If the same source -> target pair is listed N times, emit N edges (they are different steps or flows) and give each its own `flow_id` / `seq`. Never deduplicate.
4. **Fusion keeps arrows:** If Node Rule 4 fuses several entities into one node, re-attach every one of their connections to the fused node. Fusing nodes never removes edges.
5. **Audio assigns, it does not delete:** Use the transcript to decide the `flow_id`, `seq`, `type` and `notes` of each ledger edge. A connection the audio does not mention is still emitted (use type "data" and an empty note when nothing is known).
6. **Ledger edges are exempt from pruning and re-routing:** No rule below may remove a ledger edge, remove one of its endpoints, or redirect it through another node.
7. **Self-check:** In `step_by_step_reasoning`, state the number of `visual_connections` entries and the number of edges you emit. The second number must not be smaller than the first.
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
- **Ledger First, Then Verbal Grounding:** The connection ledger is the primary evidence for edges. An edge that is NOT in the ledger may be added only when the transcript explicitly states that flow (e.g., "sends to", "triggers", "stores in").
- **Completeness:** Ensure that every active service node identified is connected to the graph if a logical flow is described in the audio, avoiding orphan nodes while preventing unmentioned canonical edge hallucinations.

## STRICT EDGE ROUTING & DIRECTIONALITY:
- **Direction Comes From the Ledger:** Keep the direction of every `visual_connections` entry. Do not drop a reverse edge that is in the ledger, and do not add a reverse edge that is neither in the ledger nor explicitly stated.
- **Exact Edge Type Mapping:** Accurately differentiate `data` (direct payloads), `control` (triggers, orchestration, events), and `meta` (monitoring, feedback).
- **No Intermediate Shortcuts:** Preserve exact path routing. Do not bypass intermediate nodes.


## VIDEO URL:
https://www.youtube.com/watch?v=6CgqEzyWpeA

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I'm Orit. With me today, Shai from Sunday Sky. Hi Shai, tell us about Sunday Sky. Thanks for having me, Orit. So, Sunday Sky has been around since 2007. Our customers engage with their customers using video powered experiences in which the content of the video is personalized to the viewer. What are you going to talk about today? Today I'm going to talk about our rendering ecosystem, our rendering as a service, what we call RAS. So, I imagine you get a telco bill every month. Yes, I do. And imagine that instead of getting a PDF with static data, you'll get a personalized video for Orit. So, let's say you're watching, you get a link to watch your monthly bill from your mobile device. That request arrives into our RAS ecosystem. First stop is the API Gateway, where we make use of the different capabilities of API gateway, which is a front link and we can configure usage plans and API keys for our customers to control the load on our farm. That request arrives into a Lambda function, which is our service, RAS service frontend. That Lambda function does some validations on the rendering request and eventually, pushes rendering instruction to an SQS queue where we have engine service that are part of the RAS ecosystem pulling in for rendering jobs when they have capacity to do so. Once a request arrives into the auto scaling group, then we want to have a quick response as possible from the rendering engine. So, we immediately respond to an SQS queue, which the same Lambda function invocation pulls from. And from that, a moment on, we have a link to a playlist file. That playlist file contains links to video segments that the rendering engine uploads to S3. So, when the player on the mobile device or PC device asks for this video segment to show, then the link to CloudFront actually pulls from the origin a video segment and plays it to the user. So, your video rendering is basically based on, entirely on sport instances. How do you manage high availability? So, there's two aspects to maintain this high availability of our service. First one, we're creating instances across multiple availability zones. Second thing is we try to diversify the instance types inside the auto scaling group as much as possible. So, the combination of both spreading instances across multiple availability zones and have diversified instance types provides us with high availability even when using spot instances. How do you handle the two-minute spot interruption notice while rendering video jobs? So, that's a great question. Well, we built a mechanism for spot instance interruptions where CloudWatch notifies a Lambda function via a CloudWatch event that a certain instance ID is about to be taken. That Lambda function interacts with that instance via an API call telling that instance specifically to stop pulling requests or rendering requests from the queue and kind of drain out the current jobs that it already renders. So, because our engine service is highly efficient, we have high certainty that the rendering job would finish before the two minutes timeout will exceed. So, once the API for instance to stop taking jobs from the queue is finished, we detach the instance from the auto scaling group. Makes sense. What is the scale it currently rendering as a service support? So, we generate billions of videos yearly, millions of videos daily, in order to have highly available services. We have a scaling mechanism that we built that is reliant on CloudWatch metrics that are pushed from the rendering instances and consumed by Lambda function that is triggered by a step function every 15 seconds. So, when we calculate that we don't have or we expect higher traffic coming in, the Lambda function interacts with the auto scaling group telling it to increase the amount of instances that is currently in service. Great. It looks like you build a highly available, cost efficient and scalable service. What are the next steps for you? So, we want to make use of a recent feature announced by AWS ASG where we can map specific instance types for specific weights. That way, our scaling mechanism can interact with the auto scaling group using weights, which is more suitable for representing rendering capacity that is currently required under the load of the farm. Thank you for sharing that with us. And thank you for watching. This is my architecture. Thank you for watching. See you next time. Bye. Bye. Bye. Bye. Bye. Bye. Bye. Bye.