---
title: "client.get_segments"
slug: "clientget_segments"
excerpt: "Gets details about all user-defined Segments for a given model."
hidden: false
createdAt: "Wed Jan 10 2024 18:30:19 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 24 2024 20:50:59 GMT+0000 (Coordinated Universal Time)"
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

custom_metrics = client.get_segments(
  project_id=PROJECT_ID,
  model_id=MODEL_ID
)
```

| Return Type         | Description                                 |
| :------------------ | :------------------------------------------ |
| `List[fdl.Segment]` | List of segment objects for the given model |
