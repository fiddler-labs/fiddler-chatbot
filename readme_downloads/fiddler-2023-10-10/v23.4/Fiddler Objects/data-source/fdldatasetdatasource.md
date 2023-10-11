---
title: "fdl.DatasetDataSource"
slug: "fdldatasetdatasource"
excerpt: "Indicates the dataset to use as a source data for explainability computations."
hidden: false
createdAt: "2023-08-30T14:40:41.216Z"
updatedAt: "2023-10-05T18:49:41.097Z"
---
| Input Parameter | Type           | Default | Description                                                                 |
| :-------------- | :------------- | :------ | :-------------------------------------------------------------------------- |
| dataset_name    | str            | None    | The unique identifier for the dataset.                                      |
| source          | Optional[str]  | None    | The source file name. If not specified, using all sources from the dataset. |
| num_samples     | Optional [int] | None    | Number of samples to select for computation.                                |



```python Usage
DATASET_ID = 'example_dataset'

data_source = fdl.DatasetDataSource(
    dataset_name=DATASET_ID
  	source='baseline.csv',
  	num_samples=500,
)
```