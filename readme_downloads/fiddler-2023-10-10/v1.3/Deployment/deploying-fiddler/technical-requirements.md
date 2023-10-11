---
title: "On-prem Technical Requirements"
slug: "technical-requirements"
hidden: false
createdAt: "2022-04-19T20:20:05.290Z"
updatedAt: "2022-08-08T16:58:40.548Z"
---
Minimum System Requirements
---------------------------

Fiddler is horizontally scalable to support the throughput requirements for enormous production use-cases. The minimum system requirements below correspond to approximately 20 million inference events monitored per day (~230 EPS) for models with around 100 features, with 90 day retention.

- Kubernetes namespace
- **Compute**: 60 vCPU cores
- **Memory**: 120Gi
- **Persistent volumes**: 300 Gi 
  - POSIX-compliant block storage
  - 125 MB/s recommended
  - 3,000 IOPS recommended
- **DNS**: FQDN that resolves to an L4 or L7 loadbalancer/proxy that provides TLS termination