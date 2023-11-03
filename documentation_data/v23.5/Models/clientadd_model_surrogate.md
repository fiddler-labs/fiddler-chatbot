---
title: "client.add_model_surrogate"
slug: "clientadd_model_surrogate"
excerpt: "Adds a surrogate model to an existing a model without uploading an artifact."
hidden: false
createdAt: "2022-08-01T03:05:32.641Z"
updatedAt: "2023-10-24T04:14:06.835Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](ref:clientadd_model).

> 🚧 Surrogate models are not supported for input_type = fdl.ModelInputType.TEXT

| Input Parameter   | Type                                                       | Default | Description                                                        |
| :---------------- | :--------------------------------------------------------- | :------ | :----------------------------------------------------------------- |
| project_id        | str                                                        | None    | A unique identifier for the project.                               |
| model_id          | str                                                        | None    | A unique identifier for the model.                                 |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec. |

```python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.add_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)

# with deployment_params
client.add_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    deployment_params=fdl.DeploymentParams(cpu=250, memory=500)
)
```

| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |