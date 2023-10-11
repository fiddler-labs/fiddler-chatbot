---
title: "client.list_baselines"
slug: "list_baselines"
excerpt: "List all the baselines associated to a model in a project"
hidden: false
createdAt: "2022-11-03T16:51:18.142Z"
updatedAt: "2023-08-01T13:09:49.703Z"
---
> 🚧 Deprecated
> 
> This client method is deprecated and will be removed in the future versions. Use _client.get_project_names()_ instead.  
> Reference: [client.get_baselines](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_baselines)

Gets all the baselines in a project or attached to a single model within a project

| Input Parameter | Type | Default | Description                           |
| :-------------- | :--- | :------ | :------------------------------------ |
| project_id      | str  | None    | The unique identifier for the project |
| model_id        | str  | None    | The unique identifier for the model   |

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