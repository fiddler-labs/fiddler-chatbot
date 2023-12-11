---
title: "client.get_baseline"
slug: "get_baseline"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Thu Nov 03 2022 16:48:00 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
`get_baseline` helps get the configuration parameters of the existing baseline

| Input Parameter | Type   | Required | Description                            |
| :-------------- | :----- | :------- | :------------------------------------- |
| project_id      | string | Yes      | The unique identifier for the project  |
| model_id        | string | Yes      | The unique identifier for the model    |
| baseline_id     | string | Yes      | The unique identifier for the baseline |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'
BASELINE_NAME = 'example_preconfigured'


baseline = client.get_baseline(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
)
```



| Return Type                     | Description                                                  |
| :------------------------------ | :----------------------------------------------------------- |
| [fdl.Baseline](ref:fdlbaseline) | Baseline schema object with all the configuration parameters |