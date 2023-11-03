---
title: "client.list_projects"
slug: "clientlist_projects"
excerpt: "Retrieves the project IDs of all projects accessible by the user."
hidden: false
createdAt: "2022-05-23T16:17:06.612Z"
updatedAt: "2023-10-24T04:14:06.826Z"
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