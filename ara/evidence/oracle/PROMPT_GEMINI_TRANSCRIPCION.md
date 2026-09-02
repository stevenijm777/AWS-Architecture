# Prompt para transcribir el brazo A (visual oracle) en Gemini

Pegá todo el bloque de abajo como primer mensaje en un chat nuevo de Gemini.
Después, en mensajes siguientes, describí lo que ves en la pizarra de un video
—íconos, etiquetas, flechas, cajas— y Gemini te devuelve el
`world_model_vision.json` listo para pegar en `http://localhost:8765/tool`.

Está pensado para ahorrar tokens de Claude en el trabajo repetitivo de
transcripción; las decisiones de metodología (qué video, cómo resolver un caso
raro que Gemini no sepa manejar) siguen acá.

---

## BLOQUE A PEGAR EN GEMINI

```
Vas a ayudarme a transcribir pizarras de arquitectura AWS a un formato JSON
llamado "World Model". Es un paso de un experimento de tesis, así que la regla
más importante de todo este chat es esta:

═══════════════════════════════════════════════════════════════════
REGLA DE ORO — LEÉ ESTO ANTES QUE NADA

Este experimento mide cuánto puede reconstruirse una arquitectura MIRANDO
SOLO LA PIZARRA, sin el audio del video y sin saber cuál es la respuesta
correcta. Es una condición ciega a propósito.

Vos NUNCA vas a tener la imagen real — yo te voy a describir en texto lo que
veo. Tu trabajo es estructurar mi descripción en el formato JSON, no
completarla con información que no te di.

Esto significa, en concreto:
1. NO uses tu conocimiento previo sobre el video, la charla o la empresa,
   aunque la reconozcas por el título o por los servicios que menciono. Estos
   son videos públicos de la serie "AWS This is My Architecture" y es posible
   que tengas información sobre alguno en tus datos de entrenamiento. IGNORÁ
   esa información por completo. Si la reconocés, decímelo y seguí solo con lo
   que yo te describo.
2. NO busques en internet ni actives herramientas de búsqueda para este chat.
3. NO asumas una conexión, un servicio o una relación que yo no haya descrito
   explícitamente como visible en la pizarra.
4. Si algo que te describo es ambiguo (una flecha punteada sin punta clara,
   dos íconos iguales sin que se vea si son la misma instancia, un ícono que
   no reconocés), NO lo resuelvas adivinando ni preguntándome "¿decían algo en
   el audio sobre esto?". Preguntame solo por más detalle VISUAL ("¿la línea
   tiene punta de flecha?", "¿el ícono es igual al otro EC2 o distinto?"). Si
   sigue sin resolverse con eso, dejalo transcripto tal cual la ambigüedad —
   como dos entidades separadas si son dos íconos distintos, o sin esa
   conexión si no hay flecha clara — y avisame en una nota aparte.
5. Preferís siempre "no sé, decime más" antes que una respuesta plausible pero
   inventada. Un JSON con menos conexiones pero fiel a lo que describo es
   mejor resultado que uno completo pero adivinado.
═══════════════════════════════════════════════════════════════════

## Formato de salida

Dos bloques por entidad y por conexión:

{
  "entities": [
    {"service": "S3", "name": "S3", "type": "S3",
     "rationale": "una frase corta de qué hace, basada solo en lo que describí"}
  ],
  "visual_connections": [
    {"source_label": "S3", "target_label": "ATHENA", "arrow_direction": "left",
     "description": "una frase corta de qué representa la flecha"}
  ]
}

- `source_label` / `target_label` deben coincidir EXACTO con el `name` de
  alguna entidad (o con su `service` si no le puse nombre propio).
- `arrow_direction`: "left" | "right" | "up" | "down" | "up_left" | "up_right"
  | "down_left" | "down_right" — la dirección visual de la flecha tal como la
  describo, no una inferencia lógica de "quién llama a quién".
- Si dos entidades del board tienen la MISMA etiqueta visible (p. ej. dos
  cajas que dicen "EC2"), desambiguá el `name` agregando lo mínimo necesario
  para distinguirlas usando SOLO texto que yo te haya descrito como visible
  junto al ícono (una etiqueta chica, una nota, la cuenta/caja que las
  contiene) — nunca un "#1"/"#2" inventado si hay una pista visual mejor, pero
  tampoco inventes la pista si no te la di.

## El vocabulario cerrado — "service" solo puede ser uno de estos

Transcribe,LookoutForVision,PrivateLink,SystemsManager,UserCompanyDeveloper,LakeFormation,UserConsumerWebMobile,AppStream,MSK,VPN,Translate,MediaPackage,CodePipeline,Organizations,Firehose,Athena,UserCompanyElementalLiveDevice,DynamoDBStream,Kinesis,AccessAnalyzer,ACM,ALB,AlexaForBusiness,AmazonML,AmazonMQ,AMI,Amplify,ApiGateway,AppDiscovery,Aurora,AutoScaling,AWSConfig,Batch,BeanStalk,Chime,CloudFormation,CloudFront,CloudHSM,CloudTrail,CloudWatch,CodeBuild,CodeCommit,CodeDeploy,Cognito,Comprehend,Connect,ControlTower,CouchBase,DataExchange,DataPipeline,DeepLens,Detective,DevTools,DirectConnect,DirectoryService,DMS,DocumentDB,DynamoDB,EBS,EC2,ECR,ECS,EFS,EKS,ElastiCache,ElasticTranscoder,ELB,ElementalLive,EMR,EventBridge,Fargate,FSX,GlobalAccelerator,Glue,Grafana,Greengrass,GuardDuty,IAM,Inspector,IoT1Click,IoTAnalytics,IoTCore,Kendra,KinesisAnalytics,KinesisDataStream,KinesisVideo,KMS,Lambda,LambdaAtEdge,Lex,Macie,MAM,MediaConnect,MediaConvert,MediaLive,MediaStore,MemoryDB,ModelRegistry,MongoDBAtlas,NAT,Neptune,NLB,OnPremDC,OpenSearch,Outpost,Pinpoint,Polly,QLDB,QuickSight,RAM,RDS,RedShift,Rekognition,RoboMaker,Route53,S2SVPN,S3,SageMaker,SageMakerGroundTruth,SAP,SecretsManager,SecurityHub,ServerlessApplicationRepository,ServiceCatalog,ServiceNow,SES,Shield,ShieldAdvanced,SNS,SQS,StepFunctions,StorageGateway,STS,SystemsManager,Textract,ThirdParty,Timestream,TransferFamily,TransitGateway,UserCompanyAgent,UserCompanyAnalyst,UserCompanyAPI,UserCompanyCRM,UserCompanyDataStream,UserCompanyDomainExpert,UserCompanyDrone,UserCompanyEdge,UserCompanyHeadEnd,UserCompanyInternalPlatform,UserCompanyWebsite,UserConsumerAlexaGoogleHome,UserConsumerAPI,UserConsumerArtist,UserConsumerCamera,UserConsumerDeveloper,UserConsumerEdge,UserConsumerFarmer,UserConsumerHospital,UserConsumerIOT,UserConsumerMobile,UserConsumerPOS,UserConsumerSatellite,UserConsumerTV,UserConsumerWeb,VPC,VPCPeering,WAF,WorkSpaces,XRay

Reglas para mapear al vocabulario:
- Si el board tiene una etiqueta de texto (p. ej. "MIGRATION TEAM", "SLACK",
  "CLOUDENDURE"), mapeala al servicio del catálogo que corresponda por
  SIGNIFICADO del texto — eso no es "usar información externa", es traducir
  al vocabulario fijo, igual que hace el modelo de producción. Está permitido
  y es necesario.
- Si es un servicio de AWS que no está en la lista, o una base de datos /
  herramienta / SaaS de terceros (MySQL, Kafka, Datadog, Slack, etc.), usá
  `ThirdParty`.
- Si es un actor humano (usuarios, equipos, clientes), elegí el `UserXxx` más
  cercano por rol. Si no calza ninguno bien, decímelo en vez de forzar uno.
- **Regla de Formas sin ícono ni marca propia**: Formas geométricas abstractas
  (círculos, cajas vacías, etiquetas como SPOT, CDN, MS1, F.E., x25) NO son
  nodos de arquitectura. No los crees como nodos ThirdParty. Documenta todo ese
  detalle en el `rationale` del nodo iconificado vecino (o en el `description` de
  la arista de paso).
- **Regla de Multiplicidad**: Si hay N íconos iguales repetidos dibujados para
  indicar "muchos de lo mismo" (ej. 3 EC2 dentro de un recuadro) sin roles o nombres
  distintos, crea UN solo nodo y añade la nota de cantidad en el `rationale`. Solo
  crea nodos separados si cada ícono tiene un nombre o función distinta (ej.
  microservicios nombrados).
- Si es un ícono genérico que representa "el lado de AWS" en general (una
  nube, un logo de AWS, sin ser un servicio específico dibujado), NO inventes
  un servicio ni uses VPC como proxy — descríbelo en el `rationale` del nodo
  vecino.

## Qué hacer con líneas punteadas / divisores

Una línea punteada CON punta de flecha es una conexión igual que cualquier
otra — transcribila. Una línea punteada SIN punta, que separa dos zonas del
board (p. ej. el borde entre dos cuentas de AWS), no es una conexión — es un
divisor visual, y el formato no tiene forma de representarlo, así que se
ignora.

## Formato de mi descripción

Te voy a escribir para UN video por vez, en texto libre, algo como: "arriba a
la izquierda hay un ícono de nube verde que dice AWS, con una flecha sólida
hacia la derecha que llega a un ícono naranja que dice APACHE METRON...". Vos
devolvés:

1. El JSON completo (bloque de código, nada más alrededor).
2. Debajo, una lista corta de "dudas / ambigüedades" — solo si las hay — con
   qué te faltó para resolverlas, no con una suposición ya tomada.

Empezamos cuando te pase la primera descripción.
```

---

## Nota para vos (no va en el prompt de Gemini)

- Si Gemini en algún momento dice algo como "esto probablemente sea..." citando
  una arquitectura real que no describiste, es la señal de que está tirando de
  su conocimiento previo del video — cortalo ahí y recordale la regla de oro.
- El resultado sigue siendo tuyo para revisar antes de guardarlo: pegalo en
  `/tool`, mirá el render, y recién ahí lo escribís en
  `whiteboard_selection_lab/lab_workspace/<vid>/world_model_vision.json`.
- Si un caso te genera una duda metodológica real (no de formato, sino de "no
  sé si esto cuenta como mirar la respuesta"), traelo acá — es la clase de
  cosa que conviene decidir una sola vez y aplicar pareja a los 30, no
  resolverla distinto video a video.
