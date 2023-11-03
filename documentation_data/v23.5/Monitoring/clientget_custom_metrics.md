---
title: "client.get_custom_metrics"
slug: "clientget_custom_metrics"
excerpt: "Gets details about all user-defined Custom Metrics for a given model."
hidden: true
metadata: 
createdAt: "2023-10-26T17:18:33.877Z"
updatedAt: "2023-10-26T17:30:50.400Z"
---
| Input Parameter | Type          | Default | Required | Description                              |
| :-------------- | :------------ | :------ | :------- | :--------------------------------------- |
| project_id      | string        |         | Yes      | The unique identifier for the project    |
| model_id        | string        |         | Yes      | The unique identifier for the model      |
| limit           | Optional[int] | 300     | No       | Maximum number of items to return        |
| offset          | Optional[int] | 0       | No       | Number of items to skip before returning |

```python Usage
PROJECT_ID = 'my_project'
MODEL_ID = 'my_model'

custom_metrics = client.get_custom_metrics(
  project_id=PROJECT_ID,
  model_id=MODEL_ID
)
```

| Return Type                                       | Description                                       |
| :------------------------------------------------ | :------------------------------------------------ |
| `List[fiddler.schema.custom_metric.CustomMetric]` | List of custom metric objects for the given model |