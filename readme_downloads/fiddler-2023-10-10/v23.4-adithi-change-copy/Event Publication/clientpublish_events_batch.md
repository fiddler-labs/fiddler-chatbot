---
title: "client.publish_events_batch"
slug: "clientpublish_events_batch"
excerpt: "Publishes a batch of events to Fiddler asynchronously."
hidden: false
createdAt: "2022-05-23T20:30:23.793Z"
updatedAt: "2023-08-01T13:47:04.046Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_name",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_name",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "events_path",
    "2-1": "Path",
    "2-2": "None",
    "2-3": "pathlib.Path pointing to the events file to be uploaded.",
    "3-0": "batch_id",
    "3-1": "Optional[str]",
    "3-2": "None",
    "3-3": "",
    "4-0": "id_field",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "The field containing event IDs for events in the batch.  If not specified, Fiddler will generate its own ID, which can be retrived using the **get_slice** API.",
    "5-0": "update_event",
    "5-1": "Optional [bool]",
    "5-2": "None",
    "5-3": "If True, will only modify an existing event, referenced by _id_field_.  If an ID is provided for which there is no event, no change will take place.",
    "6-0": "timestamp_field",
    "6-1": "Optional [str]",
    "6-2": "None",
    "6-3": "The field containing timestamps for events in the batch. The format of these timestamps is given by _timestamp_format_. If no timestamp is provided for a given row, the current time will be used.",
    "7-0": "timestamp_format",
    "7-1": "Optional [fdl.FiddlerTimestamp]",
    "7-2": "fdl.FiddlerTimestamp.INFER",
    "7-3": "The format of the timestamp passed in _event_timestamp_. Can be one of  \n-fdl.FiddlerTimestamp.INFER  \n  \n- fdl.FiddlerTimestamp.EPOCH_MILLISECONDS  \n- fdl.FiddlerTimestamp.EPOCH_SECONDS  \n- fdl.FiddlerTimestamp.ISO_8601",
    "8-0": "data_source",
    "8-1": "Optional [fdl.BatchPublishType]",
    "8-2": "None",
    "8-3": "The location of the data source provided. By default, Fiddler will try to infer the value. Can be one of  \n  \n- fdl.BatchPublishType.DATAFRAME  \n- fdl.BatchPublishType.LOCAL_DISK  \n- fdl.BatchPublishType.AWS_S3",
    "9-0": "casting_type",
    "9-1": "Optional [bool]",
    "9-2": "False",
    "9-3": "If True, will try to cast the data in event to be in line with the data types defined in the model's **ModelInfo** object.",
    "10-0": "credentials",
    "10-1": "Optional [dict]",
    "10-2": "None",
    "10-3": "A dictionary containing authorization information for AWS or GCP.  \n  \nFor AWS, the expected keys are  \n  \n- 'aws_access_key_id'  \n- 'aws_secret_access_key'  \n- 'aws_session_token'For GCP, the expected keys are  \n  \n- 'gcs_access_key_id'  \n- 'gcs_secret_access_key'  \n- 'gcs_session_token'",
    "11-0": "group_by",
    "11-1": "Optional [str]",
    "11-2": "None",
    "11-3": "The field used to group events together when computing performance metrics (for ranking models only).",
    "12-0": "project_id",
    "12-1": "str",
    "12-2": "None",
    "12-3": "`Deprecated` The unique identifier for the project.",
    "13-0": "model_id",
    "13-1": "str",
    "13-2": "None",
    "13-3": "`Deprecated` A unique identifier for the model."
  },
  "cols": 4,
  "rows": 14,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

df_events = pd.read_csv('events.csv')

client.publish_events_batch(
        project_name=PROJECT_NAME,
        model_name=MODEL_NAME,
        batch_source=df_events,
        timestamp_field='inference_date')
```

| Return Type | Description                                                            |
| :---------- | :--------------------------------------------------------------------- |
| dict        | A dictionary object which reports the result of the batch publication. |

```python Example Response
{'status': 202,
 'job_uuid': '4ae7bd3a-2b3f-4444-b288-d51e07b6736d',
 'files': ['ssoqj_tmpzmczjuob.csv'],
 'message': 'Successfully received the event data. Please allow time for the event ingestion to complete in the Fiddler platform.'}
```