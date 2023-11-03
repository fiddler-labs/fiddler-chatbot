---
title: "client.publish_events_batch_schema"
slug: "clientpublish_events_batch_schema"
excerpt: "Publishes a batch of events to Fiddler asynchronously using a schema for locating fields within complex data structures."
hidden: false
createdAt: "2022-05-23T20:50:05.198Z"
updatedAt: "2023-10-24T04:14:06.842Z"
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
    "0-3": "Either a pandas DataFrame containing a batch of events, or the path to a file containing a batch of events. Supported file types are  \n  \n- CSV (.csv)",
    "1-0": "publish_schema",
    "1-1": "dict",
    "1-2": "None",
    "1-3": "A dictionary used for locating fields within complex or nested data structures.",
    "2-0": "data_source",
    "2-1": "Optional [fdl.BatchPublishType]",
    "2-2": "None",
    "2-3": "The location of the data source provided. By default, Fiddler will try to infer the value. Can be one of  \n  \n- fdl.BatchPublishType.DATAFRAME  \n- fdl.BatchPublishType.LOCAL_DISK  \n- fdl.BatchPublishType.AWS_S3",
    "3-0": "credentials",
    "3-1": "Optional [dict]",
    "3-2": "None",
    "3-3": "A dictionary containing authorization information for AWS or GCP.  \n  \nFor AWS, the expected keys are  \n  \n- 'aws_access_key_id'  \n- 'aws_secret_access_key'  \n- 'aws_session_token'For GCP, the expected keys are  \n  \n- 'gcs_access_key_id'  \n- 'gcs_secret_access_key'  \n- 'gcs_session_token'",
    "4-0": "group_by",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "The field used to group events together when computing performance metrics (for ranking models only)."
  },
  "cols": 4,
  "rows": 5,
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

path_to_batch = 'events_batch.avro'

schema = {
    '__static': {
        '__project': PROJECT_ID,
        '__model': MODEL_ID
    },
    '__dynamic': {
        'feature_1': 'features/feature_1',
        'feature_2': 'features/feature_2',
        'feature_3': 'features/feature_3',
        'output_column': 'outputs/output_column',
        'target_column': 'targets/target_column'
      ORG = '__org'
13      MODEL = '__model'
14      PROJECT = '__project'
15      TIMESTAMP = '__timestamp'
16      DEFAULT_TIMESTAMP = '__default_timestamp'
17      TIMESTAMP_FORMAT = '__timestamp_format'
18      EVENT_ID = '__event_id'
19      IS_UPDATE_EVENT = '__is_update_event'
20      STATUS = '__status'
21      LATENCY = '__latency'
22      ITERATOR_KEY = '__iterator_key'
    }
}

client.publish_events_batch_schema(
    batch_source=path_to_batch,
    publish_schema=schema
)
```



| Return Type | Description                                                            |
| :---------- | :--------------------------------------------------------------------- |
| dict        | A dictionary object which reports the result of the batch publication. |

```python Example Response
{'status': 202,
 'job_uuid': '5ae7bd3a-2b3f-4444-b288-d51e098a01d',
 'files': ['rroqj_tmpzmczjttb.csv'],
 'message': 'Successfully received the event data. Please allow time for the event ingestion to complete in the Fiddler platform.'}
```