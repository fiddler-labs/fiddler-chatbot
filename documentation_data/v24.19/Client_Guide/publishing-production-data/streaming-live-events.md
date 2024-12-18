---
title: Streaming Live Events
slug: streaming-live-events
excerpt: ''
createdAt: Tue Apr 19 2022 20:07:23 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 22 2024 18:47:45 GMT+0000 (Coordinated Universal Time)
---

# Streaming Live Events

This process is very simple, but it requires that each event is structured as a Python dictionary that maps field names (as they are defined in your Model's schema) to values.

***

### Example 1: A simple three-input fraud model.

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

```python
my_events = my_df.to_dict(orient="records")
```

***

Then to upload the event to Fiddler, all you have to do is call the Fiddler client's `fdl.Model.publish` method.

```python
# For a single event. Note it must be passed as an array.
model.publish([my_event])

# For multiple events where `my_events` is an array Python dictionaries
model.publish(my_events)
```

_After calling the function, please allow 3-5 minutes for events to populate the_ _**Monitor**_ _page._

> 📘 Info
>
> The `event_timestamp` field should contain the **Unix timestamp in milliseconds** for the time the event occurred.
>
> If you do not specify an event timestamp column in the event data published to Fiddler, the current time will be used for each published event. This timestamp will be used to plot the event on time series charts for monitoring. You can specify a custom event timestamp by setting its column name on your `fdl.Model`'s event\_ts\_col property and ensure it is present on each inference published to Fiddler.

### Example 2: Bank churn event

Here's an example using a bank churn model.

```python
# Publish an event
model.publish([{
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
}]
)
```

The `fdl.Model.publish` API can be called in real-time right after your model inference.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

