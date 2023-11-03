---
title: "client.share_project"
slug: "clientshare_project"
excerpt: "Shares a project with a user or team."
hidden: false
createdAt: "2022-05-25T15:28:34.938Z"
updatedAt: "2023-10-24T04:14:06.847Z"
---
[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "Administrators can share any project with any user. If you lack the required permissions to share a project, contact your organization administrator."
}
[/block]

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
    "1-3": "The permissions role being shared. Can be one of\n- 'READ'\n- 'WRITE'\n- 'OWNER'",
    "2-0": "user_name",
    "2-1": "Optional [str]",
    "2-2": "None",
    "2-3": "A username with which the project will be shared. Typically an email address.",
    "3-0": "team_name",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "A team with which the project will be shared."
  },
  "cols": 4,
  "rows": 4
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\n\nclient.share_project(\n    project_name=PROJECT_ID,\n    role='READ',\n    user_name='user@example.com'\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]