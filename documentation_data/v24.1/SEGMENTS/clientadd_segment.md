---
title: "client.add_segment"
slug: "clientadd_segment"
excerpt: "Adds a user-defined Segment to a model."
hidden: false
createdAt: "Wed Jan 10 2024 18:30:24 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Jan 25 2024 14:35:51 GMT+0000 (Coordinated Universal Time)"
---
For details on supported constants, operators, and functions, see [Fiddler Query Language](doc:fiddler-query-language).

| Input Parameter | Type   | Required | Description                               |
| :-------------- | :----- | :------- | :---------------------------------------- |
| name            | string | Yes      | Name of the segment                       |
| project_id      | string | Yes      | The unique identifier for the project     |
| model_id        | string | Yes      | The unique identifier for the model       |
| definition      | string | Yes      | The FQL metric definition for the segment |
| description     | string | No       | A description of the segment              |

```python Usage
PROJECT_ID = 'my_project'
MODEL_ID = 'my_model'

definition = """
    age > 50
"""

client.add_segment(
    name='Over 50',
    description='All people over the age of 50',
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    definition=definition
)
```

```python Example Response
Segment(
  id='50a1c32d-c2b4-4faf-9006-f4aeadd7a859',
  name='Over 50',
  project_name='my_project',
  organization_name='mainbuild',
  definition='age > 50',
  description='All people over the age of 50',
  created_at=None,
  created_by=None
)
```
