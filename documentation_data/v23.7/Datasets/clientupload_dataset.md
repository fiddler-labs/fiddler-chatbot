---
title: "client.upload_dataset"
slug: "clientupload_dataset"
excerpt: "Uploads a dataset from a pandas DataFrame."
hidden: false
createdAt: "Mon May 23 2022 18:58:49 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters   | Type                       | Default | Description                                                                                                                                                                                                |
| :----------------- | :------------------------- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id         | str                        | None    | The unique identifier for the project.                                                                                                                                                                     |
| dataset            | dict                       | None    | A dictionary mapping dataset slice names to pandas DataFrames.                                                                                                                                             |
| dataset_id         | str                        | None    | A unique identifier for the dataset. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| info               | Optional [fdl.DatasetInfo] | None    | The Fiddler [fdl.DatasetInfo()](ref:fdldatasetinfo) object used to describe the dataset.                                                                                                                   |
| size_check_enabled | Optional [bool]            | True    | If True, will issue a warning when a dataset has a large number of rows.                                                                                                                                   |

```python Usage
import pandas as pd

PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(
    df=df
)

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
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
