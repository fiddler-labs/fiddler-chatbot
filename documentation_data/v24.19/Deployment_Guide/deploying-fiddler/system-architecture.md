---
title: System Architecture
slug: system-architecture
excerpt: ''
createdAt: Tue Apr 19 2022 20:19:53 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 15 2024 21:49:11 GMT+0000 (Coordinated Universal Time)
---

# System Architecture

Fiddler deploys into your private cloud's existing Kubernetes clusters, for which the minimum system requirements can be found [here](technical-requirements.md). Fiddler supports AWS, Azure, or GCP managed Kubernetes services.

Updates to the Fiddler containers is accomplished through a shared container registry (that Fiddler is provided access to). Updates to the containers are orchestrated using Helm charts.

A full-stack deployment of Fiddler is shown in the diagram below.

![Fiddler system architecture](../../.gitbook/assets/fiddler\_system\_architecture\_diagram.png)

The Fiddler system components are deployed within a single namespace on a Kubernetes cluster, using the official Fiddler Helm chart.

* Fiddler core infrastructure relies on persistent volumes provided within the Kubernetes cluster. We recommend using encrypted storage volumes.
* Fiddler may be configured to utilize external infrastructure in a self-hosted environment, such as existing PostgresQL servers, but this is not required as all services are containerized by default.
* Full-stack "any-prem" Fiddler includes observability infrastructure to monitor Fiddler system health and performance. These mainstream observability components may be integrated with external observability systems to support administration in a self-hosted environment.
* HTTP traffic to the Fiddler system is handled by an L4 or L7 load balancer or other proxy. TLS termination should usually occur outside the Fiddler system.

Once the platform is running, end users can interface with the Fiddler platform using their browser, the [Fiddler Python client](../../Python\_Client\_3-x/about-client-3x.md), or Fiddler's RESTful APIs.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

