# Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-23 20:32:19*

## 1. Executive Summary

**Videos evaluated:** 63

| Metric | Precision | Recall | F1 |
|--------|-----------|--------|----|
| **Services (unique set)** | 74.4% | 81.4% | 76.8% |
| **Services (multiset)** | 71.3% | 79.8% | 74.2% |
| **Edges (service pairs)** | 39.3% | 49.1% | 42.2% |

**Edge type accuracy (data/meta):** 74.2%

**Average node count ratio (gen/gt):** 1.18x

**Average workflows:** gen=2.7 vs gt=3.3

## 2. Service F1 Score Distribution

| Range | Count | Percentage |
|-------|-------|------------|
| 🟢 Excellent (≥90%) | 12 | 19.0% |
| 🟡 Good (70-89%) | 39 | 61.9% |
| 🟠 Fair (50-69%) | 9 | 14.3% |
| 🔴 Poor (<50%) | 3 | 4.8% |

## 3. Per-Video Results (sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `6CgqEzyWpeA` | 100% | 100% | 100% | 79% | 79% | 79% | 13 | 12 | 19 | 19 | — | — |
| 2 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 77% | 71% | 74% | 11 | 10 | 13 | 14 | — | — |
| 3 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 4 | `07lfvavMdfU` | 91% | 100% | 95% | 60% | 64% | 62% | 11 | 10 | 15 | 14 | — | Lambda |
| 5 | `4WjXH8Wp0E4` | 100% | 90% | 95% | 59% | 59% | 59% | 11 | 14 | 22 | 22 | UserConsumerWeb | — |
| 6 | `7LziNjUTo7w` | 89% | 100% | 94% | 87% | 81% | 84% | 9 | 9 | 15 | 16 | — | UserCompanyDeveloper |
| 7 | `AzM_d7ZvzUE` | 89% | 100% | 94% | 76% | 65% | 70% | 12 | 11 | 17 | 20 | — | UserCompanyDeveloper |
| 8 | `-ahWdCysMYw` | 100% | 88% | 93% | 56% | 56% | 56% | 7 | 8 | 9 | 9 | VPN | — |
| 9 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 10 | `A4Lfk1Zz1dE` | 86% | 100% | 92% | 40% | 80% | 53% | 9 | 8 | 10 | 5 | — | UserCompanyDeveloper |
| 11 | `BlCXEMp_lqY` | 86% | 100% | 92% | 78% | 78% | 78% | 7 | 6 | 9 | 9 | — | UserCompanyAnalyst |
| 12 | `6YkguepAQuQ` | 90% | 90% | 90% | 15% | 20% | 17% | 10 | 10 | 13 | 10 | VPC | UserCompanyAgent |
| 13 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 14 | `BX1K8x1lVLc` | 88% | 88% | 88% | 60% | 64% | 62% | 8 | 8 | 15 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 15 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 16 | `6sew_hdI6cY` | 80% | 92% | 86% | 43% | 50% | 46% | 17 | 15 | 21 | 18 | OpenSearch | ThirdParty, UserCompanyDeveloper, UserConsumerWebMobile |
| 17 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 18 | `ww5fiygF6eg` | 86% | 86% | 86% | 76% | 80% | 78% | 11 | 10 | 21 | 20 | UserCompanyDrone | UserCompanyInternalPlatform |
| 19 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 20 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 21 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 22 | `1kWxymroGeE` | 71% | 100% | 83% | 0% | 0% | 0% | 7 | 5 | 10 | 4 | — | EKS, UserCompanyDeveloper |
| 23 | `CE03UMddoYU` | 78% | 88% | 82% | 47% | 67% | 55% | 11 | 10 | 17 | 12 | UserConsumerEdge | UserConsumerIOT, UserConsumerWebMobile |
| 24 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 25 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 26 | `1ZLiRT0C2Yo` | 67% | 100% | 80% | 0% | 0% | 0% | 11 | 6 | 19 | 0 | — | ThirdParty, UserCompanyDeveloper, UserConsumerWebMobile |
| 27 | `1SwHH7qQ6Pc` | 75% | 86% | 80% | 26% | 38% | 31% | 11 | 10 | 19 | 13 | UserConsumerMobile | UserCompanyAgent, UserCompanyInternalPlatform |
| 28 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 29 | `6EUknQqaV1w` | 75% | 86% | 80% | 13% | 18% | 15% | 12 | 9 | 15 | 11 | KinesisDataStream | EKS, Kinesis |
| 30 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 31 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 32 | `8TExnSvZqt0` | 75% | 82% | 78% | 0% | 0% | 0% | 12 | 11 | 11 | 0 | AMI, AWSConfig | EC2, ThirdParty, UserCompanyInternalPlatform |
| 33 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 34 | `Cw26CrJUqv8` | 78% | 78% | 78% | 23% | 33% | 27% | 9 | 10 | 13 | 9 | PrivateLink, UserConsumerWeb | UserCompanyDeveloper, VPC |
| 35 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 36 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 37 | `5vR5aN_xdI0` | 83% | 71% | 77% | 25% | 40% | 31% | 9 | 9 | 16 | 10 | ThirdParty, UserConsumerAPI | UserCompanyAPI |
| 38 | `66fPHLmvikk` | 71% | 83% | 77% | 21% | 38% | 27% | 9 | 7 | 14 | 8 | UserCompanyAnalyst | ECS, UserCompanyDeveloper |
| 39 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 40 | `1VcpCVe3tLQ` | 73% | 80% | 76% | 31% | 62% | 41% | 15 | 12 | 26 | 13 | UserCompanyDataStream, UserConsumerMobile | UserCompanyAnalyst, UserCompanyDomainExpert, UserCompanyInternalPlatform |
| 41 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 42 | `9LhiUsg3knw` | 80% | 73% | 76% | 27% | 50% | 35% | 10 | 13 | 15 | 8 | CouchBase, UserCompanyDomainExpert, UserConsumerArtist | ThirdParty, UserCompanyInternalPlatform |
| 43 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 44 | `5EmA67lSJEs` | 75% | 75% | 75% | 38% | 25% | 30% | 9 | 11 | 13 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAPI, UserCompanyAgent |
| 45 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 46 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 47 | `-S-R7MWRpaI` | 71% | 71% | 71% | 36% | 36% | 36% | 9 | 8 | 11 | 11 | Firehose, UserConsumerMobile | UserCompanyAnalyst, UserCompanyEdge |
| 48 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 49 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 50 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 51 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 52 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 53 | `3yJZ6rPoZfg` | 67% | 67% | 67% | 50% | 56% | 53% | 7 | 7 | 10 | 9 | UserConsumerEdge, VPC | ECR, UserConsumerWebMobile |
| 54 | `Yju3yReAQtc` | 62% | 71% | 67% | 22% | 57% | 32% | 13 | 7 | 18 | 7 | OpenSearch, UserCompanyInternalPlatform | EC2, ThirdParty, UserCompanyDeveloper |
| 55 | `BPvr0qWpJlA` | 60% | 67% | 63% | 13% | 22% | 17% | 10 | 10 | 15 | 9 | UserCompanyCRM, UserCompanyDataStream, UserConsumerMobile | EC2, SES, ThirdParty (+1) |
| 56 | `4-teOQ_dJvY` | 67% | 57% | 62% | 44% | 54% | 48% | 13 | 9 | 16 | 13 | KinesisAnalytics, UserCompanyAPI, UserCompanyEdge | UserCompanyInternalPlatform, UserConsumerIOT |
| 57 | `53sUjFv9ByI` | 57% | 67% | 62% | 27% | 50% | 35% | 7 | 6 | 11 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 58 | `-wLEkq21cvA` | 60% | 60% | 60% | 25% | 30% | 27% | 8 | 9 | 12 | 10 | AppDiscovery, UserCompanyAgent | UserCompanyAnalyst, UserCompanyEdge |
| 59 | `8s0wGRkiDrw` | 50% | 75% | 60% | 29% | 50% | 36% | 7 | 5 | 7 | 4 | OpenSearch | ThirdParty, UserCompanyAPI, UserCompanyAgent |
| 60 | `D6rG9eZ5Qus` | 55% | 67% | 60% | 33% | 44% | 38% | 11 | 9 | 12 | 9 | CloudFront, ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyAnalyst (+2) |
| 61 | `1xLjtJnfZes` | 67% | 25% | 36% | 0% | 0% | 0% | 3 | 8 | 3 | 6 | AutoScaling, ELB, ShieldAdvanced (+3) | UserCompanyAPI |
| 62 | `BgT_bDAejSQ` | 12% | 100% | 22% | 8% | 100% | 15% | 11 | 2 | 12 | 1 | — | DirectConnect, ELB, ThirdParty (+4) |
| 63 | `7dtomip_VXc` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 8 | 0 | 11 | ALB, Aurora, AutoScaling (+5) | — |

## 4. Most Frequently Missing Services (False Negatives)

Services present in ground truth but NOT in generated graphs.

| Service | Times Missed | Capability |
|---------|-------------|------------|
| UserConsumerWeb | 10 | User |
| UserConsumerMobile | 8 | User |
| UserCompanyDataStream | 8 | User |
| ThirdParty | 8 | ThirdParty |
| UserConsumerAPI | 5 | User |
| UserCompanyAgent | 4 | User |
| ALB | 4 | networking |
| UserConsumerEdge | 3 | User |
| VPC | 3 | networking |
| OpenSearch | 3 | compute |
| AutoScaling | 2 | control |
| UserCompanyAPI | 2 | User |
| UserCompanyAnalyst | 2 | User |
| OnPremDC | 1 | OnPremDC |
| Firehose | 1 | integration |
| VPN | 1 | networking |
| AppDiscovery | 1 | other |
| Fargate | 1 | compute |
| ELB | 1 | networking |
| ShieldAdvanced | 1 | networking |

## 5. Most Frequently Hallucinated Services (False Positives)

Services in generated graphs but NOT in ground truth.

| Service | Times Hallucinated | Capability |
|---------|-------------------|------------|
| UserCompanyDeveloper | 15 | User |
| UserConsumerWebMobile | 13 | User |
| ThirdParty | 12 | ThirdParty |
| UserCompanyAnalyst | 10 | User |
| UserCompanyInternalPlatform | 8 | User |
| UserCompanyAgent | 7 | User |
| UserCompanyAPI | 6 | User |
| EC2 | 6 | compute |
| Lambda | 4 | compute |
| UserCompanyDomainExpert | 4 | User |
| ELB | 4 | networking |
| UserConsumerIOT | 4 | User |
| RDS | 3 | storage |
| EKS | 3 | compute |
| UserCompanyEdge | 2 | User |
| ECS | 2 | compute |
| Kinesis | 2 | integration |
| VPC | 2 | networking |
| Glue | 1 | integration |
| CloudFormation | 1 | control |

## 6. Most Frequently Missing Edges

| Edge (src → tgt) | Times Missed |
|------------------|-------------|
| CloudFront→UserConsumerWeb | 5 |
| S3→EC2 | 5 |
| EC2→ThirdParty | 4 |
| DynamoDB→Lambda | 4 |
| S3→S3 | 4 |
| EC2→S3 | 4 |
| UserConsumerWeb→CloudFront | 4 |
| DynamoDB→EKS | 3 |
| UserConsumerMobile→EKS | 3 |
| ThirdParty→EC2 | 3 |
| S3→ECS | 3 |
| ElastiCache→ECS | 3 |
| ALB→ECS | 3 |
| ECS→ALB | 3 |
| UserConsumerWeb→ThirdParty | 3 |

## 7. Most Frequently Hallucinated Edges

| Edge (src → tgt) | Times Hallucinated |
|------------------|--------------------|
| Lambda→ApiGateway | 9 |
| Lambda→S3 | 8 |
| EKS→EC2 | 7 |
| EC2→S3 | 7 |
| EC2→ThirdParty | 6 |
| Lambda→DynamoDB | 6 |
| CloudFront→UserConsumerWebMobile | 6 |
| Lambda→EC2 | 6 |
| UserConsumerWebMobile→CloudFront | 5 |
| EC2→CloudWatch | 5 |
| UserCompanyDeveloper→ApiGateway | 5 |
| Kinesis→Kinesis | 5 |
| EC2→EC2 | 4 |
| Glue→S3 | 4 |
| ApiGateway→Lambda | 4 |

## 8. Performance by Service Capability

| Capability | GT Count | Correct | Missed | Hallucinated | Recall |
|------------|----------|---------|--------|--------------|--------|
| OnPremDC | 1 | 0 | 1 | 0 | 0.0% |
| Partner | 1 | 0 | 1 | 0 | 0.0% |
| ThirdParty | 22 | 14 | 8 | 12 | 63.6% |
| User | 65 | 17 | 48 | 74 | 26.2% |
| compute | 132 | 123 | 9 | 15 | 93.2% |
| control | 41 | 36 | 5 | 3 | 87.8% |
| integration | 37 | 35 | 2 | 4 | 94.6% |
| networking | 63 | 50 | 13 | 9 | 79.4% |
| other | 17 | 16 | 1 | 5 | 94.1% |
| storage | 108 | 105 | 3 | 4 | 97.2% |

## 9. Performance by Functional Goal Category

| Category | # Videos | Avg Svc F1 | Avg Edge F1 |
|----------|----------|------------|-------------|
| compute_intensive | 9 | 79.0% | 47.9% |
| control | 12 | 76.0% | 30.5% |
| data_ingestion | 24 | 79.2% | 48.6% |
| interactive | 26 | 75.2% | 46.6% |
| other | 5 | 77.1% | 25.2% |

## 10. Bottom 10 Worst Performing Videos

### `7dtomip_VXc` — Svc F1: 0%, Edge F1: 0%

- **Title (GT):** Akatsuki: Building Stable and Scalable Large Scale Game Servers with Amazon ECS (Japanese)
- **Nodes:** gen=0 vs gt=8
- **Edges:** gen=0 vs gt=11
- **Missing services:** ALB, Aurora, AutoScaling, CloudWatch, ECS, ElastiCache, Lambda, UserConsumerMobile
- **Missing edges:** UserConsumerMobile→ALB, Lambda→ECS, CloudWatch→Lambda, ALB→ECS, ALB→UserConsumerMobile

### `BgT_bDAejSQ` — Svc F1: 22%, Edge F1: 15%

- **Title (GT):** GoDaddy: Empowering Agility with ZeroTrust Environment Best Practices
- **Nodes:** gen=11 vs gt=2
- **Edges:** gen=12 vs gt=1
- **Hallucinated services:** DirectConnect, ELB, ThirdParty, UserCompanyDeveloper, UserConsumerWebMobile, VPC, WAF
- **Hallucinated edges:** UserCompanyDeveloper→ThirdParty, ThirdParty→UserCompanyDeveloper, VPC→DirectConnect, VPC→EKS, EKS→VPC

### `1xLjtJnfZes` — Svc F1: 36%, Edge F1: 0%

- **Title (GT):** MATTR: Building Digital Trust at Scale
- **Nodes:** gen=3 vs gt=8
- **Edges:** gen=3 vs gt=6
- **Missing services:** AutoScaling, ELB, ShieldAdvanced, ThirdParty, UserCompanyDataStream, UserConsumerAPI
- **Hallucinated services:** UserCompanyAPI
- **Missing edges:** UserConsumerAPI→UserCompanyDataStream, UserCompanyDataStream→ELB, ELB→WAF, ELB→ShieldAdvanced, ELB→EKS
- **Hallucinated edges:** UserCompanyAPI→WAF, WAF→EKS, EKS→UserCompanyAPI

### `D6rG9eZ5Qus` — Svc F1: 60%, Edge F1: 38%

- **Title (GT):** Graham Media Group: Modernizing Traditional Broadcasting with AWS
- **Nodes:** gen=11 vs gt=9
- **Edges:** gen=12 vs gt=9
- **Missing services:** CloudFront, ThirdParty, UserCompanyDataStream
- **Hallucinated services:** Lambda, SystemsManager, UserCompanyAnalyst, UserCompanyElementalLiveDevice, UserConsumerWebMobile
- **Missing edges:** UserCompanyDataStream→MediaStore, MediaStore→S3, MediaPackage→CloudFront, MediaPackage→Transcribe, ThirdParty→UserCompanyDataStream
- **Hallucinated edges:** UserCompanyElementalLiveDevice→MediaStore, UserCompanyElementalLiveDevice→S3, MediaPackage→UserConsumerWebMobile, S3→Transcribe, Transcribe→S3

### `8s0wGRkiDrw` — Svc F1: 60%, Edge F1: 36%

- **Title (GT):** Mobilewalla: S3 Access Monitoring Using ML
- **Nodes:** gen=7 vs gt=5
- **Edges:** gen=7 vs gt=4
- **Missing services:** OpenSearch
- **Hallucinated services:** ThirdParty, UserCompanyAPI, UserCompanyAgent
- **Missing edges:** OpenSearch→SNS, Lambda→OpenSearch
- **Hallucinated edges:** UserCompanyAPI→S3, S3→UserCompanyAPI, Lambda→ThirdParty, ThirdParty→SNS, SNS→UserCompanyAgent

### `-wLEkq21cvA` — Svc F1: 60%, Edge F1: 27%

- **Title (GT):** Versent: The Migration Factory
- **Nodes:** gen=8 vs gt=9
- **Edges:** gen=12 vs gt=10
- **Missing services:** AppDiscovery, UserCompanyAgent
- **Hallucinated services:** UserCompanyAnalyst, UserCompanyEdge
- **Missing edges:** AppDiscovery→EC2, EC2→AppDiscovery, UserCompanyAgent→DynamoDB, UserCompanyAgent→ThirdParty, ThirdParty→AppDiscovery
- **Hallucinated edges:** UserCompanyAnalyst→DynamoDB, UserCompanyAnalyst→ThirdParty, ThirdParty→UserCompanyAnalyst, EC2→DynamoDB, EC2→ThirdParty

### `53sUjFv9ByI` — Svc F1: 62%, Edge F1: 35%

- **Title (GT):** Neumora Therapeutics: Enabling DNA and RNA Data Insight for Rapid Genomics Sequencing Drug Discovery
- **Nodes:** gen=7 vs gt=6
- **Edges:** gen=11 vs gt=6
- **Missing services:** ThirdParty, UserCompanyDataStream
- **Hallucinated services:** S3, UserCompanyAnalyst, UserCompanyDeveloper
- **Missing edges:** EC2→ECR, EKS→ThirdParty, UserCompanyDataStream→EC2
- **Hallucinated edges:** UserCompanyDeveloper→EC2, EC2→UserCompanyDeveloper, FSX→EC2, EKS→ECR, EKS→FSX

### `4-teOQ_dJvY` — Svc F1: 62%, Edge F1: 48%

- **Title (GT):** SBB Cargo: Data Collection and Processing with Serverless Analytics Services
- **Nodes:** gen=13 vs gt=9
- **Edges:** gen=16 vs gt=13
- **Missing services:** KinesisAnalytics, UserCompanyAPI, UserCompanyEdge
- **Hallucinated services:** UserCompanyInternalPlatform, UserConsumerIOT
- **Missing edges:** UserCompanyEdge→Lambda, Kinesis→KinesisAnalytics, KinesisAnalytics→Kinesis, ApiGateway→UserCompanyAPI, DynamoDB→Lambda
- **Hallucinated edges:** UserConsumerIOT→Lambda, Lambda→Kinesis, Kinesis→Kinesis, ApiGateway→UserCompanyInternalPlatform, UserCompanyInternalPlatform→ApiGateway

### `BPvr0qWpJlA` — Svc F1: 63%, Edge F1: 17%

- **Title (GT):** ContactSuite: Automated Omni-Channel Service Desk Workflow
- **Nodes:** gen=10 vs gt=10
- **Edges:** gen=15 vs gt=9
- **Missing services:** UserCompanyCRM, UserCompanyDataStream, UserConsumerMobile
- **Hallucinated services:** EC2, SES, ThirdParty, UserConsumerWebMobile
- **Missing edges:** Lambda→ECS, DynamoDB→UserCompanyCRM, UserConsumerMobile→Connect, Connect→UserCompanyCRM, UserCompanyCRM→UserCompanyAgent
- **Hallucinated edges:** UserConsumerWebMobile→Connect, UserConsumerWebMobile→SES, UserCompanyAgent→EC2, UserCompanyAgent→UserConsumerWebMobile, Connect→EC2

### `Yju3yReAQtc` — Svc F1: 67%, Edge F1: 32%

- **Title (GT):** Fortinet Uses AWS Serverless to Provide a Highly Available ControlPlane for their FortiWeb CloudWAF
- **Nodes:** gen=13 vs gt=7
- **Edges:** gen=18 vs gt=7
- **Missing services:** OpenSearch, UserCompanyInternalPlatform
- **Hallucinated services:** EC2, ThirdParty, UserCompanyDeveloper
- **Missing edges:** CloudFront→ApiGateway, Lambda→UserCompanyInternalPlatform, DynamoDB→Lambda
- **Hallucinated edges:** UserCompanyDeveloper→CloudFront, UserCompanyDeveloper→ApiGateway, CloudFront→UserCompanyDeveloper, ApiGateway→Lambda, ApiGateway→UserCompanyDeveloper
