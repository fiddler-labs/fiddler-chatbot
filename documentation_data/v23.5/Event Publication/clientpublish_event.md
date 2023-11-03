---
title: "client.publish_event"
slug: "clientpublish_event"
excerpt: "Publishes a single production event to Fiddler asynchronously."
hidden: false
createdAt: "2022-05-23T19:53:24.116Z"
updatedAt: "2023-10-24T04:14:06.818Z"
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
    "1-3": "A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character.",
    "2-0": "event",
    "2-1": "dict",
    "2-2": "None",
    "2-3": "A dictionary mapping field names to field values. Any fields found that are not present in the model's **ModelInfo** object will be dropped from the event.",
    "3-0": "event_id",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "A unique identifier for the event. If not specified, Fiddler will generate its own ID, which can be retrived using the **get_slice** API.",
    "4-0": "update_event",
    "4-1": "Optional [bool]",
    "4-2": "None",
    "4-3": "If True, will only modify an existing event, referenced by event_id. If no event is found, no change will take place.",
    "5-0": "event_timestamp",
    "5-1": "Optional [int]",
    "5-2": "None",
    "5-3": "The name of the  timestamp input field for when the event took place. The format of this timestamp is given by _timestamp_format_. If no timestamp input is provided, the current time will be used.",
    "6-0": "timestamp_format",
    "6-1": "Optional [fdl.FiddlerTimestamp]",
    "6-2": "fdl.FiddlerTimestamp.INFER",
    "6-3": "The format of the timestamp passed in _event_timestamp_. Can be one of  \n- fdl.FiddlerTimestamp.INFER  \n- fdl.FiddlerTimestamp.EPOCH_MILLISECONDS  \n- fdl.FiddlerTimestamp.EPOCH_SECONDS  \n- fdl.FiddlerTimestamp.ISO_8601",
    "7-0": "casting_type",
    "7-1": "Optional [bool]",
    "7-2": "False",
    "7-3": "If True, will try to cast the data in event to be in line with the data types defined in the model's **ModelInfo** object.",
    "8-0": "dry_run",
    "8-1": "Optional [bool]",
    "8-2": "False",
    "8-3": "If True, the event will not be published, and instead a report will be generated with information about any problems with the event. Useful for debugging issues with event publishing."
  },
  "cols": 4,
  "rows": 9,
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

example_event = {
    'feature_1': 20.7,
    'feature_2': 45000,
    'feature_3': True,
    'output_column': 0.79,
    'target_column': 1
}

client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=example_event,
    event_id='event_001',
    event_timestamp=1637344470000
)
```

| Return Type | Description                                                                          |
| :---------- | :----------------------------------------------------------------------------------- |
| str         | returns a string with a UUID acknowledging that the event was successfully received. |

```Text Example Response
'66cfbeb6-5651-4e8b-893f-90286f435b8d'
```