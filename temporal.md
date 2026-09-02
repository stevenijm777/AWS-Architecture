# JYeXbUdFOdw
hay dos bloques  el primer bloque  es  Data ingestion 
Amazon S3(1) --> AWS Lambda(1) --> S3(2)
AWS Lambda (2) --> S3 (2)
AWS Lambda (2) --> OpenSearch (qeu dice graviton2 encima ) (1)

el segundo bbloque  
Va OpenSearch (qeu dice graviton2 encima ) (2)
S3 una flecha del ladod receho ,que viene de la nada 
Amazon RDS 
Amazon SES a USer 
# u3ZwnulzLnU
github --> lambda --> SQS <-- ECS Fargate (1) --> Ec2 
Ec2 ---> Auaroa <-- ECS fargate (2)

ECS fagate a ES (con el simbolo morado que contiene una lupa)
ECS Fargate (1) a github 
developers a github 
developers a EC2 


# jg85DzUZ9Ac
S3 --> SQS --> Lambda --> Datalake 
Lambda --> DynamoDB 
hay un lambda sin conexiones 
una linea abajo que separa 

---
OnPrem --> VPN --> DMS --> Redshift --> Datalake 
# jV8DwutbXbg
salen una flecha de la nada a kinesis 
--> Kinesis (1) --> Lambda (1) --> SQS --> Lambda (2) [de este sqs salen varias flechas que se desvanecen y solo una apunta a lambda]
lamnda (2) --> RDS (2)
lambda (2) --> Kinesis(2)
salen una flecha de la nada a RDS
--> RDS(1) --> Lambda(1)

# hMK2NJ-q9nc

ASg Sin conexiones 

cloud formation sin conexiones 
S3 sale una flecha a EC2(1), EC2(2), EC2(3) 
hay un cuadro que encierra con lineas entrecoradas a los 3 EC2
EC2(1) --> Direct connect 
EC2(2) --> Direct connect
EC2(3) --> Direct connect
Direct connect --> Twd/cnn center
Direct connect --> a satelites (hay dos satelites ATL, NYC) la feclha que va estos dice BOP 

S3 --> Twd/cnn center --> satelites

> **[Claude, 2026-08-29]** En el frame se ve un detalle que faltaba: **cada uno de los 3 EC2 tiene un "10" manuscrito a su derecha**, están apilados dentro del mismo recuadro naranja entrecortado, y el ícono de ASG está dibujado justo encima del recuadro. Los tres son idénticos y ninguno tiene etiqueta que lo distinga, así que el dibujo dice "muchas del mismo tipo", no "tres componentes distintos": **los consolidé en una sola entidad `EC2 (flota)`** con la multiplicidad y el recuadro anotados en el `rationale`. Las 3 flechas paralelas desde S3 y las 3 hacia Direct Connect quedan como una cada una.
> - Dejé `ASG` y `CloudFormation` como nodos aislados: tienen ícono de servicio propio, aunque no reciban ni emitan flechas.
> - No toqué `TWD/CNN Center` (ThirdParty) ni los satélites (UserConsumerSatellite): son íconos de edificio y de antena, el rol exacto no es determinable visualmente.
> - Efecto: svc F1 0.62 (igual), edge F1 0.27 → 0.36. Sigue siendo el más bajo de los 30, pero ahora por límite visual real y no por convención.

# f5EJBUfGZtw
expedia group --> S3(1) --> Glue --> S3(2) 
S3(1) -->  EC2 --> S3(2)

---
ECS --> Aurora --> Lambda --> SQS

me falto poner que de SQS va salesforce (no enteindo bienlo que dice revisar en texto)
# a6kqyqTNJM4
USER  --> CLoudfront --> Load Balancer --> EKS --> RDS
S3 --> CloudFront 
lambda   ---> CloudFront
EC2 --> CLoudfront (esta flecha se desvanceze y no completa el camino hacia el cloudfront)
Cloudwatch que tiene un intendo de linea hacia arriba tipo RDs, pero no alcanza a llegar hay que comprobar con texto) 
load Balancer a ---> Legacy 
EKS --> Mongo/Mafka 
# SSWwnNVYi_Q

hay 3 personistas la prierma con casco de constructor 
la segunda con un sombrero grande tipo monopoli 
la 3ra un ni;o 

de la persona de enmedio va a EC2 hay una conexion hacia AD, 
hay una flecha  vertical que separa al ec2 y las personas, y del otro lado  va un EC2 a hacia S3

luego EMR --> S3 --> (KMS) --> RDS

# c-1GXhOOOww

Haber lo que veo es lo siguiente

hay dos mu;equitos el primero hay flechas bidireccionales entre el munieco y la linea vertical 
el segundo solo tiene una flecha hacia la linea vertical
hay dos linea vertical entrecortadas y entre enllas hay la palbra CDN
del lado derecho hay un S3 bidireccional hacia la 2da linea vertical 
de la 2da linea vertical va a una flecha APPSYNC de ahi va lambda  y de hay una flecha bidirecional dynamoDB 
appsync va una flecha hacia dynamoDB 
la 2da linea vertical tiene una flecha hacia API Gateway hacia a lambda 
del Lambda va hacia una flecha bidireccional hacia SQS 

# -3lnf5lzsH0
Haber primero veo con un icono verde que tiene una nube y un candado adentro porbablemente sea s3 (1), revisar la transcripcion para coraborar
de ese s3(1) sale una flecha a apache metron (que tiene como icono de EC2), de ahi sale a otro EC2 que tiene el nombre SOAR, de ese EC2 sale una flecha hacia alerts que tiene el icono de user, de se ese icono sale a otro EC2 con nombre (WAF)

tambien hay un servicion On-Prem que tiene una flecha hacia   APache Metron 

tambien hay un cuadro punteado que contiene 
(EMR, S3, Athena ) y el cuadro esta nombrado como security DataLake 
|
de este cuadro sale una flecha hacia Apache Metron (EC2)
del Apache metron sale hacia el EMR conexion directa y de EMR va a S3 y de ahi va a Athena

> **[Claude, 2026-08-29]** Revisé el frame. Dos cambios:
> - **Revertí `S3(1)` a `VPC`.** El ícono es una NUBE verde con candado rotulada "AWS". El S3 de verdad de esta misma pizarra es el balde verde dentro del recuadro "Security Data Lake", y son dos íconos distintos. Además la justificación original para el cambio fue "si reviso el cloudscape veo que hay un s3 separado" — eso es razonar desde el ground truth, no desde la imagen, y es justo lo que el brazo ciego no puede hacer. Queda como entidad genérica única sin descomponer.
> - **`Apache Metron`: EC2 → ThirdParty.** El ícono es de EC2 pero la etiqueta es el nombre propio de un producto externo, y la etiqueta manda sobre el ícono genérico de cómputo. SOAR se queda como EC2 porque su etiqueta es una categoría, no un producto. Mismo criterio que MySQL en -kA0ahrhX3I.
> - Agregué la curva larga que vuelve a Apache Metron desde la zona alerts/SOAR, dejando anotado en el `description` que no se puede decidir cuál de los dos es el origen en este frame.
> - Efecto: svc F1 0.74 → 0.76, edge F1 0.25 → 0.48.

# -kA0ahrhX3I
ok, lo que tenemos ahora esta bien pero son solo de un bloque, falta otro bloque de macie  y s3 juntos pero no unidos solo encierran a macie
y otro bloque igual donde ahora encierran a Macie y S3, pero no los unen

> **[Claude, 2026-08-29]** Revisé el frame (es un slide, no pizarra, con marcas amarillas encima). Los tres bloques "AWS Account" y los círculos amarillos están bien transcritos: hay literalmente 3 Macie y 3 S3 en la lámina, y los dos bloques de la derecha no tienen flechas internas. Eso queda como está.
> - **Único cambio: `MySQL` de `RDS` a `ThirdParty`.** Es un recuadro morado con el texto "MySQL" y un símbolo de base de datos — nombre propio de un motor externo, no un ícono de servicio AWS. Mismo criterio que Apache Metron.
> - Efecto: svc F1 0.71 → 0.86, edge F1 0.50 → 0.67.

# -wLEkq21cvA
Haber primero teneoms un icono de ON-PREM, que va conectado a un icono de APP Discovery Service 

este ON-PREM va conectado a EC2 (HOT REPLICa) 

por otro lado en la parte de arriba tenemos un icono de user (MIgration Team) que va a un icono con el logo de la empresa estimo con el nombre SLACK, del SLACK va EC2 de este EC2 va cloudware de aqui va EC2 (Hot Replica) 
de este va a icono dibujado mano de dos filas de 3 cuadros unidos con  el nombreBRAKE AMI 
el Migration Team va a DynamoDB tambien 
y el EC2 va al App Discovery Service 
de aqui hay una linea vertcial entrecortada que separa todo lo anterior, y al lado derecho hay un icono de EC2  y abajo un icono dibujado mano de dos filas de 3 cuadros unidos con  el nombre SHARED AMI abajo 

> **[Claude, 2026-08-29]** Al hacer zoom sobre la zona derecha se ve que **el EC2 del lado derecho y SHARED AMI NO están aislados**: del EC2 central salen 5 líneas, no 3. Dos de ellas cruzan la línea vertical entrecortada — una baja con punta de flecha sobre el EC2 derecho y la otra entra con punta por la izquierda de SHARED AMI. Agregué esas dos aristas.
> - **Dejé `ON-PREM` como `OnPremDC`** (no lo revertí, aunque el GT de este video usa ThirdParty). El ícono es una pila de servidores rotulada "ON-PREM" y `OnPremDC` es la entrada del catálogo que nombra exactamente eso; revertirlo solo para que coincida con este GT sería perseguir la respuesta. **El GT es inconsistente consigo mismo** (usa `OnPremDC` en -3lnf5lzsH0 y `ThirdParty` acá) — eso es techo irreducible y va reportado como tal, no corregido.
> - Dejé `BAKE AMI` / `SHARED AMI` como nodos: tienen ícono dibujado propio (dos filas de 3 cuadros), así que la regla del ícono manda aunque `AMI` casi no exista en el GT (2 nodos en 386 grafos).
> - Registré tu observación de que el EC2 derecho podría ser el mismo que EC2(5), dejando claro en el `rationale` que la imagen no lo confirma.
> - Efecto: svc F1 0.67 (igual), edge F1 0.42 → 0.48.

# 07lfvavMdfU
el stepFunctios va conectado al dynamoDB 
el media convert NO va conectado al DynamoDB 
ahora el dynamoDB sale una flecha a un bloque que dice reach engine que engloba a (EC2, EKS)  
este mini bloque, no crea conexion por flecha entre ellos
revisa en el json que generes que se incluyen estas anotaciones para que el stage 2, vea que posiblemente se equivoco para ver si lo cmabia o no

# 1aYoIZvabbk
haber este esta dificil, lo que yo veo es que el ALB, va al spot, de ese spot va a un circulo de ese circulo sale ms1, ms2, ms3, el EKS sale una flecha que va a ms1, hay un intento de encerrar el eks con el spot, ms1 va al sqs desde ese ms1, va al sns y de ese sns va a sqs, la verdad sin el audio, nose como interpretar lo que veo que pero intentemos agreagar la mayor cantdidad de informacion descriptiva de la imagen

> **[Claude, 2026-08-29]** Corrijo algo que yo mismo te había dicho mal: **SPOT SÍ tiene ícono propio** (cuadrado gris con diana naranja, misma familia visual que el tile del ALB), no es solo texto. Aun así mantuve tu fusión `EKS (SPOT)` en un solo nodo, y la justifico con lo que se ve: los dos íconos están dentro del mismo recuadro verde entrecortado, y **el ícono de EKS no tiene ninguna punta de flecha incidente en este frame** — todas las flechas de la zona entran o salen por SPOT. Dejé la alternativa descartada escrita en el `rationale` por si querés medirla (7 entidades, EKS aislado: svc 0.77 / edge 0.36).
> - El óvalo y los textos M.S.1/2/3 confirmados: **el óvalo está vacío, sin ícono ni etiqueta, y los M.S. son texto manuscrito suelto, sin caja ni ícono.** Por eso no son entidades; sus flechas se registran desde el bloque y quedan descritas literalmente en los `description`.
> - **Revertí `USER` de `UserCompanyDeveloper` a `UserConsumerWeb`.** El ícono es una persona genérica sin ningún atributo de rol; nada en la imagen dice "developer". Ese cambio no tenía base visual y se hizo después de que el GT de este video estuviera a la vista en la sesión. **Esto BAJA el puntaje a propósito: svc F1 1.00 → 0.83, edge F1 0.91 → 0.73.** El 1.00 no era defendible.

# 2L0m28ZLmtE
haber hay bloque de texto que contieene 
SANDFI
SSO
que teiene una flecha bidireccional a cognito 
cognit tiene felcah bidireccional a S3(1) <-> cloudfront <-> User
s3(1) <-> APigateway <-> DynamoDB
s3(1) <-> ServiceCatalog <-> R Studio con simbolo de EC2 
ServiceCatalog <-> Sagemaker 
Lambda <-> translate 
Lambda <-> Comprehend Medical 
un cubo al final separado Data Lake

# 6CgqEzyWpeA
haber del lambda(4) va a sqs(6) y de autoscaling va a SQS(6) no al contrario 
del lambda(4) va dos Sqs qeu estan juntitos uno sobre otro que podria ser el sqs(5) la flecha de 7 a 5 esta bien

# 6EUknQqaV1w
falta (1) a (2) 
del (5) no sale ninguna flecha 
del (1) va al (6) que es el iconito de mensajes y debajo esta el logo 
(2) va al Elsatiserarech que creo q eu esta bien mapeado a openSEarch 
falta la flecha de este elasticSearch al (4)
tambien hay una palabra en shard va a 50M+ (no son nodos pero lo anoto como referencia)

# 6YkguepAQuQ
falta CopePipeline como nodo indiviudal 

hay una conexion de cloudformation como debe ser esta conexiones que son asi, igualmenet pon ese contexto en el json  un bloque de VPC que engloba a  (ECS, IAM , ALB )

# BZ32w0SSAoY
falta conexion de (1) a (2)
fakta conexion de (3) a (1) 
(4) <-> (3)

# wjtSHyENv0I
falta (1) a (0)

# ww5fiygF6eg
un simbolo de drone, que va undio a un third party,
luego hay una line entrecortada vertical que separa, esta seccion con los siguientes 
drone a s3  
de storage gateway a s3 
 de un bloque que tiene (server y database) sale una flecha al storage gateway 
de ese s3 sale una flecha  a este bloque (server database)
a lado de la flecha entrecortada vertcial hya un cloudwatch event que va stepfunctions de aqui va a lambda y de labmda vauna flecha a la seccion izquierda donde esta thirpart y el drone, no hay una felcha explicita que une especificamente a uno

# 2XVgpMwY5iE
User a EKS a Sagemarker a s3 a Eks (con una palabra HDS encima de la flecha)
un simbolo de un hospital que se;ala a s3(2) de s3(2) a EKS 
luego de FSx un cuadorado verde que teiene esa palabra a sagemaker 
luego un IAM a sagemaker

# 7V8wTCkjOqo
primero tenemos serviece teams es el primer icono que esta alado de ECS no presenta ninguna flecha explicita, luego de ECS va lambda que por debajo tieene un x25 como si se estubiera multiplicanod por 25  del lado derecjo t iene RDS PostgreSQL 
Dynamo SB
SNS

lueg en l a parte de aabo tenemos NON-PROD que va unido a PROD, y el NON-PROD sale una flecha a ECS

# 90rWUjKjnAE
primero tenemos una line vertical entrecortada que separa en zona izquierda y derecha, en la parte zquierda tenemos user developer con una flecha hacia git y luego de git a EKS que encima tiene Lagoon y sale una flecha que apunta a esa linea vertical 

del lado izquierdo tenemos EKS que apunta hacia abajo EKS a EC2 a Aurora RAG, luego de EKS a EC2 SPot  y de aqui una flecha hacia EBSGP3 y luego de EC2SPOT anterior va a una flecha EFS

# 9qTEHITVeLE
haber una flecha sale de la nada y va aun rectangulo azul que dice F.E dentro de ese retcangulo azul va EKS  a lado de EKS dice en texto Metamanger (no es un nodo es el nombre del EKS supongo) de este EKs va Elasitic Serarch NEO4J 
Ahora hay un bloque central celeste conlinea enrtecortadas que engloba a S3 datalake (dice encima 60tb) de aqui va EMR de este EMR va de regreso a S3
de ese s3 va Kafka (que encima dice en texto dice 600topies) de aqui vuelve a S3 
fuera de este cuadrado azul sale una felcha hacia simbolo de eC2(VERTicA) , de ses cuardarco azul (el que engloba lo anterior ) va a RDS Luego una linea abajo entrecortada horizontal que separa la parte superior anteriormente mecinoada 
y la parte de abajo: 
primero temo Un simbolo tipo RDS que dice (Multiple Data sources) que tiene flecha en ambas directions de Kafka y otra felca hacia el EKS metamanager 
alaldo derecho tenemos APPliactiosn con un simbolo rodaso que tiene flecha bidireccional hacia EMR 
y luego un sibolo user al ladoa de abajo inferior derecha un user (DA/DS)

# BlCXEMp_lqY
user consumertv a Kinesis de Kinesis Friebase a S3 dei kinesisi  firebase a REDshift y de REdshift a quicksight

# H2fOkeXxpyw
Un user (CLI) a EC2 a Dynamo DB
EC2(1) a SQS 
EC2(2) a SQS
Ec2 (2) a lambda (1)
la linea vertical verde que sepera en dos del la do derecho solo existe un lambda (1)
un user a Ec2(3)[esto va del lado izquierdo] va a lambda (1)

# 2e3vOxsHekE
Haber lo que yo veo es un grifo de agua para bomberos que va hacia el APIgateway --> S3 --> ECS --> Sagemaker 
analyst (sin conexiones afuera)

# Cgv0kfp_6xQ
Haber en este de aqui partamos desde el centro  lo que yo veo es un cuadro enrecortado con nombre W y que dice EKS 


|---[Gw]------|
|EKS          |  
|   (a) (b)   |  
|             |  
|   (c) (d)   |  
|-------------|  
        
te lo puse asi en texto para que entiendas mejor pues que dice, el EKS asi va literal en texto en la parte duperior de l acaja y los nodos reales que tienen un icono (EKS) dentro de la caja son (a), (b), (c), (d)

donde (a) es Media que tieene una flecha de GW hacia ella  y de este sale una flecha hacia el cloudfront y de ahi sale una flecha hacia s3, estan fuera de la caja obviamente

de Gw sale orta flecha hacia (b) que es MCS  y de ese MSC va android 

De ese MCS (b) va a Friendgraph 
de ese MCS (b) va a SNAP DB (c) que de aqui va Dyamo DB 
de ese MCS (b) va a ElasticaCache 

de un icono IOS va al W 

> **[Claude, 2026-08-29]** Confirmado en el frame: **"GW" es una caja rectangular vacía con texto, sin ícono de servicio**, y está apoyada sobre el borde superior del recuadro entrecortado rotulado "EKS". Como no tiene ícono ni nombre de producto, **no se transcribe como entidad**: las flechas que la atraviesan se registran entre los nodos iconificados de cada extremo (IOS → MEDIA y IOS → MCS), y la caja queda descrita en el `rationale` de MEDIA. Respondiendo a tu duda: sí, "GW" es abreviatura habitual de *gateway* en diagramas, pero eso es conocimiento de dominio — bajo la condición ciega solo podés registrar que hay una caja rotulada GW, y por eso no se convierte en un `ApiGateway`.
> - Los 4 microservicios (MEDIA, MCS, FRIEND GRAPH, SNAP DB) sí tienen ícono naranja de Kubernetes/EKS cada uno, así que los 4 nodos `EKS` están bien.
> - Anoté también las marcas manuscritas en rojo "900+EKS" y "1000+" que no estaban registradas.
> - Efecto: svc F1 0.92 → **1.00**, edge F1 0.58 → 0.78.

# FfSNnH2bbNc

de un satelite dibujado a mano va a EC2 SPOT que va a S# que teinee una flecha bidireccional a AWS Fargate Que teine una flecha bidireccional a User 
Del AWS Fargate tiene un felcha bidreccional Elasticache 

Ec2 Spot tiene una flecha a RDS de ahi una flecha bidireccional a AWS Fargate 

del icono lambda tiene una flecha bidirecional haciar RDS (la verdad no logro visualizar bein si la flecha tiene direccion unica de lambda a a RDS o bidireccional, asi que quede anotado como verificar con transquicion del video)
me falto la ocnexion de lambda a S3 que es bidireccional 
ok Elastica Cache solo tiene conexion  