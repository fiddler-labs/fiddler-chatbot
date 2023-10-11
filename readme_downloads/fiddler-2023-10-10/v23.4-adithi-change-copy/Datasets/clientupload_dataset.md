---
title: "client.upload_dataset"
slug: "clientupload_dataset"
excerpt: "Uploads a dataset from a pandas DataFrame."
hidden: false
createdAt: "2022-05-23T18:58:49.880Z"
updatedAt: "2023-08-01T13:42:31.311Z"
---
| Input Parameters   | Type                       | Default | Description                                                                                                                                                                                                            |
| :----------------- | :------------------------- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_name       | str                        | None    |  The unique identifier for the project.                                                                                                                                                                                |
| project_id         | str                        | None    | `Deprecated` The unique identifier for the project.                                                                                                                                                                    |
| dataset            | Dict[str, pd.DataFrame]    | None    | `Deprecated`A dictionary mapping dataset slice names to pandas DataFrames.                                                                                                                                             |
| dataset_id         | str                        | None    | `Deprecated`A unique identifier for the dataset. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| datasets           | dict                       | None    | A dictionary mapping dataset slice names to pandas DataFrames.                                                                                                                                                         |
| dataset_name       | str                        | None    | A unique identifier for the dataset. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character.             |
| size_check_enabled | Optional [bool]            | True    | `Deprecated` If True, will issue a warning when a dataset has a large number of rows.                                                                                                                                  |
| info               | Optional [fdl.DatasetInfo] | None    | The Fiddler [fdl.DatasetInfo()](ref:fdldatasetinfo) object used to describe the dataset.                                                                                                                               |
| wait               | Optional [bool]            | True    | A boolean value which determines if the upload method works in synchronous mode or asynchronous mode.                                                                                                                  |

```python Usage
import pandas as pd

PROJECT_NAME = 'example_project'
DATASET_NAME = 'example_dataset'

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(
    df=df
)

client.upload_dataset(
    project_name=PROJECT_NAME,
    dataset_name=DATASET_NAME,
    datasets={
        'baseline': df
    },
    info=dataset_info
)
```

| Return Type | Description                                                     |
| :---------- | :-------------------------------------------------------------- |
| dict        | A dictionary containing information about the uploaded dataset. |

```python Response
{'uuid': '7046dda1-2779-4987-97b4-120e6185cc0b',
 'name': 'Ingestion dataset Upload',
 'info': {'project_name': 'example_model',
  'resource_name': 'acme_data',
  'resource_type': 'DATASET'},
 'status': 'SUCCESS',
 'progress': 100.0,
 'error_message': None,
 'error_reason': None}
```