---
title: "fdl.DatasetInfo"
slug: "fdldatasetinfo"
excerpt: "Stores information about a dataset."
hidden: false
createdAt: "Tue May 24 2022 15:05:38 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
For information on how to customize these objects, see [Customizing Your Dataset Schema](doc:customizing-your-dataset-schema).

| Input Parameters | Type            | Default | Description                                                                |
| :--------------- | :-------------- | :------ | :------------------------------------------------------------------------- |
| display_name     | str             | None    | A display name for the dataset.                                            |
| columns          | list            | None    | A list of **fdl.Column** objects containing information about the columns. |
| files            | Optional [list] | None    | A list of strings pointing to CSV files to use.                            |
| dataset_id       | Optional [str]  | None    | The unique identifier for the dataset                                      |
| \*\*kwargs       |                 |         | Additional arguments to be passed.                                         |

```python Usage
columns = [
    fdl.Column(
        name='feature_1',
        data_type=fdl.DataType.FLOAT
    ),
    fdl.Column(
        name='feature_2',
        data_type=fdl.DataType.INTEGER
    ),
    fdl.Column(
        name='feature_3',
        data_type=fdl.DataType.BOOLEAN
    ),
    fdl.Column(
        name='output_column',
        data_type=fdl.DataType.FLOAT
    ),
    fdl.Column(
        name='target_column',
        data_type=fdl.DataType.INTEGER
    )
]

dataset_info = fdl.DatasetInfo(
    display_name='Example Dataset',
    columns=columns
)
```
