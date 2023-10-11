---
title: "client.delete_baseline"
slug: "delete_baseline"
hidden: true
createdAt: "2022-11-03T16:49:42.846Z"
updatedAt: "2022-12-08T21:51:44.702Z"
---
Deletes an existing baseline from a project

| Input Parameter | Type   | Default | Description                                          |
| :-------------- | :----- | :------ | :--------------------------------------------------- |
| project_id      | string |         | project name to which the baseline is being added to |
| baseline_id     | string |         | name for the existing baseline to be deleted         |

```python Usage
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_preconfigured'


client.delete_baseline(
  PROJECT_NAME,
  BASELINE_NAME,
)
```