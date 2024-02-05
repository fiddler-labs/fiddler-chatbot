# Onboard a Credit Approval Model to Evaluate Fairness

In this notebook, we present the steps for onboarding a model to evaluate model fairness.  

Fiddler is the pioneer in enterprise Model Performance Management (MPM), offering a unified platform that enables Data Science, MLOps, Risk, Compliance, Analytics, and LOB teams to **monitor, explain, analyze, and improve ML deployments at enterprise scale**. 
Obtain contextual insights at any stage of the ML lifecycle, improve predictions, increase transparency and fairness, and optimize business revenue.

---

You can experience Fiddler's Fairness Offering ***in minutes*** by following these four quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Upload a model package directory containing the **1) package.py and 2) model artifact**
4. Get Fairness insights

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
PROJECT_ID = 'credit_approval'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload a baseline dataset

In this example, we'll be considering the case where we're a bank and we have **a model that predicts credit approval worthiness**.
  
In order to get insights into the model's performance, **Fiddler needs a small  sample of data that can serve as a baseline** for making comparisons with data in production.


---


*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/docs/designing-a-baseline-dataset).*


```python
PATH_TO_BASELINE_CSV = 'https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/intersectionally_unfair_baseline.csv'

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
DATASET_ID = 'intersectionally_unfair'

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
3. (Optional) A **requirements.txt** specifying which python libraries need by package.py.  This example doesn't require any additional libraries to be installed so a requirements.txt file is not needed here.

---

### 3.1.a  Create the **model_info** object 

This is done by creating our [model_info](https://docs.fiddler.ai/reference/fdlmodelinfo) object.



```python
metadata_cols = ['gender','race']
feature_columns = ['FLAG_OWN_CAR', 'FLAG_OWN_REALTY', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
       'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'DAYS_BIRTH', 'DAYS_EMPLOYED',
       'CNT_FAM_MEMBERS', 'income', 'paid_off', '#_of_pastdues', 'no_loan']

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(PROJECT_ID, DATASET_ID),
    target='target', 
    features=feature_columns,
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION,
    metadata_cols = metadata_cols,
    outputs=['Approve_probability_of_credit_request'],
    display_name='Credit model with systemic racial and gender bias',
    description='logistic reg model'
)

model_info
```

### 3.1.b Add Model Information to Fiddler


```python
MODEL_ID = 'intersectionally_unfair'

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

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class SklearnModelPackage:

    def __init__(self):
        self.is_classifier = True
        self.is_multiclass = False
        self.output_columns = ['Approve_probability_of_credit_request']
        with open(PACKAGE_PATH / 'model_unfair.pkl', 'rb') as infile:
            self.model = pickle.load(infile)

    def predict(self, input_df):
        if self.is_classifier:
            if self.is_multiclass:
                predict_fn = self.model.predict_proba
            else:
                def predict_fn(x):
                    return self.model.predict_proba(x)[:, 1]
        else:
            predict_fn = self.model.predict
        return pd.DataFrame(predict_fn(input_df), columns=self.output_columns)

def get_model():
    return SklearnModelPackage()
```

### 3.3  Ensure your model's artifact is in the **/model** directory

Make sure your model artifact (*e.g. the model_unfair.pkl file*) is also present in the model package directory.  The following cell will move this model's pkl file into our */model* directory.


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_unfair.pkl", "model/model_unfair.pkl")
```

### 3.4 Define Model Parameters 

This is done by creating our [DEPLOYMENT_PARAMETERS](https://docs.fiddler.ai/reference/fdldeploymentparams) object.


```python
DEPLOYMENT_PARAMETERS = fdl.DeploymentParams(image_uri="md-base/python/machine-learning:1.0.0",  
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

# 4. Get Fairness insights

**You're all done!**
  
Now just head to your Fiddler environment's UI and explore the model's fairness metrics.


Alternatively, you can also run fairness from the Fiddler Python client:


```python
protected_features = ['gender', 'race']
positive_outcome = 1

fairness_metrics = client.get_fairness(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=200),
    protected_features=protected_features,
    positive_outcome=positive_outcome,
    score_threshold=0.6
)
fairness_metrics
```



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
