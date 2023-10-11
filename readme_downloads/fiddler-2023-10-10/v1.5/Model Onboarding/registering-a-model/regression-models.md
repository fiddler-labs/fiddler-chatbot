---
title: "Regression"
slug: "regression-models"
hidden: false
createdAt: "2022-04-19T20:11:30.130Z"
updatedAt: "2022-12-13T22:42:35.292Z"
---
## Onboarding a Regression Model

Suppose you would like to onboard a regression model for the following dataset.

![](https://files.readme.io/f17fd5e-wine_df.png "wine_df.png")

Following is an example of how you would construct a [`fdl.ModelInfo`](https://api.fiddler.ai/#fdl-modelinfo) object and onboard such a model.

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'wine_data'
MODEL_ID = 'regression_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.REGRESSION
model_target = 'quality'
model_outputs = ['predicted_quality']
model_features = [
    'fixed_acidity',
    'volatile_acidity',
    'citric_acid',
    'residual_sugar',
    'chlorides',
    'free_sulfur_dioxide',
    'total_sulfur_dioxide',
    'density',
    'ph',
    'sulphates',
    'alcohol'
]

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id=DATASET_ID,
    target=model_target,
    outputs=model_outputs,
    model_task=model_task
)

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```



> 🚧 Note
> 
> If you **do not provide model predictions** in the DataFrame used to infer the [`fdl.DatasetInfo`](https://api.fiddler.ai/#fdl-datasetinfo) object, you’ll need to pass a dictionary into the `outputs` argument of [`fdl.ModelInfo.from_dataset_info`](https://api.fiddler.ai/#fdl-modelinfo-from_dataframe) that contains the **min and max values** for the model output.
> 
> ```python
> model_outputs = {
>     'predicted_quality': (0.0, 1.0)
> }
> ```