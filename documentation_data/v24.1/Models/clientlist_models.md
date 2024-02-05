---
title: "client.list_models"
slug: "clientlist_models"
excerpt: "Retrieves the model IDs of all models accessible within a project."
hidden: false
createdAt: "Mon May 23 2022 19:06:21 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = 'example_project'

client.list_models(
    project_id=PROJECT_ID
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
