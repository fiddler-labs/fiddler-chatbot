---
title: "Customizing Your Dataset Schema"
slug: "customizing-your-dataset-schema"
hidden: false
createdAt: "2022-05-23T16:36:05.835Z"
updatedAt: "2022-05-23T16:36:05.835Z"
---
It's common to want to modify your [`fdl.DatasetInfo`](https://api.fiddler.ai/#fdl-datasetinfo) object in the case where **something was inferred incorrectly** by [`fdl.DatasetInfo.from_dataframe`](https://api.fiddler.ai/#fdl-datasetinfo-from_dataframe).

Let's walk through an example of how to do this.

***

Suppose you've loaded in a dataset as a pandas DataFrame.
[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\ndf = pd.read_csv('example_dataset.csv')",
      "language": "python"
    }
  ]
}
[/block]
Below is an example of what is displayed upon inspection.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/3ffd956-example_df_1.png",
        "example_df (1).png",
        444,
        325,
        "#f2f1f2"
      ]
    }
  ]
}
[/block]
***

Suppose you create a [`fdl.DatasetInfo`](https://api.fiddler.ai/#fdl-datasetinfo) object by inferring the details from this DataFrame.
[block:code]
{
  "codes": [
    {
      "code": "dataset_info = fdl.DatasetInfo.from_dataframe(df)",
      "language": "python"
    }
  ]
}
[/block]
Below is an example of what is displayed upon inspection.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/571f9e4-example_datasetinfo.png",
        "example_datasetinfo.png",
        939,
        521,
        "#f2f4f5"
      ]
    }
  ]
}
[/block]
But upon inspection, you notice **a few things are wrong**.

1. The [value range](#modifying-a-columns-value-range) of `output_column` is set to `[0.01, 0.99]`, when it should really be `[0.0, 1.0]`.
2. There are no [possible values](#modifying-a-columns-possible-values) set for `feature_3`.
3. The [data type](#modifying-a-columns-data-type) of `feature_3` is set to [`fdl.DataType.STRING`](https://api.fiddler.ai/#fdl-datatype), when it should really be [`fdl.DataType.CATEGORY`](https://api.fiddler.ai/#fdl-datatype).

Let's see how we can address these issues.
[block:api-header]
{
  "title": "Modifying a column’s value range"
}
[/block]
Let's say we want to modify the range of `output_column` in the above [`fdl.DatasetInfo`](https://api.fiddler.ai/#fdl-datasetinfo) object to be `[0.0, 1.0]`.

You can do this by setting the `value_range_min` and `value_range_max` of the `output_column` column.
[block:code]
{
  "codes": [
    {
      "code": "dataset_info['output_column'].value_range_min = 0.0\ndataset_info['output_column'].value_range_max = 1.0",
      "language": "python"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Modifying a column’s possible values"
}
[/block]
Let's say we want to modify the possible values of `feature_3` to be `['Yes', 'No']`.

You can do this by setting the `possible_values` of the `feature_3` column.
[block:code]
{
  "codes": [
    {
      "code": "dataset_info['feature_3'].possible_values = ['Yes', 'No']",
      "language": "python"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Modifying a column’s data type"
}
[/block]
Let's say we want to modify the data type of `feature_3` to be [`fdl.DataType.CATEGORY`](https://api.fiddler.ai/#fdl-datatype).

You can do this by setting the `data_type` of the `feature_3` column.
[block:code]
{
  "codes": [
    {
      "code": "dataset_info['feature_3'].data_type = fdl.DataType.CATEGORY",
      "language": "python"
    }
  ]
}
[/block]