---
title: "Binary Classification"
slug: "binary-classification"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 20:12:12 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Onboarding a Binary Classification Model

Suppose you would like to onboard a binary classification model for the following dataset.

![](https://files.readme.io/138d2f2-adult_df.png "adult_df.png")

Following is an example of how you would construct a [`fdl.ModelInfo`](ref:fdlmodelinfo) object and onboard such a model.

```python
PROJECT_ID = 'example_project'
DATASET_ID = 'adult_data'
MODEL_ID = 'binary_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.BINARY_CLASSIFICATION
model_target = 'income'
model_outputs = ['probability_over_50k']
model_features = [
    'age',
    'fnlwgt',
    'education_num',
    'capital_gain',
    'capital_loss',
    'hours_per_week'
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
