---
title: "System Architecture"
slug: "system-architecture"
hidden: false
createdAt: "2022-04-19T20:19:53.311Z"
updatedAt: "2023-10-19T20:59:24.638Z"
---
Fiddler deploys into your private cloud's existing Kubernetes clusters, for which the minimum system requirements can be found [here](doc:technical-requirements).  Fiddler supports deployment into Kubernetes in AWS, Azure, or GCP.  All services of the Fiddler platform are containerized in order to eliminate reliance on other cloud services and to reduce the deployment and maintenance friction of the platform.  This includes storage services like object storage and databases as well as system monitoring services like Grafana.  

Updates to the Fiddler containers is accomplished through a shared container registry (that Fiddler is provided access to).  Updates to the containers are orchestrated using Helm charts.

A full-stack deployment of Fiddler is shown in the diagram below. 

![](https://files.readme.io/7cbfe31-reference_architecture.png)

The Fiddler system components are deployed within a single namespace on a Kubernetes cluster, using the official Fiddler Helm chart.

- Fiddler core infrastructure relies on persistent volumes provided within the Kubernetes cluster. We recommend using encrypted storage volumes wherever possible.
- Fiddler may be configured to utilize external infrastructure in a self-hosted environment, such as existing PostgresQL servers, but this is not required as all services are containerized by default.
- Full-stack "any-prem" Fiddler includes observability infrastructure to monitor Fiddler system health and performance. These mainstream observability components may be integrated with external observability systems to support administration in a self-hosted environment.
- HTTP traffic to the Fiddler system is handled by an L4 or L7 load balancer or other proxy. TLS termination should usually occur outside the Fiddler system.

Once the platform is running, end users can interface with the Fiddler platform using their browser, the [Fiddler Python client](ref:about-the-fiddler-client), or Fiddler's RESTful APIs.