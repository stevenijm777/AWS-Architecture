# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-30 09:44:22*

## 1. Executive Summary (Side-by-Side Comparison)

This table compares performance metrics across all generated graph directories.

| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |
|---|---|---|---|---|---|---|
| **Standard (data/graphs)** | 104 | 78.2% | 75.5% | 45.8% | 76.1% | 1.23x |
| **Parsimonious API (data/graphs_parsimonious)** | 31 | 87.2% | 85.5% | 53.5% | 82.9% | 1.08x |

---

## Standard (data/graphs) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 9 | 0 | — | — |
| 2 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 3 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 77% | 71% | 74% | 10 | 10 | 13 | 14 | — | — |
| 4 | `IV3KuMGVNXI` | 100% | 100% | 100% | 60% | 35% | 44% | 7 | 7 | 10 | 17 | — | — |
| 5 | `Kebb0LOVC28` | 100% | 100% | 100% | 47% | 38% | 42% | 11 | 9 | 17 | 21 | — | — |
| 6 | `QnmmTIYZxNI` | 100% | 100% | 100% | 80% | 67% | 73% | 8 | 8 | 5 | 6 | — | — |
| 7 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 8 | `07lfvavMdfU` | 91% | 100% | 95% | 71% | 71% | 71% | 12 | 10 | 14 | 14 | — | Lambda |
| 9 | `4WjXH8Wp0E4` | 100% | 90% | 95% | 59% | 59% | 59% | 11 | 14 | 22 | 22 | UserConsumerWeb | — |
| 10 | `6YkguepAQuQ` | 100% | 90% | 95% | 38% | 30% | 33% | 9 | 10 | 8 | 10 | VPC | — |
| 11 | `Q6r_QbYXFpg` | 90% | 100% | 95% | 80% | 89% | 84% | 12 | 11 | 10 | 9 | — | UserCompanyDeveloper |
| 12 | `7LziNjUTo7w` | 89% | 100% | 94% | 92% | 69% | 79% | 9 | 9 | 12 | 16 | — | UserCompanyAgent |
| 13 | `AzM_d7ZvzUE` | 89% | 100% | 94% | 76% | 65% | 70% | 12 | 11 | 17 | 20 | — | UserCompanyDeveloper |
| 14 | `-ahWdCysMYw` | 100% | 88% | 93% | 56% | 56% | 56% | 7 | 8 | 9 | 9 | VPN | — |
| 15 | `6EUknQqaV1w` | 88% | 100% | 93% | 77% | 91% | 83% | 11 | 9 | 13 | 11 | — | SES |
| 16 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 17 | `A4Lfk1Zz1dE` | 86% | 100% | 92% | 40% | 80% | 53% | 9 | 8 | 10 | 5 | — | UserCompanyDeveloper |
| 18 | `Felt-hOU6kU` | 86% | 100% | 92% | 50% | 100% | 67% | 8 | 7 | 8 | 4 | — | VPC |
| 19 | `QM96Fv_NAnw` | 100% | 86% | 92% | 30% | 50% | 37% | 6 | 7 | 10 | 6 | ThirdParty | — |
| 20 | `1kWxymroGeE` | 83% | 100% | 91% | 50% | 100% | 67% | 6 | 5 | 8 | 4 | — | EC2 |
| 21 | `9yziTe6lBwk` | 90% | 90% | 90% | 80% | 50% | 62% | 10 | 10 | 10 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 22 | `Ly_UhX3LCCs` | 80% | 100% | 89% | 20% | 29% | 24% | 7 | 7 | 10 | 7 | — | UserCompanyAPI |
| 23 | `Cw26CrJUqv8` | 89% | 89% | 89% | 80% | 89% | 84% | 10 | 10 | 10 | 9 | UserConsumerWeb | UserCompanyDeveloper |
| 24 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 25 | `BX1K8x1lVLc` | 88% | 88% | 88% | 60% | 64% | 62% | 8 | 8 | 15 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 26 | `IP03SkGbP-U` | 88% | 88% | 88% | 33% | 71% | 45% | 14 | 8 | 15 | 7 | UserConsumerWeb | UserConsumerWebMobile |
| 27 | `Pc7_uOdlGKo` | 88% | 88% | 88% | 45% | 56% | 50% | 9 | 9 | 11 | 9 | UserConsumerMobile | UserCompanyAnalyst |
| 28 | `iKYvG5aiIn8` | 88% | 88% | 88% | 44% | 57% | 50% | 9 | 9 | 9 | 7 | ThirdParty | OnPremDC |
| 29 | `-kA0ahrhX3I` | 86% | 86% | 86% | 25% | 50% | 33% | 11 | 9 | 16 | 8 | UserCompanyDeveloper | UserConsumerWeb |
| 30 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 31 | `90rWUjKjnAE` | 86% | 86% | 86% | 27% | 30% | 29% | 9 | 8 | 11 | 10 | UserConsumerDeveloper | UserCompanyDeveloper |
| 32 | `Ccutfm_Srzw` | 86% | 86% | 86% | 38% | 36% | 37% | 11 | 11 | 13 | 14 | KinesisDataStream | ApiGateway |
| 33 | `GoziWpmFCS0` | 75% | 100% | 86% | 10% | 50% | 17% | 8 | 4 | 10 | 2 | — | UserCompanyDataStream |
| 34 | `NfUwtK8ALtw` | 86% | 86% | 86% | 80% | 75% | 77% | 9 | 9 | 15 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 35 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 36 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 37 | `OQKOHNtyz3E` | 80% | 89% | 84% | 61% | 46% | 52% | 12 | 11 | 18 | 24 | UserConsumerMobile | UserCompanyAnalyst, UserConsumerWebMobile |
| 38 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 39 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 40 | `PBa68gCG0Uk` | 83% | 83% | 83% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | ThirdParty | UserCompanyDataStream |
| 41 | `AS2JeM2FUzE` | 88% | 78% | 82% | 55% | 50% | 52% | 8 | 9 | 11 | 12 | UserConsumerWeb, VPCPeering | UserCompanyAnalyst |
| 42 | `Dp3YAxFp-YM` | 78% | 88% | 82% | 73% | 57% | 64% | 10 | 10 | 11 | 14 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerMobile |
| 43 | `H_S7CxtHgSM` | 78% | 88% | 82% | 41% | 58% | 48% | 11 | 11 | 17 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 44 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 45 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 46 | `JiWHomdh1oI` | 80% | 80% | 80% | 73% | 73% | 73% | 7 | 7 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 47 | `KQ6Fg206O9U` | 80% | 80% | 80% | 50% | 43% | 46% | 10 | 10 | 12 | 14 | Firehose, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 48 | `1ZLiRT0C2Yo` | 67% | 100% | 80% | 0% | 0% | 0% | 9 | 6 | 8 | 0 | — | OnPremDC, UserCompanyDeveloper, UserConsumerMobile |
| 49 | `8s0wGRkiDrw` | 67% | 100% | 80% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | UserCompanyAnalyst, UserConsumerWeb |
| 50 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 51 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 52 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 53 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 54 | `PgeQufaQy7I` | 86% | 75% | 80% | 83% | 62% | 71% | 7 | 8 | 6 | 8 | CloudFormation, UserConsumerWeb | UserConsumerWebMobile |
| 55 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 56 | `ww5fiygF6eg` | 75% | 86% | 80% | 69% | 45% | 55% | 11 | 10 | 13 | 20 | UserCompanyDrone | OnPremDC, UserCompanyAgent |
| 57 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 58 | `QnwfcDZkwh8` | 90% | 69% | 78% | 62% | 56% | 59% | 11 | 13 | 16 | 18 | UserCompanyDeveloper, UserConsumerMobile, UserConsumerTV (+1) | UserConsumerWebMobile |
| 59 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 60 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 61 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 62 | `GJ1So_pbZWk` | 70% | 88% | 78% | 67% | 43% | 53% | 13 | 9 | 15 | 23 | UserConsumerWeb | ApiGateway, UserCompanyAnalyst, UserConsumerWebMobile |
| 63 | `Kp51k6LY-2c` | 70% | 88% | 78% | 20% | 25% | 22% | 14 | 8 | 20 | 16 | UserCompanyDataStream | DirectConnect, OnPremDC, ThirdParty |
| 64 | `LxeSC3-xMlk` | 70% | 88% | 78% | 41% | 60% | 49% | 10 | 8 | 22 | 15 | UserConsumerMobile | Lambda, UserCompanyDeveloper, UserConsumerWebMobile |
| 65 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 66 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 67 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 69% | 53% | 60% | 12 | 13 | 13 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 68 | `N2mktbl8EQk` | 71% | 83% | 77% | 45% | 56% | 50% | 7 | 6 | 11 | 9 | Kinesis | KinesisVideo, ThirdParty |
| 69 | `OWLGK-eVrTw` | 71% | 83% | 77% | 10% | 6% | 8% | 8 | 6 | 10 | 16 | UserConsumerAPI | EC2, UserCompanyAPI |
| 70 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 71 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 72 | `FfSNnH2bbNc` | 75% | 75% | 75% | 67% | 42% | 52% | 8 | 8 | 12 | 19 | UserConsumerSatellite, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 73 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 74 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 75 | `KzJKdUZ3Ba4` | 60% | 100% | 75% | 30% | 50% | 37% | 5 | 4 | 10 | 6 | — | SAP, UserCompanyAgent |
| 76 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 77 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 78 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 79 | `INog0_9tCtY` | 67% | 80% | 73% | 53% | 53% | 53% | 18 | 14 | 19 | 19 | OpenSearch, UserCompanyAnalyst | CloudWatch, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 80 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 36% | 42% | 9 | 8 | 8 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 81 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 82 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 83 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 84 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 85 | `M_hqigB9C4I` | 67% | 75% | 71% | 56% | 31% | 40% | 9 | 9 | 9 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 86 | `9qTEHITVeLE` | 60% | 86% | 71% | 30% | 43% | 35% | 11 | 9 | 20 | 14 | UserConsumerWeb | EC2, OpenSearch, UserCompanyAnalyst (+1) |
| 87 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 88 | `G07keU4g-LU` | 64% | 78% | 70% | 37% | 48% | 42% | 20 | 10 | 27 | 21 | UserConsumerMobile, UserConsumerPOS | RDS, SageMaker, UserCompanyAgent (+1) |
| 89 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 90 | `MbkLJ62jtMc` | 56% | 83% | 67% | 17% | 75% | 27% | 17 | 6 | 18 | 4 | UserCompanyAPI | ApiGateway, SES, ThirdParty (+1) |
| 91 | `Ozbv9qBsDG8` | 54% | 88% | 67% | 28% | 41% | 33% | 17 | 11 | 25 | 17 | ThirdParty | CloudFormation, CloudWatch, DynamoDB (+3) |
| 92 | `JRDGId6N49E` | 57% | 80% | 67% | 9% | 33% | 14% | 10 | 6 | 11 | 3 | ThirdParty | FSX, UserCompanyDeveloper, UserCompanyInternalPlatform |
| 93 | `6sY0AunanlM` | 60% | 75% | 67% | 0% | 0% | 0% | 8 | 4 | 8 | 0 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerWebMobile |
| 94 | `K5ww_O4vsxo` | 60% | 75% | 67% | 85% | 33% | 47% | 15 | 15 | 20 | 52 | DirectConnect | OnPremDC, UserConsumerMobile |
| 95 | `KywvGM6HVXI` | 60% | 67% | 63% | 50% | 27% | 35% | 13 | 11 | 12 | 22 | EC2, Kinesis, UserConsumerWeb | EKS, KinesisDataStream, ThirdParty (+1) |
| 96 | `53sUjFv9ByI` | 57% | 67% | 62% | 50% | 50% | 50% | 7 | 6 | 6 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 97 | `DAJZAygxDZA` | 57% | 67% | 62% | 15% | 13% | 14% | 9 | 8 | 13 | 15 | ModelRegistry, UserCompanyAnalyst | ApiGateway, StepFunctions, UserCompanyDomainExpert |
| 98 | `99nNHsbwBpg` | 40% | 100% | 57% | 0% | 0% | 0% | 7 | 2 | 9 | 0 | — | ELB, ThirdParty, UserConsumerWebMobile |
| 99 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 100 | `LYP98nPBj2A` | 36% | 100% | 53% | 11% | 50% | 18% | 16 | 5 | 36 | 8 | — | CloudWatch, Macie, SecurityHub (+4) |
| 101 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 102 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |
| 103 | `HcmEFZukA-Y` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 9 | 0 | 15 | ApiGateway, EventBridge, Lambda (+6) | — |
| 104 | `JSBB-BCvavQ` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 5 | 0 | 0 | Aurora, BeanStalk, EC2 (+2) | — |

---

## Parsimonious API (data/graphs_parsimonious) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `07lfvavMdfU` | 100% | 100% | 100% | 91% | 71% | 80% | 10 | 10 | 11 | 14 | — | — |
| 2 | `6YkguepAQuQ` | 100% | 100% | 100% | 43% | 30% | 35% | 10 | 10 | 7 | 10 | — | — |
| 3 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 5 | 0 | — | — |
| 4 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 5 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 6 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 86% | 92% | 7 | 7 | 6 | 7 | — | — |
| 7 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 45% | 62% | 7 | 7 | 5 | 11 | — | — |
| 8 | `lkDq9g43djw` | 100% | 100% | 100% | 50% | 50% | 50% | 7 | 5 | 4 | 4 | — | — |
| 9 | `7LziNjUTo7w` | 89% | 100% | 94% | 91% | 62% | 74% | 9 | 9 | 11 | 16 | — | UserConsumerDeveloper |
| 10 | `bikXzsVihF4` | 88% | 100% | 93% | 57% | 40% | 47% | 8 | 7 | 7 | 10 | — | ServiceNow |
| 11 | `unFVfqj9cQ8` | 100% | 88% | 93% | 100% | 86% | 92% | 7 | 8 | 6 | 7 | ControlTower | — |
| 12 | `qi017F1UwvM` | 93% | 93% | 93% | 78% | 58% | 67% | 17 | 17 | 18 | 24 | UserConsumerWeb | UserCompanyWebsite |
| 13 | `9yziTe6lBwk` | 90% | 90% | 90% | 89% | 50% | 64% | 10 | 10 | 9 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 14 | `AzM_d7ZvzUE` | 88% | 88% | 88% | 55% | 30% | 39% | 11 | 11 | 11 | 20 | Kinesis | KinesisDataStream |
| 15 | `iKYvG5aiIn8` | 88% | 88% | 88% | 56% | 71% | 63% | 9 | 9 | 9 | 7 | UserCompanyAnalyst | UserCompanyDataStream |
| 16 | `-kA0ahrhX3I` | 86% | 86% | 86% | 50% | 62% | 56% | 11 | 9 | 10 | 8 | UserCompanyDeveloper | UserCompanyAnalyst |
| 17 | `1SwHH7qQ6Pc` | 86% | 86% | 86% | 56% | 38% | 45% | 10 | 10 | 9 | 13 | UserConsumerMobile | UserCompanyAgent |
| 18 | `pk5yddJpC_8` | 83% | 83% | 83% | 78% | 70% | 74% | 9 | 9 | 9 | 10 | UserCompanyDeveloper | UserCompanyAnalyst |
| 19 | `rPGLNw1cOGM` | 83% | 83% | 83% | 89% | 40% | 55% | 8 | 8 | 9 | 20 | UserConsumerWeb | UserCompanyDomainExpert |
| 20 | `6CgqEzyWpeA` | 88% | 78% | 82% | 73% | 42% | 53% | 11 | 12 | 11 | 19 | CloudFront, UserConsumerWebMobile | UserConsumerMobile |
| 21 | `1VcpCVe3tLQ` | 80% | 80% | 80% | 47% | 62% | 53% | 12 | 12 | 17 | 13 | UserCompanyDataStream, UserConsumerMobile | ThirdParty, UserConsumerWeb |
| 22 | `bqZWYmRAka0` | 80% | 80% | 80% | 40% | 80% | 53% | 7 | 5 | 10 | 5 | UserConsumerAPI | UserCompanyAgent |
| 23 | `JYeXbUdFOdw` | 75% | 86% | 80% | 38% | 36% | 37% | 13 | 8 | 13 | 14 | UserConsumerWeb | EC2, UserConsumerWebMobile |
| 24 | `gu54VVeDD10` | 86% | 75% | 80% | 67% | 44% | 53% | 7 | 8 | 6 | 9 | ECR, UserCompanyAnalyst | UserCompanyDeveloper |
| 25 | `c-1GXhOOOww` | 78% | 78% | 78% | 45% | 31% | 37% | 9 | 9 | 11 | 16 | ThirdParty, UserConsumerMobile | CloudFront, UserConsumerWeb |
| 26 | `4WjXH8Wp0E4` | 88% | 70% | 78% | 82% | 41% | 55% | 12 | 14 | 11 | 22 | ThirdParty, UserConsumerHospital, UserConsumerWeb | UserCompanyAgent |
| 27 | `6iK4WNj6QqI` | 71% | 83% | 77% | 43% | 30% | 35% | 7 | 6 | 7 | 10 | UserConsumerWeb | CloudFront, UserConsumerWebMobile |
| 28 | `GoziWpmFCS0` | 60% | 100% | 75% | 18% | 100% | 31% | 9 | 4 | 11 | 2 | — | UserCompanyDataStream, UserCompanyDomainExpert |
| 29 | `-3lnf5lzsH0` | 100% | 58% | 74% | 33% | 19% | 24% | 9 | 13 | 9 | 16 | CloudTrail, GuardDuty, SNS (+2) | — |
| 30 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 45% | 48% | 10 | 8 | 10 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 31 | `8ZRWzn0G39g` | 75% | 67% | 71% | 78% | 18% | 30% | 10 | 12 | 9 | 38 | EC2, ECS, UserConsumerAPI | UserCompanyAPI, UserConsumerWeb |

---
