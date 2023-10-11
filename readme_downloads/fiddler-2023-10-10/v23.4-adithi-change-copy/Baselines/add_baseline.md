---
title: "client.add_baseline"
slug: "add_baseline"
excerpt: "Adds a baseline to a project using the specified name."
hidden: false
createdAt: "2022-10-21T23:22:31.706Z"
updatedAt: "2023-08-01T13:47:28.485Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_name",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project.",
    "1-0": "model_name",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The unique identifier for the model.",
    "2-0": "baseline_name",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the baseline.",
    "3-0": "dataset_name",
    "3-1": "str",
    "3-2": "None",
    "3-3": "Training or validation dataset uploaded to Fiddler for a PRE_PRODUCTION baseline.",
    "4-0": "project_id",
    "4-1": "str",
    "4-2": "None",
    "4-3": "`Deprecated` The unique identifier for the project.",
    "5-0": "model_id",
    "5-1": "str",
    "5-2": "None",
    "5-3": "`Deprecated` The unique identifier for the model.",
    "6-0": "baseline_id",
    "6-1": "str",
    "6-2": "None",
    "6-3": "`Deprecated` The unique identifier for the baseline.",
    "7-0": "type",
    "7-1": "[fdl.BaselineType](ref:fdlbaselinetype)",
    "7-2": "None",
    "7-3": "one of :  \n  \nPRE_PRODUCTION  \nSTATIC_PRODUCTION  \nROLLING_PRODUCTION",
    "8-0": "dataset_id",
    "8-1": "str",
    "8-2": "None",
    "8-3": "`Deprecated` Training or validation dataset uploaded to Fiddler for a PRE_PRODUCTION baseline.",
    "9-0": "start_time",
    "9-1": "int",
    "9-2": "None",
    "9-3": "seconds since epoch to be used as the start time for STATIC_PRODUCTION baseline.",
    "10-0": "end_time",
    "10-1": "int",
    "10-2": "None",
    "10-3": "seconds since epoch to be used as the end time for STATIC_PRODUCTION baseline.",
    "11-0": "offset",
    "11-1": "[fdl.WindowSize](ref:fdlwindowsize)",
    "11-2": "None",
    "11-3": "offset in seconds relative to the current time to be used for ROLLING_PRODUCTION baseline.",
    "12-0": "window_size",
    "12-1": "[fdl.WindowSize](ref:fdlwindowsize)",
    "12-2": "None",
    "12-3": "width of the window in seconds to be used for ROLLING_PRODUCTION baseline.",
    "13-0": "wait",
    "13-1": "Optional[bool]",
    "13-2": "True",
    "13-3": "Whether to wait for async job to finish(True) or return(False)."
  },
  "cols": 4,
  "rows": 14,
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
  project_name=PROJECT_NAME,
  model_name=MODEL_NAME,
  baseline_name=BASELINE_NAME,
  type=BaselineType.PRE_PRODUCTION, 
  dataset_name=DATASET_NAME, 
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
  project_name=PROJECT_NAME,
  model_name=MODEL_NAME,
  baseline_name=BASELINE_NAME,
  type=BaselineType.PRE_PRODUCTION, 
  dataset_name=DATASET_NAME,
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