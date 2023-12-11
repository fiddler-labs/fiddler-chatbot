---
title: "client.add_baseline"
slug: "add_baseline"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Fri Oct 21 2022 23:22:31 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Required",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "string",
    "0-2": "Yes",
    "0-3": "The unique identifier for the project",
    "1-0": "model_id",
    "1-1": "string",
    "1-2": "Yes",
    "1-3": "The unique identifier for the model",
    "2-0": "baseline_id",
    "2-1": "string",
    "2-2": "Yes",
    "2-3": "The unique identifier for the baseline",
    "3-0": "type",
    "3-1": "[fdl.BaselineType](ref:fdlbaselinetype)",
    "3-2": "Yes",
    "3-3": "one of :  \n  \nPRE_PRODUCTION  \nSTATIC_PRODUCTION  \nROLLING_PRODUCTION",
    "4-0": "dataset_id",
    "4-1": "string",
    "4-2": "No",
    "4-3": "Training or validation dataset uploaded to Fiddler for a PRE_PRODUCTION baseline",
    "5-0": "start_time",
    "5-1": "int",
    "5-2": "No",
    "5-3": "seconds since epoch to be used as the start time for STATIC_PRODUCTION baseline",
    "6-0": "end_time",
    "6-1": "int",
    "6-2": "No",
    "6-3": "seconds since epoch to be used as the end time for STATIC_PRODUCTION baseline",
    "7-0": "offset",
    "7-1": "[fdl.WindowSize](ref:fdlwindowsize)",
    "7-2": "No",
    "7-3": "offset in seconds relative to the current time to be used for ROLLING_PRODUCTION baseline",
    "8-0": "window_size",
    "8-1": "[fdl.WindowSize](ref:fdlwindowsize)",
    "8-2": "No",
    "8-3": "width of the window in seconds to be used for ROLLING_PRODUCTION baseline"
  },
  "cols": 4,
  "rows": 9,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

### Add a pre-production baseline

```c Usage
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_pre'
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



### Add a static production baseline

```c Usage
from datetime import datetime
from fiddler import BaselineType, WindowSize

start = datetime(2023, 1, 1, 0, 0) # 12 am, 1st Jan 2023
end = datetime(2023, 1, 2, 0, 0) # 12 am, 2nd Jan 2023

PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_static'
DATASET_NAME = 'example_dataset'
MODEL_NAME = 'example_model'
START_TIME = start.timestamp()
END_TIME = end.timestamp()


client.add_baseline(
  project_id=PROJECT_NAME,
  model_id=MODEL_NAME,
  baseline_id=BASELINE_NAME,
  type=BaselineType.STATIC_PRODUCTION,
  start_time=START_TIME,
  end_time=END_TIME,
)
```



### Add a rolling time window baseline

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



| Return Type                     | Description                                                  |
| :------------------------------ | :----------------------------------------------------------- |
| [fdl.Baseline](ref:fdlbaseline) | Baseline schema object with all the configuration parameters |