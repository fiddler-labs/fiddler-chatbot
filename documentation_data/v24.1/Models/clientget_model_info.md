---
title: "client.get_model_info"
slug: "clientget_model_info"
excerpt: "Retrieves the **ModelInfo** object associated with a model."
hidden: false
createdAt: "Mon May 23 2022 19:40:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type | Default | Description                                                                                                                                                                                              |
| :-------------- | :--- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project.                                                                                                                                                                   |
| model_id        | str  | None    | A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

model_info = client.get_model_info(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```

| Return Type                       | Description                                                   |
| :-------------------------------- | :------------------------------------------------------------ |
| [fdl.ModelInfo](ref:fdlmodelinfo) | The **ModelInfo** object associated with the specified model. |
