---
title: "client.upload_dataset"
slug: "clientupload_dataset"
excerpt: "Uploads a dataset from a pandas DataFrame."
hidden: false
createdAt: "2022-05-23T18:58:49.880Z"
updatedAt: "2022-06-21T17:23:27.483Z"
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
    "1-0": "dataset",
    "1-1": "dict",
    "1-2": "None",
    "1-3": "A dictionary mapping dataset slice names to pandas DataFrames.",
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "A unique identifier for the dataset. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character.",
    "3-0": "info",
    "3-1": "Optional [fdl.DatasetInfo]",
    "3-3": "The Fiddler [fdl.DatasetInfo()](ref:fdldatasetinfo) object used to describe the dataset.",
    "3-2": "None",
    "4-0": "size_check_enabled",
    "4-1": "Optional [bool]",
    "4-2": "True",
    "4-3": "If True, will issue a warning when a dataset has a large number of rows."
  },
  "cols": 4,
  "rows": 5
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\nPROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\nclient.upload_dataset(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    dataset={\n        'baseline': df\n    },\n    info=dataset_info\n)",
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
    "0-0": "dict",
    "0-1": "A dictionary containing information about the uploaded dataset."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n  'row_count': 10000,\n  'col_count': 20,\n  'log': [\n    'Importing dataset example_dataset',\n    'Creating table for example_dataset',\n    'Importing data file: baseline.csv'\n  ]\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]