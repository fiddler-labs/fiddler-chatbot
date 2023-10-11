---
title: "Multi-class Classification"
slug: "multiclass-classification"
hidden: false
createdAt: "2022-04-19T20:12:22.899Z"
updatedAt: "2022-06-08T21:34:08.043Z"
---
[block:api-header]
{
  "title": "Registering a Multiclass Classification Model"
}
[/block]
Suppose you would like to register a multiclass classification model for the following dataset.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/5eabe9a-iris_df.png",
        "iris_df.png",
        1428,
        646,
        "#f2f2f2"
      ]
    }
  ]
}
[/block]
Following is an example of how you would construct a [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object and register such a model.

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'iris_data'
MODEL_ID = 'multiclass_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.MULTICLASS_CLASSIFICATION
model_target = 'species'
model_outputs = [
    'probability_0',
    'probability_1',
    'probability_2'
]
model_features = [
    'sepal_length',
    'sepal_width',
    'petal_length',
    'petal_width'
]

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    target=model_target,
    outputs=model_outputs,
    model_task=model_task,
    categorical_target_class_details=[0, 1, 2]
)

client.register_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```