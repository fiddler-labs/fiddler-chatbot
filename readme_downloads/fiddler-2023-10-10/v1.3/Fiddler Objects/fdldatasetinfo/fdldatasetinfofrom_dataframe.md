---
title: "fdl.DatasetInfo.from_dataframe"
slug: "fdldatasetinfofrom_dataframe"
excerpt: "Constructs a DatasetInfo object from a pandas DataFrame."
hidden: false
createdAt: "2022-05-24T15:10:45.704Z"
updatedAt: "2022-06-21T17:25:50.056Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "df",
    "0-1": "Union [pd.Dataframe, list]",
    "0-3": "Either a single pandas DataFrame or a list of DataFrames. If a list is given, all dataframes must have the same columns.",
    "1-0": "display_name",
    "1-1": "str",
    "1-2": "' '",
    "1-3": "A display_name for the dataset",
    "2-0": "max_inferred_cardinality",
    "2-1": "Optional [int]",
    "2-2": "None",
    "2-3": "If specified, any string column containing fewer than *max_inferred_cardinality* unique values will be converted to a categorical data type.",
    "3-0": "dataset_id",
    "3-1": "Optional [str]",
    "3-2": "None",
    "3-3": "The unique identifier for the dataset"
  },
  "cols": 4,
  "rows": 4
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)",
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
    "0-1": "A [fdl.DatasetInfo()](ref:fdldatasetinfo) object constructed from the pandas Dataframe provided."
  },
  "cols": 2,
  "rows": 1
}
[/block]