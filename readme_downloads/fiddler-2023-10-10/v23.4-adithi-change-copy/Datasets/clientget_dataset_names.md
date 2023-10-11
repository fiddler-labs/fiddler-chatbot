---
title: "client.get_dataset_names"
slug: "clientget_dataset_names"
excerpt: "Retrieves the dataset names of all datasets accessible within a project."
hidden: true
createdAt: "2023-07-31T11:35:23.606Z"
updatedAt: "2023-08-01T13:36:19.235Z"
---
| Input Parameters | Type | Default | Description                                         |
| :--------------- | :--- | :------ | :-------------------------------------------------- |
| project_name     | str  | None    | The unique identifier for the project.              |
| project_id       | str  | None    | `Deprecated` The unique identifier for the project. |

```python Usage
PROJECT_NAME = "example_project"

client.get_dataset_names(
    project_name=PROJECT_NAME
)
```

| Return Type | Description                                                 |
| :---------- | :---------------------------------------------------------- |
| list        | A list containing the project name string for each project. |

```python Response
[
    'dataset_a',
    'dataset_b',
    'dataset_c'
]
```