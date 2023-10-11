---
title: "Monitoring"
slug: "monitoring-ui"
hidden: false
createdAt: "2022-04-19T20:24:28.175Z"
updatedAt: "2023-09-27T18:30:48.362Z"
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

   You will need to configure bins and alerts for your model. These will be discussed in details below.

4. **Send traffic from your live deployed model to Fiddler**

   Use the Fiddler SDK to send us traffic from your live deployed model.

## Publish events to Fiddler

In order to send traffic to Fiddler, use the [`publish_event`](https://api.fiddler.ai/#client-publish_event) API from the Fiddler SDK. Here is a sample of the API call:

```python Publish Event
import fiddler as fdl
	fiddler_api = fdl.FiddlerApi(url=url, org_id=org_id, auth_token=token)
	# Publish an event
	fiddler_api.publish_event(
		project_id='bank_churn',
		model_id='bank_churn',
		event={
			"CreditScore": 650,      # data type: int
			"Geography": "France",   # data type: category
			"Gender": "Female",
			"Age": 45,
			"Tenure": 2,
			"Balance": 10000.0,      # data type: float
			"NumOfProducts": 1,
			"HasCrCard": "Yes",
			"isActiveMember": "Yes",
			"EstimatedSalary": 120000,
			"probability_churned": 0.105,
      "churn": 1
		},
		event_id=’some_unique_id’, #optional
		update_event=False, #optional
		event_timestamp=1511253040519 #optional
	)
```

The `publish_event` API can be called in real-time right after your model inference. 

> 📘 Info
> 
> You can also publish events as part of a batch call after the fact using the `publish_events_batch` API (click [here](https://api.fiddler.ai/#client-publish_events_batch) for more information). In this case, you will need to send Fiddler the original event timestamps as to accurately populate the time series charts.

Following is a description of all the parameters for `publish_event`:

- `project_id`: Project ID for the project this event belongs to.

- `model_id`: Model ID for the model this event belongs to.

- `event`: The actual event as an array. The event can contain:

  - Inputs
  - Outputs
  - Target
  - Decisions (categorical only)
  - Metadata

- `event_id`: A user-generated unique event ID that Fiddler can use to join inputs/outputs to targets/decisions/metadata sent later as an update.

- `update_event`: A flag indicating if the event is a new event (insertion) or an update to an existing event. When updating an existing event, it's required that the user sends an `event_id`.

- `event_timestamp`: The timestamp at which the event (or update) occurred, represented as a UTC timestamp in milliseconds. When updating an existing event, use the time of the update, i.e., the time the target/decision were generated and not when the model predictions were made.

## Updating events

Fiddler supports partial updates of events for your **target** column. This can be useful when you don’t have access to the ground truth for your model at the time the model's prediction is made. Other columns can only be sent at insertion time (with `update_event=False`).

Set `update_event=True` to indicate that you are updating an existing event. You only need to provide the decision, metadata, and/or target fields that you want to change—any fields you leave out will remain as they were before the update.

**Example**

Here’s an example of using the publish event API to update an existing event:

```python Update Existing Event
import fiddler as fdl

fiddler_api = fdl.FiddlerApi(
	url=url,
	org_id=org_id,
	auth_token=token
)

fiddler_api.publish_event(
	project_id='bank_churn',
	model_id='bank_churn',
	event = {
		'churn': 0,    # data type: category
	},
	event_id=’some_unique_id’,
	update_event=True
)
```

The above `publish_event` call will tell Fiddler to update the target (`'churn': 0`) of an existing event  (`event_id='some_unique_id'`).

Once you’ve used the SDK to send Fiddler your live event data, that data will show up under the **Monitor** tab in the Fiddler UI:

![](https://files.readme.io/978d0c7-Monitor_dashboard.png "Monitor_dashboard.png")

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/demo?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/4d190fd-fiddler-docs-cta-demo.png\" alt=\"Fiddler Demo\"></a>\n</div>"
}
[/block]