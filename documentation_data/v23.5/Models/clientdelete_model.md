---
title: "client.delete_model"
slug: "clientdelete_model"
excerpt: "Deletes a model from a project."
hidden: false
createdAt: "2022-05-23T19:31:30.675Z"
updatedAt: "2023-10-24T04:14:06.823Z"
---
For more information, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |
| model_id        | str  | None    | A unique identifier for the model      |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.delete_model(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```