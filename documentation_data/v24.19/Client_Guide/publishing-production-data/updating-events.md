---
title: Updating Events
slug: updating-events
excerpt: ''
createdAt: Tue Apr 19 2022 20:16:43 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 22 2024 18:57:15 GMT+0000 (Coordinated Universal Time)
---

# Updating Events

Fiddler supports _partial_ updates of events. Specifically, for your [target](../../Python\_Client\_3-x/api-methods-30.md#modelspec) column and [metadata](../../Python\_Client\_3-x/api-methods-30.md#modelspec) columns.

The most common use case for this functionality is updating ground truth labels. Existing events that lack ground truth labels can be updated once the actual values are discovered. Or you might find that the initially uploaded labels are wrong and wish to correct them.

We also support updating **metadata** columns with new values. You can observe the changes in [Analytics](../../UI\_Guide/analytics-ui/), but the [Performance](../../UI\_Guide/monitoring-ui/performance.md) metrics of the columns won't be reflected.

Other columns(Decision, Input and Output) can only be sent at insertion time (with `update_event=False`). They are dropped if you send them and set `update_event=True`.

Set `update_event=True` to indicate that you are updating an existing event. You only need to provide the fields that you want to change—any fields you leave out will remain as they were before the update.

***

### Example in client 3.x

Below is the code you can use to update the target and metadata columns values for selected events (for instance when you get ground truth data or some other information relating to the event at a later stage)

```python
model_spec = fdl.ModelSpec(
    inputs=['input1'],
    targets=['target']
    outputs='output'
    metadata=['uri', 'record_tag'],
)

fdl_model = fdl.Model.from_data(
    name=model_name,
    project_id=project.id,
    source=dataset_df,
    spec=model_spec,
    event_id_col='event_id'
)

model.publish(source='my_events.csv', update=True)
```

Where `my_events.csv` contains the corresponding columns to be updated, as well as the `event_id_col` of the model: `event_id`. Here is an example of `my_events.csv`:

| event\_id | target     | uri                      | record\_tag  |
| --------- | ---------- | ------------------------ | ------------ |
| `A1`      | `Selected` | `s3://dataset/image.jpg` | `category_1` |

Refer to [publish](../../Python\_Client\_3-x/api-methods-30.md#publish) doc for more details on different sources and parameters.

> 📘 **There are a few points to be aware of:**
>
> * [Performance](../../UI\_Guide/monitoring-ui/performance.md) metrics (available from the **Performance** tab of the **Monitor** page) will be computed as events are updated.
>   * For example, if the ground truth values are originally missing from events in a given time range, there will be **no performance metrics available** for that time range. Once the events are updated, performance metrics will be computed and will populate the monitoring charts.
>   * Events that do not originally have ground truth labels should be **uploaded with empty values**—not dummy values. If dummy values are used, you will have improper performance metrics, and once the new values come in, the old, incorrect values will still be present.
>   * Update on **Metadata** columns won't be reflected.
> * In order to update existing events, you will need access to the event IDs used at the time of upload. If you do not have access to those event IDs, you can find them by using the `fdl.Model.get_slice` API and checking the `__event_id` column from the resulting DataFrame.
> * If you pass an updated timestamp for an existing event, **this timestamp will be used** for plotting decisions and computed performance metrics on the Dashboards and Charts. That is, the bin for which data will appear will depend on the new timestamp, not the old one.

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

