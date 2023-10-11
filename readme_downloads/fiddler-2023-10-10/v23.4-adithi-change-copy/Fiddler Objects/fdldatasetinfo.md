---
title: "fdl.DatasetInfo"
slug: "fdldatasetinfo"
excerpt: "Stores information about a dataset."
hidden: false
createdAt: "2022-05-24T15:05:38.736Z"
updatedAt: "2022-06-21T17:25:44.484Z"
---
For information on how to customize these objects, see [Customizing Your Dataset Schema](doc:customizing-your-dataset-schema).
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "display_name",
    "0-1": "str",
    "0-2": "None",
    "0-3": "A display name for the dataset.",
    "1-0": "columns",
    "1-1": "list",
    "1-2": "None",
    "1-3": "A list of **fdl.Column** objects containing information about the columns.",
    "2-0": "files",
    "2-1": "Optional [list]",
    "2-2": "None",
    "2-3": "A list of strings pointing to CSV files to use.",
    "3-0": "dataset_id",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "The unique identifier for the dataset",
    "4-0": "**kwargs",
    "4-3": "Additional arguments to be passed."
  },
  "cols": 4,
  "rows": 5
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "columns = [\n    fdl.Column(\n        name='feature_1',\n        data_type=fdl.DataType.FLOAT\n    ),\n    fdl.Column(\n        name='feature_2',\n        data_type=fdl.DataType.INTEGER\n    ),\n    fdl.Column(\n        name='feature_3',\n        data_type=fdl.DataType.BOOLEAN\n    ),\n    fdl.Column(\n        name='output_column',\n        data_type=fdl.DataType.FLOAT\n    ),\n    fdl.Column(\n        name='target_column',\n        data_type=fdl.DataType.INTEGER\n    )\n]\n\ndataset_info = fdl.DatasetInfo(\n    display_name='Example Dataset',\n    columns=columns\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]