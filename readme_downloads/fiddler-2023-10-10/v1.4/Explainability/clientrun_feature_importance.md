---
title: "client.run_feature_importance"
slug: "clientrun_feature_importance"
excerpt: "Calculates feature importance for a model over a specified dataset."
hidden: false
createdAt: "2022-05-23T21:09:17.612Z"
updatedAt: "2022-06-21T17:24:54.236Z"
---
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
    "3-0": "dataset_splits",
    "3-1": "Optional [list]",
    "3-2": "None",
    "3-3": "A list of dataset splits taken from the dataset argument of upload_dataset. If specified, feature importance will only be calculated over the provided splits. Otherwise, all splits will be used.",
    "5-0": "**kwargs",
    "5-1": "",
    "5-2": "None",
    "5-3": "Additional arguments to be passed.\nCan be one or more of\n- n_inputs\n- n_iterations\n- n_references\n- ci_confidence_level\n- impact_not_importance",
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "4-0": "slice_query",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "A SQL query. If specified, feature importance will only be calculated over the dataset slice specified by the query."
  },
  "cols": 4,
  "rows": 6
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\nDATASET_ID = 'example_dataset'\n\nfeature_importance = client.run_feature_importance(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    dataset_id=DATASET_ID\n)",
      "language": "python",
      "name": "Usage"
    },
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\nDATASET_ID = 'example_dataset'\n\nslice_query = f\"\"\" SELECT * FROM \"{DATASET_ID}.{MODEL_ID}\" WHERE feature_1 < 20.0 LIMIT 100 \"\"\"\n\nfeature_importance = client.run_feature_importance(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    dataset_id=DATASET_ID,\n    slice_query=slice_query\n)",
      "language": "python",
      "name": "Usage with SQL Query"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "dict",
    "0-1": "A dictionary containing feature importance results."
  },
  "cols": 2,
  "rows": 1
}
[/block]