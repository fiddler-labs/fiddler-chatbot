---
title: "fdl.ModelInfo"
slug: "fdlmodelinfo"
excerpt: "Stores information about a model."
hidden: false
createdAt: "2023-02-08T17:05:23.795Z"
updatedAt: "2023-02-08T17:30:30.316Z"
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
    "0-2": "",
    "0-3": "A display name for the model.",
    "1-0": "input_type",
    "1-1": "fdl.ModelInputType",
    "1-2": "",
    "1-3": "A **ModelInputType** object containing the input type of the model.",
    "2-0": "model_task",
    "2-1": "fdl.ModelTask",
    "2-2": "",
    "2-3": "A **ModelTask** object containing the model task.",
    "3-0": "inputs",
    "3-1": "list",
    "3-2": "",
    "3-3": "A list of **Column** objects corresponding to the inputs (features) of the model.",
    "4-0": "outputs",
    "4-1": "list",
    "4-2": "",
    "4-3": "A list of **Column** objects corresponding to the outputs (predictions) of the model.",
    "5-0": "metadata",
    "5-1": "Optional [list]",
    "5-2": "None",
    "5-3": "A list of **Column** objects corresponding to any metadata fields.",
    "6-0": "decisions",
    "6-1": "Optional [list]",
    "6-2": "None",
    "6-3": "A list of **Column** objects corresponding to any decision fields (post-prediction business decisions).",
    "7-0": "targets",
    "7-1": "Optional [list]",
    "7-2": "None",
    "7-3": "A list of **Column** objects corresponding to the targets (ground truth) of the model.",
    "8-0": "framework",
    "8-1": "Optional [str]",
    "8-2": "None",
    "8-3": "A string providing information about the software library and version used to train and run this model.",
    "9-0": "description",
    "9-1": "Optional [str]",
    "9-2": "None",
    "9-3": "A description of the model.",
    "10-0": "datasets",
    "10-1": "Optional [list]",
    "10-2": "None",
    "10-3": "A list of the dataset IDs used by the model.",
    "11-0": "mlflow_params",
    "11-1": "Optional [fdl.MLFlowParams]",
    "11-2": "None",
    "11-3": "A **MLFlowParams** object containing information about MLFlow parameters.",
    "12-0": "model_deployment_params",
    "12-1": "Optional [fdl.ModelDeploymentParams]",
    "12-2": "None",
    "12-3": "A **ModelDeploymentParams** object containing information about model deployment.",
    "13-0": "artifact_status",
    "13-1": "Optional [fdl.ArtifactStatus]",
    "13-2": "None",
    "13-3": "An **ArtifactStatus** object containing information about the model artifact.",
    "14-0": "preferred_explanation_method",
    "14-1": "Optional [fdl.ExplanationMethod]",
    "14-2": "None",
    "14-3": "An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.",
    "15-0": "custom_explanation_names",
    "15-1": "Optional [list]",
    "15-2": "[ ]",
    "15-3": "A list of names that can be passed to the _explanation_name \\_argument of the optional user-defined \\_explain_custom_ method of the model object defined in _package.py._",
    "16-0": "binary_classification_threshold",
    "16-1": "Optional [float]",
    "16-2": ".5",
    "16-3": "The threshold used for classifying inferences for binary classifiers.",
    "17-0": "ranking_top_k",
    "17-1": "Optional [int]",
    "17-2": "50",
    "17-3": "Used only for ranking models. Sets the top _k_ results to take into consideration when computing performance metrics like MAP and NDCG.",
    "18-0": "group_by",
    "18-1": "Optional [str]",
    "18-2": "None",
    "18-3": "Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.",
    "19-0": "fall_back",
    "19-1": "Optional [dict]",
    "19-2": "None",
    "19-3": "A dictionary mapping a column name to custom missing value encodings for that column.",
    "20-0": "target_class_order",
    "20-1": "Optional [list]",
    "20-2": "None",
    "20-3": "A list denoting the order of classes in the target. This parameter is **required** in the following cases:  \n  \n_- Binary classification tasks_: If the **target** is of type _string_, you must tell Fiddler which class is considered the positive class for your **output** column. You need to provide a list with two elements. The 0th element by convention is considered the negative class, and the 1st element is considered the positive class.  When your **target** is _boolean_, you don't need to specify this argument. By default Fiddler considers `True` as the positive class. In case your target is _numerical_, you don't need to  specify this argument, by default Fiddler considers the higher of the two possible values as the positive class.  \n  \n- _Multi-class classification tasks_: You must tell Fiddler which class corresponds to which output by giving an ordered list of classes. This order should be the same as the order of the outputs.  \n  \n- _Ranking tasks_: If the target is of type _string_, you must provide a list of all the possible target values in the order of relevance. The first element will be considered as the least relevant grade and the last element from the list will be considered the most relevant grade.  \n In the case your target is _numerical_, Fiddler considers the smallest value to be the least relevant grade and the biggest value from the list will be considered the most relevant grade.",
    "21-0": "\\*\\*kwargs",
    "21-1": "",
    "21-2": "",
    "21-3": "Additional arguments to be passed."
  },
  "cols": 4,
  "rows": 22,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
inputs = [
    fdl.Column(
        name='feature_1',
        data_type=fdl.DataType.FLOAT
    ),
    fdl.Column(
        name='feature_2',
        data_type=fdl.DataType.INTEGER
    ),
    fdl.Column(
        name='feature_3',
        data_type=fdl.DataType.BOOLEAN
    )
]

outputs = [
    fdl.Column(
        name='output_column',
        data_type=fdl.DataType.FLOAT
    )
]

targets = [
    fdl.Column(
        name='target_column',
        data_type=fdl.DataType.INTEGER
    )
]

model_info = fdl.ModelInfo(
    display_name='Example Model',
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.BINARY_CLASSIFICATION,
    inputs=inputs,
    outputs=outputs,
    targets=targets
)
```