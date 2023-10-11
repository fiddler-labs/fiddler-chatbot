---
title: "client.run_fairness"
slug: "clientrun_fairness"
excerpt: "Calculates fairness metrics for a model over a specified dataset."
hidden: false
createdAt: "2022-05-25T15:16:38.209Z"
updatedAt: "2023-08-02T13:35:27.580Z"
---
Get fairness metrics for a model over a dataset.

> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Use _client.get_dataset_names()_ instead.  
> Reference: [client.get_fairness](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_fairness)get_explanation

| Input Parameter    | Type             | Default | Description                                                                                                        |
| :----------------- | :--------------- | :------ | :----------------------------------------------------------------------------------------------------------------- |
| project_id         | str              | None    | The unique identifier for the project.                                                                             |
| model_id           | str              | None    | The unique identifier for the model.                                                                               |
| dataset_id         | str              | None    | The unique identifier for the dataset.                                                                             |
| protected_features | list             | None    | A list of protected features.                                                                                      |
| positive_outcome   | Union [str, int] | None    | The name or value of the positive outcome for the model.                                                           |
| slice_query        | Optional [str]   | None    | A SQL query. If specified, fairness metrics will only be calculated over the dataset slice specified by the query. |
| score_threshold    | Optional [float] | 0.5     | The score threshold used to calculate model outcomes.                                                              |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'

protected_features = [
    'feature_1',
    'feature_2'
]

positive_outcome = 1

fairness_metrics = client.run_fairness(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    dataset_id=DATASET_ID,
    protected_features=protected_features,
    positive_outcome=positive_outcome
)
```
```python Usage - With a SQL Query
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'

protected_features = [
    'feature_1',
    'feature_2'
]

positive_outcome = 1

slice_query = f""" SELECT * FROM "{DATASET_ID}.{MODEL_ID}" WHERE feature_1 < 20.0 LIMIT 100 """

fairness_metrics = client.run_fairness(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    dataset_id=DATASET_ID,
    protected_features=protected_features,
    positive_outcome=positive_outcome,
    slice_query=slice_query
)
```

| Return Type | Description                                      |
| :---------- | :----------------------------------------------- |
| dict        | A dictionary containing fairness metric results. |