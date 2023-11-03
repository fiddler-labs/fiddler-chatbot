---
title: "client.list_datasets"
slug: "clientlist_datasets"
excerpt: "Retrieves the dataset IDs of all datasets accessible within a project."
hidden: false
createdAt: "2022-05-23T16:42:07.246Z"
updatedAt: "2023-10-24T04:14:06.831Z"
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
      "code": "PROJECT_ID = \"example_project\"\n\nclient.list_datasets(\n    project_id=PROJECT_ID\n)",
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
      "code": "[\n    'dataset_a',\n    'dataset_b',\n    'dataset_c'\n]",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]