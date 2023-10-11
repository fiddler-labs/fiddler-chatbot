---
title: "On-prem Technical Requirements"
slug: "technical-requirements"
hidden: false
createdAt: "2022-04-19T20:20:05.290Z"
updatedAt: "2022-06-01T17:53:04.403Z"
---
[block:api-header]
{
  "title": "System Requirements"
}
[/block]
The requirements and installation steps for deploying Fiddler’s scalable centralized platform architecture using different cloud services provider are described below.

## Fiddler Platform
Fiddler System requirements for scalable Centralized platform Architecture

- Deployment: Managed k8s 
- Compute: 8 cores, 32GB memory per instance (Recommended m5.2xlarge or equivalent)
- Minimum 2 instances (for product services)
- Database: DB storage (Assuming total dataset size < 100GB)
- Persistent volume: 3 blocks (rabbitmq - 32GB, postgres - 256GB) 
- Shared Storage: S3 or compatible Object Store - min 128GB (depends on data and type of models) 
- Container Registry: Quay or ECR
- Ingress Controller: Envoy-proxy/ingress-nginx
- DNS/IP address: Need to set up an IP address and direct to m/c where Fiddler is running
- Logs: Accessibility to application logs


## Software Packages

- Python3 (RHEL) 
- NodeJS
- ReactJS


## Services
Depending on the cloud service provider, the following services are needed to deploy Fiddler

| **Data Center**                      | **AWS**                      | **Azure Cloud**            | **GCP**                  |
|--------------------------------------|------------------------------|----------------------------|--------------------------|
| Load Balanacer                       | Elastic Load Balancer        | Azure Load Balancer        | Cloud Load Balancer      |
| VM Server                            | Elastic Cloud Compute        | Azure Virtual Machine      | Compute Engine           |
| Managed K8s ~(Openshift~ ~Vanilla~ ~K8s)~| Elastic Kubernetes Service  | Azure Kubernetes Service   | Google Kubernetes Engine |
| Persistent Volume/NFS                | Elastic Block Storage        | Managed Disk               | Persistent Disk          |
| Object Store ~(S3~ ~HS3~ ~MinIO)~    | S3                           | Blob Storage               | Cloud Storage            |
| Postgresql ~(Enterprise-grade)~      | RDS Postgresql               | Postgresql                 | Cloud SQL                |
| DNS                                  | Route 53                     | Azure DNS                  | Cloud DNS                |