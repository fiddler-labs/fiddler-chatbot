---
title: "client.get_mutual_information"
slug: "clientget_mutual_information"
excerpt: "Calculates the mutual information (MI) between variables over a specified dataset."
hidden: false
createdAt: "2022-05-23T21:14:37.148Z"
updatedAt: "2023-08-02T13:05:00.492Z"
---
| Input Parameter | Type            | Default | Description                                                                                                          |
| :-------------- | :-------------- | :------ | :------------------------------------------------------------------------------------------------------------------- |
| project_name    | str             | None    | The unique identifier for the project.                                                                               |
| project_name    | str             | None    | The unique identifier for the dataset.                                                                               |
| query           | str             | None    | A SQL query. If specified, mutual information will only be calculated over the dataset slice specified by the query. |
| column_name     | str             | None    | The column name to compute mutual information with respect to all the variables in the dataset.                      |
| normalized      | Optional [bool] | False   | If set to True, it will compute Normalized Mutual Information.                                                       |
| num_samples     | Optional [int]  | None    | Number of samples to select for computation.                                                                         |

```python Usage
PROJECT_NAME = 'example_project'
DATASET_NAME = 'example_dataset'

column_name = 'feature_1'

mutual_information = client.get_mutual_information(
    project_name=PROJECT_ID,
    dataset_name=DATASET_ID,
    column_name=column_name
)
```
```python Usage with SQL Query
PROJECT_NAME = 'example_project'
DATASET_NAME = 'example_dataset'

column_name = 'feature_1'

slice_query = f""" SELECT * FROM "{DATASET_ID}.{MODEL_ID}" WHERE feature_1 < 20.0 LIMIT 100 """

mutual_information = client.get_mutual_information(
    project_name=PROJECT_NAME,
    project_name=DATASET_NAME,
    column_name=column_name,
    query=slice_query
)
```

| Return Type | Description                                                                       |
| :---------- | :-------------------------------------------------------------------------------- |
| dict        | A dictionary of mutual information w.r.t the given feature for each column given. |