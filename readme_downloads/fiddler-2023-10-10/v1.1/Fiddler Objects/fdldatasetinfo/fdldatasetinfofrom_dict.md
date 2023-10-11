---
title: "fdl.DatasetInfo.from_dict"
slug: "fdldatasetinfofrom_dict"
excerpt: "Converts a dictionary to a DatasetInfo object."
hidden: false
createdAt: "2022-05-24T15:15:40.271Z"
updatedAt: "2022-06-21T17:26:00.325Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "deserialized_json",
    "0-1": "dict",
    "0-3": "The dictionary object to be converted"
  },
  "cols": 4,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\ndataset_info_dict = dataset_info.to_dict()\n\nnew_dataset_info = fdl.DatasetInfo.from_dict(\n    deserialized_json={\n        'dataset': dataset_info_dict\n    }\n)",
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
    "0-1": "A [fdl.DatasetInfo()](ref:fdldatasetinfo) object constructed from the dictionary."
  },
  "cols": 2,
  "rows": 1
}
[/block]