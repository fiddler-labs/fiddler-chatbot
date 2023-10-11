---
title: "fdl.ModelInfo"
slug: "fdlmodelinfo"
excerpt: "Stores information about a model."
hidden: false
createdAt: "2022-05-24T15:31:48.962Z"
updatedAt: "2022-06-21T17:26:08.375Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "display_name",
    "0-1": "str",
    "0-3": "A display name for the model.",
    "1-0": "input_type",
    "1-1": "fdl.ModelInputType",
    "1-3": "A **ModelInputType** object containing the input type of the model.",
    "2-0": "model_task",
    "2-1": "fdl.ModelTask",
    "2-3": "A **ModelTask** object containing the model task.",
    "3-0": "inputs",
    "3-1": "list",
    "3-3": "A list of **Column** objects corresponding to the inputs (features) of the model.",
    "4-0": "outputs",
    "4-1": "list",
    "4-3": "A list of **Column** objects corresponding to the outputs (predictions) of the model.",
    "5-0": "target_class_order",
    "5-1": "Optional [list]",
    "5-2": "None",
    "5-3": "A list denoting the order of classes in the target.",
    "6-1": "Optional [list]",
    "7-1": "Optional [list]",
    "9-1": "Optional [str]",
    "8-1": "Optional [list]",
    "10-1": "Optional [str]",
    "11-1": "Optional [list]",
    "6-0": "metadata",
    "7-0": "decisions",
    "8-0": "targets",
    "9-0": "framework",
    "10-0": "description",
    "11-0": "datasets",
    "6-2": "None",
    "7-2": "None",
    "8-2": "None",
    "9-2": "None",
    "10-2": "None",
    "11-2": "None",
    "6-3": "A list of **Column** objects corresponding to any metadata fields.",
    "7-3": "A list of **Column** objects corresponding to any decision fields (post-prediction business decisions).",
    "8-3": "A list of **Column** objects corresponding to the targets (ground truth) of the model.",
    "9-3": "A string providing information about the software library and version used to train and run this model.",
    "10-3": "A description of the model.",
    "11-3": "A list of the dataset IDs used by the model.",
    "12-0": "mlflow_params",
    "12-1": "Optional [fdl.MLFlowParams]",
    "12-3": "A **MLFlowParams** object containing information about MLFlow parameters.",
    "12-2": "None",
    "13-0": "model_deployment_params",
    "13-1": "Optional [fdl.ModelDeploymentParams]",
    "13-2": "None",
    "13-3": "A **ModelDeploymentParams** object containing information about model deployment.",
    "14-0": "artifact_status",
    "14-1": "Optional [fdl.ArtifactStatus]",
    "14-2": "None",
    "14-3": "An **ArtifactStatus** object containing information about the model artifact.",
    "15-0": "preferred_explanation_method",
    "15-1": "Optional [fdl.ExplanationMethod]",
    "15-2": "None",
    "15-3": "An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.",
    "16-0": "custom_explanation_names",
    "16-1": "Optional [list]",
    "16-2": "[ ]",
    "16-3": "A list of names that can be passed to the *explanation_name *argument of the optional user-defined *explain_custom* method of the model object defined in *package.py.* ",
    "17-0": "binary_classification_threshold",
    "17-1": "Optional [float]",
    "17-2": ".5",
    "17-3": "The threshold used for classifying inferences for binary classifiers.",
    "18-0": "ranking_top_k",
    "18-1": "Optional [int]",
    "18-2": "50",
    "18-3": "Used only for ranking models. Sets the top *k* results to take into consideration when computing performance metrics like MAP and NDCG.",
    "19-0": "group_by",
    "19-1": "Optional [str]",
    "19-2": "None",
    "19-3": "Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.",
    "20-0": "**kwargs",
    "20-3": "Additional arguments to be passed."
  },
  "cols": 4,
  "rows": 21
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "inputs = [\n    fdl.Column(\n        name='feature_1',\n        data_type=fdl.DataType.FLOAT\n    ),\n    fdl.Column(\n        name='feature_2',\n        data_type=fdl.DataType.INTEGER\n    ),\n    fdl.Column(\n        name='feature_3',\n        data_type=fdl.DataType.BOOLEAN\n    )\n]\n\noutputs = [\n    fdl.Column(\n        name='output_column',\n        data_type=fdl.DataType.FLOAT\n    )\n]\n\ntargets = [\n    fdl.Column(\n        name='target_column',\n        data_type=fdl.DataType.INTEGER\n    )\n]\n\nmodel_info = fdl.ModelInfo(\n    display_name='Example Model',\n    input_type=fdl.ModelInputType.TABULAR,\n    model_task=fdl.ModelTask.BINARY_CLASSIFICATION,\n    inputs=inputs,\n    outputs=outputs,\n    targets=targets\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]