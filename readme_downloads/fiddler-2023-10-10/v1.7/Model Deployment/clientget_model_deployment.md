---
title: "client.get_model_deployment"
slug: "clientget_model_deployment"
excerpt: "Get model deployment object"
hidden: false
createdAt: "2023-01-26T15:42:31.316Z"
updatedAt: "2023-03-01T19:25:57.932Z"
---
| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |
| model_id        | str  | None    | The unique identifier for the model.   |

```python
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

client.get_model_deployment(
    project_id=PROJECT_NAME,
    model_id=MODEL_NAME,
)
```



| Return Type | Description                                                            |
| :---------- | :--------------------------------------------------------------------- |
| dict        | returns a dictionary, with all related fields for the model deployment |

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