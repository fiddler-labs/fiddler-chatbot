---
title: "client.run_feature_importance"
slug: "clientrun_feature_importance"
excerpt: "Calculates feature importance for a model over a specified dataset."
hidden: false
createdAt: "2022-05-23T21:09:17.612Z"
updatedAt: "2023-08-02T13:12:21.574Z"
---
> 🚧 Deprecated
> 
> This client method is deprecated and will be removed in the future versions. Use _client.get_feature_importance()_  or _client.get_feature_impact()_ instead.  
> Ref: [client.get_feature_importance](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_feature_importance)  
>         [client.get_feature_impact](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_feature_impact)

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
    "2-0": "dataset_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the dataset.",
    "3-0": "dataset_splits",
    "3-1": "Optional [list]",
    "3-2": "None",
    "3-3": "A list of dataset splits taken from the dataset argument of upload_dataset. If specified, feature importance will only be calculated over the provided splits. Otherwise, all splits will be used.",
    "4-0": "slice_query",
    "4-1": "Optional [str]",
    "4-2": "None",
    "4-3": "A SQL query. If specified, feature importance will only be calculated over the dataset slice specified by the query.",
    "5-0": "\\*\\*kwargs",
    "5-1": "",
    "5-2": "None",
    "5-3": "Additional arguments to be passed.  \nCan be one or more of  \n- n_inputs  \n- n_iterations  \n- n_references  \n- ci_confidence_level  \n- impact_not_importance"
  },
  "cols": 4,
  "rows": 6,
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
DATASET_ID = 'example_dataset'

feature_importance = client.run_feature_importance(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    dataset_id=DATASET_ID
)
```
```python Usage with SQL Query
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset'

slice_query = f""" SELECT * FROM "{DATASET_ID}.{MODEL_ID}" WHERE feature_1 < 20.0 LIMIT 100 """

feature_importance = client.run_feature_importance(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    dataset_id=DATASET_ID,
    slice_query=slice_query
)
```

| Return Type | Description                                         |
| :---------- | :-------------------------------------------------- |
| dict        | A dictionary containing feature importance results. |