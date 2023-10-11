---
title: "client.create_project"
slug: "clientcreate_project"
excerpt: "Creates a project using the specified name."
hidden: false
createdAt: "2022-05-23T16:21:29.485Z"
updatedAt: "2023-08-01T11:55:28.391Z"
---
> 🚧 Deprecated
> 
> This client method is deprecated and will be removed in the future versions. Use _client.add_project()_ instead.  
> Reference: [client.add_project](https://dash.readme.com/project/fiddler/v23.4/refs/clientadd_project)

| Input Parameters | Type | Default | Description                                                                                                                                                                                                |
| :--------------- | :--- | :------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id       | str  | None    | A unique identifier for the project. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |

```python Usage
PROJECT_ID = 'example_project'

client.create_project(
    project_id=PROJECT_ID
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