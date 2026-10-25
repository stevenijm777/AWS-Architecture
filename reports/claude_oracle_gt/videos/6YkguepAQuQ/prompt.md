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
      "name": "UserCompanyDeveloper",
      "type": "UserCompanyDeveloper",
      "rationale": ""
    },
    {
      "service": "CodePipeline",
      "name": "CodePipeline",
      "type": "CodePipeline",
      "rationale": ""
    },
    {
      "service": "CodeCommit",
      "name": "CodeCommit",
      "type": "CodeCommit",
      "rationale": ""
    },
    {
      "service": "CodeBuild",
      "name": "CodeBuild",
      "type": "CodeBuild",
      "rationale": ""
    },
    {
      "service": "CloudFormation",
      "name": "CloudFormation",
      "type": "CloudFormation",
      "rationale": ""
    },
    {
      "service": "ECR",
      "name": "ECR",
      "type": "ECR",
      "rationale": ""
    },
    {
      "service": "VPC",
      "name": "VPC",
      "type": "VPC",
      "rationale": ""
    },
    {
      "service": "ECS",
      "name": "ECS",
      "type": "ECS",
      "rationale": ""
    },
    {
      "service": "IAM",
      "name": "IAM",
      "type": "IAM",
      "rationale": ""
    },
    {
      "service": "ALB",
      "name": "ALB",
      "type": "ALB",
      "rationale": ""
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserCompanyDeveloper",
      "target_label": "CodeCommit",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CodeCommit",
      "target_label": "UserCompanyDeveloper",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CodeCommit",
      "target_label": "CodeBuild",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CodeBuild",
      "target_label": "ECR",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CodeBuild",
      "target_label": "CodeCommit",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudFormation",
      "target_label": "ECR",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudFormation",
      "target_label": "VPC",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ECR",
      "target_label": "CodeBuild",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ECR",
      "target_label": "CloudFormation",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "VPC",
      "target_label": "CloudFormation",
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
https://www.youtube.com/watch?v=6YkguepAQuQ

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I'm Kurt and today we're in New York City and I'm joined by Chinead from Etion. Welcome to the show, Chinead. Thank you, great to be here. Why don't you tell us about your business? Etion is a healthcare analytics company and we leverage the field of epidemiology to provide real-world evidence-based outcomes. Thank you for that. And you told me that you guys found a very interesting way of deploying not just your applications but also the infrastructure that comes with it and you brought your architecture for us. What does this architecture solve for you? It actually solves quite a few problems. If we were to compare this to our legacy architecture, we were using different tools, we were in the cloud, but it was a bit of a mess and we wanted to streamline the entire process from when a developer commits code to where it ends up in production. So when you arrive at this VPC here with the actual production deployed product, right? That is correct. So how do you go about it? Sure. So we begin by a developer committing code to an AWS repository called CodeCommit. So this is your developer right here and he will commit any kind of change into the CodeCommit repository. Now what we do at this point is we allow the pipeline to do its magic and it simply moves that commit into the next stage, that stage being CodeBuild. Now CodeBuild is another AWS service. It allows us to spin up a container, only pay for the duration where that build takes place, and we can immediately move on to the next stage. And CodeBuild is also controlled by the developer. So if the developer wanted to modify how that build took place or add or do anything, he or she could do so by simply modifying the repository. Anyways, at the end of a successful build, CodeBuild will immediately output a container down to Amazon's ECR registry. At this point in time, we have an application container sitting as an image inside the registry ready to be deployed. So now you have built the entire application. It's sitting there in the registry ready for you to deploy. That's correct. Okay. How does the deployment work? Right. So this is where things get a little interesting. We actually have a third stage which is known as our deploy stage leveraged through CloudFormation. Okay. We had multiple options over here. We could have used CodeDeploy. We could have used the ECS task definition deployer. We could have used Lambda. But there's a specific reason why we chose CloudFormation. And that wasn't because of us just wanting to deploy an application image into, say, Elastic Container Service. So not just into ECS. That is correct. We actually recognize that our application has underlying components that are required at the time of a deployment or outside of the time of a deployment. And those items being the application load balancer, for example, and the IAM roles and permissions. And those are just some of the components. But so to accommodate for that, we actually have inside these developer repositories CloudFormation templates that define the entire application infrastructure. And so as soon as the build is done and the image is inside the registry, the CloudFormation piece gets kicked off. And that CloudFormation piece actually moves forward to deploy to a VPC, an Elastic Container Service task definition, an IAM role, as well as an application load balancer, which at any point in time on demand can be modified by the developer by simply going back up to the first stage. Great. So, Junaid, very streamlined process. You arrive at the VPC, I would assume, relatively quickly. This goes through the process fast. So you do this for many customers. How do you assure that these environments on the VPC are built consistently on the built to your and your customer standards? Right. So again, that actually goes back to the CloudFormation template. So the first thing that we do is we separate our developer environments from our production and client QA environments. In the case of our production environments, we'll have one CloudFormation template that defines exactly the baseline for how these environments should be created. Right. And that CloudFormation template stays the same. If there's a modification we want to make, you have to make it to that one template, which could potentially impact all customers. However, we recognize the fact that every single customer is deployed to a different VPC. So how do we achieve that? How do you govern that? We govern that by simply creating, number one, parallel execution. So if we have, let's say, 100 customers, we would have parallel stages over here accommodating up to 100 customers at the CloudFormation template level. So we go ahead and deploy to CloudFormation. And CloudFormation will then go to 100 different VPCs and push out the same changes. And if there are unique items such as the name of the VPC and the ECS cluster, that is through a small configuration which each one of them has. Junaid, you have a mechanism now where you can deploy this CloudFormation template many times to instantiate this VPC. But your developers could still make changes, accidental or any other way that could impact the instantiation of the VPC. What's the governing mechanism there? Right. So number one, we use a single CloudFormation template for every single VPC deployment that may take place. But the way we govern that is we will actually break down this CloudFormation stage into a three-step process. The first item over here is going to be something called a change set. So a change set is basically telling us what are the changes that you're going to make as part of this deployment. Right. And at this point in time, we'll have someone else with the proper roles and permissions to approve or reject that change. And once that change has been approved, it will actually go ahead and execute the change set in the next stage, which means go ahead and deploy out the infrastructure and the application. So now you have a mechanism to assure that you always build these component pieces the same way. It's agile because it moves fast through the infrastructure and it builds consistent images for your customers. Junaid, thank you so much for sharing your architectural pattern with us. And thank you for joining us today. And thank you for watching. This is my architecture. This is my architecture.