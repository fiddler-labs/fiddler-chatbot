---
title: "client.register_model"
slug: "clientregister_model"
excerpt: "Registers a model without uploading an artifact. Requires a** fdl.ModelInfo** object containing information about the model."
hidden: false
createdAt: "2022-05-23T19:14:26.437Z"
updatedAt: "2022-06-21T17:23:52.249Z"
---
For more information, see [Registering a Model](doc:registering-a-model).
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
    "1-3": "A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character.",
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "3-0": "model_info",
    "3-1": "fdl.ModelInfo",
    "3-3": "A [fdl.ModelInfo()](ref:fdlmodelinfo) object containing information about the model.",
    "3-2": "None",
    "4-0": "deployment",
    "4-1": "Optional [fdl.core_objects.DeploymentOptions]",
    "4-2": "None",
    "4-3": "A **DeploymentOptions** object containing information about the model deployment.",
    "5-0": "cache_global_impact_importance",
    "5-1": "Optional [bool]",
    "5-2": "True",
    "5-3": "If True, global feature impact and global feature importance will be precomputed and cached when the model is registered.",
    "6-0": "cache_global_pdps",
    "6-1": "Optional [bool]",
    "6-2": "False",
    "6-3": "If True, global partial dependence plots will be precomputed and cached when the model is registered.",
    "7-0": "cache_dataset",
    "7-1": "Optional [bool]",
    "7-2": "True",
    "7-3": "If True, histogram information for the baseline dataset will be precomputed and cached when the model is registered."
  },
  "cols": 4,
  "rows": 8
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\nMODEL_ID = 'example_model'\n\ndataset_info = client.get_dataset_info(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID\n)\n\nmodel_task = fdl.ModelTask.BINARY_CLASSIFICATION\nmodel_target = 'target_column'\nmodel_output = 'output_column'\nmodel_features = [\n    'feature_1',\n    'feature_2',\n    'feature_3'\n]\n\nmodel_info = fdl.ModelInfo.from_dataset_info(\n    dataset_info=dataset_info,\n    target=model_target,\n    outputs=[model_output],\n    model_task=model_task\n)\n\nclient.register_model(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    model_id=MODEL_ID,\n    model_info=model_info\n)",
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
    "0-0": "str",
    "0-1": "A message confirming that the model was registered."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "'Model successfully registered on Fiddler. \\n Visit https://app.fiddler.ai/projects/example_project'",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]