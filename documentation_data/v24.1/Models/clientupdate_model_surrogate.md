---
title: "client.update_model_surrogate"
slug: "clientupdate_model_surrogate"
excerpt: "Re-generate surrogate model"
hidden: false
createdAt: "Mon Jan 30 2023 08:25:06 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
> 📘 Note
> 
> This method call cannot replace user uploaded model done using [add_model_artifact](ref:clientadd_model_artifact). It can only re-generate a surrogate model

This can be used to re-generate a surrogate model for a model

| Input Parameter   | Type                                                       | Default | Description                                                        |
| :---------------- | :--------------------------------------------------------- | :------ | :----------------------------------------------------------------- |
| project_id        | str                                                        | None    | A unique identifier for the project.                               |
| model_id          | str                                                        | None    | A unique identifier for the model.                                 |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec. |
| wait              | Optional[bool]                                             | True    | Whether to wait for async job to finish(True) or return(False).    |

```python python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.update_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)

# with deployment_params
client.update_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    deployment_params=fdl.DeploymentParams(cpu=250, memory=500)
)
```

| Return Type | Description    |
| :---------- | :------------- |
| None        | Returns `None` |
