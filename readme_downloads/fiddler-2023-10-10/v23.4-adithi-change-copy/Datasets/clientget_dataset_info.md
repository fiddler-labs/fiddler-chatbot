---
title: "client.get_dataset_info"
slug: "clientget_dataset_info"
excerpt: "Retrieves the DatasetInfo object associated with a dataset."
hidden: false
createdAt: "2022-05-23T19:02:48.312Z"
updatedAt: "2023-08-01T13:43:14.522Z"
---
| Input Parameters | Type | Default | Description                                         |
| :--------------- | :--- | :------ | :-------------------------------------------------- |
| project_name     | str  | None    | The unique identifier for the project.              |
| dataset_name     | str  | None    | A unique identifier for the dataset.                |
| project_id       | str  | None    | `Deprecated` The unique identifier for the project. |
| dataset_id       | str  | None    | `Deprecated` A unique identifier for the dataset.   |

```python Usage
PROJECT_NAME = 'example_project'
DATASET_NAME = 'example_dataset'

dataset_info = client.get_dataset_info(
    project_name=PROJECT_NAME,
    dataset_name=DATASET_NAME
)
```

| Return Type     | Description                                                                               |
| :-------------- | :---------------------------------------------------------------------------------------- |
| fdl.DatasetInfo | The [fdl.DatasetInfo()](ref:fdldatasetinfo) object associated with the specified dataset. |

```python Response
#NA
```