---
title: "client.delete_baseline"
slug: "delete_baseline"
hidden: false
createdAt: "2022-11-03T16:49:42.846Z"
updatedAt: "2023-10-24T04:14:06.831Z"
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