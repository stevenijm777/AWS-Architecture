# Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-26 10:59:20*

## 1. Executive Summary

**Videos evaluated:** 54

| Metric | Precision | Recall | F1 |
|--------|-----------|--------|----|
| **Services (unique set)** | 76.4% | 84.5% | 79.4% |
| **Services (multiset)** | 73.8% | 82.8% | 77.1% |
| **Edges (service pairs)** | 44.6% | 54.9% | 47.5% |

**Edge type accuracy (data/meta):** 78.6%

**Average node count ratio (gen/gt):** 1.20x

**Average workflows:** gen=2.6 vs gt=3.2

## 2. Service F1 Score Distribution

| Range | Count | Percentage |
|-------|-------|------------|
| 🟢 Excellent (≥90%) | 13 | 24.1% |
| 🟡 Good (70-89%) | 36 | 66.7% |
| 🟠 Fair (50-69%) | 4 | 7.4% |
| 🔴 Poor (<50%) | 1 | 1.9% |

## 3. Per-Video Results (sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `iKYvG5aiIn8` | 100% | 100% | 100% | 100% | 100% | 100% | 12 | 12 | 12 | 12 | — | — |
| 2 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 3 | `07lfvavMdfU` | 91% | 100% | 95% | 60% | 64% | 62% | 11 | 10 | 15 | 14 | — | Lambda |
| 4 | `4WjXH8Wp0E4` | 100% | 90% | 95% | 59% | 59% | 59% | 11 | 14 | 22 | 22 | UserConsumerWeb | — |
| 5 | `7LziNjUTo7w` | 89% | 100% | 94% | 87% | 81% | 84% | 9 | 9 | 15 | 16 | — | UserCompanyDeveloper |
| 6 | `AzM_d7ZvzUE` | 89% | 100% | 94% | 76% | 65% | 70% | 12 | 11 | 17 | 20 | — | UserCompanyDeveloper |
| 7 | `-ahWdCysMYw` | 100% | 88% | 93% | 56% | 56% | 56% | 7 | 8 | 9 | 9 | VPN | — |
| 8 | `ww5fiygF6eg` | 88% | 100% | 93% | 75% | 90% | 82% | 12 | 10 | 24 | 20 | — | UserCompanyAgent |
| 9 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 10 | `A4Lfk1Zz1dE` | 86% | 100% | 92% | 40% | 80% | 53% | 9 | 8 | 10 | 5 | — | UserCompanyDeveloper |
| 11 | `BlCXEMp_lqY` | 86% | 100% | 92% | 78% | 78% | 78% | 7 | 6 | 9 | 9 | — | UserCompanyAnalyst |
| 12 | `1kWxymroGeE` | 83% | 100% | 91% | 31% | 100% | 47% | 6 | 5 | 13 | 4 | — | UserCompanyInternalPlatform |
| 13 | `6YkguepAQuQ` | 90% | 90% | 90% | 15% | 20% | 17% | 10 | 10 | 13 | 10 | VPC | UserCompanyAgent |
| 14 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 15 | `BX1K8x1lVLc` | 88% | 88% | 88% | 60% | 64% | 62% | 8 | 8 | 15 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 16 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 17 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 18 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 19 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 20 | `Cgv0kfp_6xQ` | 83% | 83% | 83% | 53% | 64% | 58% | 10 | 10 | 17 | 14 | UserConsumerMobile | UserConsumerWebMobile |
| 21 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 22 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 23 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 24 | `8s0wGRkiDrw` | 67% | 100% | 80% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | UserCompanyAnalyst, UserConsumerWeb |
| 25 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 26 | `6EUknQqaV1w` | 75% | 86% | 80% | 13% | 18% | 15% | 12 | 9 | 15 | 11 | KinesisDataStream | EKS, Kinesis |
| 27 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 28 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 29 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 30 | `8TExnSvZqt0` | 75% | 82% | 78% | 0% | 0% | 0% | 12 | 11 | 11 | 0 | AMI, AWSConfig | EC2, ThirdParty, UserCompanyInternalPlatform |
| 31 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 32 | `Cw26CrJUqv8` | 78% | 78% | 78% | 23% | 33% | 27% | 9 | 10 | 13 | 9 | PrivateLink, UserConsumerWeb | UserCompanyDeveloper, VPC |
| 33 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 34 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 35 | `5vR5aN_xdI0` | 83% | 71% | 77% | 25% | 40% | 31% | 9 | 9 | 16 | 10 | ThirdParty, UserConsumerAPI | UserCompanyAPI |
| 36 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 37 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 38 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 39 | `5EmA67lSJEs` | 75% | 75% | 75% | 38% | 25% | 30% | 9 | 11 | 13 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAPI, UserCompanyAgent |
| 40 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 41 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 42 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 43 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 44 | `-S-R7MWRpaI` | 71% | 71% | 71% | 36% | 36% | 36% | 9 | 8 | 11 | 11 | Firehose, UserConsumerMobile | UserCompanyAnalyst, UserCompanyEdge |
| 45 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 46 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 47 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 48 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 49 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 50 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 51 | `53sUjFv9ByI` | 57% | 67% | 62% | 50% | 50% | 50% | 7 | 6 | 6 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 52 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 53 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 54 | `BgT_bDAejSQ` | 12% | 100% | 22% | 8% | 100% | 15% | 11 | 2 | 12 | 1 | — | DirectConnect, ELB, ThirdParty (+4) |

## 4. Most Frequently Missing Services (False Negatives)

Services present in ground truth but NOT in generated graphs.

| Service | Times Missed | Capability |
|---------|-------------|------------|
| UserConsumerWeb | 10 | User |
| ThirdParty | 7 | ThirdParty |
| UserCompanyDataStream | 6 | User |
| UserConsumerMobile | 5 | User |
| UserCompanyAgent | 4 | User |
| UserConsumerAPI | 4 | User |
| ALB | 3 | networking |
| VPC | 3 | networking |
| UserConsumerEdge | 2 | User |
| EC2 | 2 | compute |
| UserCompanyAPI | 2 | User |
| OnPremDC | 1 | OnPremDC |
| Firehose | 1 | integration |
| VPN | 1 | networking |
| Fargate | 1 | compute |
| S2SVPN | 1 | networking |
| Kinesis | 1 | integration |
| UserCompanyEdge | 1 | User |
| S3 | 1 | storage |
| SageMaker | 1 | compute |

## 5. Most Frequently Hallucinated Services (False Positives)

Services in generated graphs but NOT in ground truth.

| Service | Times Hallucinated | Capability |
|---------|-------------------|------------|
| UserCompanyDeveloper | 11 | User |
| UserConsumerWebMobile | 10 | User |
| UserCompanyAnalyst | 8 | User |
| ThirdParty | 8 | ThirdParty |
| EC2 | 6 | compute |
| UserCompanyAgent | 6 | User |
| UserCompanyInternalPlatform | 5 | User |
| Lambda | 4 | compute |
| UserCompanyAPI | 4 | User |
| ELB | 4 | networking |
| UserCompanyDomainExpert | 3 | User |
| RDS | 3 | storage |
| UserConsumerWeb | 3 | User |
| UserConsumerIOT | 2 | User |
| EKS | 2 | compute |
| Kinesis | 2 | integration |
| VPC | 2 | networking |
| UserCompanyEdge | 1 | User |
| OnPremDC | 1 | OnPremDC |
| ECS | 1 | compute |

## 6. Most Frequently Missing Edges

| Edge (src → tgt) | Times Missed |
|------------------|-------------|
| CloudFront→UserConsumerWeb | 5 |
| EC2→S3 | 5 |
| EC2→ThirdParty | 4 |
| UserConsumerMobile→EKS | 4 |
| S3→EC2 | 4 |
| UserConsumerWeb→CloudFront | 4 |
| DynamoDB→EKS | 3 |
| S3→ECS | 3 |
| Lambda→Kinesis | 3 |
| Kinesis→Lambda | 3 |
| DynamoDB→Lambda | 3 |
| UserConsumerWeb→ThirdParty | 3 |
| S3→Firehose | 3 |
| S3→Lambda | 3 |
| EKS→UserConsumerMobile | 2 |

## 7. Most Frequently Hallucinated Edges

| Edge (src → tgt) | Times Hallucinated |
|------------------|--------------------|
| Lambda→S3 | 8 |
| CloudFront→UserConsumerWebMobile | 7 |
| EC2→S3 | 7 |
| EKS→EC2 | 6 |
| UserConsumerWebMobile→CloudFront | 6 |
| EKS→DynamoDB | 5 |
| EC2→EC2 | 4 |
| Lambda→DynamoDB | 4 |
| ThirdParty→ThirdParty | 4 |
| Lambda→EC2 | 4 |
| SQS→EC2 | 3 |
| UserCompanyAnalyst→QuickSight | 3 |
| EC2→UserConsumerWeb | 3 |
| ApiGateway→CloudFront | 3 |
| ELB→ECS | 3 |

## 8. Performance by Service Capability

| Capability | GT Count | Correct | Missed | Hallucinated | Recall |
|------------|----------|---------|--------|--------------|--------|
| OnPremDC | 1 | 0 | 1 | 1 | 0.0% |
| ThirdParty | 20 | 13 | 7 | 8 | 65.0% |
| User | 55 | 18 | 37 | 57 | 32.7% |
| compute | 109 | 105 | 4 | 13 | 96.3% |
| control | 35 | 33 | 2 | 4 | 94.3% |
| integration | 36 | 33 | 3 | 5 | 91.7% |
| networking | 48 | 39 | 9 | 10 | 81.2% |
| other | 17 | 17 | 0 | 4 | 100.0% |
| storage | 88 | 87 | 1 | 4 | 98.9% |

## 9. Performance by Functional Goal Category

| Category | # Videos | Avg Svc F1 | Avg Edge F1 |
|----------|----------|------------|-------------|
| compute_intensive | 7 | 77.5% | 51.0% |
| control | 9 | 77.3% | 41.6% |
| data_ingestion | 22 | 81.3% | 54.1% |
| interactive | 21 | 80.4% | 51.7% |
| other | 4 | 74.9% | 19.9% |

## 10. Bottom 10 Worst Performing Videos

### `BgT_bDAejSQ` — Svc F1: 22%, Edge F1: 15%

- **Title (GT):** GoDaddy: Empowering Agility with ZeroTrust Environment Best Practices
- **Nodes:** gen=11 vs gt=2
- **Edges:** gen=12 vs gt=1
- **Hallucinated services:** DirectConnect, ELB, ThirdParty, UserCompanyDeveloper, UserConsumerWebMobile, VPC, WAF
- **Hallucinated edges:** UserCompanyDeveloper→ThirdParty, ThirdParty→UserCompanyDeveloper, VPC→DirectConnect, VPC→EKS, EKS→VPC

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
