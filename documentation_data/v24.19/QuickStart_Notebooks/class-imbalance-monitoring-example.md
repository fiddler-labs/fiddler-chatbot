---
title: ML Monitoring - Class Imbalance
slug: class-imbalance-monitoring-example
metadata:
  title: 'Quickstart: Class Imbalance Monitoring | Fiddler Docs'
  description: >-
    This document discusses the class imbalance problem in machine learning and
    how Fiddler uses a class weighting parameter to address it, showcasing the
    difference in detecting drift signals in the minority class.
  robots: index
icon: notebook
---

# ML Monitoring - Class Imbalance

Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the _class imbalance problem_. This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class. This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the sheer number of inferences seen in the majority class.

This guide showcases how Fiddler uses a class weighting parameter to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach..

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Imbalanced_Data.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Imbalanced_Data.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Fiddler Quick Start Class Imbalance Guide

Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the class imbalance problem.  This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class.  This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the large number of inferences seen in the majority class.  The following notebook showcases how Fiddler uses a class weighting paramater to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach.

1. Connect to Fiddler
2. Load a Data Sample
3. Create Both Model Versions
4. Publish Static Baselines
5. Publish Production Events
6. Compare the Two Models

## 0. Imports


```python
%pip install -q fiddler-client;

import time

import sklearn
import numpy as np
import pandas as pd
import fiddler as fdl

print(f"Running Fiddler Python client version {fdl.__version__}")
```

# 1. Connect to Fiddler

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
MODEL_NAME = 'imbalance_cc_fraud'
MODEL_NAME_WEIGHTED = 'imbalance_cc_fraud_weighted'
STATIC_BASELINE_NAME = 'baseline_dataset'

PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_production_data.csv'
```

Now just run the following to connect to your Fiddler environment.


```python
fdl.init(url=URL, token=TOKEN)
```

#### 1.a Create New or Load Existing Project

Once you connect, you can create a new project by specifying a unique project name in the fld.Project constructor and call the `create()` method. If the project already exists, it will load it for use.


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

# 2. Load a Data Sample

In this example, we'll be looking at a fraud detection use case.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python

sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```


```python
sample_data_df['Class'].value_counts()

print(
    'Percentage of minority class: {}%'.format(
        round(
            sample_data_df['Class'].value_counts()[1] * 100 / sample_data_df.shape[0], 4
        )
    )
)
```

# 3. Create Both Model Versions

Now, we will create two models:
1. One model with class weight parameters
2. One model without class weight parameters

Below, we first create a `ModelSpec` object which is common between the two. 


```python
model_spec = fdl.ModelSpec(
    inputs=set(sample_data_df.columns) - set(['Class', 'prediction_score', 'timestamp']),
    outputs=['prediction_score'],
    targets=['Class'],
    metadata=['timestamp']
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model.


```python
# id_column = '' # Optional: Specify the name of the ID column if you have one
timestamp_column = 'timestamp'
```

Define the weighted and unweighted versions of the model task parameters


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

# Weighted Model Task Params
task_params_weighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
    class_weights=sklearn.utils.class_weight.compute_class_weight(
        class_weight="balanced",
        classes=np.unique(sample_data_df["Class"]),
        y=sample_data_df["Class"],
    ).tolist(),
)

# Unweighted Model Task Params aka default Model Task Params
task_params_unweighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
)
```

Now, we onboard (create) the two models to Fiddler -- the first without any class weights and the second with defined class weights.


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_unweighted,
    event_ts_col=timestamp_column
)

model.create()
print(f'New unweighted model created with id = {model.id} and name = {model.name}')

weighted_model = fdl.Model.from_data(
    name=MODEL_NAME_WEIGHTED,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_weighted,
    event_ts_col=timestamp_column
)

weighted_model.create()
print(f'New weighted model created with id = {weighted_model.id} and name = {weighted_model.name}')

```

# 4. Publish Static Baselines

Since Fiddler already knows how to process data for your models, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive.

Then, once we start sending production data to Fiddler, you'll be able to see **drift scores** telling you whenever it starts to diverge from this static baseline.

***

Let's publish our **original data sample** as a pre-production dataset. This will automatically add it as a baseline for each model.


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

baseline_publish_job_weighted = weighted_model.publish(
    source=sample_data_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=STATIC_BASELINE_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job_weighted.id}'
)

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# baseline_publish_job.wait()
# baseline_publish_job_weighted.wait()
```

# 5. Publish Production Events 

Publish the same events to both models with synthetic drift in the minority class


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```


```python
print(
    "Percentage of minority class: {}%".format(
        round(
            production_data_df["Class"].value_counts()[1] * 100 / production_data_df.shape[0], 4
        )
    )
)
```

We see that the percentage of minority class in production data is > 3 times than that of baseline data. This should create a big drift in the predictions.

We will now publish the same production/event data for both of the models -- the one with class weights and the one without class weights.


```python
production_publish_job = model.publish(production_data_df)

print(f'For Model: {model.name} - initiated production environment data upload with Job ID = {production_publish_job.id}')

production_publish_job_weighted = weighted_model.publish(production_data_df)

print(f'For Model: {weighted_model.name} - initiated production environment data upload with Job ID = {production_publish_job_weighted.id}')

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# production_publish_job.wait()
# production_publish_job_weighted.wait()
```

# 5. Compare the Two Models

**You're all done!**


In the Fiddler UI, we can see the model without the class weights defined the output/prediction drift in the minority class is very hard to detect (`<=0.05`) because it is obsured by the overwhelming volume of events in the majority class.  If we declare class weights, then we see a higher drift which is a more accurate respresentation of the production data where the ratio of minority is class is 3x.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/imabalance_data_1.png" />
        </td>
    </tr>
</table>

**What's Next?**

Try the [LLM Monitoring - Quick Start Notebook](https://docs.fiddler.ai/quickstart-notebooks/simple-llm-monitoring)

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Fiddler Quick Start Class Imbalance Guide

Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the class imbalance problem.  This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class.  This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the large number of inferences seen in the majority class.  The following notebook showcases how Fiddler uses a class weighting paramater to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach.

1. Connect to Fiddler
2. Load a Data Sample
3. Create Both Model Versions
4. Publish Static Baselines
5. Publish Production Events
6. Compare the Two Models

## 0. Imports


```python
%pip install -q fiddler-client;

import time

import sklearn
import numpy as np
import pandas as pd
import fiddler as fdl

print(f"Running Fiddler Python client version {fdl.__version__}")
```

# 1. Connect to Fiddler

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
MODEL_NAME = 'imbalance_cc_fraud'
MODEL_NAME_WEIGHTED = 'imbalance_cc_fraud_weighted'
STATIC_BASELINE_NAME = 'baseline_dataset'

PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_production_data.csv'
```

Now just run the following to connect to your Fiddler environment.


```python
fdl.init(url=URL, token=TOKEN)
```

#### 1.a Create New or Load Existing Project

Once you connect, you can create a new project by specifying a unique project name in the fld.Project constructor and call the `create()` method. If the project already exists, it will load it for use.


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

# 2. Load a Data Sample

In this example, we'll be looking at a fraud detection use case.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python

sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```


```python
sample_data_df['Class'].value_counts()

print(
    'Percentage of minority class: {}%'.format(
        round(
            sample_data_df['Class'].value_counts()[1] * 100 / sample_data_df.shape[0], 4
        )
    )
)
```

# 3. Create Both Model Versions

Now, we will create two models:
1. One model with class weight parameters
2. One model without class weight parameters

Below, we first create a `ModelSpec` object which is common between the two. 


```python
model_spec = fdl.ModelSpec(
    inputs=set(sample_data_df.columns) - set(['Class', 'prediction_score', 'timestamp']),
    outputs=['prediction_score'],
    targets=['Class'],
    metadata=['timestamp']
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model.


```python
# id_column = '' # Optional: Specify the name of the ID column if you have one
timestamp_column = 'timestamp'
```

Define the weighted and unweighted versions of the model task parameters


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

# Weighted Model Task Params
task_params_weighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
    class_weights=sklearn.utils.class_weight.compute_class_weight(
        class_weight="balanced",
        classes=np.unique(sample_data_df["Class"]),
        y=sample_data_df["Class"],
    ).tolist(),
)

# Unweighted Model Task Params aka default Model Task Params
task_params_unweighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
)
```

Now, we onboard (create) the two models to Fiddler -- the first without any class weights and the second with defined class weights.


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_unweighted,
    event_ts_col=timestamp_column
)

model.create()
print(f'New unweighted model created with id = {model.id} and name = {model.name}')

weighted_model = fdl.Model.from_data(
    name=MODEL_NAME_WEIGHTED,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_weighted,
    event_ts_col=timestamp_column
)

weighted_model.create()
print(f'New weighted model created with id = {weighted_model.id} and name = {weighted_model.name}')

```

# 4. Publish Static Baselines

Since Fiddler already knows how to process data for your models, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive.

Then, once we start sending production data to Fiddler, you'll be able to see **drift scores** telling you whenever it starts to diverge from this static baseline.

***

Let's publish our **original data sample** as a pre-production dataset. This will automatically add it as a baseline for each model.


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

baseline_publish_job_weighted = weighted_model.publish(
    source=sample_data_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=STATIC_BASELINE_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job_weighted.id}'
)

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# baseline_publish_job.wait()
# baseline_publish_job_weighted.wait()
```

# 5. Publish Production Events 

Publish the same events to both models with synthetic drift in the minority class


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```


```python
print(
    "Percentage of minority class: {}%".format(
        round(
            production_data_df["Class"].value_counts()[1] * 100 / production_data_df.shape[0], 4
        )
    )
)
```

We see that the percentage of minority class in production data is > 3 times than that of baseline data. This should create a big drift in the predictions.

We will now publish the same production/event data for both of the models -- the one with class weights and the one without class weights.


```python
production_publish_job = model.publish(production_data_df)

print(f'For Model: {model.name} - initiated production environment data upload with Job ID = {production_publish_job.id}')

production_publish_job_weighted = weighted_model.publish(production_data_df)

print(f'For Model: {weighted_model.name} - initiated production environment data upload with Job ID = {production_publish_job_weighted.id}')

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# production_publish_job.wait()
# production_publish_job_weighted.wait()
```

# 5. Compare the Two Models

**You're all done!**


In the Fiddler UI, we can see the model without the class weights defined the output/prediction drift in the minority class is very hard to detect (`<=0.05`) because it is obsured by the overwhelming volume of events in the majority class.  If we declare class weights, then we see a higher drift which is a more accurate respresentation of the production data where the ratio of minority is class is 3x.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/imabalance_data_1.png" />
        </td>
    </tr>
</table>

**What's Next?**

Try the [LLM Monitoring - Quick Start Notebook](https://docs.fiddler.ai/quickstart-notebooks/simple-llm-monitoring)

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Fiddler Quick Start Class Imbalance Guide

Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the class imbalance problem.  This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class.  This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the large number of inferences seen in the majority class.  The following notebook showcases how Fiddler uses a class weighting paramater to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach.

1. Connect to Fiddler
2. Load a Data Sample
3. Create Both Model Versions
4. Publish Static Baselines
5. Publish Production Events
6. Compare the Two Models

## 0. Imports


```python
%pip install -q fiddler-client;

import time

import sklearn
import numpy as np
import pandas as pd
import fiddler as fdl

print(f"Running Fiddler Python client version {fdl.__version__}")
```

# 1. Connect to Fiddler

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
MODEL_NAME = 'imbalance_cc_fraud'
MODEL_NAME_WEIGHTED = 'imbalance_cc_fraud_weighted'
STATIC_BASELINE_NAME = 'baseline_dataset'

PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_production_data.csv'
```

Now just run the following to connect to your Fiddler environment.


```python
fdl.init(url=URL, token=TOKEN)
```

#### 1.a Create New or Load Existing Project

Once you connect, you can create a new project by specifying a unique project name in the fld.Project constructor and call the `create()` method. If the project already exists, it will load it for use.


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

# 2. Load a Data Sample

In this example, we'll be looking at a fraud detection use case.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python

sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```


```python
sample_data_df['Class'].value_counts()

print(
    'Percentage of minority class: {}%'.format(
        round(
            sample_data_df['Class'].value_counts()[1] * 100 / sample_data_df.shape[0], 4
        )
    )
)
```

# 3. Create Both Model Versions

Now, we will create two models:
1. One model with class weight parameters
2. One model without class weight parameters

Below, we first create a `ModelSpec` object which is common between the two. 


```python
model_spec = fdl.ModelSpec(
    inputs=set(sample_data_df.columns) - set(['Class', 'prediction_score', 'timestamp']),
    outputs=['prediction_score'],
    targets=['Class'],
    metadata=['timestamp']
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model.


```python
# id_column = '' # Optional: Specify the name of the ID column if you have one
timestamp_column = 'timestamp'
```

Define the weighted and unweighted versions of the model task parameters


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

# Weighted Model Task Params
task_params_weighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
    class_weights=sklearn.utils.class_weight.compute_class_weight(
        class_weight="balanced",
        classes=np.unique(sample_data_df["Class"]),
        y=sample_data_df["Class"],
    ).tolist(),
)

# Unweighted Model Task Params aka default Model Task Params
task_params_unweighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
)
```

Now, we onboard (create) the two models to Fiddler -- the first without any class weights and the second with defined class weights.


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_unweighted,
    event_ts_col=timestamp_column
)

model.create()
print(f'New unweighted model created with id = {model.id} and name = {model.name}')

weighted_model = fdl.Model.from_data(
    name=MODEL_NAME_WEIGHTED,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_weighted,
    event_ts_col=timestamp_column
)

weighted_model.create()
print(f'New weighted model created with id = {weighted_model.id} and name = {weighted_model.name}')

```

# 4. Publish Static Baselines

Since Fiddler already knows how to process data for your models, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive.

Then, once we start sending production data to Fiddler, you'll be able to see **drift scores** telling you whenever it starts to diverge from this static baseline.

***

Let's publish our **original data sample** as a pre-production dataset. This will automatically add it as a baseline for each model.


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

baseline_publish_job_weighted = weighted_model.publish(
    source=sample_data_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=STATIC_BASELINE_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job_weighted.id}'
)

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# baseline_publish_job.wait()
# baseline_publish_job_weighted.wait()
```

# 5. Publish Production Events 

Publish the same events to both models with synthetic drift in the minority class


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```


```python
print(
    "Percentage of minority class: {}%".format(
        round(
            production_data_df["Class"].value_counts()[1] * 100 / production_data_df.shape[0], 4
        )
    )
)
```

We see that the percentage of minority class in production data is > 3 times than that of baseline data. This should create a big drift in the predictions.

We will now publish the same production/event data for both of the models -- the one with class weights and the one without class weights.


```python
production_publish_job = model.publish(production_data_df)

print(f'For Model: {model.name} - initiated production environment data upload with Job ID = {production_publish_job.id}')

production_publish_job_weighted = weighted_model.publish(production_data_df)

print(f'For Model: {weighted_model.name} - initiated production environment data upload with Job ID = {production_publish_job_weighted.id}')

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# production_publish_job.wait()
# production_publish_job_weighted.wait()
```

# 5. Compare the Two Models

**You're all done!**


In the Fiddler UI, we can see the model without the class weights defined the output/prediction drift in the minority class is very hard to detect (`<=0.05`) because it is obsured by the overwhelming volume of events in the majority class.  If we declare class weights, then we see a higher drift which is a more accurate respresentation of the production data where the ratio of minority is class is 3x.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/imabalance_data_1.png" />
        </td>
    </tr>
</table>

**What's Next?**

Try the [LLM Monitoring - Quick Start Notebook](https://docs.fiddler.ai/quickstart-notebooks/simple-llm-monitoring)

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Fiddler Quick Start Class Imbalance Guide

Many ML use cases, like fraud detection and facial recognition, suffer from what is known as the class imbalance problem.  This problem exists where a vast majority of the inferences seen by the model belong to only one class, known as the majority class.  This makes detecting drift in the minority class very difficult as the "signal" is completely outweighed by the large number of inferences seen in the majority class.  The following notebook showcases how Fiddler uses a class weighting paramater to deal with this problem. This notebook will onboard two identical models -- one without class imbalance weighting and one with class imbalance weighting -- to illustrate how drift signals in the minority class are easier to detect once properly amplified by Fiddler's unique class weighting approach.

1. Connect to Fiddler
2. Load a Data Sample
3. Create Both Model Versions
4. Publish Static Baselines
5. Publish Production Events
6. Compare the Two Models

## 0. Imports


```python
%pip install -q fiddler-client;

import time

import sklearn
import numpy as np
import pandas as pd
import fiddler as fdl

print(f"Running Fiddler Python client version {fdl.__version__}")
```

# 1. Connect to Fiddler

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
MODEL_NAME = 'imbalance_cc_fraud'
MODEL_NAME_WEIGHTED = 'imbalance_cc_fraud_weighted'
STATIC_BASELINE_NAME = 'baseline_dataset'

PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/imbalance_production_data.csv'
```

Now just run the following to connect to your Fiddler environment.


```python
fdl.init(url=URL, token=TOKEN)
```

#### 1.a Create New or Load Existing Project

Once you connect, you can create a new project by specifying a unique project name in the fld.Project constructor and call the `create()` method. If the project already exists, it will load it for use.


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

# 2. Load a Data Sample

In this example, we'll be looking at a fraud detection use case.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python

sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
sample_data_df
```


```python
sample_data_df['Class'].value_counts()

print(
    'Percentage of minority class: {}%'.format(
        round(
            sample_data_df['Class'].value_counts()[1] * 100 / sample_data_df.shape[0], 4
        )
    )
)
```

# 3. Create Both Model Versions

Now, we will create two models:
1. One model with class weight parameters
2. One model without class weight parameters

Below, we first create a `ModelSpec` object which is common between the two. 


```python
model_spec = fdl.ModelSpec(
    inputs=set(sample_data_df.columns) - set(['Class', 'prediction_score', 'timestamp']),
    outputs=['prediction_score'],
    targets=['Class'],
    metadata=['timestamp']
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model.


```python
# id_column = '' # Optional: Specify the name of the ID column if you have one
timestamp_column = 'timestamp'
```

Define the weighted and unweighted versions of the model task parameters


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

# Weighted Model Task Params
task_params_weighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
    class_weights=sklearn.utils.class_weight.compute_class_weight(
        class_weight="balanced",
        classes=np.unique(sample_data_df["Class"]),
        y=sample_data_df["Class"],
    ).tolist(),
)

# Unweighted Model Task Params aka default Model Task Params
task_params_unweighted = fdl.ModelTaskParams(
    target_class_order=[0, 1],
    binary_classification_threshold=0.4,
)
```

Now, we onboard (create) the two models to Fiddler -- the first without any class weights and the second with defined class weights.


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_unweighted,
    event_ts_col=timestamp_column
)

model.create()
print(f'New unweighted model created with id = {model.id} and name = {model.name}')

weighted_model = fdl.Model.from_data(
    name=MODEL_NAME_WEIGHTED,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params_weighted,
    event_ts_col=timestamp_column
)

weighted_model.create()
print(f'New weighted model created with id = {weighted_model.id} and name = {weighted_model.name}')

```

# 4. Publish Static Baselines

Since Fiddler already knows how to process data for your models, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive.

Then, once we start sending production data to Fiddler, you'll be able to see **drift scores** telling you whenever it starts to diverge from this static baseline.

***

Let's publish our **original data sample** as a pre-production dataset. This will automatically add it as a baseline for each model.


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

baseline_publish_job_weighted = weighted_model.publish(
    source=sample_data_df,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=STATIC_BASELINE_NAME,
)
print(
    f'Initiated pre-production environment data upload with Job ID = {baseline_publish_job_weighted.id}'
)

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# baseline_publish_job.wait()
# baseline_publish_job_weighted.wait()
```

# 5. Publish Production Events 

Publish the same events to both models with synthetic drift in the minority class


```python
production_data_df = pd.read_csv(PATH_TO_EVENTS_CSV)

# Shift the timestamps of the production events to be as recent as today
production_data_df['timestamp'] = production_data_df['timestamp'] + (
    int(time.time() * 1000) - production_data_df['timestamp'].max()
)
production_data_df
```


```python
print(
    "Percentage of minority class: {}%".format(
        round(
            production_data_df["Class"].value_counts()[1] * 100 / production_data_df.shape[0], 4
        )
    )
)
```

We see that the percentage of minority class in production data is > 3 times than that of baseline data. This should create a big drift in the predictions.

We will now publish the same production/event data for both of the models -- the one with class weights and the one without class weights.


```python
production_publish_job = model.publish(production_data_df)

print(f'For Model: {model.name} - initiated production environment data upload with Job ID = {production_publish_job.id}')

production_publish_job_weighted = weighted_model.publish(production_data_df)

print(f'For Model: {weighted_model.name} - initiated production environment data upload with Job ID = {production_publish_job_weighted.id}')

# Uncomment the lines below to wait for the jobs to finish, otherwise they will run in the background.
# You can check the statuses on the Jobs page in the Fiddler UI or use the job IDs to query the job statuses via the API.
# production_publish_job.wait()
# production_publish_job_weighted.wait()
```

# 5. Compare the Two Models

**You're all done!**


In the Fiddler UI, we can see the model without the class weights defined the output/prediction drift in the minority class is very hard to detect (`<=0.05`) because it is obsured by the overwhelming volume of events in the majority class.  If we declare class weights, then we see a higher drift which is a more accurate respresentation of the production data where the ratio of minority is class is 3x.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/imabalance_data_1.png" />
        </td>
    </tr>
</table>

**What's Next?**

Try the [LLM Monitoring - Quick Start Notebook](https://docs.fiddler.ai/quickstart-notebooks/simple-llm-monitoring)

---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions!

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
