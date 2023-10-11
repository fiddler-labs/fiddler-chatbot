---
title: "client.add_project"
slug: "clientadd_project"
excerpt: "Creates a project using the specified name."
hidden: true
createdAt: "2023-08-01T11:13:00.309Z"
updatedAt: "2023-08-01T13:40:38.235Z"
---
| Input Parameters | Type | Default | Description                                                                                                                                                                                                |
| :--------------- | :--- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_name     | str  | None    | A unique identifier for the project. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| project_id       | str  | None    | `Deprecated` A unique identifier for the project.                                                                                                                                                          |

```python Usage
PROJECT_NAME = 'example_project'

client.add_project(
    project_name=PROJECT_NAME
)
```

| Return Type | Description                                                                                                       |
| :---------- | :---------------------------------------------------------------------------------------------------------------- |
| dict        | A dictionary mapping project_name to the project name string specified, once the project is successfully created. |

```python Response
{
    'project_name': 'example_project'
}
```