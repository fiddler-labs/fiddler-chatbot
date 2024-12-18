---
title: ML Monitoring - NLP Inputs
slug: simple-nlp-monitoring-quick-start
excerpt: Quickstart Notebook
metadata:
  title: 'Quickstart: NLP Monitoring | Fiddler Docs'
  description: >-
    This document provides a guide on using Fiddler to monitor NLP models by
    applying a multi-class classifier to the 20newsgroup dataset and monitoring
    text embeddings using Fiddler's Vector Monitoring approach.
  image: []
  robots: index
createdAt: Mon Aug 15 2022 23:29:02 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 14:00:57 GMT+0000 (Coordinated Universal Time)
icon: notebook
---

# ML Monitoring - NLP Inputs

This guide will walk you through the basic steps required to use Fiddler for monitoring NLP models. A multi-class classifier is applied to the 20newsgroup dataset and the text embeddings are monitored using Fiddler's unique Vector Monitoring approach.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_NLP_Multiclass_Monitoring.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_NLP_Multiclass_Monitoring.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Monitoring a Multiclass Classifier Model with Text Inputs
Unstructured data such as text are usually represented as high-dimensional vectors when processed by ML models. In this example notebook we present how [Fiddler Vector Monitoring](https://www.fiddler.ai/blog/monitoring-natural-language-processing-and-computer-vision-models-part-1) can be used to monitor NLP models using a text classification use case.

Following the steps in this notebook you can see how to onboard models that deal with unstructured text inputs. In this example, we use the 20Newsgroups dataset and train a multi-class classifier that is applied to vector embeddings of text documents.

We monitor this model at production time and assess the performance of Fiddler's vector monitoring by manufacturing synthetic drift via sampling from specific text categories at different deployment time intervals.

---

Now we perform the following steps to demonstrate how Fiddler NLP monitoring works:

1. Connect to Fiddler
2. Load a Data Sample
3. Define the Model Specifications
4. Create a Model
5. Publish a Static Baseline (Optional)
6. Publish Production Events

Get insights!

## 0. Imports


```python

%pip install -q fiddler-client

import time as time

import numpy as np
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
PROJECT_NAME = 'quickstart_examples'
MODEL_NAME = 'nlp_newsgroups_multiclass'

STATIC_BASELINE_NAME = 'baseline_dataset'

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/nlp_text_multiclassifier_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/v3/nlp_text_multiclassifier_production_data.csv'
```

Now just run the following to connect to your Fiddler environment.


```python
fdl.init(url=URL, token=TOKEN)
```

#### 1.a Create New or Load Existing Project

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

Now we retrieve the 20Newsgroup dataset. This dataset is fetched from the [scikit-learn real-world datasets](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html#) and pre-processed using [this notebook](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/pre-proccessing/20newsgroups_prep_vectorization.ipynb).  For simplicity sake, we have stored a copy in our GitHub repo.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```

## 3. Define the Model Specifications

Next we should tell Fiddler a bit more about the model by creating a `ModelSpec` object that specifies the model's inputs, outputs, targets, and metadata, along with other information such as the enrichments we want performed on our model's data.

### Instruct Fiddler to generate embeddings for our unstructured model input

Fiddler offers a powerful set of enrichment services that we can use to enhance how we monitor our model's performance.  In this example, we instruct Fiddler to generate embeddings for our unstructured text.  These generated embeddings are a numerical vector that represent the content and context of our unstructured input field, _original_text_.  These embeddings then power Fiddler's vector monitoring capability for detecting drift.

Before creating a `ModelSpec` object, we define a custom feature using the [fdl.Enrichment()](https://docs.fiddler.ai/python-client-3-x/api-methods-30#fdl.enrichment-private-preview) API. When creating an enrichment, a name must be assigned to the custom feature using the `name` argument. Each enrichment appears in the monitoring tab in the Fiddler UI with this assigned name. Finally, the default clustering setup can be modified by passing the number of cluster centroids to the `n_clusters` argument.

Here we define an [embedding fdl.Enrichment](https://docs.fiddler.ai/python-client-3-x/api-methods-30#embedding-private-preview) and then use that embedding enrichment to create a [fdl.TextEmbedding](https://docs.fiddler.ai/python-client-3-x/api-methods-30#customfeature) input that can be used to track drift and to be plotted in Fiddler's UMAP visualizations.


```python
fiddler_backend_enrichments = [
    fdl.Enrichment(
        name='Enrichment Text Embedding',
        enrichment='embedding',
        columns=['original_text'],
    ),
    fdl.TextEmbedding(
        name='Original TextEmbedding',
        source_column='original_text',
        column='Enrichment Text Embedding',
        n_clusters=6,
    ),
]
```


```python
model_spec = fdl.ModelSpec(
    inputs=['original_text'],
    outputs=[col for col in sample_data_df.columns if col.startswith('prob_')],
    targets=['target'],
    metadata=['n_tokens', 'string_size', 'timestamp'],
    custom_features=fiddler_backend_enrichments,
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly. Here we are just noting the column with the event datetime.


```python
timestamp_column = 'timestamp'
```

Fiddler supports a variety of model tasks. In this case, we're setting the task type to multi-class classification to inform Fiddler that is the type of model we are monitoring.


```python
model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

task_params = fdl.ModelTaskParams(
    target_class_order=[col[5:] for col in model_spec.outputs]
)
```

## 4. Create a Model

Once we've specified information about our model, we can onboard (add) it to Fiddler by calling `Model.create`.


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

## 5. Publish a Static Baseline (Optional)

Since Fiddler already knows how to process data for your model, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive. 

Note : The data given during the model creation is purely for schema inference and not a default baseline.

Then, once we start sending production data to Fiddler, you'll be able to see **drift scores** telling you whenever it starts to diverge from this static baseline.

***

Let's publish our **original data sample** as a pre-production dataset. This will automatically add it as a baseline for the model.


*For more information on how to design your baseline dataset, [click here](https://docs.fiddler.ai/client-guide/creating-a-baseline-dataset).*


```python
baseline_publish_job = model.publish(
    source=sample_data_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=STATIC_BASELINE_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job.id}'
)

# Uncomment the line below to wait for the job to finish, otherwise it will run in the background.
# You can check the status on the Jobs page in the Fiddler UI or use the job ID to query the job status via the API.
# baseline_publish_job.wait()
```

## 6. Publish Production Events

Now let's publish some sample production events into Fiddler. For the timestamps in the middle of the event dataset, we've over-sampled from certain topics which introduces synthetic drift. This oversampling to inject drift allows us to better illustrate how Fiddler's vector monitoring approach detects drift in our unstructured inputs.


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```

Next, let's publish events our events with the synthetic drift


```python
production_publish_job = model.publish(production_data_df)

print(
    f'Initiated production environment data upload with Job ID = {production_publish_job.id}'
)

# Uncomment the line below to wait for the job to finish, otherwise it will run in the background.
# You can check the status on the Jobs page in the Fiddler UI or use the job ID to query the job status via the API.
# production_publish_job.wait()
```

# Get Insights


**You're all done!**
  
Head to the Fiddler UI to start getting enhanced observability into your model's performance.



In particular, you can go to your model's default dashboard in Fiddler and check out the resulting drift chart . The first image below is a screenshot of the automatically generated drift chart which shows the drift of the original text. The second image is a custom drift chart with traffic details at an hourly time bin. (Annotation bubbles are not generated by the Fiddler UI.)

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/nlp_multiiclass_drift_2.png"  />
        </td>
    </tr>
</table>

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/nlp_multiiclass_drift.png"  />
        </td>
    </tr>
</table>
