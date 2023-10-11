---
title: "Ranking"
slug: "ranking"
hidden: false
createdAt: "2022-05-02T15:39:22.424Z"
updatedAt: "2023-06-16T21:40:33.886Z"
---
## Onboarding a Ranking Model

Suppose you would like to onboard a ranking model for the following dataset.

![](https://files.readme.io/1d6eb09-expedia_df.png "expedia_df.png")

Following is an example of how you would construct a [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object for a ranking model.

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'expedia_data'
MODEL_ID = 'ranking_model'

model_task = fdl.ModelTask.RANKING
model_group_by = 'srch_id'
model_target = 'click_bool'
model_outputs = ['score']
raning_top_k = 20
model_features = [
    'price_usd',
    'promotion_flag',
    'weekday',
    'week_of_year',
    'hour_time',
    'minute_time'

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    features=model_features,
    group_by=model_group_by,
    ranking_top_k=ranking_top_k,
    target=model_target,
    outputs=model_outputs,
    model_task=model_task,
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

> 🚧 Note
> 
> `group_by`: when onboarding a ranking model, you **must specify** a `group_by` argument to the [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object. It will tell Fiddler which column should be used for **grouping items** so that they may be ranked within a group.
> 
> `ranking_top_k`: an optional parameter unique to ranking model. Default to `50`. It's an int representing the top k outputs to take into consideration when computing performance metrics MAP and NDCG.

> 📘 Tips
> 
> When onboarding a **graded ranking model** with **categorical target**, `categorical_target_class_detail` is a required argument for [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object. For example: `categorical_target_class_details=['booked','click_no_booking','no_click']`