---
title: "client.add_custom_metric"
slug: "clientadd_custom_metric"
excerpt: "Adds a user-defined Custom Metric to a model."
hidden: true
metadata: 
createdAt: "2023-10-26T17:22:50.764Z"
updatedAt: "2023-10-26T17:31:12.051Z"
---
For details on supported constants, operators, and functions, see [Custom Metrics](doc:custom-metrics).

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