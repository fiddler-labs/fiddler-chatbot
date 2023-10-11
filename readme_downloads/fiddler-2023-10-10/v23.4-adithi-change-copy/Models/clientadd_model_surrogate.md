---
title: "client.add_model_surrogate"
slug: "clientadd_model_surrogate"
excerpt: "Adds a surrogate model to an existing a model without uploading an artifact."
hidden: false
createdAt: "2022-08-01T03:05:32.641Z"
updatedAt: "2023-08-01T13:44:10.110Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](ref:clientadd_model).

> 🚧 Surrogate models are not supported for input_type = fdl.ModelInputType.TEXT

| Input Parameter   | Type                                                       | Default | Description                                                                                           |
| :---------------- | :--------------------------------------------------------- | :------ | :---------------------------------------------------------------------------------------------------- |
| project_name      | str                                                        | None    | A unique identifier for the project.                                                                  |
| model_name        | str                                                        | None    | A unique identifier for the model.                                                                    |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec.                                    |
| wait              | Optional [bool]                                            | True    | A boolean value which determines if the upload method works in synchronous mode or asynchronous mode. |
| project_id        | str                                                        | None    | `Deprecated` A unique identifier for the project.                                                     |
| model_id          | str                                                        | None    | `Deprecated` A unique identifier for the model.                                                       |

```python
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

client.add_model_surrogate(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME
)

# with deployment_params
client.add_model_surrogate(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    deployment_params=fdl.DeploymentParams(cpu=250, memory=500)
)
```

| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |