---
title: "client.delete_model"
slug: "clientdelete_model"
excerpt: "Deletes a model from a project."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 19:31:30 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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