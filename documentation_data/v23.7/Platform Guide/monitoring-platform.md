---
title: "Monitoring"
slug: "monitoring-platform"
excerpt: ""
hidden: false
createdAt: "Tue Nov 15 2022 18:06:49 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:34:55 GMT+0000 (Coordinated Universal Time)"
---
Fiddler Monitoring helps you identify issues with the performance of your ML models after deployment. Fiddler Monitoring has five Metric Types which can be monitored and alerted on:

1. **Data Drift**
2. **Performance**
3. **Data Integrity**
4. **Traffic**
5. **Statistic**

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

***

↪ Questions? [Join our community Slack](https://www.fiddler.ai/slackinvite) to talk to a product expert 

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/demo?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/4d190fd-fiddler-docs-cta-demo.png\" alt=\"Fiddler Demo\"></a>\n</div>"
}
[/block]
