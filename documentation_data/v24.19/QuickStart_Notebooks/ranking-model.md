---
title: ML Monitoring - Ranking
slug: ranking-model
excerpt: ''
metadata:
  title: 'Quickstart: Ranking Monitoring | Fiddler Docs'
  description: >-
    This document explains how Fiddler enables monitoring for a Ranking model
    using a dataset from Expedia that includes shopping and purchase data with
    information on price competitiveness.
  robots: index
icon: notebook
---

# ML Monitoring - Ranking

This notebook will show you how Fiddler enables monitoring for a Ranking model. This notebook uses a public dataset from Expedia that includes shopping and purchase data with information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Ranking_Model.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Ranking_Model.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Fiddler Ranking Model Quick Start Guide

Fiddler enables your teams to monitor and evaluate model rankings, providing insights into model performance and detecting issues like data drift before they impact your applications.

### Example: Expedia Search Ranking
The following dataset contains Expedia shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

1. Connect to Fiddler
2. Load a Data Sample
3. Define the Model Specifications and Model Task
4. Create a Model
5. Publish a Pre-production Baseline
6. Publish Production Events

## 0. Imports


```python
%pip install -q fiddler-client

import time as time

import pandas as pd
import fiddler as fdl

print(f"Running Fiddler Python client version {fdl.__version__}")
```

## 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using the Fiddler Python client.


---


**We need a couple pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your authorization token

Your authorization token can be found by navigating to the **Credentials** tab on the **Settings** page of your Fiddler environment.


```python
URL = ''  # Make sure to include the full URL (including https:// e.g. 'https://your_company_name.fiddler.ai').
TOKEN = ''
```

Constants for this example notebook, change as needed to create your own versions


```python
# Constants for the default example, change as needed to create your own versions
PROJECT_NAME = 'quickstart_examples'
MODEL_NAME = 'search_ranking_example'
DATASET_NAME = 'expedia_dataset'

PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/expedia_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/expedia_logs.csv'
```

Next we use these credentials to connect to the Fiddler API.


```python
fdl.init(url=URL, token=TOKEN)
```

Once you connect, you can create a new project by specifying a unique project name in the fld.Project constructor and calling the `create()` method. If the project already exists, it will load it for use.


```python
try:
    # Create project
    project = fdl.Project(name=PROJECT_NAME).create()
    print(f'New project created with id = {project.id} and name = {project.name}')
except fdl.Conflict:
    # Get project by name
    project = fdl.Project.from_name(name=PROJECT_NAME)
    print(f'Loaded existing project with id = {project.id} and name = {project.name}')
```

## 2. Load a Data Sample

Now we retrieve the Expedia Dataset as a data sample for this model.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df.head()
```

Fiddler uses this data sample to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

## 3. Define the Model Specifications and Model Task

To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `target_class_order` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
model_spec = fdl.ModelSpec(
    inputs=list(
        sample_data_df.drop(
            columns=[
                'binary_relevance',
                'score',
                'graded_relevance',
                'position',
                'timestamp',
            ]
        ).columns
    ),
    outputs=['score'],
    targets=['binary_relevance'],
    metadata=['timestamp', 'graded_relevance', 'position'],
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model in step 5.


```python
# id_column = '' # Optional: Specify the name of the ID column if you have one
timestamp_column = 'timestamp'
```


```python
model_task = fdl.ModelTask.RANKING

task_params = fdl.ModelTaskParams(
    group_by='srch_id', top_k=20, target_class_order=[0, 1]
)
```

## 4. Create a Model


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params,
    event_ts_col=timestamp_column,
)

model.create()
print(f'New model created with id = {model.id} and name = {model.name}')
```

## 5. Publish a Pre-production Baseline **(Optional)**

We can publish the data sample from earlier to add it as a baseline.

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `group_by` utility function to perform this transformation.


```python
sample_df_grouped = fdl.utils.helpers.group_by(
    df=sample_data_df, group_by_col='srch_id'
)

baseline_publish_job = model.publish(
    source=sample_df_grouped,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=DATASET_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job.id}'
)

# Uncomment the line below to wait for the job to finish, otherwise it will run in the background.
# You can check the status on the Jobs page in the Fiddler UI or use the job ID to query the job status via the API.
# baseline_publish_job.wait()
```

# 6. Publish Events For Monitoring

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.


---


Each record sent to Fiddler is called **an event**.
  
Let's load some sample events from a CSV file.


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```

Again, let's group the data before sending it to Fiddler.


```python
df_logs_grouped = fdl.utils.helpers.group_by(
    df=production_data_df, group_by_col='srch_id'
)
df_logs_grouped
```

Now publish the events


```python
production_publish_job = model.publish(df_logs_grouped)

print(
    f'Initiated production environment data upload with Job ID = {production_publish_job.id}'
)

# Uncomment the line below to wait for the job to finish, otherwise it will run in the background.
# You can check the status on the Jobs page in the Fiddler UI or use the job ID to query the job status via the API.
# production_publish_job.wait()
```

# Get insights


**You're all done!**
  
You can now head to your Fiddler environment and start getting enhanced observability into your model's performance.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/ranking_model_1.png" />
        </td>
    </tr>
</table>

--------
**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
