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
      "service": "ECS",
      "name": "ECS",
      "type": "ECS",
      "rationale": ""
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "WORKLOAD_PEEK: validate data stored in DynamoDB according to compliance requirements"
    },
    {
      "service": "RDS",
      "name": "RDS",
      "type": "RDS",
      "rationale": "compliance standards"
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": "build events (eg. code scan)"
    },
    {
      "service": "SNS",
      "name": "SNS",
      "type": "SNS",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Non Production Environment",
      "type": "ThirdParty",
      "rationale": "Non Production Environment"
    },
    {
      "service": "ThirdParty",
      "name": "Production Environment",
      "type": "ThirdParty",
      "rationale": "Production Environment"
    }
  ],
  "visual_connections": [
    {
      "source_label": "ECS",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "ECS",
      "target_label": "Non Production Environment",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "DynamoDB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "ECS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "DynamoDB",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Non Production Environment",
      "target_label": "ECS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Non Production Environment",
      "target_label": "Production Environment",
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
https://www.youtube.com/watch?v=7V8wTCkjOqo

## FULL TRANSCRIPT:
Welcome to This is My Architecture. My name is Gerardo and we're live from AW Summit in Sydney. And I'm joined today by Chris from National Australia Bank. Welcome Chris. Yeah, thanks for having me. Really excited. So can you tell us a little bit about National Australian Bank? Well, National Australia Bank is one of the largest banks in Australia and their technology strategy is quite open about moving to cloud first and we're moving thousands of workloads to AWS. That's brilliant. So I know that you've been moving a lot of workloads recently. So what are you telling us about today? Well, to do that we need a consistent compliance framework to be able to do that. And my team, which is a combined NAB team with AWS Professional Services, are building out the deputy platform to facilitate that quick move to cloud. So before you deploy the system, what challenges did you have? Well, everyone had to sort of adhere to the standards on their own and attest to them. And people did that in a bunch of different ways. And we wanted to automate that because you're not going to move a thousand workloads at the pace that we need to with different processes. So it was pretty manual, prone to error and also a lot of time wasted. Just a lot of work. Just a lot of work when we can, you know, we can focus on building great things. All right. So tell me, can you walk me through the architecture? Yeah. So we have our service teams in NAB. So they're my customers. And what actually happens is we've got in their non-production account, they're running their pipelines. Yeah. And they're sending all the events to Kong running on ECS. And we use Kong to publish our endpoints. Yeah. Which then goes over to Lambda. And Lambda then captures those events and installs them in DynamoDB. So we're capturing all the build events from a team's pipeline. And we're storing that within our DynamoDB. Brilliant. So once the events are stored in Dynamo, what happens next? So what happens next? So when a team's ready to promote, they'll make an API call to promote. And again, it'll go through the same flow. It'll hit Lambda. It'll say, you need to promote. And in RDS, what we do have, we have defined our compliance framework. It means what's the standard, what's the control, and how do we meet it? Yeah. And so when we say promote, we use the data that's been stored within DynamoDB, which is all their build events. And we match it up with the standards and controls that we want to see as part of you deploying it to your production account. Brilliant. So the validation framework is here. And this is the events. And then you use some Lambdas to validate that what they actually built is compliant. Yeah, we use Lambda to execute the assessment. Brilliant. So I'm guessing that the result of this engine is either success or failure. Yeah, it's a success or failure, black and white. What happens if it succeeds? So when it succeeds, again, from your non-production account, they'll call an API. So Deputy is basically an API solution. Yeah. And they'll make a promote call. And at that time they promote, compliance is okay. They'll make a deployment call. All right. So they'll send a notification out to the production account. Yeah. So when we do the promotion, we use SNS because some of our products within Deputy, we've got a distributed system, again, Lambda running within PROD. Yeah. And we trigger that promotion. So we copy the artifacts from here to here. Mm-hmm. Right. And then when we do the deployment, we send an SQS notification message, which triggers their deployment tools. Perfect. So why have you chosen to use technologies like Lambda and SNS? Well, we had to get something out to market very quickly. We needed to move workloads quickly. Yeah. We wanted our team to focus on building the business logic and the outcome. Yeah. So we didn't want them to manage infrastructure. Yeah. We didn't want them to manage, have operational overheads. And Lambda fitted that bill straight away. Yeah. And in terms of SNS, because we are deploying components into other people's accounts. Yeah. We don't have access to those accounts and their production accounts. Yeah. So we wanted a nice way to be able to securely send that information. Mm-hmm. And also an ability to fan out because we are talking about 80 to 100 NAB service teams that are going to jump onto this platform. Brilliant. And why two different types of databases? Well, it's really about picking out fit for purpose. Yeah. Yeah. So services, right? So with DynamoDB, it is capturing build events. Mm-hmm. I've started my build. Here's some evidence with it. I've executed a code scan. Here's my evidence. So yeah, key value pair. Dynamo is perfect for that. Go back to our key principles. Low operational overhead. Don't want to manage the infrastructure. This is perfect. It's performance. This is perfect. In terms of RDS and Postgres, well, with those compliance frameworks are relational in nature. Yeah. Standard, control, how do you test it? Yeah. And because we are going to have 80 to 100 service teams, we're going to have many pipelines sending information. So we also need to understand who the team is, what services they run. And this helps you achieve that at scale, I guess. That's right. And that's why it's relational. This is good. Look, I love how you've implemented this system that is giving your developers freedom to build, while also giving them the guard rail so that you can maintain your security standards and build trust with the regulator. This is an amazing architecture. Thank you. Thank you for sharing with us. All right. Thanks for having me. And thank you for watching. This is my architecture. Thanks for having me. And for having me. I can see.