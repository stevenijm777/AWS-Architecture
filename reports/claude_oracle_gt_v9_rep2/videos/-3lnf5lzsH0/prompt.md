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
      "service": "OnPremDC",
      "name": "OnPremDC",
      "type": "OnPremDC",
      "rationale": ""
    },
    {
      "service": "EMR",
      "name": "EMR",
      "type": "EMR",
      "rationale": ""
    },
    {
      "service": "Athena",
      "name": "Athena",
      "type": "Athena",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3 #1",
      "type": "S3",
      "rationale": ""
    },
    {
      "service": "S3",
      "name": "S3 #2",
      "type": "S3",
      "rationale": ""
    },
    {
      "service": "WAF",
      "name": "WAF",
      "type": "WAF",
      "rationale": ""
    },
    {
      "service": "ThirdParty",
      "name": "Apache Metron",
      "type": "ThirdParty",
      "rationale": "Apache Metron"
    },
    {
      "service": "SNS",
      "name": "SNS",
      "type": "SNS",
      "rationale": ""
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": ""
    },
    {
      "service": "CloudTrail",
      "name": "CloudTrail",
      "type": "CloudTrail",
      "rationale": ""
    },
    {
      "service": "GuardDuty",
      "name": "GuardDuty",
      "type": "GuardDuty",
      "rationale": ""
    },
    {
      "service": "EC2",
      "name": "EC2",
      "type": "EC2",
      "rationale": ""
    },
    {
      "service": "UserCompanyAnalyst",
      "name": "UserCompanyAnalyst",
      "type": "UserCompanyAnalyst",
      "rationale": ""
    }
  ],
  "visual_connections": [
    {
      "source_label": "OnPremDC",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EMR",
      "target_label": "S3 #2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Athena",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3 #1",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "S3 #2",
      "target_label": "Athena",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "WAF",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Apache Metron",
      "target_label": "EMR",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "Apache Metron",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SNS",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "SQS",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "CloudTrail",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "GuardDuty",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "Apache Metron",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "EC2",
      "target_label": "WAF",
      "arrow_direction": "",
      "description": "control packet to modify WAF settings"
    },
    {
      "source_label": "EC2",
      "target_label": "UserCompanyAnalyst",
      "arrow_direction": "",
      "description": ""
    },
    {
      "source_label": "UserCompanyAnalyst",
      "target_label": "EC2",
      "arrow_direction": "",
      "description": ""
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
https://www.youtube.com/watch?v=-3lnf5lzsH0

## FULL TRANSCRIPT:
Welcome to another episode of This is My Architecture. My name is Lalit. Today our guest is Vikram Mehta from MakeMyTrip. Vikram, tell us what battles you are fighting. Sure. Thanks Lalit. Pleasure to be here. At MakeMyTrip being India's leading travel aggregator. We see attacks getting more and more advanced. The adversaries are getting smarter and they are getting faster. There is a growing need to complement this by something more than just signature or rule based detection. To possess the ability to detect abnormal behavior and then respond to these attacks in a timely or semi-automated manner. So you built a SOC system grounds up. Yes. Entirely. Could you take us through the architecture, how you have built it, what are the various components and how they work together. Sure. Absolutely. I think what we see here is a typical next-gen SOC consists of practically starting with data ingest. Now the challenge with data ingest is hybrid data sources. So we've got the public cloud and we've got on-premise data sources. We've got the heart of the next-gen SOC there which is Apache Metron. A big thanks to the Hortonworks team for presenting this to the community. Post that we have a security data lake which houses telemetry events over a large period of time. We've got a security orchestration and response platform on the right-hand side which primarily deals with incident response and automation. Okay. Let's dig deeper in this. So you have disparate systems. How do you ingest logs in real time? Sure. So as I was saying, in case of a public cloud, there are various different systems that need to be integrated with in order to, you know, pull in telemetry events. For instance, S3, for instance, SNS, SQS, CloudTrail, GuardDuty. There is a need to integrate with AWS with tools like Apache NIFI that have the possess the capability to build workflows and then pull the telemetry events into Apache Metron. As for the on-prem ecosystem, it's a pretty standard syslog or Kafka integration that can be used to pull in the events directly into Apache Metron. Okay. So you got the logs in Apache Metron. What are the components within Apache Metron that works on this ingested data? Sure. So I think the first piece is to be able to convert the standard telemetry log format into a log format that Apache Metron and downstream systems understand. So we call that, I mean, we call that parsing. Essentially, it converts a syslog log message or a cloud trail or guard duty log message into another JSON format that Apache Metron understands. So it becomes a JSON format, a much more readable format. Now you're doing the parsing and there's also another process that you mentioned is about enrichment and profiling which is important. The contextual intelligence is important around logs. How does you achieve that? Absolutely. So I think enrichment is key to, you know, provide contextual information about an event, right. So let's say there is a blog that contains a source IP address and a destination IP address. Now a source and destination IP address in itself does not mean much, right. It will be important to understand where the source originates from, its geolocation, maybe the AS number. As far as the destination is concerned, in a public cloud environment, IP addresses keep changing, right. It might be important to understand what that server actually is. Is it a flight server? Is it a hotel server? Is it a payment server? This entire contextual intelligence is fed into the Apache Metron system which then tags the incoming telemetry data with this contextual intelligence. So we got real-time events in Apache Metron, we got the visibility. Now we also have security data lake. Yes. How does these two integrate and how critical is to build a security data lake? Sure. I think in any SOC environment, it's key to to store and index telemetry data for a large period of time. That could run into months, it could run into years. At the scale that we operate at, it becomes extremely important to maintain a horizontally scalable environment which can be trusted to house such large amounts of information. We were initially leveraging Apache Metron's backbone which is HDFS to store and index these events. We migrated from the on-prem HDFS setup onto the serverless security data lake as you can see here. So the persistent data in Apache Metron from HDFS is picked up by an EMR job which transforms the persistent data in HDFS into S3. From S3 we build, we leverage Athena to build SQL queries and analytics and you know for various purposes such as log mining, analytics, forensics and so on. So there is an insight from the data which is residing in S3 for a longer period of time. Absolutely. Maybe for months. Years. And then you feed it back to maybe Apache Metron to enrich it further. Absolutely, I think that's a very important aspect here. So the stream processing layer has the capability to create profiles for only a limited period of time, right, as infrastructure would allow. The security data lake gives us the flexibility to generate models or profiles over months long of telemetry information which essentially is a lot more accurate as opposed to let's say a few minutes of profile information. So that's the feedback loop that goes from the security data lake back into Apache Metron. So now at this point of time since you identify an incident, how does your users, your analyst take action or system take action on these events or incidents? Sure. So I think as important as it is to detect an incident, it's important to respond to that incident as soon as possible and in many ways and in as many ways possible in an automated or semi-automated manner. There was a need to build this entire orchestration framework which we call Blitz. It's also available in our open source GitHub repo. It essentially takes an alert from Metron, tags more relevant contextual information that can probably not be fed into Apache Metron like reverse DNS like a who is lookup for instance, presents this entire alert in a single pane of glass to a SOC analyst, you know probably on his mobile handset or via a Jira integration and hence cutting down the investigation time, right or the triage time that a SOC analyst would usually spend. The next step is to respond or mitigate the current threat. There are various different integrations that we have done with let's say a WAF or a firewall or our internal routers that an analyst could actually let's say at the click of a button respond to an incident that he receives by let's say blocking off a source. Okay. All right. So you have also automated incident response. Yes. To an extent we can say. Yeah. Understood the architecture. Could you just take a couple of use case or one use case that you're solving with this? Sure. I think that's probably the most interesting part and my favorite topic too. I think the whole concept of an external SOC is to be able to detect unusual behavior, deviations from normal activity, right. So let's talk about a use case where we are trying to detect server compromise that has actually bypassed all security, you know rule based or signature based environment or protection that one might have. A server has a typical characteristic, let's say a web server would have a certain egress and ingress ratio which is which we call producer consumer ratio and when profiled over a period of time a typical web server would have a certain pattern of normal PCR, normal PCR range. Now, if that server starts doing something that it is not supposed to do, for example, if it gets compromised that might skew the PCR ratio to an extent which is a deviation from normal behavior and which is what can be detected by a setup like this. So you're detecting the unknown? Yes, absolutely. Okay. And then what is the scale of this architecture? How many events you're handling? So I think from like various different data sources, we've probably got around I think 20 data sources operating at the moment, add up at about 5000 events per second. And as far as the security data lake is concerned, we index about 250 million events per day. Okay. All right. And now since you got the data in data lake, what are your next steps? What next you're doing on this platform? So I think as the next step we primarily, you know, feel we like to leverage the security data lake and large scale, large amounts of data available to us to carry out threat hunting, to detect even more than what we are doing today. Thanks Vikram. Thanks for the insight. Pleasure is all mine. Thank you for watching. This is my architecture.