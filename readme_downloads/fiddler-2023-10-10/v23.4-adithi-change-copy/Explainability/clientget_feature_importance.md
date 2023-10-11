---
title: "client.get_feature_importance"
slug: "clientget_feature_importance"
excerpt: "Get global feature importance for a model over a dataset or a slice."
hidden: true
createdAt: "2023-08-02T13:09:20.886Z"
updatedAt: "2023-08-02T13:27:05.387Z"
---
| Input Parameter | Type                                              | Default | Description                                                                                                      |
| :-------------- | :------------------------------------------------ | :------ | :--------------------------------------------------------------------------------------------------------------- |
| project_name    | str                                               | None    | The unique identifier for the project.                                                                           |
| model_name      | str                                               | None    | A unique identifier for the model.                                                                               |
| data_source     | Union[DatasetDataSource, SqlSliceQueryDataSource] | None    | DataSource for the input dataset to compute feature importance on (DatasetDataSource or SqlSliceQueryDataSource) |
| num_iterations  | Optional[int]                                     | None    | The maximum number of ablated model inferences per feature.                                                      |
| num_refs        | Optional[int]                                     | None    | Number of reference points used in the explanation.                                                              |
| ci_level        | Optional[float]                                   | None    | The confidence level (between 0 and 1).                                                                          |
| overwrite_cache | Optional[bool]                                    | False   | Whether to overwrite the cached values or not                                                                    |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

feature_importance = client.get_feature_impact(
    project_id=PROJECT_NAME,
    model_id=MODEL_NAME,
    data_source=DATASET_SOURCE
)
```

| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| tuple       | A named tuple with the feature impact results. |