---
title: "fdl.ModelInfo.to_dict"
slug: "fdlmodelinfoto_dict"
excerpt: "Converts a Model object to a dictionary."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue May 24 2022 15:54:52 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "dict",
    "0-1": "A dictionary containing information from the [fdl.ModelInfo()](ref:fdlmodelinfo) object."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\nmodel_info = fdl.ModelInfo.from_dataset_info(\n    dataset_info=dataset_info,\n    features=[\n        'feature_1',\n        'feature_2',\n        'feature_3'\n    ],\n    outputs=[\n        'output_column'\n    ],\n    target='target_column',\n    input_type=fdl.ModelInputType.TABULAR,\n    model_task=fdl.ModelTask.BINARY_CLASSIFICATION\n)\n\nmodel_info_dict = model_info.to_dict()",
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
      "code": "{\n    'name': 'Example Model',\n    'input-type': 'structured',\n    'model-task': 'binary_classification',\n    'inputs': [\n        {\n            'column-name': 'feature_1',\n            'data-type': 'float'\n        },\n        {\n            'column-name': 'feature_2',\n            'data-type': 'int'\n        },\n        {\n            'column-name': 'feature_3',\n            'data-type': 'bool'\n        },\n        {\n            'column-name': 'target_column',\n            'data-type': 'int'\n        }\n    ],\n    'outputs': [\n        {\n            'column-name': 'output_column',\n            'data-type': 'float'\n        }\n    ],\n    'datasets': [],\n    'targets': [\n        {\n            'column-name': 'target_column',\n            'data-type': 'int'\n        }\n    ],\n    'custom-explanation-names': []\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]