# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-06-29 19:40:38*

## 1. Executive Summary (Side-by-Side Comparison)

This table compares performance metrics across all generated graph directories.

| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |
|---|---|---|---|---|---|---|
| **Standard (data/graphs)** | 99 | 77.7% | 74.8% | 44.8% | 75.1% | 1.25x |
| **Parsimonious API (data/graphs_parsimonious)** | 31 | 94.6% | 93.7% | 76.2% | 89.1% | 1.04x |

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
| 26 | `-kA0ahrhX3I` | 86% | 86% | 86% | 25% | 50% | 33% | 11 | 9 | 16 | 8 | UserCompanyDeveloper | UserConsumerWeb |
| 27 | `37T7Nd8pL-c` | 86% | 86% | 86% | 30% | 25% | 27% | 8 | 8 | 10 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 28 | `90rWUjKjnAE` | 86% | 86% | 86% | 27% | 30% | 29% | 9 | 8 | 11 | 10 | UserConsumerDeveloper | UserCompanyDeveloper |
| 29 | `Ccutfm_Srzw` | 86% | 86% | 86% | 38% | 36% | 37% | 11 | 11 | 13 | 14 | KinesisDataStream | ApiGateway |
| 30 | `GoziWpmFCS0` | 75% | 100% | 86% | 10% | 50% | 17% | 8 | 4 | 10 | 2 | — | UserCompanyDataStream |
| 31 | `NfUwtK8ALtw` | 86% | 86% | 86% | 80% | 75% | 77% | 9 | 9 | 15 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 32 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 33 | `0gNMEyei-co` | 80% | 89% | 84% | 64% | 69% | 67% | 13 | 9 | 14 | 13 | UserCompanyDataStream | Glue, UserCompanyAPI |
| 34 | `OQKOHNtyz3E` | 80% | 89% | 84% | 61% | 46% | 52% | 12 | 11 | 18 | 24 | UserConsumerMobile | UserCompanyAnalyst, UserConsumerWebMobile |
| 35 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 36 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 37 | `PBa68gCG0Uk` | 83% | 83% | 83% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | ThirdParty | UserCompanyDataStream |
| 38 | `AS2JeM2FUzE` | 88% | 78% | 82% | 55% | 50% | 52% | 8 | 9 | 11 | 12 | UserConsumerWeb, VPCPeering | UserCompanyAnalyst |
| 39 | `Dp3YAxFp-YM` | 78% | 88% | 82% | 73% | 57% | 64% | 10 | 10 | 11 | 14 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerMobile |
| 40 | `H_S7CxtHgSM` | 78% | 88% | 82% | 41% | 58% | 48% | 11 | 11 | 17 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 41 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 42 | `BZ32w0SSAoY` | 80% | 80% | 80% | 71% | 63% | 67% | 7 | 7 | 17 | 19 | ThirdParty | RDS |
| 43 | `JiWHomdh1oI` | 80% | 80% | 80% | 73% | 73% | 73% | 7 | 7 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 44 | `KQ6Fg206O9U` | 80% | 80% | 80% | 50% | 43% | 46% | 10 | 10 | 12 | 14 | Firehose, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 45 | `1ZLiRT0C2Yo` | 67% | 100% | 80% | 0% | 0% | 0% | 9 | 6 | 8 | 0 | — | OnPremDC, UserCompanyDeveloper, UserConsumerMobile |
| 46 | `8s0wGRkiDrw` | 67% | 100% | 80% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | UserCompanyAnalyst, UserConsumerWeb |
| 47 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 48 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 49 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 50 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 51 | `PgeQufaQy7I` | 86% | 75% | 80% | 83% | 62% | 71% | 7 | 8 | 6 | 8 | CloudFormation, UserConsumerWeb | UserConsumerWebMobile |
| 52 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 53 | `ww5fiygF6eg` | 75% | 86% | 80% | 69% | 45% | 55% | 11 | 10 | 13 | 20 | UserCompanyDrone | OnPremDC, UserCompanyAgent |
| 54 | `2f_NYiPJQt4` | 69% | 90% | 78% | 32% | 67% | 43% | 13 | 10 | 19 | 9 | S2SVPN | ThirdParty, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 55 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 56 | `0wnNlOg42dc` | 70% | 88% | 78% | 40% | 50% | 44% | 11 | 8 | 15 | 12 | ALB | ELB, RDS, UserCompanyAPI |
| 57 | `CTG23wd9H74` | 70% | 88% | 78% | 23% | 45% | 30% | 11 | 8 | 22 | 11 | UserCompanyAnalyst | Lambda, ThirdParty, UserCompanyDomainExpert |
| 58 | `GJ1So_pbZWk` | 70% | 88% | 78% | 67% | 43% | 53% | 13 | 9 | 15 | 23 | UserConsumerWeb | ApiGateway, UserCompanyAnalyst, UserConsumerWebMobile |
| 59 | `Kp51k6LY-2c` | 70% | 88% | 78% | 20% | 25% | 22% | 14 | 8 | 20 | 16 | UserCompanyDataStream | DirectConnect, OnPremDC, ThirdParty |
| 60 | `LxeSC3-xMlk` | 70% | 88% | 78% | 41% | 60% | 49% | 10 | 8 | 22 | 15 | UserConsumerMobile | Lambda, UserCompanyDeveloper, UserConsumerWebMobile |
| 61 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 62 | `7V8wTCkjOqo` | 71% | 83% | 77% | 24% | 57% | 33% | 9 | 7 | 17 | 7 | ThirdParty | SQS, UserCompanyDeveloper |
| 63 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 69% | 53% | 60% | 12 | 13 | 13 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 64 | `N2mktbl8EQk` | 71% | 83% | 77% | 45% | 56% | 50% | 7 | 6 | 11 | 9 | Kinesis | KinesisVideo, ThirdParty |
| 65 | `OWLGK-eVrTw` | 71% | 83% | 77% | 10% | 6% | 8% | 8 | 6 | 10 | 16 | UserConsumerAPI | EC2, UserCompanyAPI |
| 66 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 67 | `0JxJpNjI9Y0` | 67% | 86% | 75% | 65% | 65% | 65% | 11 | 9 | 17 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserCompanyDomainExpert, UserConsumerWebMobile |
| 68 | `FfSNnH2bbNc` | 75% | 75% | 75% | 67% | 42% | 52% | 8 | 8 | 12 | 19 | UserConsumerSatellite, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 69 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 70 | `KzJKdUZ3Ba4` | 60% | 100% | 75% | 30% | 50% | 37% | 5 | 4 | 10 | 6 | — | SAP, UserCompanyAgent |
| 71 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 72 | `5CwIt-Alqhg` | 73% | 73% | 73% | 40% | 50% | 44% | 11 | 11 | 15 | 12 | ALB, S3, SageMaker | ELB, UserCompanyAnalyst, UserConsumerIOT |
| 73 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 74 | `INog0_9tCtY` | 67% | 80% | 73% | 53% | 53% | 53% | 18 | 14 | 19 | 19 | OpenSearch, UserCompanyAnalyst | CloudWatch, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 75 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 36% | 42% | 9 | 8 | 8 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 76 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 77 | `9-a9Y5THTYo` | 62% | 83% | 71% | 56% | 83% | 67% | 9 | 7 | 9 | 6 | UserConsumerWeb | CodePipeline, Organizations, UserCompanyDeveloper |
| 78 | `CDCLwX2fo2g` | 71% | 71% | 71% | 67% | 57% | 62% | 7 | 8 | 12 | 14 | ALB, UserConsumerMobile | ELB, UserConsumerWeb |
| 79 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 80 | `M_hqigB9C4I` | 67% | 75% | 71% | 56% | 31% | 40% | 9 | 9 | 9 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 81 | `9qTEHITVeLE` | 60% | 86% | 71% | 30% | 43% | 35% | 11 | 9 | 20 | 14 | UserConsumerWeb | EC2, OpenSearch, UserCompanyAnalyst (+1) |
| 82 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 83 | `G07keU4g-LU` | 64% | 78% | 70% | 37% | 48% | 42% | 20 | 10 | 27 | 21 | UserConsumerMobile, UserConsumerPOS | RDS, SageMaker, UserCompanyAgent (+1) |
| 84 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 85 | `MbkLJ62jtMc` | 56% | 83% | 67% | 17% | 75% | 27% | 17 | 6 | 18 | 4 | UserCompanyAPI | ApiGateway, SES, ThirdParty (+1) |
| 86 | `Ozbv9qBsDG8` | 54% | 88% | 67% | 28% | 41% | 33% | 17 | 11 | 25 | 17 | ThirdParty | CloudFormation, CloudWatch, DynamoDB (+3) |
| 87 | `JRDGId6N49E` | 57% | 80% | 67% | 9% | 33% | 14% | 10 | 6 | 11 | 3 | ThirdParty | FSX, UserCompanyDeveloper, UserCompanyInternalPlatform |
| 88 | `6sY0AunanlM` | 60% | 75% | 67% | 0% | 0% | 0% | 8 | 4 | 8 | 0 | UserConsumerWeb | UserCompanyDeveloper, UserConsumerWebMobile |
| 89 | `K5ww_O4vsxo` | 60% | 75% | 67% | 85% | 33% | 47% | 15 | 15 | 20 | 52 | DirectConnect | OnPremDC, UserConsumerMobile |
| 90 | `KywvGM6HVXI` | 60% | 67% | 63% | 50% | 27% | 35% | 13 | 11 | 12 | 22 | EC2, Kinesis, UserConsumerWeb | EKS, KinesisDataStream, ThirdParty (+1) |
| 91 | `53sUjFv9ByI` | 57% | 67% | 62% | 50% | 50% | 50% | 7 | 6 | 6 | 6 | ThirdParty, UserCompanyDataStream | S3, UserCompanyAnalyst, UserCompanyDeveloper |
| 92 | `DAJZAygxDZA` | 57% | 67% | 62% | 15% | 13% | 14% | 9 | 8 | 13 | 15 | ModelRegistry, UserCompanyAnalyst | ApiGateway, StepFunctions, UserCompanyDomainExpert |
| 93 | `99nNHsbwBpg` | 40% | 100% | 57% | 0% | 0% | 0% | 7 | 2 | 9 | 0 | — | ELB, ThirdParty, UserConsumerWebMobile |
| 94 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 95 | `LYP98nPBj2A` | 36% | 100% | 53% | 11% | 50% | 18% | 16 | 5 | 36 | 8 | — | CloudWatch, Macie, SecurityHub (+4) |
| 96 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 97 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |
| 98 | `HcmEFZukA-Y` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 9 | 0 | 15 | ApiGateway, EventBridge, Lambda (+6) | — |
| 99 | `JSBB-BCvavQ` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 5 | 0 | 0 | Aurora, BeanStalk, EC2 (+2) | — |

---

## Parsimonious API (data/graphs_parsimonious) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `07lfvavMdfU` | 100% | 100% | 100% | 100% | 71% | 83% | 10 | 10 | 10 | 14 | — | — |
| 2 | `1SwHH7qQ6Pc` | 100% | 100% | 100% | 100% | 100% | 100% | 10 | 10 | 13 | 13 | — | — |
| 3 | `1VcpCVe3tLQ` | 100% | 100% | 100% | 100% | 100% | 100% | 12 | 12 | 13 | 13 | — | — |
| 4 | `6CgqEzyWpeA` | 100% | 100% | 100% | 100% | 100% | 100% | 12 | 12 | 19 | 19 | — | — |
| 5 | `6YkguepAQuQ` | 100% | 100% | 100% | 57% | 40% | 47% | 10 | 10 | 7 | 10 | — | — |
| 6 | `6iK4WNj6QqI` | 100% | 100% | 100% | 100% | 100% | 100% | 6 | 6 | 10 | 10 | — | — |
| 7 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 7 | 0 | — | — |
| 8 | `AzM_d7ZvzUE` | 100% | 100% | 100% | 100% | 55% | 71% | 11 | 11 | 11 | 20 | — | — |
| 9 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 10 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 11 | `JYeXbUdFOdw` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 14 | 14 | — | — |
| 12 | `bqZWYmRAka0` | 100% | 100% | 100% | 100% | 100% | 100% | 5 | 5 | 5 | 5 | — | — |
| 13 | `c-1GXhOOOww` | 100% | 100% | 100% | 100% | 100% | 100% | 9 | 9 | 16 | 16 | — | — |
| 14 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 100% | 100% | 7 | 7 | 7 | 7 | — | — |
| 15 | `gu54VVeDD10` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 9 | 9 | — | — |
| 16 | `iKYvG5aiIn8` | 100% | 100% | 100% | 75% | 86% | 80% | 9 | 9 | 8 | 7 | — | — |
| 17 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 100% | 100% | 7 | 7 | 11 | 11 | — | — |
| 18 | `lkDq9g43djw` | 100% | 100% | 100% | 100% | 100% | 100% | 5 | 5 | 4 | 4 | — | — |
| 19 | `pk5yddJpC_8` | 100% | 100% | 100% | 100% | 100% | 100% | 9 | 9 | 10 | 10 | — | — |
| 20 | `qi017F1UwvM` | 100% | 100% | 100% | 100% | 100% | 100% | 17 | 17 | 24 | 24 | — | — |
| 21 | `rPGLNw1cOGM` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 20 | 20 | — | — |
| 22 | `unFVfqj9cQ8` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 7 | 7 | — | — |
| 23 | `7LziNjUTo7w` | 89% | 100% | 94% | 91% | 62% | 74% | 9 | 9 | 11 | 16 | — | UserConsumerDeveloper |
| 24 | `bikXzsVihF4` | 88% | 100% | 93% | 57% | 40% | 47% | 8 | 7 | 7 | 10 | — | ServiceNow |
| 25 | `9yziTe6lBwk` | 90% | 90% | 90% | 89% | 50% | 64% | 10 | 10 | 9 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 26 | `-kA0ahrhX3I` | 86% | 86% | 86% | 50% | 62% | 56% | 11 | 9 | 10 | 8 | UserCompanyDeveloper | UserCompanyAnalyst |
| 27 | `4WjXH8Wp0E4` | 88% | 70% | 78% | 82% | 41% | 55% | 12 | 14 | 11 | 22 | ThirdParty, UserConsumerHospital, UserConsumerWeb | UserCompanyAgent |
| 28 | `GoziWpmFCS0` | 60% | 100% | 75% | 18% | 100% | 31% | 9 | 4 | 11 | 2 | — | UserCompanyDataStream, UserCompanyDomainExpert |
| 29 | `-3lnf5lzsH0` | 100% | 58% | 74% | 33% | 19% | 24% | 9 | 13 | 9 | 16 | CloudTrail, GuardDuty, SNS (+2) | — |
| 30 | `-S-R7MWRpaI` | 71% | 71% | 71% | 50% | 45% | 48% | 10 | 8 | 10 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, UserCompanyEdge |
| 31 | `8ZRWzn0G39g` | 75% | 67% | 71% | 78% | 18% | 30% | 10 | 12 | 9 | 38 | EC2, ECS, UserConsumerAPI | UserCompanyAPI, UserConsumerWeb |

---
