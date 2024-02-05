---
title: "client.get_segment"
slug: "clientget_segment"
excerpt: "Gets details about a user-defined Segment."
hidden: false
createdAt: "Wed Jan 10 2024 18:30:13 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 24 2024 20:50:45 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type   | Required | Description                           |
| :-------------- | :----- | :------- | :------------------------------------ |
| segment_id      | string | Yes      | The unique identifier for the segment |

```python Usage
SEGMENT_ID = '7d06f905-80b1-4a41-9711-a153cbdda16c'

segment = client.get_segment(
  segment_id=SEGMENT_ID
)
```

| Return Type   | Description                                   |
| :------------ | :-------------------------------------------- |
| `fdl.Segment` | Segment object with details about the segment |
