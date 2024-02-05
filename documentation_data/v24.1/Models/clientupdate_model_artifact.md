---
title: "client.update_model_artifact"
slug: "clientupdate_model_artifact"
excerpt: "Update the model artifact of an existing model with artifact (surrogate or customer uploaded)"
hidden: false
createdAt: "Wed Jan 11 2023 21:01:46 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model_surrogate`](/reference/clientadd_model_surrogate) or [`add_model_artifact`](/reference/clientadd_model_artifact)

| Input Parameter   | Type                                                       | Default | Description                                                                                                                                              |
| :---------------- | :--------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id        | str                                                        | None    | The unique identifier for the project.                                                                                                                   |
| model_id          | str                                                        | None    | A unique identifier for the model.                                                                                                                       |
| model_dir         | str                                                        | None    | A path to the directory containing all of the model files needed to run the model.                                                                       |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec. Supported from server version `23.1` and above with Model Deployment feature enabled. |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.update_model_artifact(  
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir='model_dir/',
)
```
