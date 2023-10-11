---
title: "client.update_model_surrogate"
slug: "clientupdate_model_surrogate"
excerpt: "Re-generate surrogate model"
hidden: true
createdAt: "2023-01-30T08:25:06.065Z"
updatedAt: "2023-01-31T16:20:48.941Z"
---
> 📘 Note
> 
> This method call cannot replace user uploaded model done using [add_model_artifact](https://docs.fiddler.ai/v1.6/reference/clientadd_model_artifact). It can only re-generate a surrogate model

This can be used to re-generate a surrogate model for a model

| Input Parameter | Type           | Default | Description                                                     |
| :-------------- | :------------- | :------ | :-------------------------------------------------------------- |
| project_id      | str            | None    | The unique identifier for the project.                          |
| model_id        | str            | None    | The unique identifier for the model.                            |
| wait            | Optional[bool] | True    | Whether to wait for async job to finish(True) or return(False). |

```python python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.update_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```



| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |