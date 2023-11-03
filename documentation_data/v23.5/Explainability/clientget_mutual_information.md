---
title: "client.get_mutual_information"
slug: "clientget_mutual_information"
excerpt: "Get Mutual Information for a dataset over a slice."
hidden: false
createdAt: "2023-08-30T14:27:43.783Z"
updatedAt: "2023-10-24T04:14:06.868Z"
---
| Input Parameter | Type           | Default | Description                                                                               |
| :-------------- | :------------- | :------ | :---------------------------------------------------------------------------------------- |
| project_id      | str            | None    | A unique identifier for the project.                                                      |
| dataset_id      | str            | None    | A unique identifier for the dataset.                                                      |
| query           | str            | None    | Slice query to compute Mutual information on.                                             |
| column_name     | str            | None    | Column name to compute mutual information with respect to all the columns in the dataset. |
| normalized      | Optional[bool] | False   | If set to True, it will compute Normalized Mutual Information.                            |
| num_samples     | Optional[int]  | 10000   | Number of samples to select for computation.                                              |

```python Usage
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

query = f'SELECT * FROM {DATASET_ID}.{MODEL_ID} WHERE CreditScore > 700'
mutual_info = client.get_mutual_information(
  project_id=PROJECT_ID,
  dataset_id=DATASET_ID,
  query=query,
  column_name='Geography',
  normalized=True,
  num_samples=20000,
)
```

| Return Type | Description                                       |
| :---------- | :------------------------------------------------ |
| dict        | A dictionary with the mutual information results. |