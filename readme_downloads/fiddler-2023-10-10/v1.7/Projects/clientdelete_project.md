---
title: "client.delete_project"
slug: "clientdelete_project"
excerpt: "Deletes a specified project."
hidden: false
createdAt: "2022-05-23T16:24:42.097Z"
updatedAt: "2023-06-07T17:32:38.037Z"
---
| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_id       | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = 'example_project'

client.delete_project(
    project_id=PROJECT_ID
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