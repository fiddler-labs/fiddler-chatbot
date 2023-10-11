---
title: "client.get_model_info"
slug: "clientget_model_info"
excerpt: "Retrieves the **ModelInfo** object associated with a model."
hidden: false
createdAt: "2022-05-23T19:40:10.877Z"
updatedAt: "2022-06-21T17:24:16.324Z"
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
    "0-3": "The unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character."
  },
  "cols": 4,
  "rows": 2
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\nmodel_info = client.get_model_info(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID\n)",
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
    "0-0": "fdl.ModelInfo",
    "0-1": "The **ModelInfo** object associated with the specified model."
  },
  "cols": 2,
  "rows": 1
}
[/block]