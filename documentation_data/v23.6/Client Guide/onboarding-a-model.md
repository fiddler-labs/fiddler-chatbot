---
title: "Onboarding a Model"
slug: "onboarding-a-model"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:07:09 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
To onboard a model **without uploading your model artifact**, you can use the [client.add_model()](ref:clientadd_model) Python client. Let's walk through a simple example of how this can be done.

***



> 📘 Note
> 
> Using [client.add_model()](ref:clientadd_model) does not provide Fiddler with a model artifact.  Onboarding a model in this fashion is a good start for model monitoring, but Fiddler will not be able to offer model explainability features without a model artifact.  You can subsequently call [client.add_model_surrogate()](ref:clientadd_model_surrogate) or [client.add_model_artifact()](ref:clientadd_model_artifact) to provide Fiddler with a model artifact.  Please see [Uploading a Model Artifact](doc:uploading-model-artifacts) for more information.

Suppose you have uploaded the following baseline dataset, and you’ve created a [fdl.DatasetInfo()](ref:fdldatasetinfo)  object for it called `dataset_info` (See [Uploading a Baseline Dataset](doc:uploading-a-baseline-dataset)).

![](https://files.readme.io/82cf758-example_df.png "example_df.png")

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)
```



Although the data has been uploaded to Fiddler, there is still **no specification** for which columns to use for which purpose.

## Creating a ModelInfo object

To **provide this specification**, you can create a [fdl.ModelInfo()](ref:fdlmodelinfo) object.

In this case, we’d like to tell Fiddler to use

- `feature_1`, `feature_2`, and `feature_3` as features
- `output_column` as the model output
- `target_column` as the model's target/ground truth

Further you want to specify the [model task type](doc:task-types). To save time, Fiddler provides a function to add this specification to an existing [fdl.DatasetInfo()](ref:fdldatasetinfo) object.

```python
model_task = fdl.ModelTask.BINARY_CLASSIFICATION
model_target = 'target_column'
model_outputs = ['output_column']
model_features = [
    'feature_1',
    'feature_2',
    'feature_3'
]

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    features=model_features,
    target=model_target,
    outputs=model_outputs,
    model_task=model_task
)
```



The [fdl.ModelInfo.from_dataset_info()](ref:fdlmodelinfofrom_dataset_info) function allows you to specify a [fdl.DatasetInfo()](ref:fdldatasetinfo) object along with some extra specification and it will **automatically generate** your [fdl.ModelInfo()](ref:fdlmodelinfo) object for you.

## Onboarding your model

Once you have your [fdl.ModelInfo()](ref:fdlmodelinfo) object, you can call [client.add_model()](ref:clientadd_model) to onboard your model with Fiddler.

```python
MODEL_ID = 'example_model'

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```