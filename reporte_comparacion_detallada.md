# Reporte de Comparación Detallada: Arquitecturas AWS

Este reporte compara los gráficos generados por el pipeline **Gemini Parsimonious** y el **Standard Vision Pipeline** contra el **Ground Truth** manual.

| Video ID | Título | F1 Parsimonious | F1 Standard | Diagnóstico / Observaciones |
|---|---|---|---|---|
| `07lfvavMdfU` | Levels Beyond: Digital Content Orchestration | **100%** | 95.2% | Parsimonious supera a Standard por 4.8%. El clásico alucina nodos por ruidos de la transcripción. |
| `6YkguepAQuQ` | Aetion: Deploy Applications  Provision Cloud Resources with AWS Developer Tools | **100%** | 94.7% | Parsimonious supera a Standard por 5.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `6iK4WNj6QqI` | Ticketmaster: Active-Active Multi-Region Checkout for Ticket Purchases | **77%** | N/A | Comparación no disponible. |
| `8TExnSvZqt0` | AxiomSL's RegCloud®️: Secure & Scalable Risk & Regulatory Reporting on AWS | **100%** | 100.0% | Rendimiento equivalente en detección de servicios. |
| `AzM_d7ZvzUE` | Epsagon: Automatically Tracing and Analyzing Billions of AWS Serverless Events | **88%** | 94.1% | Standard supera a Parsimonious por 6.1%. El simplificado omitió detalles menores. |
| `BlCXEMp_lqY` | Vizio: Smart TV Analytics at Scale | **100%** | 100.0% | Rendimiento equivalente en detección de servicios. |
| `Cgv0kfp_6xQ` | Snap: Journey of a Snap on Snapchat Using AWS | **100%** | 100.0% | Rendimiento equivalente en detección de servicios. |
| `IV3KuMGVNXI` | Deep Instinct: Collecting RT Statistics and Applying RT Decisions with Lambda@Edge | **N/A** | 100.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `JYeXbUdFOdw` | Noventiq: Harnessing Search and Analytics with Event-Driven Architecture on Amazon OpenSearch | **80%** | N/A | Comparación no disponible. |
| `Kebb0LOVC28` | Openfit: ChatOps with Slack and AWS Lambda | **N/A** | 100.0% | Omitido en la evaluación del pipeline Parsimonious. |
| `bqZWYmRAka0` | DBS Bank: Architecting Quant Pricing Engine for Performance with Amazon ElastiCache | **80%** | N/A | Comparación no disponible. |
| `c-1GXhOOOww` | Anchor Operating System: Building a Serverless Guest Sightseeing Journey Seamlessly | **78%** | N/A | Comparación no disponible. |
| `fppIOuRMI2g` | Instructure: Elevating Digital Education to the Next-Level Event Driven CI/CD Deployments Globally | **100%** | N/A | Comparación no disponible. |
| `gu54VVeDD10` | FPL Technologies: Building On-Demand, Secure, and Scalable Serverless ML Workbenches | **80%** | N/A | Comparación no disponible. |
| `jBffL9zUCSE` | The New York Times: Giving Developers the Freedom to Deploy, While Governing Cloud Services at Scale | **100%** | N/A | Comparación no disponible. |
| `lkDq9g43djw` | FINBOURNE: How Finbourne Assures Resiliency Through Chaos Engineering Events Every 17 min | **100%** | N/A | Comparación no disponible. |
| `pk5yddJpC_8` | Benevity: Centralized Logging for Multiple Compute Classes Using OpenSearch | **83%** | N/A | Comparación no disponible. |
| `qi017F1UwvM` | Salesflo: Transforming Field-Force Operations Using Event-Driven Architecture | **93%** | N/A | Comparación no disponible. |
| `rPGLNw1cOGM` | 3M: Parallel Serverless Workflows for Materials Science | **83%** | N/A | Comparación no disponible. |
| `unFVfqj9cQ8` | Contino: Measuring and Communicating The Business Impact of Landing Zones with Flight Controller | **93%** | N/A | Comparación no disponible. |
| `-3lnf5lzsH0` | MakeMyTrip: Building Next Generation SOC | **74%** | 95.7% | Standard supera a Parsimonious por 21.7%. El simplificado omitió detalles menores. |
| `4WjXH8Wp0E4` | Kainos: Kainos Advances Patient Care with Next Generation Interoperability Platform | **78%** | 94.7% | Standard supera a Parsimonious por 16.7%. El simplificado omitió detalles menores. |
| `7LziNjUTo7w` | IHS Markit: Virtual Instructor-Led Trainings with IHS Markit (now part of S&P Global) | **94%** | 94.1% | Standard supera a Parsimonious por 0.1%. El simplificado omitió detalles menores. |
| `-S-R7MWRpaI` | mimik: Hybrid Edge Cloud Leveraging AWS to Support Edge Microservice Mesh | **71%** | 71.4% | Standard supera a Parsimonious por 0.4%. El simplificado omitió detalles menores. |
| `-ahWdCysMYw` | Summit Technology Group: Building a Data Consumption Model for Multi-Tenant Applications | **80%** | 93.3% | Standard supera a Parsimonious por 13.3%. El simplificado omitió detalles menores. |
| `-kA0ahrhX3I` | Oportun: Increasing the Accuracy of SensitiveData Discovery Using Amazon Macie | **86%** | 85.7% | Parsimonious supera a Standard por 0.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `-wLEkq21cvA` | Versent: The Migration Factory | **67%** | 72.7% | Standard supera a Parsimonious por 5.7%. El simplificado omitió detalles menores. |
| `-yCol_7qH2U` | Experian: Self-Service MLOps Platform for Financial Services Customers | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `0-db3wFRfSc` | MyHeritage: Handling the Deep Nostalgia Virality, Scaling GPU Spot Instances Using Multi-Region | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `0F7KDLz-kIQ` | Zigbang: A Hybrid API of Serverless and ECS, Infra as a Code via CDK | **87%** | 81.8% | Parsimonious supera a Standard por 5.2%. El clásico alucina nodos por ruidos de la transcripción. |
| `0JxJpNjI9Y0` | The Washington Post: Building a Content Management Platform with Speed at its Core | **80%** | 75.0% | Parsimonious supera a Standard por 5.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `0gNMEyei-co` | Infor: Ingest and Analyze Millions of Application Events Daily for Compliance Violations | **82%** | 84.2% | Standard supera a Parsimonious por 2.2%. El simplificado omitió detalles menores. |
| `0wnNlOg42dc` | Spyne.AI: High-Quality Product Visuals at Scale with AI on AWS | **89%** | 77.8% | Parsimonious supera a Standard por 11.2%. El clásico alucina nodos por ruidos de la transcripción. |
| `1aYoIZvabbk` | OLX Autos: Building Developer Platform for Rapid Global Expansion | **92%** | 92.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `1kWxymroGeE` | OutSystems: Decomposing a Data Monolith for Scale and MultiTenancy | **91%** | 90.9% | Parsimonious supera a Standard por 0.1%. El clásico alucina nodos por ruidos de la transcripción. |
| `1xLjtJnfZes` | MATTR: Building Digital Trust at Scale | **80%** | 80.0% | Rendimiento equivalente en detección de servicios. |
| `2L0m28ZLmtE` | Sanofi with TeamWork: OnDemand Data Science Environment | **96%** | 88.0% | Parsimonious supera a Standard por 8.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `2XVgpMwY5iE` | Keen Eye: Building Deep Learning Models for Digital Pathology Image Analysis | **71%** | 71.4% | Standard supera a Parsimonious por 0.4%. El simplificado omitió detalles menores. |
| `2e3vOxsHekE` | Mueller Water Products: A Water Intelligent Platform | **83%** | 83.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `2f_NYiPJQt4` | Appway: Securing Sensitive Banking Workflows with Isolated Architecture on AWS | **95%** | 78.3% | Parsimonious supera a Standard por 16.7%. El clásico alucina nodos por ruidos de la transcripción. |
| `37T7Nd8pL-c` | Docebo: How to Create Compelling e-Learning Videos from Documents via AI ML Services | **86%** | 85.7% | Parsimonious supera a Standard por 0.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `3WgTBTDlQN8` | FanFight: Building a Realtime Fantasy League Gaming Platform on AWS | **71%** | 70.6% | Parsimonious supera a Standard por 0.4%. El clásico alucina nodos por ruidos de la transcripción. |
| `3yJZ6rPoZfg` | Hexagon HxDR: Cloud-Based Visualization of Spatial Data | **50%** | 50.0% | Rendimiento equivalente en detección de servicios. |
| `4-teOQ_dJvY` | SBB Cargo: Data Collection and Processing with Serverless Analytics Services | **71%** | 57.1% | Parsimonious supera a Standard por 13.9%. El clásico alucina nodos por ruidos de la transcripción. |
| `53sUjFv9ByI` | Neumora Therapeutics: Enabling DNA and RNA Data Insight for Rapid Genomics Sequencing Drug Discovery | **67%** | 61.5% | Parsimonious supera a Standard por 5.5%. El clásico alucina nodos por ruidos de la transcripción. |
| `5CwIt-Alqhg` | Accenture: Building a Blockchain Circular Supply Chain | **100%** | 72.7% | Parsimonious supera a Standard por 27.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `5EmA67lSJEs` | Extreme Reach: The AdBridge Platform on AWS Handles 80%+ of all Commercials in the US | **80%** | 80.0% | Rendimiento equivalente en detección de servicios. |
| `5RsZJ-1_sn4` | Glidewell Dental: Precision Manufacturing in Dental Restorations using a Tailored Scalable Solution | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `5f3z1Z_9BJA` | Capgemini: Refactoring a Data Warehouse to Amazon Redshift | **86%** | 80.0% | Parsimonious supera a Standard por 6.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `5vR5aN_xdI0` | Splunk: Data at Scale by Decoupling Compute and Storage LIVE | **92%** | 76.9% | Parsimonious supera a Standard por 15.1%. El clásico alucina nodos por ruidos de la transcripción. |
| `62E9ggjGS8I` | DISH Network: Building a Self-Service Portal to Create Multiple Accounts at Scale | **100%** | 66.7% | Parsimonious supera a Standard por 33.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `6EUknQqaV1w` | CloudHealth by VMware: Secure State. Manages Over 50M Assets from Billions of Events on AWS | **86%** | 93.3% | Standard supera a Parsimonious por 7.3%. El simplificado omitió detalles menores. |
| `6E_Dg3YRil4` | Avnet: Accelerating OEM's with IoT and AI | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `6LcSv9XocTY` | Intuit: Serving 7 Million Customers Using Amazon Connect | **82%** | 76.2% | Parsimonious supera a Standard por 5.8%. El clásico alucina nodos por ruidos de la transcripción. |
| `6sY0AunanlM` | NGINX: Deploy and Scale Applications with Ease Using AWS EKS, ECS and the NGINX Ingress Controller | **89%** | 66.7% | Parsimonious supera a Standard por 22.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `6uEX5RKd0Bk` | Grindr: Leveraging Dynamo and Aurora to Build an Enhanced Chat System | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `7KqYdneuJjo` | Health eCareers: Using Generative AI to reinvent the Job Search Experience | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `7V8wTCkjOqo` | NAB: Automating Cloud Governance at the National Australia Bank | **83%** | 76.9% | Parsimonious supera a Standard por 6.1%. El clásico alucina nodos por ruidos de la transcripción. |
| `7wBOFcP1HwA` | Seera Group: Transforming Online Travel Booking with Microservices (Arabic) | **74%** | 77.8% | Standard supera a Parsimonious por 3.8%. El simplificado omitió detalles menores. |
| `8ZRWzn0G39g` | Replicon: Multi-Tenant SaaS Solution with Bring Your Own Key (BYOK) Encryption for Enterprises | **71%** | N/A | Comparación no disponible. |
| `8s0wGRkiDrw` | Mobilewalla: S3 Access Monitoring Using ML | **89%** | 80.0% | Parsimonious supera a Standard por 9.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `9-6hQdFeolc` | Lyniate: Scaling Healthcare Data Exchange At Scale with Tenant Isolation | **67%** | N/A | Comparación no disponible. |
| `9-a9Y5THTYo` | Vitesco Technologies Cloud Foundation: A Scalable and Automated Cloud Landing Zone | **77%** | 71.4% | Parsimonious supera a Standard por 5.6%. El clásico alucina nodos por ruidos de la transcripción. |
| `90rWUjKjnAE` | amazee.io: Kubernetes Deployments Made Easy | **100%** | 85.7% | Parsimonious supera a Standard por 14.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `99nNHsbwBpg` | SkyScanner: Building HighlyAvailable MultiRegion Kubernetes Clusters on 100 Amazon EC2 Spot | **100%** | 57.1% | Parsimonious supera a Standard por 42.9%. El clásico alucina nodos por ruidos de la transcripción. |
| `9Cg81Xgg7LQ` | Pushpay Holdings Ltd.: Strangling a Monolithic Application While Moving to Microservices on AWS | **100%** | N/A | Comparación no disponible. |
| `9qTEHITVeLE` | Majid Al Futtaim: Building a Custom Data Management Solution on AWS | **71%** | 70.6% | Parsimonious supera a Standard por 0.4%. El clásico alucina nodos por ruidos de la transcripción. |
| `9yziTe6lBwk` | Ânima Educação: Digitizing Student Experience for Colleges in Brazil | **90%** | 90.0% | Rendimiento equivalente en detección de servicios. |
| `A4Lfk1Zz1dE` | Spot.io: Optimizing Cloud Infrastructure Through Secure Cost Aware Automation | **92%** | 92.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `AS2JeM2FUzE` | Intellect Design Arena: Insurance Risk Assessment with Intellect FABRIC Data Services | **89%** | 82.4% | Parsimonious supera a Standard por 6.6%. El clásico alucina nodos por ruidos de la transcripción. |
| `BPvr0qWpJlA` | ContactSuite: Automated Omni-Channel Service Desk Workflow | **63%** | 73.7% | Standard supera a Parsimonious por 10.7%. El simplificado omitió detalles menores. |
| `BX1K8x1lVLc` | Love, Bonito: Achieving Scalability Using Magento with Kubernetes | **100%** | 87.5% | Parsimonious supera a Standard por 12.5%. El clásico alucina nodos por ruidos de la transcripción. |
| `BZ32w0SSAoY` | PixelStrings by Cinnafilm: A Flexible & Scalable Platform for Video Audio Optimization & Conversion | **80%** | 80.0% | Rendimiento equivalente en detección de servicios. |
| `BgT_bDAejSQ` | GoDaddy: Empowering Agility with ZeroTrust Environment Best Practices | **29%** | 20.0% | Parsimonious supera a Standard por 9.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `CDCLwX2fo2g` | Ztore: Building a Recommendation System on AWS (Cantonese) | **86%** | 71.4% | Parsimonious supera a Standard por 14.6%. El clásico alucina nodos por ruidos de la transcripción. |
| `CTG23wd9H74` | 3M: Building an HPC Modeling Platform to Simplify AWS Usage for Scientists and Engineers | **74%** | 77.8% | Standard supera a Parsimonious por 3.8%. El simplificado omitió detalles menores. |
| `Ccutfm_Srzw` | Zulily: A Compelling Suggestive Search Experience Using Amazon DocumentDB with MongoDB Compatibility | **86%** | 85.7% | Parsimonious supera a Standard por 0.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `Cw26CrJUqv8` | Salesforce: Automating SaaS Application Connectivity | **74%** | 88.9% | Standard supera a Parsimonious por 14.9%. El simplificado omitió detalles menores. |
| `D6rG9eZ5Qus` | Graham Media Group: Modernizing Traditional Broadcasting with AWS | **78%** | 70.0% | Parsimonious supera a Standard por 8.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `D77FSUkPJ3o` | Avio Aero, a GE Aviation Business: Serverless Application to Manage Expense Purchase Approvals | **86%** | 80.0% | Parsimonious supera a Standard por 6.0%. El clásico alucina nodos por ruidos de la transcripción. |
| `D9qTotVJYss` | HBO Max: Using Canaries for Outside-in Validation | **77%** | 83.3% | Standard supera a Parsimonious por 6.3%. El simplificado omitió detalles menores. |
| `DAJZAygxDZA` | BASF Digital Farming: Productionizing ML with a Cross-Account Model Deployment Solution | **73%** | 61.5% | Parsimonious supera a Standard por 11.5%. El clásico alucina nodos por ruidos de la transcripción. |
| `Dp3YAxFp-YM` | Alef Education: Building an Adaptive Learning System for K12 Students using AWS | **94%** | 82.4% | Parsimonious supera a Standard por 11.6%. El clásico alucina nodos por ruidos de la transcripción. |
| `GoziWpmFCS0` | iRobot: Serverless Data Cataloging for Data Scientists | **75%** | 85.7% | Standard supera a Parsimonious por 10.7%. El simplificado omitió detalles menores. |
| `Q6r_QbYXFpg` | SynchroNet: Extending User Automation and Amazon WorkSpaces Provisioning with AWS Step Functions | **100%** | 94.7% | Parsimonious supera a Standard por 5.3%. El clásico alucina nodos por ruidos de la transcripción. |
| `QM96Fv_NAnw` | INT: Seismic Data Visualization Platform Designed for Cloud | **92%** | 92.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `QOtCpD23118` | LeasePlan: Leverages Serverless to Increase Driver Safety Reduce Fleet Costs and Lower Risk | **75%** | 75.0% | Rendimiento equivalente en detección de servicios. |
| `QnmmTIYZxNI` | Adobe: Simplifying Networking Across Thousands of AWS Accounts with AWS Transit Gateway LIVE | **100%** | 100.0% | Rendimiento equivalente en detección de servicios. |
| `QnwfcDZkwh8` | Mediaset: Achieving an Omni-Channel Broadcasting Voting System Near Realtime at Scale | **78%** | 78.3% | Standard supera a Parsimonious por 0.3%. El simplificado omitió detalles menores. |
| `UPV6ggX4eSE` | Mission Cloud: Building a Generative AI Content Translation Pipeline Using Amazon Bedrock | **N/A** | N/A | Omitido en la evaluación del pipeline Parsimonious. |
| `bikXzsVihF4` | United Airlines: How to Use AWS Backup to Protect Data from Ransomware Events | **93%** | N/A | Comparación no disponible. |