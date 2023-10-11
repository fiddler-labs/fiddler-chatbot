---
title: "fdl.ModelInfo.from_dataset_info"
slug: "fdlmodelinfofrom_dataset_info"
excerpt: "Constructs a ModelInfo object from a DatasetInfo object."
hidden: false
createdAt: "2022-05-24T15:49:32.351Z"
updatedAt: "2022-06-21T17:26:17.050Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "dataset_info",
    "0-1": "[fdl.DatasetInfo()](ref:fdldatasetinfo)",
    "0-3": "The **DatasetInfo** object from which to construct the **ModelInfo** object.",
    "8-0": "input_type",
    "8-1": "Optional [fdl.ModelInputType]",
    "8-3": "A **ModelInputType** object containing the input type of the model.",
    "9-0": "model_task",
    "9-1": "Optional [fdl.ModelTask]",
    "9-3": "A **ModelTask** object containing the model task.",
    "10-0": "outputs",
    "10-1": "Optional [list]",
    "10-3": "A list of **Column** objects corresponding to the outputs (predictions) of the model.",
    "13-0": "target_class_order",
    "13-1": "Optional [list]",
    "13-2": "None",
    "13-3": "A list denoting the order of classes in the target.",
    "15-1": "Optional [str]",
    "14-1": "Optional [list]",
    "16-1": "Optional [list]",
    "14-0": "targets",
    "15-0": "framework",
    "16-0": "datasets",
    "14-2": "None",
    "15-2": "None",
    "16-2": "None",
    "14-3": "A list of **Column** objects corresponding to the targets (ground truth) of the model.",
    "15-3": "A string providing information about the software library and version used to train and run this model.",
    "16-3": "A list of the dataset IDs used by the model.",
    "17-0": "mlflow_params",
    "17-1": "Optional [fdl.MLFlowParams]",
    "17-3": "A **MLFlowParams** object containing information about MLFlow parameters.",
    "17-2": "None",
    "18-0": "model_deployment_params",
    "18-1": "Optional [fdl.ModelDeploymentParams]",
    "18-2": "None",
    "18-3": "A **ModelDeploymentParams** object containing information about model deployment.",
    "19-0": "preferred_explanation_method",
    "19-1": "Optional [fdl.ExplanationMethod]",
    "19-2": "None",
    "19-3": "An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.",
    "20-0": "custom_explanation_names",
    "20-1": "Optional [list]",
    "20-2": "[ ]",
    "20-3": "A list of names that can be passed to the *explanation_name *argument of the optional user-defined *explain_custom* method of the model object defined in *package.py.* ",
    "21-0": "binary_classification_threshold",
    "21-1": "Optional [float]",
    "21-2": ".5",
    "21-3": "The threshold used for classifying inferences for binary classifiers.",
    "22-0": "ranking_top_k",
    "22-1": "Optional [int]",
    "22-2": "50",
    "22-3": "Used only for ranking models. Sets the top *k* results to take into consideration when computing performance metrics like MAP and NDCG.",
    "23-0": "group_by",
    "23-1": "Optional [str]",
    "23-2": "None",
    "23-3": "Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.",
    "1-0": "target",
    "1-1": "str",
    "1-3": "The column to be used as the target (ground truth).",
    "2-0": "dataset_id",
    "2-1": "Optional [str]",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "3-0": "features",
    "3-1": "Optional [list]",
    "3-2": "None",
    "3-3": "A list of columns to be used as features.",
    "4-0": "metadata_cols",
    "4-1": "Optional [list]",
    "4-2": "None",
    "4-3": "A list of columns to be used as metadata fields.",
    "5-0": "decision_cols",
    "5-1": "Optional [list]",
    "5-2": "None",
    "5-3": "A list of columns to be used as decision fields.",
    "6-0": "display_name",
    "6-1": "Optional [str]",
    "6-2": "None",
    "6-3": "A display name for the model.",
    "7-0": "description",
    "7-1": "Optional [str]",
    "7-2": "None",
    "7-3": "A description of the model.",
    "8-2": "fdl.ModelInputType.TABULAR",
    "9-2": "None",
    "11-0": "categorical_target_class_details",
    "11-1": "Optional [list]",
    "11-2": "None",
    "11-3": "Only for multiclass classification models.  A list denoting the order of classes in the target.",
    "12-0": "model_deployment_params",
    "12-1": "Optional [fdl.ModelDeploymentParams]",
    "12-2": "None",
    "12-3": "A **ModelDeploymentParams** object containing information about model deployment."
  },
  "cols": 4,
  "rows": 24
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')\n\ndataset_info = fdl.DatasetInfo.from_dataframe(\n    df=df\n)\n\nmodel_info = fdl.ModelInfo.from_dataset_info(\n    dataset_info=dataset_info,\n    features=[\n        'feature_1',\n        'feature_2',\n        'feature_3'\n    ],\n    outputs=[\n        'output_column'\n    ],\n    target='target_column',\n    input_type=fdl.ModelInputType.TABULAR,\n    model_task=fdl.ModelTask.BINARY_CLASSIFICATION\n)",
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
    "0-1": "A [fdl.ModelInfo()](ref:fdlmodelinfo) object constructed from the [fdl.DatasetInfo()](ref:fdldatasetinfo) object provided."
  },
  "cols": 2,
  "rows": 1
}
[/block]