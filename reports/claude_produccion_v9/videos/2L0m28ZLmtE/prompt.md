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
      "service": "ThirdParty",
      "name": "Sanofi SSO",
      "type": "ThirdParty",
      "rationale": "Hand-drawn box representing external single sign-on system federating with AWS."
    },
    {
      "service": "User",
      "name": "User",
      "type": "User",
      "rationale": "Hand-drawn actor symbols indicating data scientists/users accessing the web portal."
    },
    {
      "service": "CloudFront",
      "name": "CloudFront",
      "type": "CloudFront",
      "rationale": "CloudFront distribution serving static website content from S3."
    },
    {
      "service": "Cognito",
      "name": "Cognito",
      "type": "Cognito",
      "rationale": "Cognito service facilitating authentication federated with Sanofi SSO."
    },
    {
      "service": "S3",
      "name": "S3 (Web Portal)",
      "type": "S3",
      "rationale": "S3 bucket used to host the static website files."
    },
    {
      "service": "ApiGateway",
      "name": "API Gateway",
      "type": "ApiGateway",
      "rationale": "API Gateway managing dynamic API requests from the web portal."
    },
    {
      "service": "DynamoDB",
      "name": "DynamoDB",
      "type": "DynamoDB",
      "rationale": "DynamoDB storing audit trail logs, user actions, and metadata."
    },
    {
      "service": "ServiceCatalog",
      "name": "Service Catalog",
      "type": "ServiceCatalog",
      "rationale": "Service Catalog provisioning standardized data science workspaces using CloudFormation."
    },
    {
      "service": "Lambda",
      "name": "Lambda",
      "type": "Lambda",
      "rationale": "Lambda functions containing integration logic for calling translation and NLP APIs."
    },
    {
      "service": "EC2",
      "name": "R Studio",
      "type": "EC2",
      "rationale": "R Studio environment hosted on AWS and provisioned dynamically by users."
    },
    {
      "service": "SageMaker",
      "name": "SageMaker",
      "type": "SageMaker",
      "rationale": "SageMaker notebook environments utilized by data scientists."
    },
    {
      "service": "Translate",
      "name": "Translate",
      "type": "Translate",
      "rationale": "Amazon Translate service called via Lambda for mass document translation."
    },
    {
      "service": "Comprehend",
      "name": "Comprehend Medical",
      "type": "Comprehend",
      "rationale": "Comprehend Medical used for medical entity identification in clinical notes."
    },
    {
      "service": "S3",
      "name": "Data Lake",
      "type": "S3",
      "rationale": "Secure S3 bucket representing the central data lake housing sensitive medical data."
    }
  ],
  "visual_connections": [
    {
      "source_label": "User",
      "target_label": "CloudFront",
      "arrow_direction": "bidirectional",
      "description": "Users connect to the static web portal served via CloudFront."
    },
    {
      "source_label": "CloudFront",
      "target_label": "S3 (Web Portal)",
      "arrow_direction": "down",
      "description": "CloudFront distribution fetches static website assets from the hosting S3 bucket."
    },
    {
      "source_label": "Sanofi SSO",
      "target_label": "Cognito",
      "arrow_direction": "bidirectional",
      "description": "Sanofi enterprise identity provider federates user authentication with Cognito."
    },
    {
      "source_label": "Cognito",
      "target_label": "S3 (Web Portal)",
      "arrow_direction": "bidirectional",
      "description": "Cognito validates credentials for users accessing the S3-hosted web portal."
    },
    {
      "source_label": "S3 (Web Portal)",
      "target_label": "API Gateway",
      "arrow_direction": "bidirectional",
      "description": "Web portal makes dynamic API requests through API Gateway."
    },
    {
      "source_label": "API Gateway",
      "target_label": "DynamoDB",
      "arrow_direction": "bidirectional",
      "description": "API Gateway persists session traces, metadata, and user activity directly into DynamoDB."
    },
    {
      "source_label": "S3 (Web Portal)",
      "target_label": "Service Catalog",
      "arrow_direction": "bidirectional",
      "description": "Users request workspace provisioning from Service Catalog through the web interface."
    },
    {
      "source_label": "Service Catalog",
      "target_label": "R Studio",
      "arrow_direction": "down",
      "description": "Service Catalog launches a dedicated R Studio workspace upon user request."
    },
    {
      "source_label": "Service Catalog",
      "target_label": "SageMaker",
      "arrow_direction": "down",
      "description": "Service Catalog launches a SageMaker notebook environment secure for the requesting user."
    },
    {
      "source_label": "API Gateway",
      "target_label": "Lambda",
      "arrow_direction": "bidirectional",
      "description": "API Gateway routes NLP and translation requests to orchestrating Lambda functions."
    },
    {
      "source_label": "Lambda",
      "target_label": "Translate",
      "arrow_direction": "bidirectional",
      "description": "Lambda invokes Translate API for automated document translation tasks."
    },
    {
      "source_label": "Lambda",
      "target_label": "Comprehend Medical",
      "arrow_direction": "bidirectional",
      "description": "Lambda invokes Comprehend Medical API to detect clinical entities."
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
https://www.youtube.com/watch?v=2L0m28ZLmtE

## FULL TRANSCRIPT:
Bonjour et bienvenue à This is my architecture. Je m'appelle Walid et aujourd'hui je suis accompagné par Martin de Sanofi et Arnaud de Teamwork. Bonjour Martin, parlez-nous de ce que vous faites chez Sanofi. Bonjour Walid, je travaille comme solution architecte dans le département ITS CMO, Chief Medical Officer, sur la partie Real World Evident de l'écosystème d'Arwen. Bonjour Arnaud. Bonjour, je suis data architecte au sein de la société Teamwork et nous sommes partenaires à WS. Martin, parlez-nous de votre besoin métier et pourquoi cette solution? Dans le cadre de l'écosystème d'Arwen, travaillant sur les données du monde réel, les Real World Evidence Data, on avait un besoin de nos data scientists, environ 30 à 40 % de leur analyse était nécessaire, nécessairement être faite sur des données plus moins big data, plus smart data set. Avec des environnements ou des outils plutôt centrés vers RStudio, SageMaker, il y avait aussi un besoin de traduction NLP nécessaire à leur analyse aussi. Donc vous avez besoin d'un écosystème pour des data scientists sur AWS. Oui, c'est un système sécurisé, on peut implémenter la traçabilité des données et tout ça en même temps. Très bien. Arnaud, est-ce que vous pouvez nous donner un peu plus d'input sur la partie technique? Oui, tout à fait. Nous avons construit la solution entièrement sur AWS avec l'ensemble des services qui s'offrent à nous et nous avons développé un site web statique via la fonctionnalité static website de S3 et pour réduire les coûts nous avons utilisé une distribution cloud front qui détient également le certificat. Nous avons identifié nos utilisateurs avec Cognito et le SSO de Sanofi. Puis cette partie statique, nous avons aussi une partie dynamique avec la traçabilité des données que nous avons implémentées avec API Gateway et DynamoDB. Très bien. Donc il y a un portail web auquel les utilisateurs ont accès. Donc une partie statique avec une authentification via la fédération d'identité sur Cognito et les identités sur votre SSO de Sanofi. Et une partie dynamique avec l'utilisation d'Api Gateway. Quel est l'usage de DynamoDB ici? DynamoDB permet de contenir les métadatas des utilisateurs mais aussi l'ensemble des actions qui sont effectuées sur le portail Data Analytics. Donc il y a une traçabilité forte des utilisateurs sur DynamoDB. Tout à fait. Très bien. Donc ça c'est la partie portail. A quoi les utilisateurs ont accès justement par la suite? Via ce portail, les utilisateurs ont la possibilité de se provisionner des produits que nous avons développés avec Martin. Il s'agit de deux produits principalement que sont SageMaker et RStudio. Et nous avons développé ces produits via l'utilisation de Service Catalog. En effet, Service Catalog nous permet de construire des produits spécifiques via CloudFormation. Ainsi, les SageMaker Notebooks sont chiffrés avec un disque de 100 gigas pour stocker les données, mais aussi tracés puisque chaque utilisateur a son propre SageMaker Notebook ou Machinaire Studio. Ce qui lui permet d'accéder à uniquement son set de données auxquelles il doit avoir accès. Très bien. Donc ce que je comprends ici, vous faites appel à Service Catalog pour avoir un portfolio de produits à proposer à vos utilisateurs directement depuis le portail. Sur Service Catalog, vous allez utiliser bien sûr CloudFormation qui vous permet de répéter le déploiement à ces utilisateurs-là avec des environnements spécifiques, avec un accent sur la partie sécurité et cloisonnement des utilisateurs. Tout à fait. Très bien. Alors ça, c'est la partie Service Catalog que je vois ici. Par ici, je vois d'autres services de machine learning sur AWS. À quoi ils servent et comment vous les utilisez sur votre portail? Au travers du portail que nous avons développé, nous avons utilisé deux services. Le premier, Translate, car il y avait un besoin de traduction en masse de fichiers bruts. Pour cela, nous avons utilisé directement le SDK via des lambdas afin de traduire d'une langue automatiquement détectée via Comprehend vers une langue cible choisie par l'utilisateur. La seconde possibilité également est Comprehend médical car nous avons des besoins d'identification des données au sein de fichiers bruts. Pour cela, nous avons également développé des lambdas qui utilisent le SDK de Comprehend afin d'identifier ces métadonnées. Très bien. Donc là, de ce côté-là, vous faites appel à des services proposés par AWS, qui sont préentraînés par AWS pour vos data scientists directement avec Translate et Comprehend médical. Très bien. Et là, on voit un Data Lake. À quoi il sert et comment vous l'intégrez dans votre plateforme? Aujourd'hui, la grosse criticité de cette plateforme-là, c'est que les données sont très sensibles. Donc, les données doivent rester dans l'environnement. On permet à l'utilisateur d'extraire des données dans le Data Lake, dans leur home user, leur bucket S3, et les traiter par la suite dans les différents systèmes, que ce soit Air Studio, SageMaker, Translate ou bien Comprehend, NLP. Donc, toute la donnée qui est utilisée dans notre environnement Darwin, donc au système aujourd'hui, doit rester en environnement, mais pas extractable, ne peut pas être téléchargée dans une poste de travail ou quoi que ce soit. Elle est ségrée, on utilise la partie Data Lake et l'environnement qu'on a mis en place pour ça besoin. Très bien. Donc, le Data Lake, c'est pour avoir des données, mais il y a un accent encore supplémentaire sur la ségrégation des données, sur le chiffrement des données, sur le contrôle et l'audit des données. Oui. Aujourd'hui, on utilise l'almoDB comme expliquait Arnaud pour la partie traçabilité de chaque donnée qui est utilisée dans l'environnement. Et chaque utilisateur a le droit à son propre home user où il faut mettre ses données à lui et nous faut partager avec d'autres utilisateurs. Car chaque donnée n'est accessible que par un utilisateur selon des droits déjà prédéfinis. Très bien. Alors, quel est le retour des utilisateurs avec votre portail? On ciblait au début, c'était vraiment, on est en production depuis début août, je dirais Arnaud. Oui. On ciblait 5 à 10 utilisateurs bêta-testeurs et au bout de 2-3 semaines, on a monté rapidement à 30-40 utilisateurs et on continue de monter. Donc, aujourd'hui, on regarde avec Teamwork aujourd'hui et mettre en place d'autres services basés aussi sur des outils analytiques ou des parties data lake, un peu comme Lake Formation. Mais c'est très, très positif chez nous aujourd'hui. Merci Martin. Merci Arnaud. Merci. Merci Walid. Merci d'avoir regardé Decisement Architecture. Merci à vous.