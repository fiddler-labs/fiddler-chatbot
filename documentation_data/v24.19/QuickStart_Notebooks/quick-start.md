---
title: ML Monitoring - Simple
slug: quick-start
metadata:
  title: 'Quickstart: Simple Monitoring | Fiddler Docs'
  description: >-
    This document provides a guide for using Fiddler for model monitoring using
    sample data provided by Fiddler.
  robots: index
icon: notebook
---

# ML Monitoring - Simple

This guide will walk you through the basic onboarding steps required to use Fiddler for model monitoring, **using sample data provided by Fiddler**.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Simple_Monitoring.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Simple_Monitoring.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Fiddler Simple Monitoring Quick Start Guide

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and other LOB teams to **monitor, analyze, and improve ML deployments at enterprise scale**.
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can start using Fiddler ***in minutes*** by following these quick steps:

1. Connect to Fiddler
2. Load a Data Sample
3. Define the Model Specifications
4. Set the Model Task
5. Create a Model
6. Set Up Alerts **(Optional)**
7. Create a Custom Metric **(Optional)**
8. Create a Segment **(Optional)**
9. Publish a Pre-production Baseline **(Optional)**
10. Configure a Rolling Baseline **(Optional)**
11. Publish Production Events

# 0. Imports


```python
%pip install -q fiddler-client

import time as time

import pandas as pd
import fiddler as fdl

print(f'Running Fiddler Python client version {fdl.__version__}')
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
PROJECT_NAME = 'quickstart_examples'  # If the project already exists, the notebook will create the model under the existing project.
MODEL_NAME = 'bank_churn_simple_monitoring'

STATIC_BASELINE_NAME = 'baseline_dataset'
ROLLING_BASELINE_NAME = 'rolling_baseline_1week'

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv'
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_production_data.csv'
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

You should now be able to see the newly created project in the Fiddler UI.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/simple_monitoring_1.png" />
        </td>
    </tr>
</table>

## 2. Load a Data Sample

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list  = sample_data_df.columns
sample_data_df
```

## 3. Define the Model Specifications

In order to create a model in Fiddler, create a ModelSpec object with information about what each column of your data sample should used for.

Fiddler supports four column types:
1. **Inputs**
2. **Outputs** (Model predictions)
3. **Target** (Ground truth values)
4. **Metadata**


```python
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)
```


```python
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=['churn'],  # Note: only a single Target column is allowed, use metadata columns and custom metrics for additional targets
    metadata=['customer_id', 'timestamp'],
)
```

If you have columns in your ModelSpec which denote **prediction IDs or timestamps**, then Fiddler can use these to power its analytics accordingly.

Let's call them out here and use them when configuring the Model in step 5.


```python
id_column = 'customer_id'
timestamp_column = 'timestamp'
```

## 4. Set the Model Task

Fiddler supports a variety of model tasks. In this case, we're adding a binary classification model.

For this, we'll create a ModelTask object and an additional ModelTaskParams object to specify the ordering of our positive and negative labels.

*For a detailed breakdown of all supported model tasks, click [here](https://docs.fiddler.ai/product-guide/task-types).*


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=['no', 'yes'])
```

## 5. Create a Model

Create a Model object and publish it to Fiddler, passing in
1. Your data sample
2. The ModelSpec object
3. The ModelTask and ModelTaskParams objects
4. The ID and timestamp columns


```python
model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=project.id,
    source=sample_data_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params,
    event_id_col=id_column,
    event_ts_col=timestamp_column,
)

model.create()
print(f'New model created with id = {model.id} and name = {model.name}')
```

On the project page, you should now be able to see the newly onboarded model with its model schema.

<table>
    <tr>
        <td>
            <img src="https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/images/simple_monitoring_3.png?raw=true" />
        </td>
    </tr>
</table>

<table>
    <tr>
        <td>
            <img src="https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/images/simple_monitoring_4.png?raw=true" />
        </td>
    </tr>
</table>

## 6. Set Up Alerts (Optional)

Fiddler allows creating alerting rules when your data or model predictions deviate from expected behavior.

The alert rules can compare metrics to **absolute** or **relative** values.

Please refer to [our documentation](https://docs.fiddler.ai/client-guide/alerts-with-fiddler-client) for more information on Alert Rules.

---
  
Let's set up some alert rules.

The following API call sets up a Data Integrity type rule which triggers an email notification when published events have 2 or more range violations in any 1 day bin for the `numofproducts` column.


```python
alert_rule_1 = fdl.AlertRule(
    name='Bank Churn Range Violation Alert',
    model_id=model.id,
    metric_id='range_violation_count',
    bin_size=fdl.BinSize.DAY,
    compare_to=fdl.CompareTo.RAW_VALUE,
    priority=fdl.Priority.HIGH,
    warning_threshold=2,
    critical_threshold=3,
    condition=fdl.AlertCondition.GREATER,
    columns=['numofproducts'],
)

alert_rule_1.create()
print(
    f'New alert rule created with id = {alert_rule_1.id} and name = {alert_rule_1.name}'
)

# Set notification configuration for the alert rule, a single email address for this simple example
alert_rule_1.set_notification_config(emails=['name@google.com'])
```

Let's add a second alert rule.

This one sets up a Performance type rule which triggers an email notification when precision metric is 5% higher than that from 1 hr bin one day ago.


```python
alert_rule_2 = fdl.AlertRule(
    name='Bank Churn Performance Alert',
    model_id=model.id,
    metric_id='precision',
    bin_size=fdl.BinSize.HOUR,
    compare_to=fdl.CompareTo.TIME_PERIOD,
    compare_bin_delta=24,  # Multiple of the bin size
    condition=fdl.AlertCondition.GREATER,
    warning_threshold=0.05,
    critical_threshold=0.1,
    priority=fdl.Priority.HIGH,
)

alert_rule_2.create()
print(
    f'New alert rule created with id = {alert_rule_2.id} and name = {alert_rule_2.name}'
)

# Set notification configuration for the alert rule, a single email address for this simple example
alert_rule_2.set_notification_config(emails=['name@google.com'])
```

## 7. Create a Custom Metric (Optional)

Fiddler's [Custom Metric API](https://docs.fiddler.ai/python-client-3-x/api-methods-30#custommetric) enables user-defined formulas for custom metrics.  Custom metrics will be tracked over time and can be used in Charts and Alerts just like the many out of the box metrics provided by Fiddler.  Custom metrics can also be managed in the Fiddler UI.

Please refer to [our documentation](https://docs.fiddler.ai/product-guide/monitoring-platform/custom-metrics) for more information on Custom Metrics.

---
  
Let's create an example custom metric.


```python
custom_metric = fdl.CustomMetric(
    name='Lost Revenue',
    model_id=model.id,
    description='A metric to track revenue lost for each false positive prediction.',
    definition="""sum(if(fp(),1,0) * -100)""",  # This is an excel like formula which adds -$100 for each false positive predicted by the model
)

custom_metric.create()
print(
    f'New custom metric created with id = {custom_metric.id} and name = {custom_metric.name}'
)
```

## 8. Create a Segment (Optional)
Fiddler's [Segment API](https://docs.fiddler.ai/python-client-3-x/api-methods-30#segments) enables defining named cohorts/sub-segments in your production data. These segments can be tracked over time, added to charts, and alerted upon. Segments can also be managed in the Fiddler UI.

Please refer to our [documentation](https://docs.fiddler.ai/product-guide/monitoring-platform/segments) for more information on the creation and management of segments.

Let's create a segment to track customers from Hawaii for a specific age range.


```python
segment = fdl.Segment(
    name='Hawaii Customers between 30 and 60',
    model_id=model.id,
    description='Hawaii Customers between 30 and 60',
    definition="(age<60 or age>30) and geography=='Hawaii'",
)

segment.create()
print(f'New segment created with id = {segment.id} and name = {segment.name}')
```

## 9. Publish a Static Baseline (Optional)

Since Fiddler already knows how to process data for your model, we can now add a **baseline dataset**.

You can think of this as a static dataset which represents **"golden data,"** or the kind of data your model expects to receive.

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

## 10. Configure a Rolling Baseline (Optional)

Fiddler also allows you to configure a baseline based on **past production data.**

This means instead of looking at a static slice of data, it will look into past production events and use what it finds for drift calculation.

Please refer to [our documentation](https://docs.fiddler.ai/client-guide/creating-a-baseline-dataset) for more information on Baselines.

---
  
Let's set up a rolling baseline that will allow us to calculate drift relative to production data from 1 week back.


```python
rolling_baseline = fdl.Baseline(
    model_id=model.id,
    name=ROLLING_BASELINE_NAME,
    type_=fdl.BaselineType.ROLLING,
    environment=fdl.EnvType.PRODUCTION,
    window_bin_size=fdl.WindowBinSize.DAY,  # Size of the sliding window
    offset_delta=7,  # How far back to set our window (multiple of window_bin_size)
)

rolling_baseline.create()
print(
    f'New rolling baseline created with id = {rolling_baseline.id} and name = {rolling_baseline.name}'
)
```

## 11. Publish Production Events

Finally, let's send in some production data!


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
  
Return to your Fiddler environment to get enhanced observability into your model's performance.

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/simple_monitoring_5.png" />
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
