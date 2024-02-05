---
title: "fdl.DatasetDataSource"
slug: "fdldatasetdatasource"
excerpt: "Indicates the dataset to use as a source data for explainability computations."
hidden: false
createdAt: "Wed Aug 30 2023 14:40:41 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 14 2023 15:05:02 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type           | Default | Description                                                                 |
| :-------------- | :------------- | :------ | :-------------------------------------------------------------------------- |
| dataset_id      | str            | None    | The unique identifier for the dataset.                                      |
| source          | Optional[str]  | None    | The source file name. If not specified, using all sources from the dataset. |
| num_samples     | Optional [int] | None    | Number of samples to select for computation.                                |

```python Usage
DATASET_ID = 'example_dataset'

data_source = fdl.DatasetDataSource(
    dataset_id=DATASET_ID
  	source='baseline.csv',
  	num_samples=500,
)
```
