---
title: "client.delete_segment"
slug: "clientdelete_segment"
excerpt: "Deletes a user-defined Segment from a model."
hidden: false
createdAt: "Wed Jan 10 2024 18:30:30 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 24 2024 20:51:25 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type   | Required | Description                           |
| :-------------- | :----- | :------- | :------------------------------------ |
| segment_id      | string | Yes      | The unique identifier for the segment |

```python Usage
SEGMENT_ID = '7d06f905-80b1-4a41-9711-a153cbdda16c'

client.delete_segment(
  segment_id=SEGMENT_ID
)
```
