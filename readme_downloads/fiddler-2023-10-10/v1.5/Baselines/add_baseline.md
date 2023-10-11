---
title: "client.add_baseline"
slug: "add_baseline"
hidden: true
createdAt: "2022-10-21T23:22:31.706Z"
updatedAt: "2022-12-08T21:52:29.791Z"
---
| Input Parameter | Type   | Default | Description                                                                                                                                |
| :-------------- | :----- | :------ | :----------------------------------------------------------------------------------------------------------------------------------------- |
| project_id      | string |         | project name to which the baseline is being added to                                                                                       |
| name            | string |         | name for the baseline being configured                                                                                                     |
| model_id        | string |         | model on which we can use the baseline                                                                                                     |
| type            | string |         | one of : PRE_PRODUCTION, STATIC_PRODUCTION, ROLLING_PRODUCTION                                                                             |
| dataset_id      | string |         | (optional) training or validation dataset uploaded to Fiddler. Required when setting up "PRE_PRODUCTION" baseline                          |
| start_time      | int    |         | (optional) time in millisecond to be used as start time of static time window on production data for "STATIC_PRODUCTION" baseline          |
| end_time        | int    |         | (optional) time in millisecond to be used as end time of static time window on production data for "STATIC_PRODUCTION" baseline            |
| offset          | int    |         | (optional) seconds from current time to be used for "ROLLING_PRODUCTION" baseline. Events from the current model will be used as baseline. |
| window_size     | int    |         | (optional) width of window in seconds to be used for "ROLLING_PRODUCTION" baseline. Supported windows are 3600, 86400, 604800, 2592000     |

### Add a pre-production baseline

```python Usage
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_pre'
DATASET_NAME = 'example_validation'
MODEL_NAME = 'example_model'


client.add_baseline(
  PROJECT_NAME,
  MODEL_NAME,
  BASELINE_NAME,
  type='PRE_PRODUCTION', 
  dataset_name=DATASET_NAME, 
)
```



### Add a static production baseline

```python
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_static'
DATASET_NAME = 'example_dataset'
START_TIME = 1656658800000 # JULY 01 2022
END_TIME = 1659164400000 # JULY 30 2022


client.add_baseline(
  PROJECT_NAME,
  MODEL_NAME,
  BASELINE_NAME,
  type='STATIC_PRODUCTION',
  start_time=START_TIME,
  end_time=END_TIME,
)
```



### Add a rolling time window baseline

```python Usage
PROJECT_NAME = 'example_project'
BASELINE_NAME = 'example_rolling'
DATASET_NAME = 'example_validation'
MODEL_NAME = 'example_model'
MONTH_AGO=259200
WEEK_WINDOW=604800

client.add_baseline(
  PROJECT_NAME,
  MODEL_NAME,
  BASELINE_NAME,
  type='ROLLING_PRODUCTION', 
  offset=MONTH_AGO,
  window_size=WEEK_WINDOW,
)
```