---
title: "fdl.ModelDeployment"
slug: "fdlmodeldeployment"
excerpt: "Represents the model deployment"
hidden: true
createdAt: "2023-02-13T18:42:47.994Z"
updatedAt: "2023-02-21T19:35:01.049Z"
---
> Supported from server version `23.1` and above with Model Deployment feature enabled.

| Input Parameter   | Type              | Default | Description                                                               |
| :---------------- | :---------------- | :------ | :------------------------------------------------------------------------ |
| id                | int               | None    | Unique identifier for the model deployment - auto-incrementing integer    |
| uuid              | UUID              | None    | Unique identifier for the model deployment - UUID                         |
| organization_name | str               | None    | The unique identifier for the organization.                               |
| project_name      | str               | None    | The unique identifier for the project.                                    |
| model_name        | str               | None    | The unique identifier for the model.                                      |
| artifact_type     | str               | None    | Model artifact type (`SURROGATE` or `PYTHON_PACKAGE`)                     |
| deployment_type   | str               | None    | Type of deployment ( Only `BASE_CONTAINER` is supported)                  |
| active            | bool              | True    | Indicates if the deployment is active or not for this model.              |
| image_uri         | Optional[str]     | None    | Reference to the docker image to create a new runtime to serve the model. |
| replicas          | Optional[int]     | None    | The number of replicas running the model.                                 |
| cpu               | Optional[int]     | None    | The amount of CPU (milli cpus) reserved per replica.                      |
| memory            | Optional[int]     | None    | The amount of memory (mebibytes) reserved per replica.                    |
| created_by        | fdl.UserCompact   | None    | Who created this record                                                   |
| updated_by        | fdl.UserCompact   | None    | Who last updated the record                                               |
| created_at        | datetime.datetime | None    | When was this record created                                              |
| updated_at        | datetime.datetime | None    | When was this record last updated                                         |
| job_uuid          | Optional[UUID]    | None    | UUUID to fetch asynchronous job status                                    |

```python Usage
fdl.ModelDeployment(
  id=106548,
  uuid=UUID("123e4567-e89b-12d3-a456-426614174000"),
  model_name="MODEL_NAME",
  project_name="PROJECT_NAME",
  organization_name="ORGANIZATION_NAME",
  artifact_type="PYTHON_PACKAGE",
  deployment_type="BASE_CONTAINER",
  active=True,
  image_uri="md-base/python/machine-learning:1.0.0",
  replicas=1,
  cpu=250,
  memory=512,
  created_by=fdl.UserCompact(
    id=4839,
    full_name="first_name last_name",
    email="example_email@gmail.com",
  ),
  updated_by=fdl.UserCompact(
    id=4839,
    full_name="first_name last_name",
    email="example_email@gmail.com",
  ),
  created_at=datetime(2023, 1, 27, 10, 9, 39, 793829),
  updated_at=datetime(2023, 1, 30, 17, 3, 17, 813865),
  job_uuid=UUID("539j9630-a69b-98d5-g496-326117174805")
)
```



The `UserCompact` is only used for de-serializing the API response which has details of the user.