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
      "service": "EC2",
      "name": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "type": "EC2",
      "rationale": "NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code"
    },
    {
      "service": "EC2",
      "name": "EC2 — WORKLOAD_PEEK: poll jobs from SQS and launch Lambda to execute",
      "type": "EC2",
      "rationale": "WORKLOAD_PEEK: poll jobs from SQS and launch Lambda to execute"
    },
    {
      "service": "EC2",
      "name": "EC2 — WORKLOAD_PEEK: do permission check and decide which Lambda to launch",
      "type": "EC2",
      "rationale": "WORKLOAD_PEEK: do permission check and decide which Lambda to launch"
    },
    {
      "service": "UserCompanyDeveloper",
      "name": "UserCompanyDeveloper",
      "type": "UserCompanyDeveloper",
      "rationale": ""
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": "NOTES: use queues because there is limited rate Lambda could be launch, so ec2_1 puts jobs to queue (instead of launch directly), and let ec2_2 to launch whenever it can"
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": "states, e.g., progress of deployment"
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "NOTES: use v8 isolate (a JavaScript v8 engine construct) to isolate tenants, e.g., disallow global variable shared across invocations\nWORKLOAD_PEEK: execute CI/CD jobs"
    }
  ],
  "visual_connections": [
    {
      "source_label": "UserConsumerWeb",
      "target_label": "EC2 — WORKLOAD_PEEK: do permission check and decide which Lambda to launch",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "target_label": "DynamoDB",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "target_label": "UserCompanyDeveloper",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "target_label": "SQS",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2 — WORKLOAD_PEEK: poll jobs from SQS and launch Lambda to execute",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": "lambda in a different account"
    },
    {
      "source_label": "EC2 — WORKLOAD_PEEK: do permission check and decide which Lambda to launch",
      "target_label": "Lambda",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserCompanyDeveloper",
      "target_label": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SQS",
      "target_label": "EC2 — WORKLOAD_PEEK: poll jobs from SQS and launch Lambda to execute",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "DynamoDB",
      "target_label": "EC2 — NOTES: behind ALB to scale to handle the loads\nWORKLOAD_PEEK: web services for developers to submit code",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Lambda",
      "target_label": "UserConsumerWeb",
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
https://www.youtube.com/watch?v=H2fOkeXxpyw

## FULL TRANSCRIPT:
Welcome to This is My Architecture. I'm Matt from AWS. Today I'm joined by Rohan from Atlassian. Thanks for joining. Hi Matt, thanks for having me. So I'm a big Atlassian fan, you know, Jira, Confluence, a lot of great products. But today we're going to talk about something called Atlassian Forge, right? That's correct. So tell us about Atlassian Forge. Atlassian Forge is Atlassian's next generation platform, enabling customers and developers, third party vendors to develop custom applications and extend our products. Okay, so what does that mean? Like making different Atlassian products work together? It allows them to make products work together, they can build custom add-ons. If they want to show data from another data source, they can show it in Confluence, for example. Oh, so I could take like a Jira ticket, for example, and show it in Confluence? You can take a Jira ticket and show it in Confluence. Okay, cool. Well, let's dig into how that actually works. So I see we have CLI and browser. You know, how does this all begin? So there are basically two parts to the Forge platform. The first part has to do with deployment, because we're deploying customer code. The second part has to do with invocation of that customer code, where we actually execute the code that was deployed. Okay. So I'll take you through the first part. So it starts with the developer writing code in JavaScript or TypeScript, typically. They then deploy that using our CLI to one of our services. So when you say deploying code or deploying an application, does that mean a Lambda function, I'm guessing? Or how does it represent? It will eventually turn out to be a Lambda function. To them, it looks like a normal JavaScript function, which we translate into a Lambda function. Okay, so the customer, in your case, is not writing a Lambda function, they're writing the code, deploying through a web service on EC2? That's correct. This web service is behind ALB, so it can scale to handle the load from various customers. Okay. And, you know, you said scaling. Are you talking like hundreds of customers, thousands of customers? What kind of scale are we talking about? We're talking thousands of customers. Wow, okay. So, scalable sort of application ingestion tier or whatever you want to call it. Exactly. And so what happens next? So, we need to keep track of all the deployments we want to do. To do that, we store the state in DynamoDB. Yeah. This allows us to know the progress of a deployment, whether it's completed, failed, etc. So we can report back to the user as to what happened to that deployment. Great. Yeah, DynamoDB, NoSQL database, great for storing things like state, for example. Exactly. So, now you have multiple EC2s with an SQS queue in the middle. Why do you have this architecture? Well, as you mentioned previously, we have thousands of customers that potentially want to do deployments. And we are typically limited on the control plane on Lambda on how many invocations we can do, how many Lambdas we can create in a certain time interval. Okay. To cater for that, what we do is we queue the deployment request onto SQS. Then on the back end, we have a service that reads the deployment request from SQS. It can then, in its own time, create the Lambda when it's allowed to do that. So, it won't be rate limited. Great. So, to avoid rate limiting for creating new functions in Lambda, you sort of separate it by having a queue in the middle. So, you can pull them off the queue as you go. Exactly. Okay. And I see there's a line here, though. Does that denote like a VPC or an account boundary? What's going on here? The line here is an account boundary. So, for us, trust or security is extremely important. So, the customer code runs its own account. There's nothing else in that account. And the Forge platform runs in a separate account that does not touch the customer Lambda account or the Lambda account does not touch our Forge account. So, the Atlassian Forge platform, like other Atlassian products, I imagine, is a SaaS application, multi-tenant? That's correct. Is this part over here with the Lambda functions also multi-tenant or is it one per customer? How does it work? That is multi-tenanted. So, a Lambda can be shared between multiple customers. Okay. Well, then how do you handle security considerations? That's a very good point. As you know, Lambdas can keep state between invocations. And since we'll have multiple customer, different customer requests going through the Lambda, that's not an ideal state to be in. So, what we do on every request, we spin up a V8 isolate to run the customer's code in that specific isolate. So, you wouldn't want, for example, like a global variable that could be available between two invocations to be shared between customers? Exactly. So, even though the customer might write code that tries to do that, what we do, because we spin up an isolate on every invocation and delete the isolate after the invocation, that global variable disappears again. So, some of our viewers may not be familiar with isolates. Can you tell us a little bit more about that? V8 isolate is a JavaScript V8 engine construct that allows JavaScript to spin up a very small, almost like a virtual machine in which to run JavaScript, with nothing in that virtual machine. So, that virtual machine can almost do nothing, or can't do anything really. And we have to allow it to do very specific things. Okay. And then you can explicitly wipe it out when it terminates or if it's not used or whatever. Exactly. Once the request is finished, we delete the isolate, leaving all traces of all the code, all variables are gone, disappeared. Interesting. I love that multi-level security approach to really make it safe and secure for your customers. Yeah. Okay. So, I understand how you load the application, you've decoupled it with a queue in the middle, you create the Lambda function with the customer code, you store the state in DynamoDB. It all makes sense so far. It's a good secure architecture. What happens next? So, now we've got the Lambda deployed, but Lambda sitting there doing nothing is not much use. Yeah. So, we have the browser that now needs to invoke the Lambda. What happens in that case is the browser makes a call to one of our internal services that does various things. It checks security permissions, is the user behind the browser allowed to execute that Lambda. It finds the right Lambda associated with that user, with that product. Once it's found that information, it goes ahead and invokes the Lambda. So, in addition to authentication, there's a bunch of logic that happens at this level, and then it picks up the Lambda that's associated with that request and returns the data to the user? Exactly. Because no data stored in the Lambda, the service actually sends the correct parameters to the Lambda, so the Lambda knows what to do. Got it. So, once the Lambda is executed, we can get information from other systems, from other products, from whatever it feels like. It will return that data, and a page fragment will be constructed, which is returned to the browser, and the browser will then render that page fragment. Okay. Well, I really like how you approach security, really making it sort of a secure, safe offering for your customers with the account boundaries, with the isolates, you know, having all sorts of techniques. You scale by adding things like SQS and, you know, scalable tiers behind ALB. It's really an elegant architecture. Thank you very much. As you mentioned, security is of primary concern for us. That's where we have these multiple layers of security. So, in case something goes wrong, an attack will have to go through various layers to even affect anything else. Great. Well, like we always say, security is job zero. Exactly. So, thanks for sharing this with us. Thank you very much. And thank you for watching. This is my architecture. Thank you.