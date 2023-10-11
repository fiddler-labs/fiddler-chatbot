---
title: "client.get_mutual_information"
slug: "clientget_mutual_information"
excerpt: "Calculates the mutual information (MI) between variables over a specified dataset."
hidden: false
createdAt: "2022-05-23T21:14:37.148Z"
updatedAt: "2022-06-21T17:25:00.154Z"
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
    "2-0": "features",
    "2-1": "list",
    "2-2": "None",
    "2-3": "A list of features for which to compute mutual information.",
    "6-0": "seed",
    "6-1": "Optional [float]",
    "6-2": "0.25",
    "6-3": "The random seed used to sample when *sample_size* is specified.",
    "1-0": "dataset_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The unique identifier for the dataset.",
    "4-0": "slice_query",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "A SQL query. If specified, mutual information will only be calculated over the dataset slice specified by the query.",
    "3-0": "normalized",
    "3-1": "Optional [bool]",
    "3-2": "False",
    "3-3": "If True, will compute normalized mutual information (NMI) instead.",
    "5-0": "sample_size",
    "5-1": "Optional [int]",
    "5-2": "None",
    "5-3": "If specified, only *sample_size* samples will be used in the mutual information calculation."
  },
  "cols": 4,
  "rows": 7
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\nmutual_information_features = [\n    'feature_1',\n    'feature_2',\n    'feature_3'\n]\n\nmutual_information = client.get_mutual_information(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    features=mutual_information_features\n)",
      "language": "python",
      "name": "Usage"
    },
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\n\nmutual_information_features = [\n    'feature_1',\n    'feature_2',\n    'feature_3'\n]\n\nslice_query = f\"\"\" SELECT * FROM \"{DATASET_ID}.{MODEL_ID}\" WHERE feature_1 < 20.0 LIMIT 100 \"\"\"\n\nmutual_information = client.get_mutual_information(\n    project_id=PROJECT_ID,\n    dataset_id=DATASET_ID,\n    features=mutual_information_features,\n    slice_query=slice_query\n)",
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
    "0-1": "A dictionary containing mutual information results."
  },
  "cols": 2,
  "rows": 1
}
[/block]