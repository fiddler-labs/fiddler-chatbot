---
title: "client.run_explanation"
slug: "clientrun_explaination"
excerpt: "Runs a point explanation for a given input vector."
hidden: false
createdAt: "2022-05-23T21:03:07.614Z"
updatedAt: "2023-01-31T19:01:12.753Z"
---
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
    "3-0": "df",
    "3-1": "pd.DataFrame",
    "3-2": "None",
    "3-3": "A pandas DataFrame containing a model input vector as a row. If more than one row is included, the first row will be used.",
    "4-0": "explanations",
    "4-1": "Union [str, list]",
    "4-2": "'shap'",
    "4-3": "A string or list of strings specifying which explanation algorithms to run.  \nCan be one or more of  \n- 'fiddler_shapley_values'  \n- 'shap'  \n- 'ig_flex'  \n- 'ig'  \n- 'mean_reset'  \n- 'zero_reset'  \n- 'permute'",
    "5-0": "n_permutation",
    "5-1": "Optional[int]",
    "5-2": "None",
    "5-3": "Number of permutations used for fiddler_shapley_values and the permute algorithm. Can be used for both tabular and text data.  \nBy default (None), we use 300 permutations.",
    "6-0": "n_background",
    "6-1": "Optional[int]",
    "6-2": "None",
    "6-3": "Number of background observations used for fiddler_shapley_values, permute and mean_reset algorithms for tabular data.  \nBy default (None), we use 200.",
    "7-0": "casting_type",
    "7-1": "Optional [bool]",
    "7-2": "False",
    "7-3": "If True, will try to cast the data in the events to be in line with the data types defined in the model's **ModelInfo** object.",
    "8-0": "return_raw_response",
    "8-1": "Optional [bool]",
    "8-2": "False",
    "8-3": "If True, a raw output will be returned instead of explanation objects."
  },
  "cols": 4,
  "rows": 9,
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
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

df = pd.read_csv('example_data.csv')

explanation = client.run_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    dataset_id=DATASET_ID,
    df=df
)
```



| Return Type                                                                                                                                                                                                                                            | Description                                                                                                                                                               |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Union\[[fdl.AttributionExplanation](https://dash.readme.com/project/fiddler/v1.5/refs/fdlattributionexplanation), [fdl.MulticlassAttributionExplanation](https://dash.readme.com/project/fiddler/v1.5/refs/fdlmulticlassattributionexplanation), list] | A **fdl.AttributionExplanation** object, **fdl.MulticlassAttributionExplanation** object, or list of such objects for each explanation method specified in _explanations_ |