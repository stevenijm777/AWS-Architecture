#!/usr/bin/env python3
"""
construir_datos.py — Congela los datos que C1 y C2 usan, y verifica que no tocan el panel.

  datos/alias.json      diccionario de alias de C1 (texto → servicio del catálogo)
  datos/reglas_c2.json  reglas de convención de C2

Las dos salen de reports/reglas_convencion/particion.json (semilla 42):
  - alias: grafos de inducción + validación. Ninguno es del panel.
  - reglas: estimadas SOLO en inducción con `estimar` de la fase 1a; se quedan las familias
    que mejoraron en validación (actor +0,90, ida y vuelta +0,24). `invertir` empeoró en
    validación (−0,46) y queda fuera.

Cada archivo guarda los ids que usó, y `verificar()` comprueba de nuevo, al cargarlos, que
ninguno está en PANEL_30. Sin API.

    .venv/Scripts/python -m multiagent.construir_datos
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts" / "reglas"))

import networkx as nx  # noqa: E402

from scripts.ablation.rerun_panel import PANEL_30  # noqa: E402

DATOS = Path(__file__).resolve().parent / "datos"
PARTICION = ROOT / "reports" / "reglas_convencion" / "particion.json"
GT_DIR = ROOT / "data" / "cloudscape_gt"
SERVICES_CSV = GT_DIR / "services.csv"

# Nombres oficiales y abreviaturas de AWS que no se deducen del nombre corto del catálogo.
# Escritos a mano desde la nomenclatura pública de AWS, no desde grafos.
ALIAS_MANUALES = {
    "simple storage service": "S3", "s3 bucket": "S3", "bucket": "S3",
    "simple queue service": "SQS", "simple notification service": "SNS",
    "simple email service": "SES", "elastic compute cloud": "EC2", "ec2 instance": "EC2",
    "spot instance": "EC2", "virtual machine": "EC2",
    "relational database service": "RDS", "postgres": "RDS", "postgresql": "RDS", "mysql": "RDS",
    "aurora postgresql": "Aurora", "aurora mysql": "Aurora", "aurora serverless": "Aurora",
    "dynamo": "DynamoDB", "dynamodb streams": "DynamoDBStream", "dynamo stream": "DynamoDBStream",
    "kinesis data streams": "KinesisDataStream", "kinesis stream": "KinesisDataStream",
    "kinesis data firehose": "Firehose", "kinesis firehose": "Firehose",
    "data firehose": "Firehose", "kinesis data analytics": "KinesisAnalytics",
    "kinesis video streams": "KinesisVideo", "managed streaming for apache kafka": "MSK",
    "managed streaming for kafka": "MSK", "elastic container service": "ECS",
    "elastic kubernetes service": "EKS", "kubernetes": "EKS", "elastic container registry": "ECR",
    "application load balancer": "ALB", "network load balancer": "NLB",
    "elastic load balancer": "ELB", "elastic load balancing": "ELB", "load balancer": "ELB",
    "api gateway": "ApiGateway", "step functions": "StepFunctions", "state machine": "StepFunctions",
    "lambda function": "Lambda", "lambda functions": "Lambda", "lambda edge": "LambdaAtEdge",
    "lambda at edge": "LambdaAtEdge", "elastic beanstalk": "BeanStalk", "beanstalk": "BeanStalk",
    "elastic file system": "EFS", "elastic block store": "EBS", "elastic mapreduce": "EMR",
    "elasticsearch": "OpenSearch", "elasticsearch service": "OpenSearch",
    "opensearch service": "OpenSearch", "redshift": "RedShift", "redis": "ElastiCache",
    "memcached": "ElastiCache", "elasticache redis": "ElastiCache",
    "database migration service": "DMS", "key management service": "KMS",
    "identity and access management": "IAM", "security token service": "STS",
    "certificate manager": "ACM", "web application firewall": "WAF", "route 53": "Route53",
    "virtual private cloud": "VPC", "transit gateway": "TransitGateway",
    "direct connect": "DirectConnect", "site to site vpn": "S2SVPN", "vpn": "VPN",
    "nat gateway": "NAT", "x ray": "XRay", "xray": "XRay", "event bridge": "EventBridge",
    "cloudwatch events": "EventBridge", "cloudwatch logs": "CloudWatch",
    "cloud watch": "CloudWatch", "cloud front": "CloudFront", "cloud formation": "CloudFormation",
    "cloud trail": "CloudTrail", "systems manager": "SystemsManager", "ssm": "SystemsManager",
    "secrets manager": "SecretsManager", "parameter store": "SystemsManager",
    "iot core": "IoTCore", "iot": "IoTCore", "iot analytics": "IoTAnalytics",
    "iot greengrass": "Greengrass", "sagemaker ground truth": "SageMakerGroundTruth",
    "machine learning": "AmazonML", "mq": "AmazonMQ", "amazon mq": "AmazonMQ",
    "elemental medialive": "MediaLive", "elemental mediaconvert": "MediaConvert",
    "elemental mediapackage": "MediaPackage", "elemental mediastore": "MediaStore",
    "elemental mediaconnect": "MediaConnect", "transfer family": "TransferFamily",
    "sftp": "TransferFamily", "storage gateway": "StorageGateway", "fsx": "FSX",
    "on premises": "OnPremDC", "on prem": "OnPremDC", "on premise": "OnPremDC",
    "data center": "OnPremDC", "datacenter": "OnPremDC", "corporate data center": "OnPremDC",
    "auto scaling": "AutoScaling", "autoscaling group": "AutoScaling", "asg": "AutoScaling",
    "code pipeline": "CodePipeline", "code build": "CodeBuild", "code commit": "CodeCommit",
    "code deploy": "CodeDeploy", "lake formation": "LakeFormation", "quick sight": "QuickSight",
    "app sync": "AppSync", "graphql": "AppSync", "cognito user pool": "Cognito",
    "documentdb": "DocumentDB", "document db": "DocumentDB", "mongodb atlas": "MongoDBAtlas",
    "service now": "ServiceNow", "workspaces": "WorkSpaces", "global accelerator": "GlobalAccelerator",
    "shield advanced": "ShieldAdvanced", "security hub": "SecurityHub", "guard duty": "GuardDuty",
    "control tower": "ControlTower", "outposts": "Outpost", "batch": "Batch", "fargate": "Fargate",
}


def ids_particion() -> dict[str, list[str]]:
    p = json.loads(PARTICION.read_text(encoding="utf-8"))
    return {"induccion": p["induccion"], "validacion": p["validacion"]}


def verificar(ids: list[str], que: str) -> None:
    """Corta si algún grafo del panel de 30 entró en la construcción de `que`."""
    cruce = sorted(set(ids) & set(PANEL_30))
    if cruce:
        raise RuntimeError(f"{que} usa {len(cruce)} grafos del panel: {cruce[:5]}")


def limpiar(texto: str) -> str:
    """Forma comparable: minúsculas, sin 'amazon'/'aws' al inicio, sin signos."""
    t = re.sub(r"([a-z])([A-Z])", r"\1 \2", texto)            # CamelCase → palabras
    t = t.lower().replace("&", " and ")
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    t = re.sub(r"^(amazon|aws)\s+", "", t)
    return t


def construir_alias(ids: list[str]) -> dict:
    verificar(ids, "alias")
    catalogo = []
    with open(SERVICES_CSV, encoding="utf-8") as fh:
        for linea in fh.readlines()[1:]:
            nombre = linea.split(",")[0].strip()
            if nombre:
                catalogo.append(nombre)
    alias: dict[str, str] = {}
    origen: dict[str, str] = {}
    for nombre in catalogo:
        if nombre.startswith("User"):
            continue                       # el subtipo de actor lo decide A3 con el catálogo
        for forma in {limpiar(nombre), nombre.lower()}:
            alias[forma.replace(" ", "")] = nombre
            origen[forma.replace(" ", "")] = "catalogo"
    for texto, servicio in ALIAS_MANUALES.items():
        assert servicio in catalogo, servicio
        clave = limpiar(texto).replace(" ", "")
        alias.setdefault(clave, servicio)
        origen.setdefault(clave, "manual")
    # Nombres escritos en el GT para nodos ThirdParty (Kafka, Salesforce, SAP…): la convención
    # de Cloudscape es anotarlos como ThirdParty con su nombre. Solo los que el catálogo no cubre.
    gt = Counter()
    for vid in ids:
        G = nx.read_graphml(GT_DIR / f"{vid}.graphml")
        for _, d in G.nodes(data=True):
            if d.get("name") and d.get("service") == "ThirdParty":
                gt[limpiar(d["name"]).replace(" ", "")] += 1
    for clave, n in gt.items():
        if clave and clave not in alias and not clave.startswith("user"):
            alias[clave] = "ThirdParty"
            origen[clave] = f"gt×{n}"
    return {"construido_con": sorted(ids), "n_grafos": len(ids), "alias": alias, "origen": origen}


def construir_reglas(induccion: list[str], validacion: list[str]) -> dict:
    verificar(induccion, "reglas (inducción)")
    verificar(validacion, "reglas (validación)")
    from fase1a_huella_y_reglas import UMBRAL, SOPORTE, estimar, leer, pares  # noqa: E402

    r = estimar(induccion)
    # Pares cerca del umbral: C2 no los decide y se los pasa a A4 como casos ambiguos.
    dire = defaultdict(Counter)
    for vid in induccion:
        d = set(pares(leer(GT_DIR / f"{vid}.graphml")))
        for a, b in {tuple(sorted(p)) for p in d if p[0] != p[1]}:
            dire[(a, b)]["ambas" if (a, b) in d and (b, a) in d else "uno"] += 1
    dudosos = {f"{a}|{b}": round(c["ambas"] / sum(c.values()), 2)
               for (a, b), c in dire.items()
               if sum(c.values()) >= SOPORTE and 0.5 <= c["ambas"] / sum(c.values()) < UMBRAL}
    validacion_f1 = json.loads((ROOT / "reports" / "reglas_convencion" / "fase1a_resumen.json")
                               .read_text(encoding="utf-8"))["edge_f1_validacion"]
    return {
        "estimado_con": sorted(induccion), "seleccionado_con": sorted(validacion),
        "soporte_minimo": SOPORTE, "umbral": UMBRAL,
        "edge_f1_validacion": validacion_f1,
        "reglas": {
            "actor_subtipo": r["actor"],
            "ida_y_vuelta": sorted(f"{a}|{b}" for a, b in r["ambas"]),
        },
        "descartadas": {"invertir": {"pares": len(r["invertir"]),
                                     "motivo": "empeora en validación (58,10 → 57,64)"}},
        "dudosos_para_a4": dudosos,
    }


def main() -> None:
    p = ids_particion()
    DATOS.mkdir(exist_ok=True)
    alias = construir_alias(p["induccion"] + p["validacion"])
    (DATOS / "alias.json").write_text(json.dumps(alias, indent=1, ensure_ascii=False), encoding="utf-8")
    reglas = construir_reglas(p["induccion"], p["validacion"])
    (DATOS / "reglas_c2.json").write_text(json.dumps(reglas, indent=1, ensure_ascii=False),
                                          encoding="utf-8")
    print(f"alias: {len(alias['alias'])} claves de {alias['n_grafos']} grafos fuera del panel")
    print(f"reglas: {len(reglas['reglas']['ida_y_vuelta'])} pares ida y vuelta, "
          f"{len(reglas['reglas']['actor_subtipo'])} de actor, "
          f"{len(reglas['dudosos_para_a4'])} dudosos para A4")
    print("verificado: ningún grafo de PANEL_30 entra en alias ni reglas")


if __name__ == "__main__":
    main()
