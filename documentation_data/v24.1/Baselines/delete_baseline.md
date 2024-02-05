---
title: "client.delete_baseline"
slug: "delete_baseline"
excerpt: ""
hidden: false
createdAt: "Thu Nov 03 2022 16:49:42 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
Deletes an existing baseline from a project

| Input Parameter | Type   | Required | Description                            |
| :-------------- | :----- | :------- | :------------------------------------- |
| project_id      | string | Yes      | The unique identifier for the project  |
| model_id        | string | Yes      | The unique identifier for the model    |
| baseline_id     | string | Yes      | The unique identifier for the baseline |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'
BASELINE_NAME = 'example_preconfigured'


client.delete_baseline(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
)
```
