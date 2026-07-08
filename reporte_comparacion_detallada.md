# Reporte de Comparación Detallada: Arquitecturas AWS

Este reporte compara los gráficos generados por el pipeline **Gemini Parsimonious** y el **Standard Vision Pipeline** contra el **Ground Truth** manual.

## Evaluación Core (Ground Truths Válidos)

| Video ID | Título | F1 Parsimonious | F1 Standard | Diagnóstico / Observaciones |
|---|---|---|---|---|
| `-3lnf5lzsH0` | MakeMyTrip: Building Next Generation SOC | **74%** | 95.7% | Standard supera a Parsimonious por 21.7%. El simplificado omitió detalles menores. |
| `-kA0ahrhX3I` | Oportun: Increasing the Accuracy of SensitiveData Discovery Using Amazon Macie | **86%** | 85.7% | Parsimonious supera a Standard por 0.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `-wLEkq21cvA` | Versent: The Migration Factory | **100%** | 90.9% | Parsimonious supera a Standard por 9.1%. El clásico alucina nodos por ruidos de la transcripción. |
| `07lfvavMdfU` | Levels Beyond: Digital Content Orchestration | **100%** | 95.2% | Parsimonious supera a Standard por 4.8%. El clásico alucina nodos por ruidos de la transcripción. |
| `0F7KDLz-kIQ` | Zigbang: A Hybrid API of Serverless and ECS, Infra as a Code via CDK | **87%** | 81.8% | Parsimonious supera a Standard por 5.2%. El clásico alucina nodos por ruidos de la transcripción. |
| `1aYoIZvabbk` | OLX Autos: Building Developer Platform for Rapid Global Expansion | **92%** | 92.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `1xLjtJnfZes` | MATTR: Building Digital Trust at Scale | **80%** | 80.0% | Rendimiento equivalente en detección de servicios. |
| `2L0m28ZLmtE` | Sanofi with TeamWork: OnDemand Data Science Environment | **96%** | 88.0% | Parsimonious supera a Standard por 8.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `2XVgpMwY5iE` | Keen Eye: Building Deep Learning Models for Digital Pathology Image Analysis | **71%** | 71.4% | Standard supera a Parsimonious por 0.4%. El simplificado omitió detalles menores. |
| `2e3vOxsHekE` | Mueller Water Products: A Water Intelligent Platform | **83%** | 83.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `3BGPEFFCpvk` | Video 3BGPEFFCpvk | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `3WgTBTDlQN8` | FanFight: Building a Realtime Fantasy League Gaming Platform on AWS | **71%** | 70.6% | Parsimonious supera a Standard por 0.4%. El clásico alucina nodos por ruidos de la transcripción. |
| `3yJZ6rPoZfg` | Hexagon HxDR: Cloud-Based Visualization of Spatial Data | **50%** | 50.0% | Rendimiento equivalente en detección de servicios. |
| `4-teOQ_dJvY` | SBB Cargo: Data Collection and Processing with Serverless Analytics Services | **71%** | 57.1% | Parsimonious supera a Standard por 13.9%. El clásico alucina nodos por ruidos de la transcripción. |
| `5EmA67lSJEs` | Extreme Reach: The AdBridge Platform on AWS Handles 80%+ of all Commercials in the US | **80%** | 80.0% | Rendimiento equivalente en detección de servicios. |
| `5f3z1Z_9BJA` | Capgemini: Refactoring a Data Warehouse to Amazon Redshift | **86%** | 80.0% | Parsimonious supera a Standard por 6.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `5vR5aN_xdI0` | Splunk: Data at Scale by Decoupling Compute and Storage LIVE | **92%** | 76.9% | Parsimonious supera a Standard por 15.1%. El clásico alucina nodos por ruidos de la transcripción. |
| `6EUknQqaV1w` | CloudHealth by VMware: Secure State. Manages Over 50M Assets from Billions of Events on AWS | **86%** | 93.3% | Standard supera a Parsimonious por 7.3%. El simplificado omitió detalles menores. |
| `6LcSv9XocTY` | Intuit: Serving 7 Million Customers Using Amazon Connect | **82%** | 76.2% | Parsimonious supera a Standard por 5.8%. El clásico alucina nodos por ruidos de la transcripción. |
| `6YkguepAQuQ` | Aetion: Deploy Applications  Provision Cloud Resources with AWS Developer Tools | **100%** | 94.7% | Parsimonious supera a Standard por 5.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `6iK4WNj6QqI` | Ticketmaster: Active-Active Multi-Region Checkout for Ticket Purchases | **77%** | N/A | Comparación no disponible. |
| `7wBOFcP1HwA` | Seera Group: Transforming Online Travel Booking with Microservices (Arabic) | **74%** | 77.8% | Standard supera a Parsimonious por 3.8%. El simplificado omitió detalles menores. |
| `8ZRWzn0G39g` | Replicon: Multi-Tenant SaaS Solution with Bring Your Own Key (BYOK) Encryption for Enterprises | **71%** | N/A | Comparación no disponible. |
| `9Cg81Xgg7LQ` | Pushpay Holdings Ltd.: Strangling a Monolithic Application While Moving to Microservices on AWS | **100%** | N/A | Comparación no disponible. |
| `AS2JeM2FUzE` | Intellect Design Arena: Insurance Risk Assessment with Intellect FABRIC Data Services | **89%** | 82.4% | Parsimonious supera a Standard por 6.6%. El clásico alucina nodos por ruidos de la transcripción. |
| `BPvr0qWpJlA` | ContactSuite: Automated Omni-Channel Service Desk Workflow | **63%** | 73.7% | Standard supera a Parsimonious por 10.7%. El simplificado omitió detalles menores. |
| `Cgv0kfp_6xQ` | Snap: Journey of a Snap on Snapchat Using AWS | **100%** | 100.0% | Rendimiento equivalente en detección de servicios. |
| `D6rG9eZ5Qus` | Graham Media Group: Modernizing Traditional Broadcasting with AWS | **78%** | 70.0% | Parsimonious supera a Standard por 8.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `D9qTotVJYss` | HBO Max: Using Canaries for Outside-in Validation | **77%** | 83.3% | Standard supera a Parsimonious por 6.3%. El simplificado omitió detalles menores. |
| `DAJZAygxDZA` | BASF Digital Farming: Productionizing ML with a Cross-Account Model Deployment Solution | **73%** | 61.5% | Parsimonious supera a Standard por 11.5%. El clásico alucina nodos por ruidos de la transcripción. |
| `Felt-hOU6kU` | Xero: Building a Scalable Self-Service Portal for Thousands of Developers Provisioning Resources | **N/A** | 92.3% | Omitido en la evaluación del pipeline Parsimonious. |
| `FqCs3BD6qvo` | Video FqCs3BD6qvo | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `G07keU4g-LU` | Jubilant FoodWorks: Driving a Quality Customer Experience Using Data Lake | **N/A** | 70.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `GJ1So_pbZWk` | Taysols: Next Best Offer Recommendation System using Amazon SageMaker | **N/A** | 77.8% | Omitido en la evaluación del pipeline Parsimonious. |
| `H_S7CxtHgSM` | Raiffeisen Bank International: Automated Integration of OnPremises Key Management with AWS KMS | **N/A** | 82.4% | Omitido en la evaluación del pipeline Parsimonious. |
| `INog0_9tCtY` | Threat Stack: Proactive Risk Identification and Real-time Threat Detection across AWS | **N/A** | 72.7% | Omitido en la evaluación del pipeline Parsimonious. |
| `JYeXbUdFOdw` | Noventiq: Harnessing Search and Analytics with Event-Driven Architecture on Amazon OpenSearch | **80%** | N/A | Comparación no disponible. |
| `JiWHomdh1oI` | Datacoral: Using Serverless to Create Data Pipelines | **N/A** | 80.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `Jkx6kVbDpL4` | Nielsen: Processing 55TB of Data Per Day with AWS Lambda | **N/A** | 76.9% | Omitido en la evaluación del pipeline Parsimonious. |
| `Kebb0LOVC28` | Openfit: ChatOps with Slack and AWS Lambda | **N/A** | 100.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `KywvGM6HVXI` | Capillary Technologies: Building an OmniChannel Data Ingestion Platform | **N/A** | 63.2% | Omitido en la evaluación del pipeline Parsimonious. |
| `KzJKdUZ3Ba4` | PwC: Streamlining Asset Tracking with Amazon Managed Blockchain | **N/A** | 75.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `LYP98nPBj2A` | Singtel: Next-Generation Mobile Financial Services Platform on AWS and Amazon Aurora PostgreSQL | **N/A** | 53.3% | Omitido en la evaluación del pipeline Parsimonious. |
| `LxeSC3-xMlk` | St. Louis University: Using Amazon Lex to Answer Students' Questions Through Alexa and a Mobile App | **N/A** | 77.8% | Omitido en la evaluación del pipeline Parsimonious. |
| `Ly_UhX3LCCs` | AWS Solutions: Simple and Secure Media Exchange on AWS | **N/A** | 88.9% | Omitido en la evaluación del pipeline Parsimonious. |
| `M_hqigB9C4I` | Innovaccer: Deriving Insights from Healthcare Data to Empower Care Teams | **N/A** | 70.6% | Omitido en la evaluación del pipeline Parsimonious. |
| `MbkLJ62jtMc` | Mueller Water Products: Scalable Ingestion of Sensor Data for Municipal Water Conservation LIVE | **N/A** | 66.7% | Omitido en la evaluación del pipeline Parsimonious. |
| `NfUwtK8ALtw` | MX Player: Achieving Massive Scalability Using Amazon EKS with Spot Instances | **N/A** | 85.7% | Omitido en la evaluación del pipeline Parsimonious. |
| `OQKOHNtyz3E` | Vodafone NZ: Data Driven Omni Channel Contact Center via Automation and Continuous Improvement | **N/A** | 84.2% | Omitido en la evaluación del pipeline Parsimonious. |
| `OWLGK-eVrTw` | Heimdall Data: Query Caching Without Code Changes | **N/A** | 76.9% | Omitido en la evaluación del pipeline Parsimonious. |
| `Pc7_uOdlGKo` | Panasonic Avionics: Weather Data and ML Models Improve In-Flight Entertainment Customer Satisfaction | **N/A** | 87.5% | Omitido en la evaluación del pipeline Parsimonious. |
| `PgeQufaQy7I` | MindTickle: Building a Secure, Automated, Multi-Region Architecture on AWS | **N/A** | 80.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `QOtCpD23118` | LeasePlan: Leverages Serverless to Increase Driver Safety Reduce Fleet Costs and Lower Risk | **75%** | 75.0% | Rendimiento equivalente en detección de servicios. |
| `Yju3yReAQtc` | Fortinet Uses AWS Serverless to Provide a Highly Available ControlPlane for their FortiWeb CloudWAF | **N/A** | 80.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `bikXzsVihF4` | United Airlines: How to Use AWS Backup to Protect Data from Ransomware Events | **93%** | N/A | Comparación no disponible. |
| `fppIOuRMI2g` | Instructure: Elevating Digital Education to the Next-Level Event Driven CI/CD Deployments Globally | **100%** | N/A | Comparación no disponible. |
| `gpWR5JBC64A` | FoodHub: Enabling Massive Scale Order Processing with Serverless Architecture | **N/A** | 75.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `jBffL9zUCSE` | The New York Times: Giving Developers the Freedom to Deploy, While Governing Cloud Services at Scale | **100%** | N/A | Comparación no disponible. |
| `lkDq9g43djw` | FINBOURNE: How Finbourne Assures Resiliency Through Chaos Engineering Events Every 17 min | **100%** | N/A | Comparación no disponible. |
| `pk5yddJpC_8` | Benevity: Centralized Logging for Multiple Compute Classes Using OpenSearch | **83%** | N/A | Comparación no disponible. |
| `qi017F1UwvM` | Salesflo: Transforming Field-Force Operations Using Event-Driven Architecture | **93%** | N/A | Comparación no disponible. |
| `rPGLNw1cOGM` | 3M: Parallel Serverless Workflows for Materials Science | **83%** | N/A | Comparación no disponible. |
| `unFVfqj9cQ8` | Contino: Measuring and Communicating The Business Impact of Landing Zones with Flight Controller | **93%** | N/A | Comparación no disponible. |
| `wjtSHyENv0I` | Main Street America Insurance: The Independent Agent Portal, Breaking up the Monolith | **N/A** | 85.7% | Omitido en la evaluación del pipeline Parsimonious. |

## Validación / Excluidos (Ground Truths Inválidos o Sin Ground Truth)

| Video ID | Título | F1 Parsimonious | F1 Standard | Diagnóstico / Observaciones |
|---|---|---|---|---|
| `-yCol_7qH2U` | Experian: Self-Service MLOps Platform for Financial Services Customers | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `0-db3wFRfSc` | MyHeritage: Handling the Deep Nostalgia Virality, Scaling GPU Spot Instances Using Multi-Region | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `62E9ggjGS8I` | DISH Network: Building a Self-Service Portal to Create Multiple Accounts at Scale | **100%** | 66.7% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `6E_Dg3YRil4` | Avnet: Accelerating OEM's with IoT and AI | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `6uEX5RKd0Bk` | Grindr: Leveraging Dynamo and Aurora to Build an Enhanced Chat System | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `7KqYdneuJjo` | Health eCareers: Using Generative AI to reinvent the Job Search Experience | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `8TExnSvZqt0` | AxiomSL's RegCloud®️: Secure & Scalable Risk & Regulatory Reporting on AWS | **100%** | 100.0% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `99nNHsbwBpg` | SkyScanner: Building HighlyAvailable MultiRegion Kubernetes Clusters on 100 Amazon EC2 Spot | **100%** | 57.1% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `BgT_bDAejSQ` | GoDaddy: Empowering Agility with ZeroTrust Environment Best Practices | **29%** | 20.0% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `GoziWpmFCS0` | iRobot: Serverless Data Cataloging for Data Scientists | **75%** | 85.7% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `K5ww_O4vsxo` | Samsung Cloud: Global Hybrid Network Optimization Across 5 AWS Regions Using AWS Transit Gateway | **N/A** | 66.7% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `OTPyxlTjWp0` | Experian: Scalable and Flexible Machine Learning Batch Transformation | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `QnmmTIYZxNI` | Adobe: Simplifying Networking Across Thousands of AWS Accounts with AWS Transit Gateway LIVE | **100%** | 100.0% | Excluido de evaluación: Ground Truth marcado como inválido/incompleto. |
| `UPV6ggX4eSE` | Mission Cloud: Building a Generative AI Content Translation Pipeline Using Amazon Bedrock | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `W4QzOaKCX2Y` | Vercara UltraDNS Analytics & Operations: Petabyte-Scale Data on Amazon S3 and Amazon Athena | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `_cca2eNePC4` | Infinitium: Low Latency Fraud Detection System with Amazon Neptune Graph Database | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `cczJb4heExQ` | First Orion: Improved Operational Efficiency with Response Times Leveraging Amazon Q | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `npQWtmnuM6s` | Swyftx: Building Automated, Secure, and Attestable Pipelines from Engineers to Production | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `s4eerNhXf84` | Aqua Security: Enabling Real Time Blocking, Scalability, and High Availability in Containers | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `t8JCvcnFX10` | Age of Learning: Highly Scalable Continuous Integration Platform with Amazon EKS and Amazon EC2-Spot | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `vQgUkn3rAMY` | AssemblyAI: Building a Scalable Machine Learning Platform for Voice Data Transcription and Analysis | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
| `ym_Gz_zH7w8` | Peloton: Improved Customer Satisfaction and Engagement Powered by Real-Time Recommendations | **N/A** | N/A | Solo validación: No existe Ground Truth manual. |
