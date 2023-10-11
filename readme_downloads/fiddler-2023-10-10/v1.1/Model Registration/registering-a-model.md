---
title: "Registering a Model"
slug: "registering-a-model"
hidden: false
createdAt: "2022-04-19T20:07:09.839Z"
updatedAt: "2022-06-08T15:49:55.181Z"
---
To register a model **without uploading your model artifact**, you can use the [client.register_model()](ref:clientregister_model) API. Let's walk through a simple example of how this can be done.

***

Suppose you have uploaded the following dataset, and you’ve created a [fdl.DatasetInfo()](ref:fdldatasetinfo)  object for it called `dataset_info` (See [Uploading a Baseline Dataset](doc:uploading-a-baseline-dataset)).
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/82cf758-example_df.png",
        "example_df.png",
        444,
        325,
        "#f2f1f2"
      ]
    }
  ]
}
[/block]
```python
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)
```

Although the data has been uploaded to Fiddler, there is still **no specification** for which columns to use for which purpose.

[block:api-header]
{
  "title": "Creating a ModelInfo object"
}
[/block]
To **provide this specification**, you can create a [fdl.ModelInfo()](ref:fdlmodelinfo) object.

In this case, we’d like to tell Fiddler to use

* `feature_1`, `feature_2`, and `feature_3` as features
* `output_column` as the model output
* `target_column` as the model's target/ground truth

To save time, Fiddler provides a function to add this specification to an existing [fdl.DatasetInfo()](ref:fdldatasetinfo) object.

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
    target=model_target,
    outputs=model_outputs,
    model_task=model_task
)
```

The [fdl.ModelInfo.from_dataset_info()](ref:fdlmodelinfofrom_dataset_info) function allows you to specify a [fdl.DatasetInfo()](ref:fdldatasetinfo) object along with some extra specification and it will **automatically generate** your [fdl.ModelInfo()](ref:fdlmodelinfo) object for you.

[block:api-header]
{
  "title": "Registering your model"
}
[/block]
Once you have your [fdl.ModelInfo()](ref:fdlmodelinfo) object, you can call [client.register_model()](ref:clientregister_model) to register your model with Fiddler.

```python
MODEL_ID = 'example_model'

client.register_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```