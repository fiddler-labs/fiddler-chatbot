---
title: "fdl.CompareTo"
slug: "fdlcompareto"
excerpt: "Metrics comparison criteria"
hidden: false
createdAt: "Tue Jan 31 2023 07:26:58 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
**Whether the metric value is to be compared against a static value or the same time bin from a previous time period(set using compare_period\[[ComparePeriod](ref:fdlcompareperiod)]).**

[block:parameters]
{
  "data": {
    "h-0": "Enums",
    "h-1": "Value",
    "0-0": "fdl.CompareTo.RAW_VALUE",
    "0-1": "When comparing to  \nan absolute value",
    "1-0": "fdl.CompareTo.TIME_PERIOD",
    "1-1": "When comparing to the same  \nbin size from a previous time period"
  },
  "cols": 2,
  "rows": 2,
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
    model_name = 'binary_classification_model-a',
    alert_type = fdl.AlertType.PERFORMANCE,
    metric = fdl.Metric.PRECISION,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.TIME_PERIOD, <----
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
           model_id='binary_classification_model-a',
           name='perf-gt-5prec-1hr-1d-ago',
           alert_type=AlertType.PERFORMANCE,
           metric=Metric.PRECISION,
           priority=Priority.HIGH,
           compare_to='CompareTo.TIME_PERIOD, <---
           compare_period=ComparePeriod.ONE_DAY,
           compare_threshold=None,
           raw_threshold=None,
           warning_threshold=0.05,
           critical_threshold=0.1,
           condition=AlertCondition.GREATER,
           bin_size=BinSize.ONE_HOUR)]
```
