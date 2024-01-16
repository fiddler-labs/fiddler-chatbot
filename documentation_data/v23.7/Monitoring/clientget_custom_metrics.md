---
title: "client.get_custom_metrics"
slug: "clientget_custom_metrics"
excerpt: "Gets details about all user-defined Custom Metrics for a given model."
hidden: false
createdAt: "Thu Oct 26 2023 17:18:33 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
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
