---
title: "fdl.BinSize"
slug: "fdlbinsize"
excerpt: "Supported Bin Size values for Alert Rules"
hidden: false
createdAt: "Tue Jan 31 2023 07:28:35 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:07 GMT+0000 (Coordinated Universal Time)"
---
**This field signifies the durations for which fiddler monitoring calculates the metric values **

[block:parameters]
{
  "data": {
    "h-0": "Enums",
    "h-1": "Values",
    "0-0": "fdl.BinSize.ONE_HOUR",
    "0-1": "3600 \\* 1000 millisecond  \ni.e one hour",
    "1-0": "fdl.BinSize.ONE_DAY",
    "1-1": "86400 \\* 1000 millisecond  \ni.e one day",
    "2-0": "fdl.BinSize.SEVEN_DAYS",
    "2-1": "604800 \\* 1000 millisecond  \ni.e seven days"
  },
  "cols": 2,
  "rows": 3,
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
    bin_size = fdl.BinSize.ONE_HOUR, <----
    compare_to = fdl.CompareTo.TIME_PERIOD,
    compare_period = fdl.ComparePeriod.ONE_DAY,
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
           compare_period=ComparePeriod.ONE_DAY,
           compare_threshold=None,
           raw_threshold=None,
           warning_threshold=0.05,
           critical_threshold=0.1,
           condition=AlertCondition.GREATER,
           bin_size=BinSize.ONE_HOUR)] <-----
```
