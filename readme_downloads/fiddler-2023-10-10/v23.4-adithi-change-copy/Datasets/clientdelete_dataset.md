---
title: "client.delete_dataset"
slug: "clientdelete_dataset"
excerpt: "Deletes a dataset from a project."
hidden: false
createdAt: "2022-05-23T19:00:39.913Z"
updatedAt: "2023-08-01T13:42:58.814Z"
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

client.delete_dataset(
    project_name=PROJECT_NAME,
    dataset_name=DATASET_NAME
)
```

| Return Type | Description                                        |
| :---------- | :------------------------------------------------- |
| str         | A message confirming that the dataset was deleted. |

```python Response
'Dataset deleted example_dataset'
```

> 🚧 Caution
> 
> You cannot delete a dataset without deleting the models associated with that dataset first.