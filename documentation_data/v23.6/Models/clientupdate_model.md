---
title: "client.update_model"
slug: "clientupdate_model"
excerpt: "Replaces the model artifact for a model."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 19:26:42 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
For more information, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

> 🚧 Warning
> 
> This function does not allow for changes in a model's schema. The inputs and outputs to the model must remain the same.

| Input Parameter   | Type         | Default | Description                                                                                                                       |
| :---------------- | :----------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| project_id        | str          | None    | The unique identifier for the project.                                                                                            |
| model_id          | str          | None    | A unique identifier for the model.                                                                                                |
| model_dir         | pathlib.Path | None    | A path to the directory containing all of the model files needed to run the model.                                                |
| force_pre_compute | bool         | True    | If True, re-run precomputation steps for the model. This can also be done manually by calling **client.trigger_pre_computation**. |

```python Usage
import pathlib

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

model_dir = pathlib.Path('model_dir')

client.update_model(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir=model_dir
)
```



| Return Type | Description                                           |
| :---------- | :---------------------------------------------------- |
| bool        | A boolean denoting whether the update was successful. |

```python Response
True
```