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
      "service": "User",
      "name": "USER",
      "type": "User",
      "rationale": "End user accessing the Orion portal to request a new environment."
    },
    {
      "service": "Route53",
      "name": "ROUTE 53",
      "type": "Route53",
      "rationale": "Used for DNS resolution of the Orion portal request."
    },
    {
      "service": "ALB",
      "name": "ALB",
      "type": "ALB",
      "rationale": "Application Load Balancer routing incoming traffic to the EKS cluster and pods."
    },
    {
      "service": "EKS",
      "name": "EKS",
      "type": "EKS",
      "rationale": "Amazon Elastic Kubernetes Service orchestrating the containerized workloads."
    },
    {
      "service": "EC2",
      "name": "SPOT",
      "type": "EC2",
      "rationale": "100% Spot instances running the Kubernetes pods and microservice jobs."
    },
    {
      "service": "SNS",
      "name": "SNS",
      "type": "SNS",
      "rationale": "Amazon SNS receiving events when microservice jobs are triggered."
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": "Amazon SQS queue storing state and unfinished jobs to ensure consistency during spot terminations."
    }
  ],
  "visual_connections": [
    {
      "source_label": "USER",
      "target_label": "ROUTE 53",
      "arrow_direction": "forward",
      "description": "User accesses the portal via HTTPS"
    },
    {
      "source_label": "ROUTE 53",
      "target_label": "ALB",
      "arrow_direction": "forward",
      "description": "Resolves DNS to the Application Load Balancer"
    },
    {
      "source_label": "ALB",
      "target_label": "EKS",
      "arrow_direction": "forward",
      "description": "Routes traffic to the EKS cluster"
    },
    {
      "source_label": "ALB",
      "target_label": "SPOT",
      "arrow_direction": "forward",
      "description": "Routes traffic to the application pods running on Spot instances"
    },
    {
      "source_label": "EKS",
      "target_label": "SNS",
      "arrow_direction": "forward",
      "description": "Triggers events to SNS when microservice jobs are created"
    },
    {
      "source_label": "SNS",
      "target_label": "SQS",
      "arrow_direction": "forward",
      "description": "Fans out messages to SQS queue"
    },
    {
      "source_label": "SQS",
      "target_label": "SPOT",
      "arrow_direction": "forward",
      "description": "New jobs watch SQS to resume unfinished tasks from terminated spot instances"
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
https://www.youtube.com/watch?v=1aYoIZvabbk

## FULL TRANSCRIPT:
Hi everyone, welcome to This is my Architecture. I'm Jasmine and I have here with me Nikhil Sharma from OLX Autos. Hi Nikhil, thanks for joining us. Hi Jasmine, thank you, thank you for having me. Tell us about OLX Autos. At OLX Autos we offer a one-stop solution to buy and sell used vehicles from having an online evaluation of your car to have an own inspection. We offer anything and everything. Okay, and do you have global presence? Yes, we do. As of now we are operational in 11 countries including India, Indonesia, South America and Turkey. And what are the challenges of going global? So there have been countless challenges. A few of the challenges we have solved is by building an internal developer platform tool because primarily one of the challenges was to reduce our time to market and accelerate our deployment velocity. Okay, and so if I as a user have to create the platform, what's there under the hood of this architecture? Okay, so as an end user if you want to have an environment, you just go to the Orion portal and you'll just go with the... And then once you have the... We also open up the Orion portal, and then the DNS resolution goes to the Amazon Rout of 53. We are using it for the DNS resolution. And then it resolves the DNS to the Amazon Application Load Balancer. And then the Amazon Load Application Load Balancer is going to send the request to our Kubernetes pods. We are using Amazon EKS as a container orchestrator. And then all of our workload is running on AWS EKS. So when you are creating a request to our new environment, you will mention some details like name of the environment, the business use case of the environment, and the business vertical that you want to create for which this environment is needed. And then this request goes to our application pod that is running on Amazon EKS and underlying it is using spot instances. Okay. And what percent of spot do you use? As of now, we are using 100% spot instances. Wow. That's amazing. So how about the cost optimization that you've achieved with 100%? So the use case that we had is that we are creating the replicas of Olex orders environments. And we had to keep the cost in check because if we're creating too many replicas, we obviously increase in the cost exponentially. So that's why we just finalized that we are going to go with 100% spot for the efficient cost utilization. And we just have to figure out how we can leverage spot to its maximum capacity. Okay. And as you are leveraging spot, you also need to take care of spot termination, right? How do you do that? Yes. Yes. So for that, we are using AWS node termination handler. So whenever Amazon is about to terminate any spot instances, it senses an event which AWS termination handler is listening to and then it drains out that nodes. So all the workload that was running on that spot instances gets shifted to another node. So would not experience any disruption in the business. Got it. So basically the request comes to the ports which are deployed on spot, right? And this is orchestrated by Amazon Elastic Kubernetes Service. Exactly. Okay. And how does Amazon EKS help you? It helps us by offloading the operational overhead and it is helping us by handling the MS load that we are putting on it. We started with the 100 ports and now we are running with 10,000 plus ports. So we are incrementally stress testing Amazon EKS. Wow. And that's quite a journey, right? Starting from 100 ports to 10,000 ports. Yes. So that's amazing. And how about this Amazon SNS and SKS? What is the role of these two? Okay. So when a user is trying to making a request to create an environment, ultimately what it's requesting is I need a bunch of microservices for that business vertical. For example, if you are creating an environment for business vertical X, it may need 70 plus microservices. So this our main application running as a pod, it is going to create the number of jobs, Kubernetes jobs for each microservice. For example, if you're launching three microservices, then it will create a job that will take care of launching microservice one, launching microservice two, launching microservice three. Now, as we are running everything on spot, there is a strong likelihood that before the time this job gets completed, spot instances terminates the underlying node and this job gets disrupted. EKS takes care of replacing this job by another job, but ultimately the process was not able to finish up the task that it was assigned to. So what we are doing is whenever a job gets triggered to create the microservice, it sends an event to Amazon SNS and then Amazon SNS finds out that message to SQS. So the new job that is getting replaced by this one watches out the AWS SQS and notices, okay, there is an unfinished job and that job was supposed to launch microservice one, but it failed to do so due to XYZ reason. So that takes care of launching and finishing the job. Okay, great. So you have different jobs spinning up different microservices. Yes. Right? Every job stores the state through SNS to SQS. Yes. And when the job comes up, the new job comes up, it also checks SQS if there is anything pending to be processed. Exactly. So it watches out SQS so that we are having consistent state of the provisioning and maintenance of environments. Okay. And what's the benefit of this architecture? So with this architecture, we are able to increase our deployment velocity and our global expansion. In December 2021, we are operating in nine markets. Now we are operating in 11 markets, such as well. And it also helped in reducing our time to market, shipping up our features faster to production. Amazing. Thank you so much, Nikhil, for sharing this architecture. It's a pleasure, Jasmine. Thank you. Thank you. And thank you everyone for joining us for This is My Architecture. Thank you.