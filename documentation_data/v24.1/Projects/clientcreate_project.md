---
title: "client.create_project"
slug: "clientcreate_project"
excerpt: "Creates a project using the specified ID."
hidden: false
createdAt: "Mon May 23 2022 16:21:29 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters | Type | Default | Description                                                                                                                                                                                                |
| :--------------- | :--- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id       | str  | None    | A unique identifier for the project. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |

```python Usage
PROJECT_ID = 'example_project'

client.create_project(
    project_id=PROJECT_ID
)
```

| Return Type | Description                                                                                                     |
| :---------- | :-------------------------------------------------------------------------------------------------------------- |
| dict        | A dictionary mapping project_name to the project ID string specified, once the project is successfully created. |

```python Response
{
    'project_name': 'example_project'
}
```
