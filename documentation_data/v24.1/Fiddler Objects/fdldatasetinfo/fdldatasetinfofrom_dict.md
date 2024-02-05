---
title: "fdl.DatasetInfo.from_dict"
slug: "fdldatasetinfofrom_dict"
excerpt: "Converts a dictionary to a DatasetInfo object."
hidden: false
createdAt: "Tue May 24 2022 15:15:40 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters  | Type | Default | Description                           |
| :---------------- | :--- | :------ | :------------------------------------ |
| deserialized_json | dict |         | The dictionary object to be converted |

```python Usage
import pandas as pd

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(df=df, max_inferred_cardinality=100)

dataset_info_dict = dataset_info.to_dict()

new_dataset_info = fdl.DatasetInfo.from_dict(
    deserialized_json={
        'dataset': dataset_info_dict
    }
)
```

| Return Type     | Description                                                                       |
| :-------------- | :-------------------------------------------------------------------------------- |
| fdl.DatasetInfo | A [fdl.DatasetInfo()](ref:fdldatasetinfo) object constructed from the dictionary. |
