---
title: "System Architecture"
slug: "system-architecture"
hidden: false
createdAt: "2022-04-19T20:19:53.311Z"
updatedAt: "2022-08-08T13:55:22.386Z"
---
System Architecture
-------------------

The Fiddler system architecture is designed to fit seamlessly into most Kubernetes-based environments, with minimal external dependencies. 

A full-stack deployment of Fiddler is shown in the diagram below. Fiddler platform applications and infrastructure are shown in blue and orange, respectively. External systems are shown in lavender.

![](https://files.readme.io/cad1a8e-image.png)

- The Fiddler system components are deployed within a single namespace on a Kubernetes cluster, typically using the official Fiddler Helm chart.
  - Fiddler core infrastructure relies on persistent volumes provided within the Kubernetes cluster. We recommend using encrypted storage volumes wherever possible.
  - Fiddler may be configured to utilize external infrastructure in a self-hosted environment, such as existing PostgresQL servers.
- Full-stack "any-prem" Fiddler includes observability infrastructure to monitor Fiddler system health and performance. These mainstream observability components may be integrated with external observability systems to support administration in a self-hosted environment.
- HTTP traffic to the Fiddler system is handled by an L4 or L7 load balancer or other proxy. TLS termination should usually occur outside the Fiddler system.