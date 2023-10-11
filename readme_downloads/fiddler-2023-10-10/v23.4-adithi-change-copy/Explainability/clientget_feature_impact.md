---
title: "client.get_feature_impact"
slug: "clientget_feature_impact"
excerpt: "Get global feature impact for a model over a dataset or a slice."
hidden: true
createdAt: "2023-08-02T13:08:22.817Z"
updatedAt: "2023-08-02T13:26:44.970Z"
---
| Input Parameter | Type                                              | Default | Description                                                                                                                                                              |
| :-------------- | :------------------------------------------------ | :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_name    | str                                               | None    | The unique identifier for the project.                                                                                                                                   |
| model_name      | str                                               | None    | A unique identifier for the model.                                                                                                                                       |
| data_source     | Union[DatasetDataSource, SqlSliceQueryDataSource] | None    | DataSource for the input dataset to compute feature importance on (DatasetDataSource or SqlSliceQueryDataSource)                                                         |
| num_iterations  | Optional[int]                                     | None    | The maximum number of ablated model inferences per feature.                                                                                                              |
| num_refs        | Optional[int]                                     | None    | Number of reference points used in the explanation.                                                                                                                      |
| ci_level        | Optional[float]                                   | None    | The confidence level (between 0 and 1).                                                                                                                                  |
| output_columns  | Optional\[List[str]]                              | None    | Only used for NLP (TEXT inputs) models. Output column names to compute feature impact on.                                                                                |
| min_support     | Optional[int]                                     | None    | Only used for NLP (TEXT inputs) models. Specify a minimum support (number of times a specific word was present in the sample data) to retrieve top words. Default to 15. |
| overwrite_cache | Optional[bool]                                    | False   | Whether to overwrite the cached values or not                                                                                                                            |

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