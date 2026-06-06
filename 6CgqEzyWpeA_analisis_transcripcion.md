# Análisis de Transcripción y Detección de Plantillas — Video 6CgqEzyWpeA (Sunday Sky)

Este documento detalla el análisis del video **6CgqEzyWpeA** (Sunday Sky - Rendering as a Service - RAS) y explica el comportamiento de la selección de plantillas y la ausencia de **CloudSearch** en los resultados.

---

## 🔍 ¿Por qué no se detectó o consideró CloudSearch?

El sistema de filtrado por plantilla basado en transcripción (`pizarra_template_matching_transcript.py`) optimiza el rendimiento y reduce los falsos positivos buscando únicamente los logotipos de los servicios de AWS que **fueron mencionados en el audio del video**.

### 1. Palabras clave configuradas para CloudSearch
En el código, el servicio `cloudsearch` tiene asignadas las siguientes palabras clave para su búsqueda en la transcripción:
```python
"cloudsearch": ["cloudsearch", "cloud search", "search"]
```

### 2. Análisis del audio de Whisper
Al analizar la transcripción completa del video (`data/raw/6CgqEzyWpeA_transcript.json`), se comprueba que **ninguna** de esas palabras clave aparece en el diálogo de los presentadores. 

Los presentadores explican la arquitectura de renderizado de Sunday Sky, detallando la interacción entre:
* API Gateway
* Lambda
* SQS
* Auto Scaling Group
* Spot Instances
* S3
* CloudFront
* CloudWatch
* Step Functions

Dado que no se menciona "cloudsearch", "cloud search" ni "search", el script **excluyó deliberadamente** la plantilla `cloudsearch.png` del proceso de emparejamiento.

### 3. Explicación del 11/11
El directorio `data/templates/` contiene un total de **12 plantillas** de iconos. 
Al descartar `cloudsearch` por no ser mencionado en el audio, el número total de plantillas cargadas para este video fue de **11**. 

En el fotograma ganador (`6CgqEzyWpeA_frame_0039.jpg`), el algoritmo detectó con éxito los 11 servicios restantes, logrando una puntuación perfecta de **11/11** (11 detectados de 11 buscados).

---

## 📋 Servicios de AWS Identificados y Detectados

A continuación se detallan los 11 servicios que sí fueron mencionados en el audio y detectados en la pizarra:

| Servicio | Palabras Clave Detectadas | Detecciones en Pizarra | Comentarios |
| :--- | :--- | :---: | :--- |
| **API Gateway** | "api gateway" | 1 | Canal de entrada para las peticiones de renderizado (RAS). |
| **Lambda** | "lambda" | **3** | Valida peticiones y coordina la cola SQS y el auto-escalado. |
| **SQS** | "sqs" | **3** | Colas de entrada y de respuesta rápida para trabajos de renderizado. |
| **Auto Scaling** | "auto scaling", "autoscaling" | 1 | Grupo de auto-escalado (ASG) que aloja los motores de renderizado. |
| **S3** | "s3", "bucket" | 1 | Almacena los segmentos de video renderizados. |
| **CloudFront** | "cloudfront" | 1 | Distribuye y entrega los segmentos de video personalizados. |
| **Spot Instance**| "spot instances", "sport" | 1 | Motores de renderizado que corren sobre instancias Spot para reducir costes. |
| **CloudWatch** | "cloudwatch" | 1 | Captura eventos de interrupción de instancias Spot y métricas. |
| **Step Functions**| "step function" | 1 | Orquesta la función Lambda que calcula la capacidad de escalado cada 15s. |
| **Phone** (Dispositivo) | "mobile device" | 1 | Dispositivo del usuario final que solicita y visualiza el video. |
| **Machine** (PC) | "pc device" | 1 | Ordenador/PC del usuario final. |

*Nota: Gracias a la nueva actualización con **Supresión de No Máximos (NMS)**, ahora se identifican correctamente las múltiples instancias físicas en el diagrama de la pizarra (como los 3 Lambdas y los 3 SQS).*

---

## 📝 Transcripción Completa del Video (Whisper)

A continuación se muestra el texto completo transcrito por Whisper para referencia:

```text
Welcome to This is My Architecture. I'm Orit. With me today, Shai from Sunday Sky. Hi Shai, tell us about Sunday Sky. Thanks for having me, Orit. So, Sunday Sky has been around since 2007. Our customers engage with their customers using video powered experiences in which the content of the video is personalized to the viewer. What are you going to talk about today? Today I'm going to talk about our rendering ecosystem, our rendering as a service, what we call RAS.

So, I imagine you get a telco bill every month. Yes, I do. And imagine that instead of getting a PDF with static data, you'll get a personalized video for Orit. So, let's say you're watching, you get a link to watch your monthly bill from your mobile device. That request arrives into our RAS ecosystem. First stop is the API Gateway, where we make use of the different capabilities of API gateway, which is a front link and we can configure usage plans and API keys for our customers to control the load on our farm.

That request arrives into a Lambda function, which is our service, RAS service frontend. That Lambda function does some validations on the rendering request and eventually, pushes rendering instruction to an SQS queue where we have engine service that are part of the RAS ecosystem pulling in for rendering jobs when they have capacity to do so.

Once a request arrives into the auto scaling group, then we want to have a quick response as possible from the rendering engine. So, we immediately respond to an SQS queue, which the same Lambda function invocation pulls from. And from that, a moment on, we have a link to a playlist file. That playlist file contains links to video segments that the rendering engine uploads to S3. So, when the player on the mobile device or PC device asks for this video segment to show, then the link to CloudFront actually pulls from the origin a video segment and plays it to the user.

So, your video rendering is basically based on, entirely on sport instances. How do you manage high availability? So, there's two aspects to maintain this high availability of our service. First one, we're creating instances across multiple availability zones. Second thing is we try to diversify the instance types inside the auto scaling group as much as possible. So, the combination of both spreading instances across multiple availability zones and have diversified instance types provides us with high availability even when using spot instances.

How do you handle the two-minute spot interruption notice while rendering video jobs? So, that's a great question. Well, we built a mechanism for spot instance interruptions where CloudWatch notifies a Lambda function via a CloudWatch event that a certain instance ID is about to be taken. That Lambda function interacts with that instance via an API call telling that instance specifically to stop pulling requests or rendering requests from the queue and kind of drain out the current jobs that it already renders. So, because our engine service is highly efficient, we have high certainty that the rendering job would finish before the two minutes timeout will exceed. So, once the API for instance to stop taking jobs from the queue is finished, we detach the instance from the auto scaling group.

Makes sense. What is the scale it currently rendering as a service support? So, we generate billions of videos yearly, millions of videos daily, in order to have highly available services. We have a scaling mechanism that we built that is reliant on CloudWatch metrics that are pushed from the rendering instances and consumed by Lambda function that is triggered by a step function every 15 seconds. So, when we calculate that we don't have or we expect higher traffic coming in, the Lambda function interacts with the auto scaling group telling it to increase the amount of instances that is currently in service.

Great. It looks like you build a highly available, cost efficient and scalable service. What are the next steps for you? So, we want to make use of a recent feature announced by AWS ASG where we can map specific instance types for specific weights. That way, our scaling mechanism can interact with the auto scaling group using weights, which is more suitable for representing rendering capacity that is currently required under the load of the farm. Thank you for sharing that with us. And thank you for watching. This is my architecture. It's my architecture.
```
