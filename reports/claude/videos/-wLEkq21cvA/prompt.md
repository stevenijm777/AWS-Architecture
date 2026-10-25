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
      "service": "OnPremDC",
      "name": "ON-PREM",
      "type": "OnPremDC",
      "rationale": "Ícono gris de pila de servidores rotulado ON-PREM. Se mapea a OnPremDC por ser la entrada del catálogo que nombra exactamente eso; mismo criterio que en -3lnf5lzsH0 y jg85DzUZ9Ac. Conecta hacia App Discovery Service y EC2 (HOT REPLICA)."
    },
    {
      "service": "AppDiscovery",
      "name": "APP DISCOVERY SERVICE",
      "type": "AppDiscovery",
      "rationale": "AWS Application Discovery Service receptor de ON-PREM y EC2 (5)."
    },
    {
      "service": "EC2",
      "name": "EC2 (HOT REPLICA)",
      "type": "EC2",
      "rationale": "Instancia EC2 etiquetada como Hot Replica que posee únicamente 2 entradas (desde ON-PREM y CLOUDENDURE)."
    },
    {
      "service": "UserCompanyDeveloper",
      "name": "MIGRATION TEAM",
      "type": "UserCompanyDeveloper",
      "rationale": "Ícono de usuario (Migration Team) que conecta a Slack y DynamoDB."
    },
    {
      "service": "ThirdParty",
      "name": "SLACK",
      "type": "ThirdParty",
      "rationale": "Plataforma Slack receptora de Migration Team y conectada a EC2 (5)."
    },
    {
      "service": "EC2",
      "name": "EC2 (5)",
      "type": "EC2",
      "rationale": "Instancia EC2 central. Recibe 1 entrada desde SLACK y dibuja 5 salidas: hacia APP DISCOVERY SERVICE, CLOUDENDURE, BAKE AMI, y dos líneas que cruzan la línea vertical entrecortada hacia EC2 (Lado Derecho) y SHARED AMI."
    },
    {
      "service": "ThirdParty",
      "name": "CLOUDENDURE",
      "type": "ThirdParty",
      "rationale": "Servicio de migración (CloudEndure) receptor de EC2 (5) y emisor hacia EC2 (HOT REPLICA)."
    },
    {
      "service": "AMI",
      "name": "BAKE AMI",
      "type": "AMI",
      "rationale": "Ícono de AMI (dos filas de 3 cuadros) nombrado BAKE AMI receptor desde EC2 (5)."
    },
    {
      "service": "DynamoDB",
      "name": "DYNAMODB",
      "type": "DynamoDB",
      "rationale": "Base de datos DynamoDB receptora desde Migration Team."
    },
    {
      "service": "EC2",
      "name": "EC2 (Lado Derecho)",
      "type": "EC2",
      "rationale": "Ícono de EC2 al otro lado de la línea vertical entrecortada. NO está aislado: recibe una línea que sale de EC2 (5), cruza el divisor y baja con punta de flecha sobre él. El anotador dejó constancia de que podría ser la MISMA instancia que EC2 (5) redibujada al otro lado del divisor, pero en la imagen no hay nada que lo confirme: son dos íconos separados y así se transcriben."
    },
    {
      "service": "AMI",
      "name": "SHARED AMI",
      "type": "AMI",
      "rationale": "Ícono dibujado a mano de dos filas de 3 cuadros, igual que BAKE AMI, rotulado SHARED AMI. NO está aislado: recibe una línea desde EC2 (5) que cruza el divisor entrecortado y entra con punta de flecha por su izquierda."
    }
  ],
  "visual_connections": [
    {
      "source_label": "ON-PREM",
      "target_label": "APP DISCOVERY SERVICE",
      "arrow_direction": "down",
      "description": "Flecha desde ON-PREM hacia APP DISCOVERY SERVICE."
    },
    {
      "source_label": "ON-PREM",
      "target_label": "EC2 (HOT REPLICA)",
      "arrow_direction": "right",
      "description": "Flecha desde ON-PREM hacia EC2 (HOT REPLICA)."
    },
    {
      "source_label": "MIGRATION TEAM",
      "target_label": "SLACK",
      "arrow_direction": "left",
      "description": "Flecha desde MIGRATION TEAM hacia SLACK."
    },
    {
      "source_label": "MIGRATION TEAM",
      "target_label": "DYNAMODB",
      "arrow_direction": "right",
      "description": "Flecha desde MIGRATION TEAM hacia DYNAMODB."
    },
    {
      "source_label": "SLACK",
      "target_label": "EC2 (5)",
      "arrow_direction": "down_right",
      "description": "Única entrada a EC2 (5) desde SLACK."
    },
    {
      "source_label": "EC2 (5)",
      "target_label": "APP DISCOVERY SERVICE",
      "arrow_direction": "left",
      "description": "Primera salida de EC2 (5) hacia APP DISCOVERY SERVICE."
    },
    {
      "source_label": "EC2 (5)",
      "target_label": "CLOUDENDURE",
      "arrow_direction": "down_right",
      "description": "Segunda salida de EC2 (5) hacia CLOUDENDURE."
    },
    {
      "source_label": "EC2 (5)",
      "target_label": "BAKE AMI",
      "arrow_direction": "down",
      "description": "Tercera salida de EC2 (5): la línea baja y entra con punta de flecha por la derecha de BAKE AMI."
    },
    {
      "source_label": "EC2 (5)",
      "target_label": "EC2 (Lado Derecho)",
      "arrow_direction": "down_right",
      "description": "Cuarta salida de EC2 (5): línea que va a la derecha, cruza la línea vertical entrecortada y baja con punta de flecha sobre EC2 (Lado Derecho)."
    },
    {
      "source_label": "EC2 (5)",
      "target_label": "SHARED AMI",
      "arrow_direction": "down_right",
      "description": "Quinta salida de EC2 (5): línea que va a la derecha, cruza la línea vertical entrecortada, baja y entra con punta de flecha por la izquierda de SHARED AMI."
    },
    {
      "source_label": "CLOUDENDURE",
      "target_label": "EC2 (HOT REPLICA)",
      "arrow_direction": "left",
      "description": "Segunda entrada a EC2 (HOT REPLICA) desde CLOUDENDURE."
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
https://www.youtube.com/watch?v=-wLEkq21cvA

## FULL TRANSCRIPT:
Welcome to another episode of This is My Architecture. We're live here in Sydney. There's a great buzz here in the auditorium and it's great to be here. With me today is Josh Lopez. Josh, you're the distinguished engineer of cloud migrations at Versant. Fantastic to have you here. Thanks for coming. Thank you for having me. Could you tell us a little bit about what Versant does please? Sure. So Versant is the premier consulting partner of AWS. We've got our AWS competencies in migration, security and DevOps. We've also just recently received our managed service provider status and we're really really passionate about delivering outcomes for our customers. Awesome. So one of those important outcomes for customers is migrations and that's what we're going to talk about today. Can you walk us through or draw us through this architecture that we've got on the board please? Sure. So this architecture came about about three years ago when we were manually migrating service from on-premises on-premises to AWS. It was taking about three or four hours. So we decided to actually deliver this through automation and it first starts with agents getting installed. First the application discovery service is installed the on-premises server. This really gives us the inbound and outbound TCP connections. So that's metadata around the on-premises instances? Sure. And it also provides us with performance utilizations to give us the instance types that we need to provision in AWS. Okay. We then deploy the CloudEndure live migration agent as well and this is volume replication. So it's block by block replication from the on-premises server to AWS. So it's really making sure that it's continuously replicating across. We've actually had customers test this product by putting a file deep in the file system. Yep. And when it moves from on-premises to AWS that file actually still exists. So awesome. Okay. So we've got our metadata around those on-premises servers and we've got the data replicated into AWS. What's driving that? What's integrating with that? Sure. So we've got DynamoDB and effectively what we've got here is the migration team filling DynamoDB with actually metadata. So this is operational information. So RTOs, RPOs, so the infrastructure owners, the business owners as well. Really giving the actual tags that will be placed on the EC2 instance. Also the target account. Yep. The subnet, the IP as well. And that's all over here in the target account. That's the target account effectively. Yeah. So we've gathered the TCP connections. We've got the replicated data and we've also got the tags that will live on that server. Okay. And what are they actually interfacing with here? What's this instance doing, the migration factory itself? So the migration factory effectively is the thing that moves the server from on-premises to AWS. It does all the integrations. So it's kicked off from Slack. So the migration team will issue one command. That then effectively talks to the EC2 instance. So it's calling an API on there? So it calls the API on the EC2 instance. Effectively that then starts the migration. So from there, the EC2 instance will talk to the application discovery service to gather the TCB inbound and outbound connections. It will also talk to CloudEndure. And again, these are just API calls to those services? These are all API calls. CloudEndure will then effectively stop the replication. So that replication is then stopped. Yep. From there, the EC2 instance, or the migration factory, will then bake the AMI. Yep. And that's another just API call. That's another API call. So we've got the hot replicated instance. So making sure that the data that was on on-premises is now living in an AMI. Yep. So from there, we effectively share that AMI across to the target account. Yep. Using the metadata that lives in DynamoDB. So we know exactly which target account that needs to live in. And then once effectively that is shared, it's shared through encryption as well. Yep. We then start that instance. And at that point, you're applying all of your sizing and your firewall rules, your metadata that was stored in DynamoDB. Is that right? Correct. Yeah. So we've got the instance type in there. We've got the specific IP address. We've also got the specific tags. So we're making sure that every server that goes across into AWS has a set tag. Around 10 tags, which really describe that specific server. And we understand exactly what that server is. Awesome. So you've gone from a state where it was taking four hours per instance to how long did you say? It takes about 10 minutes. So moving from on-premises now through all this entire flow, it's about 10 minutes to get across. So where next for this? So effectively what we've got is AWS has actually acquired TSO Logic. And that gives us the instance types. Effectively for us, we want to then grab those instance types and place those in DynamoDB. And then use those to actually drive the instance type that gets actually launched. So we're not actually using the performance metrics out of Discovery Service. We're using those out of TSO Logic. Awesome. Josh, thank you so much for coming and sharing your architecture with us and telling us how you're helping customers to migrate in a more faster and robust fashion. Thanks very much for tuning in to another episode of This Is My Architecture. And now, back to the desk. Thank you.