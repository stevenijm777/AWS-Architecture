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
      "name": "USER",
      "type": "UserConsumerWeb",
      "rationale": "Ícono genérico de persona (cabeza y hombros) rotulado USER, sin ningún atributo visual que indique el rol. De él sale una línea con la palabra manuscrita 'https://...' encima hacia ROUTE 53. El rol concreto no es determinable solo con la imagen."
    },
    {
      "service": "Route53",
      "name": "ROUTE 53",
      "type": "Route53",
      "rationale": "Servicio DNS Amazon Route 53 resolviendo peticiones iniciales."
    },
    {
      "service": "ALB",
      "name": "ALB",
      "type": "ALB",
      "rationale": "Application Load Balancer distribuyendo tráfico hacia las instancias de cómputo."
    },
    {
      "service": "EKS",
      "name": "EKS (SPOT)",
      "type": "EKS",
      "rationale": "Dos íconos apilados dentro de un mismo recuadro verde entrecortado (arco abierto por arriba y por la derecha): arriba el ícono naranja de EKS rotulado EKS, y debajo un ícono gris con una diana naranja rotulado SPOT. Se transcriben como UNA entidad porque comparten el recuadro y porque SPOT es el modificador de capacidad del cluster, no un componente aparte; el ícono de EKS no tiene ninguna punta de flecha incidente en este frame — todas las flechas de la zona entran o salen por SPOT. Del lado izquierdo de SPOT sale una flecha hacia un óvalo dibujado a mano SIN ícono ni etiqueta, del que cuelgan tres textos manuscritos 'M.S.1', 'M.S.2' y 'M.S.3' (sin ícono, sin caja): esos cuatro elementos no se transcriben como entidades y las flechas que nacen de ellos se registran desde este bloque. ALTERNATIVA DESCARTADA: dejar SPOT como nodo EC2 propio (tiene ícono), lo que daría 7 entidades y dejaría a EKS aislado."
    },
    {
      "service": "SNS",
      "name": "SNS",
      "type": "SNS",
      "rationale": "Amazon Simple Notification Service recibiendo notificaciones desde la zona de microservicios (MS1) y conectando a SQS."
    },
    {
      "service": "SQS",
      "name": "SQS",
      "type": "SQS",
      "rationale": "Amazon Simple Queue Service recibiendo mensajes desde la zona de microservicios (MS1) y desde SNS."
    }
  ],
  "visual_connections": [
    {
      "source_label": "USER",
      "target_label": "ROUTE 53",
      "arrow_direction": "right",
      "description": "El usuario resuelve el dominio a través de Route 53."
    },
    {
      "source_label": "ROUTE 53",
      "target_label": "ALB",
      "arrow_direction": "right",
      "description": "Route 53 enruta el tráfico hacia el Application Load Balancer."
    },
    {
      "source_label": "ALB",
      "target_label": "EKS (SPOT)",
      "arrow_direction": "right",
      "description": "ALB envía tráfico hacia el bloque EKS/SPOT que se distribuye a través del nodo circular a los microservicios MS1, MS2, MS3."
    },
    {
      "source_label": "EKS (SPOT)",
      "target_label": "SQS",
      "arrow_direction": "down_right",
      "description": "Flecha saliente desde el área de microservicios (MS1) directamente hacia la cola SQS."
    },
    {
      "source_label": "EKS (SPOT)",
      "target_label": "SNS",
      "arrow_direction": "up_right",
      "description": "Flecha saliente desde el área de microservicios (MS1) hacia el tema SNS."
    },
    {
      "source_label": "SNS",
      "target_label": "SQS",
      "arrow_direction": "down",
      "description": "SNS publica y envía mensajes a la cola SQS."
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
https://www.youtube.com/watch?v=1aYoIZvabbk

## FULL TRANSCRIPT:
Hi everyone, welcome to This is my Architecture. I'm Jasmine and I have here with me Nikhil Sharma from OLX Autos. Hi Nikhil, thanks for joining us. Hi Jasmine, thank you, thank you for having me. Tell us about OLX Autos. At OLX Autos we offer a one-stop solution to buy and sell used vehicles from having an online evaluation of your car to have an own inspection. We offer anything and everything. Okay, and do you have global presence? Yes, we do. As of now we are operational in 11 countries including India, Indonesia, South America and Turkey. And what are the challenges of going global? So there have been countless challenges. A few of the challenges we have solved is by building an internal developer platform tool because primarily one of the challenges was to reduce our time to market and accelerate our deployment velocity. Okay, and so if I as a user have to create the platform, what's there under the hood of this architecture? Okay, so as an end user if you want to have an environment, you just go to the Orion portal and you'll just go with the... And then once you have the... We also open up the Orion portal, and then the DNS resolution goes to the Amazon Rout of 53. We are using it for the DNS resolution. And then it resolves the DNS to the Amazon Application Load Balancer. And then the Amazon Load Application Load Balancer is going to send the request to our Kubernetes pods. We are using Amazon EKS as a container orchestrator. And then all of our workload is running on AWS EKS. So when you are creating a request to our new environment, you will mention some details like name of the environment, the business use case of the environment, and the business vertical that you want to create for which this environment is needed. And then this request goes to our application pod that is running on Amazon EKS and underlying it is using spot instances. Okay. And what percent of spot do you use? As of now, we are using 100% spot instances. Wow. That's amazing. So how about the cost optimization that you've achieved with 100%? So the use case that we had is that we are creating the replicas of Olex orders environments. And we had to keep the cost in check because if we're creating too many replicas, we obviously increase in the cost exponentially. So that's why we just finalized that we are going to go with 100% spot for the efficient cost utilization. And we just have to figure out how we can leverage spot to its maximum capacity. Okay. And as you are leveraging spot, you also need to take care of spot termination, right? How do you do that? Yes. Yes. So for that, we are using AWS node termination handler. So whenever Amazon is about to terminate any spot instances, it senses an event which AWS termination handler is listening to and then it drains out that nodes. So all the workload that was running on that spot instances gets shifted to another node. So would not experience any disruption in the business. Got it. So basically the request comes to the ports which are deployed on spot, right? And this is orchestrated by Amazon Elastic Kubernetes Service. Exactly. Okay. And how does Amazon EKS help you? It helps us by offloading the operational overhead and it is helping us by handling the MS load that we are putting on it. We started with the 100 ports and now we are running with 10,000 plus ports. So we are incrementally stress testing Amazon EKS. Wow. And that's quite a journey, right? Starting from 100 ports to 10,000 ports. Yes. So that's amazing. And how about this Amazon SNS and SKS? What is the role of these two? Okay. So when a user is trying to making a request to create an environment, ultimately what it's requesting is I need a bunch of microservices for that business vertical. For example, if you are creating an environment for business vertical X, it may need 70 plus microservices. So this our main application running as a pod, it is going to create the number of jobs, Kubernetes jobs for each microservice. For example, if you're launching three microservices, then it will create a job that will take care of launching microservice one, launching microservice two, launching microservice three. Now, as we are running everything on spot, there is a strong likelihood that before the time this job gets completed, spot instances terminates the underlying node and this job gets disrupted. EKS takes care of replacing this job by another job, but ultimately the process was not able to finish up the task that it was assigned to. So what we are doing is whenever a job gets triggered to create the microservice, it sends an event to Amazon SNS and then Amazon SNS finds out that message to SQS. So the new job that is getting replaced by this one watches out the AWS SQS and notices, okay, there is an unfinished job and that job was supposed to launch microservice one, but it failed to do so due to XYZ reason. So that takes care of launching and finishing the job. Okay, great. So you have different jobs spinning up different microservices. Yes. Right? Every job stores the state through SNS to SQS. Yes. And when the job comes up, the new job comes up, it also checks SQS if there is anything pending to be processed. Exactly. So it watches out SQS so that we are having consistent state of the provisioning and maintenance of environments. Okay. And what's the benefit of this architecture? So with this architecture, we are able to increase our deployment velocity and our global expansion. In December 2021, we are operating in nine markets. Now we are operating in 11 markets, such as well. And it also helped in reducing our time to market, shipping up our features faster to production. Amazing. Thank you so much, Nikhil, for sharing this architecture. It's a pleasure, Jasmine. Thank you. Thank you. And thank you everyone for joining us for This is My Architecture. Thank you.