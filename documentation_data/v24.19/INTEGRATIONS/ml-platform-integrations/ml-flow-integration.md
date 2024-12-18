---
title: ML Flow Integration
slug: ml-flow-integration
excerpt: ''
createdAt: Fri Sep 15 2023 18:36:23 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)
---

# ML Flow Integration

Fiddler allows your team to onboard, monitor, explain, and analyze your models developed with [MLFlow](https://mlflow.org/).

This guide shows you how to ingest the model metadata and artifacts stored in your MLFlow model registry and use them to set up model observability in the Fiddler Platform:

1. Exporting Model Metadata from MLFlow to Fiddler
2. Uploading Model Artifacts to Fiddler for XAI

### Adding Model Information

Using the \*\*[MLFlow API](https://mlflow.org/docs/latest/python\_api/mlflow.html) \*\* you can query the model registry and get the **model signature** which describes the inputs and outputs as a dictionary. You can use this dictionary to build out the [ModelInfo](broken-reference) object required to the model to Fiddler:

```python
import mlflow 
from mlflow.tracking import MlflowClient

client = MlflowClient() #initiate MLFlow Client 

#Get the model URI
model_version_info = client.get_model_version(model_name, model_version)
model_uri = client.get_model_version_download_uri(model_name, model_version_info) 

#Get the Model Signature
mlflow_model_info = mlflow.models.get_model_info(model_uri)
model_inputs_schema = model_info.signature.inputs.to_dict()
model_inputs = [ sub['name'] for sub in model_inputs_schema ]
```

Now you can use the model signature to build the Fiddler ModelInfo object:

```python
features = model_inputs

model_task = fdl.ModelTask.BINARY_CLASSIFICATION

model_info = fdl.ModelInfo.from_dataset_info(
	dataset_info = client.get_dataset_info(YOUR_PROJECT,YOUR_DATASET),
	target =  "TARGET COLUMN", 
  dataset_id=DATASET_ID,
  model_task=model_task, 
  features=features,
  outputs=['output_column'])
```

### Uploading Model Files

Sharing your [model artifacts](../../product-guide/explainability/artifacts-and-surrogates.md#model-artifacts-and-model-package) helps Fiddler explain your models. By leveraging the MLFlow API you can download these model files:

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

Once you have the model file, you can create a [package.py](../../Client\_Guide/model-task-examples/binary-classification-1.md) file in this model directory that describes how to access this model.

Finally, you can upload all the model artifacts to Fiddler:

```python
client.add_model_artifact(  
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    model_dir='model/',
)
```

Alternatively, you can skip uploading your model and use Fiddler to generate a [surrogate model](../../product-guide/explainability/artifacts-and-surrogates.md#surrogate-model) to get low-fidelity explanations for your model.
