---
title: "client.add_model_surrogate"
slug: "clientadd_model_surrogate"
excerpt: "Adds a surrogate model to an existing a model without uploading an artifact."
hidden: false
createdAt: "2022-08-01T03:05:32.641Z"
updatedAt: "2023-01-12T14:00:06.130Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](/reference/clientadd_model).



| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |
| model_id        | str  | None    | A unique identifier for the model.     |

```python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.add_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```



| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |