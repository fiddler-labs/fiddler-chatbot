---
title: "client.list_baselines"
slug: "list_baselines"
excerpt: ""
hidden: false
createdAt: "Thu Nov 03 2022 16:51:18 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
Gets all the baselines in a project or attached to a single model within a project

| Input Parameter | Type   | Required | Description                           |
| :-------------- | :----- | :------- | :------------------------------------ |
| project_id      | string | Yes      | The unique identifier for the project |
| model_id        | string | No       | The unique identifier for the model   |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'

# list baselines across all models within a project
client.list_baselines(
  project_id=ROJECT_NAME
)

# list baselines within a model
client.list_baselines(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
)
```

| Return Type                             | Description                     |
| :-------------------------------------- | :------------------------------ |
| [List\[fdl.Baseline\]](ref:fdlbaseline) | List of baseline config objects |
