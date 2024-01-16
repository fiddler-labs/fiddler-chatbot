---
title: "fdl.DatasetInfo.to_dict"
slug: "fdldatasetinfoto_dict"
excerpt: "Converts a DatasetInfo object to a dictionary."
hidden: false
createdAt: "Tue May 24 2022 15:13:18 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Return Type | Description                                                                                  |
| :---------- | :------------------------------------------------------------------------------------------- |
| dict        | A dictionary containing information from the [fdl.DatasetInfo()](ref:fdldatasetinfo) object. |

```python Usage
import pandas as pd

df = pd.read_csv('example_dataset.csv')

dataset_info = fdl.DatasetInfo.from_dataframe(df=df, max_inferred_cardinality=100)

dataset_info_dict = dataset_info.to_dict()
```

```python Response
{
    'name': 'Example Dataset',
    'columns': [
        {
            'column-name': 'feature_1',
            'data-type': 'float'
        },
        {
            'column-name': 'feature_2',
            'data-type': 'int'
        },
        {
            'column-name': 'feature_3',
            'data-type': 'bool'
        },
        {
            'column-name': 'output_column',
            'data-type': 'float'
        },
        {
            'column-name': 'target_column',
            'data-type': 'int'
        }
    ],
    'files': []
}
```
