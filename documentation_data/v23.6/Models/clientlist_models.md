---
title: "client.list_models"
slug: "clientlist_models"
excerpt: "Retrieves the model IDs of all models accessible within a project."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 19:06:21 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "0-0": "project_id",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
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
      "code": "PROJECT_ID = 'example_project'\n\nclient.list_models(\n    project_id=PROJECT_ID\n)",
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
    "0-0": "list",
    "0-1": "A list containing the string ID of each model."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "[\n    'model_a',\n    'model_b',\n    'model_c'\n]",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]