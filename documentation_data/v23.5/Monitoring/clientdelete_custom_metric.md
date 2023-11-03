---
title: "client.delete_custom_metric"
slug: "clientdelete_custom_metric"
excerpt: "Deletes a user-defined Custom Metric from a model."
hidden: true
metadata: 
createdAt: "2023-10-26T17:22:55.406Z"
updatedAt: "2023-10-26T17:31:30.619Z"
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