---
title: "client.run_fairness"
slug: "clientrun_fairness"
excerpt: "Calculates fairness metrics for a model over a specified dataset."
hidden: false
createdAt: "2022-05-25T15:16:38.209Z"
updatedAt: "2022-06-21T17:25:10.915Z"
---
Get fairness metrics for a model over a dataset.
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
    "1-3": "The unique identifier for the model.",
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "3-0": "protected_features",
    "3-1": "list",
    "3-2": "None",
    "3-3": "A list of protected features.",
    "4-0": "positive_outcome",
    "4-1": "Union [str, int]",
    "4-2": "None",
    "4-3": "The name or value of the positive outcome for the model.",
    "5-0": "slice_query",
    "5-1": "Optional [str]",
    "5-2": "None",
    "5-3": "A SQL query. If specified, fairness metrics will only be calculated over the dataset slice specified by the query.",
    "6-0": "score_threshold",
    "6-1": "Optional [float]",
    "6-2": "0.5",
    "6-3": "The score threshold used to calculate model outcomes."
  },
  "cols": 4,
  "rows": 7
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\nDATASET_ID = 'example_dataset'\n\nprotected_features = [\n    'feature_1',\n    'feature_2'\n]\n\npositive_outcome = 1\n\nfairness_metrics = client.run_fairness(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    dataset_id=DATASET_ID,\n    protected_features=protected_features,\n    positive_outcome=positive_outcome\n)",
      "language": "python",
      "name": "Usage"
    },
    {
      "code": "PROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\nDATASET_ID = 'example_dataset'\n\nprotected_features = [\n    'feature_1',\n    'feature_2'\n]\n\npositive_outcome = 1\n\nslice_query = f\"\"\" SELECT * FROM \"{DATASET_ID}.{MODEL_ID}\" WHERE feature_1 < 20.0 LIMIT 100 \"\"\"\n\nfairness_metrics = client.run_fairness(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    dataset_id=DATASET_ID,\n    protected_features=protected_features,\n    positive_outcome=positive_outcome,\n    slice_query=slice_query\n)",
      "language": "python",
      "name": "Usage - With a SQL Query"
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
    "0-1": "A dictionary containing fairness metric results."
  },
  "cols": 2,
  "rows": 1
}
[/block]