---
title: "fdl.ModelInfo"
slug: "fdlmodelinfo"
excerpt: "Stores information about a model."
hidden: false
createdAt: "2022-05-24T15:31:48.962Z"
updatedAt: "2022-08-16T13:53:57.407Z"
---
| Input Parameters                | Type                                 | Default | Description                                                                                                                                                                |
| :------------------------------ | :----------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| display_name                    | str                                  |         | A display name for the model.                                                                                                                                              |
| input_type                      | fdl.ModelInputType                   |         | A **ModelInputType** object containing the input type of the model.                                                                                                        |
| model_task                      | fdl.ModelTask                        |         | A **ModelTask** object containing the model task.                                                                                                                          |
| inputs                          | list                                 |         | A list of **Column** objects corresponding to the inputs (features) of the model.                                                                                          |
| outputs                         | list                                 |         | A list of **Column** objects corresponding to the outputs (predictions) of the model.                                                                                      |
| target_class_order              | Optional [list]                      | None    | A list denoting the order of classes in the target.                                                                                                                        |
| metadata                        | Optional [list]                      | None    | A list of **Column** objects corresponding to any metadata fields.                                                                                                         |
| decisions                       | Optional [list]                      | None    | A list of **Column** objects corresponding to any decision fields (post-prediction business decisions).                                                                    |
| targets                         | Optional [list]                      | None    | A list of **Column** objects corresponding to the targets (ground truth) of the model.                                                                                     |
| framework                       | Optional [str]                       | None    | A string providing information about the software library and version used to train and run this model.                                                                    |
| description                     | Optional [str]                       | None    | A description of the model.                                                                                                                                                |
| datasets                        | Optional [list]                      | None    | A list of the dataset IDs used by the model.                                                                                                                               |
| mlflow_params                   | Optional [fdl.MLFlowParams]          | None    | A **MLFlowParams** object containing information about MLFlow parameters.                                                                                                  |
| model_deployment_params         | Optional [fdl.ModelDeploymentParams] | None    | A **ModelDeploymentParams** object containing information about model deployment.                                                                                          |
| artifact_status                 | Optional [fdl.ArtifactStatus]        | None    | An **ArtifactStatus** object containing information about the model artifact.                                                                                              |
| preferred_explanation_method    | Optional [fdl.ExplanationMethod]     | None    | An **ExplanationMethod** object that specifies the default explanation algorithm to use for the model.                                                                     |
| custom_explanation_names        | Optional [list]                      | [ ]     | A list of names that can be passed to the _explanation_name \_argument of the optional user-defined \_explain_custom_ method of the model object defined in _package.py._  |
| binary_classification_threshold | Optional [float]                     | .5      | The threshold used for classifying inferences for binary classifiers.                                                                                                      |
| ranking_top_k                   | Optional [int]                       | 50      | Used only for ranking models. Sets the top _k_ results to take into consideration when computing performance metrics like MAP and NDCG.                                    |
| group_by                        | Optional [str]                       | None    | Used only for ranking models.  The column by which to group events for certain performance metrics like MAP and NDCG.                                                      |
| fall_back                       | Optional [dict]                      | None    | A dictionary mapping a column name to custom missing value encodings for that column.                                                                                      |
| \*\*kwargs                      |                                      |         | Additional arguments to be passed.                                                                                                                                         |

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