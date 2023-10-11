---
title: "client.run_explanation"
slug: "clientrun_explaination"
excerpt: "Runs a point explanation for a given input vector."
hidden: false
createdAt: "2022-05-23T21:03:07.614Z"
updatedAt: "2022-06-21T17:24:48.073Z"
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
    "3-0": "df",
    "3-1": "pd.DataFrame",
    "3-2": "None",
    "3-3": "A pandas DataFrame containing a model input vector as a row. If more than one row is included, the first row will be used.",
    "5-0": "casting_type",
    "5-1": "Optional [bool]",
    "5-2": "False",
    "5-3": "If True, will try to cast the data in the events to be in line with the data types defined in the model's **ModelInfo** object.",
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "4-0": "explanations",
    "4-1": "Union [str, list]",
    "4-2": "'shap'",
    "4-3": "A string or list of strings specifying which explanation algorithms to run.\nCan be one or more of\n- 'fiddler_shapley_values'\n- 'shap'\n- 'ig_flex'\n- 'ig'\n- 'mean_reset'\n- 'zero_reset'\n- 'permute'",
    "6-0": "return_raw_response",
    "6-1": "Optional [bool]",
    "6-2": "False",
    "6-3": "If True, a raw output will be returned instead of explanation objects."
  },
  "cols": 4,
  "rows": 7
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\nMODEL_ID = 'example_model'\n\ndf = pd.read_csv('example_data.csv')\n\nexplanation = client.run_explanation(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    dataset_id=DATASET_ID,\n    df=df\n)",
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
    "0-0": "Union[fdl.AttributionExplanation, fdl.MulticlassAttributionExplanation, list]",
    "0-1": "A **fdl.AttributionExplanation** object, **fdl.MulticlassAttributionExplanation** object, or list of such objects for each explanation method specified in *explanations* "
  },
  "cols": 2,
  "rows": 1
}
[/block]