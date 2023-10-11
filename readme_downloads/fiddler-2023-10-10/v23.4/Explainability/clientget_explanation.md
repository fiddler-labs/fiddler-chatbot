---
title: "client.get_explanation"
slug: "clientget_explanation"
excerpt: "Get explanation for a single observation."
hidden: false
createdAt: "2023-08-16T11:21:48.321Z"
updatedAt: "2023-10-06T19:22:27.730Z"
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
    "0-3": "A unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "input_data_source",
    "2-1": "Union\\[[fdl.RowDataSource](ref:fdldatasetdatasource), [fdl.EventIdDataSource](ref:fdleventiddatasource)]",
    "2-2": "None",
    "2-3": "Type of data source for the input dataset to compute explanation on (RowDataSource, EventIdDataSource). A single row explanation is currently supported.",
    "3-0": "ref_data_source",
    "3-1": "Optional\\[Union\\[[fdl.DatasetDataSource](ref:fdldatasetdatasource), [fdl.SqlSliceQueryDataSource](ref:fdlsqlslicequerydatasource)] ]",
    "3-2": "None",
    "3-3": "Type of data source for the reference data to compute explanation on (DatasetDataSource, SqlSliceQueryDataSource).  \nOnly used for non-text models and the following methods:  \n'SHAP', 'FIDDLER_SHAP', 'PERMUTE', 'MEAN_RESET'",
    "4-0": "explanation_type",
    "4-1": "Optional[str]",
    "4-2": "'FIDDLER_SHAP'",
    "4-3": "Explanation method name. Could be your custom  \nexplanation method or one of the following method:  \n'SHAP', 'FIDDLER_SHAP', 'IG', 'PERMUTE', 'MEAN_RESET', 'ZERO_RESET'",
    "5-0": "num_permutations",
    "5-1": "Optional[int]",
    "5-2": "300",
    "5-3": "- For Fiddler SHAP, num_permutations corresponds to the number of coalitions to sample to estimate the Shapley values of each single-reference game.  \n- For the permutation algorithms, num_permutations corresponds to the number of permutations from the dataset to use for the computation.",
    "6-0": "ci_level",
    "6-1": "Optional[float]",
    "6-2": "0.95",
    "6-3": "The confidence level (between 0 and 1).",
    "7-0": "top_n_class",
    "7-1": "Optional[int]",
    "7-2": "None",
    "7-3": "For multi-class classification models only, specifying if only the n top classes are computed or all classes (when parameter is None)."
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
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
DATASET_ID = 'example_dataset

# FIDDLER SHAP - Dataset reference data source
row = df.to_dict(orient='records')[0]
client.get_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_data_source=fdl.RowDataSource(row=row),
    ref_data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID, num_samples=300),
    explanation_type='FIDDLER_SHAP',
    num_permutations=200,
    ci_level=0.95,
)

# FIDDLER SHAP - Slice ref data source
row = df.to_dict(orient='records')[0]
query = f'SELECT * from {DATASET_ID}.{MODEL_ID} WHERE sulphates >= 0.8'
client.get_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_data_source=fdl.RowDataSource(row=row),
    ref_data_source=fdl.SqlSliceQueryDataSource(query=query, num_samples=100),
    explanation_type='FIDDLER_SHAP',
    num_permutations=200,
    ci_level=0.95,
)

# FIDDLER SHAP - Multi-class classification (top classes)
row = df.to_dict(orient='records')[0]
client.get_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_data_source=fdl.RowDataSource(row=row),
    ref_data_source=fdl.DatasetDataSource(dataset_id=DATASET_ID),
    explanation_type='FIDDLER_SHAP',
    top_n_class=2
)

# IG (Not available by default, need to be enabled via package.py)
row = df.to_dict(orient='records')[0]
client.get_explanation(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    input_data_source=fdl.RowDataSource(row=row),
    explanation_type='IG',
)
```

| Return Type | Description                                 |
| :---------- | :------------------------------------------ |
| tuple       | A named tuple with the explanation results. |