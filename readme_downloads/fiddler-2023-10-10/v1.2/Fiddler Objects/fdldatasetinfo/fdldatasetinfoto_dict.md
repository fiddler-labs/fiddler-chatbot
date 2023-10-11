---
title: "fdl.DatasetInfo.to_dict"
slug: "fdldatasetinfoto_dict"
excerpt: "Converts a DatasetInfo object to a dictionary."
hidden: false
createdAt: "2022-05-24T15:13:18.451Z"
updatedAt: "2022-06-21T17:25:55.571Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "dict",
    "0-1": "A dictionary containing information from the [fdl.DatasetInfo()](ref:fdldatasetinfo) object."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\ndataset_info_dict = dataset_info.to_dict()",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n    'name': 'Example Dataset',\n    'columns': [\n        {\n            'column-name': 'feature_1',\n            'data-type': 'float'\n        },\n        {\n            'column-name': 'feature_2',\n            'data-type': 'int'\n        },\n        {\n            'column-name': 'feature_3',\n            'data-type': 'bool'\n        },\n        {\n            'column-name': 'output_column',\n            'data-type': 'float'\n        },\n        {\n            'column-name': 'target_column',\n            'data-type': 'int'\n        }\n    ],\n    'files': []\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]