---
title: ML Monitoring - User-defined Feature Impact
slug: user-defined-feature-impact-quick-start
excerpt: Quickstart Notebook
metadata:
  title: 'Quickstart: User-defined Feature Impact | Fiddler Docs'
  description: >-
    This document provides a guide on using Fiddler's feature impact upload API
    to supply your own feature impact values for your Fiddler model.
  image: []
  robots: index
createdAt: Tue Nov 19 2024 14:00:57 GMT+0000 (Coordinated Universal Time)
updatedAt: Tue Nov 19 2024 14:00:57 GMT+0000 (Coordinated Universal Time)
icon: notebook
---

# ML Monitoring - Feature Impact

### User-defined Feature Impact Upload

This guide will walk you through the steps needed to upload your model's existing feature impact values to your Fiddler model. This notebook uses the same example model leveraged in the [ML Monitoring - Simple](quick-start.md) quick start. If you have already run that notebook and the model exists in your Fiddler instance, then you may skip the setup steps in this guide as noted in the instructions.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_User_Defined_Feature_Impact.ipynb)

<div align="left"><figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure></div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_User_Defined_Feature_Impact.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Fiddler User-Defined Feature Impact Quick Start Guide

In this notebook we demonstrate how to upload your own precomputed feature impact values to a Fiddler model. Previous versions of Fiddler required you create either a surrogate or user model artifact with which to calculate the feature impact values within Fiddler. Both surrogate and user model artifact require extra steps when onboarding a model and may be unnecessary if the feature impact values already exist. 


---

The documentation for the user-defined feature impact upload API can be found online [here](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact).

User-Defined Feature Impact is supported on Fiddler version 24.12+ using Fiddler Python client API versions 3.3 and higher.

**Please note that you may skip Steps #2 - #5 and resume at [Step #6](#section_06)** if you have already run Fiddler's [Simple Monitoring Quick Start Guide](https://docs.fiddler.ai/quickstart-notebooks/quick-start) and used the default values and sample data.

1. Connect to Fiddler - Initialization, create a project
2. Load a Data Sample
3. Define Your Model Specifications
4. Set a Model Task
5. Add Your Model
6. Upload Your Feature Impact Values

# 0. Imports


```python
%pip install -q fiddler-client

import pandas as pd
import fiddler as fdl

print(f"Running client version {fdl.__version__}")
```

## 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client API.


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

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv'
PATH_TO_FI_VALUES = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores.json'
PATH_TO_FI_VALUES_UPDATED = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores_alt.json'
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

## 2. Load a Data Sample

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list = sample_data_df.columns
sample_data_df
```

## 3. Define Your Model Specifications

In order to add your model to Fiddler, simply create a ModelSpec object with information about what each column of your data sample should used for.

Fiddler supports four column types:
1. **Inputs**
2. **Outputs** (Model predictions)
3. **Target** (Ground truth values)
4. **Metadata**


```python
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=[
        'churn'
    ],  # Note: only a single Target column is allowed, use metadata columns and custom metrics for additional targets
    metadata=['customer_id', 'timestamp'],
)
id_column = (
    'customer_id'  # Indicates which column is your unique identifier for each event
)
timestamp_column = (
    'timestamp'  # Indicates which column is your timestamp for each event
)
```

## 4. Set a Model Task

Fiddler supports a variety of model tasks. In this case, we're adding a binary classification model.

For this, we'll create a ModelTask object and an additional ModelTaskParams object to specify the ordering of our positive and negative labels.

*For a detailed breakdown of all supported model tasks, click here.*


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=['no', 'yes'])
```

## 5. Add Your Model

Create a Model object and publish it to Fiddler, passing in
1. Your data sample
2. Your ModelSpec object
3. Your ModelTask and ModelTaskParams objects
4. Your ID and timestamp columns


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

## 6. Upload your feature impact values

**Note:** If skipping Steps #2 - #5 because the Simple Monitoring Quick Start model already exists, you will still need to instantiate the fdl.Model object. Uncomment the next cell and run it.



```python
# model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)  # Load the model
# model 
```

Uploading your own feature impact values requires:

1. A Python dict containing each input column defined in your Model's schema and its numeric value
2. A local reference to the fdl.Model

In this example, the feature impact scores are stored as JSON so first they are converted to a dict after reading from the JSON file.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=False
)
feature_impacts
```

Feature impact values can be updated at any time simply by setting the `update` parameter to True when calling [upload_feature_impact()](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact). The change takes effect immediately.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES_UPDATED, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=True
)
feature_impacts
```
# Fiddler User-Defined Feature Impact Quick Start Guide

In this notebook we demonstrate how to upload your own precomputed feature impact values to a Fiddler model. Previous versions of Fiddler required you create either a surrogate or user model artifact with which to calculate the feature impact values within Fiddler. Both surrogate and user model artifact require extra steps when onboarding a model and may be unnecessary if the feature impact values already exist. 


---

The documentation for the user-defined feature impact upload API can be found online [here](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact).

User-Defined Feature Impact is supported on Fiddler version 24.12+ using Fiddler Python client API versions 3.3 and higher.

**Please note that you may skip Steps #2 - #5 and resume at [Step #6](#section_06)** if you have already run Fiddler's [Simple Monitoring Quick Start Guide](https://docs.fiddler.ai/quickstart-notebooks/quick-start) and used the default values and sample data.

1. Connect to Fiddler - Initialization, create a project
2. Load a Data Sample
3. Define Your Model Specifications
4. Set a Model Task
5. Add Your Model
6. Upload Your Feature Impact Values

# 0. Imports


```python
%pip install -q fiddler-client

import pandas as pd
import fiddler as fdl

print(f"Running client version {fdl.__version__}")
```

## 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client API.


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

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv'
PATH_TO_FI_VALUES = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores.json'
PATH_TO_FI_VALUES_UPDATED = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores_alt.json'
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

## 2. Load a Data Sample

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list = sample_data_df.columns
sample_data_df
```

## 3. Define Your Model Specifications

In order to add your model to Fiddler, simply create a ModelSpec object with information about what each column of your data sample should used for.

Fiddler supports four column types:
1. **Inputs**
2. **Outputs** (Model predictions)
3. **Target** (Ground truth values)
4. **Metadata**


```python
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=[
        'churn'
    ],  # Note: only a single Target column is allowed, use metadata columns and custom metrics for additional targets
    metadata=['customer_id', 'timestamp'],
)
id_column = (
    'customer_id'  # Indicates which column is your unique identifier for each event
)
timestamp_column = (
    'timestamp'  # Indicates which column is your timestamp for each event
)
```

## 4. Set a Model Task

Fiddler supports a variety of model tasks. In this case, we're adding a binary classification model.

For this, we'll create a ModelTask object and an additional ModelTaskParams object to specify the ordering of our positive and negative labels.

*For a detailed breakdown of all supported model tasks, click here.*


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=['no', 'yes'])
```

## 5. Add Your Model

Create a Model object and publish it to Fiddler, passing in
1. Your data sample
2. Your ModelSpec object
3. Your ModelTask and ModelTaskParams objects
4. Your ID and timestamp columns


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

## 6. Upload your feature impact values

**Note:** If skipping Steps #2 - #5 because the Simple Monitoring Quick Start model already exists, you will still need to instantiate the fdl.Model object. Uncomment the next cell and run it.



```python
# model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)  # Load the model
# model 
```

Uploading your own feature impact values requires:

1. A Python dict containing each input column defined in your Model's schema and its numeric value
2. A local reference to the fdl.Model

In this example, the feature impact scores are stored as JSON so first they are converted to a dict after reading from the JSON file.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=False
)
feature_impacts
```

Feature impact values can be updated at any time simply by setting the `update` parameter to True when calling [upload_feature_impact()](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact). The change takes effect immediately.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES_UPDATED, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=True
)
feature_impacts
```
# Fiddler User-Defined Feature Impact Quick Start Guide

In this notebook we demonstrate how to upload your own precomputed feature impact values to a Fiddler model. Previous versions of Fiddler required you create either a surrogate or user model artifact with which to calculate the feature impact values within Fiddler. Both surrogate and user model artifact require extra steps when onboarding a model and may be unnecessary if the feature impact values already exist. 


---

The documentation for the user-defined feature impact upload API can be found online [here](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact).

User-Defined Feature Impact is supported on Fiddler version 24.12+ using Fiddler Python client API versions 3.3 and higher.

**Please note that you may skip Steps #2 - #5 and resume at [Step #6](#section_06)** if you have already run Fiddler's [Simple Monitoring Quick Start Guide](https://docs.fiddler.ai/quickstart-notebooks/quick-start) and used the default values and sample data.

1. Connect to Fiddler - Initialization, create a project
2. Load a Data Sample
3. Define Your Model Specifications
4. Set a Model Task
5. Add Your Model
6. Upload Your Feature Impact Values

# 0. Imports


```python
%pip install -q fiddler-client

import pandas as pd
import fiddler as fdl

print(f"Running client version {fdl.__version__}")
```

## 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client API.


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

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv'
PATH_TO_FI_VALUES = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores.json'
PATH_TO_FI_VALUES_UPDATED = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores_alt.json'
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

## 2. Load a Data Sample

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list = sample_data_df.columns
sample_data_df
```

## 3. Define Your Model Specifications

In order to add your model to Fiddler, simply create a ModelSpec object with information about what each column of your data sample should used for.

Fiddler supports four column types:
1. **Inputs**
2. **Outputs** (Model predictions)
3. **Target** (Ground truth values)
4. **Metadata**


```python
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=[
        'churn'
    ],  # Note: only a single Target column is allowed, use metadata columns and custom metrics for additional targets
    metadata=['customer_id', 'timestamp'],
)
id_column = (
    'customer_id'  # Indicates which column is your unique identifier for each event
)
timestamp_column = (
    'timestamp'  # Indicates which column is your timestamp for each event
)
```

## 4. Set a Model Task

Fiddler supports a variety of model tasks. In this case, we're adding a binary classification model.

For this, we'll create a ModelTask object and an additional ModelTaskParams object to specify the ordering of our positive and negative labels.

*For a detailed breakdown of all supported model tasks, click here.*


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=['no', 'yes'])
```

## 5. Add Your Model

Create a Model object and publish it to Fiddler, passing in
1. Your data sample
2. Your ModelSpec object
3. Your ModelTask and ModelTaskParams objects
4. Your ID and timestamp columns


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

## 6. Upload your feature impact values

**Note:** If skipping Steps #2 - #5 because the Simple Monitoring Quick Start model already exists, you will still need to instantiate the fdl.Model object. Uncomment the next cell and run it.



```python
# model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)  # Load the model
# model 
```

Uploading your own feature impact values requires:

1. A Python dict containing each input column defined in your Model's schema and its numeric value
2. A local reference to the fdl.Model

In this example, the feature impact scores are stored as JSON so first they are converted to a dict after reading from the JSON file.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=False
)
feature_impacts
```

Feature impact values can be updated at any time simply by setting the `update` parameter to True when calling [upload_feature_impact()](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact). The change takes effect immediately.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES_UPDATED, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=True
)
feature_impacts
```
# Fiddler User-Defined Feature Impact Quick Start Guide

In this notebook we demonstrate how to upload your own precomputed feature impact values to a Fiddler model. Previous versions of Fiddler required you create either a surrogate or user model artifact with which to calculate the feature impact values within Fiddler. Both surrogate and user model artifact require extra steps when onboarding a model and may be unnecessary if the feature impact values already exist. 


---

The documentation for the user-defined feature impact upload API can be found online [here](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact).

User-Defined Feature Impact is supported on Fiddler version 24.12+ using Fiddler Python client API versions 3.3 and higher.

**Please note that you may skip Steps #2 - #5 and resume at [Step #6](#section_06)** if you have already run Fiddler's [Simple Monitoring Quick Start Guide](https://docs.fiddler.ai/quickstart-notebooks/quick-start) and used the default values and sample data.

1. Connect to Fiddler - Initialization, create a project
2. Load a Data Sample
3. Define Your Model Specifications
4. Set a Model Task
5. Add Your Model
6. Upload Your Feature Impact Values

# 0. Imports


```python
%pip install -q fiddler-client

import pandas as pd
import fiddler as fdl

print(f"Running client version {fdl.__version__}")
```

## 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client API.


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

# Sample data hosted on GitHub
PATH_TO_SAMPLE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv'
PATH_TO_FI_VALUES = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores.json'
PATH_TO_FI_VALUES_UPDATED = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/custom_feature_impact_scores_alt.json'
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

## 2. Load a Data Sample

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.
  
In order to get insights into the model's performance, **Fiddler needs a small sample of data** to learn the schema of incoming data.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list = sample_data_df.columns
sample_data_df
```

## 3. Define Your Model Specifications

In order to add your model to Fiddler, simply create a ModelSpec object with information about what each column of your data sample should used for.

Fiddler supports four column types:
1. **Inputs**
2. **Outputs** (Model predictions)
3. **Target** (Ground truth values)
4. **Metadata**


```python
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=[
        'churn'
    ],  # Note: only a single Target column is allowed, use metadata columns and custom metrics for additional targets
    metadata=['customer_id', 'timestamp'],
)
id_column = (
    'customer_id'  # Indicates which column is your unique identifier for each event
)
timestamp_column = (
    'timestamp'  # Indicates which column is your timestamp for each event
)
```

## 4. Set a Model Task

Fiddler supports a variety of model tasks. In this case, we're adding a binary classification model.

For this, we'll create a ModelTask object and an additional ModelTaskParams object to specify the ordering of our positive and negative labels.

*For a detailed breakdown of all supported model tasks, click here.*


```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION

task_params = fdl.ModelTaskParams(target_class_order=['no', 'yes'])
```

## 5. Add Your Model

Create a Model object and publish it to Fiddler, passing in
1. Your data sample
2. Your ModelSpec object
3. Your ModelTask and ModelTaskParams objects
4. Your ID and timestamp columns


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

## 6. Upload your feature impact values

**Note:** If skipping Steps #2 - #5 because the Simple Monitoring Quick Start model already exists, you will still need to instantiate the fdl.Model object. Uncomment the next cell and run it.



```python
# model = fdl.Model.from_name(name=MODEL_NAME, project_id=project.id)  # Load the model
# model 
```

Uploading your own feature impact values requires:

1. A Python dict containing each input column defined in your Model's schema and its numeric value
2. A local reference to the fdl.Model

In this example, the feature impact scores are stored as JSON so first they are converted to a dict after reading from the JSON file.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=False
)
feature_impacts
```

Feature impact values can be updated at any time simply by setting the `update` parameter to True when calling [upload_feature_impact()](https://docs.fiddler.ai/python-client-3-x/api-methods-30#upload_feature_impact). The change takes effect immediately.


```python
fi_values_series = pd.read_json(PATH_TO_FI_VALUES_UPDATED, typ='series')
fi_values_dict = fi_values_series.to_dict()

feature_impacts = model.upload_feature_impact(
    feature_impact_map=fi_values_dict, update=True
)
feature_impacts
```
