---
title: "client.get_explanation"
slug: "clientget_explanation"
excerpt: "Get explanation for a single observation."
hidden: true
createdAt: "2023-08-01T13:22:39.245Z"
updatedAt: "2023-08-02T13:32:42.277Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_name",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_name",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "input_data_source",
    "2-1": "Union[DatasetDataSource, SqlSliceQueryDataSource]",
    "2-2": "None",
    "2-3": "DataSource for the input dataset to compute feature importance on (DatasetDataSource or SqlSliceQueryDataSource)",
    "3-0": "ref_data_source",
    "3-1": "Optional\\[ Union[DatasetDataSource, SqlSliceQueryDataSource] ]",
    "3-2": "None",
    "3-3": "ataSource for the reference data to compute explanation on (DatasetDataSource, SqlSliceQueryDataSource).  \nOnly used for non-text models and the following methods:  \n'SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET'",
    "4-0": "explanation_type",
    "4-1": "Optional[str]",
    "4-2": "None",
    "4-3": "Explanation method name. Could be your custom  \nexplanation method or one of the following method:  \n'SHAP', 'FIDDLER_SHAP', 'IG', 'PERMUTE', 'MEAN_RESET', 'ZERO_RESET'",
    "5-0": "num_permutations",
    "5-1": "Optional[int]",
    "5-2": "None",
    "5-3": "For Fiddler SHAP, that corresponds to the number of coalitions to sample to estimate the Shapley values of each single-reference game. For the permutation algorithms, this corresponds to the number of permutations from the dataset to use for the computation.",
    "6-0": "ci_level",
    "6-1": "Optional[float]",
    "6-2": "None",
    "6-3": "The confidence level (between 0 and 1).",
    "7-0": "top_n_class",
    "7-1": "Optional[int]",
    "7-2": "None",
    "7-3": "For multiclass classification models only, specifying if only the n top classes are computed or all classes (when parameter is None)"
  },
  "cols": 4,
  "rows": 8,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

df = pd.read_csv('example_data.csv')

explanation = client.run_explanation(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME,
    input_data_source=df
)
```

| Return Type | Description                                 |
| :---------- | :------------------------------------------ |
| tuple       | A named tuple with the explanation results. |