---
title: "client.add_model_artifact"
slug: "clientadd_model_artifact"
excerpt: "Adds a model artifact to an existing model"
hidden: false
createdAt: "2022-08-01T03:09:29.086Z"
updatedAt: "2022-12-14T19:27:27.268Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](/reference/clientadd_model).

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
    "2-0": "model_dir",
    "2-1": "str",
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
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.add_model_artifact(
    model_dir='model_dir/',
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```