---
title: "client.delete_project"
slug: "clientdelete_project"
excerpt: "Deletes a specified project."
hidden: false
createdAt: "Mon May 23 2022 16:24:42 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
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
