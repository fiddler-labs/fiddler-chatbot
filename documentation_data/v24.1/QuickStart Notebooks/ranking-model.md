---
title: "Ranking Monitoring Example"
slug: "ranking-model"
excerpt: ""
hidden: false
metadata: 
  title: "Quickstart: Ranking Monitoring | Fiddler Docs"
  description: "This document explains how Fiddler enables monitoring and explainability for a Ranking model using a dataset from Expedia that includes shopping and purchase data with information on price competitiveness."
  image: []
  robots: "index"
createdAt: "Fri Jun 16 2023 21:38:41 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 23 2024 20:53:52 GMT+0000 (Coordinated Universal Time)"
---
This notebook will show you how Fiddler enables monitoring and explainability for a Ranking model. This notebook uses a dataset from Expedia that includes shopping and purchase data with information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website.

Click the following link to try it now with Google Colab:

<div class="colab-box">
    <a href="https://colab.research.google.com/github/fiddler-labs/fiddler-examples/blob/main/quickstart/24.1/Fiddler_Quickstart_Ranking_Model.ipynb" target="_blank">
        <div>
            Open in Google Colab →
        </div>
    </a>
    <div>
            <img src="https://colab.research.google.com/img/colab_favicon_256px.png" />
    </div>
</div>
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'danny3_search_ranking'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
df.head()
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to sotre your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://github.com/fiddler-labs/fiddler-examples/blob/main/quickstart/models/ranking_model.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Send Traffic For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs.tail()
```


```python
#timeshift to move the data to last 29 days
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
```


```python
df_logs_grouped.head(2)
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 7. Get insights


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
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'search_ranking_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
baseline_df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': baseline_df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to store your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(baseline_df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_ranking.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Publish Events For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs
```


```python
#timeshift the data to be current day
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
df_logs_grouped
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 6. Get insights


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
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'search_ranking_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
baseline_df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': baseline_df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to store your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(baseline_df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_ranking.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Publish Events For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs
```


```python
#timeshift the data to be current day
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
df_logs_grouped
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 6. Get insights


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
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'search_ranking_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
baseline_df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': baseline_df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to store your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(baseline_df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_ranking.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Publish Events For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs
```


```python
#timeshift the data to be current day
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
df_logs_grouped
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 6. Get insights


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
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'search_ranking_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
baseline_df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': baseline_df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to store your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(baseline_df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_ranking.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Publish Events For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs
```


```python
#timeshift the data to be current day
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
df_logs_grouped
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 6. Get insights


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
# Fiddler Ranking Model Quick Start Guide

Fiddler offer the ability for your teams to observe you ranking models to understand thier performance and catch issues like data drift before they affect your applications.

# Quickstart: Expedia Search Ranking
The following dataset is coming from Expedia. It includes shopping and purchase data as well as information on price competitiveness. The data are organized around a set of “search result impressions”, or the ordered list of hotels that the user sees after they search for a hotel on the Expedia website. In addition to impressions from the existing algorithm, the data contain impressions where the hotels were randomly sorted, to avoid the position bias of the existing algorithm. The user response is provided as a click on a hotel. From: https://www.kaggle.com/c/expedia-personalized-sort/overview

# 0. Imports


```python
!pip install lightgbm
```


```python
import pandas as pd
import lightgbm as lgb
import numpy as np
import time as time
import datetime
```

# 1. Connect to Fiddler and Create a Project
First we install and import the Fiddler Python client.


```python
!pip install -q fiddler-client
import fiddler as fdl
print(f"Running client version {fdl.__version__}")
```

Before you can add information about your model with Fiddler, you'll need to connect using our API client.

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

Next we run the following code block to connect to the Fiddler API.


```python
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Once you connect, you can create a new project by specifying a unique project ID in the client's `create_project` function.


```python
PROJECT_ID = 'search_ranking_example'

if not PROJECT_ID in client.list_projects():
    print(f'Creating project: {PROJECT_ID}')
    client.create_project(PROJECT_ID)
else:
    print(f'Project: {PROJECT_ID} already exists')
```

# 2. Upload the Baseline Dataset

Now we retrieve the Expedia Dataset as a baseline for this model.


```python
baseline_df = pd.read_csv("https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_baseline_data.csv")
baseline_df
```

Fiddler uses this baseline dataset to keep track of important information about your data.
  
This includes **data types**, **data ranges**, and **unique values** for categorical variables.

---

You can construct a `DatasetInfo` object to be used as **a schema for keeping track of this information** by running the following code block.


```python
dataset_info = fdl.DatasetInfo.from_dataframe(df=baseline_df, max_inferred_cardinality=100)
dataset_info
```

Then use the client's [upload_dataset](https://docs.fiddler.ai/reference/clientupload_dataset) function to send this information to Fiddler!
  
*Just include:*
1. A unique dataset ID
2. The baseline dataset as a pandas DataFrame
3. The [DatasetInfo](https://docs.fiddler.ai/reference/fdldatasetinfo) object you just created


```python
DATASET_ID = 'expedia_data'
client.upload_dataset(project_id=PROJECT_ID,
                      dataset={'baseline': baseline_df},
                      dataset_id=DATASET_ID,
                      info=dataset_info)
```

# 3. Share Model Metadata and Upload the Model


```python
#create model directory to store your model files
import os
model_dir = "model"
os.makedirs(model_dir)
```

### 3.a Adding model metadata to Fiddler
To add a Ranking model you must specify the ModelTask as `RANKING` in the model info object.  

Additionally, you must provide the `group_by` argument that corresponds to the query search id. This `group_by` column should be present either in:
- `features` : if it is used to build and run the model
- `metadata_cols` : if not used by the model 

Optionally, you can give a `ranking_top_k` number (default is 50). This will be the number of results within each query to take into account while computing the performance metrics in monitoring.  

Unless the prediction column was part of your baseline dataset, you must provide the minimum and maximum values predictions can take in a dictionary format (see below).  

If your target is categorical (string), you need to provide the `categorical_target_class_details` argument. If your target is numerical and you don't specify this argument, Fiddler will infer it.   

This will be the list of possible values for the target **ordered**. The first element should be the least relevant target level, the last element should be the most relevant target level.


```python
target = 'binary_relevance'
features = list(baseline_df.drop(columns=['binary_relevance', 'score', 'graded_relevance', 'position']).columns)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=client.get_dataset_info(project_id=PROJECT_ID, dataset_id=DATASET_ID),
    target=target,
    features=features,
    input_type=fdl.ModelInputType.TABULAR,
    model_task=fdl.ModelTask.RANKING,
    outputs={'score':[-5.0, 3.0]},
    group_by='srch_id',
    ranking_top_k=20,
    categorical_target_class_details=[0, 1]
)

# inspect model info and modify as needed
model_info
```


```python
MODEL_ID = 'expedia_model'

if not MODEL_ID in client.list_models(project_id=PROJECT_ID):
    client.add_model(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        model_id=MODEL_ID,
        model_info=model_info
    )
else:
    print(f'Model: {MODEL_ID} already exists in Project: {PROJECT_ID}. Please use a different name.')
```

### 3.b Create a Model Wrapper Script

Package.py is the interface between Fiddler’s backend and your model. This code helps Fiddler to understand the model, its inputs and outputs.

You need to implement three parts:
- init: Load the model, and any associated files such as feature transformers.
- transform: If you use some pre-processing steps not part of the model file, transform the data into a format that the model recognizes.
- predict: Make predictions using the model.


```python
%%writefile model/package.py

import pickle
from pathlib import Path
import pandas as pd

PACKAGE_PATH = Path(__file__).parent

class ModelPackage:

    def __init__(self):
        """
         Load the model file and any pre-processing files if needed.
        """
        self.output_columns = ['score']
        
        with open(PACKAGE_PATH / 'model.pkl', 'rb') as infile:
            self.model = pickle.load(infile)
    
    def transform(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Use pre-processing file to transform the data if needed. 
        In this example we don't need to transform the data.
        Outputs a pandas DataFrame object containing transformed data.
        """
        return input_df
    
    def predict(self, input_df):
        """
        Accepts a pandas DataFrame object containing rows of raw feature vectors. 
        Outputs a pandas DataFrame object containing the model predictions whose column labels 
        must match the output column names in model info.
        """
        transformed_df = self.transform(input_df)
        pred = self.model.predict(transformed_df)
        return pd.DataFrame(pred, columns=self.output_columns)
    
def get_model():
    return ModelPackage()
```

### 3.c Retriving the model files 

To explain a model's inner workigs we need to upload the model artifacts. We will retrive a pre-trained model from the Fiddler Repo that was trained with **lightgbm 2.3.0**


```python
import urllib.request
urllib.request.urlretrieve("https://raw.githubusercontent.com/fiddler-labs/fiddler-examples/main/quickstart/models/model_ranking.pkl", "model/model.pkl")
```

### 3.d Upload the model files to Fiddler


Now as a final step in the setup you can upload the model artifact files using `add_model_artifact`. 
   - The `model_dir` is the path for the folder containing the model file(s) and the `package.py` from ther last step.
   - Since each model artifact uploaded to Fiddler gets deployed in its own container, the [deployment params](https://docs.fiddler.ai/reference/fdldeploymentparams) allow us to specify the compute needs and library set of the container.


```python
#Uploading Model files
deployment_params = fdl.DeploymentParams(
    image_uri="md-base/python/machine-learning:1.1.0",
    cpu=100,
    memory=256,
    replicas=1,
)

client.add_model_artifact(
    model_dir=model_dir, 
    project_id=PROJECT_ID, 
    model_id=MODEL_ID,
    deployment_params=deployment_params
)
```

# 5. Publish Events For Monitoring

### 5.a Gather and prepare Production Events
This is the production log file we are going to upload in Fiddler.


```python
df_logs = pd.read_csv('https://media.githubusercontent.com/media/fiddler-labs/fiddler-examples/main/quickstart/data/expedia_logs.csv')
df_logs
```


```python
#timeshift the data to be current day
df_logs['time_epoch'] = df_logs['time_epoch'] + (float(time.time()) - df_logs['time_epoch'].max())
```

For ranking, we need to ingest all events from a given query or search ID together. To do that, we need to transform the data to a grouped format.  
You can use the `convert_flat_csv_data_to_grouped` utility function to do the transformation.



```python
df_logs_grouped = fdl.utils.pandas_helper.convert_flat_csv_data_to_grouped(input_data=df_logs, group_by_col='srch_id')
df_logs_grouped
```

### 5.b Publish events


```python
client.publish_events_batch(project_id=PROJECT_ID,
                            model_id=MODEL_ID,
                            batch_source=df_logs_grouped,
                            timestamp_field='time_epoch')
```

# 6. Get insights


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
