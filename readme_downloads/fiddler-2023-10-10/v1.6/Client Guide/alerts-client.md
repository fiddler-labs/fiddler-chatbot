---
title: "Alerts with Fiddler Client"
slug: "alerts-client"
hidden: false
createdAt: "2022-10-25T16:49:32.709Z"
updatedAt: "2023-04-06T22:17:14.087Z"
---
The complete user guide for alerts and setting up alert rules in the Fiddler UI is provided [here](doc:alerts-ui). In addition to using the Fiddler UI, users have the flexibility to set up alert rules using the Fiddler API client. In particular, the Fiddler client enables the following workflows:

- Add alert rules
- Delete alert rules
- Get the list of all alert rules
- Get the list of triggered alerts

In this document we present examples of how to use the Fiddler client for different alert rule tasks.

## Add an Alert Rule

The Fiddler client can be used to create a variety of alert rules. Rules can be of **Data Drift**, **Performance**, **Data Integrity**, and **Service Metrics ** types and they can be compared to absolute or to relative values.

### Notifications

Before creating a new alert rule, users choose the type of the notification that will be leveraged by Fiddler when an alert is raised. Currently Fiddler client supports email and PagerDuty services as notifications. To create a notification configuration we call the [build_notifications_config()](https://dash.readme.com/project/fiddler/v1.5/refs/clientbuild_notifications_config) API. For example, the following code snippet creates a notification configuration using a comma separated list of email addresses.

```python python
notifications_config_emails = client.build_notifications_config(
  emails = "username_1@email.com,username_2@email.com"
)
```



To create a notification configuration using both email addresses and pager duty.

```python python
notifications_config = client.build_notifications_config(
  emails = "username_1@email.com,username_2@email.com"
  pagerduty_services = 'pagerduty_service_1,"pagerduty_service_2",
  pagerduty_severity = 'critical'
)
```



### Example 1: Data Integrity Alert Rule to compare against a raw value

Now let's sets up a Data Integrity alert rule which triggers an email notification when published events have 5% null values in any 1 hour bin for the _age_ column. Notice compare_to = 'raw_value'. The [add_alert_rule()](https://dash.readme.com/project/fiddler/v1.5/refs/clientadd_alert_rule) API is used to create alert rules.

```python
client.add_alert_rule(
    name = "age-null-1hr",
    project_id = PROJECT_ID,
    model_id = MODEL_ID,
    alert_type = fdl.AlertType.DATA_INTEGRITY,
    metric = fdl.Metric.MISSING_VALUE,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.RAW_VALUE,
    warning_threshold = 5,
    critical_threshold = 10,
    condition = fdl.AlertCondition.GREATER,
    column = "age",
    priority = fdl.Priority.HIGH,
    notifications_config = notifications_config
)
```



Please note, the possible values for bin_size are 'one_hour', 'one_day', and 'seven_days'. When  alert_type is 'data_integrity', use one of 'missing_value', 'range_violation', or 'type_violation' for metric type. 

### Example 2: Performance Alert Rule to compare against a previous time window

And the following API call sets up a Performance alert rule which triggers an email notification when precision metric is 5% higher than that from 1 hr bin one day ago. Notice compare_to = 'time_period' and compare_period = '1 day'.

```python
client.add_alert_rule(
    name = "perf-gt-5prec-1hr-1d-ago",
    project_id = 'project-a',
    model_id = 'model-a',
    alert_type = fdl.AlertType.PERFORMANCE,
    metric = fdl.Metric.PRECISION,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.TIME_PERIOD,
    compare_period = fdl.ComparePeriod.ONE_DAY,
    warning_threshold = 0.05,
    critical_threshold = 0.1,
    condition = fdl.AlertCondition.GREATER,
    priority = fdl.Priority.HIGH,
    notifications_config = notifications_config
)
```



Please note, the possible values for compare_period are 'one_day', 'seven_days', 'one_month', and 'three_months'.

## Get Alert Rules

The [get_alert_rules()](https://dash.readme.com/project/fiddler/v1.5/refs/clientget_alert_rules) API can be used to get a list of all alert rules with respect to the filtering parameters and it returns a paginated list of alert rules.

```python
import fiddler as fdl

alert_rules = client.get_alert_rules(
    project_id = 'project-a',
    model_id = 'model-a', 
    alert_type = fdl.AlertType.DATA_INTEGRITY, 
    metric = fdl.Metric.MISSING_VALUE,
    column = "age", 
    ordering = ['critical_threshold'], #['-critical_threshold'] for descending
    limit= 4, ## to set the number of rules to show in one go
    offset = 0, # page offset (multiple of limit)
)
```



Here is an example output of get_alert_rules() API:

```
[AlertRule(alert_rule_uuid='9b8711fa-735e-4a72-977c-c4c8b16543ae',
           organization_name='some_org_name',
           project_id='some_project_id',
           model_id='some_model_id',
           name='age-null-1hr',
           alert_type=AlertType.DATA_INTEGRITY,
           metric=Metric.MISSING_VALUE,
           column='age',
           priority=Priority.HIGH,
           compare_to=CompareTo.RAW_VALUE,
           compare_period=None,
           warning_threshold=0.05,
           critical_threshold=0.1,
           condition=AlertCondition.GREATER,
           bin_size=BinSize.ONE_HOUR)]
```



## Delete an Alert Rule

To delete an alert rule we need the corresponding unique **alert_rule_uuid** which is part of the output we get from  [get_alert_rules()](https://dash.readme.com/project/fiddler/v1.5/refs/clientget_alert_rules). Then we can delete a rule by calling the [delete_alert_rule()](https://dash.readme.com/project/fiddler/v1.5/refs/clientdelete_alert_rule)  API as shown below:

```python
client.delete_alert_rule(alert_rule_uuid = "some_alert_rule_uuid")
```



## Get Triggered Alerts

Finally, to get a paginated list of triggered alerts for a given alert rule in a given time range we can call the [get_triggered_alerts()](https://dash.readme.com/project/fiddler/v1.5/refs/clientget_triggered_alerts) API as the following:

```python
triggered_alerts = client.get_triggered_alerts(
    alert_rule_uuid = "some_alert_rule_uuid",
    start_time = "2022-05-01",
    end_time = "2022-09-30"
    ordering = ['alert_time_bucket'], #['-alert_time_bucket'] for descending, optional.
    limit= 4, ## to set number of rules to show in one go, optional.
    offset = 0, # optional, page offset.
)
```



```python
trigerred_alerts = client.get_triggered_alerts(
    alert_rule_uuid = "some_alert_rule_uuid",
    start_time = "2022-05-01",
    end_time = "2022-09-30"
    ordering = ['alert_time_bucket'], #['-alert_time_bucket'] for descending, optional.
    limit= 4, ## to set number of rules to show in one go, optional.
    offset = 0, # optional, page offset.
)
```