---
title: "Databricks Integration"
slug: "databricks-integration"
hidden: false
createdAt: "2023-02-02T20:38:54.971Z"
updatedAt: "2023-06-01T20:30:50.575Z"
---
Databricks is a web-based platform for working with Spark, that provides automated cluster management and IPython-style notebooks for data engineering and machine learning.

This guide will walk you through the process of getting data from Databricks tables into a _Pandas_ dataframe. Once you have a dataframe ready you can easily upload that data into Fiddler.

## Create the Dataframe in your Notebook

Start by creating a Notebook in your Databricks workspace. Databricks has a lot of pre-installed libraries like _Spark_ and _Pandas_. Using the Spark library you can interact with all your delta lake assets.

To get your data into a _Pandas_ dataframe use the following code snippet. Just replace `table_name` with your desired table in your Databricks environment.

```python
spark_dataframe = spark.read.table(table_name)
baseline_df = spark_dataframe.toPandas()
```

## Upload the Dataframe to Fiddler

Now that we have a dataframe, you are ready to upload it to Fiddler. You will need to do the following: 

1. [Authorize the Fiddler client](doc:authorizing-the-client)
2. [Create a Project ](ref:clientcreate_project)
3. [Upload the Baseline Dataset ](doc:uploading-a-baseline-dataset)

The following code snippet combines all the steps mentioned above

```python
!pip install -q fiddler-client
import fiddler as fdl
import pandas as pd

#set up fiddler client
URL = '' # Make sure to include the full URL (including https://). For example, https://abc.xyz.ai
ORG_ID = '' # Found in General section under the settings tab 
AUTH_TOKEN ='' # Found in the Credentials section under the settings tab 

# Initiate Fiddler client
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)

#create a project
PROJECT_ID = 'project_name'

client.create_project(PROJECT_ID)

#let Fiddler understand your data
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info

#Upload baseline dataset
DATASET_ID = 'dataset_name'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Your dataset should be available in Fiddler UI listed under the project you just created. Now you can onboard a model for this dataset.