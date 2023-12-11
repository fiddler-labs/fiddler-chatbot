---
title: "client.list_projects"
slug: "clientlist_projects"
excerpt: "Retrieves the project IDs of all projects accessible by the user."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 16:17:06 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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