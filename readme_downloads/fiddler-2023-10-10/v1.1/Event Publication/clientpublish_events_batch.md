---
title: "client.publish_events_batch"
slug: "clientpublish_events_batch"
excerpt: "Publishes a batch of events to Fiddler asynchronously."
hidden: false
createdAt: "2022-05-23T20:30:23.793Z"
updatedAt: "2022-06-21T17:24:31.826Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "0-0": "project_id",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "batch_source",
    "2-1": "Union[pd.Dataframe, str]",
    "2-2": "None",
    "2-3": "Either a pandas DataFrame containing a batch of events, or the path to a file containing a batch of events. Supported file types are\n* CSV (.csv)\n* Parquet (.pq)\n* Pickled DataFrame (.pkl)",
    "3-0": "id_field",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "The field containing event IDs for events in the batch.  If not specified, Fiddler will generate its own ID, which can be retrived using the **get_slice** API.",
    "4-0": "update_event",
    "4-1": "Optional [bool]",
    "4-2": "None",
    "4-3": "If True, will only modify an existing event, referenced by *id_field*.  If an ID is provided for which there is no event, no change will take place.",
    "5-0": "timestamp_field",
    "5-1": "Optional [str]",
    "5-2": "None",
    "5-3": "The field containing timestamps for events in the batch. The format of these timestamps is given by *timestamp_format*. If no timestamp is provided for a given row, the current time will be used.",
    "6-0": "timestamp_format",
    "6-1": "Optional [fdl.FiddlerTimestamp]",
    "6-2": "fdl.FiddlerTimestamp.INFER",
    "6-3": "The format of the timestamp passed in *event_timestamp*. Can be one of\n-fdl.FiddlerTimestamp.INFER\n- fdl.FiddlerTimestamp.EPOCH_MILLISECONDS\n- fdl.FiddlerTimestamp.EPOCH_SECONDS\n- fdl.FiddlerTimestamp.ISO_8601",
    "8-0": "casting_type",
    "8-1": "Optional [bool]",
    "8-2": "False",
    "8-3": "If True, will try to cast the data in event to be in line with the data types defined in the model's **ModelInfo** object.",
    "10-0": "group_by",
    "10-1": "Optional [str]",
    "10-2": "None",
    "10-3": "The field used to group events together when computing performance metrics (for ranking models only).",
    "7-0": "data_source",
    "7-1": "Optional [fdl.BatchPublishType]",
    "7-2": "None",
    "7-3": "The location of the data source provided. By default, Fiddler will try to infer the value. Can be one of\n- fdl.BatchPublishType.DATAFRAME\n- fdl.BatchPublishType.LOCAL_DISK\n- fdl.BatchPublishType.AWS_S3\n- fdl.BatchPublishType.GCP_STORAGE",
    "9-0": "credentials",
    "9-1": "Optional [dict]",
    "9-2": "None",
    "9-3": "A dictionary containing authorization information for AWS or GCP.\n\nFor AWS, the expected keys are\n- 'aws_access_key_id'\n- 'aws_secret_access_key'\n- 'aws_session_token'\n\nFor GCP, the expected keys are\n- 'gcs_access_key_id'\n- 'gcs_secret_access_key'\n- 'gcs_session_token'"
  },
  "cols": 4,
  "rows": 11
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\ndf_events = pd.read_csv('events.csv')\n\nclient.publish_events_batch(\n        project_id=PROJECT_ID,\n        model_id=MODEL_ID,\n        batch_source=df_events,\n        timestamp_field='inference_date')",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]