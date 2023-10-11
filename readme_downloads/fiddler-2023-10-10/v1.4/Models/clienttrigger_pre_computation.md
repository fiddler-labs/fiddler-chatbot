---
title: "client.trigger_pre_computation"
slug: "clienttrigger_pre_computation"
excerpt: "Runs a variety of precomputation steps for a model."
hidden: false
createdAt: "2022-05-23T19:36:35.716Z"
updatedAt: "2022-06-21T17:24:11.809Z"
---
[block:callout]
{
  "type": "info",
  "title": "Note",
  "body": "This method should be called after *client.upload_model_package()*.  It is not necessary after calling *client.register_model()* as this step happens automatically when registering a model."
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
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "3-0": "overwrite_cache",
    "3-1": "Optional [bool]",
    "3-3": "If True, will overwrite existing cached information.",
    "3-2": "True",
    "4-0": "batch_size",
    "4-1": "Optional [int]",
    "4-2": "10",
    "4-3": "The batch size used for global PDP calculations.",
    "6-0": "cache_global_impact_importance",
    "6-1": "Optional [bool]",
    "6-2": "True",
    "6-3": "If True, global feature impact and global feature importance will be precomputed and cached when the model is registered.",
    "7-0": "cache_global_pdps",
    "7-1": "Optional [bool]",
    "7-2": "True",
    "7-3": "If True, global partial dependence plots will be precomputed and cached when the model is registered.",
    "8-0": "cache_dataset",
    "8-1": "Optional [bool]",
    "8-2": "False",
    "8-3": "If True, histogram information for the baseline dataset will be precomputed and cached when the model is registered.",
    "5-0": "calculate_predictions",
    "5-1": "Optional [bool]",
    "5-2": "True",
    "5-3": "If True, will precompute and store model predictions."
  },
  "cols": 4,
  "rows": 9
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\nMODEL_ID = 'example_model'\n\nclient.trigger_pre_computation(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    model_id=MODEL_ID\n)",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]