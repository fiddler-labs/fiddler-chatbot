---
title: "fdl.ComparePeriod"
slug: "fdlcompareperiod"
excerpt: "Supported Relative comparison values time period"
hidden: false
createdAt: "2022-11-21T13:29:21.415Z"
updatedAt: "2022-12-14T21:34:02.172Z"
---
**Required when compare_to = CompareTo.TIME_PERIOD, this field is used to set when comparing against the same bin for a previous time period. Choose from the following:**

[block:parameters]
{
  "data": {
    "h-0": "Enums",
    "h-1": "values",
    "0-0": "fdl.ComparePeriod.ONE_DAY",
    "0-1": "86400000 millisecond  \ni.e 1 day",
    "1-0": "fdl.ComparePeriod.SEVEN_DAYS",
    "1-1": "604800000 millisecond  \ni.e 7 days",
    "2-0": "fdl.ComparePeriod.ONE_MONTH",
    "2-1": "2629743000 millisecond  \ni.e 30 days",
    "3-0": "fdl.ComparePeriod.THREE_MONTHS",
    "3-1": "7776000000 millisecond  \ni.e 90 days"
  },
  "cols": 2,
  "rows": 4,
  "align": [
    "left",
    "left"
  ]
}
[/block]

```coffeescript Usage
import fiddler as fdl

client.add_alert_rule(
    name = "perf-gt-5prec-1hr-1d-ago",
    project_name = 'project-a',
    model_name = 'model-a',
    alert_type = fdl.AlertType.PERFORMANCE, 
    metric = fdl.Metric.PRECISION,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.TIME_PERIOD,
    compare_period = fdl.ComparePeriod.ONE_DAY, <----
    warning_threshold = 0.05,
    critical_threshold = 0.1,
    condition = fdl.AlertCondition.GREATER,
    priority = fdl.Priority.HIGH,
    notifications_config = notifications_config
)
```
```coffeescript Outputs
[AlertRule(alert_rule_uuid='9b8711fa-735e-4a72-977c-c4c8b16543ae',
           organization_name='some_org_name',
           project_id='project-a',
           model_id='model-a',
           name='perf-gt-5prec-1hr-1d-ago',
           alert_type=AlertType.PERFORMANCE, 
           metric=Metric.PRECISION,
           priority=Priority.HIGH,
           compare_to='CompareTo.TIME_PERIOD,
           compare_period=ComparePeriod.ONE_DAY, <----
           compare_threshold=None,
           raw_threshold=None,
           warning_threshold=0.05,
           critical_threshold=0.1,
           condition=AlertCondition.GREATER,
           bin_size=BinSize.ONE_HOUR)]
```