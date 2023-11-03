---
title: "fdl.SqlSliceQueryDataSource"
slug: "fdlsqlslicequerydatasource"
excerpt: "Indicates the slice of data to use as a source data for explainability computations."
hidden: false
createdAt: "2023-08-30T14:40:59.522Z"
updatedAt: "2023-10-24T04:14:06.840Z"
---
| Input Parameter | Type           | Default | Description                                           |
| :-------------- | :------------- | :------ | :---------------------------------------------------- |
| query           | str            | None    | Slice query defining the data to use for computation. |
| num_samples     | Optional [int] | None    | Number of samples to select for computation.          |



```python Usage
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

query = f'SELECT * FROM {DATASET_ID}.{MODEL_ID} WHERE CreditScore > 700'
data_source = fdl.SqlSliceQueryDataSource(
    query=query,
  	num_samples=500,
)
```