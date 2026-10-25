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
      "service": "Kinesis",
      "name": "Kinesis (1)",
      "type": "Kinesis",
      "rationale": "Primer ícono de Kinesis con flecha entrante desde el exterior."
    },
    {
      "service": "Lambda",
      "name": "Lambda (1)",
      "type": "Lambda",
      "rationale": "Primera función Lambda que recibe de Kinesis (1) y RDS(1), y conecta hacia SQS."
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": "Cola SQS que recibe de Lambda (1) y conecta hacia Lambda (2)."
    },
    {
      "service": "Lambda",
      "name": "Lambda (2)",
      "type": "Lambda",
      "rationale": "Segunda función Lambda que conecta hacia RDS(2) y Kinesis(2)."
    },
    {
      "service": "Kinesis",
      "name": "Kinesis(2)",
      "type": "Kinesis",
      "rationale": "Segundo ícono de Kinesis receptor desde Lambda (2)."
    },
    {
      "service": "RDS",
      "name": "RDS(1)",
      "type": "RDS",
      "rationale": "Primer ícono de RDS con flecha entrante desde el exterior que conecta a Lambda (1)."
    },
    {
      "service": "RDS",
      "name": "RDS(2)",
      "type": "RDS",
      "rationale": "Segundo ícono de RDS receptor desde Lambda (2)."
    }
  ],
  "visual_connections": [
    {
      "source_label": "Kinesis (1)",
      "target_label": "Lambda (1)",
      "arrow_direction": "right",
      "description": "Flecha desde Kinesis (1) hacia Lambda (1)."
    },
    {
      "source_label": "Lambda (1)",
      "target_label": "SQS",
      "arrow_direction": "right",
      "description": "Flecha desde Lambda (1) hacia SQS."
    },
    {
      "source_label": "SQS",
      "target_label": "Lambda (2)",
      "arrow_direction": "right",
      "description": "Flecha desde SQS hacia Lambda (2)."
    },
    {
      "source_label": "Lambda (2)",
      "target_label": "RDS(2)",
      "arrow_direction": "right",
      "description": "Flecha desde Lambda (2) hacia RDS(2)."
    },
    {
      "source_label": "Lambda (2)",
      "target_label": "Kinesis(2)",
      "arrow_direction": "right",
      "description": "Flecha desde Lambda (2) hacia Kinesis(2)."
    },
    {
      "source_label": "RDS(1)",
      "target_label": "Lambda (1)",
      "arrow_direction": "up",
      "description": "Flecha desde RDS(1) hacia Lambda (1)."
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
https://www.youtube.com/watch?v=jV8DwutbXbg

## FULL TRANSCRIPT:
Hi, I'm Toby from AWS. Welcome to This Is My Architecture. I'm joined today by Damian from Tandem. Hi, Damian. Hi, good to be here. Good, welcome. Thanks. Tell me a bit about Tandem. So everyone wants to be better at managing their money and Tandem thinks that your bank should be doing more for you. They have all your transaction data. They know what you spend your money on. They could be providing you with more insights on how you need to get to the end of the month, how much you can save, that kind of thing. Sure. Okay. So I know you're a data scientist and I see we've got Kinesis here. It looks like a data pipeline. Do you want to talk me through what we've got here? Yeah. So to start with, Tandem not only provides your standard banking services, we also connect to pretty much all other banks in the UK to consume all of the transaction data that you might have. So coming in before this, there's another service which will do the account aggregation that goes and scrapes the websites for your bank. And when that's done, there'll be an event here published on the Kinesis stream to say this user's account has been updated. Okay. So that might be a collection of say monthly statements from a particular third party bank that that user's using and you bring it into Kinesis. Yeah. And that could be, we trigger that by a schedule or when the user logs in and refreshes their app. Okay. So that's typically going to be like a CSV file maybe, you know, date, description, amount, something like that and a list of those. That's what comes back from the bank. Yeah. That goes into RDS by the other service. Okay. What we get here on the Kinesis stream is an account ID and we're listening for this event to happen to know that we need to go and do something for that user. Okay. This Lambda function here, we've purposely made it very lean and very fast. All it's basically doing is taking in transactions which are in the RDS database. So that's going to do a SQL query to RDS to say, give me the transactions for user ABC. Exactly. Okay. And then it's gathering those up into batches of say a hundred and then publishing a new message to SQS, which is all the strings that are the transaction descriptions. Okay. So we've still got effectively the raw data that's come from those third party banks. So it's going to hit the SQS queue. And I see we've got Lambda here. Is this where you're doing some sort of processing to understand those strings? Yeah. So originally this Lambda that does all the work was connected directly to Kinesis. But to do the processing that it needs to do takes a few seconds and we've got tens of millions of transactions coming in here. So there's only one Lambda that you can have connected to a Kinesis shard at a time and they work sequentially. So it meant we could never keep up with the data that was incoming. Okay. So using SQS and Lambda with a second tier of Lambda, you've got a fan out system here with you? Yeah, exactly. So there's lots of these. It can scale out to pretty much anything. Okay. And this is the part which does the NLP, the natural language processing. What are you using for that? What sort of code base or what libraries? It's a tool called Antler. It does parser generation. So we write a domain specific grammar file. That gets compiled into Python code. We bundle that up in a Lambda function. And there's blue logic to connect all the other bits. Okay. So the types of dictionary listings you've got in there would be things like, you know, merchant name, currencies, those sorts of things, dates, obviously. Yeah. We want to extract exchange rates, merchant location. Yeah. Okay. And once you've done that, then you're writing that, if you like, that cleansed data or that enriched data, you're writing that to a lot of data. So you're writing that to RDS, are you? Yes. We have a table here which has all the columns for all those fields. We're storing those process transactions along with a version of the model that's run so we can analyze it later, compare it back later. So nice forward thinking there. So every transaction you write, you write the version of the model which was used to process that? Yeah. Okay. That allows us to iterate on our model development as new features get noticed. And I guess updating the NLP model here is a big part of your focus, isn't it? So how do you manage those updates to the model? Yeah. We've built our own tool which bundles up the Lambda plus all the Python dependencies, the C extensions, and some shared object stuff. That's actually being published as an open source tool. So that gets deployed through Jenkins and CloudFormation. Okay. Good. All right. And then I guess I can see we've also got Kinesis here. Is this where you're going to publish the results or is that a, what is that? Is that an event stream or? Yeah. So when we've got to this point, the data science part is done. We, we are saying that the customer transactions have been finished. And it's up to another part within the organization to trigger from that event. So it might be picking up those and refreshing the app with the friendly descriptions. Okay. Those transactions. And, you know, I, I, I, I personally, I'd like to say that, you know, the, the value you're giving your end users here is, is pretty considerable. As someone who spent hours with an Excel file going through household expense items, you know, I can see that this would be really valuable. So I'm tempted to give it a try. Yeah. And this is just the first, well, one of the first steps towards building more models on the top of it. Once we actually extract these features, we've got an enriched data set. Great. Well, thanks Damien for sharing today. Thank you. And thanks for watching. This is my architecture.