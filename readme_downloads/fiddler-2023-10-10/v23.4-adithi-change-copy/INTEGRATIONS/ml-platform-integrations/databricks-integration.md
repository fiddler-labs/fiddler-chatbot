---
title: "Databricks Integration"
slug: "databricks-integration"
hidden: false
createdAt: "2023-02-02T20:38:54.971Z"
updatedAt: "2023-08-14T17:16:36.875Z"
---
Fiddler allows your team to monitor, explain and analyze your models developed and deployed in [Databricks Workspace](https://docs.databricks.com/introduction/index.html) by integrating with [MLFlow](https://docs.databricks.com/mlflow/index.html) for model asset management and utilizing Databricks Spark environment for data management. 

To validate and monitor models built on Databricks using Fiddler, you can follow these steps:

1. [Creating a Fiddler Project](doc:databricks-integration#creating-a-fiddler-project)
2. [Uploading a Baseline Dataset](doc:databricks-integration#uploading-a-baseline-dataset)
3. [Adding Model Information ](doc:databricks-integration#adding-model-information)
4. [Uploading Model Files (for Explainability)](doc:databricks-integration#uploading-model-files)
5. [Publishing Events](doc:databricks-integration#publishing-events)
   1. Batch Models 
   2. Live Models 

## Creating a Fiddler Project

Launch a [Databricks notebook](https://docs.databricks.com/notebooks/index.html) from your workspace and run the following code:

```python
!pip install -q fiddler-client
import fiddler as fdl
```

Now that you have the Fiddler library installed, you can connect to your Fiddler environment. Please use the [UI administration guide](doc:administration-ui) to help you find your Fiddler credentials.

```python
URL = ""
ORG_ID = ""
AUTH_TOKEN = ""
client = fdl.FiddlerApi(url=URL, org_id=ORG_ID, auth_token=AUTH_TOKEN)
```

Finally, you can set up a new project using:

```python
client.create_project("YOUR_PROJECT_NAME")
```

## Uploading a Baseline Dataset

You can grab your baseline dataset from a[ delta table](https://docs.databricks.com/getting-started/dataframes-python.html) and share it with Fiddler as a baseline dataset:

```python
baseline_dataset = spark.read.table("YOUR_DATASET").select("*").toPandas()

dataset_info = fdl.DatasetInfo.from_dataframe(baseline_upload, max_inferred_cardinality=100)
  
client.upload_dataset(
  project_id=PROJECT_ID,
  dataset_id=DATASET_ID,
  dataset={'baseline': baseline_upload},
  info=dataset_info)
```

## Adding Model Information

Using the **[MLFlow API](https://docs.databricks.com/reference/mlflow-api.html) ** you can query the model registry and get the **model signature** which describes the inputs and outputs as a dictionary. You can use this dictionary to build out the [ModelInfo](ref:fdlmodelinfo) object required to the model to Fiddler:

```python Python
mport mlflow 

model_uri = MlflowClient.get_model_version_download_uri(model_name, model_version) #spevify the model name and model version you want to share wth Fiddler

model_info = mlflow.models.ModelSignature.to_dict(model_uri)  #MLFlow_Params_Object with model I/O info
```

Now you can share the model signature with Fiddler as part of the Fiddler ModelInfo object :

```python
model_info = fdl.ModelInfo.from_dataset_info(
	dataset_info = client.get_dataset_info(YOUR_PROJECT,YOUR_DATASET),
	target =  "TARGET COLUMN",
	#optionalArguments
	mlflow_params = fdl.MLFlowParams(mlflow.models.ModelSignature.to_dict())  
)
```

## Uploading Model Files

Sharing your [model artifacts](https://docs.fiddler.ai/docs/uploading-model-artifacts) helps Fiddler explain your models. By leveraging the MLFlow API you can download these model files:

```python
import os  
import mlflow  
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository

model_name = "example-model-name"  
model_stage = "Staging"  # Should be either 'Staging' or 'Production'

mlflow.set_tracking_uri("databricks")  
os.makedirs("model", exist_ok=True)  
local_path = ModelsArtifactRepository(
  f'models:/{model_name}/{model_stage}').download_artifacts("", dst_path="model")  

print(f'{model_stage} Model {model_name} is downloaded at {local_path}')  
```

Once you have the model file, you can create a [package.py](doc:binary-classification-1) file in this model directory that describes how to access this model.

Finally, you can upload all the model artifacts to Fiddler:

```python
client.add_model_artifact(  
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir='model/',
)
```

Alternatively, you can skip uploading your model and use Fiddler to generate a [surrogate model](doc:surrogate-models-client-guide) to get low-fidelity explanations for your model.

## Publishing Events

Now you can publish all the events from your models. You can do this in two ways:

### Batch Models

If your models run batch processes with your models or your aggregate model outputs over a timeframe, then you can use the table change feed from Databricks to select only the new events and send them to Fiddler:

```python Python
changes_df = spark.read.format("delta") \
.option("readChangeFeed", "true") \
.option("startingVersion",last_version) \
.option("endingVersion", new_version) \
.table("inferences").toPandas()


client.publish_events_batch(
   project_id=PROJECT_ID,
   model_id=MODEL_ID,
   batch_source=changes_df,
   timestamp_field='timestamp')

```

### Live Models

For models with live predictions or real-time applications, you can add the following code snippet to your prediction pipeline and send every event to Fiddler in real-time: 

```python Python
example_event = model_output.toPandas() #turn your model's ouput in a pandas datafram 

client.publish_event(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    event=example_event,
    event_id='event_001',
    event_timestamp=1637344470000)
```

_Support for Inference tables and hosted endpoints is coming soon!_