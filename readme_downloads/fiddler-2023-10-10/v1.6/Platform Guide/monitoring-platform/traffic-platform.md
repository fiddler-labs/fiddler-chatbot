---
title: "Traffic"
slug: "traffic-platform"
excerpt: "Platform Guide"
hidden: false
createdAt: "2022-12-19T19:28:11.378Z"
updatedAt: "2023-02-02T00:06:59.679Z"
---
Traffic as a service metric gives you basic insights into the operational health of your ML service in production.

![](https://files.readme.io/d2c1eaa-Screenshot_2023-02-01_at_5.13.34_PM.png)

## What is being tracked?

- **_Traffic_** — The volume of traffic received by the model over time.

## Why is it being tracked?

- Traffic is a basic high-level metric that informs us of the overall system's health.

## What steps should I take when I see an outlier?

- A dip or spike in traffic needs to be investigated. For example, a dip could be due to a production model server going down; a spike could be an adversarial attack.

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_