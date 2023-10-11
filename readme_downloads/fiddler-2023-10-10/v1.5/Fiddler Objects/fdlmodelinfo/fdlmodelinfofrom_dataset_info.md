---
title: "fdl.ModelInfo.from_dataset_info"
slug: "fdlmodelinfofrom_dataset_info"
excerpt: "Constructs a ModelInfo object from a DatasetInfo object."
hidden: false
createdAt: "2023-02-08T16:34:44.810Z"
updatedAt: "2023-02-08T17:24:23.102Z"
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
    "0-2": "",
    "0-3": "The **DatasetInfo** object from which to construct the **ModelInfo** object.",
    "1-0": "target",
    "1-1": "str",
    "1-2": "",
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
    "8-0": "input_type",
    "8-1": "Optional [fdl.ModelInputType]",
    "8-2": "fdl.ModelInputType.TABULAR",
    "8-3": "A **ModelInputType** object containing the input type of the model.",
    "9-0": "model_task",
    "9-1": "Optional [fdl.ModelTask]",
    "9-2": "None",
    "9-3": "A **ModelTask** object containing the model task.",
    "10-0": "outputs",
    "10-1": "Optional [list]",
    "10-2": "",
    "10-3": "A list of **Column** objects corresponding to the outputs (predictions) of the model.",
    "11-0": "targets",
    "11-1": "Optional [list]",
    "11-2": "None",
    "11-3": "A list of **Column** objects corresponding to the targets (ground truth) of the model.",
    "12-0": "model_deployment_params",
    "12-1": "Optional [fdl.ModelDeploymentParams]",
    "12-2": "None",
    "12-3": "A **ModelDeploymentParams** object containing information about model deployment.",
    "13-0": "framework",
    "13-1": "Optional [str]",
    "13-2": "None",
    "13-3": "A string providing information about the software library and version used to train and run this model.",
    "14-0": "datasets",
    "14-1": "Optional [list]",
    "14-2": "None",
    "14-3": "A list of the dataset IDs used by the model.",
    "15-0": "mlflow_params",
    "15-1": "Optional [fdl.MLFlowParams]",
    "15-2": "None",
    "15-3": "A **MLFlowParams** object containing information about MLFlow parameters.",
    "16-0": "preferred_explanation_method",
    "16-1": "Optional [fdl.ExplanationMethod]",
    "16-2": "None",
    "16-3": "An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.",
    "17-0": "custom_explanation_names",
    "17-1": "Optional [list]",
    "17-2": "[ ]",
    "17-3": "A list of names that can be passed to the _explanation_name \\_argument of the optional user-defined \\_explain_custom_ method of the model object defined in _package.py._",
    "18-0": "binary_classification_threshold",
    "18-1": "Optional [float]",
    "18-2": ".5",
    "18-3": "The threshold used for classifying inferences for binary classifiers.",
    "19-0": "ranking_top_k",
    "19-1": "Optional [int]",
    "19-2": "50",
    "19-3": "Used only for ranking models. Sets the top _k_ results to take into consideration when computing performance metrics like MAP and NDCG.",
    "20-0": "group_by",
    "20-1": "Optional [str]",
    "20-2": "None",
    "20-3": "Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.",
    "21-0": "fall_back",
    "21-1": "Optional [dict]",
    "21-2": "None",
    "21-3": "A dictionary mapping a column name to custom missing value encodings for that column.",
    "22-0": "categorical_target_class_details",
    "22-1": "Optional \\[Union[list, int, str]]",
    "22-2": "None",
    "22-3": "A list denoting the order of classes in the target. This parameter is **required** in the following cases:  \n  \n_- Binary classification tasks_: If the **target** is of type _string_, you must tell Fiddler which class is considered the positive class for your **output** column. If you provide a single element, it is considered the positive class. Alternatively, you can provide a list with two elements. The 0th element by convention is considered the negative class, and the 1st element is considered the positive class.  When your **target** is _boolean_, you don't need to specify this argument. By default Fiddler considers `True` as the positive class. In case your target is _numerical_, you don't need to  specify this argument, by default Fiddler considers the higher of the two possible values as the positive class.  \n  \n- _Multi-class classification tasks_: You must tell Fiddler which class corresponds to which output by giving an ordered list of classes. This order should be the same as the order of the outputs.  \n  \n- _Ranking tasks_: If the target is of type _string_, you must provide a list of all the possible target values in the order of relevance. The first element will be considered as the least relevant grade and the last element from the list will be considered the most relevant grade.  \nIn the case your target is _numerical_, Fiddler considers the smallest value to be the least relevant grade and the biggest value from the list will be considered the most relevant grade."
  },
  "cols": 4,
  "rows": 23,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
import pandas as pd

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(
    df=df
)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    features=[
        'feature_1',
        'feature_2',
        'feature_3'
    ],
    outputs=[
        'output_column'
    ],
    target='target_column',
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.BINARY_CLASSIFICATION
)
```



| Return Type   | Description                                                                                                                |
| :------------ | :------------------------------------------------------------------------------------------------------------------------- |
| fdl.ModelInfo | A [fdl.ModelInfo()](ref:fdlmodelinfo) object constructed from the [fdl.DatasetInfo()](ref:fdldatasetinfo) object provided. |