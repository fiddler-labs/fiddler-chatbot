---
title: "fdl.BaselineType"
slug: "fdlbaselinetype"
excerpt: "Enum for different types of baselines"
hidden: false
createdAt: "2023-02-01T00:05:29.179Z"
updatedAt: "2023-10-24T04:14:06.818Z"
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