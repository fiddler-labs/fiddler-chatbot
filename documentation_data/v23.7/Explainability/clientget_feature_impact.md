---
title: "client.get_feature_impact"
slug: "clientget_feature_impact"
excerpt: "Get global feature impact for a model over a dataset or a slice."
hidden: false
createdAt: "Wed Aug 16 2023 11:23:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type                                                                                                                     | Default | Description                                                                                                                                                                      |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id      | str                                                                                                                      | None    | A unique identifier for the project.                                                                                                                                             |
| model_id        | str                                                                                                                      | None    | A unique identifier for the model.                                                                                                                                               |
| data_source     | Union\[[fdl.DatasetDataSource](ref:fdldatasetdatasource), [fdl.SqlSliceQueryDataSource](ref:fdlsqlslicequerydatasource)] | None    | Type of data source for the input dataset to compute feature impact on (DatasetDataSource or SqlSliceQueryDataSource)                                                            |
| num_iterations  | Optional[int]                                                                                                            | 10000   | The maximum number of ablated model inferences per feature. Used for TABULAR data only.                                                                                          |
| num_refs        | Optional[int]                                                                                                            | 10000   | Number of reference points used in the explanation. Used for TABULAR data only.                                                                                                  |
| ci_level        | Optional[float]                                                                                                          | 0.95    | The confidence level (between 0 and 1). Used for TABULAR data only.                                                                                                              |
| output_columns  | Optional\[List[str]]                                                                                                     | None    | Only used for NLP (TEXT inputs) models. Output column names to compute feature impact on. Useful for Multi-class Classification models. If None, compute for all output columns. |
| min_support     | Optional[int]                                                                                                            | 15      | Only used for NLP (TEXT inputs) models. Specify a minimum support (number of times a specific word was present in the sample data) to retrieve top words. Default to 15.         |
| overwrite_cache | Optional[bool]                                                                                                           | False   | Whether to overwrite the feature impact cached values or not.                                                                                                                    |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'

# Feature Impact for TABULAR data - Dataset Data Source
feature_impact = client.get_feature_impact(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=200),
    num_iterations=300,
    num_refs=200,
    ci_level=0.90,
)

# Feature Impact for TABULAR data - Slice Query data source
query = f'SELECT * FROM {DATASET_ID}.{MODEL_ID} WHERE CreditScore > 700'
feature_impact = client.get_feature_impact(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.SqlSliceQueryDataSource(query=query, num_samples=80),
    num_iterations=300,
    num_refs=200,
    ci_level=0.90,
)

# Feature Impact for TEXT data
feature_impact = client.get_feature_impact(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=50),
    output_columns= ['probability_A', 'probability_B'],
  	min_support=30
)
```

| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| tuple       | A named tuple with the feature impact results. |
