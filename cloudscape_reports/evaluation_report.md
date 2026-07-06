# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-07-06 13:51:45*

## 1. Executive Summary (Side-by-Side Comparison)

This table compares performance metrics across all generated graph directories.

| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |
|---|---|---|---|---|---|---|
| **Standard (data/graphs)** | 70 | 75.8% | 72.5% | 42.5% | 75.1% | 1.28x |
| **Parsimonious API (data/graphs_parsimonious)** | 47 | 83.6% | 81.5% | 52.0% | 83.7% | 1.18x |

---

## Standard (data/graphs) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 9 | 0 | — | — |
| 2 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 77% | 71% | 74% | 10 | 10 | 13 | 14 | — | — |
| 3 | `Kebb0LOVC28` | 100% | 100% | 100% | 47% | 38% | 42% | 11 | 9 | 17 | 21 | — | — |
| 4 | `QnmmTIYZxNI` | 100% | 100% | 100% | 80% | 67% | 73% | 8 | 8 | 5 | 6 | — | — |
| 5 | `-3lnf5lzsH0` | 100% | 92% | 96% | 40% | 38% | 39% | 14 | 13 | 15 | 16 | OnPremDC | — |
| 6 | `07lfvavMdfU` | 91% | 100% | 95% | 71% | 71% | 71% | 12 | 10 | 14 | 14 | — | Lambda |
| 7 | `6YkguepAQuQ` | 100% | 90% | 95% | 38% | 30% | 33% | 9 | 10 | 8 | 10 | VPC | — |
| 8 | `6EUknQqaV1w` | 88% | 100% | 93% | 77% | 91% | 83% | 11 | 9 | 13 | 11 | — | SES |
| 9 | `1aYoIZvabbk` | 86% | 100% | 92% | 44% | 80% | 57% | 7 | 6 | 9 | 5 | — | EC2 |
| 10 | `Felt-hOU6kU` | 86% | 100% | 92% | 50% | 100% | 67% | 8 | 7 | 8 | 4 | — | VPC |
| 11 | `Ly_UhX3LCCs` | 80% | 100% | 89% | 20% | 29% | 24% | 7 | 7 | 10 | 7 | — | UserCompanyAPI |
| 12 | `2L0m28ZLmtE` | 85% | 92% | 88% | 15% | 36% | 21% | 15 | 13 | 27 | 11 | ThirdParty | CloudFormation, UserCompanyAnalyst |
| 13 | `IP03SkGbP-U` | 88% | 88% | 88% | 33% | 71% | 45% | 14 | 8 | 15 | 7 | UserConsumerWeb | UserConsumerWebMobile |
| 14 | `Pc7_uOdlGKo` | 88% | 88% | 88% | 45% | 56% | 50% | 9 | 9 | 11 | 9 | UserConsumerMobile | UserCompanyAnalyst |
| 15 | `-kA0ahrhX3I` | 86% | 86% | 86% | 25% | 50% | 33% | 11 | 9 | 16 | 8 | UserCompanyDeveloper | UserConsumerWeb |
| 16 | `Ccutfm_Srzw` | 86% | 86% | 86% | 38% | 36% | 37% | 11 | 11 | 13 | 14 | KinesisDataStream | ApiGateway |
| 17 | `GoziWpmFCS0` | 75% | 100% | 86% | 10% | 50% | 17% | 8 | 4 | 10 | 2 | — | UserCompanyDataStream |
| 18 | `NfUwtK8ALtw` | 86% | 86% | 86% | 80% | 75% | 77% | 9 | 9 | 15 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 19 | `wjtSHyENv0I` | 86% | 86% | 86% | 62% | 71% | 67% | 8 | 8 | 16 | 14 | UserConsumerWeb | UserCompanyAgent |
| 20 | `OQKOHNtyz3E` | 80% | 89% | 84% | 61% | 46% | 52% | 12 | 11 | 18 | 24 | UserConsumerMobile | UserCompanyAnalyst, UserConsumerWebMobile |
| 21 | `2e3vOxsHekE` | 83% | 83% | 83% | 67% | 67% | 67% | 6 | 6 | 6 | 6 | UserConsumerEdge | UserConsumerIOT |
| 22 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 23 | `PBa68gCG0Uk` | 83% | 83% | 83% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | ThirdParty | UserCompanyDataStream |
| 24 | `AS2JeM2FUzE` | 88% | 78% | 82% | 55% | 50% | 52% | 8 | 9 | 11 | 12 | UserConsumerWeb, VPCPeering | UserCompanyAnalyst |
| 25 | `H_S7CxtHgSM` | 78% | 88% | 82% | 41% | 58% | 48% | 11 | 11 | 17 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 26 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 27 | `JiWHomdh1oI` | 80% | 80% | 80% | 73% | 73% | 73% | 7 | 7 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 28 | `KQ6Fg206O9U` | 80% | 80% | 80% | 50% | 43% | 46% | 10 | 10 | 12 | 14 | Firehose, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 29 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 30 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 31 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 32 | `D77FSUkPJ3o` | 75% | 86% | 80% | 36% | 42% | 38% | 10 | 8 | 14 | 12 | UserConsumerWeb | KMS, UserCompanyInternalPlatform |
| 33 | `PgeQufaQy7I` | 86% | 75% | 80% | 83% | 62% | 71% | 7 | 8 | 6 | 8 | CloudFormation, UserConsumerWeb | UserConsumerWebMobile |
| 34 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 35 | `ww5fiygF6eg` | 75% | 86% | 80% | 69% | 45% | 55% | 11 | 10 | 13 | 20 | UserCompanyDrone | OnPremDC, UserCompanyAgent |
| 36 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 37 | `GJ1So_pbZWk` | 70% | 88% | 78% | 67% | 43% | 53% | 13 | 9 | 15 | 23 | UserConsumerWeb | ApiGateway, UserCompanyAnalyst, UserConsumerWebMobile |
| 38 | `Kp51k6LY-2c` | 70% | 88% | 78% | 20% | 25% | 22% | 14 | 8 | 20 | 16 | UserCompanyDataStream | DirectConnect, OnPremDC, ThirdParty |
| 39 | `LxeSC3-xMlk` | 70% | 88% | 78% | 41% | 60% | 49% | 10 | 8 | 22 | 15 | UserConsumerMobile | Lambda, UserCompanyDeveloper, UserConsumerWebMobile |
| 40 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 41 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 69% | 53% | 60% | 12 | 13 | 13 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 42 | `N2mktbl8EQk` | 71% | 83% | 77% | 45% | 56% | 50% | 7 | 6 | 11 | 9 | Kinesis | KinesisVideo, ThirdParty |
| 43 | `OWLGK-eVrTw` | 71% | 83% | 77% | 10% | 6% | 8% | 8 | 6 | 10 | 16 | UserConsumerAPI | EC2, UserCompanyAPI |
| 44 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 45 | `FfSNnH2bbNc` | 75% | 75% | 75% | 67% | 42% | 52% | 8 | 8 | 12 | 19 | UserConsumerSatellite, UserConsumerWeb | ThirdParty, UserConsumerWebMobile |
| 46 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 47 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 48 | `KzJKdUZ3Ba4` | 60% | 100% | 75% | 30% | 50% | 37% | 5 | 4 | 10 | 6 | — | SAP, UserCompanyAgent |
| 49 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 50 | `-wLEkq21cvA` | 67% | 80% | 73% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | UserCompanyAgent | OnPremDC, UserCompanyDeveloper |
| 51 | `INog0_9tCtY` | 67% | 80% | 73% | 53% | 53% | 53% | 18 | 14 | 19 | 19 | OpenSearch, UserCompanyAnalyst | CloudWatch, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 52 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 53 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 54 | `M_hqigB9C4I` | 67% | 75% | 71% | 56% | 31% | 40% | 9 | 9 | 9 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 55 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 56 | `G07keU4g-LU` | 64% | 78% | 70% | 37% | 48% | 42% | 20 | 10 | 27 | 21 | UserConsumerMobile, UserConsumerPOS | RDS, SageMaker, UserCompanyAgent (+1) |
| 57 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 58 | `MbkLJ62jtMc` | 56% | 83% | 67% | 17% | 75% | 27% | 17 | 6 | 18 | 4 | UserCompanyAPI | ApiGateway, SES, ThirdParty (+1) |
| 59 | `Ozbv9qBsDG8` | 54% | 88% | 67% | 28% | 41% | 33% | 17 | 11 | 25 | 17 | ThirdParty | CloudFormation, CloudWatch, DynamoDB (+3) |
| 60 | `JRDGId6N49E` | 57% | 80% | 67% | 9% | 33% | 14% | 10 | 6 | 11 | 3 | ThirdParty | FSX, UserCompanyDeveloper, UserCompanyInternalPlatform |
| 61 | `K5ww_O4vsxo` | 60% | 75% | 67% | 85% | 33% | 47% | 15 | 15 | 20 | 52 | DirectConnect | OnPremDC, UserConsumerMobile |
| 62 | `KywvGM6HVXI` | 60% | 67% | 63% | 50% | 27% | 35% | 13 | 11 | 12 | 22 | EC2, Kinesis, UserConsumerWeb | EKS, KinesisDataStream, ThirdParty (+1) |
| 63 | `DAJZAygxDZA` | 57% | 67% | 62% | 15% | 13% | 14% | 9 | 8 | 13 | 15 | ModelRegistry, UserCompanyAnalyst | ApiGateway, StepFunctions, UserCompanyDomainExpert |
| 64 | `99nNHsbwBpg` | 40% | 100% | 57% | 0% | 0% | 0% | 7 | 2 | 9 | 0 | — | ELB, ThirdParty, UserConsumerWebMobile |
| 65 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 66 | `LYP98nPBj2A` | 36% | 100% | 53% | 11% | 50% | 18% | 16 | 5 | 36 | 8 | — | CloudWatch, Macie, SecurityHub (+4) |
| 67 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 68 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |
| 69 | `HcmEFZukA-Y` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 9 | 0 | 15 | ApiGateway, EventBridge, Lambda (+6) | — |
| 70 | `JSBB-BCvavQ` | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 5 | 0 | 0 | Aurora, BeanStalk, EC2 (+2) | — |

---

## Parsimonious API (data/graphs_parsimonious) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `07lfvavMdfU` | 100% | 100% | 100% | 91% | 71% | 80% | 10 | 10 | 11 | 14 | — | — |
| 2 | `62E9ggjGS8I` | 100% | 100% | 100% | 100% | 44% | 62% | 7 | 7 | 4 | 9 | — | — |
| 3 | `6YkguepAQuQ` | 100% | 100% | 100% | 43% | 30% | 35% | 10 | 10 | 7 | 10 | — | — |
| 4 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 5 | 0 | — | — |
| 5 | `99nNHsbwBpg` | 100% | 100% | 100% | 0% | 0% | 0% | 5 | 2 | 4 | 0 | — | — |
| 6 | `9Cg81Xgg7LQ` | 100% | 100% | 100% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | — | — |
| 7 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 8 | `QnmmTIYZxNI` | 100% | 100% | 100% | 40% | 33% | 36% | 8 | 8 | 5 | 6 | — | — |
| 9 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 86% | 92% | 7 | 7 | 6 | 7 | — | — |
| 10 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 45% | 62% | 7 | 7 | 5 | 11 | — | — |
| 11 | `lkDq9g43djw` | 100% | 100% | 100% | 50% | 50% | 50% | 7 | 5 | 4 | 4 | — | — |
| 12 | `2L0m28ZLmtE` | 92% | 100% | 96% | 83% | 91% | 87% | 14 | 13 | 12 | 11 | — | UserCompanyAnalyst |
| 13 | `bikXzsVihF4` | 88% | 100% | 93% | 57% | 40% | 47% | 8 | 7 | 7 | 10 | — | ServiceNow |
| 14 | `unFVfqj9cQ8` | 100% | 88% | 93% | 100% | 86% | 92% | 7 | 8 | 6 | 7 | ControlTower | — |
| 15 | `qi017F1UwvM` | 93% | 93% | 93% | 78% | 58% | 67% | 17 | 17 | 18 | 24 | UserConsumerWeb | UserCompanyWebsite |
| 16 | `1aYoIZvabbk` | 86% | 100% | 92% | 57% | 80% | 67% | 7 | 6 | 7 | 5 | — | AutoScaling |
| 17 | `5vR5aN_xdI0` | 100% | 86% | 92% | 62% | 50% | 56% | 9 | 9 | 8 | 10 | UserConsumerAPI | — |
| 18 | `AS2JeM2FUzE` | 89% | 89% | 89% | 89% | 67% | 76% | 9 | 9 | 9 | 12 | UserCompanyDataStream | ThirdParty |
| 19 | `0F7KDLz-kIQ` | 83% | 91% | 87% | 82% | 50% | 62% | 14 | 13 | 17 | 28 | UserConsumerWeb | CloudFormation, ECS |
| 20 | `-kA0ahrhX3I` | 86% | 86% | 86% | 50% | 62% | 56% | 11 | 9 | 10 | 8 | UserCompanyDeveloper | UserCompanyAnalyst |
| 21 | `5f3z1Z_9BJA` | 86% | 86% | 86% | 91% | 59% | 71% | 11 | 11 | 11 | 17 | UserCompanyDataStream | ThirdParty |
| 22 | `6EUknQqaV1w` | 86% | 86% | 86% | 73% | 73% | 73% | 8 | 9 | 11 | 11 | UserCompanyDataStream | EC2 |
| 23 | `Ccutfm_Srzw` | 86% | 86% | 86% | 60% | 43% | 50% | 10 | 11 | 10 | 14 | Kinesis | KinesisAnalytics |
| 24 | `D77FSUkPJ3o` | 86% | 86% | 86% | 70% | 58% | 64% | 8 | 8 | 10 | 12 | UserConsumerWeb | UserCompanyAgent |
| 25 | `2e3vOxsHekE` | 83% | 83% | 83% | 75% | 50% | 60% | 6 | 6 | 4 | 6 | UserConsumerEdge | UserCompanyEdge |
| 26 | `pk5yddJpC_8` | 83% | 83% | 83% | 78% | 70% | 74% | 9 | 9 | 9 | 10 | UserCompanyDeveloper | UserCompanyAnalyst |
| 27 | `rPGLNw1cOGM` | 83% | 83% | 83% | 89% | 40% | 55% | 8 | 8 | 9 | 20 | UserConsumerWeb | UserCompanyDomainExpert |
| 28 | `6LcSv9XocTY` | 88% | 78% | 82% | 67% | 33% | 44% | 10 | 11 | 9 | 18 | Firehose, UserConsumerWeb | UserConsumerWebMobile |
| 29 | `1xLjtJnfZes` | 86% | 75% | 80% | 67% | 67% | 67% | 8 | 8 | 6 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 30 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserConsumerWebMobile |
| 31 | `JYeXbUdFOdw` | 75% | 86% | 80% | 38% | 36% | 37% | 13 | 8 | 13 | 14 | UserConsumerWeb | EC2, UserConsumerWebMobile |
| 32 | `D6rG9eZ5Qus` | 78% | 78% | 78% | 62% | 56% | 59% | 9 | 9 | 8 | 9 | ThirdParty, UserCompanyDataStream | OnPremDC, SystemsManager |
| 33 | `6iK4WNj6QqI` | 71% | 83% | 77% | 43% | 30% | 35% | 7 | 6 | 7 | 10 | UserConsumerWeb | CloudFront, UserConsumerWebMobile |
| 34 | `D9qTotVJYss` | 71% | 83% | 77% | 67% | 40% | 50% | 7 | 6 | 6 | 10 | UserCompanyAgent | EventBridge, UserCompanyInternalPlatform |
| 35 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 36 | `GoziWpmFCS0` | 60% | 100% | 75% | 18% | 100% | 31% | 9 | 4 | 11 | 2 | — | UserCompanyDataStream, UserCompanyDomainExpert |
| 37 | `-3lnf5lzsH0` | 100% | 58% | 74% | 33% | 19% | 24% | 9 | 13 | 9 | 16 | CloudTrail, GuardDuty, SNS (+2) | — |
| 38 | `7wBOFcP1HwA` | 70% | 78% | 74% | 50% | 40% | 44% | 11 | 10 | 8 | 10 | ELB, UserConsumerWeb | ALB, EC2, UserConsumerWebMobile |
| 39 | `DAJZAygxDZA` | 80% | 67% | 73% | 22% | 13% | 17% | 9 | 8 | 9 | 15 | ThirdParty, UserCompanyAnalyst | StepFunctions |
| 40 | `2XVgpMwY5iE` | 71% | 71% | 71% | 56% | 42% | 48% | 8 | 7 | 9 | 12 | UserCompanyAgent, UserCompanyDataStream | ThirdParty, UserConsumerHospital |
| 41 | `4-teOQ_dJvY` | 71% | 71% | 71% | 67% | 62% | 64% | 10 | 9 | 12 | 13 | UserCompanyAPI, UserCompanyEdge | ThirdParty, UserCompanyInternalPlatform |
| 42 | `3WgTBTDlQN8` | 75% | 67% | 71% | 50% | 36% | 42% | 9 | 9 | 10 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 43 | `8ZRWzn0G39g` | 75% | 67% | 71% | 78% | 18% | 30% | 10 | 12 | 9 | 38 | EC2, ECS, UserConsumerAPI | UserCompanyAPI, UserConsumerWeb |
| 44 | `-wLEkq21cvA` | 57% | 80% | 67% | 45% | 50% | 48% | 11 | 9 | 11 | 10 | UserCompanyAgent | AMI, OnPremDC, UserCompanyDeveloper |
| 45 | `BPvr0qWpJlA` | 60% | 67% | 63% | 33% | 33% | 33% | 11 | 10 | 9 | 9 | UserCompanyCRM, UserCompanyDataStream, UserConsumerMobile | EC2, SES, ThirdParty (+1) |
| 46 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 25% | 22% | 24% | 8 | 7 | 8 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 47 | `BgT_bDAejSQ` | 17% | 100% | 29% | 0% | 0% | 0% | 9 | 2 | 6 | 1 | — | ALB, NAT, OnPremDC (+2) |

---
