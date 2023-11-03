# Fiddler DIY Quickstart Working Notebook

You can start using Fiddler ***in minutes*** by following these five quick steps:

1. Connect to Fiddler
2. Upload a baseline dataset
3. Add your model with Fiddler
4. Publish production events
5. Get insights

## 0. Imports


```python
!pip install -q fiddler-client;

import numpy as np
import pandas as pd
import fiddler as fdl

print(f"Running client version {fdl.__version__}")
```

## 1. Connect to Fiddler


```python
URL = ''  # Make sure to include the full URL (including https://).
ORG_ID = ''
AUTH_TOKEN = ''

client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```


```python
PROJECT_ID = "quickstart_diy"

client.create_project(PROJECT_ID)
```

## 2. Upload a baseline dataset

*For more information on how to design a baseline dataset, [click here](https://docs.fiddler.ai/pages/user-guide/data-science-concepts/monitoring/designing-a-baseline-dataset/).*


```python
PATH_TO_BASELINE_CSV = #

baseline_df = pd.read_csv(PATH_TO_BASELINE_CSV)
baseline_df
```


```python
dataset_info = fdl.DatasetInfo.from_dataframe(baseline_df, max_inferred_cardinality=100)
dataset_info
```


```python
DATASET_ID = #

client.upload_dataset(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    dataset={
        'baseline': baseline_df
    },
    info=dataset_info
)
```

## 3. Add your model



```python
# Specify task
model_task = #

if model_task == 'regression':
    model_task = fdl.ModelTask.REGRESSION
    
elif model_task == 'binary':
    model_task = fdl.ModelTask.BINARY_CLASSIFICATION

elif model_task == 'multiclass':
    model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION

    
# Specify column types
target = #
outputs = [#]
decision_cols = [#]
features = [#]
    
# Generate ModelInfo
model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    model_task=model_task,
    target=target,
    categorical_target_class_details='yes',
    outputs=outputs,
    decision_cols=decision_cols,
    features=features
)
model_info
```


```python
MODEL_ID = #

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```

## 4. Publish production events


```python
PATH_TO_EVENTS_CSV = #

production_df = pd.read_csv(PATH_TO_EVENTS_CSV)
production_df
```


```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source=production_df,
    timestamp_field='timestamp'
)
```

## 5. Get insights

**You're all done!**

Now just head to your Fiddler environment's UI and start getting enhanced monitoring, analytics, and explainability.



---


**Questions?**  
  
Check out [our docs](https://docs.fiddler.ai/) for a more detailed explanation of what Fiddler has to offer.

If you're still looking for answers, fill out a ticket on [our support page](https://fiddlerlabs.zendesk.com/) and we'll get back to you shortly.
