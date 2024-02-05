---
title: "client.list_datasets"
slug: "clientlist_datasets"
excerpt: "Retrieves the dataset IDs of all datasets accessible within a project."
hidden: false
createdAt: "Mon May 23 2022 16:42:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 24 2024 19:33:13 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_id       | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = "example_project"

client.list_datasets(
    project_id=PROJECT_ID
)
```

| Return Type | Description                                                |
| :---------- | :--------------------------------------------------------- |
| list        | A list containing the dataset ID strings for each project. |

```python Response
[
    'dataset_a',
    'dataset_b',
    'dataset_c'
]
```
