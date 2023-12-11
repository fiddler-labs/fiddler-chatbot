---
title: "client.update_model (COPY)"
slug: "clientupdate_model-copy"
excerpt: "Update model metadata"
hidden: true
metadata: 
image: []
robots: "index"
createdAt: "Thu Sep 14 2023 14:54:35 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
> 🚧 Warning
> 
> This function does not allow for changes in a model's schema. The inputs and outputs to the model must remain the same.
> 
> This function does not update the model artifacts. Please see `client.update_model_artifact` for updating the artifacts.

| Input Parameter | Type                    | Default | Description                            |
| :-------------- | :---------------------- | :------ | :------------------------------------- |
| project_id      | str                     | None    | The unique identifier for the project. |
| model_id        | str                     | None    | A unique identifier for the model.     |
| info            | Optional[fdl.ModelInfo] | None    | New ModelInfo object to update         |
| framework       | Optional[str]           | None    | New framework to update                |
| requirements    | Optional[str]           | None    | New requirements to update             |

```python Usage
import pathlib

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

model_dir = pathlib.Path('model_dir')

client.update_model(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    info=model_info,
)
```

| Return Type | Description         |
| :---------- | :------------------ |
| Model       | Model schema object |