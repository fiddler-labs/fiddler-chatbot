---
title: "client.delete_model"
slug: "clientdelete_model"
excerpt: "Deletes a model from a project."
hidden: false
createdAt: "2022-05-23T19:31:30.675Z"
updatedAt: "2023-08-01T13:44:19.106Z"
---
For more information, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

| Input Parameter | Type | Default | Description                                         |
| :-------------- | :--- | :------ | :-------------------------------------------------- |
| project_name    | str  | None    | The unique identifier for the project.              |
| model_name      | str  | None    | A unique identifier for the model                   |
| project_id      | str  | None    | `Deprecated` The unique identifier for the project. |
| model_id        | str  | None    | `Deprecated` A unique identifier for the model      |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

client.delete_model(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME
)
```