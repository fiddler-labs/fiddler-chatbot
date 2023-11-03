---
title: "client.create_project"
slug: "clientcreate_project"
excerpt: "Creates a project using the specified ID."
hidden: false
createdAt: "2022-05-23T16:21:29.485Z"
updatedAt: "2023-10-24T04:14:06.837Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "0-0": "project_id",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-1": "str",
    "0-2": "None",
    "0-3": "A unique identifier for the project. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character."
  },
  "cols": 4,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\n\nclient.create_project(\n    project_id=PROJECT_ID\n)",
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
    "0-0": "dict",
    "h-1": "Description",
    "0-1": "A dictionary mapping project_name to the project ID string specified, once the project is successfully created."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n    'project_name': 'example_project'\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]