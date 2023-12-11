---
title: "fdl.DatasetInfo.from_dataframe"
slug: "fdldatasetinfofrom_dataframe"
excerpt: "Constructs a DatasetInfo object from a pandas DataFrame."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue May 24 2022 15:10:45 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters         | Type                       | Default | Description                                                                                                                                  |
| :----------------------- | :------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| df                       | Union [pd.Dataframe, list] |         | Either a single pandas DataFrame or a list of DataFrames. If a list is given, all dataframes must have the same columns.                     |
| display_name             | str                        | ' '     | A display_name for the dataset                                                                                                               |
| max_inferred_cardinality | Optional [int]             | 100     | If specified, any string column containing fewer than _max_inferred_cardinality_ unique values will be converted to a categorical data type. |
| dataset_id               | Optional [str]             | None    | The unique identifier for the dataset                                                                                                        |

```python Usage
import pandas as pd

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(df=df, max_inferred_cardinality=100)
```



| Return Type     | Description                                                                                      |
| :-------------- | :----------------------------------------------------------------------------------------------- |
| fdl.DatasetInfo | A [fdl.DatasetInfo()](ref:fdldatasetinfo) object constructed from the pandas Dataframe provided. |