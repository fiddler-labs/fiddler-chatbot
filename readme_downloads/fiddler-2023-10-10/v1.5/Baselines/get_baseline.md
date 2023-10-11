---
title: "client.get_baseline"
slug: "get_baseline"
hidden: true
createdAt: "2022-11-03T16:48:00.709Z"
updatedAt: "2022-12-08T21:52:05.761Z"
---
get_baseline helps get the configuration parameters of existing baseline

| Input Parameter | Type   | Default | Description                                          |
| :-------------- | :----- | :------ | :--------------------------------------------------- |
| project_id      | string |         | project name to which the baseline is being added to |
| baseline_id     | string |         | name for the existing baseline to be attached        |

```python Usage
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_preconfigured'


client.get_baseline(
  PROJECT_NAME,
  BASELINE_NAME,

)
```