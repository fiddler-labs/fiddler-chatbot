---
title: "LLM"
slug: "llm"
excerpt: "Large Language Model"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Oct 10 2023 18:52:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
## Onboarding an LLM task

Suppose you would like to onboard an LLM model for the following dataset:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f781abd-Screen_Shot_2023-10-10_at_4.24.17_PM.png",
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
DATASET_ID = 'dialogue_data'
MODEL_ID = 'llm_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.LLM

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