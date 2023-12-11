---
title: "client.add_model_surrogate"
slug: "clientadd_model_surrogate"
excerpt: "Adds a surrogate model to an existing a model without uploading an artifact."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon Aug 01 2022 03:05:32 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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