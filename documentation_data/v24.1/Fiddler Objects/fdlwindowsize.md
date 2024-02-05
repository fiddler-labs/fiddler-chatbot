---
title: "fdl.WindowSize"
slug: "fdlwindowsize"
excerpt: "Enum for supported window sizes as seconds"
hidden: false
createdAt: "Wed Feb 08 2023 23:50:58 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Jan 09 2024 20:47:26 GMT+0000 (Coordinated Universal Time)"
---
| Enum                     | Value   |
| :----------------------- | :------ |
| fdl.WindowSize.ONE_HOUR  | 3600    |
| fdl.WindowSize.ONE_DAY   | 86400   |
| fdl.WindowSize.ONE_WEEK  | 604800  |
| fdl.WindowSize.ONE_MONTH | 2592000 |

```c Usage
from fiddler import BaselineType, WindowSize

PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_rolling'
DATASET_NAME = 'example_validation'
MODEL_NAME = 'example_model'

client.add_baseline(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
  type=BaselineType.ROLLING_PRODUCTION,
  offset=WindowSize.ONE_MONTH, # How far back to set our window
  window_size=WindowSize.ONE_WEEK, # Size of the sliding window
)
```
