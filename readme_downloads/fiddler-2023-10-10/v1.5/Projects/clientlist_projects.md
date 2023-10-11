---
title: "client.list_projects"
slug: "clientlist_projects"
excerpt: "Retrieves the project IDs of all projects accessible by the user."
hidden: false
createdAt: "2022-05-23T16:17:06.612Z"
updatedAt: "2022-06-21T17:23:09.184Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "list",
    "0-1": "A list containing the project ID string for each project."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "client.list_projects()",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "[\n  'project_a',\n  'project_b',\n  'project_c'\n]",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]