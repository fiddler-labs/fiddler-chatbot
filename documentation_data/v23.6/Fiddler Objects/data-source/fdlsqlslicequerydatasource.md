---
title: "fdl.SqlSliceQueryDataSource"
slug: "fdlsqlslicequerydatasource"
excerpt: "Indicates the slice of data to use as a source data for explainability computations."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed Aug 30 2023 14:40:59 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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