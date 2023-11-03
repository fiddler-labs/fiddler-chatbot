---
title: "fdl.Column"
slug: "fdlcolumn"
excerpt: "Represents a column of a dataset."
hidden: false
createdAt: "2022-05-25T15:03:57.235Z"
updatedAt: "2023-10-24T04:14:06.816Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "0-0": "name",
    "0-1": "str",
    "1-0": "data_type",
    "1-1": "[fdl.DataType](ref:fdldatatype)",
    "2-0": "possible_values",
    "3-0": "is_nullable",
    "2-1": "Optional [list]",
    "3-1": "Optional [bool]",
    "4-0": "value_range_min",
    "4-1": "Optional [float]",
    "h-2": "Default",
    "h-3": "Description",
    "0-2": "None",
    "0-3": "The name of the column",
    "1-2": "None",
    "1-3": "The [fdl.DataType](ref:fdldatatype) object corresponding to the data type of the column.",
    "2-2": "None",
    "2-3": "A list of unique values used for categorical columns.",
    "3-2": "None",
    "3-3": "If True, will expect missing values in the column.",
    "4-2": "None",
    "4-3": "The minimum value used for numeric columns.",
    "5-3": "The maximum value used for numeric columns.",
    "5-2": "None",
    "5-1": "Optional [float]",
    "5-0": "value_range_max"
  },
  "cols": 4,
  "rows": 6
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "column = fdl.Column(\n    name='feature_1',\n    data_type=fdl.DataType.FLOAT,\n    value_range_min=0.0,\n    value_range_max=80.0\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]