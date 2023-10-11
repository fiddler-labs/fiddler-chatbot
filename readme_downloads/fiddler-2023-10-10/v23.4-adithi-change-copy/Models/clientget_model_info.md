---
title: "client.get_model_info"
slug: "clientget_model_info"
excerpt: "Retrieves the **ModelInfo** object associated with a model."
hidden: false
createdAt: "2022-05-23T19:40:10.877Z"
updatedAt: "2023-08-01T13:44:26.698Z"
---
| Input Parameter | Type | Default | Description                                                                                                                                                                                                           |
| :-------------- | :--- | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_name    | str  | None    | The unique identifier for the project.                                                                                                                                                                                |
| model_name      | str  | None    | A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character.              |
| project_id      | str  | None    | `Deprecated` The unique identifier for the project.                                                                                                                                                                   |
| model_id        | str  | None    | `Deprecated` A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

model_info = client.get_model_info(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
)
```

| Return Type                       | Description                                                   |
| :-------------------------------- | :------------------------------------------------------------ |
| [fdl.ModelInfo](ref:fdlmodelinfo) | The **ModelInfo** object associated with the specified model. |