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
      "service": "ThirdParty",
      "name": "SANDFI SSO",
      "type": "ThirdParty",
      "rationale": "Bloque de texto SANDFI SSO con conexión bidireccional a Cognito."
    },
    {
      "service": "Cognito",
      "name": "Amazon Cognito",
      "type": "Cognito",
      "rationale": "Servicio Amazon Cognito de autenticación."
    },
    {
      "service": "S3",
      "name": "Amazon S3 (1)",
      "type": "S3",
      "rationale": "Bucket S3 central de datos con múltiples conexiones bidireccionales."
    },
    {
      "service": "CloudFront",
      "name": "Amazon CloudFront",
      "type": "CloudFront",
      "rationale": "Distribución CloudFront entre S3(1) y el usuario."
    },
    {
      "service": "UserConsumerWeb",
      "name": "User",
      "type": "UserConsumerWeb",
      "rationale": "Usuario final conectado bidireccionalmente a CloudFront."
    },
    {
      "service": "ApiGateway",
      "name": "Amazon API Gateway",
      "type": "ApiGateway",
      "rationale": "API Gateway conectado entre S3(1) y DynamoDB."
    },
    {
      "service": "DynamoDB",
      "name": "Amazon DynamoDB",
      "type": "DynamoDB",
      "rationale": "Base de datos DynamoDB conectada a API Gateway."
    },
    {
      "service": "ServiceCatalog",
      "name": "AWS Service Catalog",
      "type": "ServiceCatalog",
      "rationale": "Service Catalog conectado a S3(1), RStudio y SageMaker."
    },
    {
      "service": "EC2",
      "name": "RStudio (EC2)",
      "type": "EC2",
      "rationale": "Instancia RStudio con ícono de EC2 conectada a Service Catalog."
    },
    {
      "service": "SageMaker",
      "name": "Amazon SageMaker",
      "type": "SageMaker",
      "rationale": "Servicio Amazon SageMaker conectado a Service Catalog."
    },
    {
      "service": "Lambda",
      "name": "AWS Lambda",
      "type": "Lambda",
      "rationale": "Función AWS Lambda conectada a Translate y Comprehend Medical."
    },
    {
      "service": "Translate",
      "name": "Amazon Translate",
      "type": "Translate",
      "rationale": "Servicio de traducción conectado a AWS Lambda."
    },
    {
      "service": "Comprehend",
      "name": "Amazon Comprehend Medical",
      "type": "Comprehend",
      "rationale": "Servicio Comprehend Medical conectado a AWS Lambda."
    },
    {
      "service": "S3",
      "name": "Data Lake",
      "type": "S3",
      "rationale": "Cubo (bucket) separado etiquetado como Data Lake sin conexiones explícitas."
    }
  ],
  "visual_connections": [
    {
      "source_label": "SANDFI SSO",
      "target_label": "Amazon Cognito",
      "arrow_direction": "right",
      "description": "Ida: SANDFI SSO hacia Cognito."
    },
    {
      "source_label": "Amazon Cognito",
      "target_label": "SANDFI SSO",
      "arrow_direction": "left",
      "description": "Retorno: Cognito hacia SANDFI SSO."
    },
    {
      "source_label": "Amazon Cognito",
      "target_label": "Amazon S3 (1)",
      "arrow_direction": "right",
      "description": "Ida: Cognito hacia S3(1)."
    },
    {
      "source_label": "Amazon S3 (1)",
      "target_label": "Amazon Cognito",
      "arrow_direction": "left",
      "description": "Retorno: S3(1) hacia Cognito."
    },
    {
      "source_label": "Amazon S3 (1)",
      "target_label": "Amazon CloudFront",
      "arrow_direction": "right",
      "description": "Ida: S3(1) hacia CloudFront."
    },
    {
      "source_label": "Amazon CloudFront",
      "target_label": "Amazon S3 (1)",
      "arrow_direction": "left",
      "description": "Retorno: CloudFront hacia S3(1)."
    },
    {
      "source_label": "Amazon CloudFront",
      "target_label": "User",
      "arrow_direction": "right",
      "description": "Ida: CloudFront hacia User."
    },
    {
      "source_label": "User",
      "target_label": "Amazon CloudFront",
      "arrow_direction": "left",
      "description": "Retorno: User hacia CloudFront."
    },
    {
      "source_label": "Amazon S3 (1)",
      "target_label": "Amazon API Gateway",
      "arrow_direction": "down",
      "description": "Ida: S3(1) hacia API Gateway."
    },
    {
      "source_label": "Amazon API Gateway",
      "target_label": "Amazon S3 (1)",
      "arrow_direction": "up",
      "description": "Retorno: API Gateway hacia S3(1)."
    },
    {
      "source_label": "Amazon API Gateway",
      "target_label": "Amazon DynamoDB",
      "arrow_direction": "right",
      "description": "Ida: API Gateway hacia DynamoDB."
    },
    {
      "source_label": "Amazon DynamoDB",
      "target_label": "Amazon API Gateway",
      "arrow_direction": "left",
      "description": "Retorno: DynamoDB hacia API Gateway."
    },
    {
      "source_label": "Amazon S3 (1)",
      "target_label": "AWS Service Catalog",
      "arrow_direction": "up_right",
      "description": "Ida: S3(1) hacia Service Catalog."
    },
    {
      "source_label": "AWS Service Catalog",
      "target_label": "Amazon S3 (1)",
      "arrow_direction": "down_left",
      "description": "Retorno: Service Catalog hacia S3(1)."
    },
    {
      "source_label": "AWS Service Catalog",
      "target_label": "RStudio (EC2)",
      "arrow_direction": "right",
      "description": "Ida: Service Catalog hacia RStudio."
    },
    {
      "source_label": "RStudio (EC2)",
      "target_label": "AWS Service Catalog",
      "arrow_direction": "left",
      "description": "Retorno: RStudio hacia Service Catalog."
    },
    {
      "source_label": "AWS Service Catalog",
      "target_label": "Amazon SageMaker",
      "arrow_direction": "up",
      "description": "Ida: Service Catalog hacia SageMaker."
    },
    {
      "source_label": "Amazon SageMaker",
      "target_label": "AWS Service Catalog",
      "arrow_direction": "down",
      "description": "Retorno: SageMaker hacia Service Catalog."
    },
    {
      "source_label": "AWS Lambda",
      "target_label": "Amazon Translate",
      "arrow_direction": "right",
      "description": "Ida: Lambda hacia Translate."
    },
    {
      "source_label": "Amazon Translate",
      "target_label": "AWS Lambda",
      "arrow_direction": "left",
      "description": "Retorno: Translate hacia Lambda."
    },
    {
      "source_label": "AWS Lambda",
      "target_label": "Amazon Comprehend Medical",
      "arrow_direction": "down_right",
      "description": "Ida: Lambda hacia Comprehend Medical."
    },
    {
      "source_label": "Amazon Comprehend Medical",
      "target_label": "AWS Lambda",
      "arrow_direction": "up_left",
      "description": "Retorno: Comprehend Medical hacia Lambda."
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
https://www.youtube.com/watch?v=2L0m28ZLmtE

## FULL TRANSCRIPT:
Bonjour et bienvenue à This is my architecture. Je m'appelle Walid et aujourd'hui je suis accompagné par Martin de Sanofi et Arnaud de Teamwork. Bonjour Martin, parlez-nous de ce que vous faites chez Sanofi. Bonjour Walid, je travaille comme solution architecte dans le département ITS CMO, Chief Medical Officer, sur la partie Real World Evident de l'écosystème d'Arwen. Bonjour Arnaud. Bonjour, je suis data architecte au sein de la société Teamwork et nous sommes partenaires à WS. Martin, parlez-nous de votre besoin métier et pourquoi cette solution? Dans le cadre de l'écosystème d'Arwen, travaillant sur les données du monde réel, les Real World Evidence Data, on avait un besoin de nos data scientists, environ 30 à 40 % de leur analyse était nécessaire, nécessairement être faite sur des données plus moins big data, plus smart data set. Avec des environnements ou des outils plutôt centrés vers RStudio, SageMaker, il y avait aussi un besoin de traduction NLP nécessaire à leur analyse aussi. Donc vous avez besoin d'un écosystème pour des data scientists sur AWS. Oui, c'est un système sécurisé, on peut implémenter la traçabilité des données et tout ça en même temps. Très bien. Arnaud, est-ce que vous pouvez nous donner un peu plus d'input sur la partie technique? Oui, tout à fait. Nous avons construit la solution entièrement sur AWS avec l'ensemble des services qui s'offrent à nous et nous avons développé un site web statique via la fonctionnalité static website de S3 et pour réduire les coûts nous avons utilisé une distribution cloud front qui détient également le certificat. Nous avons identifié nos utilisateurs avec Cognito et le SSO de Sanofi. Puis cette partie statique, nous avons aussi une partie dynamique avec la traçabilité des données que nous avons implémentées avec API Gateway et DynamoDB. Très bien. Donc il y a un portail web auquel les utilisateurs ont accès. Donc une partie statique avec une authentification via la fédération d'identité sur Cognito et les identités sur votre SSO de Sanofi. Et une partie dynamique avec l'utilisation d'Api Gateway. Quel est l'usage de DynamoDB ici? DynamoDB permet de contenir les métadatas des utilisateurs mais aussi l'ensemble des actions qui sont effectuées sur le portail Data Analytics. Donc il y a une traçabilité forte des utilisateurs sur DynamoDB. Tout à fait. Très bien. Donc ça c'est la partie portail. A quoi les utilisateurs ont accès justement par la suite? Via ce portail, les utilisateurs ont la possibilité de se provisionner des produits que nous avons développés avec Martin. Il s'agit de deux produits principalement que sont SageMaker et RStudio. Et nous avons développé ces produits via l'utilisation de Service Catalog. En effet, Service Catalog nous permet de construire des produits spécifiques via CloudFormation. Ainsi, les SageMaker Notebooks sont chiffrés avec un disque de 100 gigas pour stocker les données, mais aussi tracés puisque chaque utilisateur a son propre SageMaker Notebook ou Machinaire Studio. Ce qui lui permet d'accéder à uniquement son set de données auxquelles il doit avoir accès. Très bien. Donc ce que je comprends ici, vous faites appel à Service Catalog pour avoir un portfolio de produits à proposer à vos utilisateurs directement depuis le portail. Sur Service Catalog, vous allez utiliser bien sûr CloudFormation qui vous permet de répéter le déploiement à ces utilisateurs-là avec des environnements spécifiques, avec un accent sur la partie sécurité et cloisonnement des utilisateurs. Tout à fait. Très bien. Alors ça, c'est la partie Service Catalog que je vois ici. Par ici, je vois d'autres services de machine learning sur AWS. À quoi ils servent et comment vous les utilisez sur votre portail? Au travers du portail que nous avons développé, nous avons utilisé deux services. Le premier, Translate, car il y avait un besoin de traduction en masse de fichiers bruts. Pour cela, nous avons utilisé directement le SDK via des lambdas afin de traduire d'une langue automatiquement détectée via Comprehend vers une langue cible choisie par l'utilisateur. La seconde possibilité également est Comprehend médical car nous avons des besoins d'identification des données au sein de fichiers bruts. Pour cela, nous avons également développé des lambdas qui utilisent le SDK de Comprehend afin d'identifier ces métadonnées. Très bien. Donc là, de ce côté-là, vous faites appel à des services proposés par AWS, qui sont préentraînés par AWS pour vos data scientists directement avec Translate et Comprehend médical. Très bien. Et là, on voit un Data Lake. À quoi il sert et comment vous l'intégrez dans votre plateforme? Aujourd'hui, la grosse criticité de cette plateforme-là, c'est que les données sont très sensibles. Donc, les données doivent rester dans l'environnement. On permet à l'utilisateur d'extraire des données dans le Data Lake, dans leur home user, leur bucket S3, et les traiter par la suite dans les différents systèmes, que ce soit Air Studio, SageMaker, Translate ou bien Comprehend, NLP. Donc, toute la donnée qui est utilisée dans notre environnement Darwin, donc au système aujourd'hui, doit rester en environnement, mais pas extractable, ne peut pas être téléchargée dans une poste de travail ou quoi que ce soit. Elle est ségrée, on utilise la partie Data Lake et l'environnement qu'on a mis en place pour ça besoin. Très bien. Donc, le Data Lake, c'est pour avoir des données, mais il y a un accent encore supplémentaire sur la ségrégation des données, sur le chiffrement des données, sur le contrôle et l'audit des données. Oui. Aujourd'hui, on utilise l'almoDB comme expliquait Arnaud pour la partie traçabilité de chaque donnée qui est utilisée dans l'environnement. Et chaque utilisateur a le droit à son propre home user où il faut mettre ses données à lui et nous faut partager avec d'autres utilisateurs. Car chaque donnée n'est accessible que par un utilisateur selon des droits déjà prédéfinis. Très bien. Alors, quel est le retour des utilisateurs avec votre portail? On ciblait au début, c'était vraiment, on est en production depuis début août, je dirais Arnaud. Oui. On ciblait 5 à 10 utilisateurs bêta-testeurs et au bout de 2-3 semaines, on a monté rapidement à 30-40 utilisateurs et on continue de monter. Donc, aujourd'hui, on regarde avec Teamwork aujourd'hui et mettre en place d'autres services basés aussi sur des outils analytiques ou des parties data lake, un peu comme Lake Formation. Mais c'est très, très positif chez nous aujourd'hui. Merci Martin. Merci Arnaud. Merci. Merci Walid. Merci d'avoir regardé Decisement Architecture. Merci à vous.