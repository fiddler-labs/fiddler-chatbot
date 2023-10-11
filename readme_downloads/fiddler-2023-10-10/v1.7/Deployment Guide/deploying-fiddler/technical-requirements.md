---
title: "On-prem Technical Requirements"
slug: "technical-requirements"
hidden: false
createdAt: "2022-04-19T20:20:05.290Z"
updatedAt: "2023-05-18T20:17:38.550Z"
---
## Minimum System Requirements

Fiddler is horizontally scalable to support the throughput requirements for enormous production use-cases. The minimum system requirements below correspond to approximately 20 million inference events monitored per day (~230 EPS) for models with around 100 features, with 90 day retention.

- Kubernetes namespace
- **Compute**: 96 vCPU cores
- **Memory**: 384Gi
- **Persistent volumes**: 500 Gi storage across 10 volumes 
  - POSIX-compliant block storage
  - 125 MB/s recommended
  - 3,000 IOPS recommended
- **Ingress Controller**: Ingress-nginx or AWS/GCP/Azure Load Balancer Controller
- **DNS**: FQDN that resolves to an L4 or L7 load balancer/proxy that provides TLS termination

## Kubernetes Cluster Requirements

As stated above, Fiddler requires a Kubernetes cluster to install into.  The following outlines the requirements for this K8 cluster:

- **Node Groups**:  2 node groups -  1 for core Fiddler services, 1 for Clickhouse (Fiddler's event database)
- **Resources**:
  - Fiddler :  48 vCPUs, 192 Gi
  - Clickhouse :  64 vCPUs, 256 Gi [tagged & tainted]
- **Persistent Volumes**: 500 GB (minimum) /  1 TB (recommended)
- **Instance Sizes**

  | Instance Size | AWS    | Azure      | GCP        |
  | :------------ | :----- | :--------- | :--------- |
  | Minimum       | m5.4xl | Std_D16_v3 | c2d_std_16 |
  | Recommended   | m5.8xl | Std_D32_v3 | c2d_std_32 |