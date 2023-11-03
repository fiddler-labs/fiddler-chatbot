---
title: "Streaming Live Events"
slug: "streaming-live-events"
hidden: false
createdAt: "2022-04-19T20:07:23.715Z"
updatedAt: "2023-10-19T20:59:24.642Z"
---
> 📘 Info
> 
> See [`client.publish_event`](ref:clientpublish_event) for detailed information on function usage.

One way to publish production data to Fiddler is by streaming data asynchronously.

This process is very simple, but it requires that each event is structured as a Python dictionary that maps field names (as they are [onboarded](ref:fdlmodelinfo) with Fiddler) to values.

***

## Example 1: A simple three-input fraud model.

```python
my_event = {
    "age": 30,
    "gender": "Male",
    "salary": 80000.0,
    "predicted_fraud": 0.89,
    "is_fraud": 1
}
```

> 🚧 Note
> 
> If you have a pandas DataFrame, you can easily **convert it into a list of event dictionaries** in the above form by using its `to_dict` function.

```python Python
my_events = my_df.to_dict(orient="records")
```

***

Then to upload the event to Fiddler, all you have to do is call the Fiddler client's `publish_event` method.

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=my_event,
    event_timestamp=1635862057000
)
```

_After calling the function, please allow 3-5 minutes for events to populate the_ **_Monitor_** _page._

> 📘 Info
> 
> The `event_timestamp` field should contain the **Unix timestamp in milliseconds** for the time the event occurred. This timestamp will be used to plot the event on time series charts for monitoring.
> 
> If you do not specify an event timestamp, the current time will be used.

## Example 2: Bank churn event

In order to send traffic to Fiddler, use the [`publish_event`](ref:clientpublish_event) API from the Fiddler SDK. Here is a sample of the API call:

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
> You can also publish events as part of a batch call after the fact using the `publish_events_batch` API (click [here](ref:clientpublish_events_batch) for more information). In this case, you will need to send Fiddler the original event timestamps as to accurately populate the time series charts.

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