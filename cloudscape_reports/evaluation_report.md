# Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-27 18:50:47*

## 1. Executive Summary

**Videos evaluated:** 56

| Metric | Precision | Recall | F1 |
|--------|-----------|--------|----|
| **Services (unique set)** | 77.9% | 85.5% | 80.6% |
| **Services (multiset)** | 75.4% | 84.2% | 78.6% |
| **Edges (service pairs)** | 48.9% | 53.7% | 49.8% |

**Edge type accuracy (data/meta):** 77.6%

**Average node count ratio (gen/gt):** 1.21x

**Average workflows:** gen=2.7 vs gt=3.1

## 2. Service F1 Score Distribution

| Range | Count | Percentage |
|-------|-------|------------|
| 🟢 Excellent (≥90%) | 15 | 26.8% |
| 🟡 Good (70-89%) | 36 | 64.3% |
| 🟠 Fair (50-69%) | 4 | 7.1% |
| 🔴 Poor (<50%) | 1 | 1.8% |

## 3. Per-Video Results (sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 9 | 0 | — | — |
| 2 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 3 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 77% | 71% | 74% | 10 | 10 | 13 | 14 | — | — |
| 4 | `iKYvG5aiIn8` | 100% | 100% | 100% | 100% | 100% | 100% | 12 | 12 | 12 | 12 | — | — |
| 5 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 6 | `07lfvavMdfU` | 91% | 100% | 95% | 71% | 71% | 71% | 12 | 10 | 14 | 14 | — | Lambda |
| 7 | `4WjXH8Wp0E4` | 100% | 90% | 95% | 59% | 59% | 59% | 11 | 14 | 22 | 22 | UserConsumerWeb | — |
| 8 | `6YkguepAQuQ` | 100% | 90% | 95% | 38% | 30% | 33% | 9 | 10 | 8 | 10 | VPC | — |
| 9 | `7LziNjUTo7w` | 89% | 100% | 94% | 92% | 69% | 79% | 9 | 9 | 12 | 16 | — | UserCompanyAgent |
| 10 | `AzM_d7ZvzUE` | 89% | 100% | 94% | 76% | 65% | 70% | 12 | 11 | 17 | 20 | — | UserCompanyDeveloper |
| 11 | `-ahWdCysMYw` | 100% | 88% | 93% | 56% | 56% | 56% | 7 | 8 | 9 | 9 | VPN | — |
| 12 | `6EUknQqaV1w` | 88% | 100% | 93% | 77% | 91% | 83% | 11 | 9 | 13 | 11 | — | SES |
| 13 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 14 | `A4Lfk1Zz1dE` | 86% | 100% | 92% | 40% | 80% | 53% | 9 | 8 | 10 | 5 | — | UserCompanyDeveloper |
| 15 | `1kWxymroGeE` | 83% | 100% | 91% | 50% | 100% | 67% | 6 | 5 | 8 | 4 | — | EC2 |
| 16 | `Cw26CrJUqv8` | 89% | 89% | 89% | 80% | 89% | 84% | 10 | 10 | 10 | 9 | UserConsumerWeb | UserCompanyDeveloper |
| 17 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 18 | `BX1K8x1lVLc` | 88% | 88% | 88% | 60% | 64% | 62% | 8 | 8 | 15 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 19 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 20 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 21 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 22 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 23 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 24 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 25 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 26 | `1ZLiRT0C2Yo` | 67% | 100% | 80% | 0% | 0% | 0% | 9 | 6 | 8 | 0 | — | OnPremDC, UserCompanyDeveloper, UserConsumerMobile |
| 27 | `8s0wGRkiDrw` | 67% | 100% | 80% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | UserCompanyAnalyst, UserConsumerWeb |
| 28 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 29 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 30 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 31 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 32 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 33 | `ww5fiygF6eg` | 75% | 86% | 80% | 69% | 45% | 55% | 11 | 10 | 13 | 20 | UserCompanyDrone | OnPremDC, UserCompanyAgent |
| 34 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 35 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 36 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 37 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 38 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 39 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 40 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 41 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 42 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 43 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 44 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 45 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 46 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 36% | 42% | 9 | 8 | 8 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 47 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 48 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 49 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 50 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 51 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 52 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 53 | `53sUjFv9ByI` | 57% | 67% | 62% | 50% | 50% | 50% | 7 | 6 | 6 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 54 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 55 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 56 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |

## 4. Most Frequently Missing Services (False Negatives)

Services present in ground truth but NOT in generated graphs.

| Service | Times Missed | Capability |
|---------|-------------|------------|
| UserConsumerWeb | 10 | User |
| UserCompanyDataStream | 7 | User |
| ThirdParty | 7 | ThirdParty |
| UserConsumerAPI | 5 | User |
| UserConsumerMobile | 4 | User |
| UserCompanyAgent | 4 | User |
| ALB | 3 | networking |
| VPC | 3 | networking |
| Kinesis | 2 | integration |
| UserConsumerEdge | 2 | User |
| EC2 | 2 | compute |
| UserCompanyAPI | 2 | User |
| OnPremDC | 1 | OnPremDC |
| VPN | 1 | networking |
| Fargate | 1 | compute |
| S2SVPN | 1 | networking |
| UserCompanyEdge | 1 | User |
| S3 | 1 | storage |
| SageMaker | 1 | compute |
| UserCompanyCRM | 1 | User |

## 5. Most Frequently Hallucinated Services (False Positives)

Services in generated graphs but NOT in ground truth.

| Service | Times Hallucinated | Capability |
|---------|-------------------|------------|
| UserCompanyDeveloper | 11 | User |
| UserConsumerWebMobile | 8 | User |
| ThirdParty | 7 | ThirdParty |
| EC2 | 6 | compute |
| UserCompanyAnalyst | 6 | User |
| UserCompanyAgent | 6 | User |
| OnPremDC | 4 | OnPremDC |
| Lambda | 4 | compute |
| UserConsumerWeb | 4 | User |
| UserCompanyDomainExpert | 3 | User |
| ELB | 3 | networking |
| RDS | 3 | storage |
| UserConsumerMobile | 3 | User |
| UserCompanyInternalPlatform | 3 | User |
| KinesisDataStream | 2 | integration |
| UserCompanyAPI | 2 | User |
| UserConsumerIOT | 2 | User |
| SES | 2 | other |
| UserCompanyEdge | 1 | User |
| ECS | 1 | compute |

## 6. Most Frequently Missing Edges

| Edge (src → tgt) | Times Missed |
|------------------|-------------|
| CloudFront→UserConsumerWeb | 5 |
| EC2→S3 | 5 |
| EC2→ThirdParty | 4 |
| S3→EC2 | 4 |
| UserConsumerWeb→CloudFront | 4 |
| UserConsumerMobile→EKS | 3 |
| S3→ECS | 3 |
| Lambda→Kinesis | 3 |
| Kinesis→Lambda | 3 |
| DynamoDB→Lambda | 3 |
| UserConsumerWeb→ThirdParty | 3 |
| S3→Firehose | 3 |
| S3→Lambda | 3 |
| S3→ThirdParty | 2 |
| DynamoDB→EKS | 2 |

## 7. Most Frequently Hallucinated Edges

| Edge (src → tgt) | Times Hallucinated |
|------------------|--------------------|
| Lambda→S3 | 8 |
| EC2→S3 | 7 |
| CloudFront→UserConsumerWebMobile | 6 |
| UserConsumerWebMobile→CloudFront | 5 |
| EKS→EC2 | 5 |
| EC2→EC2 | 4 |
| Lambda→DynamoDB | 4 |
| Lambda→EC2 | 4 |
| SQS→EC2 | 3 |
| UserCompanyDeveloper→ThirdParty | 3 |
| EC2→DynamoDB | 3 |
| ApiGateway→CloudFront | 3 |
| ELB→ECS | 3 |
| EC2→RDS | 3 |
| ApiGateway→Lambda | 3 |

## 8. Performance by Service Capability

| Capability | GT Count | Correct | Missed | Hallucinated | Recall |
|------------|----------|---------|--------|--------------|--------|
| OnPremDC | 1 | 0 | 1 | 4 | 0.0% |
| ThirdParty | 21 | 14 | 7 | 7 | 66.7% |
| User | 57 | 18 | 39 | 53 | 31.6% |
| compute | 111 | 107 | 4 | 12 | 96.4% |
| control | 37 | 37 | 0 | 4 | 100.0% |
| integration | 36 | 34 | 2 | 5 | 94.4% |
| networking | 53 | 45 | 8 | 9 | 84.9% |
| other | 17 | 17 | 0 | 5 | 100.0% |
| storage | 90 | 89 | 1 | 4 | 98.9% |

## 9. Performance by Functional Goal Category

| Category | # Videos | Avg Svc F1 | Avg Edge F1 |
|----------|----------|------------|-------------|
| compute_intensive | 7 | 78.2% | 53.0% |
| control | 10 | 77.8% | 39.5% |
| data_ingestion | 22 | 81.7% | 57.2% |
| interactive | 22 | 80.7% | 51.9% |
| other | 4 | 83.1% | 34.1% |

## 10. Bottom 10 Worst Performing Videos

### `BgT_bDAejSQ` — Svc F1: 20%, Edge F1: 0%

- **Title (GT):** GoDaddy: Empowering Agility with ZeroTrust Environment Best Practices
- **Nodes:** gen=12 vs gt=2
- **Edges:** gen=9 vs gt=1
- **Hallucinated services:** ALB, DirectConnect, NAT, OnPremDC, ThirdParty, UserCompanyDeveloper, UserConsumerWeb, WAF
- **Missing edges:** EKS→EKS
- **Hallucinated edges:** UserCompanyDeveloper→ThirdParty, EKS→NAT, EKS→DirectConnect, DirectConnect→OnPremDC, UserConsumerWeb→WAF

### `3yJZ6rPoZfg` — Svc F1: 50%, Edge F1: 33%

- **Title (GT):** Hexagon HxDR: Cloud-Based Visualization of Spatial Data
- **Nodes:** gen=8 vs gt=7
- **Edges:** gen=9 vs gt=9
- **Missing services:** EC2, UserConsumerEdge, VPC
- **Hallucinated services:** AutoScaling, UserConsumerWebMobile, VPCPeering
- **Missing edges:** EKS→VPC, EKS→EC2, VPC→EKS, EC2→S3, S3→UserConsumerEdge
- **Hallucinated edges:** UserConsumerWebMobile→S3, EKS→VPCPeering, VPCPeering→EKS, EKS→SQS, SQS→AutoScaling

### `4-teOQ_dJvY` — Svc F1: 57%, Edge F1: 40%

- **Title (GT):** SBB Cargo: Data Collection and Processing with Serverless Analytics Services
- **Nodes:** gen=9 vs gt=9
- **Edges:** gen=12 vs gt=13
- **Missing services:** Kinesis, UserCompanyAPI, UserCompanyEdge
- **Hallucinated services:** KinesisDataStream, ThirdParty, UserCompanyInternalPlatform
- **Missing edges:** UserCompanyEdge→Lambda, Lambda→Kinesis, Kinesis→KinesisAnalytics, Kinesis→Lambda, KinesisAnalytics→Kinesis
- **Hallucinated edges:** ThirdParty→Lambda, Lambda→KinesisDataStream, KinesisDataStream→KinesisAnalytics, KinesisAnalytics→KinesisDataStream, KinesisDataStream→Lambda

### `53sUjFv9ByI` — Svc F1: 62%, Edge F1: 50%

- **Title (GT):** Neumora Therapeutics: Enabling DNA and RNA Data Insight for Rapid Genomics Sequencing Drug Discovery
- **Nodes:** gen=7 vs gt=6
- **Edges:** gen=6 vs gt=6
- **Missing services:** ThirdParty, UserCompanyDataStream
- **Hallucinated services:** S3, UserCompanyAnalyst, UserCompanyDeveloper
- **Missing edges:** EC2→ECR, EKS→ThirdParty, UserCompanyDataStream→EC2
- **Hallucinated edges:** UserCompanyDeveloper→EC2, EKS→S3, S3→UserCompanyAnalyst

### `62E9ggjGS8I` — Svc F1: 67%, Edge F1: 19%

- **Title (GT):** DISH Network: Building a Self-Service Portal to Create Multiple Accounts at Scale
- **Nodes:** gen=9 vs gt=7
- **Edges:** gen=12 vs gt=9
- **Missing services:** VPC
- **Hallucinated services:** EC2, EKS, Lambda, RDS
- **Missing edges:** ThirdParty→UserCompanyDeveloper, ControlTower→ThirdParty, ServiceCatalog→VPC, TransitGateway→VPC, TransitGateway→TransitGateway
- **Hallucinated edges:** UserCompanyDeveloper→ServiceCatalog, ControlTower→ServiceCatalog, ServiceCatalog→Lambda, ServiceCatalog→EC2, ServiceCatalog→EKS

### `D6rG9eZ5Qus` — Svc F1: 70%, Edge F1: 53%

- **Title (GT):** Graham Media Group: Modernizing Traditional Broadcasting with AWS
- **Nodes:** gen=11 vs gt=9
- **Edges:** gen=10 vs gt=9
- **Missing services:** ThirdParty, UserCompanyDataStream
- **Hallucinated services:** Lambda, SystemsManager, UserCompanyElementalLiveDevice, UserConsumerWebMobile
- **Missing edges:** UserCompanyDataStream→MediaStore, MediaPackage→Transcribe, Rekognition→S3, ThirdParty→UserCompanyDataStream
- **Hallucinated edges:** UserCompanyElementalLiveDevice→MediaStore, CloudFront→UserConsumerWebMobile, S3→Transcribe, SystemsManager→UserCompanyElementalLiveDevice, Lambda→SystemsManager

### `3WgTBTDlQN8` — Svc F1: 71%, Edge F1: 43%

- **Title (GT):** FanFight: Building a Realtime Fantasy League Gaming Platform on AWS
- **Nodes:** gen=11 vs gt=9
- **Edges:** gen=14 vs gt=14
- **Missing services:** EC2, UserCompanyAPI, UserConsumerMobile
- **Hallucinated services:** ThirdParty, UserConsumerWebMobile
- **Missing edges:** UserConsumerMobile→ApiGateway, ApiGateway→UserConsumerMobile, Lambda→EC2, EC2→Lambda, EC2→S3
- **Hallucinated edges:** UserConsumerWebMobile→ApiGateway, ApiGateway→UserConsumerWebMobile, Lambda→ThirdParty, ThirdParty→Lambda, Lambda→S3

### `CDCLwX2fo2g` — Svc F1: 71%, Edge F1: 62%

- **Title (GT):** Ztore: Building a Recommendation System on AWS (Cantonese)
- **Nodes:** gen=7 vs gt=8
- **Edges:** gen=12 vs gt=14
- **Missing services:** ALB, UserConsumerMobile
- **Hallucinated services:** ELB, UserConsumerWeb
- **Missing edges:** ALB→ECS, ALB→UserConsumerMobile, ECS→ALB, DynamoDB→EC2, S3→ECS
- **Hallucinated edges:** UserConsumerWeb→ELB, ELB→ECS, ELB→UserConsumerWeb, ECS→ELB

### `9-a9Y5THTYo` — Svc F1: 71%, Edge F1: 67%

- **Title (GT):** Vitesco Technologies Cloud Foundation: A Scalable and Automated Cloud Landing Zone
- **Nodes:** gen=9 vs gt=7
- **Edges:** gen=9 vs gt=6
- **Missing services:** UserConsumerWeb
- **Hallucinated services:** CodePipeline, Organizations, UserCompanyDeveloper
- **Missing edges:** UserConsumerWeb→ApiGateway
- **Hallucinated edges:** UserCompanyDeveloper→ApiGateway, StepFunctions→Organizations, SES→UserCompanyDeveloper, CodePipeline→Organizations

### `2XVgpMwY5iE` — Svc F1: 71%, Edge F1: 38%

- **Title (GT):** Keen Eye: Building Deep Learning Models for Digital Pathology Image Analysis
- **Nodes:** gen=8 vs gt=7
- **Edges:** gen=14 vs gt=12
- **Missing services:** UserCompanyAgent, UserCompanyDataStream
- **Hallucinated services:** UserCompanyDomainExpert, UserConsumerHospital
- **Missing edges:** UserCompanyDataStream→S3, UserCompanyAgent→EKS, EKS→S3, EKS→UserCompanyAgent, FSX→SageMaker
- **Hallucinated edges:** UserConsumerHospital→S3, UserConsumerHospital→EKS, UserCompanyDomainExpert→EKS, S3→SageMaker, EKS→UserCompanyDomainExpert
