---
title: "Customizing Your Dataset Schema"
slug: "customizing-your-dataset-schema"
excerpt: ""
hidden: false
createdAt: "Mon May 23 2022 16:36:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
It's common to want to modify your [`fdl.DatasetInfo`](ref:fdldatasetinfo) object in the case where **something was inferred incorrectly** by [`fdl.DatasetInfo.from_dataframe`](ref:fdldatasetinfo).

Let's walk through an example of how to do this.

***

Suppose you've loaded in a dataset as a pandas DataFrame.

```python
import pandas as pd

df = pd.read_csv('example_dataset.csv')
```

Below is an example of what is displayed upon inspection.

![](https://files.readme.io/3ffd956-example_df_1.png "example_df (1).png")

***

Suppose you create a [`fdl.DatasetInfo`](ref:fdldatasetinfo) object by inferring the details from this DataFrame.

```python
dataset_info = fdl.DatasetInfo.from_dataframe(df)
```

Below is an example of what is displayed upon inspection.

![](https://files.readme.io/571f9e4-example_datasetinfo.png "example_datasetinfo.png")

But upon inspection, you notice **a few things are wrong**.

1. The [value range](doc:customizing-your-dataset-schema#modifying-a-columns-value-range) of `output_column` is set to `[0.01, 0.99]`, when it should really be `[0.0, 1.0]`.
2. There are no [possible values](doc:customizing-your-dataset-schema#modifying-a-columns-possible-values) set for `feature_3`.
3. The [data type](#modifying-a-columns-data-type) of `feature_3` is set to [`fdl.DataType.STRING`](ref:fdldatatype), when it should really be [`fdl.DataType.CATEGORY`](ref:fdldatatype).

Let's see how we can address these issues.

## Modifying a column’s value range

Let's say we want to modify the range of `output_column` in the above [`fdl.DatasetInfo`](ref:fdldatasetinfo) object to be `[0.0, 1.0]`.

You can do this by setting the `value_range_min` and `value_range_max` of the `output_column` column.

```python
dataset_info['output_column'].value_range_min = 0.0
dataset_info['output_column'].value_range_max = 1.0
```

## Modifying a column’s possible values

Let's say we want to modify the possible values of `feature_3` to be `['Yes', 'No']`.

You can do this by setting the `possible_values` of the `feature_3` column.

```python
dataset_info['feature_3'].possible_values = ['Yes', 'No']
```

## Modifying a column’s data type

Let's say we want to modify the data type of `feature_3` to be [`fdl.DataType.CATEGORY`](ref:fdldatatype).

You can do this by setting the `data_type` of the `feature_3` column.

```python
dataset_info['feature_3'].data_type = fdl.DataType.CATEGORY
```

> 🚧 Note when modifying a column's data type to Category
> 
> Note that it is also required when modifying a column's data type to Category to also set the column's possible_values to the list of unique values for that column.
> 
> dataset_info['feature_3'].data_type = fdl.DataType.CATEGORY  
> dataset_info['feature_3'].possible_values = ['Yes', 'No']
