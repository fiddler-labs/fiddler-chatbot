---
title: "client.list_projects"
slug: "clientlist_projects"
excerpt: "Retrieves the project IDs of all projects accessible by the user."
hidden: false
createdAt: "2022-05-23T16:17:06.612Z"
updatedAt: "2023-03-08T20:45:14.289Z"
---
```python Usage
response = client.list_projects()
```



| Return Type | Description                                              |
| :---------- | :------------------------------------------------------- |
| list        | A list containing the project ID string for each project |

```python Response
[
  'project_a',
  'project_b',
  'project_c'
]
```