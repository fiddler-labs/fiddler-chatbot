---
title: "Using Custom Timestamps"
slug: "using-custom-timestamps"
hidden: false
createdAt: "2022-07-06T16:25:21.887Z"
updatedAt: "2022-07-06T16:25:21.887Z"
---
Fiddler supports **custom timestamp formats when publishing events**.

By default, Fiddler will try to infer your timestamp format, but if you would like to manually specify it, you can do so as well.

When calling [`client.publish_event`](https://api.fiddler.ai/#client-publish_event), there is a `timestamp_format` argument that can be specified to tell Fiddler which format you are using in the event timestamp (specified by `event_timestamp`).

Fiddler supports the following timestamp formats:
[block:api-header]
{
  "title": "Unix/epoch time in milliseconds"
}
[/block]
These timestamps take the form of `1637344470000`.

We can specify this timestamp format by passing `fdl.FiddlerTimestamp.EPOCH_MILLISECONDS` into the `timestamp_format` argument.

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=example_event,
    event_id='event_001',
    event_timestamp=1637344470000,
    timestamp_format=fdl.FiddlerTimestamp.EPOCH_MILLISECONDS
)
```
[block:api-header]
{
  "title": "Unix/epoch time in seconds"
}
[/block]
These timestamps take the form of `1637344470`.

We can specify this timestamp format by passing `fdl.FiddlerTimestamp.EPOCH_SECONDS` into the `timestamp_format` argument.

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=example_event,
    event_id='event_001',
    event_timestamp=1637344470,
    timestamp_format=fdl.FiddlerTimestamp.EPOCH_SECONDS
)
```
[block:api-header]
{
  "title": "ISO 8601"
}
[/block]
These timestamps take the form of `2021-11-19 17:54:30`.

We can specify this timestamp format by passing `fdl.FiddlerTimestamp.ISO_8601` into the `timestamp_format` argument.

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=example_event,
    event_id='event_001',
    event_timestamp='2021-11-19 17:54:30',
    timestamp_format=fdl.FiddlerTimestamp.ISO_8601
)
```

[block:api-header]
{
  "title": "What if I'm using batch publishing?"
}
[/block]
The same argument (`timestamp_format`) is available in both the [`client.publish_events_batch`](https://api.fiddler.ai/#client-publish_events_batch) and [`client.publish_events_batch_schema`](https://api.fiddler.ai/#client-publish_events_batch_schema) functions.