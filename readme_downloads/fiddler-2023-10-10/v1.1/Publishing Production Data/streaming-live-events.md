---
title: "Streaming Live Events"
slug: "streaming-live-events"
hidden: false
createdAt: "2022-04-19T20:07:23.715Z"
updatedAt: "2022-05-02T16:25:01.252Z"
---
[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "See [`client.publish_event`](https://api.fiddler.ai/#client-publish_event) for detailed information on function usage."
}
[/block]
One way to publish production data to Fiddler is by streaming data asynchronously.

This process is very simple, but it requires that each event is structured as a Python dictionary that maps field names (as they are registered with Fiddler) to values.

***

Below is an example event for a simple three-input fraud model.

```python
my_event = {
    "age": 30,
    "gender": "Male",
    "salary": 80000.0,
    "predicted_fraud": 0.89,
    "is_fraud": 1
}
```
[block:callout]
{
  "type": "warning",
  "title": "Note",
  "body": "If you have a pandas DataFrame, you can easily **convert it into a list of event dictionaries** in the above form by using its `to_dict` function."
}
[/block]
    ```python
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

*After calling the function, please allow 3-5 minutes for events to populate the* ***Monitor*** *page.*

[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "The `event_timestamp` field should contain the **Unix timestamp in milliseconds** for the time the event occurred. This timestamp will be used to plot the event on time series charts for monitoring.\n\nIf you do not specify an event timestamp, the current time will be used."
}
[/block]