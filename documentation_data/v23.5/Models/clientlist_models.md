---
title: "client.list_models"
slug: "clientlist_models"
excerpt: "Retrieves the model IDs of all models accessible within a project."
hidden: false
createdAt: "2022-05-23T19:06:21.547Z"
updatedAt: "2023-10-24T04:14:06.870Z"
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