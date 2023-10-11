---
title: "client.get_baseline"
slug: "get_baseline"
hidden: false
createdAt: "2022-11-03T16:48:00.709Z"
updatedAt: "2023-08-01T13:47:38.913Z"
---
`get_baseline` helps get the configuration parameters of the existing baseline

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


baseline = client.get_baseline(
  project_name=PROJECT_NAME,
  model_name=MODEL_NAME,
  baseline_name=BASELINE_NAME,
)
```

| Return Type                     | Description                                                  |
| :------------------------------ | :----------------------------------------------------------- |
| [fdl.Baseline](ref:fdlbaseline) | Baseline schema object with all the configuration parameters |