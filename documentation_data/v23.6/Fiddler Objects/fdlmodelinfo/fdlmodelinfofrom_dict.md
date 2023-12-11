---
title: "fdl.ModelInfo.from_dict"
slug: "fdlmodelinfofrom_dict"
excerpt: "Converts a dictionary to a ModelInfo object."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue May 24 2022 15:56:13 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\nmodel_info = fdl.ModelInfo.from_dataset_info(\n    dataset_info=dataset_info,\n    features=[\n        'feature_1',\n        'feature_2',\n        'feature_3'\n    ],\n    outputs=[\n        'output_column'\n    ],\n    target='target_column',\n    input_type=fdl.ModelInputType.TABULAR,\n    model_task=fdl.ModelTask.BINARY_CLASSIFICATION\n)\n\nmodel_info_dict = model_info.to_dict()\n\nnew_model_info = fdl.ModelInfo.from_dict(\n    deserialized_json={\n        'model': model_info_dict\n    }\n)",
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
    "0-1": "A [fdl.ModelInfo()](ref:fdlmodelinfo) object constructed from the dictionary."
  },
  "cols": 2,
  "rows": 1
}
[/block]