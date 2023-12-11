---
title: "client.add_custom_metric"
slug: "clientadd_custom_metric"
excerpt: "Adds a user-defined Custom Metric to a model."
hidden: false
createdAt: "Thu Oct 26 2023 17:22:50 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Nov 21 2023 22:21:45 GMT+0000 (Coordinated Universal Time)"
---
For details on supported constants, operators, and functions, see [Fiddler Query Language](doc:fiddler-query-language).

| Input Parameter | Type   | Required | Description                                     |
| :-------------- | :----- | :------- | :---------------------------------------------- |
| name            | string | Yes      | Name of the custom metric                       |
| project_id      | string | Yes      | The unique identifier for the project           |
| model_id        | string | Yes      | The unique identifier for the model             |
| definition      | string | Yes      | The FQL metric definition for the custom metric |
| description     | string | No       | A description of the custom metric              |

```python Usage
PROJECT_ID = 'my_project'
MODEL_ID = 'my_model'

definition = """
    average(if(Prediction < 0.5 and Target == 1, -40, if(Prediction >= 0.5 and Target == 0, -400, 250)))
"""

client.add_custom_metric(
    name='Loan Value',
    description='A custom value score assigned to a loan',
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    definition=definition
)
```