---
title: "fdl.DeploymentParams"
slug: "fdldeploymentparams"
excerpt: "Represents the deployment parameters for a model"
hidden: false
createdAt: "2023-01-11T22:32:19.679Z"
updatedAt: "2023-02-01T22:33:47.616Z"
---
> Supported from server version `23.1` and above with Model Deployment feature enabled.

| Input Parameter | Type          | Default | Description                                                           |
| :-------------- | :------------ | :------ | :-------------------------------------------------------------------- |
| image_uri       | Optional[str] | None    | Reference to docker image to create a new runtime to serve the model. |
| replicas        | Optional[int] | None    | The number of replicas running the model.                             |
| memory          | Optional[int] | None    | The amount of memory (mebibytes) reserved per replica.                |
| cpu             | Optional[int] | None    | The amount of CPU (milli cpus) reserved per replica.                  |

```python Usage
deployment_params = fdl.DeploymentParams(
        image_uri="md-base/python/machine-learning:1.0.0",
        cpu=250,
        memory=512,
  		  replicas=1,
)
```