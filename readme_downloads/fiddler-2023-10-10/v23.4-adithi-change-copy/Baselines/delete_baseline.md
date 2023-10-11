---
title: "client.delete_baseline"
slug: "delete_baseline"
excerpt: "Delete a baseline from a project"
hidden: false
createdAt: "2022-11-03T16:49:42.846Z"
updatedAt: "2023-08-01T13:48:06.699Z"
---
Deletes an existing baseline from a project

| Input Parameter | Type | Default | Description                                         |
| :-------------- | :--- | :------ | :-------------------------------------------------- |
| project_id      | str  | None    | `Deprecated` The unique identifier for the project  |
| model_id        | str  | None    | `Deprecated` The unique identifier for the model    |
| baseline_id     | str  | None    | `Deprecated` The unique identifier for the baseline |
| project_name    | str  | None    | The unique identifier for the project               |
| model_name      | str  | None    | The unique identifier for the model                 |
| baseline_name   | str  | None    | The unique identifier for the baseline              |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'
BASELINE_NAME = 'example_preconfigured'


client.delete_baseline(
  project_name=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
)
```