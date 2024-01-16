---
title: "client.get_feature_importance"
slug: "clientget_feature_importance"
excerpt: "Get global feature importance for a model over a dataset or a slice."
hidden: false
createdAt: "Wed Aug 16 2023 11:25:39 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type                                                                                                                     | Default | Description                                                                                                               |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------ |
| project_id      | str                                                                                                                      | None    | A unique identifier for the project.                                                                                      |
| model_id        | str                                                                                                                      | None    | A unique identifier for the model.                                                                                        |
| data_source     | Union\[[fdl.DatasetDataSource,](ref:fdldatasetdatasource) [fdl.SqlSliceQueryDataSource](ref:fdlsqlslicequerydatasource)] | None    | Type of data source for the input dataset to compute feature importance on (DatasetDataSource or SqlSliceQueryDataSource) |
| num_iterations  | Optional[int]                                                                                                            | 10000   | The maximum number of ablated model inferences per feature.                                                               |
| num_refs        | Optional[int]                                                                                                            | 10000   | Number of reference points used in the explanation.                                                                       |
| ci_level        | Optional[float]                                                                                                          | 0.95    | The confidence level (between 0 and 1).                                                                                   |
| overwrite_cache | Optional[bool]                                                                                                           | False   | Whether to overwrite the feature importance cached values or not                                                          |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'


# Feature Importance - Dataset data source
feature_importance = client.get_feature_importance(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=200),
    num_iterations=300,
    num_refs=200,
    ci_level=0.90,
)

# Feature Importance - Slice Query data source
query = f'SELECT * FROM {DATASET_ID}.{MODEL_ID} WHERE CreditScore > 700'
feature_importance = client.get_feature_importance(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.SqlSliceQueryDataSource(query=query, num_samples=80),
    num_iterations=300,
    num_refs=200,
    ci_level=0.90,
)
```

| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| tuple       | A named tuple with the feature impact results. |
