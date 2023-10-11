---
title: "Updating Events"
slug: "updating-events"
hidden: false
createdAt: "2022-04-19T20:16:43.433Z"
updatedAt: "2022-06-30T22:46:37.653Z"
---
Events can be updated after they are published.

The most common use case for this functionality is updating ground truth labels. Existing events that lack ground truth labels can be updated once the actual values are discovered. Or you might find first uploaded labels are wrong and wish to correct them.

To update events, you can use any of our event publishing APIs, just being sure to set the `update_event` flag to `True`.

***

For [`client.publish_event`](https://api.fiddler.ai/#client-publish_event):

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=my_event,
    event_id=my_id,
    update_event=True
)
```

For [`client.publish_events_batch`](https://api.fiddler.ai/#client-publish_events_batch):

```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source="my_batch.csv",
    id_field=my_id_field,
    update_event=True
)
```

For [`client.publish_events_batch_schema`](https://api.fiddler.ai/#client-publish_events_batch_schema):

```python
client.publish_events_batch_schema(
    batch_source="my_batch.csv",
    publish_schema=my_schema,
    update_event=True
)
```

***

**There are a few points to be aware of:**

* Performance metrics (available from the **Performance** tab of the **Monitor** page) will be computed as events are updated.
    * For example, if the ground truth values are originally missing from events in a given time range, there will be **no performance metrics available** for that time range. Once the events are updated, performance metrics will be computed and will populate the monitoring charts.
    * Events that do not originally have ground truth labels should be **uploaded with empty values**—not dummy values. If dummy values are used, you will have improper performance metrics, and once the new values come in, the old, incorrect values will still be present.
* In order to update existing events, you will need access to the event IDs used at the time of upload. If you do not have access to those event IDs, you can find them by using the [`client.get_slice`](https://api.fiddler.ai/#client-get_slice) API and checking the `__event_id` column from the resulting DataFrame.
* If you pass an updated timestamp for an existing event, **this timestamp will be used** for plotting decisions and computed performance metrics on the **Monitor** page. That is, the bin for which data will appear will depend on the new timestamp, not the old one.