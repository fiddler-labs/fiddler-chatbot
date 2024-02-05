---
title: "Using Custom Timestamps"
slug: "using-custom-timestamps"
excerpt: ""
hidden: false
createdAt: "Wed Jul 06 2022 16:25:21 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
Fiddler supports **custom timestamp formats when publishing events**.

By default, Fiddler will try to infer your timestamp format, but if you would like to manually specify it, you can do so as well.

When calling [`client.publish_event`](ref:clientpublish_event), there is a `timestamp_format` argument that can be specified to tell Fiddler which format you are using in the event timestamp (specified by `event_timestamp`).

Fiddler supports the following timestamp formats:

## Unix/epoch time in milliseconds

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

## Unix/epoch time in seconds

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

## ISO 8601

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

## What if I'm using batch publishing?

The same argument (`timestamp_format`) is available in both the [`client.publish_events_batch`](ref:clientpublish_events_batch) and [`client.publish_events_batch_schema`](ref:clientpublish_events_batch_schema) functions.
