---
title: "Monitoring"
slug: "monitoring-platform"
hidden: false
createdAt: "2022-11-15T18:06:49.755Z"
updatedAt: "2023-02-14T01:15:59.411Z"
---
Fiddler Monitoring helps you identify issues with the performance of your ML models after deployment. Fiddler Monitoring has five main features:

1. **Data Drift**
2. **Performance**
3. **Data Integrity**
4. **Service Metrics**
5. **Alerts**

## Integrate with Fiddler Monitoring

Integrating Fiddler monitoring is a four-step process:

1. **Upload dataset**

   Fiddler needs a dataset to be used as a baseline for monitoring. A dataset can be uploaded to Fiddler using our UI and Python package. For more information, see:

   - [client.upload_dataset()](ref:clientupload_dataset) 

2. **Onboard model**

   Fiddler needs some specifications about your model in order to help you troubleshoot production issues. Fiddler supports a wide variety of model formats. For more information, see:

   - [client.add_model()](ref:clientadd_model) 

3. **Configure monitoring for this model**

   You will need to configure bins and alerts for your model. These will be discussed in detail below.

4. **Send traffic from your live deployed model to Fiddler**

   Use the Fiddler SDK to send us traffic from your live deployed model.

## Publish events to Fiddler

In order to send traffic to Fiddler, use the [`publish_event`](ref:clientpublish_event) API from the Fiddler SDK.

The `publish_event` API can be called in real-time right after your model inference. 

An event can contain the following:

- Inputs
- Outputs
- Target
- Decisions (categorical only)
- Metadata

These aspects of an event can be monitored on the platform.

> 📘 Info
> 
> You can also publish events as part of a batch call after the fact using the `publish_events_batch` API (click [here](ref:clientpublish_events_batch) for more information). In this case, you will need to send Fiddler the original event timestamps as to accurately populate the time series charts.

## Updating events

Fiddler supports [partial updates of events](doc:updating-events) for your **target** column. This can be useful when you don’t have access to the ground truth for your model at the time the model's prediction is made. Other columns can only be sent at insertion time (with `update_event=False`).

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/trial?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/af83f1a-fiddler-docs-cta-trial.png\" alt=\"Fiddler Free Trial\"></a>\n</div>"
}
[/block]