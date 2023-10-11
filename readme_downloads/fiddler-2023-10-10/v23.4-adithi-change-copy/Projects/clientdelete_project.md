---
title: "client.delete_project"
slug: "clientdelete_project"
excerpt: "Deletes a specified project."
hidden: false
createdAt: "2022-05-23T16:24:42.097Z"
updatedAt: "2023-08-01T11:25:31.519Z"
---
| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_name     | str  | None    | The unique identifier for the project. |
| project_id       | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_NAME = 'example_project'

client.delete_project(
    project_name=PROJECT_NAME
)
```

| Return Type | Description                                         |
| :---------- | :-------------------------------------------------- |
| bool        | A boolean denoting whether deletion was successful. |

```python Response
True
```



> 🚧 Caution
> 
> You cannot delete a project without deleting the datasets and the models associated with that project.