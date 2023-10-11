---
title: "client.delete_dataset"
slug: "clientdelete_dataset"
excerpt: "Deletes a dataset from a project."
hidden: false
createdAt: "2022-05-23T19:00:39.913Z"
updatedAt: "2022-06-21T17:23:38.106Z"
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
    "0-3": "The unique identifier for the project.",
    "1-0": "dataset_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the dataset."
  },
  "cols": 4,
  "rows": 2
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\nclient.delete_dataset(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID\n)",
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
    "0-0": "str",
    "0-1": "A message confirming that the dataset was deleted."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "'Dataset deleted example_dataset'",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]