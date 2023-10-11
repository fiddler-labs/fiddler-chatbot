---
title: "Ranking"
slug: "ranking"
hidden: false
createdAt: "2022-05-02T15:39:22.424Z"
updatedAt: "2022-05-02T16:22:03.390Z"
---
[block:api-header]
{
  "title": "Registering a Ranking Model"
}
[/block]
Suppose you would like to register a ranking model for the following dataset.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1d6eb09-expedia_df.png",
        "expedia_df.png",
        1480,
        658,
        "#f4f4f4"
      ]
    }
  ]
}
[/block]
Following is an example of how you would construct a [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object for such a model.
[block:callout]
{
  "type": "warning",
  "body": "When registering a ranking model, you **must specify** a `group_by` argument to the [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object. This will tell Fiddler which column should be used for **grouping items** so that they may be ranked within a group.",
  "title": "Note"
}
[/block]
```python
PROJECT_ID = 'example_project'
DATASET_ID = 'expedia_data'
MODEL_ID = 'ranking_model'

model_task = fdl.ModelTask.RANKING
model_group_by = 'srch_id'
model_target = 'click_bool'
model_outputs = ['score']
model_features = [
    'price_usd',
    'promotion_flag',
    'weekday',
    'week_of_year',
    'hour_time',
    'minute_time'
]

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    group_by=model_group_by,
    target=model_target,
    outputs=model_outputs,
    model_task=model_task
)

client.register_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```