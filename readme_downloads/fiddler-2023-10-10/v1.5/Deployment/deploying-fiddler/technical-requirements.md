---
title: "On-prem Technical Requirements"
slug: "technical-requirements"
hidden: false
createdAt: "2022-04-19T20:20:05.290Z"
updatedAt: "2023-01-31T17:21:08.432Z"
---
## System Architecture

Fiddler deploys into your private cloud's existing Kubernetes clusters, for which the minimum system requirements can be found [below](https://docs.fiddler.ai/docs/technical-requirements#minimum-system-requirements).  Fiddler supports deployment into Kubernetes in AWS, Azure, or GCP.  All services of the Fiddler platform are containerized in order to eliminate reliance on other cloud services and to reduce the deployment and maintenance friction of the platform.  This includes storage services like object storage and databases as well as system monitoring services like Grafana.  

Please see the system reference architecture below for more detail. \[click the image to enlarge].

![](https://files.readme.io/ecad416-Screenshot_2022-12-08_at_12.26.17_PM.png)

As depicted in the reference architecture above, updates to the Fiddler containers is accomplished through a shared container registry (that Fiddler is provided access to).  Updates to the containers are orchestrated using Helm charts.

Once the platform is running, end users can interface with the Fiddler platform using their browser, the [Fiddler Python client](https://docs.fiddler.ai/reference/about-the-fiddler-client), or Fiddler's RESTful APIs.

## Minimum System Requirements

Fiddler is horizontally scalable to support the throughput requirements for enormous production use-cases. The minimum system requirements below correspond to approximately 20 million inference events monitored per day (~230 EPS) for models with around 100 features, with 90 day retention.

- Kubernetes namespace
- **Compute**: 60 vCPU cores
- **Memory**: 120Gi
- **Persistent volumes**: 300 Gi 
  - POSIX-compliant block storage
  - 125 MB/s recommended
  - 3,000 IOPS recommended
- **DNS**: FQDN that resolves to an L4 or L7 load balancer/proxy that provides TLS termination