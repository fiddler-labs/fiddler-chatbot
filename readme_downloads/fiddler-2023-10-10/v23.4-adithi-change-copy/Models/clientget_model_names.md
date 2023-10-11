---
title: "client.get_model_names"
slug: "clientget_model_names"
excerpt: "Retrieves the model IDs of all models accessible within a project."
hidden: true
createdAt: "2023-08-01T11:52:26.825Z"
updatedAt: "2023-08-01T13:44:43.645Z"
---
| Input Parameter | Type | Default | Description                                         |
| :-------------- | :--- | :------ | :-------------------------------------------------- |
| project_name    | str  | None    | The unique identifier for the project.              |
| project_id      | str  | None    | `Deprecated` The unique identifier for the project. |

```python Usage
PROJECT_NAME = 'example_project'

client.list_models(
    project_name=PROJECT_NAME
)
```

| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| list        | A list containing the string ID of each model. |

```python Response
[
    'model_a',
    'model_b',
    'model_c'
]
```