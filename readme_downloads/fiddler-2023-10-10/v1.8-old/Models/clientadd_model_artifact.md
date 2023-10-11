---
title: "client.add_model_artifact"
slug: "clientadd_model_artifact"
excerpt: "Adds a model artifact to an existing model"
hidden: false
createdAt: "2022-08-01T03:09:29.086Z"
updatedAt: "2023-08-14T22:43:04.910Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](/reference/clientadd_model).

| Input Parameter   | Type                                                       | Default | Description                                                                                                                                              |
| :---------------- | :--------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id        | str                                                        | None    | The unique identifier for the project.                                                                                                                   |
| model_id          | str                                                        | None    | A unique identifier for the model.                                                                                                                       |
| model_dir         | str                                                        | None    | A path to the directory containing all of the [model files](doc:artifacts-and-surrogates) needed to run the model.                                       |
| deployment_params | Optional\[[fdl.DeploymentParams](ref:fdldeploymentparams)] | None    | Deployment parameters object for tuning the model deployment spec. Supported from server version `23.1` and above with Model Deployment feature enabled. |

```python python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.add_model_artifact(  
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir='model_dir/',
)
```