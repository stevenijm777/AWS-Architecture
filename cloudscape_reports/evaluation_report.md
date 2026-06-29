# Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-28 21:23:51*

## 1. Executive Summary

**Videos evaluated:** 94

| Metric | Precision | Recall | F1 |
|--------|-----------|--------|----|
| **Services (unique set)** | 74.4% | 83.4% | 77.8% |
| **Services (multiset)** | 70.9% | 82.0% | 74.9% |
| **Edges (service pairs)** | 45.2% | 48.8% | 45.0% |

**Edge type accuracy (data/meta):** 74.9%

**Average node count ratio (gen/gt):** 1.23x

**Average workflows:** gen=2.8 vs gt=3.5

## 2. Service F1 Score Distribution

| Range | Count | Percentage |
|-------|-------|------------|
| 🟢 Excellent (≥90%) | 18 | 19.1% |
| 🟡 Good (70-89%) | 61 | 64.9% |
| 🟠 Fair (50-69%) | 12 | 12.8% |
| 🔴 Poor (<50%) | 3 | 3.2% |

## 3. Per-Video Results (sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 9 | 0 | — | — |
| 2 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 3 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 77% | 71% | 74% | 10 | 10 | 13 | 14 | — | — |
| 4 | `IV3KuMGVNXI` | 100% | 100% | 100% | 60% | 35% | 44% | 7 | 7 | 10 | 17 | — | — |
| 5 | `Kebb0LOVC28` | 100% | 100% | 100% | 47% | 38% | 42% | 11 | 9 | 17 | 21 | — | — |
| 6 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 7 | `07lfvavMdfU` | 91% | 100% | 95% | 71% | 71% | 71% | 12 | 10 | 14 | 14 | — | Lambda |
| 8 | `4WjXH8Wp0E4` | 100% | 90% | 95% | 59% | 59% | 59% | 11 | 14 | 22 | 22 | UserConsumerWeb | — |
| 9 | `6YkguepAQuQ` | 100% | 90% | 95% | 38% | 30% | 33% | 9 | 10 | 8 | 10 | VPC | — |
| 10 | `7LziNjUTo7w` | 89% | 100% | 94% | 92% | 69% | 79% | 9 | 9 | 12 | 16 | — | UserCompanyAgent |
| 11 | `AzM_d7ZvzUE` | 89% | 100% | 94% | 76% | 65% | 70% | 12 | 11 | 17 | 20 | — | UserCompanyDeveloper |
| 12 | `-ahWdCysMYw` | 100% | 88% | 93% | 56% | 56% | 56% | 7 | 8 | 9 | 9 | VPN | — |
| 13 | `6EUknQqaV1w` | 88% | 100% | 93% | 77% | 91% | 83% | 11 | 9 | 13 | 11 | — | SES |
| 14 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 15 | `A4Lfk1Zz1dE` | 86% | 100% | 92% | 40% | 80% | 53% | 9 | 8 | 10 | 5 | — | UserCompanyDeveloper |
| 16 | `Felt-hOU6kU` | 86% | 100% | 92% | 50% | 100% | 67% | 8 | 7 | 8 | 4 | — | VPC |
| 17 | `1kWxymroGeE` | 83% | 100% | 91% | 50% | 100% | 67% | 6 | 5 | 8 | 4 | — | EC2 |
| 18 | `9yziTe6lBwk` | 90% | 90% | 90% | 80% | 50% | 62% | 10 | 10 | 10 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 19 | `Ly_UhX3LCCs` | 80% | 100% | 89% | 20% | 29% | 24% | 7 | 7 | 10 | 7 | — | UserCompanyAPI |
| 20 | `Cw26CrJUqv8` | 89% | 89% | 89% | 80% | 89% | 84% | 10 | 10 | 10 | 9 | UserConsumerWeb | UserCompanyDeveloper |
| 21 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 22 | `BX1K8x1lVLc` | 88% | 88% | 88% | 60% | 64% | 62% | 8 | 8 | 15 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 23 | `IP03SkGbP-U` | 88% | 88% | 88% | 33% | 71% | 45% | 14 | 8 | 15 | 7 | UserConsumerWeb | UserConsumerWebMobile |
| 24 | `Pc7_uOdlGKo` | 88% | 88% | 88% | 45% | 56% | 50% | 9 | 9 | 11 | 9 | UserConsumerMobile | UserCompanyAnalyst |
| 25 | `iKYvG5aiIn8` | 88% | 88% | 88% | 44% | 57% | 50% | 9 | 9 | 9 | 7 | ThirdParty | OnPremDC |
| 26 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 27 | `90rWUjKjnAE` | 86% | 86% | 86% | 27% | 30% | 29% | 9 | 8 | 11 | 10 | UserConsumerDeveloper | UserCompanyDeveloper |
| 28 | `Ccutfm_Srzw` | 86% | 86% | 86% | 38% | 36% | 37% | 11 | 11 | 13 | 14 | KinesisDataStream | ApiGateway |
| 29 | `GoziWpmFCS0` | 75% | 100% | 86% | 10% | 50% | 17% | 8 | 4 | 10 | 2 | — | UserCompanyDataStream |
| 30 | `NfUwtK8ALtw` | 86% | 86% | 86% | 80% | 75% | 77% | 9 | 9 | 15 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 31 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 32 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 33 | `OQKOHNtyz3E` | 80% | 89% | 84% | 61% | 46% | 52% | 12 | 11 | 18 | 24 | UserConsumerMobile | UserCompanyAnalyst, UserConsumerWebMobile |
| 34 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 35 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 36 | `AS2JeM2FUzE` | 88% | 78% | 82% | 55% | 50% | 52% | 8 | 9 | 11 | 12 | UserConsumerWeb, VPCPeering | UserCompanyAnalyst |
| 37 | `Dp3YAxFp-YM` | 78% | 88% | 82% | 73% | 57% | 64% | 10 | 10 | 11 | 14 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerMobile |
| 38 | `H_S7CxtHgSM` | 78% | 88% | 82% | 41% | 58% | 48% | 11 | 11 | 17 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 39 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 40 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 41 | `JiWHomdh1oI` | 80% | 80% | 80% | 73% | 73% | 73% | 7 | 7 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 42 | `KQ6Fg206O9U` | 80% | 80% | 80% | 50% | 43% | 46% | 10 | 10 | 12 | 14 | Firehose, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 43 | `1ZLiRT0C2Yo` | 67% | 100% | 80% | 0% | 0% | 0% | 9 | 6 | 8 | 0 | — | OnPremDC, UserCompanyDeveloper, UserConsumerMobile |
| 44 | `8s0wGRkiDrw` | 67% | 100% | 80% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | UserCompanyAnalyst, UserConsumerWeb |
| 45 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 46 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 47 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 48 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 49 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 50 | `ww5fiygF6eg` | 75% | 86% | 80% | 69% | 45% | 55% | 11 | 10 | 13 | 20 | UserCompanyDrone | OnPremDC, UserCompanyAgent |
| 51 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 52 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 53 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 54 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 55 | `GJ1So_pbZWk` | 70% | 88% | 78% | 67% | 43% | 53% | 13 | 9 | 15 | 23 | UserConsumerWeb | ApiGateway, UserCompanyAnalyst, UserConsumerWebMobile |
| 56 | `Kp51k6LY-2c` | 70% | 88% | 78% | 20% | 25% | 22% | 14 | 8 | 20 | 16 | UserCompanyDataStream | DirectConnect, OnPremDC, ThirdParty |
| 57 | `LxeSC3-xMlk` | 70% | 88% | 78% | 41% | 60% | 49% | 10 | 8 | 22 | 15 | UserConsumerMobile | Lambda, UserCompanyDeveloper, UserConsumerWebMobile |
| 58 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 59 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 60 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 69% | 53% | 60% | 12 | 13 | 13 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 61 | `N2mktbl8EQk` | 71% | 83% | 77% | 45% | 56% | 50% | 7 | 6 | 11 | 9 | Kinesis | KinesisVideo, ThirdParty |
| 62 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 63 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 64 | `FfSNnH2bbNc` | 75% | 75% | 75% | 67% | 42% | 52% | 8 | 8 | 12 | 19 | UserConsumerSatellite, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 65 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 66 | `KzJKdUZ3Ba4` | 60% | 100% | 75% | 30% | 50% | 37% | 5 | 4 | 10 | 6 | — | SAP, UserCompanyAgent |
| 67 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 68 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 69 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 70 | `INog0_9tCtY` | 67% | 80% | 73% | 53% | 53% | 53% | 18 | 14 | 19 | 19 | OpenSearch, UserCompanyAnalyst | CloudWatch, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 71 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 36% | 42% | 9 | 8 | 8 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 72 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 73 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 74 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 75 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 76 | `M_hqigB9C4I` | 67% | 75% | 71% | 56% | 31% | 40% | 9 | 9 | 9 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 77 | `9qTEHITVeLE` | 60% | 86% | 71% | 30% | 43% | 35% | 11 | 9 | 20 | 14 | UserConsumerWeb | EC2, OpenSearch, UserCompanyAnalyst (+1) |
| 78 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 79 | `G07keU4g-LU` | 64% | 78% | 70% | 37% | 48% | 42% | 20 | 10 | 27 | 21 | UserConsumerMobile, UserConsumerPOS | RDS, SageMaker, UserCompanyAgent (+1) |
| 80 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 81 | `MbkLJ62jtMc` | 56% | 83% | 67% | 17% | 75% | 27% | 17 | 6 | 18 | 4 | UserCompanyAPI | ApiGateway, SES, ThirdParty (+1) |
| 82 | `Ozbv9qBsDG8` | 54% | 88% | 67% | 28% | 41% | 33% | 17 | 11 | 25 | 17 | ThirdParty | CloudFormation, CloudWatch, DynamoDB (+3) |
| 83 | `JRDGId6N49E` | 57% | 80% | 67% | 9% | 33% | 14% | 10 | 6 | 11 | 3 | ThirdParty | FSX, UserCompanyDeveloper, UserCompanyInternalPlatform |
| 84 | `6sY0AunanlM` | 60% | 75% | 67% | 0% | 0% | 0% | 8 | 4 | 8 | 0 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerWebMobile |
| 85 | `K5ww_O4vsxo` | 60% | 75% | 67% | 85% | 33% | 47% | 15 | 15 | 20 | 52 | DirectConnect | OnPremDC, UserConsumerMobile |
| 86 | `KywvGM6HVXI` | 60% | 67% | 63% | 50% | 27% | 35% | 13 | 11 | 12 | 22 | EC2, Kinesis, UserConsumerWeb | EKS, KinesisDataStream, ThirdParty (+1) |
| 87 | `53sUjFv9ByI` | 57% | 67% | 62% | 50% | 50% | 50% | 7 | 6 | 6 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 88 | `DAJZAygxDZA` | 57% | 67% | 62% | 15% | 13% | 14% | 9 | 8 | 13 | 15 | ModelRegistry, UserCompanyAnalyst | ApiGateway, StepFunctions, UserCompanyDomainExpert |
| 89 | `99nNHsbwBpg` | 40% | 100% | 57% | 0% | 0% | 0% | 7 | 2 | 9 | 0 | — | ELB, ThirdParty, UserConsumerWebMobile |
| 90 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 91 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 92 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |
| 93 | `HcmEFZukA-Y` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 9 | 0 | 15 | ApiGateway, EventBridge, Lambda (+6) | — |
| 94 | `JSBB-BCvavQ` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 5 | 0 | 0 | Aurora, BeanStalk, EC2 (+2) | — |

## 4. Most Frequently Missing Services (False Negatives)

Services present in ground truth but NOT in generated graphs.

| Service | Times Missed | Capability |
|---------|-------------|------------|
| UserConsumerWeb | 21 | User |
| UserCompanyDataStream | 11 | User |
| ThirdParty | 11 | ThirdParty |
| UserConsumerMobile | 10 | User |
| UserCompanyAgent | 5 | User |
| UserConsumerAPI | 5 | User |
| Kinesis | 4 | integration |
| EC2 | 4 | compute |
| UserCompanyAnalyst | 4 | User |
| ALB | 3 | networking |
| UserCompanyAPI | 3 | User |
| VPC | 3 | networking |
| UserConsumerEdge | 2 | User |
| UserConsumerPOS | 2 | User |
| Lambda | 2 | compute |
| OnPremDC | 1 | OnPremDC |
| VPN | 1 | networking |
| Fargate | 1 | compute |
| S2SVPN | 1 | networking |
| UserCompanyEdge | 1 | User |

## 5. Most Frequently Hallucinated Services (False Positives)

Services in generated graphs but NOT in ground truth.

| Service | Times Hallucinated | Capability |
|---------|-------------------|------------|
| UserConsumerWebMobile | 22 | User |
| UserCompanyDeveloper | 18 | User |
| ThirdParty | 15 | ThirdParty |
| UserCompanyAnalyst | 11 | User |
| UserCompanyAgent | 11 | User |
| OnPremDC | 8 | OnPremDC |
| EC2 | 8 | compute |
| Lambda | 5 | compute |
| RDS | 5 | storage |
| UserConsumerMobile | 5 | User |
| UserCompanyDomainExpert | 4 | User |
| UserCompanyAPI | 4 | User |
| ELB | 4 | networking |
| UserCompanyInternalPlatform | 4 | User |
| UserConsumerWeb | 4 | User |
| ApiGateway | 4 | networking |
| KinesisDataStream | 3 | integration |
| EKS | 3 | compute |
| SES | 3 | other |
| CloudFormation | 2 | control |

## 6. Most Frequently Missing Edges

| Edge (src → tgt) | Times Missed |
|------------------|-------------|
| VPC→TransitGateway | 8 |
| DynamoDB→Lambda | 7 |
| S3→EC2 | 7 |
| UserConsumerWeb→CloudFront | 7 |
| CloudFront→UserConsumerWeb | 6 |
| EC2→S3 | 6 |
| ThirdParty→DirectConnect | 6 |
| Lambda→ThirdParty | 6 |
| ThirdParty→Lambda | 6 |
| DirectConnect→ThirdParty | 5 |
| RDS→EC2 | 5 |
| TransitGateway→VPC | 5 |
| S3→Lambda | 5 |
| EC2→ThirdParty | 4 |
| UserCompanyAgent→ThirdParty | 4 |

## 7. Most Frequently Hallucinated Edges

| Edge (src → tgt) | Times Hallucinated |
|------------------|--------------------|
| ThirdParty→S3 | 10 |
| EC2→S3 | 9 |
| Lambda→S3 | 9 |
| UserCompanyDeveloper→ThirdParty | 8 |
| EC2→EC2 | 7 |
| UserConsumerWebMobile→CloudFront | 7 |
| CloudFront→UserConsumerWebMobile | 7 |
| Glue→S3 | 6 |
| EKS→EKS | 6 |
| Lambda→DynamoDB | 5 |
| EC2→RDS | 5 |
| EKS→EC2 | 5 |
| ThirdParty→Lambda | 5 |
| SQS→EC2 | 4 |
| ApiGateway→Lambda | 4 |

## 8. Performance by Service Capability

| Capability | GT Count | Correct | Missed | Hallucinated | Recall |
|------------|----------|---------|--------|--------------|--------|
| OnPremDC | 1 | 0 | 1 | 8 | 0.0% |
| Partner | 2 | 1 | 1 | 1 | 50.0% |
| ThirdParty | 39 | 28 | 11 | 15 | 71.8% |
| User | 102 | 33 | 69 | 92 | 32.4% |
| compute | 171 | 160 | 11 | 20 | 93.6% |
| control | 49 | 49 | 0 | 8 | 100.0% |
| integration | 63 | 55 | 8 | 7 | 87.3% |
| networking | 76 | 65 | 11 | 16 | 85.5% |
| other | 33 | 31 | 2 | 6 | 93.9% |
| storage | 149 | 147 | 2 | 8 | 98.7% |

## 9. Performance by Functional Goal Category

| Category | # Videos | Avg Svc F1 | Avg Edge F1 |
|----------|----------|------------|-------------|
| compute_intensive | 11 | 75.4% | 47.0% |
| control | 17 | 77.5% | 36.5% |
| data_ingestion | 37 | 79.4% | 51.4% |
| interactive | 34 | 78.3% | 47.3% |
| other | 8 | 71.3% | 30.2% |

## 10. Bottom 10 Worst Performing Videos

### `JSBB-BCvavQ` — Svc F1: 0%, Edge F1: 0%

- **Title (GT):** Talabat: Applying the Right Strategies for a Successful Migration
- **Nodes:** gen=0 vs gt=5
- **Edges:** gen=0 vs gt=0
- **Missing services:** Aurora, BeanStalk, EC2, EKS, Lambda

### `HcmEFZukA-Y` — Svc F1: 0%, Edge F1: 0%

- **Title (GT):** 7-Eleven: Innovation with Serverless for Cash-Based Digital Wallet
- **Nodes:** gen=0 vs gt=9
- **Edges:** gen=0 vs gt=15
- **Missing services:** ApiGateway, EventBridge, Lambda, MongoDBAtlas, Pinpoint, SQS, ThirdParty, UserConsumerMobile, UserConsumerPOS
- **Missing edges:** UserConsumerMobile→ApiGateway, UserConsumerPOS→ThirdParty, ThirdParty→ApiGateway, ApiGateway→Pinpoint, ApiGateway→UserConsumerMobile

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

### `99nNHsbwBpg` — Svc F1: 57%, Edge F1: 0%

- **Title (GT):** SkyScanner: Building HighlyAvailable MultiRegion Kubernetes Clusters on 100 Amazon EC2 Spot
- **Nodes:** gen=7 vs gt=2
- **Edges:** gen=9 vs gt=0
- **Hallucinated services:** ELB, ThirdParty, UserConsumerWebMobile
- **Hallucinated edges:** UserConsumerWebMobile→ELB, ELB→EC2, EC2→ELB, EC2→EC2, AutoScaling→EC2

### `DAJZAygxDZA` — Svc F1: 62%, Edge F1: 14%

- **Title (GT):** BASF Digital Farming: Productionizing ML with a Cross-Account Model Deployment Solution
- **Nodes:** gen=9 vs gt=8
- **Edges:** gen=13 vs gt=15
- **Missing services:** ModelRegistry, UserCompanyAnalyst
- **Hallucinated services:** ApiGateway, StepFunctions, UserCompanyDomainExpert
- **Missing edges:** UserCompanyAnalyst→SageMaker, UserCompanyAnalyst→ModelRegistry, ModelRegistry→ThirdParty, ModelRegistry→SageMaker, UserCompanyDeveloper→ThirdParty
- **Hallucinated edges:** UserCompanyDomainExpert→SageMaker, UserCompanyDomainExpert→ThirdParty, SageMaker→ThirdParty, UserCompanyDeveloper→ApiGateway, ApiGateway→StepFunctions

### `53sUjFv9ByI` — Svc F1: 62%, Edge F1: 50%

- **Title (GT):** Neumora Therapeutics: Enabling DNA and RNA Data Insight for Rapid Genomics Sequencing Drug Discovery
- **Nodes:** gen=7 vs gt=6
- **Edges:** gen=6 vs gt=6
- **Missing services:** ThirdParty, UserCompanyDataStream
- **Hallucinated services:** S3, UserCompanyAnalyst, UserCompanyDeveloper
- **Missing edges:** EC2→ECR, EKS→ThirdParty, UserCompanyDataStream→EC2
- **Hallucinated edges:** UserCompanyDeveloper→EC2, EKS→S3, S3→UserCompanyAnalyst

### `KywvGM6HVXI` — Svc F1: 63%, Edge F1: 35%

- **Title (GT):** Capillary Technologies: Building an OmniChannel Data Ingestion Platform
- **Nodes:** gen=13 vs gt=11
- **Edges:** gen=12 vs gt=22
- **Missing services:** EC2, Kinesis, UserConsumerWeb
- **Hallucinated services:** EKS, KinesisDataStream, ThirdParty, UserConsumerWebMobile
- **Missing edges:** UserConsumerWeb→ApiGateway, ALB→EC2, ALB→UserCompanyDeveloper, EC2→DynamoDB, EC2→ALB
- **Hallucinated edges:** ALB→EKS, EKS→DynamoDB, UserConsumerWebMobile→ThirdParty, ThirdParty→ApiGateway, Lambda→KinesisDataStream

### `K5ww_O4vsxo` — Svc F1: 67%, Edge F1: 47%

- **Title (GT):** Samsung Cloud: Global Hybrid Network Optimization Across 5 AWS Regions Using AWS Transit Gateway
- **Nodes:** gen=15 vs gt=15
- **Edges:** gen=20 vs gt=52
- **Missing services:** DirectConnect
- **Hallucinated services:** OnPremDC, UserConsumerMobile
- **Missing edges:** VPC→TransitGateway, TransitGateway→VPC, TransitGateway→TransitGateway, TransitGateway→DirectConnect, TransitGateway→ThirdParty
- **Hallucinated edges:** UserConsumerMobile→VPC, OnPremDC→ThirdParty, ThirdParty→ThirdParty
