---
title: "fdl.WeightingParams"
slug: "fdlweightingparams"
hidden: false
createdAt: "2022-07-06T13:41:14.177Z"
updatedAt: "2023-10-24T04:14:06.856Z"
---
Holds weighting information for class imbalanced models which can then be passed into a [fdl.ModelInfo](/reference/fdlmodelinfo) object. Please note that the use of weighting params requires the presence of model outputs in the baseline dataset.
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "class_weight",
    "0-1": "List[float]",
    "0-3": "List of floats representing weights for each of the classes. The length must equal the no. of classes.",
    "0-2": "None",
    "1-0": "weighted_reference_histograms",
    "1-1": "bool",
    "1-2": "True",
    "1-3": "Flag indicating if baseline histograms must be weighted or not when calculating drift metrics.",
    "2-0": "weighted_surrogate_training",
    "2-1": "bool",
    "2-2": "True",
    "2-3": "Flag indicating if weighting scheme should be used when training the surrogate model."
  },
  "cols": 4,
  "rows": 3
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\nimport sklearn.utils\nimport fiddler as fdl\n\ndf = pd.read_csv('example_dataset.csv')\ncomputed_weight = sklearn.utils.class_weight.compute_class_weight(\n        class_weight='balanced',\n        classes=np.unique(df[TARGET_COLUMN]),\n        y=df[TARGET_COLUMN]\n    ).tolist()\nweighting_params =  fdl.WeightingParams(class_weight=computed_weight)\ndataset_info = fdl.DatasetInfo.from_dataframe(df=df)\n\nmodel_info = fdl.ModelInfo.from_dataset_info(\n    dataset_info=dataset_info,\n    features=[\n        'feature_1',\n        'feature_2',\n        'feature_3'\n    ],\n    outputs=['output_column'],\n    target='target_column',\n    weighting_params=weighting_params,\n    input_type=fdl.ModelInputType.TABULAR,\n    model_task=fdl.ModelTask.BINARY_CLASSIFICATION\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]