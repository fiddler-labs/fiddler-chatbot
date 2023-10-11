---
title: "client.update_model_artifact"
slug: "clientupdate_model_artifact"
excerpt: "Update the model artifact of an existing model with artifact (surrogate or customer uploaded)"
hidden: false
createdAt: "2023-01-11T21:01:46.995Z"
updatedAt: "2023-08-14T22:54:09.259Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model_surrogate`](/reference/clientadd_model_surrogate) or [`add_model_artifact`](/reference/clientadd_model_artifact)

| Input Parameter   | Type                                                       | Default | Description                                                                                                                                              |
| :---------------- | :--------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_name      | str                                                        | None    | The unique identifier for the project.                                                                                                                   |
| model_name        | str                                                        | None    | A unique identifier for the model.                                                                                                                       |
| artifact_dir      | str                                                        | None    | A path to the directory containing all of the model files needed to run the model.                                                                       |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec. Supported from server version `23.1` and above with Model Deployment feature enabled. |
| wait              | Optional [bool]                                            | True    | A boolean value which determines if the upload method works in synchronous mode or asynchronous mode.                                                    |
| project_id        | str                                                        | None    | `Deprecated` The unique identifier for the project.                                                                                                      |
| model_id          | str                                                        | None    | `Deprecated` A unique identifier for the model.                                                                                                          |
| model_dir         | str                                                        | None    | `Deprecated` A path to the directory containing all of the model files needed to run the model.                                                          |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

client.update_model_artifact(  
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    artifact_dir='artifact_dir/',
)
```