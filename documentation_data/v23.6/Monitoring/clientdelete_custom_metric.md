---
title: "client.delete_custom_metric"
slug: "clientdelete_custom_metric"
excerpt: "Deletes a user-defined Custom Metric from a model."
hidden: false
createdAt: "Thu Oct 26 2023 17:22:55 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Nov 21 2023 22:21:56 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type   | Required | Description                                 |
| :-------------- | :----- | :------- | :------------------------------------------ |
| uuid            | string | Yes      | The unique identifier for the custom metric |

```python Usage
METRIC_ID = '7d06f905-80b1-4a41-9711-a153cbdda16c'

client.delete_custom_metric(
  metric_id=METRIC_ID
)
```