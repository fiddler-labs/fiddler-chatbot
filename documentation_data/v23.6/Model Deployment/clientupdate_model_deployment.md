---
title: "client.update_model_deployment"
slug: "clientupdate_model_deployment"
excerpt: "Fine-tune the model deployment based on the scaling requirements"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Thu Jan 26 2023 15:42:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type            | Default | Description                                                            |
| :-------------- | :-------------- | :------ | :--------------------------------------------------------------------- |
| project_id      | str             | None    | The unique identifier for the project.                                 |
| model_id        | str             | None    | The unique identifier for the model.                                   |
| active          | Optional [bool] | None    | Set `False` to scale down model deployment and `True` to scale up.     |
| replicas        | Optional[int]   | None    | The number of replicas running the model.                              |
| cpu             | Optional [int]  | None    | The amount of CPU (milli cpus) reserved per replica.                   |
| memory          | Optional [int]  | None    | The amount of memory (mebibytes) reserved per replica.                 |
| wait            | Optional[bool]  | True    | Whether to wait for the async job to finish (`True`) or not (`False`). |

## Example use cases:

- **Horizontal scaling**: horizontal scaling via replicas parameter. This will create multiple Kubernetes pods internally to handle requests.

  ```python
  PROJECT_NAME = 'example_project'
  MODEL_NAME = 'example_model'


  # Create 3 Kubernetes pods internally to handle requests
  client.update_model_deployment(
      project_id=PROJECT_NAME,
      model_id=MODEL_NAME,
      replicas=3,
  )
  ```

- **Vertical scaling**: Model deployments support vertical scaling via cpu and memory parameters. Some models might need more memory to load the artifacts into memory or process the requests.

  ```python
  PROJECT_NAME = 'example_project'
  MODEL_NAME = 'example_model'

  client.update_model_deployment(
      project_id=PROJECT_NAME,
    	model_id=MODEL_NAME,
      cpu=500,
      memory=1024,
  )
  ```

- **Scale down**: You may want to scale down the model deployments to avoid allocating the resources when the model is not in use. Use active parameters to scale down the deployment.

  ```python
  PROJECT_NAME = 'example_project'
  MODEL_NAME = 'example_model'

  client.update_model_deployment(
      project_id=PROJECT_NAME,
    	model_id=MODEL_NAME,
      active=False,
  )
  ```

- **Scale up**: This will again create the model deployment Kubernetes pods with the resource values available in the database.

  ```python
  PROJECT_NAME = 'example_project'
  MODEL_NAME = 'example_model'

  client.update_model_deployment(
      project_id=PROJECT_NAME,
    	model_id=MODEL_NAME,
      active=True,
  )
  ```

| Return Type | Description                                                        |
| :---------- | :----------------------------------------------------------------- |
| dict        | returns a dictionary, with all related fields for model deployment |

> Supported from server version `23.1` and above with Flexible Model Deployment feature enabled.

```python Response
{
  id: 106548,
  uuid: UUID("123e4567-e89b-12d3-a456-426614174000"),
  model_id: "MODEL_NAME",
  project_id : "PROJECT_NAME",
  organization_id: "ORGANIZATION_NAME",
  artifact_type: "PYTHON_PACKAGE",
  deployment_type: "BASE_CONTAINER",
  active: True,
  image_uri: "md-base/python/machine-learning:1.0.0",
  replicas: 1,
  cpu: 250,
  memory: 512,
  created_by: {
    id: 4839,
    full_name: "first_name last_name",
    email: "example_email@gmail.com",
  },
  updated_by: {
    id: 4839,
    full_name: "first_name last_name",
    email: "example_email@gmail.com",
  },
  created_at: datetime(2023, 1, 27, 10, 9, 39, 793829),
  updated_at: datetime(2023, 1, 30, 17, 3, 17, 813865),
  job_uuid: UUID("539j9630-a69b-98d5-g496-326117174805")
}
```