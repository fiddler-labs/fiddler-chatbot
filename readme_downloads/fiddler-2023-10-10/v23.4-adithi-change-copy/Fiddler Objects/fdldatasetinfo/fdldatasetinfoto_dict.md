---
title: "fdl.DatasetInfo.to_dict"
slug: "fdldatasetinfoto_dict"
excerpt: "Converts a DatasetInfo object to a dictionary."
hidden: false
createdAt: "2022-05-24T15:13:18.451Z"
updatedAt: "2022-10-31T14:43:53.121Z"
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