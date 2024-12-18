---
icon: notebook
---

# ML Monitoring - Model Versions

This guide will walk you through how you can use Model Versions feature in setting up multiple versions of the same model, **using sample data provided by Fiddler**.

Click [this link to get started using Google Colab →](https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Model_Versions.ipynb)

<div align="left">

<figure><img src="https://colab.research.google.com/img/colab_favicon_256px.png" alt="Google Colab" width="188"><figcaption></figcaption></figure>

</div>

Or download the notebook directly from [GitHub](https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/latest/Fiddler_Quickstart_Model_Versions.ipynb).

{% include "../.gitbook/includes/main-doc-footer.md" %}

# Model Versions

In this notebook, we present the steps for creating addtional versions of a model.  When a model is onboarded to Fiddler it is considered version 1 by default. To make signifacant changes to an existing model, such as altering the model schema, a new version of the model must be created. A model can have as many versions as desired and each can be live simultaneously or retained for historical viewing. 

This notebook is an example of how changes can be made in a `ModelSchema` and how Fiddler maintains them using versioning.

---

Model versioning docs can be referenced [here](https://docs.fiddler.ai/product-guide/monitoring-platform/model-versions) 

Model Versions are supported on Fiddler Python client version 3.1.0 and above using Python version 3.10+.

You can experience Fiddler's Model Versioning in minutes by following these quick steps:

1. Connect to Fiddler
2. Load a Data Sample
3. Create a Model: first version with no ModelTask
4. Second Version: target class and binary classification task & defined threshold
5. Third Version: change the datatype of a column and delete a column 
6. Fourth Version: change the column names
7. Fifth version: update column value range
8. Update Version Name
9. Delete a Model Version

# 0. Imports


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
PROJECT_NAME = 'quickstart_examples'
MODEL_NAME = 'bank_churn_model_versions'
DATASET_NAME = 'baseline_dataset'

PATH_TO_SAMPLE_CSV = "https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/v3/churn_data_sample.csv"
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

Load the sample dataset, store the list of columns, and create a subset of input columns (model features) for later use.


```python
sample_data_df = pd.read_csv(PATH_TO_SAMPLE_CSV)
column_list = sample_data_df.columns
input_columns = list(
    column_list.drop(['predicted_churn', 'churn', 'customer_id', 'timestamp'])
)

sample_data_df
```

## 3. Create a Model

Create the first version of model in the project with NOT_SET task

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/model_versions_1.png" />
        </td>
    </tr>
</table>


```python
# Note the model version label is semantic and can be set to any desired alphanumeric string
# **** rules? ****
version_v1 = 'v1'

# Define the model specification, the role each column plays in the Fiddler model
model_spec = fdl.ModelSpec(
    inputs=input_columns,
    outputs=['predicted_churn'],
    targets=['churn'],
    metadata=['customer_id', 'timestamp'],
    decisions=[],
    custom_features=[],
)

try:
    model_v1 = fdl.Model.from_name(
        name=MODEL_NAME, project_id=project.id, version=version_v1
    )

    print(
        f'Loaded existing model with id = {model_v1.id}, name = {model_v1.name} and version = {model_v1.version}'
    )
except fdl.NotFound:
    model_v1 = fdl.Model.from_data(
        source=sample_data_df,
        name=MODEL_NAME,
        version=version_v1,
        project_id=project.id,
        spec=model_spec,
        task=fdl.ModelTask.NOT_SET,  # this sets the modeltask as NOT SET
    )

    model_v1.create()  # this creates the model
    print(
        f'New model created with id = {model_v1.id}, name = {model_v1.name} and version = {model_v1.version}'
    )
```

## 4. Second Version

Add a second Model version with binary classification task.

Update the version and provide target class and binary classification task & threshold.



```python
version_v2 = 'v2'

task_params = fdl.ModelTaskParams(
    binary_classification_threshold=0.5,
    target_class_order=['no', 'yes'],
)

try:
    model_v2 = fdl.Model.from_name(
        name=MODEL_NAME, project_id=project.id, version=version_v2
    )

    print(
        f'Loaded existing model with id = {model_v2.id}, name = {model_v2.name} and version = {model_v2.version}'
    )
except fdl.NotFound:
    model_v2 = model_v1.duplicate(version=version_v2)
    model_v2.task_params = task_params
    model_v2.task = fdl.ModelTask.BINARY_CLASSIFICATION

    model_v2.create()
    print(
        f'New model created with id = {model_v2.id}, name = {model_v2.name} and version = {model_v2.version}'
    )
```

## 5. Third Version

For this third version of the Model we are:
1. Removing the input parameter "tenure"
2. Changing the datatype of column "geography" from Category to String


```python
version_v3 = 'v3'

try:
    model_v3 = fdl.Model.from_name(
        name=MODEL_NAME, project_id=project.id, version=version_v3
    )

    print(
        f'Loaded existing model with id = {model_v3.id}, name = {model_v3.name} and version = {model_v3.version}'
    )
except fdl.NotFound:
    model_v3 = model_v2.duplicate(version=version_v3)

    # Remove the "tenure" column from the Model
    del model_v3.schema[
        'tenure'
    ]  # this deletes the tenure column from the Model schema and subsequently the inputs
    input_columns.remove('tenure')
    model_v3.spec.inputs = input_columns

    # Categorical column "hascrcard" is currently numerical, changing it to categorical
    model_v3.schema['hascrcard'].min = (
        None  # Removing min and mix of a numerical column before changing datatype
    )
    model_v3.schema['hascrcard'].max = None
    model_v3.schema['hascrcard'].data_type = fdl.DataType.BOOLEAN
    model_v3.schema['hascrcard'].categories = [True, False]

    model_v3.create()
    print(
        f'New model created with id = {model_v3.id}, name = {model_v3.name} and version = {model_v3.version}'
    )
```

## 6. Fourth Version

Add a fourth version with a change in schema by changing the name of the columns


```python
version_v4 = 'v4'

try:
    model_v4 = fdl.Model.from_name(
        name=MODEL_NAME, project_id=project.id, version=version_v4
    )

    print(
        f'Loaded existing model with id = {model_v4.id}, name = {model_v4.name} and version = {model_v4.version}'
    )
except fdl.NotFound:
    model_v4 = model_v3.duplicate(version=version_v4)
    model_v4.schema['age'].name = 'Age'  # we are renaming the column names
    model_v4.schema['creditscore'].name = 'CreditScore'
    model_v4.schema['geography'].name = 'Geography'
    model_v4.schema['balance'].name = 'BalanceNew'
    model_v4.schema['numofproducts'].name = 'NumOfProducts'
    model_v4.schema['hascrcard'].name = 'HasCrCard'
    model_v4.schema['isactivemember'].name = 'IsActiveMember'
    model_v4.schema['estimatedsalary'].name = 'EstimatedSalary'
    model_v4.spec.inputs = [
        'CreditScore',
        'Geography',
        'Age',
        'BalanceNew',
        'NumOfProducts',
        'HasCrCard',
        'IsActiveMember',
        'EstimatedSalary',
    ]

    model_v4.create()
    print(
        f'New model created with id = {model_v4.id}, name = {model_v4.name} and version = {model_v4.version}'
    )
```

## 7. Fifth Version

Add a fifth version with where the schema is changing by increasing the max limit of the balance field.


```python
version_v5 = 'v5'

try:
    model_v5 = fdl.Model.from_name(
        name=MODEL_NAME, project_id=project.id, version=version_v5
    )
    print(
        f'Loaded existing model with id = {model_v5.id}, name = {model_v5.name} and version = {model_v5.version}'
    )
except fdl.NotFound as e:
    model_v5 = model_v4.duplicate(version=version_v5)
    model_v5.schema['Age'].min = (
        18  # This sets the min and max of the age column, overriding what was inferred from the sample data
    )
    model_v5.schema['Age'].max = 85

    model_v5.schema['BalanceNew'].max = (
        1250000  # This sets the max value for the balance column, overriding what was inferred from the sample data
    )

    model_v5.create()
    print(
        f'New model created with id = {model_v5.id}, name = {model_v5.name} and version = {model_v5.version}'
    )
```

## 8. Update version name


```python
model_v4.version = 'v4-old'  # Rename the existing version name to 'v4-old'
model_v4.update()

print(f'Model version updated to: {model_v4.version}')
```

<table>
    <tr>
        <td>
            <img src="https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/images/model_versions_3.png" />
        </td>
    </tr>
</table>

## 9. Delete Model Version

Delete version v5 of the Model


```python
model_delete_job = model_v5.delete()  # this deletes a specified version of the model

# Uncomment the line below to wait for the job to finish, otherwise it will run in the background.
# You can check the status on the Jobs page in the Fiddler UI or use the job ID to query the job status via the API.
# model_delete_job.wait()
```



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
