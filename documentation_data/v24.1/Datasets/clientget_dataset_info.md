---
title: "client.get_dataset_info"
slug: "clientget_dataset_info"
excerpt: "Retrieves the DatasetInfo object associated with a dataset."
hidden: false
createdAt: "Mon May 23 2022 19:02:48 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_id       | str  | None    | The unique identifier for the project. |
| dataset_id       | str  | None    | A unique identifier for the dataset.   |

```python Usage
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)
```

| Return Type     | Description                                                                               |
| :-------------- | :---------------------------------------------------------------------------------------- |
| fdl.DatasetInfo | The [fdl.DatasetInfo()](ref:fdldatasetinfo) object associated with the specified dataset. |

```python Response
#NA
```
