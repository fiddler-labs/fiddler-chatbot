---
title: "client.delete_model"
slug: "clientdelete_model"
excerpt: "Replaces the model artifact for a model."
hidden: false
createdAt: "2022-05-23T19:31:30.675Z"
updatedAt: "2023-03-29T14:46:29.520Z"
---
For more information, see [Uploading a Model Artifact](doc:uploading-a-model-artifact).

| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |
| model_id        | str  | None    | A unique identifier for the model.     |



```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.delete_model(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```