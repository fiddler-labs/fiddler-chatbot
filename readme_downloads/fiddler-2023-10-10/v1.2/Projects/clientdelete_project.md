---
title: "client.delete_project"
slug: "clientdelete_project"
excerpt: "Deletes a specified project."
hidden: false
createdAt: "2022-05-23T16:24:42.097Z"
updatedAt: "2022-06-21T17:23:16.713Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project."
  },
  "cols": 4,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\n\nclient.delete_project(\n    project_id=PROJECT_ID\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "bool",
    "0-1": "A boolean denoting whether deletion was successful."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "True",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]