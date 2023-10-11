---
title: "client.get_baselines"
slug: "clientget_baselines"
excerpt: "List all the baselines associated to a model in a project"
hidden: true
createdAt: "2023-08-01T13:04:50.574Z"
updatedAt: "2023-08-01T13:47:56.045Z"
---
Gets all the baselines in a project or attached to a single model within a project

| Input Parameter | Type | Default | Description                                        |
| :-------------- | :--- | :------ | :------------------------------------------------- |
| project_id      | str  | None    | `Deprecated` The unique identifier for the project |
| model_id        | str  | None    | `Deprecated` The unique identifier for the model   |
| project_name    | str  | None    | The unique identifier for the project              |
| model_name      | str  | None    | The unique identifier for the model                |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

# list baselines across all models within a project
client.get_baselines(
  project_name=ROJECT_NAME
)

# list baselines within a model
client.get_baselines(
  project_name=PROJECT_NAME,
  model_name=MODEL_NAME,
)
```

| Return Type                             | Description                     |
| :-------------------------------------- | :------------------------------ |
| [List\[fdl.Baseline\]](ref:fdlbaseline) | List of baseline config objects |