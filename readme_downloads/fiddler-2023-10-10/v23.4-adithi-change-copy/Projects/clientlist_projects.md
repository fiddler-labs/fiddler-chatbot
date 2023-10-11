---
title: "client.list_projects"
slug: "clientlist_projects"
excerpt: "Retrieves the project IDs of all projects accessible by the user."
hidden: false
createdAt: "2022-05-23T16:17:06.612Z"
updatedAt: "2023-08-01T11:55:34.414Z"
---
> 🚧 Deprecated
> 
> This client method is deprecated and will be removed in the future versions. Use _client.get_project_names()_ instead.  
> Reference: [client.get_project_names](https://dash.readme.com/project/fiddler/v23.4/refs/client-get_project_names)

```python Usage
response = client.list_projects()
```

| Return Type | Description                                                 |
| :---------- | :---------------------------------------------------------- |
| list        | A list containing the project names string for each project |

```python Response
[
  'project_a',
  'project_b',
  'project_c'
]
```