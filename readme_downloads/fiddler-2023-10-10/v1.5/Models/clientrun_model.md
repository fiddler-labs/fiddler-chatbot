---
title: "client.run_model"
slug: "clientrun_model"
excerpt: "Runs a model on a pandas DataFrame and returns the predictions."
hidden: false
createdAt: "2022-05-23T20:56:16.995Z"
updatedAt: "2022-06-21T17:24:21.221Z"
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
    "2-0": "df",
    "2-1": "pd.DataFrame",
    "2-2": "None",
    "2-3": "A pandas DataFrame containing model input vectors as rows.",
    "3-0": "log_events",
    "3-1": "Optional [bool]",
    "3-3": "If True, the rows of df along with the model predictions will be logged as production events.",
    "3-2": "False",
    "4-0": "casting_type",
    "4-1": "Optional [bool]",
    "4-2": "False",
    "4-3": "If True, will try to cast the data in the events to be in line with the data types defined in the model's **ModelInfo** object."
  },
  "cols": 4,
  "rows": 5
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\nPROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\ndf = pd.read_csv('example_data.csv')\n\npredictions = client.run_model(\n    project_id=PROJECT_ID,\n    model_id=MODEL_ID,\n    df=df\n)",
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
    "0-0": "pd.DataFrame",
    "0-1": "A pandas DataFrame containing model predictions for the given input vectors."
  },
  "cols": 2,
  "rows": 1
}
[/block]