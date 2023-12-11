---
title: "fdl.BaselineType"
slug: "fdlbaselinetype"
excerpt: "Enum for different types of baselines"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed Feb 01 2023 00:05:29 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
| Enum                                | Description                                                                               |
| :---------------------------------- | :---------------------------------------------------------------------------------------- |
| fdl.BaselineType.PRE_PRODUCTION     | Used for baselines on uploaded datasets.They can be training or validation datasets.      |
| fdl.BaselineType.STATIC_PRODUCTION  | Used to describe a baseline on production events of a model between a specific time range |
| fdl.BaselineType.ROLLING_PRODUCTION | Used to describe a baseline on production events of a model relative to the current time  |

```c Usage
from fiddler import BaselineType

PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_rolling'
DATASET_NAME = 'example_validation'
MODEL_NAME = 'example_model'

client.add_baseline(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
  type=BaselineType.PRE_PRODUCTION,
  dataset_id=DATASET_NAME,
)
```