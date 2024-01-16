---
title: "client.unshare_project"
slug: "clientunshare_project"
excerpt: "Unshares a project with a user or team."
hidden: false
createdAt: "Wed May 25 2022 15:29:55 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
> 📘 Info
> 
> Administrators and project owners can unshare any project with any user. If you lack the required permissions to unshare a project, contact your organization administrator.

[block:parameters]
{
  "data": {
    "h-0": "Input Paraemter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "role",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The permissions role being revoked. Can be one of  \n- 'READ'  \n- 'WRITE'  \n- 'OWNER'",
    "2-0": "user_name",
    "2-1": "Optional [str]",
    "2-2": "None",
    "2-3": "A username with which the project will be revoked. Typically an email address.",
    "3-0": "team_name",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "A team with which the project will be revoked."
  },
  "cols": 4,
  "rows": 4,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


```python Usage
PROJECT_ID = 'example_project'

client.unshare_project(
    project_name=PROJECT_ID,
    role='READ',
    user_name='user@example.com'
)
```
