---
title: "client.get_dataset_info"
slug: "clientget_dataset_info"
excerpt: "Retrieves the DatasetInfo object associated with a dataset."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Mon May 23 2022 19:02:48 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\ndataset_info = client.get_dataset_info(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID\n)",
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
    "0-0": "fdl.DatasetInfo",
    "0-1": "The [fdl.DatasetInfo()](ref:fdldatasetinfo) object associated with the specified dataset."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "#NA",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]