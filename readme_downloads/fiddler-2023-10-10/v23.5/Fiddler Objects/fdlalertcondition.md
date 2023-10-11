---
title: "fdl.AlertCondition"
slug: "fdlalertcondition"
excerpt: "Alert conditions for comparisons"
hidden: false
createdAt: "2023-01-31T07:25:05.386Z"
updatedAt: "2023-01-31T07:25:05.386Z"
---
**If condition = fdl.AlertCondition.GREATER/LESSER is specified, and an alert is triggered every time the metric value is greater/lesser than the specified threshold.**

| Enum                       | Value   |
| :------------------------- | :------ |
| fdl.AlertCondition.GREATER | greater |
| fdl.AlertCondition.LESSER  | lesser  |

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
    compare_period = fdl.ComparePeriod.ONE_DAY,
    warning_threshold = 0.05,
    critical_threshold = 0.1,
    condition = fdl.AlertCondition.GREATER, <-----
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
           alert_type=AlertType.PERFORMANCE, <---
           metric=Metric.PRECISION,
           priority=Priority.HIGH,
           compare_to='CompareTo.TIME_PERIOD,
           compare_period=ComparePeriod.ONE_DAY,
           compare_threshold=None,
           raw_threshold=None,
           warning_threshold=0.05,
           critical_threshold=0.1,
           condition=AlertCondition.GREATER, <-----
           bin_size=BinSize.ONE_HOUR)]
```