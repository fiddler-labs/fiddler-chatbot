---
title: "fdl.Column"
slug: "fdlcolumn"
excerpt: "Represents a column of a dataset."
hidden: false
createdAt: "Wed May 25 2022 15:03:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type                            | Default | Description                                                                              |
| :-------------- | :------------------------------ | :------ | :--------------------------------------------------------------------------------------- |
| name            | str                             | None    | The name of the column                                                                   |
| data_type       | [fdl.DataType](ref:fdldatatype) | None    | The [fdl.DataType](ref:fdldatatype) object corresponding to the data type of the column. |
| possible_values | Optional [list]                 | None    | A list of unique values used for categorical columns.                                    |
| is_nullable     | Optional [bool]                 | None    | If True, will expect missing values in the column.                                       |
| value_range_min | Optional [float]                | None    | The minimum value used for numeric columns.                                              |
| value_range_max | Optional [float]                | None    | The maximum value used for numeric columns.                                              |

```python Usage
column = fdl.Column(
    name='feature_1',
    data_type=fdl.DataType.FLOAT,
    value_range_min=0.0,
    value_range_max=80.0
)
```
