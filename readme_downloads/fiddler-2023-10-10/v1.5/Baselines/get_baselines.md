---
title: "client.get_baselines"
slug: "get_baselines"
hidden: true
createdAt: "2022-11-03T16:51:18.142Z"
updatedAt: "2022-12-08T21:51:21.086Z"
---
Gets all the baselines attached to a model

| Input Parameter | Type   | Default | Description                                          |
| :-------------- | :----- | :------ | :--------------------------------------------------- |
| project_id      | string |         | project name to which the baseline is being added to |
| model_id        | string |         | name of the model                                    |

```python Usage
PROJECT_NAME = 'example_project'
MODEL_NAME = 'example_model'


client.get_baselines(
  PROJECT_NAME,
  MODEL_NAME,
)
```