---
title: "Multiclass Classification"
slug: "multiclass-classification"
hidden: false
createdAt: "2022-04-19T20:12:22.899Z"
updatedAt: "2023-04-06T22:32:05.867Z"
---
## Onboarding a Multiclass Classification Model

Suppose you would like to onboard a multiclass classification model for the following dataset.

![](https://files.readme.io/5eabe9a-iris_df.png "iris_df.png")

Following is an example of how you would construct a [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object and onboard such a model.


[block:tutorial-tile]
{
  "backgroundColor": "#018FF4",
  "emoji": "🦉",
  "id": "64d50e7b48a709212aad40d9",
  "link": "https://docs.fiddler.ai/v1.5/recipes/add-a-multi-class-classification-model",
  "slug": "add-a-multi-class-classification-model",
  "title": "Add a Multi-class Classification Model"
}
[/block]




> 📘 categorical_target_class_details
> 
> For multiclass models, the `categorical_target_class_details` argument is required.
> 
> This argument should be a **list of your target classes** in the order that your model outputs predictions for them.

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

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```



> 📘 Note
> 
> Using [client.add_model()](ref:clientadd_model) does not provide Fiddler with a model artifact.  Onboarding a model in this fashion is a good start for model monitoring, but Fiddler will not be able to offer model explainability features without a model artifact.  You can subsequently call [client.add_model_surrogate()](ref:clientadd_model_surrogate) or [client.add_model_artifact()](ref:clientadd_model_artifact) to provide Fiddler with a model artifact.  Please see [Uploading a Model Artifact](doc:uploading-model-artifacts) for more information.