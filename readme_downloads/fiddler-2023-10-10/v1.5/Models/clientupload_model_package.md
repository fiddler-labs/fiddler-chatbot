---
title: "client.upload_model_package"
slug: "clientupload_model_package"
excerpt: "Registers a model with Fiddler and uploads a model artifact to be used for explainability and fairness capabilities."
hidden: false
createdAt: "2022-05-23T19:21:34.380Z"
updatedAt: "2022-12-12T19:54:14.586Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Please use _client.add_model_artifact()_ going forward.

For more information, see [Uploading a Model Artifact](doc:uploading-a-model-artifact).

[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "artifact_path",
    "2-1": "pathlib.Path",
    "2-2": "None",
    "2-3": "A path to the directory containing all of the model files needed to run the model.",
    "3-0": "deployment_type",
    "3-1": "Optional [str]",
    "3-2": "'predictor'",
    "3-3": "The type of deployment for the model. Can be one of  \n_ 'predictor' — Just a predict endpoint is exposed.  \n_ 'executor' — The model's internals are exposed.",
    "4-0": "image_uri",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "A URI of the form '/:'. If specified, the image will be used to create a new runtime to serve the model.",
    "5-0": "namespace",
    "5-1": "Optional [str]",
    "5-2": "'default'",
    "5-3": "The Kubernetes namespace to use for the newly created runtime. image_uri must be specified.",
    "6-0": "port",
    "6-1": "Optional [int]",
    "6-2": "5100",
    "6-3": "The port to use for the newly created runtime. image_uri must be specified.",
    "7-0": "replicas",
    "7-1": "Optional [int]",
    "7-2": "1",
    "7-3": "The number of replicas running the model. image_uri must be specified.",
    "8-0": "cpus",
    "8-1": "Optional [int]",
    "8-2": "0.25",
    "8-3": "The number of CPU cores reserved per replica. image_uri must be specified.",
    "9-0": "memory",
    "9-1": "Optional [str]",
    "9-2": "'128m'",
    "9-3": "The amount of memory reserved per replica. image_uri must be specified.",
    "10-0": "gpus",
    "10-1": "Optional [int]",
    "10-2": "0",
    "10-3": "The number of GPU cores reserved per replica. image_uri must be specified.",
    "11-0": "await_deployment",
    "11-1": "Optional [bool]",
    "11-2": "True",
    "11-3": "If True, will block until deployment completes."
  },
  "cols": 4,
  "rows": 12,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
import pathlib

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

artifact_path = pathlib.Path('model_dir')

client.upload_model_package(
    artifact_path=artifact_path,
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```