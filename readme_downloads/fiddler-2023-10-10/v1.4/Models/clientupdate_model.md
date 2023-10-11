---
title: "client.update_model"
slug: "clientupdate_model"
excerpt: "Replaces the model artifact for a model."
hidden: false
createdAt: "2022-05-23T19:26:42.714Z"
updatedAt: "2022-06-21T17:24:02.553Z"
---
For more information, see [Uploading a Model Artifact](doc:uploading-a-model-artifact).
[block:callout]
{
  "type": "warning",
  "title": "Warning",
  "body": "This function does not allow for changes in a model's schema. The inputs and outputs to the model must remain the same."
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "0-0": "project_id",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "3-0": "force_pre_compute",
    "3-1": "bool",
    "3-2": "True",
    "3-3": "If True, re-run precomputation steps for the model. This can also be done manually by calling **client.trigger_pre_computation**.",
    "2-0": "model_dir",
    "2-1": "pathlib.Path",
    "2-2": "None",
    "2-3": "A path to the directory containing all of the model files needed to run the model."
  },
  "cols": 4,
  "rows": 4
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pathlib\n\nPROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\nmodel_dir = pathlib.Path('model_dir')\n\nclient.update_model(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    model_dir=model_dir\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "bool",
    "0-1": "A boolean denoting whether the update was successful."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "True",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]