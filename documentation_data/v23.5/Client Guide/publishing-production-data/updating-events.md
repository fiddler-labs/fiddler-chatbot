---
title: "Updating Events"
slug: "updating-events"
hidden: false
createdAt: "2022-04-19T20:16:43.433Z"
updatedAt: "2023-10-19T20:59:24.694Z"
---
Fiddler supports _partial_ updates of events. Specifically, for your **[target](ref:fdlmodelinfo)** column. 

The most common use case for this functionality is updating ground truth labels. Existing events that lack ground truth labels can be updated once the actual values are discovered. Or you might find that the initially uploaded labels are wrong and wish to correct them. Other columns can only be sent at insertion time (with `update_event=False`).

Set `update_event=True` to indicate that you are updating an existing event. You only need to provide the decision, metadata, and/or target fields that you want to change—any fields you leave out will remain as they were before the update.

***



For [`client.publish_event`](ref:clientpublish_event):

```python
client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=my_event,
    event_id=my_id,
    update_event=True
)
```



For [`client.publish_events_batch`](ref:clientpublish_events_batch):

```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source="my_batch.csv",
    id_field=my_id_field,
    update_event=True
)
```



For [`client.publish_events_batch_schema`](ref:clientpublish_events_batch_schema):

```python
client.publish_events_batch_schema(
    batch_source="my_batch.csv",
    publish_schema=my_schema,
    update_event=True
)
```



***



> 📘 **There are a few points to be aware of:**
> 
> - [Performance](doc:performance) metrics (available from the **Performance** tab of the **Monitor** page) will be computed as events are updated.
>   - For example, if the ground truth values are originally missing from events in a given time range, there will be **no performance metrics available** for that time range. Once the events are updated, performance metrics will be computed and will populate the monitoring charts.
>   - Events that do not originally have ground truth labels should be **uploaded with empty values**—not dummy values. If dummy values are used, you will have improper performance metrics, and once the new values come in, the old, incorrect values will still be present.
> - In order to update existing events, you will need access to the event IDs used at the time of upload. If you do not have access to those event IDs, you can find them by using the [`client.get_slice`](ref:clientget_slice) API and checking the `__event_id` column from the resulting DataFrame.
> - If you pass an updated timestamp for an existing event, **this timestamp will be used** for plotting decisions and computed performance metrics on the **[Monitor](doc:monitoring-ui)** page. That is, the bin for which data will appear will depend on the new timestamp, not the old one.