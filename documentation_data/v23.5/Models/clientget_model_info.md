---
title: "client.get_model_info"
slug: "clientget_model_info"
excerpt: "Retrieves the **ModelInfo** object associated with a model."
hidden: false
createdAt: "2022-05-23T19:40:10.877Z"
updatedAt: "2023-10-24T04:14:06.813Z"
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