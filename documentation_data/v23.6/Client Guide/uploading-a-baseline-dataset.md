---
title: "Uploading a Baseline Dataset"
slug: "uploading-a-baseline-dataset"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:07:03 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
To upload a baseline dataset to Fiddler, you can use the [`client.upload_dataset`](ref:clientupload_dataset) API. Let's walk through a simple example of how this can be done.

***

The first step is to load your baseline dataset into a pandas DataFrame.

```python
import pandas as pd

df = pd.read_csv('example_dataset.csv')
```

## Creating a DatasetInfo object

Then, you'll need to create a [fdl.DatasetInfo()](ref:fdldatasetinfo) object that can be used to **define the schema for your dataset**.

This schema can be inferred from your DataFrame using the [fdl.DatasetInfo.from_dataframe()](ref:fdldatasetinfofrom_dataframe) function.

```python
dataset_info = fdl.DatasetInfo.from_dataframe(df)
```

> 📘 Info
> 
> In the case that you have **categorical columns in your dataset that are encoded as strings**, you can use the `max_inferred_cardinality` argument.
> 
> This argument specifies a threshold for unique values in a column. Any column with fewer than `max_inferred_cardinality` unique values will be converted to [fdl.DataType.CATEGORY](ref:fdldatatype)  type.

```python
dataset_info = fdl.DatasetInfo.from_dataframe(
        df=df,
        max_inferred_cardinality=1000
    )
```

## Uploading your dataset

Once you have your [fdl.DatasetInfo()](ref:fdldatasetinfo) object, you can make any **necessary adjustments** before upload (see [Customizing Your Dataset Schema](doc:customizing-your-dataset-schema) ).

When you're ready, the dataset can be uploaded using [client.upload_dataset()](ref:clientupload_dataset).

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': df
    },
    info=dataset_info
)
```