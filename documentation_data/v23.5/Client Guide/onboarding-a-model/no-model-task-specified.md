---
title: "No Model Task Specified"
slug: "no-model-task-specified"
hidden: false
createdAt: "2023-10-10T18:52:44.017Z"
updatedAt: "2023-10-19T20:59:24.603Z"
---
## Onboarding a model without specifying a model task

The model task `NOT_SET` can be used if Fiddler doesn't provide the model task needed or if XAI and scoring functionalities are not necessary. This model task doesn't have any restrictions for the outputs and targets field, meaning those can be omitted or specified for any columns (no restriction on the number or type of columns).

Suppose you would like to onboard a model for the following dataset.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/235babe-f17fd5e-wine_df.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Following is an example of how you could construct a [`fdl.ModelInfo`](ref:fdlmodelinfo) object and onboard such a model.

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'wine_data'
MODEL_ID = 'example_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.NOT_SET

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    model_task=model_task
)

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```