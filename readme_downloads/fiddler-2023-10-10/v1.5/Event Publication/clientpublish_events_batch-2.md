---
title: "client.publish_events_batch"
slug: "clientpublish_events_batch-2"
excerpt: "Publishes a batch of events to Fiddler asynchronously."
hidden: true
createdAt: "2023-02-08T19:13:10.954Z"
updatedAt: "2023-02-10T01:14:25.597Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The unique identifier for the model.",
    "2-0": "batch_source",
    "2-1": "Union[pd.Dataframe, str]",
    "2-2": "None",
    "2-3": "Either a pandas DataFrame containing a batch of events, or the path to a file containing a batch of events. Supported file types are  \n- CSV (.csv)",
    "3-0": "id_field",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "The field containing event IDs for events in the batch.  If not specified, Fiddler will generate its own ID, which can be retrieved using the **[get_slice](ref:clientget_slice)** API.",
    "4-0": "update_event",
    "4-1": "Optional [bool]",
    "4-2": "None",
    "4-3": "If True, it will only modify an existing event referenced by _id_field_.  If an ID is provided for which there is no event, no change will take place.",
    "5-0": "timestamp_field",
    "5-1": "Optional [str]",
    "5-2": "None",
    "5-3": "The field containing timestamps for events in the batch. Fiddler infers the timestamp format from the column. If timestamp_field is not provided, the Fiddler will assume all the messages are received at the current time.",
    "6-0": "group_by",
    "6-1": "Optional [str]",
    "6-2": "None",
    "6-3": "The field is used to group events when computing performance metrics (for ranking models only)."
  },
  "cols": 4,
  "rows": 7,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

df_events = pd.read_csv('events.csv')

client.publish_events_batch(
        project_id=PROJECT_ID,
        model_id=MODEL_ID,
        batch_source=df_events,
        timestamp_field='inference_date')
```