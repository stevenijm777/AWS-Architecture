# Combined Evaluation Report: Generated Graphs vs Cloudscape Ground Truth

*Generated: 2026-08-29 01:20:35*

## 1. Executive Summary (Side-by-Side Comparison)

This table compares performance metrics across all generated graph directories.

| Run Directory | Videos | Service F1 (unique) | Service F1 (multiset) | Edge F1 | Edge Type Acc | Node Ratio |
|---|---|---|---|---|---|---|
| **Standard (data/graphs)** | 385 | 86.7% | 84.3% | 59.3% | 61.4% | 1.03x |
| **Parsimonious API (data/graphs_parsimonious)** | 385 | 85.5% | 83.6% | 56.9% | 84.0% | 1.05x |

### Fleiss's Kappa Inter-Rater Reliability

Fleiss's Kappa measures agreement among 3 raters (Ground Truth, Standard, and Parsimonious) 
across all 336 shared videos and 169 services:

- **Fleiss's Kappa (K):** `0.8738`

- **Interpretation:** Acuerdo casi perfecto (Altamente confiable)


---

## Standard (data/graphs) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

### Detailed Results Table: Core Evaluation (Valid Ground Truths)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `1SwHH7qQ6Pc` | 100% | 100% | 100% | 86% | 46% | 60% | 10 | 10 | 7 | 13 | — | — |
| 2 | `66h7DrOEF5k` | 100% | 100% | 100% | 90% | 100% | 95% | 12 | 9 | 10 | 9 | — | — |
| 3 | `6YkguepAQuQ` | 100% | 100% | 100% | 100% | 40% | 57% | 10 | 10 | 4 | 10 | — | — |
| 4 | `7dtomip_VXc` | 100% | 100% | 100% | 88% | 64% | 74% | 8 | 8 | 8 | 11 | — | — |
| 5 | `8s0wGRkiDrw` | 100% | 100% | 100% | 67% | 100% | 80% | 7 | 5 | 6 | 4 | — | — |
| 6 | `9Cg81Xgg7LQ` | 100% | 100% | 100% | 71% | 71% | 71% | 7 | 7 | 7 | 7 | — | — |
| 7 | `A4Lfk1Zz1dE` | 100% | 100% | 100% | 14% | 20% | 17% | 8 | 8 | 7 | 5 | — | — |
| 8 | `AzM_d7ZvzUE` | 100% | 100% | 100% | 100% | 55% | 71% | 11 | 11 | 11 | 20 | — | — |
| 9 | `BX1K8x1lVLc` | 100% | 100% | 100% | 100% | 57% | 73% | 8 | 8 | 8 | 14 | — | — |
| 10 | `BlCXEMp_lqY` | 100% | 100% | 100% | 100% | 56% | 71% | 6 | 6 | 5 | 9 | — | — |
| 11 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 12 | `DkPPwq517aE` | 100% | 100% | 100% | 100% | 64% | 78% | 10 | 10 | 9 | 14 | — | — |
| 13 | `E8wYXtvGy5k` | 100% | 100% | 100% | 100% | 75% | 86% | 10 | 10 | 9 | 12 | — | — |
| 14 | `HcmEFZukA-Y` | 100% | 100% | 100% | 100% | 80% | 89% | 9 | 9 | 12 | 15 | — | — |
| 15 | `IV3KuMGVNXI` | 100% | 100% | 100% | 83% | 29% | 43% | 7 | 7 | 6 | 17 | — | — |
| 16 | `JG5p-i8Cr2E` | 100% | 100% | 100% | 86% | 50% | 63% | 11 | 11 | 14 | 24 | — | — |
| 17 | `JcHSFIZMYHc` | 100% | 100% | 100% | 100% | 89% | 94% | 8 | 8 | 8 | 9 | — | — |
| 18 | `KiH7hVJKzns` | 100% | 100% | 100% | 89% | 57% | 70% | 8 | 8 | 9 | 14 | — | — |
| 19 | `Q6r_QbYXFpg` | 100% | 100% | 100% | 100% | 100% | 100% | 11 | 11 | 9 | 9 | — | — |
| 20 | `Qi9soN5bpU4` | 100% | 100% | 100% | 100% | 70% | 82% | 8 | 8 | 7 | 10 | — | — |
| 21 | `Qz8uXtDC1bY` | 100% | 100% | 100% | 87% | 76% | 81% | 15 | 14 | 15 | 17 | — | — |
| 22 | `RCWl0rf8lpE` | 100% | 100% | 100% | 100% | 70% | 82% | 7 | 7 | 7 | 10 | — | — |
| 23 | `U8xlmurP-6o` | 100% | 100% | 100% | 80% | 80% | 80% | 12 | 10 | 10 | 10 | — | — |
| 24 | `Wur1GWB03hk` | 100% | 100% | 100% | 100% | 64% | 78% | 9 | 9 | 9 | 14 | — | — |
| 25 | `Xi6tDqctLsY` | 100% | 100% | 100% | 100% | 50% | 67% | 8 | 8 | 8 | 16 | — | — |
| 26 | `YlGUMhls9ZA` | 100% | 100% | 100% | 100% | 78% | 88% | 14 | 14 | 14 | 18 | — | — |
| 27 | `YrEc8oMIxDs` | 100% | 100% | 100% | 100% | 64% | 78% | 10 | 10 | 9 | 14 | — | — |
| 28 | `ZA_0RMeeWpY` | 100% | 100% | 100% | 71% | 62% | 67% | 8 | 5 | 7 | 8 | — | — |
| 29 | `ZNt9qI_LlPk` | 100% | 100% | 100% | 67% | 60% | 63% | 6 | 5 | 9 | 10 | — | — |
| 30 | `aN26J-7q9Hw` | 100% | 100% | 100% | 64% | 54% | 58% | 10 | 10 | 11 | 13 | — | — |
| 31 | `amh7nzl32v4` | 100% | 100% | 100% | 86% | 43% | 57% | 8 | 8 | 7 | 14 | — | — |
| 32 | `asZIXK7V-U4` | 100% | 100% | 100% | 100% | 81% | 90% | 10 | 10 | 13 | 16 | — | — |
| 33 | `az-C2c33trQ` | 100% | 100% | 100% | 100% | 53% | 69% | 8 | 8 | 9 | 17 | — | — |
| 34 | `bikXzsVihF4` | 100% | 100% | 100% | 71% | 50% | 59% | 8 | 7 | 7 | 10 | — | — |
| 35 | `c2TGPlvAHLs` | 100% | 100% | 100% | 80% | 80% | 80% | 6 | 6 | 5 | 5 | — | — |
| 36 | `chQ1phTqvnY` | 100% | 100% | 100% | 90% | 38% | 53% | 10 | 10 | 10 | 24 | — | — |
| 37 | `cnZeOytEkIM` | 100% | 100% | 100% | 67% | 67% | 67% | 8 | 6 | 6 | 6 | — | — |
| 38 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 86% | 92% | 7 | 7 | 6 | 7 | — | — |
| 39 | `h0HE3bOEiMk` | 100% | 100% | 100% | 89% | 89% | 89% | 7 | 7 | 9 | 9 | — | — |
| 40 | `hnMQFnTGr3I` | 100% | 100% | 100% | 100% | 50% | 67% | 12 | 9 | 12 | 24 | — | — |
| 41 | `hrhBOOrR5v0` | 100% | 100% | 100% | 89% | 67% | 76% | 8 | 9 | 9 | 12 | — | — |
| 42 | `ilsJgwcAshE` | 100% | 100% | 100% | 80% | 89% | 84% | 10 | 9 | 10 | 9 | — | — |
| 43 | `iwDNnyiD26M` | 100% | 100% | 100% | 58% | 78% | 67% | 10 | 9 | 12 | 9 | — | — |
| 44 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 45% | 62% | 7 | 7 | 5 | 11 | — | — |
| 45 | `jV8DwutbXbg` | 100% | 100% | 100% | 100% | 55% | 71% | 7 | 7 | 6 | 11 | — | — |
| 46 | `k7h0jpLcWdE` | 100% | 100% | 100% | 75% | 75% | 75% | 8 | 8 | 8 | 8 | — | — |
| 47 | `ktonI7J3kLY` | 100% | 100% | 100% | 60% | 38% | 46% | 6 | 5 | 5 | 8 | — | — |
| 48 | `l0mvXogANE4` | 100% | 100% | 100% | 100% | 79% | 88% | 9 | 8 | 11 | 14 | — | — |
| 49 | `lecbHMBD8KQ` | 100% | 100% | 100% | 71% | 62% | 67% | 12 | 12 | 7 | 8 | — | — |
| 50 | `lkDq9g43djw` | 100% | 100% | 100% | 75% | 75% | 75% | 7 | 5 | 4 | 4 | — | — |
| 51 | `mZxF1IJEsaY` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 8 | 8 | — | — |
| 52 | `mxKhbU_ToMs` | 100% | 100% | 100% | 100% | 69% | 82% | 9 | 9 | 9 | 13 | — | — |
| 53 | `nM-AkqNh7Yo` | 100% | 100% | 100% | 40% | 60% | 48% | 11 | 8 | 15 | 10 | — | — |
| 54 | `plce6pRdx6o` | 100% | 100% | 100% | 33% | 33% | 33% | 12 | 8 | 6 | 6 | — | — |
| 55 | `sSa4ikC8-Jc` | 100% | 100% | 100% | 83% | 42% | 56% | 13 | 11 | 12 | 24 | — | — |
| 56 | `uOSpWdAyrZo` | 100% | 100% | 100% | 78% | 100% | 88% | 9 | 8 | 9 | 7 | — | — |
| 57 | `uda9s3U7vFw` | 100% | 100% | 100% | 100% | 90% | 95% | 10 | 10 | 9 | 10 | — | — |
| 58 | `unFVfqj9cQ8` | 100% | 100% | 100% | 80% | 57% | 67% | 8 | 8 | 5 | 7 | — | — |
| 59 | `wE3TmHxyRdA` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 9 | 9 | — | — |
| 60 | `wzj2VQutJws` | 100% | 100% | 100% | 100% | 50% | 67% | 8 | 9 | 4 | 8 | — | — |
| 61 | `x76BIV88j_M` | 100% | 100% | 100% | 86% | 55% | 67% | 8 | 8 | 7 | 11 | — | — |
| 62 | `yXpd8gPfows` | 100% | 100% | 100% | 85% | 58% | 69% | 9 | 9 | 13 | 19 | — | — |
| 63 | `zr3Kib0i-OQ` | 100% | 100% | 100% | 100% | 100% | 100% | 9 | 7 | 6 | 6 | — | — |
| 64 | `2L0m28ZLmtE` | 92% | 100% | 96% | 67% | 73% | 70% | 14 | 13 | 12 | 11 | — | UserCompanyAnalyst |
| 65 | `6sew_hdI6cY` | 100% | 92% | 96% | 100% | 56% | 71% | 14 | 15 | 10 | 18 | EFS | — |
| 66 | `YosezjoL4MU` | 100% | 92% | 96% | 100% | 91% | 95% | 11 | 12 | 10 | 11 | UserCompanyAnalyst | — |
| 67 | `2f_NYiPJQt4` | 91% | 100% | 95% | 78% | 78% | 78% | 11 | 10 | 9 | 9 | — | UserConsumerWeb |
| 68 | `dAQhNjwkOX8` | 100% | 91% | 95% | 79% | 46% | 58% | 12 | 14 | 14 | 24 | UserConsumerAPI | — |
| 69 | `07lfvavMdfU` | 100% | 90% | 95% | 89% | 57% | 70% | 9 | 10 | 9 | 14 | UserConsumerWeb | — |
| 70 | `Eoq7E6jMtBs` | 90% | 100% | 95% | 69% | 45% | 55% | 10 | 10 | 13 | 20 | — | UserConsumerWeb |
| 71 | `J4vHfpL66Zk` | 100% | 90% | 95% | 100% | 65% | 79% | 9 | 10 | 11 | 17 | UserConsumerAPI | — |
| 72 | `OQKOHNtyz3E` | 90% | 100% | 95% | 75% | 38% | 50% | 12 | 11 | 12 | 24 | — | UserCompanyAnalyst |
| 73 | `rRvy5Fbei1s` | 100% | 90% | 95% | 82% | 69% | 75% | 11 | 13 | 11 | 13 | UserConsumerAPI | — |
| 74 | `vp8oPiHN4cA` | 100% | 90% | 95% | 45% | 26% | 33% | 9 | 14 | 11 | 19 | UserConsumerWeb | — |
| 75 | `0wnNlOg42dc` | 89% | 100% | 94% | 89% | 67% | 76% | 9 | 8 | 9 | 12 | — | ThirdParty |
| 76 | `4zVB5RbSTCo` | 100% | 89% | 94% | 100% | 43% | 60% | 8 | 9 | 6 | 14 | UserConsumerMobile | — |
| 77 | `5QbKp0LQaZo` | 89% | 100% | 94% | 50% | 31% | 38% | 10 | 10 | 10 | 16 | — | UserConsumerAPI |
| 78 | `7LziNjUTo7w` | 89% | 100% | 94% | 90% | 56% | 69% | 9 | 9 | 10 | 16 | — | UserCompanyDeveloper |
| 79 | `Cw26CrJUqv8` | 100% | 89% | 94% | 89% | 89% | 89% | 9 | 10 | 9 | 9 | UserConsumerWeb | — |
| 80 | `Dp3YAxFp-YM` | 89% | 100% | 94% | 82% | 64% | 72% | 10 | 10 | 11 | 14 | — | UserConsumerWebMobile |
| 81 | `HwHVFWdczVw` | 100% | 89% | 94% | 100% | 89% | 94% | 8 | 9 | 8 | 9 | UserConsumerWebMobile | — |
| 82 | `LxeSC3-xMlk` | 89% | 100% | 94% | 88% | 47% | 61% | 9 | 8 | 8 | 15 | — | UserConsumerWeb |
| 83 | `Ozbv9qBsDG8` | 89% | 100% | 94% | 75% | 35% | 48% | 11 | 11 | 8 | 17 | — | CloudFormation |
| 84 | `dy-drIboyNA` | 100% | 89% | 94% | 83% | 77% | 80% | 12 | 15 | 12 | 13 | UserConsumerAPI | — |
| 85 | `f5EJBUfGZtw` | 100% | 89% | 94% | 78% | 88% | 82% | 10 | 10 | 9 | 8 | UserConsumerAPI | — |
| 86 | `fRv8sOUyhZw` | 100% | 89% | 94% | 100% | 77% | 87% | 9 | 10 | 10 | 13 | UserCompanyAPI | — |
| 87 | `j9OZ-7aCAyA` | 100% | 89% | 94% | 83% | 33% | 48% | 8 | 9 | 6 | 15 | UserCompanyDataStream | — |
| 88 | `m8xtR3-ZQs8` | 89% | 100% | 94% | 88% | 70% | 78% | 10 | 10 | 8 | 10 | — | VPC |
| 89 | `oEmuI32GYww` | 100% | 89% | 94% | 57% | 80% | 67% | 10 | 10 | 7 | 5 | UserConsumerEdge | — |
| 90 | `uQFtb0iMC_s` | 89% | 100% | 94% | 82% | 100% | 90% | 9 | 8 | 11 | 9 | — | SageMaker |
| 91 | `vdujJAab1LM` | 100% | 89% | 94% | 100% | 70% | 82% | 8 | 9 | 7 | 10 | Lambda | — |
| 92 | `yPJf85tjv6M` | 100% | 89% | 94% | 70% | 54% | 61% | 11 | 11 | 10 | 13 | UserConsumerWeb | — |
| 93 | `-ahWdCysMYw` | 100% | 88% | 93% | 67% | 44% | 53% | 7 | 8 | 6 | 9 | UserCompanyAnalyst | — |
| 94 | `CTG23wd9H74` | 100% | 88% | 93% | 78% | 64% | 70% | 7 | 8 | 9 | 11 | UserCompanyAnalyst | — |
| 95 | `G5tNCpmD2uQ` | 100% | 88% | 93% | 67% | 33% | 44% | 11 | 9 | 6 | 12 | UserConsumerMobile | — |
| 96 | `HrYfdnPp6qs` | 100% | 88% | 93% | 80% | 44% | 57% | 7 | 10 | 5 | 9 | ThirdParty | — |
| 97 | `OuQvFd44vw4` | 100% | 88% | 93% | 64% | 78% | 70% | 10 | 10 | 11 | 9 | UserCompanyAPI | — |
| 98 | `Wk9mCHyjtBU` | 100% | 88% | 93% | 100% | 38% | 55% | 8 | 10 | 6 | 16 | UserConsumerWeb | — |
| 99 | `bxvZBfbyhiA` | 100% | 88% | 93% | 88% | 58% | 70% | 8 | 9 | 8 | 12 | UserConsumerDeveloper | — |
| 100 | `gu54VVeDD10` | 100% | 88% | 93% | 83% | 56% | 67% | 7 | 8 | 6 | 9 | ECR | — |
| 101 | `iKYvG5aiIn8` | 100% | 88% | 93% | 86% | 86% | 86% | 8 | 9 | 7 | 7 | UserCompanyAnalyst | — |
| 102 | `iWK0iRUi-b4` | 100% | 88% | 93% | 75% | 50% | 60% | 8 | 8 | 8 | 12 | UserConsumerWeb | — |
| 103 | `qN5-v4NlKac` | 88% | 100% | 93% | 89% | 80% | 84% | 10 | 10 | 9 | 10 | — | OpenSearch |
| 104 | `rHLuQTO6eoo` | 100% | 88% | 93% | 83% | 71% | 77% | 9 | 10 | 12 | 14 | UserCompanyAnalyst | — |
| 105 | `u3ZwnulzLnU` | 88% | 100% | 93% | 67% | 62% | 64% | 9 | 8 | 12 | 13 | — | OpenSearch |
| 106 | `yVgxqT1vikk` | 100% | 88% | 93% | 67% | 38% | 48% | 9 | 10 | 9 | 16 | UserCompanyDataStream | — |
| 107 | `qi017F1UwvM` | 93% | 93% | 93% | 65% | 46% | 54% | 17 | 17 | 17 | 24 | Kinesis | Firehose |
| 108 | `d0EE1HuZSEU` | 92% | 92% | 92% | 80% | 57% | 67% | 13 | 13 | 15 | 21 | ThirdParty | OnPremDC |
| 109 | `-kA0ahrhX3I` | 100% | 86% | 92% | 50% | 50% | 50% | 10 | 9 | 8 | 8 | UserCompanyDeveloper | — |
| 110 | `37T7Nd8pL-c` | 100% | 86% | 92% | 57% | 33% | 42% | 6 | 8 | 7 | 12 | UserConsumerAPI | — |
| 111 | `5vR5aN_xdI0` | 100% | 86% | 92% | 71% | 50% | 59% | 9 | 9 | 7 | 10 | UserConsumerAPI | — |
| 112 | `6EUknQqaV1w` | 100% | 86% | 92% | 67% | 55% | 60% | 7 | 9 | 9 | 11 | UserCompanyDataStream | — |
| 113 | `CDCLwX2fo2g` | 100% | 86% | 92% | 88% | 50% | 64% | 8 | 8 | 8 | 14 | UserConsumerMobile | — |
| 114 | `CsD5bmM6mpY` | 86% | 100% | 92% | 50% | 57% | 53% | 8 | 6 | 8 | 7 | — | ThirdParty |
| 115 | `FftalZUxyiM` | 100% | 86% | 92% | 100% | 50% | 67% | 8 | 9 | 7 | 14 | UserConsumerWeb | — |
| 116 | `Kp088QTRmLk` | 100% | 86% | 92% | 100% | 90% | 95% | 8 | 9 | 9 | 10 | UserConsumerWeb | — |
| 117 | `O5Sn5QCEAzE` | 86% | 100% | 92% | 57% | 44% | 50% | 7 | 7 | 7 | 9 | — | EKS |
| 118 | `QM96Fv_NAnw` | 100% | 86% | 92% | 38% | 50% | 43% | 6 | 7 | 8 | 6 | ThirdParty | — |
| 119 | `SSWwnNVYi_Q` | 100% | 86% | 92% | 80% | 40% | 53% | 7 | 8 | 5 | 10 | UserConsumerWeb | — |
| 120 | `a1sEfGVDpEQ` | 100% | 86% | 92% | 100% | 69% | 82% | 9 | 10 | 9 | 13 | ThirdParty | — |
| 121 | `hf9nMAG9XoU` | 100% | 86% | 92% | 86% | 55% | 67% | 7 | 8 | 7 | 11 | UserCompanyDataStream | — |
| 122 | `pwxhclKcMas` | 100% | 86% | 92% | 100% | 54% | 70% | 8 | 10 | 7 | 13 | UserCompanyAPI | — |
| 123 | `xKaPAihW_gE` | 100% | 86% | 92% | 100% | 100% | 100% | 7 | 8 | 8 | 8 | VPC | — |
| 124 | `F4KDOGNpSoI` | 92% | 92% | 92% | 87% | 68% | 76% | 14 | 14 | 15 | 19 | UserConsumerMobile | UserConsumerWebMobile |
| 125 | `0F7KDLz-kIQ` | 91% | 91% | 91% | 88% | 50% | 64% | 13 | 13 | 16 | 28 | UserConsumerWeb | ECS |
| 126 | `5CwIt-Alqhg` | 91% | 91% | 91% | 90% | 75% | 82% | 11 | 11 | 10 | 12 | UserCompanyAgent | UserConsumerMobile |
| 127 | `D9qTotVJYss` | 100% | 83% | 91% | 80% | 40% | 53% | 6 | 6 | 5 | 10 | UserCompanyAgent | — |
| 128 | `OrC9cLYMbas` | 83% | 100% | 91% | 50% | 29% | 36% | 7 | 5 | 4 | 7 | — | ECS |
| 129 | `RxAmb57NCPM` | 100% | 83% | 91% | 82% | 75% | 78% | 12 | 13 | 11 | 12 | UserCompanyAPI | — |
| 130 | `WS2Qgx0qgCM` | 83% | 100% | 91% | 43% | 38% | 40% | 7 | 6 | 7 | 8 | — | ThirdParty |
| 131 | `_EPfIJnBCoM` | 83% | 100% | 91% | 50% | 80% | 62% | 9 | 6 | 8 | 5 | — | RDS |
| 132 | `dWCQw_KvlYQ` | 100% | 83% | 91% | 100% | 53% | 70% | 10 | 12 | 8 | 15 | ThirdParty, UserConsumerTV | — |
| 133 | `ooVtAAoSH2k` | 100% | 83% | 91% | 100% | 56% | 71% | 6 | 7 | 5 | 9 | UserCompanyDeveloper | — |
| 134 | `pCZ0bxgBL5c` | 83% | 100% | 91% | 88% | 47% | 61% | 7 | 8 | 8 | 15 | — | UserConsumerMobile |
| 135 | `qIO_54vJ_JI` | 100% | 83% | 91% | 100% | 86% | 92% | 7 | 8 | 6 | 7 | UserConsumerMobile | — |
| 136 | `sQsAGl7mSQs` | 100% | 83% | 91% | 77% | 42% | 54% | 11 | 12 | 13 | 24 | UserCompanyDeveloper | — |
| 137 | `sezX7CSbXTg` | 100% | 83% | 91% | 67% | 50% | 57% | 6 | 7 | 6 | 8 | UserConsumerMobile | — |
| 138 | `uhrheMJTV4A` | 91% | 91% | 91% | 90% | 60% | 72% | 11 | 11 | 10 | 15 | UserCompanyDataStream | ThirdParty |
| 139 | `9yziTe6lBwk` | 90% | 90% | 90% | 89% | 50% | 64% | 10 | 10 | 9 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 140 | `XmIhHtPJWog` | 90% | 90% | 90% | 90% | 90% | 90% | 10 | 10 | 10 | 10 | UserCompanyAgent | UserCompanyAnalyst |
| 141 | `ec6j-MaOSUc` | 100% | 82% | 90% | 78% | 35% | 48% | 11 | 11 | 9 | 20 | UserCompanyAnalyst, UserCompanyDeveloper | — |
| 142 | `kD57QUn5myc` | 90% | 90% | 90% | 40% | 33% | 36% | 10 | 10 | 10 | 12 | Kinesis | KinesisVideo |
| 143 | `oTtPNgcZ05I` | 90% | 90% | 90% | 62% | 45% | 53% | 10 | 10 | 8 | 11 | UserCompanyAnalyst | UserCompanyDeveloper |
| 144 | `w-qGSyzDL6g` | 100% | 82% | 90% | 80% | 50% | 62% | 11 | 12 | 10 | 16 | UserCompanyAnalyst, UserCompanyDataStream | — |
| 145 | `4WjXH8Wp0E4` | 100% | 80% | 89% | 92% | 50% | 65% | 13 | 14 | 12 | 22 | UserConsumerHospital, UserConsumerWeb | — |
| 146 | `DxHO2TWVN8I` | 100% | 80% | 89% | 64% | 37% | 47% | 8 | 10 | 11 | 19 | UserCompanyAnalyst, UserConsumerWeb | — |
| 147 | `FqCs3BD6qvo` | 100% | 80% | 89% | 38% | 30% | 33% | 7 | 6 | 8 | 10 | VPC | — |
| 148 | `Ly_UhX3LCCs` | 80% | 100% | 89% | 43% | 43% | 43% | 9 | 7 | 7 | 7 | — | ThirdParty |
| 149 | `R-DPMUjZEf4` | 100% | 80% | 89% | 100% | 83% | 91% | 6 | 7 | 5 | 6 | UserConsumerWeb | — |
| 150 | `hlVnmCfydIs` | 100% | 80% | 89% | 100% | 85% | 92% | 8 | 11 | 11 | 13 | ThirdParty, UserConsumerMobile | — |
| 151 | `lHM96P5kP2k` | 80% | 100% | 89% | 69% | 64% | 67% | 11 | 11 | 13 | 14 | — | UserCompanyInternalPlatform |
| 152 | `6CgqEzyWpeA` | 89% | 89% | 89% | 60% | 47% | 53% | 12 | 12 | 15 | 19 | EC2 | AutoScaling |
| 153 | `AS2JeM2FUzE` | 89% | 89% | 89% | 80% | 67% | 73% | 9 | 9 | 10 | 12 | UserCompanyDataStream | ThirdParty |
| 154 | `JVcKidzqpYY` | 89% | 89% | 89% | 80% | 62% | 70% | 9 | 9 | 10 | 13 | UserCompanyDataStream | ThirdParty |
| 155 | `Jz2RPRhF6Fs` | 89% | 89% | 89% | 89% | 62% | 73% | 10 | 10 | 9 | 13 | UserConsumerMobile | UserConsumerWebMobile |
| 156 | `KywvGM6HVXI` | 89% | 89% | 89% | 91% | 45% | 61% | 11 | 11 | 11 | 22 | UserConsumerWeb | ThirdParty |
| 157 | `c6yBZBMwtLk` | 89% | 89% | 89% | 75% | 69% | 72% | 11 | 11 | 12 | 13 | UserCompanyElementalLiveDevice | UserConsumerCamera |
| 158 | `iSkWd31X7zo` | 89% | 89% | 89% | 86% | 67% | 75% | 9 | 9 | 7 | 9 | UserConsumerAPI | UserConsumerWebMobile |
| 159 | `mKZw29_UtoU` | 89% | 89% | 89% | 92% | 65% | 76% | 10 | 10 | 12 | 17 | UserCompanyEdge | ThirdParty |
| 160 | `nt4lQx6tAI8` | 89% | 89% | 89% | 75% | 45% | 56% | 10 | 10 | 12 | 20 | UserConsumerMobile | UserConsumerWebMobile |
| 161 | `uWUAcc68MWI` | 89% | 89% | 89% | 80% | 53% | 64% | 12 | 11 | 10 | 15 | UserConsumerWeb | UserConsumerIOT |
| 162 | `vb-o1DvvHxk` | 89% | 89% | 89% | 57% | 73% | 64% | 11 | 10 | 14 | 11 | UserCompanyDataStream | ThirdParty |
| 163 | `6LcSv9XocTY` | 100% | 78% | 88% | 88% | 39% | 54% | 9 | 11 | 8 | 18 | Firehose, UserConsumerWeb | — |
| 164 | `PoYiSKUy8sE` | 100% | 78% | 88% | 90% | 47% | 62% | 12 | 14 | 10 | 19 | UserConsumerAPI, UserConsumerEdge | — |
| 165 | `UsngU-HjH_Q` | 100% | 78% | 88% | 30% | 30% | 30% | 12 | 9 | 10 | 10 | UserCompanyDataStream, UserConsumerAPI | — |
| 166 | `a59halVklMI` | 100% | 78% | 88% | 100% | 50% | 67% | 10 | 12 | 8 | 16 | MSK, ThirdParty | — |
| 167 | `5EmA67lSJEs` | 88% | 88% | 88% | 55% | 30% | 39% | 10 | 11 | 11 | 20 | UserConsumerAPI | UserCompanyAgent |
| 168 | `FfSNnH2bbNc` | 88% | 88% | 88% | 85% | 58% | 69% | 8 | 8 | 13 | 19 | UserConsumerSatellite | ThirdParty |
| 169 | `IP03SkGbP-U` | 88% | 88% | 88% | 56% | 71% | 63% | 8 | 8 | 9 | 7 | UserConsumerWeb | VPC |
| 170 | `Kp51k6LY-2c` | 88% | 88% | 88% | 75% | 38% | 50% | 8 | 8 | 8 | 16 | UserCompanyDataStream | OnPremDC |
| 171 | `SC6n6J8Bi58` | 88% | 88% | 88% | 54% | 47% | 50% | 10 | 11 | 13 | 15 | UserConsumerDeveloper | NLB |
| 172 | `SpIlpGxuwFM` | 88% | 88% | 88% | 71% | 62% | 67% | 8 | 8 | 7 | 8 | ThirdParty | CloudFormation |
| 173 | `T048vs9p1h4` | 88% | 88% | 88% | 87% | 57% | 68% | 12 | 12 | 15 | 23 | UserConsumerAPI | ApiGateway |
| 174 | `ZCj2wuKBBu4` | 88% | 88% | 88% | 62% | 56% | 59% | 9 | 9 | 8 | 9 | EC2 | AutoScaling |
| 175 | `cmlhEbm1kPk` | 88% | 88% | 88% | 56% | 28% | 37% | 9 | 9 | 9 | 18 | MediaConnect | Connect |
| 176 | `co4_t2gN1T8` | 88% | 88% | 88% | 89% | 50% | 64% | 9 | 9 | 9 | 16 | UserCompanyDeveloper | UserConsumerDeveloper |
| 177 | `gpWR5JBC64A` | 88% | 88% | 88% | 71% | 83% | 77% | 8 | 8 | 7 | 6 | UserConsumerMobile | Amplify |
| 178 | `jg85DzUZ9Ac` | 88% | 88% | 88% | 91% | 91% | 91% | 10 | 10 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 179 | `kHPGZOpbnok` | 88% | 88% | 88% | 56% | 42% | 48% | 8 | 8 | 9 | 12 | UserConsumerWeb | ThirdParty |
| 180 | `nflGdpwbf54` | 88% | 88% | 88% | 70% | 64% | 67% | 8 | 8 | 10 | 11 | UserConsumerWeb | UserCompanyDomainExpert |
| 181 | `U1P8vZTEB-k` | 91% | 83% | 87% | 54% | 50% | 52% | 11 | 12 | 13 | 14 | UserCompanyDeveloper, UserConsumerAPI | DMS |
| 182 | `S85DeDgWQSc` | 90% | 82% | 86% | 70% | 50% | 58% | 10 | 12 | 10 | 14 | StepFunctions, UserCompanyAnalyst | UserCompanyDomainExpert |
| 183 | `j-lPgPGBTwQ` | 82% | 90% | 86% | 60% | 56% | 58% | 12 | 11 | 15 | 16 | ThirdParty | UserConsumerIOT, UserConsumerMobile |
| 184 | `5f3z1Z_9BJA` | 86% | 86% | 86% | 91% | 59% | 71% | 11 | 11 | 11 | 17 | UserCompanyDataStream | ThirdParty |
| 185 | `90rWUjKjnAE` | 86% | 86% | 86% | 78% | 70% | 74% | 9 | 8 | 9 | 10 | UserConsumerDeveloper | UserCompanyDeveloper |
| 186 | `Ccutfm_Srzw` | 86% | 86% | 86% | 85% | 79% | 81% | 11 | 11 | 13 | 14 | KinesisDataStream | KinesisAnalytics |
| 187 | `D77FSUkPJ3o` | 86% | 86% | 86% | 60% | 50% | 55% | 8 | 8 | 10 | 12 | UserConsumerWeb | UserCompanyAgent |
| 188 | `EiljRL0977M` | 86% | 86% | 86% | 80% | 31% | 44% | 7 | 7 | 5 | 13 | ThirdParty | S3 |
| 189 | `Fd2c7NDYfpo` | 86% | 86% | 86% | 75% | 50% | 60% | 8 | 8 | 8 | 12 | ThirdParty | SES |
| 190 | `Felt-hOU6kU` | 75% | 100% | 86% | 50% | 100% | 67% | 9 | 7 | 8 | 4 | — | ThirdParty, VPC |
| 191 | `JYeXbUdFOdw` | 86% | 86% | 86% | 54% | 50% | 52% | 12 | 8 | 13 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 192 | `K27WjYwyqw8` | 86% | 86% | 86% | 78% | 64% | 70% | 8 | 8 | 9 | 11 | UserConsumerMobile | ThirdParty |
| 193 | `Pc7_uOdlGKo` | 100% | 75% | 86% | 100% | 78% | 88% | 7 | 9 | 7 | 9 | UserCompanyAgent, UserConsumerMobile | — |
| 194 | `Yju3yReAQtc` | 86% | 86% | 86% | 60% | 43% | 50% | 12 | 7 | 5 | 7 | UserCompanyInternalPlatform | ThirdParty |
| 195 | `aOY6YCpcjz8` | 100% | 75% | 86% | 91% | 71% | 80% | 10 | 11 | 11 | 14 | UserCompanyAPI | — |
| 196 | `cZuoiXQ0xUk` | 86% | 86% | 86% | 62% | 38% | 48% | 8 | 8 | 8 | 13 | ThirdParty | UserCompanyWebsite |
| 197 | `eEfWd4EgH_s` | 86% | 86% | 86% | 89% | 80% | 84% | 10 | 10 | 9 | 10 | UserCompanyDataStream | ThirdParty |
| 198 | `fSV0u48sEVg` | 86% | 86% | 86% | 25% | 18% | 21% | 7 | 7 | 8 | 11 | Fargate | ECS |
| 199 | `fTxvwVj02P0` | 86% | 86% | 86% | 86% | 60% | 71% | 8 | 8 | 7 | 10 | UserConsumerWeb | UserConsumerWebMobile |
| 200 | `ftIdBG-UgFY` | 100% | 75% | 86% | 80% | 44% | 57% | 6 | 8 | 5 | 9 | EC2, VPC | — |
| 201 | `pZ7Lr94noLo` | 100% | 75% | 86% | 78% | 47% | 58% | 10 | 13 | 9 | 15 | ApiGateway, UserConsumerWeb | — |
| 202 | `uBiaWJbTRsE` | 75% | 100% | 86% | 67% | 89% | 76% | 10 | 8 | 12 | 9 | — | EC2, ThirdParty |
| 203 | `unF9tdYjqvU` | 86% | 86% | 86% | 44% | 50% | 47% | 11 | 7 | 9 | 8 | UserConsumerWeb | UserConsumerWebMobile |
| 204 | `wjtSHyENv0I` | 86% | 86% | 86% | 67% | 43% | 52% | 8 | 8 | 9 | 14 | UserConsumerWeb | UserCompanyAgent |
| 205 | `ww5fiygF6eg` | 86% | 86% | 86% | 56% | 25% | 34% | 8 | 10 | 9 | 20 | UserCompanyDrone | OnPremDC |
| 206 | `zhCNn7v7mvs` | 86% | 86% | 86% | 70% | 64% | 67% | 9 | 8 | 10 | 11 | UserConsumerAPI | ThirdParty |
| 207 | `7wBOFcP1HwA` | 80% | 89% | 84% | 67% | 60% | 63% | 11 | 10 | 9 | 10 | UserConsumerWeb | EC2, UserConsumerWebMobile |
| 208 | `DnTQ3matqts` | 80% | 89% | 84% | 58% | 50% | 54% | 14 | 14 | 12 | 14 | UserConsumerEdge | SNS, UserConsumerIOT |
| 209 | `ErXwuwF2mRU` | 80% | 89% | 84% | 44% | 40% | 42% | 10 | 9 | 9 | 10 | UserConsumerWeb | Aurora, ThirdParty |
| 210 | `KQ6Fg206O9U` | 89% | 80% | 84% | 55% | 43% | 48% | 10 | 10 | 11 | 14 | LambdaAtEdge, UserConsumerWeb | UserConsumerWebMobile |
| 211 | `StSuG6-iKW4` | 80% | 89% | 84% | 50% | 57% | 53% | 11 | 10 | 8 | 7 | UserConsumerEdge | UserCompanyEdge, UserConsumerMobile |
| 212 | `hFx0EF9KEZU` | 80% | 89% | 84% | 67% | 43% | 53% | 15 | 15 | 15 | 23 | Firehose | Kinesis, UserCompanyAgent |
| 213 | `kszaIJEnKPk` | 89% | 80% | 84% | 82% | 69% | 75% | 10 | 11 | 11 | 13 | LambdaAtEdge, UserConsumerEdge | ThirdParty |
| 214 | `nvhG60gFbso` | 89% | 80% | 84% | 42% | 31% | 36% | 11 | 13 | 12 | 16 | ThirdParty, VPC | OnPremDC |
| 215 | `r2xfxJ-sXMY` | 80% | 89% | 84% | 70% | 70% | 70% | 11 | 9 | 10 | 10 | UserConsumerWebMobile | UserConsumerMobile, UserConsumerWeb |
| 216 | `1aYoIZvabbk` | 83% | 83% | 83% | 67% | 80% | 73% | 6 | 6 | 6 | 5 | UserCompanyDeveloper | EC2 |
| 217 | `2e3vOxsHekE` | 83% | 83% | 83% | 80% | 67% | 73% | 6 | 6 | 5 | 6 | UserConsumerEdge | ThirdParty |
| 218 | `66fPHLmvikk` | 83% | 83% | 83% | 50% | 62% | 56% | 11 | 7 | 10 | 8 | UserCompanyAnalyst | UserCompanyDeveloper |
| 219 | `7V8wTCkjOqo` | 83% | 83% | 83% | 25% | 29% | 27% | 6 | 7 | 8 | 7 | ThirdParty | UserCompanyDeveloper |
| 220 | `H2fOkeXxpyw` | 83% | 83% | 83% | 86% | 60% | 71% | 8 | 8 | 7 | 10 | UserCompanyDeveloper | UserConsumerDeveloper |
| 221 | `QJZHs1CSxu0` | 83% | 83% | 83% | 50% | 50% | 50% | 6 | 6 | 6 | 6 | UserConsumerMobile | UserConsumerWebMobile |
| 222 | `Vrx9csoawWc` | 83% | 83% | 83% | 60% | 29% | 39% | 8 | 7 | 10 | 21 | UserConsumerWeb | UserCompanyAnalyst |
| 223 | `XG6mHvi4eNU` | 83% | 83% | 83% | 83% | 50% | 62% | 7 | 6 | 6 | 10 | UserCompanyDeveloper | UserConsumerDeveloper |
| 224 | `_vjB_vF4Uec` | 83% | 83% | 83% | 33% | 33% | 33% | 10 | 6 | 9 | 9 | UserConsumerEdge | ThirdParty |
| 225 | `aQFztbu0BG0` | 83% | 83% | 83% | 75% | 75% | 75% | 8 | 8 | 8 | 8 | ThirdParty | OnPremDC |
| 226 | `ccPhkyPm_3w` | 83% | 83% | 83% | 50% | 67% | 57% | 9 | 6 | 8 | 6 | UserCompanyDataStream | ThirdParty |
| 227 | `ekXdohpAy5U` | 83% | 83% | 83% | 83% | 56% | 67% | 6 | 6 | 6 | 9 | UserCompanyDataStream | ThirdParty |
| 228 | `hbz63Ve-eIY` | 83% | 83% | 83% | 43% | 23% | 30% | 6 | 6 | 7 | 13 | UserCompanyDeveloper | ThirdParty |
| 229 | `pk5yddJpC_8` | 83% | 83% | 83% | 88% | 70% | 78% | 9 | 9 | 8 | 10 | UserCompanyDeveloper | UserCompanyInternalPlatform |
| 230 | `rPGLNw1cOGM` | 83% | 83% | 83% | 92% | 55% | 69% | 8 | 8 | 12 | 20 | UserConsumerWeb | UserCompanyDomainExpert |
| 231 | `tBavPTWewvI` | 83% | 83% | 83% | 50% | 33% | 40% | 6 | 6 | 6 | 9 | MSK | ThirdParty |
| 232 | `tVjrkpjWG5o` | 83% | 83% | 83% | 86% | 75% | 80% | 8 | 7 | 7 | 8 | UserConsumerAPI | UserCompanyAnalyst |
| 233 | `D_4dsXVqzMs` | 71% | 100% | 83% | 71% | 50% | 59% | 8 | 7 | 7 | 10 | — | Lambda, OnPremDC |
| 234 | `WtCfHP6rUAY` | 100% | 71% | 83% | 100% | 62% | 76% | 9 | 11 | 8 | 13 | UserCompanyAPI, UserCompanyDataStream | — |
| 235 | `twsGnp2X-aQ` | 100% | 71% | 83% | 100% | 62% | 77% | 6 | 7 | 5 | 8 | UserCompanyAnalyst, UserCompanyDataStream | — |
| 236 | `0gNMEyei-co` | 88% | 78% | 82% | 82% | 69% | 75% | 9 | 9 | 11 | 13 | Kinesis, UserCompanyDataStream | KinesisDataStream |
| 237 | `CE03UMddoYU` | 78% | 88% | 82% | 80% | 67% | 73% | 11 | 10 | 10 | 12 | UserConsumerEdge | UserConsumerIOT, UserConsumerMobile |
| 238 | `GJ1So_pbZWk` | 78% | 88% | 82% | 80% | 35% | 48% | 10 | 9 | 10 | 23 | UserConsumerWeb | ApiGateway, QuickSight |
| 239 | `H_S7CxtHgSM` | 78% | 88% | 82% | 54% | 58% | 56% | 12 | 11 | 13 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 240 | `RU__HBEMDvQ` | 88% | 78% | 82% | 43% | 30% | 35% | 8 | 9 | 7 | 10 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 241 | `_pXybA6832o` | 78% | 88% | 82% | 82% | 82% | 82% | 10 | 9 | 11 | 11 | UserConsumerAlexaGoogleHome | AlexaForBusiness, ThirdParty |
| 242 | `mq3XuoN0rUM` | 88% | 78% | 82% | 50% | 38% | 43% | 8 | 9 | 10 | 13 | ThirdParty, UserCompanyDeveloper | UserCompanyAgent |
| 243 | `FHdtOtznWuA` | 100% | 70% | 82% | 100% | 39% | 56% | 7 | 10 | 7 | 18 | CloudFormation, ServerlessApplicationRepository, UserConsumerEdge | — |
| 244 | `YiOTd6IfGoU` | 82% | 82% | 82% | 73% | 62% | 67% | 12 | 12 | 11 | 13 | CloudWatch, UserCompanyDataStream | EventBridge, UserCompanyInternalPlatform |
| 245 | `ZPsBzAwJzoI` | 82% | 82% | 82% | 67% | 47% | 55% | 12 | 12 | 12 | 17 | EC2, UserConsumerTV | UserConsumerCamera, UserConsumerWebMobile |
| 246 | `gcgtLDB0cKA` | 82% | 82% | 82% | 83% | 56% | 67% | 13 | 13 | 12 | 18 | UserCompanyEdge, UserConsumerWeb | UserConsumerIOT, UserConsumerWebMobile |
| 247 | `BZ32w0SSAoY` | 80% | 80% | 80% | 82% | 47% | 60% | 7 | 7 | 11 | 19 | ThirdParty | RDS |
| 248 | `JRDGId6N49E` | 80% | 80% | 80% | 25% | 33% | 29% | 6 | 6 | 4 | 3 | ThirdParty | FSX |
| 249 | `JiWHomdh1oI` | 80% | 80% | 80% | 80% | 73% | 76% | 7 | 7 | 10 | 11 | UserCompanyDataStream | ThirdParty |
| 250 | `XqsgQxyZ2Tw` | 80% | 80% | 80% | 64% | 44% | 52% | 10 | 11 | 11 | 16 | UserConsumerAPI | CouchBase |
| 251 | `YV8e36ZywLk` | 80% | 80% | 80% | 0% | 0% | 0% | 5 | 5 | 4 | 4 | ThirdParty | SAP |
| 252 | `bqZWYmRAka0` | 80% | 80% | 80% | 31% | 80% | 44% | 10 | 5 | 13 | 5 | UserConsumerAPI | UserCompanyInternalPlatform |
| 253 | `illMCyp4O9A` | 80% | 80% | 80% | 64% | 50% | 56% | 10 | 10 | 11 | 14 | ThirdParty, UserCompanyAPI | IoTCore, Lambda |
| 254 | `wbh51O3QrE4` | 80% | 80% | 80% | 55% | 60% | 57% | 10 | 10 | 11 | 10 | ALB, UserConsumerMobile | ELB, UserCompanyAnalyst |
| 255 | `-3lnf5lzsH0` | 100% | 67% | 80% | 44% | 25% | 32% | 9 | 13 | 9 | 16 | CloudTrail, GuardDuty, SNS (+1) | — |
| 256 | `DAJZAygxDZA` | 100% | 67% | 80% | 50% | 33% | 40% | 9 | 8 | 10 | 15 | ModelRegistry, UserCompanyAnalyst | — |
| 257 | `PBa68gCG0Uk` | 100% | 67% | 80% | 83% | 71% | 77% | 5 | 7 | 6 | 7 | OpenSearch, ThirdParty | — |
| 258 | `0JxJpNjI9Y0` | 75% | 86% | 80% | 60% | 35% | 44% | 10 | 9 | 10 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserConsumerWeb |
| 259 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 8 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerWebMobile |
| 260 | `9qTEHITVeLE` | 75% | 86% | 80% | 45% | 36% | 40% | 10 | 9 | 11 | 14 | UserConsumerWeb | OpenSearch, UserCompanyAnalyst |
| 261 | `Gds8hl8dKuo` | 75% | 86% | 80% | 56% | 42% | 48% | 10 | 8 | 9 | 12 | UserCompanyAgent | ThirdParty, UserCompanyDeveloper |
| 262 | `NfUwtK8ALtw` | 75% | 86% | 80% | 27% | 19% | 22% | 9 | 9 | 11 | 16 | UserConsumerWeb | AutoScaling, UserConsumerWebMobile |
| 263 | `O11BgSm7V14` | 86% | 75% | 80% | 89% | 62% | 73% | 9 | 10 | 9 | 13 | EventBridge, UserConsumerWeb | ThirdParty |
| 264 | `PgeQufaQy7I` | 86% | 75% | 80% | 83% | 62% | 71% | 7 | 8 | 6 | 8 | CloudFormation, UserConsumerWeb | UserConsumerWebMobile |
| 265 | `TTlyNWh0gjM` | 75% | 86% | 80% | 56% | 33% | 42% | 11 | 11 | 9 | 15 | UserConsumerAPI | CloudFront, ElastiCache |
| 266 | `W5qVQr-n5M8` | 86% | 75% | 80% | 89% | 40% | 55% | 9 | 10 | 9 | 20 | ThirdParty, UserConsumerWeb | RDS |
| 267 | `XUCGMzLx8wY` | 86% | 75% | 80% | 50% | 44% | 47% | 7 | 8 | 8 | 9 | MSK, UserConsumerMobile | ThirdParty |
| 268 | `XpFNznmRoQ0` | 73% | 89% | 80% | 79% | 69% | 73% | 14 | 12 | 14 | 16 | UserCompanyDataStream | RDS, ThirdParty, UserCompanyAnalyst |
| 269 | `mtZvA7ARepM` | 86% | 75% | 80% | 75% | 38% | 50% | 8 | 9 | 8 | 16 | Kinesis, UserConsumerAPI | KinesisDataStream |
| 270 | `vr00Jg_G6qs` | 86% | 75% | 80% | 40% | 29% | 33% | 12 | 11 | 10 | 14 | UserCompanyInternalPlatform, UserConsumerHospital | ThirdParty |
| 271 | `QnwfcDZkwh8` | 90% | 69% | 78% | 83% | 56% | 67% | 10 | 13 | 12 | 18 | UserCompanyDeveloper, UserConsumerMobile, UserConsumerTV (+1) | UserConsumerWebMobile |
| 272 | `WYK-smWKywA` | 75% | 82% | 78% | 73% | 35% | 47% | 12 | 11 | 11 | 23 | ThirdParty, UserConsumerMobile | DirectConnect, OnPremDC, UserConsumerWeb |
| 273 | `l0hlxVNmJPI` | 82% | 75% | 78% | 30% | 75% | 43% | 12 | 14 | 10 | 4 | AutoScaling, RDS, UserConsumerEdge | CloudWatch, ThirdParty |
| 274 | `D6rG9eZ5Qus` | 78% | 78% | 78% | 62% | 56% | 59% | 9 | 9 | 8 | 9 | ThirdParty, UserCompanyDataStream | SystemsManager, UserCompanyElementalLiveDevice |
| 275 | `E8BGpIxzYc4` | 78% | 78% | 78% | 60% | 55% | 57% | 10 | 10 | 10 | 11 | QuickSight, UserCompanyDataStream | MongoDBAtlas, ThirdParty |
| 276 | `KM5ONS2fnG0` | 78% | 78% | 78% | 78% | 35% | 48% | 10 | 10 | 9 | 20 | Kinesis, UserCompanyDataStream | Firehose, KinesisDataStream |
| 277 | `a6kqyqTNJM4` | 78% | 78% | 78% | 27% | 20% | 23% | 11 | 11 | 11 | 15 | ThirdParty, UserConsumerWeb | ELB, UserConsumerWebMobile |
| 278 | `c-1GXhOOOww` | 78% | 78% | 78% | 33% | 25% | 29% | 9 | 9 | 12 | 16 | ThirdParty, UserConsumerMobile | CloudFront, UserConsumerWebMobile |
| 279 | `INog0_9tCtY` | 88% | 70% | 78% | 55% | 32% | 40% | 11 | 14 | 11 | 19 | OpenSearch, UserCompanyAnalyst, VPC | MSK |
| 280 | `Kebb0LOVC28` | 100% | 62% | 77% | 83% | 24% | 37% | 6 | 9 | 6 | 21 | CodeBuild, ECR, UserCompanyDeveloper | — |
| 281 | `4-teOQ_dJvY` | 83% | 71% | 77% | 78% | 54% | 64% | 9 | 9 | 9 | 13 | UserCompanyAPI, UserCompanyEdge | ThirdParty |
| 282 | `6iK4WNj6QqI` | 71% | 83% | 77% | 43% | 30% | 35% | 7 | 6 | 7 | 10 | UserConsumerWeb | CloudFront, UserConsumerWebMobile |
| 283 | `9-6hQdFeolc` | 83% | 71% | 77% | 33% | 25% | 29% | 8 | 8 | 6 | 8 | UserCompanyCRM, UserCompanyDeveloper | UserConsumerHospital |
| 284 | `9-a9Y5THTYo` | 71% | 83% | 77% | 62% | 83% | 71% | 8 | 7 | 8 | 6 | UserConsumerWeb | Organizations, UserCompanyDeveloper |
| 285 | `ItpY_KKR94k` | 83% | 71% | 77% | 71% | 71% | 71% | 8 | 8 | 7 | 7 | S3, UserCompanyCRM | ThirdParty |
| 286 | `Jkx6kVbDpL4` | 83% | 71% | 77% | 86% | 71% | 77% | 12 | 13 | 14 | 17 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 287 | `MbkLJ62jtMc` | 71% | 83% | 77% | 50% | 75% | 60% | 8 | 6 | 6 | 4 | UserCompanyAPI | SES, ThirdParty |
| 288 | `S-JSSZZaa94` | 83% | 71% | 77% | 38% | 27% | 32% | 7 | 8 | 8 | 11 | ThirdParty, UserConsumerMobile | OpenSearch |
| 289 | `XGVWdSnml6A` | 83% | 71% | 77% | 29% | 25% | 27% | 8 | 7 | 7 | 8 | UserConsumerAPI, UserConsumerEdge | EC2 |
| 290 | `aY-wF9g0qkM` | 83% | 71% | 77% | 67% | 43% | 52% | 9 | 10 | 9 | 14 | ThirdParty, UserConsumerEdge | UserConsumerCamera |
| 291 | `bQqJpjv-FXs` | 71% | 83% | 77% | 50% | 80% | 62% | 7 | 6 | 8 | 5 | UserCompanyDataStream | ThirdParty, UserConsumerIOT |
| 292 | `iwZLadQ3XpY` | 83% | 71% | 77% | 60% | 43% | 50% | 6 | 7 | 5 | 7 | ThirdParty, UserConsumerMobile | UserConsumerWebMobile |
| 293 | `lTSZT10JMQA` | 83% | 71% | 77% | 78% | 33% | 47% | 10 | 10 | 9 | 21 | UserCompanyDataStream, UserConsumerTV | ThirdParty |
| 294 | `DrkaU99l9S8` | 73% | 80% | 76% | 67% | 62% | 64% | 11 | 12 | 12 | 13 | UserConsumerEdge, UserConsumerWeb | Greengrass, KinesisAnalytics, UserCompanyAnalyst |
| 295 | `SxFag4CMWU8` | 67% | 89% | 76% | 70% | 50% | 58% | 14 | 11 | 10 | 14 | UserConsumerWeb | ELB, Glue, UserCompanyWebsite (+1) |
| 296 | `Bi-1xjXvKgs` | 75% | 75% | 75% | 43% | 50% | 46% | 8 | 5 | 7 | 6 | UserConsumerWeb | AutoScaling |
| 297 | `M_hqigB9C4I` | 75% | 75% | 75% | 50% | 25% | 33% | 9 | 9 | 8 | 16 | UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent |
| 298 | `QOtCpD23118` | 75% | 75% | 75% | 67% | 80% | 73% | 11 | 11 | 12 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 299 | `acm-HWJhEOA` | 75% | 75% | 75% | 70% | 50% | 58% | 10 | 8 | 10 | 14 | UserCompanyAPI, UserCompanyDataStream | ThirdParty, UserConsumerWebMobile |
| 300 | `l3f29v3IJGA` | 67% | 86% | 75% | 20% | 13% | 16% | 9 | 9 | 10 | 15 | EC2 | EKS, SQS, ThirdParty |
| 301 | `lcLw-Le_tXQ` | 75% | 75% | 75% | 57% | 57% | 57% | 7 | 6 | 7 | 7 | EKS | CloudFront |
| 302 | `uNAmsoLed1E` | 86% | 67% | 75% | 57% | 27% | 36% | 10 | 10 | 7 | 15 | EC2, RDS, UserCompanyDataStream | ThirdParty |
| 303 | `LD5ksgnu8r8` | 78% | 70% | 74% | 67% | 62% | 64% | 11 | 11 | 12 | 13 | UserCompanyDataStream, UserConsumerAPI, UserConsumerWeb | ThirdParty, UserCompanyAgent |
| 304 | `53sUjFv9ByI` | 80% | 67% | 73% | 80% | 67% | 73% | 5 | 6 | 5 | 6 | ThirdParty, UserCompanyDataStream | S3 |
| 305 | `OWLGK-eVrTw` | 80% | 67% | 73% | 17% | 6% | 9% | 7 | 6 | 6 | 16 | ThirdParty, UserConsumerAPI | EC2 |
| 306 | `gD8pzUnXgsU` | 67% | 80% | 73% | 25% | 25% | 25% | 10 | 6 | 4 | 4 | OnPremDC | EC2, SAP |
| 307 | `-S-R7MWRpaI` | 71% | 71% | 71% | 33% | 27% | 30% | 10 | 8 | 9 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, MongoDBAtlas |
| 308 | `2XVgpMwY5iE` | 71% | 71% | 71% | 50% | 42% | 45% | 8 | 7 | 10 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 309 | `aOZ4H98XROc` | 83% | 62% | 71% | 14% | 11% | 12% | 8 | 8 | 7 | 9 | ApiGateway, ThirdParty, UserConsumerEdge | UserConsumerDeveloper |
| 310 | `8ZRWzn0G39g` | 75% | 67% | 71% | 58% | 18% | 28% | 10 | 12 | 12 | 38 | EC2, EKS, UserConsumerAPI | UserCompanyWebsite, UserConsumerWeb |
| 311 | `G07keU4g-LU` | 75% | 67% | 71% | 50% | 29% | 36% | 10 | 10 | 12 | 21 | ThirdParty, UserCompanyAnalyst, UserConsumerMobile | RDS, UserConsumerWebMobile |
| 312 | `i4ueYgjVDCw` | 62% | 80% | 70% | 50% | 50% | 50% | 13 | 10 | 8 | 8 | ALB, UserConsumerMobile | AutoScaling, DirectConnect, DocumentDB (+2) |
| 313 | `c863uNkF0w4` | 83% | 56% | 67% | 60% | 38% | 46% | 6 | 10 | 5 | 8 | CloudFormation, SystemsManager, UserConsumerAPI (+1) | AutoScaling |
| 314 | `-wLEkq21cvA` | 57% | 80% | 67% | 42% | 50% | 45% | 11 | 9 | 12 | 10 | UserCompanyAgent | AMI, OnPremDC, UserCompanyDeveloper |
| 315 | `3WgTBTDlQN8` | 67% | 67% | 67% | 50% | 36% | 42% | 9 | 9 | 10 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | MongoDBAtlas, ThirdParty, UserConsumerWebMobile |
| 316 | `GxjMSvwcgvw` | 67% | 67% | 67% | 71% | 38% | 50% | 8 | 8 | 7 | 13 | UserCompanyAPI, UserConsumerAPI | ThirdParty, UserConsumerMobile |
| 317 | `KzJKdUZ3Ba4` | 67% | 67% | 67% | 25% | 17% | 20% | 3 | 4 | 4 | 6 | UserConsumerMobile | SAP |
| 318 | `N2mktbl8EQk` | 67% | 67% | 67% | 40% | 22% | 29% | 6 | 6 | 5 | 9 | Kinesis, UserConsumerWeb | KinesisVideo, ThirdParty |
| 319 | `WxMBuBBIwpI` | 67% | 67% | 67% | 40% | 29% | 33% | 6 | 6 | 5 | 7 | EC2, Lambda | AutoScaling, UserConsumerWeb |
| 320 | `cmYI6axlicc` | 80% | 57% | 67% | 30% | 21% | 25% | 9 | 10 | 10 | 14 | MSK, UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 321 | `q_5U7z_vNug` | 71% | 62% | 67% | 44% | 27% | 33% | 7 | 8 | 9 | 15 | ThirdParty, UserCompanyAnalyst, UserConsumerEdge | RDS, UserCompanyEdge |
| 322 | `qgW8LQ8iBuA` | 62% | 71% | 67% | 40% | 50% | 44% | 11 | 10 | 5 | 4 | ThirdParty, UserCompanyAgent | AutoScaling, OpenSearch, UserConsumerWeb |
| 323 | `sKksbPPDznM` | 67% | 67% | 67% | 50% | 38% | 43% | 6 | 6 | 6 | 8 | ShieldAdvanced, UserConsumerMobile | Shield, UserConsumerWebMobile |
| 324 | `wtl7CrSQnHA` | 64% | 70% | 67% | 50% | 50% | 50% | 13 | 12 | 14 | 14 | Kinesis, UserConsumerEdge, UserConsumerWeb | KinesisAnalytics, KinesisDataStream, ThirdParty (+1) |
| 325 | `LYP98nPBj2A` | 60% | 75% | 67% | 60% | 38% | 46% | 9 | 5 | 5 | 8 | UserConsumerMobile | VPC, VPN |
| 326 | `Dxq_U1TNx1s` | 60% | 67% | 63% | 55% | 35% | 43% | 11 | 11 | 11 | 17 | Aurora, UserConsumerMobile, UserConsumerSatellite | RDS, ThirdParty, UserCompanyAgent (+1) |
| 327 | `KgRib8AM0fs` | 56% | 71% | 63% | 22% | 25% | 24% | 9 | 7 | 9 | 8 | UserConsumerEdge, UserConsumerWebMobile | AutoScaling, UserConsumerCamera, UserConsumerMobile (+1) |
| 328 | `FmhL2334GIY` | 75% | 50% | 60% | 33% | 27% | 30% | 9 | 10 | 9 | 11 | ECS, UserCompanyDeveloper, UserCompanyWebsite | ThirdParty |
| 329 | `hMK2NJ-q9nc` | 75% | 50% | 60% | 20% | 40% | 27% | 8 | 6 | 10 | 5 | CloudFormation, UserCompanyDataStream, UserCompanyEdge | ThirdParty |
| 330 | `BPvr0qWpJlA` | 62% | 56% | 59% | 43% | 33% | 38% | 10 | 10 | 7 | 9 | UserCompanyAgent, UserCompanyCRM, UserCompanyDataStream (+1) | EC2, SES, ThirdParty |
| 331 | `mmM_JnYygZM` | 56% | 62% | 59% | 22% | 14% | 17% | 12 | 10 | 9 | 14 | UserCompanyDataStream, UserConsumerPOS, UserConsumerWeb | CouchBase, MongoDBAtlas, Shield (+1) |
| 332 | `mpgM2qeAfaQ` | 56% | 62% | 59% | 20% | 20% | 20% | 11 | 9 | 10 | 10 | Kinesis, UserCompanyAnalyst, UserConsumerWebMobile | KinesisDataStream, UserConsumerCamera, UserConsumerMobile (+1) |
| 333 | `WZ4YL4Z177Q` | 55% | 55% | 55% | 9% | 7% | 8% | 12 | 12 | 11 | 14 | EC2, Kinesis, RDS (+2) | KinesisDataStream, MSK, MongoDBAtlas (+2) |
| 334 | `cRxvZBIa-gI` | 50% | 60% | 55% | 0% | 0% | 0% | 7 | 5 | 4 | 4 | ThirdParty, UserConsumerMobile | DocumentDB, EC2, UserConsumerWebMobile |
| 335 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 25% | 22% | 24% | 8 | 7 | 8 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 336 | `wzGYJ6BB0iY` | 44% | 50% | 47% | 10% | 8% | 9% | 11 | 10 | 10 | 12 | UserCompanyAPI, UserCompanyDataStream, UserConsumerAPI (+1) | DirectConnect, EC2, OnPremDC (+2) |


### Detailed Results Table: Excluded Validation (Invalid/Placeholder Ground Truths)

> [!NOTE]

> These graphs are excluded from the main average F1 calculations above.

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `62E9ggjGS8I` | 100% | 100% | 100% | 100% | 44% | 62% | 7 | 7 | 4 | 9 | — | — |
| 2 | `8TExnSvZqt0` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 11 | 4 | 0 | — | — |
| 3 | `E68ufJOduio` | 100% | 100% | 100% | 0% | 0% | 0% | 9 | 9 | 9 | 0 | — | — |
| 4 | `GoziWpmFCS0` | 100% | 100% | 100% | 25% | 100% | 40% | 7 | 4 | 8 | 2 | — | — |
| 5 | `QnmmTIYZxNI` | 100% | 100% | 100% | 80% | 67% | 73% | 8 | 8 | 5 | 6 | — | — |
| 6 | `ZsabzCVjkIk` | 100% | 100% | 100% | 100% | 88% | 93% | 10 | 10 | 7 | 8 | — | — |
| 7 | `c8615P0yfi8` | 100% | 100% | 100% | 0% | 0% | 0% | 10 | 10 | 11 | 0 | — | — |
| 8 | `jzKCg9Z5_8Q` | 100% | 100% | 100% | 0% | 0% | 0% | 7 | 6 | 6 | 0 | — | — |
| 9 | `mT4KDGRgo4k` | 100% | 100% | 100% | 83% | 56% | 67% | 8 | 5 | 6 | 9 | — | — |
| 10 | `r3g1Nym-ebY` | 100% | 100% | 100% | 0% | 0% | 0% | 7 | 7 | 5 | 0 | — | — |
| 11 | `tTQ36qQF_vA` | 100% | 100% | 100% | 0% | 0% | 0% | 9 | 5 | 5 | 0 | — | — |
| 12 | `uMX94Mn9u-4` | 100% | 100% | 100% | 80% | 80% | 80% | 10 | 10 | 10 | 10 | — | — |
| 13 | `zqiNLMmEeSo` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 10 | 6 | 0 | — | — |
| 14 | `ihB2dRYLOOI` | 100% | 91% | 95% | 44% | 57% | 50% | 11 | 12 | 9 | 7 | UserConsumerAPI | — |
| 15 | `qv9q0sFt6aY` | 89% | 100% | 94% | 42% | 29% | 34% | 11 | 11 | 12 | 17 | — | OnPremDC |
| 16 | `YT21s0_ZJVQ` | 88% | 100% | 93% | 20% | 50% | 29% | 13 | 7 | 5 | 2 | — | EC2 |
| 17 | `1ZLiRT0C2Yo` | 86% | 100% | 92% | 0% | 0% | 0% | 7 | 6 | 5 | 0 | — | OnPremDC |
| 18 | `H51Ups01ZpU` | 86% | 100% | 92% | 0% | 0% | 0% | 7 | 6 | 6 | 0 | — | ThirdParty |
| 19 | `aAYvbRhZFPo` | 86% | 100% | 92% | 40% | 33% | 36% | 11 | 7 | 5 | 6 | — | ThirdParty |
| 20 | `1kWxymroGeE` | 83% | 100% | 91% | 50% | 100% | 67% | 6 | 5 | 8 | 4 | — | ThirdParty |
| 21 | `9LhiUsg3knw` | 100% | 82% | 90% | 45% | 62% | 53% | 10 | 13 | 11 | 8 | UserCompanyDomainExpert, UserConsumerArtist | — |
| 22 | `u5AT15mgbHk` | 80% | 100% | 89% | 0% | 0% | 0% | 6 | 6 | 2 | 0 | — | RDS |
| 23 | `b93-zn-DtBw` | 89% | 89% | 89% | 18% | 50% | 27% | 11 | 9 | 11 | 4 | SageMaker | ThirdParty |
| 24 | `ameanoaMldM` | 78% | 100% | 88% | 10% | 50% | 17% | 11 | 7 | 10 | 2 | — | ACM, ServiceCatalog |
| 25 | `YjASp_VccmI` | 88% | 88% | 88% | 56% | 83% | 67% | 10 | 10 | 9 | 6 | UserConsumerWeb | UserConsumerWebMobile |
| 26 | `vp2Ipv2_uCg` | 80% | 89% | 84% | 0% | 0% | 0% | 10 | 10 | 6 | 0 | UserConsumerAlexaGoogleHome | AlexaForBusiness, ThirdParty |
| 27 | `Ujs9o3CXUTU` | 78% | 88% | 82% | 20% | 50% | 29% | 9 | 8 | 5 | 2 | DynamoDB | ALB, DocumentDB |
| 28 | `W96L6ICcF3s` | 80% | 80% | 80% | 0% | 0% | 0% | 7 | 7 | 3 | 0 | ECS | Fargate |
| 29 | `6sY0AunanlM` | 67% | 100% | 80% | 0% | 0% | 0% | 8 | 4 | 8 | 0 | — | ThirdParty, UserCompanyDeveloper |
| 30 | `OmVQ6pNDbaY` | 67% | 100% | 80% | 0% | 0% | 0% | 6 | 2 | 4 | 0 | — | ThirdParty |
| 31 | `QuyZHin9B70` | 67% | 100% | 80% | 0% | 0% | 0% | 9 | 4 | 7 | 0 | — | OnPremDC, Outpost |
| 32 | `U1kY6nSS2YQ` | 75% | 86% | 80% | 75% | 17% | 27% | 10 | 11 | 4 | 18 | UserCompanyDeveloper | CouchBase, OpenSearch |
| 33 | `hEB1J9-iOqs` | 75% | 86% | 80% | 0% | 0% | 0% | 10 | 9 | 9 | 0 | UserCompanyAPI | SES, ServiceNow |
| 34 | `ruOhUEooJH0` | 89% | 73% | 80% | 38% | 50% | 43% | 10 | 11 | 8 | 6 | Aurora, UserCompanyDataStream, UserConsumerDeveloper | RDS |
| 35 | `JSBB-BCvavQ` | 62% | 100% | 77% | 0% | 0% | 0% | 10 | 5 | 11 | 0 | — | DMS, OnPremDC, Route53 |
| 36 | `1tGmQd0yOzE` | 75% | 75% | 75% | 60% | 25% | 35% | 8 | 8 | 5 | 12 | ThirdParty | SAP |
| 37 | `LPZlrX2cNjo` | 75% | 75% | 75% | 25% | 25% | 25% | 4 | 4 | 4 | 4 | UserConsumerWeb | UserConsumerWebMobile |
| 38 | `e3N5ZuHh7G0` | 75% | 75% | 75% | 50% | 33% | 40% | 5 | 6 | 4 | 6 | ECS | EC2 |
| 39 | `lA0lAgN0hTI` | 75% | 75% | 75% | 0% | 0% | 0% | 8 | 8 | 10 | 0 | UserConsumerWeb | UserConsumerWebMobile |
| 40 | `fOgb0Es-lVs` | 67% | 80% | 73% | 71% | 83% | 77% | 8 | 7 | 7 | 6 | UserCompanyDataStream | Organizations, ThirdParty |
| 41 | `i10a06IU4WQ` | 67% | 80% | 73% | 22% | 25% | 24% | 8 | 6 | 9 | 8 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 42 | `m8CBJEyHKIM` | 80% | 67% | 73% | 80% | 57% | 67% | 6 | 6 | 5 | 7 | NLB, UserConsumerMobile | ELB |
| 43 | `K5ww_O4vsxo` | 60% | 75% | 67% | 82% | 17% | 29% | 11 | 15 | 11 | 52 | ThirdParty | OnPremDC, S2SVPN |
| 44 | `phN08pi3YzY` | 50% | 75% | 60% | 0% | 0% | 0% | 6 | 5 | 5 | 0 | ThirdParty | GuardDuty, KMS, SystemsManager |
| 45 | `X3mC6Yfd138` | 50% | 67% | 57% | 0% | 0% | 0% | 11 | 9 | 9 | 10 | EC2, UserCompanyDeveloper | AutoScaling, RDS, UserCompanyWebsite (+1) |
| 46 | `99nNHsbwBpg` | 50% | 50% | 50% | 0% | 0% | 0% | 3 | 2 | 2 | 0 | EC2 | ThirdParty |
| 47 | `u9DZRkJxvWo` | 25% | 100% | 40% | 14% | 100% | 25% | 8 | 2 | 7 | 1 | — | Comprehend, Lambda, S3 (+3) |
| 48 | `zmJ7rL1iQBY` | 25% | 100% | 40% | 0% | 0% | 0% | 7 | 1 | 5 | 0 | — | DirectoryService, IAM, ThirdParty |
| 49 | `BgT_bDAejSQ` | 17% | 100% | 29% | 0% | 0% | 0% | 7 | 2 | 5 | 1 | — | ALB, NAT, OnPremDC (+2) |



---

## Parsimonious API (data/graphs_parsimonious) Evaluation Details

### Detailed Results Table (Sorted by Service F1)

### Detailed Results Table: Core Evaluation (Valid Ground Truths)

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `1SwHH7qQ6Pc` | 100% | 100% | 100% | 88% | 54% | 67% | 10 | 10 | 8 | 13 | — | — |
| 2 | `4zVB5RbSTCo` | 100% | 100% | 100% | 100% | 57% | 73% | 9 | 9 | 8 | 14 | — | — |
| 3 | `6YkguepAQuQ` | 100% | 100% | 100% | 75% | 30% | 43% | 10 | 10 | 4 | 10 | — | — |
| 4 | `7dtomip_VXc` | 100% | 100% | 100% | 100% | 55% | 71% | 8 | 8 | 6 | 11 | — | — |
| 5 | `9Cg81Xgg7LQ` | 100% | 100% | 100% | 100% | 71% | 83% | 7 | 7 | 5 | 7 | — | — |
| 6 | `A4Lfk1Zz1dE` | 100% | 100% | 100% | 29% | 40% | 33% | 8 | 8 | 7 | 5 | — | — |
| 7 | `Cgv0kfp_6xQ` | 100% | 100% | 100% | 100% | 71% | 83% | 11 | 10 | 10 | 14 | — | — |
| 8 | `DkPPwq517aE` | 100% | 100% | 100% | 100% | 64% | 78% | 10 | 10 | 9 | 14 | — | — |
| 9 | `F4KDOGNpSoI` | 100% | 100% | 100% | 94% | 79% | 86% | 14 | 14 | 16 | 19 | — | — |
| 10 | `G5tNCpmD2uQ` | 100% | 100% | 100% | 71% | 42% | 53% | 10 | 9 | 7 | 12 | — | — |
| 11 | `H2fOkeXxpyw` | 100% | 100% | 100% | 100% | 70% | 82% | 8 | 8 | 7 | 10 | — | — |
| 12 | `HcmEFZukA-Y` | 100% | 100% | 100% | 89% | 53% | 67% | 9 | 9 | 9 | 15 | — | — |
| 13 | `IV3KuMGVNXI` | 100% | 100% | 100% | 80% | 24% | 36% | 7 | 7 | 5 | 17 | — | — |
| 14 | `JcHSFIZMYHc` | 100% | 100% | 100% | 100% | 89% | 94% | 8 | 8 | 8 | 9 | — | — |
| 15 | `Jz2RPRhF6Fs` | 100% | 100% | 100% | 100% | 69% | 82% | 10 | 10 | 9 | 13 | — | — |
| 16 | `Ly_UhX3LCCs` | 100% | 100% | 100% | 40% | 57% | 47% | 9 | 7 | 10 | 7 | — | — |
| 17 | `O5Sn5QCEAzE` | 100% | 100% | 100% | 100% | 78% | 88% | 7 | 7 | 7 | 9 | — | — |
| 18 | `Q6r_QbYXFpg` | 100% | 100% | 100% | 100% | 100% | 100% | 11 | 11 | 9 | 9 | — | — |
| 19 | `QJZHs1CSxu0` | 100% | 100% | 100% | 83% | 83% | 83% | 6 | 6 | 6 | 6 | — | — |
| 20 | `Qi9soN5bpU4` | 100% | 100% | 100% | 100% | 60% | 75% | 8 | 8 | 6 | 10 | — | — |
| 21 | `U8xlmurP-6o` | 100% | 100% | 100% | 89% | 80% | 84% | 10 | 10 | 9 | 10 | — | — |
| 22 | `WS2Qgx0qgCM` | 100% | 100% | 100% | 100% | 88% | 93% | 6 | 6 | 7 | 8 | — | — |
| 23 | `Wur1GWB03hk` | 100% | 100% | 100% | 100% | 29% | 44% | 9 | 9 | 4 | 14 | — | — |
| 24 | `XG6mHvi4eNU` | 100% | 100% | 100% | 100% | 60% | 75% | 7 | 6 | 6 | 10 | — | — |
| 25 | `Xi6tDqctLsY` | 100% | 100% | 100% | 100% | 62% | 77% | 8 | 8 | 10 | 16 | — | — |
| 26 | `XmIhHtPJWog` | 100% | 100% | 100% | 100% | 100% | 100% | 10 | 10 | 10 | 10 | — | — |
| 27 | `YlGUMhls9ZA` | 100% | 100% | 100% | 93% | 72% | 81% | 14 | 14 | 14 | 18 | — | — |
| 28 | `YrEc8oMIxDs` | 100% | 100% | 100% | 100% | 64% | 78% | 10 | 10 | 9 | 14 | — | — |
| 29 | `_EPfIJnBCoM` | 100% | 100% | 100% | 50% | 80% | 62% | 9 | 6 | 8 | 5 | — | — |
| 30 | `aN26J-7q9Hw` | 100% | 100% | 100% | 73% | 62% | 67% | 10 | 10 | 11 | 13 | — | — |
| 31 | `amh7nzl32v4` | 100% | 100% | 100% | 86% | 43% | 57% | 8 | 8 | 7 | 14 | — | — |
| 32 | `asZIXK7V-U4` | 100% | 100% | 100% | 85% | 69% | 76% | 10 | 10 | 13 | 16 | — | — |
| 33 | `az-C2c33trQ` | 100% | 100% | 100% | 100% | 53% | 69% | 8 | 8 | 9 | 17 | — | — |
| 34 | `cnZeOytEkIM` | 100% | 100% | 100% | 57% | 67% | 62% | 8 | 6 | 7 | 6 | — | — |
| 35 | `co4_t2gN1T8` | 100% | 100% | 100% | 100% | 56% | 72% | 9 | 9 | 9 | 16 | — | — |
| 36 | `fSV0u48sEVg` | 100% | 100% | 100% | 67% | 73% | 70% | 7 | 7 | 12 | 11 | — | — |
| 37 | `fppIOuRMI2g` | 100% | 100% | 100% | 100% | 86% | 92% | 7 | 7 | 6 | 7 | — | — |
| 38 | `ftIdBG-UgFY` | 100% | 100% | 100% | 75% | 33% | 46% | 8 | 8 | 4 | 9 | — | — |
| 39 | `hbz63Ve-eIY` | 100% | 100% | 100% | 100% | 38% | 56% | 6 | 6 | 5 | 13 | — | — |
| 40 | `hnMQFnTGr3I` | 100% | 100% | 100% | 100% | 46% | 63% | 11 | 9 | 11 | 24 | — | — |
| 41 | `hrhBOOrR5v0` | 100% | 100% | 100% | 78% | 58% | 67% | 8 | 9 | 9 | 12 | — | — |
| 42 | `iKYvG5aiIn8` | 100% | 100% | 100% | 75% | 86% | 80% | 9 | 9 | 8 | 7 | — | — |
| 43 | `jBffL9zUCSE` | 100% | 100% | 100% | 100% | 45% | 62% | 7 | 7 | 5 | 11 | — | — |
| 44 | `jV8DwutbXbg` | 100% | 100% | 100% | 100% | 64% | 78% | 7 | 7 | 7 | 11 | — | — |
| 45 | `ktonI7J3kLY` | 100% | 100% | 100% | 60% | 38% | 46% | 6 | 5 | 5 | 8 | — | — |
| 46 | `l0mvXogANE4` | 100% | 100% | 100% | 100% | 79% | 88% | 9 | 8 | 11 | 14 | — | — |
| 47 | `lecbHMBD8KQ` | 100% | 100% | 100% | 75% | 38% | 50% | 7 | 12 | 4 | 8 | — | — |
| 48 | `lkDq9g43djw` | 100% | 100% | 100% | 50% | 50% | 50% | 7 | 5 | 4 | 4 | — | — |
| 49 | `nM-AkqNh7Yo` | 100% | 100% | 100% | 50% | 60% | 55% | 10 | 8 | 12 | 10 | — | — |
| 50 | `qi017F1UwvM` | 100% | 100% | 100% | 82% | 58% | 68% | 17 | 17 | 17 | 24 | — | — |
| 51 | `rPGLNw1cOGM` | 100% | 100% | 100% | 100% | 40% | 57% | 8 | 8 | 8 | 20 | — | — |
| 52 | `sQsAGl7mSQs` | 100% | 100% | 100% | 73% | 46% | 56% | 12 | 12 | 15 | 24 | — | — |
| 53 | `uOSpWdAyrZo` | 100% | 100% | 100% | 88% | 100% | 93% | 8 | 8 | 8 | 7 | — | — |
| 54 | `unF9tdYjqvU` | 100% | 100% | 100% | 78% | 88% | 82% | 11 | 7 | 9 | 8 | — | — |
| 55 | `vdujJAab1LM` | 100% | 100% | 100% | 89% | 80% | 84% | 9 | 9 | 9 | 10 | — | — |
| 56 | `wE3TmHxyRdA` | 100% | 100% | 100% | 100% | 100% | 100% | 8 | 8 | 9 | 9 | — | — |
| 57 | `wzj2VQutJws` | 100% | 100% | 100% | 100% | 62% | 77% | 8 | 9 | 5 | 8 | — | — |
| 58 | `x76BIV88j_M` | 100% | 100% | 100% | 75% | 55% | 63% | 7 | 8 | 8 | 11 | — | — |
| 59 | `yXpd8gPfows` | 100% | 100% | 100% | 100% | 58% | 73% | 9 | 9 | 11 | 19 | — | — |
| 60 | `zr3Kib0i-OQ` | 100% | 100% | 100% | 100% | 100% | 100% | 7 | 7 | 6 | 6 | — | — |
| 61 | `2L0m28ZLmtE` | 92% | 100% | 96% | 83% | 91% | 87% | 14 | 13 | 12 | 11 | — | UserCompanyDeveloper |
| 62 | `6sew_hdI6cY` | 100% | 92% | 96% | 100% | 56% | 71% | 14 | 15 | 10 | 18 | EFS | — |
| 63 | `-3lnf5lzsH0` | 100% | 92% | 96% | 75% | 56% | 64% | 12 | 13 | 12 | 16 | EC2 | — |
| 64 | `YosezjoL4MU` | 100% | 92% | 96% | 100% | 55% | 71% | 11 | 12 | 6 | 11 | UserCompanyAnalyst | — |
| 65 | `2f_NYiPJQt4` | 91% | 100% | 95% | 50% | 33% | 40% | 11 | 10 | 6 | 9 | — | UserConsumerWebMobile |
| 66 | `Qz8uXtDC1bY` | 91% | 100% | 95% | 87% | 76% | 81% | 15 | 14 | 15 | 17 | — | RedShift |
| 67 | `ec6j-MaOSUc` | 100% | 91% | 95% | 89% | 40% | 55% | 10 | 11 | 9 | 20 | UserCompanyDeveloper | — |
| 68 | `Eoq7E6jMtBs` | 90% | 100% | 95% | 64% | 35% | 45% | 10 | 10 | 11 | 20 | — | UserCompanyAgent |
| 69 | `FHdtOtznWuA` | 100% | 90% | 95% | 100% | 28% | 43% | 9 | 10 | 5 | 18 | UserConsumerEdge | — |
| 70 | `J4vHfpL66Zk` | 100% | 90% | 95% | 100% | 59% | 74% | 9 | 10 | 10 | 17 | UserConsumerAPI | — |
| 71 | `hlVnmCfydIs` | 100% | 90% | 95% | 92% | 85% | 88% | 9 | 11 | 12 | 13 | UserConsumerMobile | — |
| 72 | `rRvy5Fbei1s` | 100% | 90% | 95% | 100% | 46% | 63% | 11 | 13 | 6 | 13 | UserConsumerAPI | — |
| 73 | `uWUAcc68MWI` | 90% | 100% | 95% | 80% | 53% | 64% | 13 | 11 | 10 | 15 | — | UserConsumerIOT |
| 74 | `vp8oPiHN4cA` | 100% | 90% | 95% | 42% | 26% | 32% | 9 | 14 | 12 | 19 | UserConsumerWeb | — |
| 75 | `0wnNlOg42dc` | 89% | 100% | 94% | 89% | 67% | 76% | 9 | 8 | 9 | 12 | — | UserConsumerWebMobile |
| 76 | `66h7DrOEF5k` | 89% | 100% | 94% | 82% | 100% | 90% | 12 | 9 | 11 | 9 | — | UserConsumerWebMobile |
| 77 | `7LziNjUTo7w` | 89% | 100% | 94% | 78% | 44% | 56% | 9 | 9 | 9 | 16 | — | UserCompanyAgent |
| 78 | `Dp3YAxFp-YM` | 89% | 100% | 94% | 89% | 57% | 70% | 10 | 10 | 9 | 14 | — | UserCompanyAgent |
| 79 | `LxeSC3-xMlk` | 89% | 100% | 94% | 78% | 47% | 58% | 10 | 8 | 9 | 15 | — | UserConsumerWeb |
| 80 | `a59halVklMI` | 100% | 89% | 94% | 100% | 56% | 72% | 11 | 12 | 9 | 16 | MSK | — |
| 81 | `dy-drIboyNA` | 100% | 89% | 94% | 82% | 69% | 75% | 12 | 15 | 11 | 13 | UserConsumerAPI | — |
| 82 | `j9OZ-7aCAyA` | 100% | 89% | 94% | 88% | 47% | 61% | 8 | 9 | 8 | 15 | UserCompanyDataStream | — |
| 83 | `m8xtR3-ZQs8` | 89% | 100% | 94% | 78% | 70% | 74% | 10 | 10 | 9 | 10 | — | VPC |
| 84 | `mq3XuoN0rUM` | 100% | 89% | 94% | 62% | 38% | 48% | 8 | 9 | 8 | 13 | ThirdParty | — |
| 85 | `uQFtb0iMC_s` | 89% | 100% | 94% | 82% | 100% | 90% | 9 | 8 | 11 | 9 | — | SageMaker |
| 86 | `yPJf85tjv6M` | 100% | 89% | 94% | 80% | 62% | 70% | 11 | 11 | 10 | 13 | UserConsumerWeb | — |
| 87 | `CTG23wd9H74` | 100% | 88% | 93% | 88% | 64% | 74% | 7 | 8 | 8 | 11 | UserCompanyAnalyst | — |
| 88 | `HrYfdnPp6qs` | 100% | 88% | 93% | 80% | 44% | 57% | 7 | 10 | 5 | 9 | ThirdParty | — |
| 89 | `NfUwtK8ALtw` | 88% | 100% | 93% | 42% | 31% | 36% | 9 | 9 | 12 | 16 | — | AutoScaling |
| 90 | `PgeQufaQy7I` | 100% | 88% | 93% | 100% | 75% | 86% | 7 | 8 | 6 | 8 | CloudFormation | — |
| 91 | `XUCGMzLx8wY` | 100% | 88% | 93% | 50% | 44% | 47% | 7 | 8 | 8 | 9 | UserConsumerMobile | — |
| 92 | `bikXzsVihF4` | 88% | 100% | 93% | 57% | 40% | 47% | 8 | 7 | 7 | 10 | — | ServiceNow |
| 93 | `bxvZBfbyhiA` | 100% | 88% | 93% | 100% | 58% | 74% | 8 | 9 | 7 | 12 | UserConsumerDeveloper | — |
| 94 | `iWK0iRUi-b4` | 100% | 88% | 93% | 58% | 58% | 58% | 8 | 8 | 12 | 12 | UserConsumerWeb | — |
| 95 | `pZ7Lr94noLo` | 100% | 88% | 93% | 75% | 40% | 52% | 11 | 13 | 8 | 15 | ApiGateway | — |
| 96 | `plce6pRdx6o` | 88% | 100% | 93% | 57% | 67% | 62% | 9 | 8 | 7 | 6 | — | UserConsumerWebMobile |
| 97 | `qN5-v4NlKac` | 88% | 100% | 93% | 89% | 80% | 84% | 10 | 10 | 9 | 10 | — | OpenSearch |
| 98 | `rHLuQTO6eoo` | 100% | 88% | 93% | 77% | 71% | 74% | 9 | 10 | 13 | 14 | UserCompanyAnalyst | — |
| 99 | `u3ZwnulzLnU` | 88% | 100% | 93% | 73% | 62% | 67% | 9 | 8 | 11 | 13 | — | OpenSearch |
| 100 | `unFVfqj9cQ8` | 100% | 88% | 93% | 100% | 71% | 83% | 7 | 8 | 5 | 7 | ControlTower | — |
| 101 | `d0EE1HuZSEU` | 92% | 92% | 92% | 80% | 57% | 67% | 13 | 13 | 15 | 21 | ThirdParty | OnPremDC |
| 102 | `1aYoIZvabbk` | 86% | 100% | 92% | 57% | 80% | 67% | 7 | 6 | 7 | 5 | — | EC2 |
| 103 | `5vR5aN_xdI0` | 100% | 86% | 92% | 50% | 20% | 29% | 9 | 9 | 4 | 10 | UserConsumerAPI | — |
| 104 | `6EUknQqaV1w` | 100% | 86% | 92% | 82% | 82% | 82% | 8 | 9 | 11 | 11 | UserCompanyDataStream | — |
| 105 | `6iK4WNj6QqI` | 86% | 100% | 92% | 38% | 30% | 33% | 7 | 6 | 8 | 10 | — | CloudFront |
| 106 | `CDCLwX2fo2g` | 100% | 86% | 92% | 90% | 64% | 75% | 8 | 8 | 10 | 14 | UserConsumerMobile | — |
| 107 | `Ccutfm_Srzw` | 100% | 86% | 92% | 62% | 36% | 45% | 8 | 11 | 8 | 14 | KinesisDataStream | — |
| 108 | `CsD5bmM6mpY` | 86% | 100% | 92% | 43% | 43% | 43% | 8 | 6 | 7 | 7 | — | ThirdParty |
| 109 | `FftalZUxyiM` | 100% | 86% | 92% | 100% | 50% | 67% | 8 | 9 | 7 | 14 | UserConsumerWeb | — |
| 110 | `K27WjYwyqw8` | 100% | 86% | 92% | 88% | 64% | 74% | 7 | 8 | 8 | 11 | UserConsumerMobile | — |
| 111 | `QM96Fv_NAnw` | 100% | 86% | 92% | 60% | 50% | 55% | 6 | 7 | 5 | 6 | ThirdParty | — |
| 112 | `a1sEfGVDpEQ` | 100% | 86% | 92% | 100% | 54% | 70% | 9 | 10 | 7 | 13 | ThirdParty | — |
| 113 | `c2TGPlvAHLs` | 86% | 100% | 92% | 67% | 80% | 73% | 7 | 6 | 6 | 5 | — | UserConsumerWebMobile |
| 114 | `hf9nMAG9XoU` | 100% | 86% | 92% | 86% | 55% | 67% | 7 | 8 | 7 | 11 | UserCompanyDataStream | — |
| 115 | `mZxF1IJEsaY` | 86% | 100% | 92% | 80% | 100% | 89% | 9 | 8 | 10 | 8 | — | UserConsumerWeb |
| 116 | `pwxhclKcMas` | 100% | 86% | 92% | 75% | 46% | 57% | 8 | 10 | 8 | 13 | UserCompanyAPI | — |
| 117 | `sezX7CSbXTg` | 86% | 100% | 92% | 75% | 75% | 75% | 8 | 7 | 8 | 8 | — | UserCompanyInternalPlatform |
| 118 | `uBiaWJbTRsE` | 86% | 100% | 92% | 73% | 89% | 80% | 9 | 8 | 11 | 9 | — | EC2 |
| 119 | `xKaPAihW_gE` | 100% | 86% | 92% | 88% | 88% | 88% | 7 | 8 | 8 | 8 | VPC | — |
| 120 | `5CwIt-Alqhg` | 91% | 91% | 91% | 90% | 75% | 82% | 11 | 11 | 10 | 12 | UserCompanyAgent | UserConsumerMobile |
| 121 | `PBa68gCG0Uk` | 100% | 83% | 91% | 83% | 71% | 77% | 6 | 7 | 6 | 7 | ThirdParty | — |
| 122 | `RxAmb57NCPM` | 100% | 83% | 91% | 82% | 75% | 78% | 12 | 13 | 11 | 12 | UserCompanyAPI | — |
| 123 | `U1P8vZTEB-k` | 100% | 83% | 91% | 77% | 71% | 74% | 11 | 12 | 13 | 14 | UserCompanyAnalyst, UserConsumerAPI | — |
| 124 | `ZNt9qI_LlPk` | 83% | 100% | 91% | 56% | 50% | 53% | 7 | 5 | 9 | 10 | — | UserConsumerWeb |
| 125 | `dWCQw_KvlYQ` | 100% | 83% | 91% | 100% | 53% | 70% | 10 | 12 | 8 | 15 | ThirdParty, UserConsumerTV | — |
| 126 | `gcgtLDB0cKA` | 91% | 91% | 91% | 92% | 61% | 73% | 13 | 13 | 12 | 18 | UserCompanyEdge | UserConsumerIOT |
| 127 | `ooVtAAoSH2k` | 100% | 83% | 91% | 100% | 56% | 71% | 6 | 7 | 5 | 9 | UserCompanyDeveloper | — |
| 128 | `pCZ0bxgBL5c` | 83% | 100% | 91% | 88% | 47% | 61% | 7 | 8 | 8 | 15 | — | UserConsumerMobile |
| 129 | `qIO_54vJ_JI` | 100% | 83% | 91% | 100% | 86% | 92% | 7 | 8 | 6 | 7 | UserCompanyAgent | — |
| 130 | `07lfvavMdfU` | 90% | 90% | 90% | 82% | 64% | 72% | 10 | 10 | 11 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 131 | `9yziTe6lBwk` | 90% | 90% | 90% | 89% | 50% | 64% | 10 | 10 | 9 | 16 | UserConsumerMobile | UserConsumerWebMobile |
| 132 | `DxHO2TWVN8I` | 90% | 90% | 90% | 62% | 42% | 50% | 10 | 10 | 13 | 19 | UserConsumerWeb | UserConsumerWebMobile |
| 133 | `ErXwuwF2mRU` | 82% | 100% | 90% | 50% | 50% | 50% | 11 | 9 | 10 | 10 | — | Aurora, ThirdParty |
| 134 | `JG5p-i8Cr2E` | 90% | 90% | 90% | 77% | 42% | 54% | 11 | 11 | 13 | 24 | UserCompanyDeveloper | UserCompanyAgent |
| 135 | `KQ6Fg206O9U` | 90% | 90% | 90% | 82% | 64% | 72% | 10 | 10 | 11 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 136 | `oTtPNgcZ05I` | 90% | 90% | 90% | 67% | 18% | 29% | 10 | 10 | 3 | 11 | UserCompanyAnalyst | UserCompanyDeveloper |
| 137 | `w-qGSyzDL6g` | 100% | 82% | 90% | 70% | 44% | 54% | 11 | 12 | 10 | 16 | UserCompanyAnalyst, UserCompanyDataStream | — |
| 138 | `4WjXH8Wp0E4` | 100% | 80% | 89% | 83% | 45% | 59% | 13 | 14 | 12 | 22 | ThirdParty, UserConsumerWeb | — |
| 139 | `INog0_9tCtY` | 100% | 80% | 89% | 73% | 42% | 53% | 12 | 14 | 11 | 19 | OpenSearch, UserCompanyAnalyst | — |
| 140 | `RCWl0rf8lpE` | 80% | 100% | 89% | 73% | 80% | 76% | 10 | 7 | 11 | 10 | — | ThirdParty |
| 141 | `ZA_0RMeeWpY` | 80% | 100% | 89% | 71% | 62% | 67% | 8 | 5 | 7 | 8 | — | VPC |
| 142 | `l0hlxVNmJPI` | 80% | 100% | 89% | 33% | 50% | 40% | 15 | 14 | 6 | 4 | — | CloudWatch, UserCompanyDeveloper, UserConsumerIOT |
| 143 | `lHM96P5kP2k` | 80% | 100% | 89% | 69% | 64% | 67% | 11 | 11 | 13 | 14 | — | UserConsumerWeb |
| 144 | `6CgqEzyWpeA` | 89% | 89% | 89% | 62% | 53% | 57% | 12 | 12 | 16 | 19 | EC2 | AutoScaling |
| 145 | `Cw26CrJUqv8` | 89% | 89% | 89% | 80% | 89% | 84% | 10 | 10 | 10 | 9 | UserConsumerWeb | UserCompanyDeveloper |
| 146 | `JVcKidzqpYY` | 89% | 89% | 89% | 80% | 62% | 70% | 9 | 9 | 10 | 13 | UserCompanyDataStream | ThirdParty |
| 147 | `OQKOHNtyz3E` | 89% | 89% | 89% | 82% | 38% | 51% | 12 | 11 | 11 | 24 | UserConsumerMobile | UserConsumerWeb |
| 148 | `c6yBZBMwtLk` | 89% | 89% | 89% | 69% | 69% | 69% | 11 | 11 | 13 | 13 | UserCompanyElementalLiveDevice | ThirdParty |
| 149 | `f5EJBUfGZtw` | 89% | 89% | 89% | 70% | 88% | 78% | 10 | 10 | 10 | 8 | UserConsumerAPI | UserCompanyInternalPlatform |
| 150 | `iSkWd31X7zo` | 89% | 89% | 89% | 86% | 67% | 75% | 9 | 9 | 7 | 9 | UserConsumerAPI | UserConsumerWebMobile |
| 151 | `mKZw29_UtoU` | 89% | 89% | 89% | 92% | 65% | 76% | 10 | 10 | 12 | 17 | UserCompanyEdge | UserConsumerIOT |
| 152 | `nt4lQx6tAI8` | 89% | 89% | 89% | 73% | 40% | 52% | 10 | 10 | 11 | 20 | UserConsumerMobile | UserConsumerWebMobile |
| 153 | `vb-o1DvvHxk` | 89% | 89% | 89% | 57% | 73% | 64% | 11 | 10 | 14 | 11 | UserCompanyDataStream | ThirdParty |
| 154 | `Gds8hl8dKuo` | 78% | 100% | 88% | 43% | 25% | 32% | 10 | 8 | 7 | 12 | — | STS, VPC |
| 155 | `5EmA67lSJEs` | 88% | 88% | 88% | 67% | 40% | 50% | 10 | 11 | 12 | 20 | UserConsumerAPI | ThirdParty |
| 156 | `5QbKp0LQaZo` | 88% | 88% | 88% | 40% | 25% | 31% | 10 | 10 | 10 | 16 | UserConsumerWeb | UserConsumerWebMobile |
| 157 | `AzM_d7ZvzUE` | 88% | 88% | 88% | 55% | 30% | 39% | 11 | 11 | 11 | 20 | Kinesis | KinesisDataStream |
| 158 | `BX1K8x1lVLc` | 88% | 88% | 88% | 88% | 50% | 64% | 8 | 8 | 8 | 14 | UserConsumerWeb | UserConsumerWebMobile |
| 159 | `FfSNnH2bbNc` | 88% | 88% | 88% | 89% | 42% | 57% | 8 | 8 | 9 | 19 | UserConsumerSatellite | ThirdParty |
| 160 | `IP03SkGbP-U` | 88% | 88% | 88% | 56% | 71% | 63% | 8 | 8 | 9 | 7 | UserConsumerWeb | VPC |
| 161 | `OuQvFd44vw4` | 88% | 88% | 88% | 78% | 78% | 78% | 10 | 10 | 9 | 9 | ThirdParty | UserCompanyInternalPlatform |
| 162 | `Pc7_uOdlGKo` | 88% | 88% | 88% | 89% | 89% | 89% | 9 | 9 | 9 | 9 | UserConsumerMobile | UserConsumerWeb |
| 163 | `SpIlpGxuwFM` | 88% | 88% | 88% | 71% | 62% | 67% | 8 | 8 | 7 | 8 | ThirdParty | CloudFormation |
| 164 | `T048vs9p1h4` | 88% | 88% | 88% | 80% | 35% | 48% | 12 | 12 | 10 | 23 | UserConsumerAPI | ApiGateway |
| 165 | `Wk9mCHyjtBU` | 88% | 88% | 88% | 75% | 38% | 50% | 9 | 10 | 8 | 16 | UserConsumerWeb | UserCompanyInternalPlatform |
| 166 | `_pXybA6832o` | 88% | 88% | 88% | 82% | 82% | 82% | 9 | 9 | 11 | 11 | UserConsumerAlexaGoogleHome | AlexaForBusiness |
| 167 | `chQ1phTqvnY` | 88% | 88% | 88% | 80% | 33% | 47% | 10 | 10 | 10 | 24 | AmazonML | SageMaker |
| 168 | `iwDNnyiD26M` | 88% | 88% | 88% | 44% | 44% | 44% | 10 | 9 | 9 | 9 | ThirdParty | OnPremDC |
| 169 | `jg85DzUZ9Ac` | 88% | 88% | 88% | 82% | 82% | 82% | 10 | 10 | 11 | 11 | UserCompanyDataStream | OnPremDC |
| 170 | `k7h0jpLcWdE` | 88% | 88% | 88% | 75% | 75% | 75% | 8 | 8 | 8 | 8 | UserConsumerWeb | UserConsumerWebMobile |
| 171 | `kHPGZOpbnok` | 88% | 88% | 88% | 56% | 42% | 48% | 8 | 8 | 9 | 12 | Kinesis | KinesisDataStream |
| 172 | `nflGdpwbf54` | 88% | 88% | 88% | 70% | 64% | 67% | 8 | 8 | 10 | 11 | UserConsumerWeb | UserCompanyDomainExpert |
| 173 | `uda9s3U7vFw` | 88% | 88% | 88% | 78% | 70% | 74% | 10 | 10 | 9 | 10 | UserConsumerMobile | UserConsumerWebMobile |
| 174 | `QnwfcDZkwh8` | 100% | 77% | 87% | 80% | 44% | 57% | 10 | 13 | 10 | 18 | UserCompanyDeveloper, UserConsumerMobile, UserConsumerTV | — |
| 175 | `S85DeDgWQSc` | 90% | 82% | 86% | 70% | 50% | 58% | 10 | 12 | 10 | 14 | StepFunctions, UserCompanyAnalyst | UserCompanyAgent |
| 176 | `37T7Nd8pL-c` | 86% | 86% | 86% | 50% | 33% | 40% | 7 | 8 | 8 | 12 | UserConsumerAPI | UserConsumerWebMobile |
| 177 | `5f3z1Z_9BJA` | 86% | 86% | 86% | 92% | 71% | 80% | 11 | 11 | 13 | 17 | UserCompanyDataStream | OnPremDC |
| 178 | `90rWUjKjnAE` | 86% | 86% | 86% | 75% | 60% | 67% | 9 | 8 | 8 | 10 | UserConsumerDeveloper | UserCompanyDeveloper |
| 179 | `D77FSUkPJ3o` | 86% | 86% | 86% | 60% | 50% | 55% | 8 | 8 | 10 | 12 | UserConsumerWeb | UserCompanyAgent |
| 180 | `E8wYXtvGy5k` | 86% | 86% | 86% | 89% | 67% | 76% | 10 | 10 | 9 | 12 | UserConsumerMobile | UserCompanyAgent |
| 181 | `EiljRL0977M` | 86% | 86% | 86% | 67% | 31% | 42% | 7 | 7 | 6 | 13 | ThirdParty | S3 |
| 182 | `Fd2c7NDYfpo` | 86% | 86% | 86% | 75% | 50% | 60% | 8 | 8 | 8 | 12 | ThirdParty | SES |
| 183 | `Felt-hOU6kU` | 75% | 100% | 86% | 50% | 100% | 67% | 9 | 7 | 8 | 4 | — | ThirdParty, VPC |
| 184 | `ItpY_KKR94k` | 86% | 86% | 86% | 75% | 86% | 80% | 9 | 8 | 8 | 7 | UserCompanyCRM | ThirdParty |
| 185 | `Jkx6kVbDpL4` | 86% | 86% | 86% | 88% | 82% | 85% | 13 | 13 | 16 | 17 | UserCompanyAnalyst | ThirdParty |
| 186 | `SSWwnNVYi_Q` | 86% | 86% | 86% | 67% | 40% | 50% | 8 | 8 | 6 | 10 | UserConsumerWeb | UserCompanyAnalyst |
| 187 | `cZuoiXQ0xUk` | 86% | 86% | 86% | 62% | 38% | 48% | 8 | 8 | 8 | 13 | ThirdParty | UserConsumerWeb |
| 188 | `eEfWd4EgH_s` | 86% | 86% | 86% | 89% | 80% | 84% | 10 | 10 | 9 | 10 | UserCompanyDataStream | RDS |
| 189 | `fTxvwVj02P0` | 86% | 86% | 86% | 86% | 60% | 71% | 8 | 8 | 7 | 10 | ThirdParty | EC2 |
| 190 | `h0HE3bOEiMk` | 86% | 86% | 86% | 78% | 78% | 78% | 7 | 7 | 9 | 9 | ThirdParty | OnPremDC |
| 191 | `wjtSHyENv0I` | 86% | 86% | 86% | 71% | 36% | 48% | 8 | 8 | 7 | 14 | UserConsumerWeb | UserCompanyAgent |
| 192 | `ww5fiygF6eg` | 86% | 86% | 86% | 57% | 20% | 30% | 7 | 10 | 7 | 20 | UserCompanyDrone | OnPremDC |
| 193 | `zhCNn7v7mvs` | 86% | 86% | 86% | 70% | 64% | 67% | 9 | 8 | 10 | 11 | UserConsumerAPI | ThirdParty |
| 194 | `AS2JeM2FUzE` | 80% | 89% | 84% | 73% | 67% | 70% | 10 | 9 | 11 | 12 | UserCompanyDataStream | ThirdParty, UserCompanyAgent |
| 195 | `DnTQ3matqts` | 80% | 89% | 84% | 60% | 43% | 50% | 14 | 14 | 10 | 14 | UserConsumerEdge | SNS, UserConsumerIOT |
| 196 | `HwHVFWdczVw` | 80% | 89% | 84% | 80% | 89% | 84% | 10 | 9 | 10 | 9 | UserConsumerWebMobile | ThirdParty, UserConsumerWeb |
| 197 | `Ozbv9qBsDG8` | 73% | 100% | 84% | 58% | 41% | 48% | 14 | 11 | 12 | 17 | — | CloudFormation, DynamoDB, RDS |
| 198 | `StSuG6-iKW4` | 80% | 89% | 84% | 50% | 57% | 53% | 10 | 10 | 8 | 7 | UserConsumerEdge | UserConsumerIOT, UserConsumerWebMobile |
| 199 | `a6kqyqTNJM4` | 80% | 89% | 84% | 56% | 33% | 42% | 11 | 11 | 9 | 15 | UserConsumerWeb | ELB, UserConsumerWebMobile |
| 200 | `r2xfxJ-sXMY` | 80% | 89% | 84% | 60% | 60% | 60% | 11 | 9 | 10 | 10 | EC2 | UserConsumerMobile, UserConsumerWeb |
| 201 | `2e3vOxsHekE` | 83% | 83% | 83% | 75% | 50% | 60% | 6 | 6 | 4 | 6 | UserConsumerEdge | UserConsumerIOT |
| 202 | `66fPHLmvikk` | 83% | 83% | 83% | 50% | 75% | 60% | 11 | 7 | 12 | 8 | UserCompanyAnalyst | UserCompanyDeveloper |
| 203 | `BlCXEMp_lqY` | 83% | 83% | 83% | 60% | 33% | 43% | 6 | 6 | 5 | 9 | Kinesis | KinesisDataStream |
| 204 | `N2mktbl8EQk` | 83% | 83% | 83% | 60% | 33% | 43% | 6 | 6 | 5 | 9 | Kinesis | KinesisVideo |
| 205 | `WxMBuBBIwpI` | 83% | 83% | 83% | 80% | 57% | 67% | 6 | 6 | 5 | 7 | Lambda | UserConsumerWeb |
| 206 | `_vjB_vF4Uec` | 83% | 83% | 83% | 14% | 11% | 12% | 10 | 6 | 7 | 9 | UserConsumerEdge | UserCompanyEdge |
| 207 | `aQFztbu0BG0` | 83% | 83% | 83% | 75% | 75% | 75% | 8 | 8 | 8 | 8 | ThirdParty | OnPremDC |
| 208 | `ccPhkyPm_3w` | 83% | 83% | 83% | 33% | 33% | 33% | 9 | 6 | 6 | 6 | UserCompanyDataStream | ThirdParty |
| 209 | `ekXdohpAy5U` | 83% | 83% | 83% | 80% | 44% | 57% | 6 | 6 | 5 | 9 | UserCompanyDataStream | ThirdParty |
| 210 | `pk5yddJpC_8` | 83% | 83% | 83% | 88% | 70% | 78% | 9 | 9 | 8 | 10 | UserCompanyDeveloper | UserCompanyInternalPlatform |
| 211 | `0F7KDLz-kIQ` | 77% | 91% | 83% | 76% | 46% | 58% | 15 | 13 | 17 | 28 | UserConsumerWeb | DevTools, ECS, UserConsumerWebMobile |
| 212 | `D_4dsXVqzMs` | 71% | 100% | 83% | 83% | 50% | 62% | 8 | 7 | 6 | 10 | — | Lambda, OnPremDC |
| 213 | `OrC9cLYMbas` | 71% | 100% | 83% | 25% | 14% | 18% | 7 | 5 | 4 | 7 | — | ECS, UserCompanyInternalPlatform |
| 214 | `6LcSv9XocTY` | 88% | 78% | 82% | 75% | 33% | 46% | 10 | 11 | 8 | 18 | Firehose, ThirdParty | UserCompanyCRM |
| 215 | `CE03UMddoYU` | 78% | 88% | 82% | 75% | 75% | 75% | 11 | 10 | 12 | 12 | UserConsumerEdge | UserConsumerIOT, UserConsumerMobile |
| 216 | `GJ1So_pbZWk` | 78% | 88% | 82% | 80% | 35% | 48% | 10 | 9 | 10 | 23 | UserConsumerWeb | UserCompanyAnalyst, UserConsumerAPI |
| 217 | `H_S7CxtHgSM` | 78% | 88% | 82% | 54% | 58% | 56% | 12 | 11 | 13 | 12 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 218 | `KiH7hVJKzns` | 78% | 88% | 82% | 70% | 50% | 58% | 9 | 8 | 10 | 14 | UserConsumerWebMobile | UserConsumerMobile, UserConsumerWeb |
| 219 | `RU__HBEMDvQ` | 88% | 78% | 82% | 71% | 50% | 59% | 8 | 9 | 7 | 10 | UserCompanyAnalyst, UserCompanyDataStream | ThirdParty |
| 220 | `c863uNkF0w4` | 88% | 78% | 82% | 60% | 38% | 46% | 8 | 10 | 5 | 8 | UserConsumerAPI, UserConsumerEdge | AutoScaling |
| 221 | `fRv8sOUyhZw` | 88% | 78% | 82% | 73% | 62% | 67% | 10 | 10 | 11 | 13 | OpenSearch, UserCompanyAPI | ApiGateway |
| 222 | `oEmuI32GYww` | 88% | 78% | 82% | 50% | 80% | 62% | 8 | 10 | 8 | 5 | ThirdParty, UserConsumerEdge | UserConsumerIOT |
| 223 | `yVgxqT1vikk` | 78% | 88% | 82% | 55% | 38% | 44% | 11 | 10 | 11 | 16 | UserCompanyDataStream | UserCompanyAnalyst, UserConsumerWebMobile |
| 224 | `YiOTd6IfGoU` | 82% | 82% | 82% | 73% | 62% | 67% | 12 | 12 | 11 | 13 | ThirdParty, UserCompanyDataStream | EC2, UserCompanyInternalPlatform |
| 225 | `dAQhNjwkOX8` | 82% | 82% | 82% | 62% | 42% | 50% | 13 | 14 | 16 | 24 | UserCompanyAgent, UserConsumerAPI | UserCompanyAnalyst, UserConsumerWebMobile |
| 226 | `uhrheMJTV4A` | 82% | 82% | 82% | 70% | 47% | 56% | 11 | 11 | 10 | 15 | Kinesis, UserCompanyDataStream | KinesisDataStream, UserCompanyEdge |
| 227 | `BZ32w0SSAoY` | 80% | 80% | 80% | 88% | 37% | 52% | 7 | 7 | 8 | 19 | ThirdParty | RDS |
| 228 | `FqCs3BD6qvo` | 80% | 80% | 80% | 43% | 30% | 35% | 9 | 6 | 7 | 10 | VPN | OnPremDC |
| 229 | `JRDGId6N49E` | 80% | 80% | 80% | 33% | 33% | 33% | 7 | 6 | 3 | 3 | ThirdParty | FSX |
| 230 | `JiWHomdh1oI` | 80% | 80% | 80% | 89% | 73% | 80% | 7 | 7 | 9 | 11 | UserCompanyDataStream | ThirdParty |
| 231 | `R-DPMUjZEf4` | 80% | 80% | 80% | 83% | 83% | 83% | 7 | 7 | 6 | 6 | UserConsumerWeb | UserConsumerWebMobile |
| 232 | `YV8e36ZywLk` | 80% | 80% | 80% | 0% | 0% | 0% | 5 | 5 | 4 | 4 | ThirdParty | SAP |
| 233 | `bqZWYmRAka0` | 80% | 80% | 80% | 33% | 80% | 47% | 10 | 5 | 12 | 5 | UserConsumerAPI | UserConsumerWeb |
| 234 | `gD8pzUnXgsU` | 80% | 80% | 80% | 50% | 50% | 50% | 9 | 6 | 4 | 4 | ThirdParty | EC2 |
| 235 | `j-lPgPGBTwQ` | 80% | 80% | 80% | 55% | 38% | 44% | 11 | 11 | 11 | 16 | Fargate, ThirdParty | ECS, UserConsumerIOT |
| 236 | `kD57QUn5myc` | 80% | 80% | 80% | 29% | 17% | 21% | 10 | 10 | 7 | 12 | Kinesis, UserConsumerMobile | KinesisVideo, UserConsumerWebMobile |
| 237 | `nvhG60gFbso` | 80% | 80% | 80% | 36% | 25% | 30% | 12 | 13 | 11 | 16 | ThirdParty, VPC | OnPremDC, UserConsumerWeb |
| 238 | `LYP98nPBj2A` | 67% | 100% | 80% | 43% | 38% | 40% | 8 | 5 | 7 | 8 | — | UserCompanyAgent, VPC |
| 239 | `-ahWdCysMYw` | 86% | 75% | 80% | 40% | 22% | 29% | 7 | 8 | 5 | 9 | ThirdParty, UserCompanyAnalyst | OnPremDC |
| 240 | `0JxJpNjI9Y0` | 75% | 86% | 80% | 70% | 41% | 52% | 10 | 9 | 10 | 17 | UserConsumerAPI | UserCompanyDeveloper, UserConsumerWebMobile |
| 241 | `1xLjtJnfZes` | 86% | 75% | 80% | 60% | 50% | 55% | 8 | 8 | 5 | 6 | UserCompanyDataStream, UserConsumerAPI | UserConsumerWebMobile |
| 242 | `9qTEHITVeLE` | 75% | 86% | 80% | 67% | 57% | 62% | 10 | 9 | 12 | 14 | UserConsumerWeb | OpenSearch, UserCompanyAnalyst |
| 243 | `JYeXbUdFOdw` | 75% | 86% | 80% | 45% | 36% | 40% | 13 | 8 | 11 | 14 | UserConsumerWeb | EC2, UserConsumerWebMobile |
| 244 | `Kp088QTRmLk` | 75% | 86% | 80% | 80% | 80% | 80% | 9 | 9 | 10 | 10 | UserConsumerWeb | RDS, UserConsumerWebMobile |
| 245 | `Kp51k6LY-2c` | 86% | 75% | 80% | 67% | 25% | 36% | 7 | 8 | 6 | 16 | UserCompanyAnalyst, UserCompanyDataStream | OnPremDC |
| 246 | `O11BgSm7V14` | 86% | 75% | 80% | 80% | 31% | 44% | 9 | 10 | 5 | 13 | EventBridge, UserConsumerWeb | ThirdParty |
| 247 | `XpFNznmRoQ0` | 73% | 89% | 80% | 79% | 69% | 73% | 14 | 12 | 14 | 16 | UserCompanyDataStream | RDS, ThirdParty, UserConsumerWeb |
| 248 | `Yju3yReAQtc` | 75% | 86% | 80% | 50% | 43% | 46% | 13 | 7 | 6 | 7 | UserCompanyInternalPlatform | ThirdParty, UserConsumerWeb |
| 249 | `ZCj2wuKBBu4` | 86% | 75% | 80% | 50% | 33% | 40% | 7 | 9 | 6 | 9 | EC2, ThirdParty | AutoScaling |
| 250 | `mtZvA7ARepM` | 86% | 75% | 80% | 75% | 38% | 50% | 8 | 9 | 8 | 16 | Kinesis, UserConsumerAPI | KinesisDataStream |
| 251 | `sSa4ikC8-Jc` | 75% | 86% | 80% | 78% | 29% | 42% | 11 | 11 | 9 | 24 | UserConsumerWeb | UserCompanyInternalPlatform, UserConsumerWebMobile |
| 252 | `WYK-smWKywA` | 75% | 82% | 78% | 73% | 35% | 47% | 12 | 11 | 11 | 23 | ThirdParty, UserConsumerMobile | DirectConnect, OnPremDC, UserConsumerWeb |
| 253 | `ZPsBzAwJzoI` | 75% | 82% | 78% | 67% | 47% | 55% | 12 | 12 | 12 | 17 | EC2, UserConsumerTV | UserConsumerCamera, UserConsumerMobile, UserConsumerWeb |
| 254 | `0gNMEyei-co` | 78% | 78% | 78% | 82% | 69% | 75% | 9 | 9 | 11 | 13 | ThirdParty, UserCompanyDataStream | CloudWatch, UserCompanyInternalPlatform |
| 255 | `D6rG9eZ5Qus` | 78% | 78% | 78% | 62% | 56% | 59% | 9 | 9 | 8 | 9 | ThirdParty, UserCompanyDataStream | OnPremDC, SystemsManager |
| 256 | `E8BGpIxzYc4` | 78% | 78% | 78% | 55% | 55% | 55% | 10 | 10 | 11 | 11 | QuickSight, UserCompanyDataStream | MongoDBAtlas, ThirdParty |
| 257 | `G07keU4g-LU` | 78% | 78% | 78% | 55% | 29% | 37% | 10 | 10 | 11 | 21 | ThirdParty, UserCompanyAnalyst | EC2, RDS |
| 258 | `KM5ONS2fnG0` | 78% | 78% | 78% | 75% | 30% | 43% | 10 | 10 | 8 | 20 | Kinesis, UserCompanyDataStream | Firehose, KinesisDataStream |
| 259 | `KywvGM6HVXI` | 78% | 78% | 78% | 73% | 36% | 48% | 11 | 11 | 11 | 22 | Kinesis, UserConsumerWeb | KinesisDataStream, ThirdParty |
| 260 | `UsngU-HjH_Q` | 78% | 78% | 78% | 10% | 10% | 10% | 12 | 9 | 10 | 10 | UserCompanyDataStream, UserConsumerAPI | UserCompanyInternalPlatform, UserConsumerSatellite |
| 261 | `cmlhEbm1kPk` | 70% | 88% | 78% | 45% | 28% | 34% | 11 | 9 | 11 | 18 | MediaConnect | Connect, UserCompanyAgent, UserConsumerWebMobile |
| 262 | `gu54VVeDD10` | 70% | 88% | 78% | 64% | 78% | 70% | 10 | 8 | 11 | 9 | UserCompanyAnalyst | KinesisDataStream, ThirdParty, UserCompanyDeveloper |
| 263 | `mpgM2qeAfaQ` | 70% | 88% | 78% | 70% | 70% | 70% | 11 | 9 | 10 | 10 | UserConsumerWebMobile | UserConsumerCamera, UserConsumerMobile, UserConsumerWeb |
| 264 | `vr00Jg_G6qs` | 70% | 88% | 78% | 33% | 29% | 31% | 14 | 11 | 12 | 14 | UserConsumerHospital | ThirdParty, UserCompanyAgent, UserCompanyWebsite |
| 265 | `wtl7CrSQnHA` | 88% | 70% | 78% | 50% | 29% | 36% | 12 | 12 | 8 | 14 | Firehose, OpenSearch, UserConsumerEdge | ThirdParty |
| 266 | `Kebb0LOVC28` | 100% | 62% | 77% | 83% | 24% | 37% | 6 | 9 | 6 | 21 | CodeBuild, ECR, UserCompanyDeveloper | — |
| 267 | `53sUjFv9ByI` | 71% | 83% | 77% | 67% | 67% | 67% | 7 | 6 | 6 | 6 | ThirdParty | S3, UserCompanyAnalyst |
| 268 | `7V8wTCkjOqo` | 71% | 83% | 77% | 33% | 14% | 20% | 8 | 7 | 3 | 7 | ThirdParty | UserCompanyDeveloper, VPC |
| 269 | `9-6hQdFeolc` | 83% | 71% | 77% | 33% | 25% | 29% | 8 | 8 | 6 | 8 | UserCompanyCRM, UserCompanyDeveloper | ThirdParty |
| 270 | `D9qTotVJYss` | 71% | 83% | 77% | 67% | 40% | 50% | 7 | 6 | 6 | 10 | UserCompanyAgent | EventBridge, UserCompanyInternalPlatform |
| 271 | `S-JSSZZaa94` | 83% | 71% | 77% | 100% | 27% | 43% | 7 | 8 | 3 | 11 | ThirdParty, UserConsumerMobile | OpenSearch |
| 272 | `WtCfHP6rUAY` | 83% | 71% | 77% | 70% | 54% | 61% | 10 | 11 | 10 | 13 | UserCompanyAPI, UserCompanyDataStream | UserConsumerWeb |
| 273 | `aY-wF9g0qkM` | 83% | 71% | 77% | 56% | 36% | 43% | 9 | 10 | 9 | 14 | ThirdParty, UserConsumerEdge | UserConsumerCamera |
| 274 | `bQqJpjv-FXs` | 71% | 83% | 77% | 50% | 80% | 62% | 7 | 6 | 8 | 5 | UserCompanyDataStream | DynamoDB, UserConsumerIOT |
| 275 | `iwZLadQ3XpY` | 83% | 71% | 77% | 60% | 43% | 50% | 6 | 7 | 5 | 7 | ThirdParty, UserConsumerMobile | UserConsumerWebMobile |
| 276 | `lTSZT10JMQA` | 83% | 71% | 77% | 78% | 33% | 47% | 10 | 10 | 9 | 21 | UserCompanyDataStream, UserConsumerTV | ThirdParty |
| 277 | `twsGnp2X-aQ` | 83% | 71% | 77% | 100% | 62% | 77% | 7 | 7 | 5 | 8 | UserCompanyAnalyst, UserCompanyDataStream | UserCompanyInternalPlatform |
| 278 | `DrkaU99l9S8` | 73% | 80% | 76% | 54% | 54% | 54% | 11 | 12 | 13 | 13 | UserConsumerEdge, UserConsumerWeb | Greengrass, KinesisAnalytics, UserCompanyAnalyst |
| 279 | `8s0wGRkiDrw` | 75% | 75% | 75% | 29% | 50% | 36% | 8 | 5 | 7 | 4 | OpenSearch | ThirdParty |
| 280 | `Bi-1xjXvKgs` | 75% | 75% | 75% | 43% | 50% | 46% | 7 | 5 | 7 | 6 | UserConsumerWeb | UserConsumerWebMobile |
| 281 | `PoYiSKUy8sE` | 86% | 67% | 75% | 60% | 32% | 41% | 12 | 14 | 10 | 19 | Kinesis, UserConsumerAPI, UserConsumerEdge | KinesisDataStream |
| 282 | `QOtCpD23118` | 75% | 75% | 75% | 73% | 80% | 76% | 11 | 11 | 11 | 10 | ThirdParty, UserCompanyEdge | OnPremDC, UserConsumerIOT |
| 283 | `SC6n6J8Bi58` | 75% | 75% | 75% | 54% | 47% | 50% | 10 | 11 | 13 | 15 | UserConsumerDeveloper, UserConsumerIOT | NLB, UserCompanyAgent |
| 284 | `W5qVQr-n5M8` | 75% | 75% | 75% | 80% | 40% | 53% | 10 | 10 | 10 | 20 | ThirdParty, UserConsumerWeb | RDS, UserConsumerWebMobile |
| 285 | `aOY6YCpcjz8` | 75% | 75% | 75% | 91% | 71% | 80% | 11 | 11 | 11 | 14 | UserCompanyAPI | UserCompanyDeveloper |
| 286 | `7wBOFcP1HwA` | 70% | 78% | 74% | 40% | 40% | 40% | 11 | 10 | 10 | 10 | ELB, UserConsumerWeb | ALB, EC2, UserConsumerWebMobile |
| 287 | `LD5ksgnu8r8` | 78% | 70% | 74% | 67% | 46% | 55% | 11 | 11 | 9 | 13 | UserCompanyDataStream, UserConsumerAPI, UserConsumerWeb | ThirdParty, UserCompanyAgent |
| 288 | `hFx0EF9KEZU` | 70% | 78% | 74% | 77% | 43% | 56% | 15 | 15 | 13 | 23 | Firehose, UserConsumerWebMobile | Kinesis, UserCompanyAgent, UserConsumerMobile |
| 289 | `DAJZAygxDZA` | 80% | 67% | 73% | 22% | 13% | 17% | 9 | 8 | 9 | 15 | ThirdParty, UserCompanyAnalyst | StepFunctions |
| 290 | `FmhL2334GIY` | 80% | 67% | 73% | 40% | 36% | 38% | 10 | 10 | 10 | 11 | ECS, UserCompanyWebsite | ThirdParty |
| 291 | `OWLGK-eVrTw` | 80% | 67% | 73% | 17% | 6% | 9% | 7 | 6 | 6 | 16 | ThirdParty, UserConsumerAPI | EC2 |
| 292 | `tVjrkpjWG5o` | 80% | 67% | 73% | 14% | 12% | 13% | 8 | 7 | 7 | 8 | ThirdParty, UserConsumerAPI | UserCompanyAnalyst |
| 293 | `-kA0ahrhX3I` | 71% | 71% | 71% | 60% | 38% | 46% | 11 | 9 | 5 | 8 | ThirdParty, UserCompanyDeveloper | RDS, UserCompanyAnalyst |
| 294 | `2XVgpMwY5iE` | 71% | 71% | 71% | 56% | 42% | 48% | 8 | 7 | 9 | 12 | UserCompanyAgent, UserCompanyDataStream | UserCompanyDomainExpert, UserConsumerHospital |
| 295 | `KgRib8AM0fs` | 71% | 71% | 71% | 14% | 12% | 13% | 7 | 7 | 7 | 8 | UserConsumerEdge, UserConsumerWebMobile | AutoScaling, UserConsumerWeb |
| 296 | `MbkLJ62jtMc` | 62% | 83% | 71% | 43% | 75% | 55% | 8 | 6 | 7 | 4 | UserCompanyAPI | SES, UserConsumerMobile, UserConsumerWeb |
| 297 | `aOZ4H98XROc` | 83% | 62% | 71% | 17% | 11% | 13% | 8 | 8 | 6 | 9 | ApiGateway, ThirdParty, UserConsumerEdge | UserCompanyDeveloper |
| 298 | `mxKhbU_ToMs` | 71% | 71% | 71% | 50% | 31% | 38% | 8 | 9 | 8 | 13 | ThirdParty, UserConsumerWeb | ECS, UserConsumerWebMobile |
| 299 | `qgW8LQ8iBuA` | 71% | 71% | 71% | 67% | 50% | 57% | 10 | 10 | 3 | 4 | ThirdParty, UserCompanyAgent | OpenSearch, UserConsumerWeb |
| 300 | `acm-HWJhEOA` | 67% | 75% | 71% | 55% | 43% | 48% | 12 | 8 | 11 | 14 | UserCompanyAPI, UserCompanyDataStream | ApiGateway, ThirdParty, UserConsumerWeb |
| 301 | `c-1GXhOOOww` | 75% | 67% | 71% | 50% | 31% | 38% | 8 | 9 | 10 | 16 | ThirdParty, UserConsumerAPI, UserConsumerMobile | CloudFront, UserConsumerWebMobile |
| 302 | `gpWR5JBC64A` | 67% | 75% | 71% | 43% | 50% | 46% | 9 | 8 | 7 | 6 | Kinesis, UserConsumerMobile | Amplify, KinesisDataStream, UserConsumerWeb |
| 303 | `mmM_JnYygZM` | 67% | 75% | 71% | 40% | 14% | 21% | 10 | 10 | 5 | 14 | UserCompanyDataStream, UserConsumerWeb | CouchBase, MongoDBAtlas, UserCompanyAgent |
| 304 | `uNAmsoLed1E` | 75% | 67% | 71% | 57% | 27% | 36% | 10 | 10 | 7 | 15 | EC2, RDS, UserCompanyDataStream | OnPremDC, ThirdParty |
| 305 | `l3f29v3IJGA` | 60% | 86% | 71% | 18% | 13% | 15% | 10 | 9 | 11 | 15 | EC2 | EKS, SQS, ThirdParty (+1) |
| 306 | `BPvr0qWpJlA` | 64% | 78% | 70% | 27% | 33% | 30% | 12 | 10 | 11 | 9 | UserCompanyDataStream, UserConsumerMobile | EC2, SES, UserCompanyInternalPlatform (+1) |
| 307 | `SxFag4CMWU8` | 64% | 78% | 70% | 50% | 36% | 42% | 11 | 11 | 10 | 14 | ThirdParty, UserConsumerWeb | ELB, Glue, OnPremDC (+1) |
| 308 | `illMCyp4O9A` | 70% | 70% | 70% | 55% | 43% | 48% | 10 | 10 | 11 | 14 | ThirdParty, UserCompanyAPI, UserConsumerEdge | IoTCore, Lambda, UserConsumerIOT |
| 309 | `kszaIJEnKPk` | 70% | 70% | 70% | 62% | 38% | 48% | 11 | 11 | 8 | 13 | Kinesis, LambdaAtEdge, UserConsumerEdge | KinesisDataStream, ThirdParty, UserConsumerWeb |
| 310 | `WZ4YL4Z177Q` | 67% | 73% | 70% | 33% | 29% | 31% | 12 | 12 | 12 | 14 | RDS, UserConsumerAPI, UserConsumerWebMobile | MSK, MongoDBAtlas, UserConsumerMobile (+1) |
| 311 | `-S-R7MWRpaI` | 62% | 71% | 67% | 33% | 27% | 30% | 10 | 8 | 9 | 11 | Kinesis, UserConsumerMobile | KinesisDataStream, MongoDBAtlas, UserCompanyEdge |
| 312 | `-wLEkq21cvA` | 57% | 80% | 67% | 45% | 50% | 48% | 11 | 9 | 11 | 10 | UserCompanyAgent | AMI, OnPremDC, UserCompanyDeveloper |
| 313 | `3WgTBTDlQN8` | 67% | 67% | 67% | 56% | 36% | 43% | 9 | 9 | 9 | 14 | EC2, UserCompanyAPI, UserConsumerMobile | MongoDBAtlas, ThirdParty, UserConsumerWebMobile |
| 314 | `9-a9Y5THTYo` | 67% | 67% | 67% | 50% | 67% | 57% | 8 | 7 | 8 | 6 | SES, UserConsumerWeb | ThirdParty, UserCompanyDeveloper |
| 315 | `GxjMSvwcgvw` | 67% | 67% | 67% | 71% | 38% | 50% | 8 | 8 | 7 | 13 | UserCompanyAPI, UserConsumerAPI | OnPremDC, UserConsumerMobile |
| 316 | `Vrx9csoawWc` | 67% | 67% | 67% | 50% | 24% | 32% | 8 | 7 | 10 | 21 | ThirdParty, UserConsumerWeb | UserCompanyAnalyst, UserCompanyInternalPlatform |
| 317 | `XGVWdSnml6A` | 62% | 71% | 67% | 29% | 25% | 27% | 8 | 7 | 7 | 8 | UserConsumerAPI, UserConsumerEdge | EC2, UserCompanyDeveloper, UserCompanyEdge |
| 318 | `cmYI6axlicc` | 62% | 71% | 67% | 33% | 21% | 26% | 9 | 10 | 9 | 14 | MSK, UserCompanyDataStream | OnPremDC, ThirdParty, UserConsumerWeb |
| 319 | `sKksbPPDznM` | 67% | 67% | 67% | 33% | 25% | 29% | 6 | 6 | 6 | 8 | ShieldAdvanced, UserConsumerMobile | Shield, UserConsumerWebMobile |
| 320 | `tBavPTWewvI` | 67% | 67% | 67% | 29% | 22% | 25% | 6 | 6 | 7 | 9 | MSK, UserConsumerWebMobile | ThirdParty, UserConsumerMobile |
| 321 | `Dxq_U1TNx1s` | 60% | 67% | 63% | 55% | 35% | 43% | 11 | 11 | 11 | 17 | Aurora, UserConsumerMobile, UserConsumerSatellite | RDS, ThirdParty, UserCompanyAgent (+1) |
| 322 | `TTlyNWh0gjM` | 56% | 71% | 63% | 56% | 33% | 42% | 11 | 11 | 9 | 15 | UserConsumerAPI, UserConsumerWeb | CloudFront, ElastiCache, UserCompanyAnalyst (+1) |
| 323 | `M_hqigB9C4I` | 62% | 62% | 62% | 38% | 19% | 25% | 9 | 9 | 8 | 16 | ThirdParty, UserCompanyDataStream, UserConsumerWeb | EC2, UserCompanyAgent, UserConsumerHospital |
| 324 | `q_5U7z_vNug` | 62% | 62% | 62% | 55% | 40% | 46% | 8 | 8 | 11 | 15 | ThirdParty, UserCompanyAnalyst, UserConsumerEdge | RDS, UserCompanyEdge, UserConsumerWeb |
| 325 | `hMK2NJ-q9nc` | 57% | 67% | 62% | 18% | 40% | 25% | 10 | 6 | 11 | 5 | UserCompanyDataStream, UserCompanyEdge | AutoScaling, OnPremDC, UserConsumerSatellite |
| 326 | `i4ueYgjVDCw` | 54% | 70% | 61% | 0% | 0% | 0% | 13 | 10 | 7 | 8 | ALB, UserConsumerMobile, WAF | ApiGateway, AutoScaling, DirectConnect (+3) |
| 327 | `XqsgQxyZ2Tw` | 60% | 60% | 60% | 18% | 12% | 15% | 10 | 11 | 11 | 16 | ThirdParty, UserConsumerAPI | CouchBase, MSK |
| 328 | `wbh51O3QrE4` | 60% | 60% | 60% | 36% | 40% | 38% | 10 | 10 | 11 | 10 | ALB, Kinesis, UserConsumerEdge (+1) | ELB, KinesisDataStream, UserCompanyAgent (+1) |
| 329 | `8ZRWzn0G39g` | 62% | 56% | 59% | 33% | 8% | 13% | 10 | 12 | 9 | 38 | EC2, ECS, EKS (+1) | Lambda, ThirdParty, UserConsumerWeb |
| 330 | `KzJKdUZ3Ba4` | 50% | 67% | 57% | 25% | 17% | 20% | 7 | 4 | 4 | 6 | UserConsumerMobile | SAP, UserCompanyAgent |
| 331 | `lcLw-Le_tXQ` | 67% | 50% | 57% | 50% | 43% | 46% | 6 | 6 | 6 | 7 | EKS, UserConsumerAPI | UserConsumerWebMobile |
| 332 | `4-teOQ_dJvY` | 57% | 57% | 57% | 33% | 23% | 27% | 9 | 9 | 9 | 13 | Kinesis, UserCompanyAPI, UserCompanyEdge | KinesisDataStream, UserCompanyDataStream, UserCompanyInternalPlatform |
| 333 | `ilsJgwcAshE` | 60% | 50% | 55% | 50% | 56% | 53% | 10 | 9 | 10 | 9 | EKS, UserCompanyHeadEnd, UserConsumerCamera | OnPremDC, ThirdParty |
| 334 | `3yJZ6rPoZfg` | 50% | 50% | 50% | 25% | 22% | 24% | 8 | 7 | 8 | 9 | EC2, UserConsumerEdge, VPC | AutoScaling, UserConsumerWebMobile, VPCPeering |
| 335 | `cRxvZBIa-gI` | 33% | 40% | 36% | 0% | 0% | 0% | 7 | 5 | 4 | 4 | Aurora, ThirdParty, UserConsumerMobile | EC2, RDS, S3 (+1) |
| 336 | `wzGYJ6BB0iY` | 29% | 25% | 27% | 11% | 8% | 10% | 12 | 10 | 9 | 12 | ALB, ThirdParty, UserCompanyAPI (+3) | , DirectConnect, EC2 (+2) |


### Detailed Results Table: Excluded Validation (Invalid/Placeholder Ground Truths)

> [!NOTE]

> These graphs are excluded from the main average F1 calculations above.

| # | Video ID | Svc P | Svc R | Svc F1 | Edge P | Edge R | Edge F1 | Gen N | GT N | Gen E | GT E | Missing | Hallucinated |
|---|----------|-------|-------|--------|--------|--------|---------|-------|------|-------|------|---------|--------------|
| 1 | `E68ufJOduio` | 100% | 100% | 100% | 0% | 0% | 0% | 9 | 9 | 8 | 0 | — | — |
| 2 | `LPZlrX2cNjo` | 100% | 100% | 100% | 50% | 50% | 50% | 4 | 4 | 4 | 4 | — | — |
| 3 | `QnmmTIYZxNI` | 100% | 100% | 100% | 40% | 33% | 36% | 8 | 8 | 5 | 6 | — | — |
| 4 | `ZsabzCVjkIk` | 100% | 100% | 100% | 100% | 75% | 86% | 10 | 10 | 6 | 8 | — | — |
| 5 | `c8615P0yfi8` | 100% | 100% | 100% | 0% | 0% | 0% | 10 | 10 | 11 | 0 | — | — |
| 6 | `jzKCg9Z5_8Q` | 100% | 100% | 100% | 0% | 0% | 0% | 7 | 6 | 2 | 0 | — | — |
| 7 | `mT4KDGRgo4k` | 100% | 100% | 100% | 100% | 56% | 71% | 7 | 5 | 5 | 9 | — | — |
| 8 | `r3g1Nym-ebY` | 100% | 100% | 100% | 0% | 0% | 0% | 7 | 7 | 4 | 0 | — | — |
| 9 | `tTQ36qQF_vA` | 100% | 100% | 100% | 0% | 0% | 0% | 9 | 5 | 5 | 0 | — | — |
| 10 | `u5AT15mgbHk` | 100% | 100% | 100% | 0% | 0% | 0% | 6 | 6 | 2 | 0 | — | — |
| 11 | `uMX94Mn9u-4` | 100% | 100% | 100% | 0% | 0% | 0% | 10 | 10 | 0 | 10 | — | — |
| 12 | `zqiNLMmEeSo` | 100% | 100% | 100% | 0% | 0% | 0% | 11 | 10 | 0 | 0 | — | — |
| 13 | `vp2Ipv2_uCg` | 90% | 100% | 95% | 0% | 0% | 0% | 10 | 10 | 5 | 0 | — | UserConsumerWebMobile |
| 14 | `qv9q0sFt6aY` | 89% | 100% | 94% | 42% | 29% | 34% | 11 | 11 | 12 | 17 | — | OnPremDC |
| 15 | `YT21s0_ZJVQ` | 88% | 100% | 93% | 20% | 50% | 29% | 13 | 7 | 5 | 2 | — | EC2 |
| 16 | `1ZLiRT0C2Yo` | 86% | 100% | 92% | 0% | 0% | 0% | 7 | 6 | 6 | 0 | — | OnPremDC |
| 17 | `H51Ups01ZpU` | 86% | 100% | 92% | 0% | 0% | 0% | 7 | 6 | 6 | 0 | — | ThirdParty |
| 18 | `aAYvbRhZFPo` | 86% | 100% | 92% | 40% | 33% | 36% | 11 | 7 | 5 | 6 | — | ThirdParty |
| 19 | `1kWxymroGeE` | 83% | 100% | 91% | 36% | 100% | 53% | 8 | 5 | 11 | 4 | — | UserCompanyInternalPlatform |
| 20 | `b93-zn-DtBw` | 89% | 89% | 89% | 20% | 50% | 29% | 10 | 9 | 10 | 4 | SageMaker | ThirdParty |
| 21 | `U1kY6nSS2YQ` | 78% | 100% | 88% | 75% | 17% | 27% | 12 | 11 | 4 | 18 | — | CouchBase, UserConsumerWeb |
| 22 | `ameanoaMldM` | 78% | 100% | 88% | 12% | 50% | 20% | 9 | 7 | 8 | 2 | — | ACM, ServiceCatalog |
| 23 | `YjASp_VccmI` | 88% | 88% | 88% | 71% | 83% | 77% | 10 | 10 | 7 | 6 | UserConsumerWeb | UserConsumerWebMobile |
| 24 | `ihB2dRYLOOI` | 90% | 82% | 86% | 40% | 29% | 33% | 11 | 12 | 5 | 7 | UserCompanyDeveloper, UserConsumerAPI | UserConsumerWeb |
| 25 | `62E9ggjGS8I` | 83% | 83% | 83% | 50% | 22% | 31% | 7 | 7 | 4 | 9 | ThirdParty | ServiceNow |
| 26 | `8TExnSvZqt0` | 82% | 82% | 82% | 0% | 0% | 0% | 11 | 11 | 4 | 0 | AMI, AWSConfig | EC2, ThirdParty |
| 27 | `ruOhUEooJH0` | 82% | 82% | 82% | 100% | 83% | 91% | 11 | 11 | 5 | 6 | UserCompanyDataStream, UserConsumerDeveloper | OnPremDC, ThirdParty |
| 28 | `W96L6ICcF3s` | 80% | 80% | 80% | 0% | 0% | 0% | 7 | 7 | 3 | 0 | ECS | Fargate |
| 29 | `6sY0AunanlM` | 67% | 100% | 80% | 0% | 0% | 0% | 8 | 4 | 8 | 0 | — | ThirdParty, UserCompanyDeveloper |
| 30 | `OmVQ6pNDbaY` | 67% | 100% | 80% | 0% | 0% | 0% | 6 | 2 | 4 | 0 | — | ThirdParty |
| 31 | `9LhiUsg3knw` | 89% | 73% | 80% | 22% | 25% | 24% | 10 | 13 | 9 | 8 | UserCompanyDomainExpert, UserConsumerArtist, UserConsumerMobile | UserConsumerWebMobile |
| 32 | `JSBB-BCvavQ` | 62% | 100% | 77% | 0% | 0% | 0% | 10 | 5 | 11 | 0 | — | DMS, OnPremDC, Route53 |
| 33 | `1tGmQd0yOzE` | 75% | 75% | 75% | 40% | 17% | 24% | 5 | 8 | 5 | 12 | ThirdParty | UserConsumerWebMobile |
| 34 | `hEB1J9-iOqs` | 67% | 86% | 75% | 0% | 0% | 0% | 11 | 9 | 10 | 0 | UserCompanyAPI | SES, ServiceNow, UserCompanyDeveloper |
| 35 | `lA0lAgN0hTI` | 75% | 75% | 75% | 0% | 0% | 0% | 6 | 8 | 8 | 0 | UserConsumerWeb | UserConsumerWebMobile |
| 36 | `GoziWpmFCS0` | 60% | 100% | 75% | 18% | 100% | 31% | 9 | 4 | 11 | 2 | — | UserCompanyDataStream, UserCompanyDomainExpert |
| 37 | `Ujs9o3CXUTU` | 64% | 88% | 74% | 17% | 50% | 25% | 11 | 8 | 6 | 2 | DynamoDB | ALB, DocumentDB, Organizations (+1) |
| 38 | `fOgb0Es-lVs` | 67% | 80% | 73% | 62% | 83% | 71% | 8 | 7 | 8 | 6 | UserCompanyDataStream | KMS, ThirdParty |
| 39 | `i10a06IU4WQ` | 67% | 80% | 73% | 33% | 38% | 35% | 9 | 6 | 9 | 8 | UserCompanyAgent | IAM, UserCompanyDeveloper |
| 40 | `m8CBJEyHKIM` | 67% | 67% | 67% | 67% | 57% | 62% | 7 | 6 | 6 | 7 | NLB, UserConsumerMobile | ELB, UserConsumerWebMobile |
| 41 | `K5ww_O4vsxo` | 60% | 75% | 67% | 82% | 17% | 29% | 11 | 15 | 11 | 52 | ThirdParty | OnPremDC, S2SVPN |
| 42 | `QuyZHin9B70` | 60% | 75% | 67% | 0% | 0% | 0% | 8 | 4 | 7 | 0 | ThirdParty | OnPremDC, Outpost |
| 43 | `phN08pi3YzY` | 50% | 75% | 60% | 0% | 0% | 0% | 6 | 5 | 0 | 0 | ThirdParty | GuardDuty, KMS, SystemsManager |
| 44 | `X3mC6Yfd138` | 50% | 67% | 57% | 0% | 0% | 0% | 10 | 9 | 5 | 10 | EC2, UserCompanyDeveloper | AutoScaling, RDS, UserConsumerDeveloper (+1) |
| 45 | `99nNHsbwBpg` | 50% | 50% | 50% | 0% | 0% | 0% | 3 | 2 | 2 | 0 | EC2 | ThirdParty |
| 46 | `e3N5ZuHh7G0` | 50% | 50% | 50% | 0% | 0% | 0% | 6 | 6 | 5 | 6 | ECS, ThirdParty | EC2, UserConsumerWebMobile |
| 47 | `u9DZRkJxvWo` | 25% | 100% | 40% | 0% | 0% | 0% | 8 | 2 | 7 | 1 | — | Comprehend, Lambda, S3 (+3) |
| 48 | `zmJ7rL1iQBY` | 25% | 100% | 40% | 0% | 0% | 0% | 6 | 1 | 5 | 0 | — | DirectoryService, IAM, UserCompanyInternalPlatform |
| 49 | `BgT_bDAejSQ` | 17% | 100% | 29% | 0% | 0% | 0% | 9 | 2 | 0 | 1 | — | ALB, NAT, OnPremDC (+2) |



---
