---
title: "client.publish_events_batch_schema"
slug: "clientpublish_events_batch_schema"
excerpt: "Publishes a batch of events to Fiddler asynchronously using a schema for locating fields within complex data structures."
hidden: false
createdAt: "2022-05-23T20:50:05.198Z"
updatedAt: "2022-06-21T17:24:36.680Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "batch_source",
    "0-1": "Union[pd.Dataframe, str]",
    "0-2": "None",
    "0-3": "Either a pandas DataFrame containing a batch of events, or the path to a file containing a batch of events. Supported file types are\n- CSV (.csv)\n- Avro (.avro)",
    "1-0": "publish_schema",
    "1-1": "dict",
    "1-2": "None",
    "1-3": "A dictionary used for locating fields within complex or nested data structures.",
    "4-0": "group_by",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "The field used to group events together when computing performance metrics (for ranking models only).",
    "2-0": "data_source",
    "2-1": "Optional [fdl.BatchPublishType]",
    "2-2": "None",
    "2-3": "The location of the data source provided. By default, Fiddler will try to infer the value. Can be one of\n- fdl.BatchPublishType.DATAFRAME\n- fdl.BatchPublishType.LOCAL_DISK\n- fdl.BatchPublishType.AWS_S3\n- fdl.BatchPublishType.GCP_STORAGE",
    "3-0": "credentials",
    "3-1": "Optional [dict]",
    "3-2": "None",
    "3-3": "A dictionary containing authorization information for AWS or GCP.\n\nFor AWS, the expected keys are\n- 'aws_access_key_id'\n- 'aws_secret_access_key'\n- 'aws_session_token'\n\nFor GCP, the expected keys are\n- 'gcs_access_key_id'\n- 'gcs_secret_access_key'\n- 'gcs_session_token'"
  },
  "cols": 4,
  "rows": 5
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\npath_to_batch = 'events_batch.avro'\n\nschema = {\n    '__static': {\n        '__project': PROJECT_ID,\n        '__model': MODEL_ID\n    },\n    '__dynamic': {\n        'feature_1': 'features/feature_1',\n        'feature_2': 'features/feature_2',\n        'feature_3': 'features/feature_3',\n        'output_column': 'outputs/output_column',\n        'target_column': 'targets/target_column'\n      ORG = '__org'\n13      MODEL = '__model'\n14      PROJECT = '__project'\n15      TIMESTAMP = '__timestamp'\n16      DEFAULT_TIMESTAMP = '__default_timestamp'\n17      TIMESTAMP_FORMAT = '__timestamp_format'\n18      EVENT_ID = '__event_id'\n19      IS_UPDATE_EVENT = '__is_update_event'\n20      STATUS = '__status'\n21      LATENCY = '__latency'\n22      ITERATOR_KEY = '__iterator_key'\n    }\n}\n\nclient.publish_events_batch_schema(\n    batch_source=path_to_batch,\n    publish_schema=schema\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]