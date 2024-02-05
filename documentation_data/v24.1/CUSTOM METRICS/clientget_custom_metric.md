---
title: "client.get_custom_metric"
slug: "clientget_custom_metric"
excerpt: "Gets details about a user-defined Custom Metric."
hidden: false
createdAt: "Thu Oct 26 2023 17:14:40 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type   | Required | Description                                 |
| :-------------- | :----- | :------- | :------------------------------------------ |
| metric_id       | string | Yes      | The unique identifier for the custom metric |

```python Usage
METRIC_ID = '7d06f905-80b1-4a41-9711-a153cbdda16c'

custom_metric = client.get_custom_metric(
  metric_id=METRIC_ID
)
```

| Return Type                                 | Description                                        |
| :------------------------------------------ | :------------------------------------------------- |
| `fiddler.schema.custom_metric.CustomMetric` | Custom metric object with details about the metric |
