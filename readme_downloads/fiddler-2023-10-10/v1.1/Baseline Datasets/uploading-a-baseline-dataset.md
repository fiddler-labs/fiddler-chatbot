---
title: "Uploading a Baseline Dataset"
slug: "uploading-a-baseline-dataset"
hidden: false
createdAt: "2022-04-19T20:07:03.211Z"
updatedAt: "2022-06-08T15:32:37.948Z"
---
To upload a baseline dataset to Fiddler, you can use the [`client.upload_dataset`](https://api.fiddler.ai/#client-upload_dataset) API. Let's walk through a simple example of how this can be done.

***

The first step is to load your baseline dataset into a pandas DataFrame.
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

[block:api-header]
{
  "title": "Creating a DatasetInfo object"
}
[/block]
Then, you'll need to create a [fdl.DatasetInfo()](ref:fdldatasetinfo) object that can be used to **define the schema for your dataset**.

This schema can be inferred from your DataFrame using the [fdl.DatasetInfo.from_dataframe()](ref:fdldatasetinfofrom_dataframe) function.
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

[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "In the case that you have **categorical columns in your dataset that are encoded as strings**, you can use the `max_inferred_cardinality` argument.\n    \nThis argument specifies a threshold for unique values in a column. Any column with fewer than `max_inferred_cardinality` unique values will be converted to[fdl.DataType.CATEGORY](ref:fdldatatype)  type."
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": " dataset_info = fdl.DatasetInfo.from_dataframe(\n        df=df,\n        max_inferred_cardinality=1000\n    )",
      "language": "python"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Uploading your dataset"
}
[/block]
Once you have your [fdl.DatasetInfo()](ref:fdldatasetinfo) object, you can make any **necessary adjustments** before upload (see [Customizing Your Dataset Schema](doc:customizing-your-dataset-schema) ).

When you're ready, the dataset can be uploaded using [client.upload_dataset()](ref:clientupload_dataset).
[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\nclient.upload_dataset(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    dataset={\n        'baseline': df\n    },\n    info=dataset_info\n)",
      "language": "python"
    }
  ]
}
[/block]