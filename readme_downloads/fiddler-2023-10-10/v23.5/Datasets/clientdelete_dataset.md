---
title: "client.delete_dataset"
slug: "clientdelete_dataset"
excerpt: "Deletes a dataset from a project."
hidden: false
createdAt: "2022-05-23T19:00:39.913Z"
updatedAt: "2023-06-07T17:34:03.931Z"
---
| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_id       | str  | None    | The unique identifier for the project. |
| dataset_id       | str  | None    | A unique identifier for the dataset.   |

```python Usage
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

client.delete_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
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