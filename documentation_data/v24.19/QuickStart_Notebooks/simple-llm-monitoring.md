---
title: LLM Monitoring - Simple
slug: simple-llm-monitoring
createdAt: Mon Feb 26 2024 20:06:46 GMT+0000 (Coordinated Universal Time)
updatedAt: Tue Apr 16 2024 14:59:37 GMT+0000 (Coordinated Universal Time)
icon: notebook
---

# LLM Monitoring - Simple

This guide will walk you through the basic onboarding steps required to use Fiddler for monitoring of LLM applications, **using sample data provided by Fiddler**.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_LLM_Chatbot.ipynb)&#x20;

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_LLM_Chatbot.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Fiddler LLM Application Quick Start Guide

Fiddler is the pioneer in enterprise AI Observability, offering a unified platform that enables all model stakeholders to monitor model performance and to investigate the true source of model degredation.  Fiddler's AI Observability platform supports both traditional ML models as well as Generative AI applications.  This guide walks you through how to onboard an LLM chatbot application that is built using a RAG architecture.

---

You can start using Fiddler ***in minutes*** by following these 8 quick steps:

1. Connect to Fiddler
2. Create a Fiddler Project
3. Load a Data Sample
4. Opt-in to Specific Fiddler LLM Enrichments
5. Add Information About the LLM Application
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

Before you can add information about your LLM Application with Fiddler, you'll need to connect using the Fiddler Python client.


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
PROJECT_NAME = 'quickstart_examples'  # If the project already exists, the notebook will create the model under the existing project.
MODEL_NAME = 'fiddler_rag_llm_chatbot'

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/v3/chatbot_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/v3/chatbot_production_data.csv'
```

Now just run the following code block to connect to the Fiddler API!


```python
fdl.init(url=URL, token=TOKEN)
```

## 2. Create a Fiddler Project

Once you connect, you can create a new project by specifying a unique project name in the `Project` constructor and calling the `create()` method. If the project already exists, it will load it for use.


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

## 3. Load a Data Sample

In this example, we'll be onboarding data in order to observe our **Fiddler chatbot application**.
  
In order to get insights into the LLM Applications's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.
Let's use a file with some historical prompts, source docs, and responses from our chatbot for the sample.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```

Fiddler will uses this data sample to keep track of important information about your data.  This includes **data types**, **data ranges**, and **unique values** for categorical variables.

## 4. Opt-in to Specific Fiddler LLM Enrichments

After picking a sample of our chatbot's prompts and responses, we can request that Fiddler execute a series of enrichment services that can "score" our prompts and responses for a variety of insights.  These enrichment services can detect AI safety issues like PII leakage, hallucinations, toxicity, and more.  We can also opt-in for enrichment services like embedding generation which will allow us to track prompt and response outliers and drift. A full description of these enrichments can be found [here](https://docs.fiddler.ai/platform-guide/llm-monitoring/enrichments-private-preview).

---

Let's define the enrichment services we'd like to use.  Here we will opt in for embedding generation for our prompts, responses and source docs.  Additionally, let's opt in for PII detection, outlier detection through centroid distance metrics, and some other text-based evaluation scores.


```python
fiddler_backend_enrichments = [
    # prompt enrichment
    fdl.TextEmbedding(
        name='Prompt TextEmbedding',
        source_column='question',
        column='Enrichment Prompt Embedding',
        n_tags=10,
    ),
    # response enrichment
    fdl.TextEmbedding(
        name='Response TextEmbedding',
        source_column='response',
        column='Enrichment Response Embedding',
        n_tags=10,
    ),
    # rag document enrichments
    fdl.TextEmbedding(
        name='Source Docs TextEmbedding',
        source_column='source_docs',
        column='Enrichment Source Docs Embedding',
        n_tags=10,
    ),
    # safety
    fdl.Enrichment(
        name='FTL Safety',
        enrichment='ftl_prompt_safety',
        columns=['question', 'response'],
    ),
    # hallucination
    fdl.Enrichment(
        name='Faithfulness',
        enrichment='ftl_response_faithfulness',
        columns=['source_docs', 'response'],
        config={'context_field': 'source_docs', 'response_field': 'response'},
    ),
    # text quality
    fdl.Enrichment(
        name='Enrichment QA TextStat',
        enrichment='textstat',
        columns=['question', 'response'],
        config={
            'statistics': [
                'char_count',
                'flesch_reading_ease',
                'flesch_kincaid_grade',
            ]
        },
    ),
    fdl.Enrichment(
        name='Enrichment QA Sentiment',
        enrichment='sentiment',
        columns=['question', 'response'],
    ),
    # PII detection
    fdl.Enrichment(
        name='Rag PII', enrichment='pii', columns=['question'], allow_list=['fiddler']
    ),
]
```

## 5.  Add Information About the LLM application

Now it's time to onboard information about our LLM application to Fiddler.  We do this by defining a `ModelSpec` object.


---


The `ModelSpec` object will contain some **information about how your LLM application operates**.
  
*Just include:*
1. The **input/output** columns.  For a LLM application, these are just the raw inputs and outputs of our LLM application.
2. Any **metadata** columns.
3. The **custom features** which contain the configuration of the enrichments we opted for.

We'll also want a few other pieces of information:
1. The **task** your model or LLM application is performing (LLM, regression, binary classification, not set, etc.)
2. Which column to use to read timestamps from.


```python
model_spec = fdl.ModelSpec(
    inputs=['question', 'response', 'source_docs'],
    metadata=['session_id', 'comment', 'timestamp', 'feedback'],
    custom_features=fiddler_backend_enrichments,
)

model_task = fdl.ModelTask.LLM

timestamp_column = 'timestamp'
```

Then just publish all of this to Fiddler by configuring a `Model` object to represent your LLM application in Fiddler.


```python
llm_application = fdl.Model.from_data(
    source=sample_data_df,
    name=MODEL_NAME,
    project_id=project.id,
    spec=model_spec,
    task=model_task,
    event_ts_col=timestamp_column,
    max_cardinality=5,
)
```

Now call the `create` method to publish it to Fiddler!


```python
llm_application.create()
print(
    f'New model created with id = {llm_application.id} and name = {llm_application.name}'
)
```

## 6. Publish Production Events

Information about your LLM application is now onboarded to Fiddler. It's time to start publishing some production data!  


---


Each record sent to Fiddler is called **an event**.  Events simply contain the inputs and outputs of a predictive model or LLM application.
  
Let's load in some sample events (prompts and responses) from a CSV file.


```python
llm_events_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Timeshifting the timestamp column in the events file so the events are as recent as today
llm_events_df['timestamp'] = pd.to_datetime(llm_events_df['timestamp'])
time_diff = pd.Timestamp.now().normalize() - llm_events_df['timestamp'].max()
llm_events_df['timestamp'] += time_diff

llm_events_df
```

You can use the `Model.publish` function to start pumping data into Fiddler!
  
Just pass in the DataFrame containing your events.


```python
# Define the number of rows per chunk
chunk_size = 10

# Splitting the DataFrame into smaller chunks
for start in range(0, llm_events_df.shape[0], chunk_size):
    df_chunk = llm_events_df.iloc[start : start + chunk_size]
    llm_application.publish(df_chunk)
```

# Get insights

**You're all done!**
  
You can now head to your Fiddler environment and start getting enhanced observability into your LLM application's performance.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/LLM_chatbot_UMAP.png" />
        </td>
    </tr>
</table>

**What's Next?**

Try the [ML Monitoring - Quick Start Guide](https://docs.fiddler.ai/quickstart-notebooks/quick-start)

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.


```python

```
