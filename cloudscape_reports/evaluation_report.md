# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-07-19 19:40:40*

## 1. Executive Summary (Side-by-Side Comparison)

This table compares performance metrics across all generated graph directories.

| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |
|---|---|---|---|---|---|---|
| **Standard (data/graphs)** | 63 | 75.7% | 71.5% | 45.0% | 71.5% | 1.17x |
| **Parsimonious API (data/graphs_parsimonious)** | 94 | 84.9% | 83.4% | 56.6% | 91.6% | 1.06x |

### Fleiss's Kappa Inter-Rater Reliability

Fleiss's Kappa measures agreement among 3 raters (Ground Truth, Standard, and Parsimonious) 
across all 45 shared videos and 169 services:

- **Fleiss's Kappa (K):** `0.7887`

- **Interpretation:** Acuerdo sustancial


---

## Standard (data/graphs) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

### Detailed Results Table: Core Evaluation (Valid Ground Truths)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `CsD5bmM6mpY` | 100% | 100% | 100% | 100% | 100% | 100% | 6 | 6 | 7 | 7 | — | — |
| 2 | `Kebb0LOVC28` | 100% | 100% | 100% | 47% | 38% | 42% | 11 | 9 | 17 | 21 | — | — |
| 3 | `l0mvXogANE4` | 100% | 100% | 100% | 100% | 79% | 88% | 9 | 8 | 11 | 14 | — | — |
| 4 | `wjtSHyENv0I` | 100% | 100% | 100% | 78% | 50% | 61% | 8 | 8 | 9 | 14 | — | — |
| 5 | `Felt-hOU6kU` | 86% | 100% | 92% | 50% | 100% | 67% | 8 | 7 | 8 | 4 | — | VPC |
| 6 | `2L0m28ZLmtE` | 92% | 92% | 92% | 53% | 82% | 64% | 14 | 13 | 17 | 11 | EC2 | UserConsumerWeb |
| 7 | `Ly_UhX3LCCs` | 80% | 100% | 89% | 20% | 29% | 24% | 7 | 7 | 10 | 7 | — | UserCompanyAPI |
| 8 | `Pc7_uOdlGKo` | 88% | 88% | 88% | 45% | 56% | 50% | 9 | 9 | 11 | 9 | UserConsumerMobile | UserCompanyAnalyst |
| 9 | `07lfvavMdfU` | 82% | 90% | 86% | 69% | 64% | 67% | 11 | 10 | 13 | 14 | MediaConvert | Lambda, ThirdParty |
| 10 | `NfUwtK8ALtw` | 86% | 86% | 86% | 80% | 75% | 77% | 9 | 9 | 15 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 11 | `6CgqEzyWpeA` | 80% | 89% | 84% | 69% | 58% | 63% | 13 | 12 | 16 | 19 | UserConsumerWebMobile | ThirdParty, UserConsumerWeb |
| 12 | `OQKOHNtyz3E` | 80% | 89% | 84% | 61% | 46% | 52% | 12 | 11 | 18 | 24 | UserConsumerMobile | UserCompanyAnalyst, UserConsumerWebMobile |
| 13 | `D9qTotVJYss` | 83% | 83% | 83% | 44% | 40% | 42% | 6 | 6 | 9 | 10 | UserCompanyAgent | UserCompanyInternalPlatform |
| 14 | `AS2JeM2FUzE` | 88% | 78% | 82% | 55% | 50% | 52% | 8 | 9 | 11 | 12 | UserConsumerWeb, VPCPeering | UserCompanyAnalyst |
| 15 | `H_S7CxtHgSM` | 78% | 88% | 82% | 41% | 58% | 48% | 11 | 11 | 17 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 16 | `-3lnf5lzsH0` | 90% | 75% | 82% | 64% | 56% | 60% | 14 | 13 | 14 | 16 | EC2, OnPremDC, UserCompanyAnalyst | UserConsumerWeb |
| 17 | `0F7KDLz-kIQ` | 82% | 82% | 82% | 45% | 32% | 38% | 12 | 13 | 20 | 28 | Fargate, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 18 | `BZ32w0SSAoY` | 80% | 80% | 80% | 86% | 63% | 73% | 7 | 7 | 14 | 19 | UserConsumerWeb | RDS |
| 19 | `JiWHomdh1oI` | 80% | 80% | 80% | 73% | 73% | 73% | 7 | 7 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 20 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 7 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 21 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserCompanyAgent |
| 22 | `5f3z1Z_9BJA` | 75% | 86% | 80% | 40% | 35% | 38% | 12 | 11 | 15 | 17 | UserCompanyDataStream | ThirdParty, UserCompanyAnalyst |
| 23 | `G5tNCpmD2uQ` | 86% | 75% | 80% | 60% | 25% | 35% | 11 | 9 | 5 | 12 | ALB, UserConsumerMobile | ThirdParty |
| 24 | `PgeQufaQy7I` | 86% | 75% | 80% | 83% | 62% | 71% | 7 | 8 | 6 | 8 | CloudFormation, UserConsumerWeb | UserConsumerWebMobile |
| 25 | `Yju3yReAQtc` | 75% | 86% | 80% | 31% | 57% | 40% | 13 | 7 | 13 | 7 | UserCompanyInternalPlatform | EC2, UserConsumerWeb |
| 26 | `7wBOFcP1HwA` | 78% | 78% | 78% | 35% | 60% | 44% | 11 | 10 | 17 | 10 | ThirdParty, UserConsumerWeb | EC2, UserConsumerWebMobile |
| 27 | `GJ1So_pbZWk` | 70% | 88% | 78% | 67% | 43% | 53% | 13 | 9 | 15 | 23 | UserConsumerWeb | ApiGateway, UserCompanyAnalyst, UserConsumerWebMobile |
| 28 | `LxeSC3-xMlk` | 70% | 88% | 78% | 41% | 60% | 49% | 10 | 8 | 22 | 15 | UserConsumerMobile | Lambda, UserCompanyDeveloper, UserConsumerWebMobile |
| 29 | `-kA0ahrhX3I` | 83% | 71% | 77% | 0% | 0% | 0% | 11 | 9 | 8 | 8 | S3, UserCompanyDeveloper | UserConsumerWeb |
| 30 | `5vR5aN_xdI0` | 83% | 71% | 77% | 50% | 50% | 50% | 9 | 9 | 10 | 10 | ThirdParty, UserConsumerAPI | UserCompanyDataStream |
| 31 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 69% | 53% | 60% | 12 | 13 | 13 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 32 | `OWLGK-eVrTw` | 71% | 83% | 77% | 10% | 6% | 8% | 8 | 6 | 10 | 16 | UserConsumerAPI | EC2, UserCompanyAPI |
| 33 | `6LcSv9XocTY` | 67% | 89% | 76% | 56% | 50% | 53% | 13 | 11 | 16 | 18 | UserConsumerWeb | Kinesis, Lex, UserCompanyAgent (+1) |
| 34 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 35 | `gpWR5JBC64A` | 75% | 75% | 75% | 42% | 83% | 56% | 8 | 8 | 12 | 6 | UserCompanyAgent, UserConsumerMobile | UserCompanyAnalyst, UserConsumerPOS |
| 36 | `KzJKdUZ3Ba4` | 60% | 100% | 75% | 30% | 50% | 37% | 5 | 4 | 10 | 6 | — | SAP, UserCompanyAgent |
| 37 | `BPvr0qWpJlA` | 70% | 78% | 74% | 27% | 33% | 30% | 11 | 10 | 11 | 9 | UserCompanyCRM, UserCompanyDataStream | EC2, SES, ThirdParty |
| 38 | `6EUknQqaV1w` | 100% | 57% | 73% | 25% | 27% | 26% | 9 | 9 | 12 | 11 | KinesisDataStream, OpenSearch, UserCompanyDataStream | — |
| 39 | `INog0_9tCtY` | 67% | 80% | 73% | 53% | 53% | 53% | 18 | 14 | 19 | 19 | OpenSearch, UserCompanyAnalyst | CloudWatch, UserCompanyAgent, UserCompanyDeveloper (+1) |
| 40 | `2XVgpMwY5iE` | 71% | 71% | 71% | 36% | 42% | 38% | 8 | 7 | 14 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 41 | `3WgTBTDlQN8` | 75% | 67% | 71% | 43% | 43% | 43% | 11 | 9 | 14 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 42 | `M_hqigB9C4I` | 67% | 75% | 71% | 56% | 31% | 40% | 9 | 9 | 9 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 43 | `D6rG9eZ5Qus` | 64% | 78% | 70% | 50% | 56% | 53% | 11 | 9 | 10 | 9 | ThirdParty, UserCompanyDataStream | Lambda, SystemsManager, UserCompanyElementalLiveDevice (+1) |
| 44 | `G07keU4g-LU` | 64% | 78% | 70% | 37% | 48% | 42% | 20 | 10 | 27 | 21 | UserConsumerMobile, UserConsumerPOS | RDS, SageMaker, UserCompanyAgent (+1) |
| 45 | `MbkLJ62jtMc` | 56% | 83% | 67% | 17% | 75% | 27% | 17 | 6 | 18 | 4 | UserCompanyAPI | ApiGateway, SES, ThirdParty (+1) |
| 46 | `2e3vOxsHekE` | 67% | 67% | 67% | 60% | 50% | 55% | 6 | 6 | 5 | 6 | UserCompanyAnalyst, UserConsumerEdge | ThirdParty, UserConsumerWeb |
| 47 | `-wLEkq21cvA` | 75% | 60% | 67% | 45% | 50% | 48% | 9 | 9 | 11 | 10 | AppDiscovery, UserCompanyAgent | UserConsumerWeb |
| 48 | `KywvGM6HVXI` | 60% | 67% | 63% | 50% | 27% | 35% | 13 | 11 | 12 | 22 | EC2, Kinesis, UserConsumerWeb | EKS, KinesisDataStream, ThirdParty (+1) |
| 49 | `DAJZAygxDZA` | 57% | 67% | 62% | 15% | 13% | 14% | 9 | 8 | 13 | 15 | ModelRegistry, UserCompanyAnalyst | ApiGateway, StepFunctions, UserCompanyDomainExpert |
| 50 | `ww5fiygF6eg` | 100% | 43% | 60% | 12% | 5% | 7% | 8 | 10 | 8 | 20 | Lambda, S3, StorageGateway (+1) | — |
| 51 | `4-teOQ_dJvY` | 57% | 57% | 57% | 42% | 38% | 40% | 9 | 9 | 12 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, ThirdParty, UserCompanyInternalPlatform |
| 52 | `Cgv0kfp_6xQ` | 60% | 50% | 55% | 0% | 0% | 0% | 11 | 10 | 10 | 14 | EKS, S3, UserConsumerMobile | ThirdParty, UserConsumerWeb |
| 53 | `LYP98nPBj2A` | 36% | 100% | 53% | 11% | 50% | 18% | 16 | 5 | 36 | 8 | — | CloudWatch, Macie, SecurityHub (+4) |
| 54 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 33% | 33% | 33% | 8 | 7 | 9 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 55 | `6YkguepAQuQ` | 67% | 40% | 50% | 11% | 10% | 11% | 10 | 10 | 9 | 10 | ALB, ECR, ECS (+3) | ThirdParty, UserConsumerWeb |
| 56 | `1aYoIZvabbk` | 33% | 17% | 22% | 0% | 0% | 0% | 7 | 6 | 7 | 5 | ALB, EKS, SNS (+2) | ThirdParty, UserConsumerWeb |


### Detailed Results Table: Excluded Validation (Invalid/Placeholder Ground Truths)

> [!NOTE]

> These graphs are excluded from the main average F1 calculations above.

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 9 | 0 | — | — |
| 2 | `QnmmTIYZxNI` | 100% | 100% | 100% | 80% | 67% | 73% | 8 | 8 | 5 | 6 | — | — |
| 3 | `GoziWpmFCS0` | 75% | 100% | 86% | 10% | 50% | 17% | 8 | 4 | 10 | 2 | — | UserCompanyDataStream |
| 4 | `62E9ggjGS8I` | 56% | 83% | 67% | 17% | 22% | 19% | 9 | 7 | 12 | 9 | VPC | EC2, EKS, Lambda (+1) |
| 5 | `K5ww_O4vsxo` | 60% | 75% | 67% | 85% | 33% | 47% | 15 | 15 | 20 | 52 | DirectConnect | OnPremDC, UserConsumerMobile |
| 6 | `99nNHsbwBpg` | 40% | 100% | 57% | 0% | 0% | 0% | 7 | 2 | 9 | 0 | — | ELB, ThirdParty, UserConsumerWebMobile |
| 7 | `BgT_bDAejSQ` | 11% | 100% | 20% | 0% | 0% | 0% | 12 | 2 | 9 | 1 | — | ALB, DirectConnect, NAT (+5) |



---

## Parsimonious API (data/graphs_parsimonious) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

### Detailed Results Table: Core Evaluation (Valid Ground Truths)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `-wLEkq21cvA` | 100% | 100% | 100% | 80% | 80% | 80% | 9 | 9 | 10 | 10 | — | — |
| 2 | `07lfvavMdfU` | 100% | 100% | 100% | 91% | 71% | 80% | 10 | 10 | 11 | 14 | — | — |
| 3 | `6YkguepAQuQ` | 100% | 100% | 100% | 43% | 30% | 35% | 10 | 10 | 7 | 10 | — | — |
| 4 | `9Cg81Xgg7LQ` | 100% | 100% | 100% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | — | — |
| 5 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 6 | `G5tNCpmD2uQ` | 100% | 100% | 100% | 71% | 42% | 53% | 10 | 9 | 7 | 12 | — | — |
| 7 | `H2fOkeXxpyw` | 100% | 100% | 100% | 100% | 70% | 82% | 8 | 8 | 7 | 10 | — | — |
| 8 | `JcHSFIZMYHc` | 100% | 100% | 100% | 100% | 89% | 94% | 8 | 8 | 8 | 9 | — | — |
| 9 | `Jz2RPRhF6Fs` | 100% | 100% | 100% | 100% | 69% | 82% | 10 | 10 | 9 | 13 | — | — |
| 10 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 86% | 92% | 7 | 7 | 6 | 7 | — | — |
| 11 | `iKYvG5aiIn8` | 100% | 100% | 100% | 75% | 86% | 80% | 9 | 9 | 8 | 7 | — | — |
| 12 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 45% | 62% | 7 | 7 | 5 | 11 | — | — |
| 13 | `l0mvXogANE4` | 100% | 100% | 100% | 100% | 79% | 88% | 9 | 8 | 11 | 14 | — | — |
| 14 | `lkDq9g43djw` | 100% | 100% | 100% | 50% | 50% | 50% | 7 | 5 | 4 | 4 | — | — |
| 15 | `2L0m28ZLmtE` | 92% | 100% | 96% | 83% | 91% | 87% | 14 | 13 | 12 | 11 | — | UserCompanyAnalyst |
| 16 | `Eoq7E6jMtBs` | 90% | 100% | 95% | 64% | 35% | 45% | 10 | 10 | 11 | 20 | — | UserCompanyAgent |
| 17 | `0gNMEyei-co` | 100% | 89% | 94% | 82% | 69% | 75% | 9 | 9 | 11 | 13 | UserCompanyDataStream | — |
| 18 | `0wnNlOg42dc` | 89% | 100% | 94% | 89% | 67% | 76% | 9 | 8 | 9 | 12 | — | UserConsumerWeb |
| 19 | `LxeSC3-xMlk` | 89% | 100% | 94% | 78% | 47% | 58% | 10 | 8 | 9 | 15 | — | UserConsumerWeb |
| 20 | `-ahWdCysMYw` | 100% | 88% | 93% | 20% | 11% | 14% | 7 | 8 | 5 | 9 | UserCompanyAnalyst | — |
| 21 | `bikXzsVihF4` | 88% | 100% | 93% | 57% | 40% | 47% | 8 | 7 | 7 | 10 | — | ServiceNow |
| 22 | `unFVfqj9cQ8` | 100% | 88% | 93% | 100% | 86% | 92% | 7 | 8 | 6 | 7 | ControlTower | — |
| 23 | `qi017F1UwvM` | 93% | 93% | 93% | 78% | 58% | 67% | 17 | 17 | 18 | 24 | UserConsumerWeb | UserCompanyWebsite |
| 24 | `1aYoIZvabbk` | 86% | 100% | 92% | 57% | 80% | 67% | 7 | 6 | 7 | 5 | — | AutoScaling |
| 25 | `5vR5aN_xdI0` | 100% | 86% | 92% | 62% | 50% | 56% | 9 | 9 | 8 | 10 | UserConsumerAPI | — |
| 26 | `CsD5bmM6mpY` | 86% | 100% | 92% | 43% | 43% | 43% | 8 | 6 | 7 | 7 | — | ThirdParty |
| 27 | `ErXwuwF2mRU` | 82% | 100% | 90% | 50% | 50% | 50% | 11 | 9 | 10 | 10 | — | Aurora, ThirdParty |
| 28 | `JG5p-i8Cr2E` | 90% | 90% | 90% | 77% | 42% | 54% | 11 | 11 | 13 | 24 | UserCompanyDeveloper | UserCompanyAgent |
| 29 | `INog0_9tCtY` | 100% | 80% | 89% | 73% | 42% | 53% | 12 | 14 | 11 | 19 | OpenSearch, UserCompanyAnalyst | — |
| 30 | `6CgqEzyWpeA` | 89% | 89% | 89% | 77% | 53% | 62% | 12 | 12 | 13 | 19 | UserConsumerWebMobile | UserConsumerWeb |
| 31 | `AS2JeM2FUzE` | 89% | 89% | 89% | 89% | 67% | 76% | 9 | 9 | 9 | 12 | UserCompanyDataStream | ThirdParty |
| 32 | `Gds8hl8dKuo` | 78% | 100% | 88% | 43% | 25% | 32% | 10 | 8 | 7 | 12 | — | STS, VPC |
| 33 | `0F7KDLz-kIQ` | 83% | 91% | 87% | 82% | 50% | 62% | 14 | 13 | 17 | 28 | UserConsumerWeb | CloudFormation, ECS |
| 34 | `2f_NYiPJQt4` | 82% | 90% | 86% | 50% | 33% | 40% | 11 | 10 | 6 | 9 | S2SVPN | ThirdParty, UserConsumerWeb |
| 35 | `-kA0ahrhX3I` | 86% | 86% | 86% | 50% | 62% | 56% | 11 | 9 | 10 | 8 | UserCompanyDeveloper | UserCompanyAnalyst |
| 36 | `37T7Nd8pL-c` | 86% | 86% | 86% | 57% | 33% | 42% | 7 | 8 | 7 | 12 | UserConsumerAPI | UserConsumerWeb |
| 37 | `5f3z1Z_9BJA` | 86% | 86% | 86% | 91% | 59% | 71% | 11 | 11 | 11 | 17 | UserCompanyDataStream | ThirdParty |
| 38 | `6EUknQqaV1w` | 86% | 86% | 86% | 73% | 73% | 73% | 8 | 9 | 11 | 11 | UserCompanyDataStream | EC2 |
| 39 | `E8wYXtvGy5k` | 86% | 86% | 86% | 89% | 67% | 76% | 10 | 10 | 9 | 12 | UserConsumerMobile | UserCompanyAgent |
| 40 | `Fd2c7NDYfpo` | 86% | 86% | 86% | 75% | 50% | 60% | 8 | 8 | 8 | 12 | ThirdParty | SES |
| 41 | `Felt-hOU6kU` | 75% | 100% | 86% | 50% | 100% | 67% | 9 | 7 | 8 | 4 | — | ThirdParty, VPC |
| 42 | `Jkx6kVbDpL4` | 86% | 86% | 86% | 88% | 82% | 85% | 13 | 13 | 16 | 17 | UserCompanyAnalyst | ThirdParty |
| 43 | `wjtSHyENv0I` | 86% | 86% | 86% | 71% | 36% | 48% | 8 | 8 | 7 | 14 | UserConsumerWeb | UserCompanyAgent |
| 44 | `HwHVFWdczVw` | 80% | 89% | 84% | 80% | 89% | 84% | 10 | 9 | 10 | 9 | UserConsumerWebMobile | ThirdParty, UserConsumerWeb |
| 45 | `2e3vOxsHekE` | 83% | 83% | 83% | 75% | 50% | 60% | 6 | 6 | 4 | 6 | UserConsumerEdge | UserCompanyEdge |
| 46 | `66fPHLmvikk` | 83% | 83% | 83% | 50% | 50% | 50% | 8 | 7 | 8 | 8 | UserCompanyAnalyst | UserCompanyDeveloper |
| 47 | `pk5yddJpC_8` | 83% | 83% | 83% | 78% | 70% | 74% | 9 | 9 | 9 | 10 | UserCompanyDeveloper | UserCompanyAnalyst |
| 48 | `rPGLNw1cOGM` | 83% | 83% | 83% | 89% | 40% | 55% | 8 | 8 | 9 | 20 | UserConsumerWeb | UserCompanyDomainExpert |
| 49 | `-S-R7MWRpaI` | 100% | 71% | 83% | 50% | 36% | 42% | 9 | 8 | 8 | 11 | Firehose, Kinesis | — |
| 50 | `6LcSv9XocTY` | 88% | 78% | 82% | 67% | 33% | 44% | 10 | 11 | 9 | 18 | Firehose, UserConsumerWeb | UserConsumerWebMobile |
| 51 | `CE03UMddoYU` | 78% | 88% | 82% | 75% | 75% | 75% | 11 | 10 | 12 | 12 | UserConsumerEdge | UserConsumerIOT, UserConsumerMobile |
| 52 | `GJ1So_pbZWk` | 78% | 88% | 82% | 80% | 35% | 48% | 10 | 9 | 10 | 23 | UserConsumerWeb | UserCompanyAnalyst, UserConsumerAPI |
| 53 | `H_S7CxtHgSM` | 78% | 88% | 82% | 54% | 58% | 56% | 12 | 11 | 13 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 54 | `KiH7hVJKzns` | 78% | 88% | 82% | 70% | 50% | 58% | 9 | 8 | 10 | 14 | UserConsumerWebMobile | UserConsumerMobile, UserConsumerWeb |
| 55 | `6sew_hdI6cY` | 79% | 85% | 81% | 75% | 50% | 60% | 16 | 15 | 12 | 18 | EFS, OpenSearch | ThirdParty, UserCompanyAgent, UserConsumerWeb |
| 56 | `BZ32w0SSAoY` | 80% | 80% | 80% | 88% | 37% | 52% | 7 | 7 | 8 | 19 | ThirdParty | RDS |
| 57 | `JiWHomdh1oI` | 80% | 80% | 80% | 89% | 73% | 80% | 7 | 7 | 9 | 11 | UserCompanyDataStream | ThirdParty |
| 58 | `LYP98nPBj2A` | 67% | 100% | 80% | 43% | 38% | 40% | 8 | 5 | 7 | 8 | — | UserCompanyAgent, VPC |
| 59 | `0JxJpNjI9Y0` | 75% | 86% | 80% | 70% | 41% | 52% | 10 | 9 | 10 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserConsumerWeb |
| 60 | `1xLjtJnfZes` | 86% | 75% | 80% | 67% | 67% | 67% | 8 | 8 | 6 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerMobile |
| 61 | `5EmA67lSJEs` | 86% | 75% | 80% | 58% | 35% | 44% | 10 | 11 | 12 | 20 | UserConsumerAPI, UserConsumerWeb | UserConsumerWebMobile |
| 62 | `DnTQ3matqts` | 73% | 89% | 80% | 47% | 57% | 52% | 15 | 14 | 17 | 14 | UserConsumerEdge | SNS, ThirdParty, UserConsumerWeb |
| 63 | `JYeXbUdFOdw` | 75% | 86% | 80% | 38% | 36% | 37% | 13 | 8 | 13 | 14 | UserConsumerWeb | EC2, UserConsumerWebMobile |
| 64 | `D6rG9eZ5Qus` | 78% | 78% | 78% | 62% | 56% | 59% | 9 | 9 | 8 | 9 | ThirdParty, UserCompanyDataStream | OnPremDC, SystemsManager |
| 65 | `G07keU4g-LU` | 78% | 78% | 78% | 55% | 29% | 37% | 10 | 10 | 11 | 21 | ThirdParty, UserCompanyAnalyst | EC2, RDS |
| 66 | `Kebb0LOVC28` | 100% | 62% | 77% | 83% | 24% | 37% | 6 | 9 | 6 | 21 | CodeBuild, ECR, UserCompanyDeveloper | — |
| 67 | `6iK4WNj6QqI` | 71% | 83% | 77% | 43% | 30% | 35% | 7 | 6 | 7 | 10 | UserConsumerWeb | CloudFront, UserConsumerWebMobile |
| 68 | `D9qTotVJYss` | 71% | 83% | 77% | 67% | 40% | 50% | 7 | 6 | 6 | 10 | UserCompanyAgent | EventBridge, UserCompanyInternalPlatform |
| 69 | `DrkaU99l9S8` | 73% | 80% | 76% | 54% | 54% | 54% | 11 | 12 | 13 | 13 | UserConsumerEdge, UserConsumerWeb | Greengrass, KinesisAnalytics, UserCompanyAnalyst |
| 70 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 71 | `-3lnf5lzsH0` | 100% | 58% | 74% | 33% | 19% | 24% | 9 | 13 | 9 | 16 | CloudTrail, GuardDuty, SNS (+2) | — |
| 72 | `7wBOFcP1HwA` | 70% | 78% | 74% | 50% | 40% | 44% | 11 | 10 | 8 | 10 | ELB, UserConsumerWeb | ALB, EC2, UserConsumerWebMobile |
| 73 | `DAJZAygxDZA` | 80% | 67% | 73% | 22% | 13% | 17% | 9 | 8 | 9 | 15 | ThirdParty, UserCompanyAnalyst | StepFunctions |
| 74 | `FmhL2334GIY` | 80% | 67% | 73% | 40% | 36% | 38% | 10 | 10 | 10 | 11 | ECS, UserCompanyWebsite | ThirdParty |
| 75 | `2XVgpMwY5iE` | 71% | 71% | 71% | 56% | 42% | 48% | 8 | 7 | 9 | 12 | UserCompanyAgent, UserCompanyDataStream | ThirdParty, UserConsumerHospital |
| 76 | `4-teOQ_dJvY` | 71% | 71% | 71% | 67% | 62% | 64% | 10 | 9 | 12 | 13 | UserCompanyAPI, UserCompanyEdge | ThirdParty, UserCompanyInternalPlatform |
| 77 | `3WgTBTDlQN8` | 75% | 67% | 71% | 50% | 36% | 42% | 9 | 9 | 10 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | ThirdParty, UserConsumerWebMobile |
| 78 | `8ZRWzn0G39g` | 75% | 67% | 71% | 78% | 18% | 30% | 10 | 12 | 9 | 38 | EC2, ECS, UserConsumerAPI | UserCompanyAPI, UserConsumerWeb |
| 79 | `ww5fiygF6eg` | 62% | 71% | 67% | 38% | 15% | 21% | 8 | 10 | 8 | 20 | CloudWatch, UserCompanyDrone | EventBridge, OnPremDC, UserCompanyAgent |
| 80 | `BPvr0qWpJlA` | 60% | 67% | 63% | 33% | 33% | 33% | 11 | 10 | 9 | 9 | UserCompanyCRM, UserCompanyDataStream, UserConsumerMobile | EC2, SES, ThirdParty (+1) |
| 81 | `Dxq_U1TNx1s` | 60% | 67% | 63% | 55% | 35% | 43% | 11 | 11 | 11 | 17 | Aurora, UserConsumerMobile, UserConsumerSatellite | RDS, ThirdParty, UserCompanyAgent (+1) |
| 82 | `KzJKdUZ3Ba4` | 50% | 67% | 57% | 25% | 17% | 20% | 7 | 4 | 4 | 6 | UserConsumerMobile | SAP, UserCompanyAgent |
| 83 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 25% | 22% | 24% | 8 | 7 | 8 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |


### Detailed Results Table: Excluded Validation (Invalid/Placeholder Ground Truths)

> [!NOTE]

> These graphs are excluded from the main average F1 calculations above.

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `62E9ggjGS8I` | 100% | 100% | 100% | 100% | 44% | 62% | 7 | 7 | 4 | 9 | — | — |
| 2 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 5 | 0 | — | — |
| 3 | `99nNHsbwBpg` | 100% | 100% | 100% | 0% | 0% | 0% | 5 | 2 | 4 | 0 | — | — |
| 4 | `LPZlrX2cNjo` | 100% | 100% | 100% | 50% | 50% | 50% | 4 | 4 | 4 | 4 | — | — |
| 5 | `QnmmTIYZxNI` | 100% | 100% | 100% | 40% | 33% | 36% | 8 | 8 | 5 | 6 | — | — |
| 6 | `1kWxymroGeE` | 83% | 100% | 91% | 33% | 75% | 46% | 8 | 5 | 9 | 4 | — | EC2 |
| 7 | `1ZLiRT0C2Yo` | 75% | 100% | 86% | 0% | 0% | 0% | 8 | 6 | 6 | 0 | — | OnPremDC, UserConsumerWeb |
| 8 | `9LhiUsg3knw` | 82% | 82% | 82% | 29% | 62% | 40% | 12 | 13 | 17 | 8 | UserCompanyDomainExpert, UserConsumerArtist | UserCompanyAgent, UserConsumerWeb |
| 9 | `GoziWpmFCS0` | 60% | 100% | 75% | 18% | 100% | 31% | 9 | 4 | 11 | 2 | — | UserCompanyDataStream, UserCompanyDomainExpert |
| 10 | `K5ww_O4vsxo` | 60% | 75% | 67% | 82% | 17% | 29% | 11 | 15 | 11 | 52 | ThirdParty | OnPremDC, S2SVPN |
| 11 | `BgT_bDAejSQ` | 17% | 100% | 29% | 0% | 0% | 0% | 9 | 2 | 6 | 1 | — | ALB, NAT, OnPremDC (+2) |



---
