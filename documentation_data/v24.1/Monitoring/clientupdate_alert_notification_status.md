---
title: "client.update_alert_notification_status"
slug: "clientupdate_alert_notification_status"
excerpt: "To enable/disable the notifications for a list of Alert Ids or for a given Model Id."
hidden: false
createdAt: "Wed Jan 10 2024 06:55:26 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 10 2024 07:06:50 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameters    | Type                 | Default | Description                                          |
| :------------------ | :------------------- | :------ | :--------------------------------------------------- |
| notification_status | bool                 | None    | The status of notification for the alerts.           |
| alert_config_ids    | Optional\[List[str]] | None    | List of Alert Ids that we want to update.            |
| model_id            | Optional[str]        | None    | The Model Id for which we want to update all alerts. |

> 📘 Info
> 
> The Fiddler client can be used to update the notification status of multiple alerts at once.

```python Model

updated_alert_configs = client.update_alert_notification_status(
    notification_status = True,
    model_id = "9f8180d3-3fa0-40c4-8656-b9b1d2de1b69",
)
```
```Text Alert Ids
updated_alert_configs = client.update_alert_notification_status(
    notification_status = True,
    alert_config_ids = ["9b8711fa-735e-4a72-977c-c4c8b16543ae"],
)
```

| Return Type     | Description                                   |
| :-------------- | :-------------------------------------------- |
| List[AlertRule] | List of Alert Rules updated from this method. |

Example responses:

```python Response for time_period rule
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
           bin_size=BinSize.ONE_HOUR)]
```
