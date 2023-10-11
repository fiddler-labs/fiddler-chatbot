---
title: "client.get_fairness"
slug: "clientget_fairness"
excerpt: "Get fairness analysis on a dataset or a slice."
hidden: false
createdAt: "2023-08-16T11:16:57.636Z"
updatedAt: "2023-10-06T19:22:17.806Z"
---
> 🚧 
> 
> Only Binary classification models with categorical protected attributes are currently supported.

| Input Parameter    | Type                                                                                                                     | Default | Description                                                                                             |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------ |
| project_id         | str                                                                                                                      | None    | The unique identifier for the project.                                                                  |
| model_id           | str                                                                                                                      | None    | The unique identifier for the model.                                                                    |
| data_source        | Union\[[fdl.DatasetDataSource](ref:fdldatasetdatasource), [fdl.SqlSliceQueryDataSource](ref:fdlsqlslicequerydatasource)] | None    | DataSource for the input dataset to compute fairness on (DatasetDataSource or SqlSliceQueryDataSource). |
| protected_features | list[str]                                                                                                                | None    | A list of protected features.                                                                           |
| positive_outcome   | Union[str, int, float, bool]                                                                                             | None    | Value of the positive outcome (from the target column) for Fairness analysis.                           |
| score_threshold    | Optional [float]                                                                                                         | 0.5     | The score threshold used to calculate model outcomes.                                                   |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'

# Fairness - Dataset data source
fairness_metrics = client.get_fairness(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=200),
    protected_features=['feature_1', 'feature_2'],
    positive_outcome='Approved',
    score_threshold=0.6
)

# Fairness - Slice Query data source
query = f'SELECT * FROM {DATASET_ID}.{MODEL_ID} WHERE CreditSCore > 700'
fairness_metrics = client.get_fairness(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.SqlSliceQueryDataSource(query=query, num_samples=200),
    protected_features=['feature_1', 'feature_2'],
    positive_outcome='Approved',
    score_threshold=0.6
)
```

| Return Type | Description                                      |
| :---------- | :----------------------------------------------- |
| dict        | A dictionary containing fairness metric results. |