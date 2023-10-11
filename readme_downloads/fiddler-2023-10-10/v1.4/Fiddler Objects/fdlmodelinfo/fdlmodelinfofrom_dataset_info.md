---
title: "fdl.ModelInfo.from_dataset_info"
slug: "fdlmodelinfofrom_dataset_info"
excerpt: "Constructs a ModelInfo object from a DatasetInfo object."
hidden: false
createdAt: "2022-05-24T15:49:32.351Z"
updatedAt: "2022-08-16T13:54:51.240Z"
---
| Input Parameters                 | Type                                    | Default                    | Description                                                                                                                                                                |
| :------------------------------- | :-------------------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dataset_info                     | [fdl.DatasetInfo()](ref:fdldatasetinfo) |                            | The **DatasetInfo** object from which to construct the **ModelInfo** object.                                                                                               |
| target                           | str                                     |                            | The column to be used as the target (ground truth).                                                                                                                        |
| dataset_id                       | Optional [str]                          | None                       | The unique identifier for the dataset.                                                                                                                                     |
| features                         | Optional [list]                         | None                       | A list of columns to be used as features.                                                                                                                                  |
| metadata_cols                    | Optional [list]                         | None                       | A list of columns to be used as metadata fields.                                                                                                                           |
| decision_cols                    | Optional [list]                         | None                       | A list of columns to be used as decision fields.                                                                                                                           |
| display_name                     | Optional [str]                          | None                       | A display name for the model.                                                                                                                                              |
| description                      | Optional [str]                          | None                       | A description of the model.                                                                                                                                                |
| input_type                       | Optional [fdl.ModelInputType]           | fdl.ModelInputType.TABULAR | A **ModelInputType** object containing the input type of the model.                                                                                                        |
| model_task                       | Optional [fdl.ModelTask]                | None                       | A **ModelTask** object containing the model task.                                                                                                                          |
| outputs                          | Optional [list]                         |                            | A list of **Column** objects corresponding to the outputs (predictions) of the model.                                                                                      |
| categorical_target_class_details | Optional [list]                         | None                       | Only for multiclass classification models.  A list denoting the order of classes in the target.                                                                            |
| model_deployment_params          | Optional [fdl.ModelDeploymentParams]    | None                       | A **ModelDeploymentParams** object containing information about model deployment.                                                                                          |
| target_class_order               | Optional [list]                         | None                       | A list denoting the order of classes in the target.                                                                                                                        |
| targets                          | Optional [list]                         | None                       | A list of **Column** objects corresponding to the targets (ground truth) of the model.                                                                                     |
| framework                        | Optional [str]                          | None                       | A string providing information about the software library and version used to train and run this model.                                                                    |
| datasets                         | Optional [list]                         | None                       | A list of the dataset IDs used by the model.                                                                                                                               |
| mlflow_params                    | Optional [fdl.MLFlowParams]             | None                       | A **MLFlowParams** object containing information about MLFlow parameters.                                                                                                  |
| model_deployment_params          | Optional [fdl.ModelDeploymentParams]    | None                       | A **ModelDeploymentParams** object containing information about model deployment.                                                                                          |
| preferred_explanation_method     | Optional [fdl.ExplanationMethod]        | None                       | An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.                                                                     |
| custom_explanation_names         | Optional [list]                         | [ ]                        | A list of names that can be passed to the _explanation_name \_argument of the optional user-defined \_explain_custom_ method of the model object defined in _package.py._  |
| binary_classification_threshold  | Optional [float]                        | .5                         | The threshold used for classifying inferences for binary classifiers.                                                                                                      |
| ranking_top_k                    | Optional [int]                          | 50                         | Used only for ranking models. Sets the top _k_ results to take into consideration when computing performance metrics like MAP and NDCG.                                    |
| group_by                         | Optional [str]                          | None                       | Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.                                                      |
| fall_back                        | Optional [dict]                         | None                       | A dictionary mapping a column name to custom missing value encodings for that column.                                                                                      |

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