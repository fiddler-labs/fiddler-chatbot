---
title: "fdl.WindowSize"
slug: "fdlwindowsize"
excerpt: "Enum for supported window sizes as seconds"
hidden: false
createdAt: "2023-02-08T23:50:58.012Z"
updatedAt: "2023-05-11T19:23:12.314Z"
---
| Enum                     | Value  |
| :----------------------- | :----- |
| fdl.WindowSize.ONE_HOUR  | 3600   |
| fdl.WindowSize.ONE_DAY   | 86400  |
| fdl.WindowSize.ONE_WEEK  | 604800 |
| fdl.WindowSize.ONE_MONTH | 259200 |

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