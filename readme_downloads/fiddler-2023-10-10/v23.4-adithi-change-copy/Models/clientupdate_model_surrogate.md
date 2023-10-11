---
title: "client.update_model_surrogate"
slug: "clientupdate_model_surrogate"
excerpt: "Re-generate surrogate model"
hidden: false
createdAt: "2023-01-30T08:25:06.065Z"
updatedAt: "2023-08-01T13:46:18.873Z"
---
> 📘 Note
> 
> This method call cannot replace user uploaded model done using [add_model_artifact](ref:clientadd_model_artifact). It can only re-generate a surrogate model

This can be used to re-generate a surrogate model for a model

| Input Parameter   | Type                                                       | Default | Description                                                                                           |
| :---------------- | :--------------------------------------------------------- | :------ | :---------------------------------------------------------------------------------------------------- |
| project_name      | str                                                        | None    | A unique identifier for the project.                                                                  |
| model_name        | str                                                        | None    | A unique identifier for the model.                                                                    |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec.                                    |
| wait              | Optional[bool]                                             | True    | A boolean value which determines if the update method works in synchronous mode or asynchronous mode. |
| project_id        | str                                                        | None    | `Deprecated` A unique identifier for the project.                                                     |
| model_id          | str                                                        | None    | `Deprecated` A unique identifier for the model.                                                       |

```python python
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

client.update_model_surrogate(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME
)

# with deployment_params
client.update_model_surrogate(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    deployment_params=fdl.DeploymentParams(cpu=250, memory=500)
)
```

| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |

> 🚧 Warning
> 
> 1. project_id is renamed to project_name.
> 2. model_id is renamed to model_name.
> 3. wait is added.