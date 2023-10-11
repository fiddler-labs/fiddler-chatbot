---
title: "Service Metrics"
slug: "service-metrics"
hidden: false
createdAt: "2022-04-19T20:25:31.308Z"
updatedAt: "2022-09-14T20:00:18.638Z"
---
This tool gives you basic insights into the operational health of your ML service in production.

![](https://files.readme.io/c47e26c-Monitor_Service.png "Monitor_Service.png")



## What is being tracked?

- **_Traffic_** — The volume of traffic received by the model over time.
- **_Latency_** —  The average latency of the model, i.e. the time it takes to respond to prediction requests (in milliseconds).
- **_Errors_** —  The number of errors the model has made in its predictions.

## Why is it being tracked?

- These are basic high-level metrics that inform us of the overall system health.

## What steps should I take when I see an outlier?

- A dip or spike in traffic needs to be investigated. For example, a dip could be due to a production model server going down; a spike could be an adversarial attack.
- An increase in model latency also needs to be investigated. It could be an indicator of requests building up due to high QPS.
- An increase in error counts could, for example, point to data pipeline issues.

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_