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
      "service": "S3",
      "name": "S3",
      "type": "S3",
      "rationale": "Amazon S3 bucket receiving raw media assets and triggering processing workflows."
    },
    {
      "service": "StepFunctions",
      "name": "STEP FUNCTIONS",
      "type": "StepFunctions",
      "rationale": "AWS Step Functions orchestrating the pipeline with a direct visible arrow pointing to DynamoDB."
    },
    {
      "service": "MediaConvert",
      "name": "ELEMENTAL MEDIACONVERT",
      "type": "MediaConvert",
      "rationale": "AWS Elemental MediaConvert performing video transcoding; no visual arrow connecting it to DynamoDB."
    },
    {
      "service": "Rekognition",
      "name": "REKOGNITION",
      "type": "Rekognition",
      "rationale": "Amazon Rekognition extracting visual entities and features from video."
    },
    {
      "service": "Transcribe",
      "name": "TRANSCRIBE",
      "type": "Transcribe",
      "rationale": "Amazon Transcribe converting audio streams into speech-to-text transcriptions."
    },
    {
      "service": "Comprehend",
      "name": "COMPREHEND",
      "type": "Comprehend",
      "rationale": "Amazon Comprehend performing natural language processing on text transcripts."
    },
    {
      "service": "DynamoDB",
      "name": "DYNAMODB",
      "type": "DynamoDB",
      "rationale": "Amazon DynamoDB storing metadata, receiving arrows from Step Functions, Rekognition, Transcribe, and Comprehend."
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": "Amazon EC2 component inside the Reach Engine box receiving arrow from DynamoDB."
    },
    {
      "service": "EKS",
      "name": "EKS",
      "type": "EKS",
      "rationale": "Amazon EKS cluster component inside the Reach Engine box alongside EC2, without direct internal arrows between EC2 and EKS."
    }
  ],
  "visual_connections": [
    {
      "source_label": "S3",
      "target_label": "STEP FUNCTIONS",
      "arrow_direction": "down",
      "description": "S3 event triggers the execution of the Step Functions orchestration workflow."
    },
    {
      "source_label": "STEP FUNCTIONS",
      "target_label": "ELEMENTAL MEDIACONVERT",
      "arrow_direction": "up_right",
      "description": "Step Functions invokes MediaConvert to initiate video transcoding jobs."
    },
    {
      "source_label": "STEP FUNCTIONS",
      "target_label": "REKOGNITION",
      "arrow_direction": "right",
      "description": "Step Functions triggers Amazon Rekognition for computer vision processing."
    },
    {
      "source_label": "STEP FUNCTIONS",
      "target_label": "TRANSCRIBE",
      "arrow_direction": "down_right",
      "description": "Step Functions triggers Amazon Transcribe for speech-to-text conversion."
    },
    {
      "source_label": "STEP FUNCTIONS",
      "target_label": "DYNAMODB",
      "arrow_direction": "down_right",
      "description": "Step Functions connects directly to DynamoDB via a visible arrow."
    },
    {
      "source_label": "REKOGNITION",
      "target_label": "DYNAMODB",
      "arrow_direction": "right",
      "description": "Rekognition outputs object detection and computer vision metadata to DynamoDB."
    },
    {
      "source_label": "TRANSCRIBE",
      "target_label": "DYNAMODB",
      "arrow_direction": "up_right",
      "description": "Transcribe writes text transcription results directly to DynamoDB."
    },
    {
      "source_label": "TRANSCRIBE",
      "target_label": "COMPREHEND",
      "arrow_direction": "right",
      "description": "Transcribed text is passed to Amazon Comprehend for natural language processing."
    },
    {
      "source_label": "COMPREHEND",
      "target_label": "DYNAMODB",
      "arrow_direction": "up_right",
      "description": "Comprehend stores extracted NLP entities and sentiment analysis in DynamoDB."
    },
    {
      "source_label": "DYNAMODB",
      "target_label": "EC2",
      "arrow_direction": "up",
      "description": "DynamoDB arrow points to the Reach Engine box (containing EC2 and EKS)."
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
https://www.youtube.com/watch?v=07lfvavMdfU

## FULL TRANSCRIPT:
Hello and welcome to This is My Architecture. I'm Joe and I'm joined today with Bailey from Levels Beyond. Thanks for having me. So Bailey, talk to me a little bit about Levels Beyond. What do you guys do actually? So we help our clients monetize their media starting from the camera card, taking it all the way to the screen. Outstanding, outstanding. So you have a lot of AWS services up here. Can you walk us through kind of start to finish as far as how you guys ingest that data? Sure. So this right here is our Media to Cloud workflow and it starts with the user uploading a file to an S3 bucket. That upload triggers a step function. The first thing that the step function does is kick off the transcode and media convert. Okay. What exactly are you doing with media convert there? So media convert is creating us a proxy that's going to be good for playing back in the browser. So that our user is going to be able to have a kind of visual check to go along with all the metadata that we're going to be extracting. Do you have multiple customers leveraging different kinds of video feeds, different formats? Yep. We have basically every format you can imagine is coming into Reach Engine as a platform. Okay. Okay. Yeah. Continue. Sure. So after that proxy is generated, the step function is going to trigger some lambdas. It's going to extract checksums, other kind of standard technical metadata, and it's going to store that over in DynamoDB. Okay. Now is this just metadata about the video itself, just high level metadata? Correct. Yeah. You know, check some of the videos so that you could, you know, validate its authenticity. Sure. It's going to pull out, you know, frame rates, all kinds of media info. Useful for the customer that's going to leverage that. Yep. Okay. Got it. After all that kind of basic metadata is extracted, we're going to trigger another step function, and that's going to start off in Recognition. Recognition is going to take that video. It's going to identify any celebrities, any violence, any nudity, any kind of data that our clients might want to be able to extract from that content. Now is that just tagging that information? How are you handling that? So we're going to take all that data. It's going to be associated with time codes, and that is going to go into DynamoDB. Okay. After that, we're going to trigger Transcribe using that same step function. Transcribe is going to take the audio from that content and translate it into text. After it's translated to text that's going to get driven into Comprehend, where we can run analysis on that text to extract entities, you know, understand things like when profanity is happening. And then all the data that comes out of both of these guys is going to go into DynamoDB. Excellent. Now, do you store DynamoDB data forever, or is that something temporary? So DynamoDB is a temporary data store. So after the data is there, we're going to trigger an ingest into Reach Engine. Talk to me about Reach Engine. So Reach Engine is really the meat of our product. It is going to allow the users to play this, play the content back that they ingested here. It's going to allow them to view all that metadata that was extracted. It's going to allow them to search on all that metadata. It's going to, you know, particularly, with recognition, it's going to make a nice visualization where you can see, you know, tracks for each celebrity and when they appear in the video. Yep. And then with all this metadata, they can pump that into our orchestration engine, which will allow them to take that content from Reach Engine and put it places where it's going to allow them to make money. And that's outside of your Reach Engine platform at that point. Correct. Possibly on the client, it's hybrid, or whoever you guys deploy that. Yep. Outstanding. I love the solution. You know, I do appreciate coming in and talking about your solution. It seems like a very powerful solution. And I thank you for coming in and describing what that is. Thanks for having me. Sure. Thank you for watching. This is my architecture.