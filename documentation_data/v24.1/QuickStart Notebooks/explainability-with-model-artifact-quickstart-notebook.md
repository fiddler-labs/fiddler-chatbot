---
title: "Explainability with Model Artifact"
slug: "explainability-with-model-artifact-quickstart-notebook"
excerpt: "Quickstart Notebook"
hidden: false
metadata: 
  title: "Quickstart: Explainability with Model Artifact | Fiddler Docs"
  description: "This document provides a guide on how to onboard a model in Fiddler with its model artifact to achieve high-fidelity explanations."
  image: []
  robots: "index"
createdAt: "Tue Dec 13 2022 22:00:20 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 23 2024 20:53:35 GMT+0000 (Coordinated Universal Time)"
---
This guide will walk you through the basic steps required to onboard a model in Fiddler with its model artifact.  When Fiddler is provided with the actual model artifact, it can produce high-fidelity explanations. In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Click the following link to get started using Google Colab:

<div class="colab-box">
    <a href="https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/24.1/Fiddler_Quickstart_Add_Model_Artifact.ipynb" target="_blank">
        <div>
            Open in Google Colab →
        </div>
    </a>
    <div>
            <img src="https://colab.research.google.com/img/colab_favicon_256px.png" />
    </div>
</div>
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
# Adding a Model Artifact

In this notebook, we present the steps for onboarding a model with its model artifact.  When Fiddler is provided with your real model artifact, it can produce high-fidelity explanations.  In contrast, models within Fiddler that use a surrogate model or no model artifact at all provide approximative explainability or no explainability at all.

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's NLP monitoring ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Publish production events
5. Get insights (including high-fidelity explainability, or XAI!)

# 0. Imports


```python
!pip install -q fiddler-client

import fiddler as fdl
import pandas as pd
import yaml
import datetime
import time
from IPython.display import clear_output

print(f"Running Fiddler client version {fdl.__version__}")
```

# 1. Connect to Fiddler

Before you can add information about your model with Fiddler, you'll need to connect using our Python client.

---

**We need a few pieces of information to get started.**
1. The URL you're using to connect to Fiddler
2. Your organization ID
3. Your authorization token

The latter two of these can be found by pointing your browser to your Fiddler URL and navigating to the **Settings** page.


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''
```

Now just run the following code block to connect the client to your Fiddler environment.


```python
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's [create_project](https://docs.fiddler.ai/reference/clientcreate_project) function.


```python
PROJECT_ID = 'simple_model_artifact_upload'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts churn for our customers**.  
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/churn_baseline.csv'

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler.
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The `DatasetInfo` object you just created


```python
DATASET_ID = 'churn_data'

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

Within your Fiddler environment's UI, you should now be able to see the newly created dataset within your project.

## 3. Upload your model package

Now it's time to upload your model package to Fiddler.  To complete this step, we need to ensure we have 2 assets in a directory.  It doesn't matter what this directory is called, but for this example we will call it **/model**.


```python
import os
os.makedirs("model")
```

***Your model package directory will need to contain:***
1. A **package.py** file which explains to Fiddler how to invoke your model's prediction endpoint
2. And the **model artifact** itself
3. A **requirements.txt** specifying which python libraries need by package.py

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
# Specify task
model_task = 'binary'

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

elif model_task == 'ranking':
    model_task = fdl.ModelTask.RANKING
    
metadata_cols = ['gender']
decision_cols = ['decision']
feature_columns = ['creditscore', 'geography', 'age', 'tenure',
       'balance', 'numofproducts', 'hascrcard', 'isactivemember',
       'estimatedsalary']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    model_task=model_task,
    target='churn', 
    categorical_target_class_details='yes',
    features=feature_columns,
    decision_cols = decision_cols,
    metadata_cols = metadata_cols,
    outputs=['predicted_churn'],
    display_name='Random Forest Model',
    description='This is models customer bank churn'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'customer_churn_rf'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

### 3.2 Create the **package.py** file

The contents of the cell below will be written into our ***package.py*** file.  This is the step that will be most unique based on model type, framework and use case.  The model's ***package.py*** file also allows for preprocessing transformations and other processing before the model's prediction endpoint is called.  For more information about how to create the ***package.py*** file for a variety of model tasks and frameworks, please reference the [Uploading a Model Artifact](https://docs.fiddler.ai/docs/uploading-a-model-artifact#packagepy-script) section of the Fiddler product documentation.


```python
%%writefile model/package.py

import pandas as pd
from pathlib import Path
import os
from sklearn.ensemble import RandomForestClassifier
import pickle as pkl

 
PACKAGE_PATH = Path(__file__).parent
TARGET = 'churn'
PREDICTION = 'predicted_churn'

class Random_Forest:


    def __init__(self, model_path, output_column=None):
        """
        :param model_path: The directory where the model is saved.
        :param output_column: list of column name(s) for the output.
        """
        self.model_path = model_path
        self.output_column = output_column
        
       
        file_path = os.path.join(self.model_path, 'model.pkl')
        with open(file_path, 'rb') as file:
            self.model = pkl.load(file)
    
    
    def predict(self, input_df):
        return pd.DataFrame(
            self.model.predict_proba(input_df.loc[:, input_df.columns != TARGET])[:,1], 
            columns=self.output_column)
    

def get_model():
    return Random_Forest(model_path=PACKAGE_PATH, output_column=[PREDICTION])
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model .pkl file*) is also present in the model package directory as well as any dependencies called out in a *requirements.txt* file.  The following cell will move this model's pkl file and requirements.txt file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model.pkl", "model/model.pkl")
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/requirements.txt", "model/requirements.txt")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/python-39:1.1.0",  
                                    cpu=100,
                                    memory=256,
                                    replicas=1)
```

### Finally, upload the model package directory

Once the model's artifact is in the */model* directory along with the **pacakge.py** file and requirments.txt the model package directory can be uploaded to Fiddler.


```python
client.add_model_artifact(model_dir='model/', project_id=PROJECT_ID, model_id=MODEL_ID, deployment_params=DEPLOYMENT_PARAMETERS)
```

Within your Fiddler environment's UI, you should now be able to see the newly created model.

# 4. Publish production events

Your model artifact is uploaded.  Now it's time to start publishing some production data! 

Fiddler will **monitor this data and compare it to your baseline to generate powerful insights into how your model is behaving**.  

With the model artifact available to Fiddler, **high-fidelity explanations are also avaialbe**.


---


Each record sent to Fiddler is called **an event**.  An event is just **a dictionary that maps column names to column values**.
  
Let's load in some sample events from a CSV file.  Then we can create an artificial timestamp for the events and publish them to fiddler one by one in a streaming fashion using the Fiddler client's [publish_event](https://docs.fiddler.ai/reference/clientpublish_event) function.


```python
PATH_TO_EVENTS_CSV = 'https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/data/hawaii_drift_demo_large.csv'

event_log = pd.read_csv(PATH_TO_EVENTS_CSV)
event_log
```


```python
NUM_EVENTS_TO_SEND = 11500

FIVE_MINUTES_MS = 300000
ONE_DAY_MS = 8.64e+7
NUM_DAYS_BACK_TO_START=39 #set the start of the event data publishing this many days in the past
start_date = round(time.time() * 1000) - (ONE_DAY_MS * NUM_DAYS_BACK_TO_START) 
print(datetime.datetime.fromtimestamp(start_date/1000.0))
```


```python
def event_generator_df():
    for ind, row in event_log.iterrows():
        event_dict = dict(row)
        event_id = event_dict.pop('event_id')
        event_time = start_date + ind * FIVE_MINUTES_MS #publish an event every FIVE_MINUTES_MS
        yield event_id, event_dict, event_time
        
event_queue_df = event_generator_df()

def get_next_event_df():
    return next(event_queue_df)
```


```python
for ind in range(NUM_EVENTS_TO_SEND):
    event_id_tmp, event_dict, event_time = get_next_event_df()
   
    result = client.publish_event(PROJECT_ID,
                                  MODEL_ID,
                                  event_dict,
                                  event_timestamp=event_time,
                                  event_id= event_id_tmp,
                                  update_event= False)
    
    readable_timestamp = datetime.datetime.fromtimestamp(event_time/1000.0)
    clear_output(wait = True)
    
    print(f'Sending {ind+1} / {NUM_EVENTS_TO_SEND} \n{readable_timestamp} UTC: \n{event_dict}')
    time.sleep(0.001)
```

# 5. Get insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
