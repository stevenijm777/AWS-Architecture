# 🔬 Prompt Improvement Rules (Auto-Generated)

Generated from analysis of 56 usable video evaluations.

Overall Model Performance: Svc F1=75.7%, Edge F1=45.0%

## 🔴 Regla 1: Servicios Frecuentemente Omitidos

El modelo tiende a olvidar estos servicios. Agregar reglas explícitas al prompt.

| Servicio | Capability | Veces Omitido | Veces en GT | Miss Rate |
|----------|------------|---------------|-------------|-----------|
| UserConsumerWeb | User | 11 | 14 | 79% |
| UserCompanyDataStream | User | 9 | 10 | 90% |
| UserConsumerMobile | User | 8 | 12 | 67% |
| EC2 | compute | 5 | 20 | 25% |
| UserCompanyAnalyst | User | 5 | 6 | 83% |
| UserCompanyAgent | User | 5 | 8 | 62% |
| UserConsumerAPI | User | 4 | 4 | 100% |
| ThirdParty | ThirdParty | 4 | 24 | 17% |
| S3 | storage | 3 | 35 | 9% |
| ALB | networking | 3 | 7 | 43% |
| UserCompanyDeveloper | User | 3 | 8 | 38% |
| UserCompanyAPI | User | 3 | 3 | 100% |

## 🟡 Regla 2: Servicios Frecuentemente Alucinados

El modelo inventa estos servicios con frecuencia. Agregar restricciones al prompt.

| Servicio | Capability | Veces Alucinado | Acción Sugerida |
|----------|------------|-----------------|-----------------|
| ThirdParty | ThirdParty | 15 | No crear ThirdParty a menos que sea explícitamente on-prem |
| UserConsumerWebMobile | User | 13 | Clarificar cuándo usar cada tipo de User actor |
| UserConsumerWeb | User | 10 | Clarificar cuándo usar cada tipo de User actor |
| UserCompanyAgent | User | 8 | Clarificar cuándo usar cada tipo de User actor |
| UserCompanyAnalyst | User | 7 | Clarificar cuándo usar cada tipo de User actor |
| EC2 | compute | 5 | Verificar que el servicio aparezca como icono en la pizarra |
| UserCompanyDeveloper | User | 3 | Clarificar cuándo usar cada tipo de User actor |
| UserCompanyAPI | User | 3 | Clarificar cuándo usar cada tipo de User actor |
| Lambda | compute | 3 | Verificar que el servicio aparezca como icono en la pizarra |
| ApiGateway | networking | 3 | Verificar que el servicio aparezca como icono en la pizarra |

## 👤 Regla 3: Normalización de User Actors

El modelo tiene problemas significativos con la clasificación de actores/usuarios.

**Problema principal:** Confusión entre tipos de User (Web vs Mobile vs WebMobile vs API).

**Acciones sugeridas:**

- El modelo pone **UserConsumerWebMobile** cuando debería ser **UserConsumerWeb** (6 veces)
- El modelo pone **UserConsumerWebMobile** cuando debería ser **UserConsumerMobile** (4 veces)
- El modelo pone **UserConsumerWeb** cuando debería ser **UserCompanyDeveloper** (3 veces)
- El modelo pone **UserCompanyAgent** cuando debería ser **UserConsumerWeb** (3 veces)
- El modelo pone **UserCompanyAnalyst** cuando debería ser **UserConsumerMobile** (3 veces)
- El modelo pone **UserConsumerWeb** cuando debería ser **UserCompanyAnalyst** (2 veces)
- El modelo pone **UserConsumerHospital** cuando debería ser **UserCompanyDataStream** (2 veces)
- El modelo pone **UserCompanyAnalyst** cuando debería ser **UserConsumerWeb** (2 veces)
- El modelo pone **UserConsumerWeb** cuando debería ser **UserCompanyAgent** (1 veces)
- El modelo pone **UserConsumerMobile** cuando debería ser **UserCompanyDataStream** (1 veces)

## 🔗 Regla 4: Aristas Problemáticas

**Aristas que el modelo olvida con frecuencia:**

- `DynamoDB→Lambda` (omitida 7 veces)
- `S3→EC2` (omitida 6 veces)
- `CloudFront→UserConsumerWeb` (omitida 5 veces)
- `EC2→S3` (omitida 5 veces)
- `Lambda→S3` (omitida 5 veces)
- `EC2→ThirdParty` (omitida 4 veces)
- `S3→Athena` (omitida 4 veces)
- `UserCompanyAgent→ThirdParty` (omitida 4 veces)
- `UserConsumerWeb→CloudFront` (omitida 4 veces)
- `S3→CloudFront` (omitida 4 veces)

**Aristas que el modelo inventa con frecuencia:**

- `ThirdParty→ThirdParty` (alucinada 24 veces)
- `ThirdParty→S3` (alucinada 6 veces)
- `Lambda→ThirdParty` (alucinada 6 veces)
- `UserConsumerWebMobile→CloudFront` (alucinada 5 veces)
- `CloudFront→UserConsumerWebMobile` (alucinada 5 veces)
- `UserConsumerWeb→CloudFront` (alucinada 5 veces)
- `ThirdParty→Lambda` (alucinada 5 veces)
- `EC2→CloudWatch` (alucinada 5 veces)
- `EC2→RDS` (alucinada 5 veces)
- `ThirdParty→DynamoDB` (alucinada 4 veces)

## 📉 Regla 5: Capabilities con Peor Rendimiento

- **OnPremDC**: Recall=0%, 
  1 de 1 omitidos, 2 alucinados
- **User**: Recall=24%, 
  57 de 75 omitidos, 56 alucinados

## 📊 Regla 6: Balance de Conteo de Nodos

**OK:** Ratio promedio gen/gt = 1.17x (dentro del rango aceptable).
