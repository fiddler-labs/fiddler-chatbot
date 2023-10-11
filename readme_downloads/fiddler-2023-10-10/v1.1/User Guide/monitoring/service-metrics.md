---
title: "Service Metrics"
slug: "service-metrics"
hidden: false
createdAt: "2022-04-19T20:25:31.308Z"
updatedAt: "2022-05-10T16:12:39.477Z"
---
This tool gives you basic insights into the operational health of your ML service in production.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c47e26c-Monitor_Service.png",
        "Monitor_Service.png",
        3222,
        1506,
        "#fdfdfe"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "What is being tracked?"
}
[/block]
* ***Traffic*** — The volume of traffic received by the model over time.
* ***Latency*** —  The average latency of the model, i.e. the time it takes to respond to prediction requests (in milliseconds).
* ***Errors*** —  The number of errors the model has made in its predictions.
[block:api-header]
{
  "title": "Why is it being tracked?"
}
[/block]
* These are basic high-level metrics that inform us of the overall system health.
[block:api-header]
{
  "title": "What steps should I take when I see an outlier?"
}
[/block]
* A dip or spike in traffic needs to be investigated. For example, a dip could be due to a production model server going down; a spike could be an adversarial attack.
* An increase in model latency also needs to be investigated. It could be an indicator of requests building up due to high QPS.
* An increase in error counts could, for example, point to data pipeline issues.

**Reference**

* See our article on [*The Rise of MLOps Monitoring*](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*