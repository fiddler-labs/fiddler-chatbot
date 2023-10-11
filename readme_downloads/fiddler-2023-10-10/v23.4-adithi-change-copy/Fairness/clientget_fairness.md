---
title: "client.get_fairness"
slug: "clientget_fairness"
excerpt: "Get fairness analysis on a dataset or a slice."
hidden: true
createdAt: "2023-08-02T13:34:22.318Z"
updatedAt: "2023-08-02T13:44:20.945Z"
---
| Input Parameter    | Type                                              | Default | Description                                                                                                        |
| :----------------- | :------------------------------------------------ | :------ | :----------------------------------------------------------------------------------------------------------------- |
| project_name       | str                                               | None    | The unique identifier for the project.                                                                             |
| model_name         | str                                               | None    | The unique identifier for the model.                                                                               |
| data_source        | Union[DatasetDataSource, SqlSliceQueryDataSource] | None    | DataSource for the input dataset to compute fairness on (DatasetDataSource or SqlSliceQueryDataSource).            |
| protected_features | list[str]                                         | None    | A list of protected features.                                                                                      |
| positive_outcome   | Union[str, int, float, bool]                      | None    | A SQL query. If specified, fairness metrics will only be calculated over the dataset slice specified by the query. |
| score_threshold    | Optional [float]                                  | 0.5     | The score threshold used to calculate model outcomes.                                                              |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

protected_features = [
    'feature_1',
    'feature_2'
]

positive_outcome = 1

fairness_metrics = client.get_fairness(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    protected_features=protected_features,
    positive_outcome=positive_outcome
)
```

| Return Type | Description                                      |
| :---------- | :----------------------------------------------- |
| dict        | A dictionary containing fairness metric results. |