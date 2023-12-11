---
title: "client.add_alert_rule"
slug: "clientadd_alert_rule"
excerpt: "To add an alert rule"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Nov 01 2022 05:06:57 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "name",
    "0-1": "str",
    "0-2": "None",
    "0-3": "A name for the alert rule",
    "1-0": "project_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The unique identifier for the project.",
    "2-0": "model_id",
    "2-1": "str",
    "2-2": "None",
    "2-3": "The unique identifier for the model.",
    "3-0": "alert_type",
    "3-1": "[fdl.AlertType](ref:fdlalerttype)",
    "3-2": "None",
    "3-3": "One of `AlertType.PERFORMANCE`,  \n`AlertType.DATA_DRIFT`,  \n`AlertType.DATA_INTEGRITY`, `AlertType.SERVICE_METRICS`, or  \n`AlertType.STATISTIC`",
    "4-0": "metric",
    "4-1": "[fdl.Metric](ref:fdlmetric)",
    "4-2": "None",
    "4-3": "When alert_type is `AlertType.SERVICE_METRICS` this should be `Metric.TRAFFIC`.  \n  \nWhen alert_type is `AlertType.PERFORMANCE`, choose one of the following based on the ML model task:  \n  \nFor binary_classfication:  \n`Metric.ACCURACY`  \n`Metric.TPR`  \n`Metric.FPR`  \n`Metric.PRECISION`  \n`Metric.RECALL`  \n`Metric.F1_SCORE`  \n`Metric.ECE`  \n`Metric.AUC`  \n  \nFor regression:  \n`Metric.R2`  \n`Metric.MSE`  \n`Metric.MAE`  \n`Metric.MAPE`  \n`Metric.WMAPE`  \n  \nFor multi-class classification:  \n`Metric.ACCURACY`  \n`Metric.LOG_LOSS`  \n  \nFor ranking:  \n`Metric.MAP`  \n`Metric.MEAN_NDCG`  \n  \nWhen alert_type is `AlertType.DATA_DRIFT` choose one of the following:  \n`Metric.PSI`  \n`Metric.JSD`  \n  \nWhen alert_type is `AlertType.DATA_INTEGRITY` choose one of the following:  \n`Metric.RANGE_VIOLATION`  \n`Metric.MISSING_VALUE`  \n`Metric.TYPE_VIOLATION`  \n  \nWhen alert_type is `AlertType.STATISTIC` choose one of the following:  \n`Metric.AVERAGE`  \n`Metric.SUM`",
    "5-0": "bin_size",
    "5-1": "[fdl.BinSize](ref:fdlbinsize)",
    "5-2": "ONE_DAY",
    "5-3": "Duration for which the metric value is calculated. Choose one of the following:  \n`BinSize.ONE_HOUR`  \n`BinSize.ONE_DAY` `BinSize.SEVEN_DAYS`",
    "6-0": "compare_to",
    "6-1": "[fdl.CompareTo](ref:fdlcompareto)",
    "6-2": "None",
    "6-3": "Whether the metric value compared against a static value or the same bin from a previous time period.  \n`CompareTo.RAW_VALUE` `CompareTo.TIME_PERIOD`.",
    "7-0": "compare_period",
    "7-1": "[fdl.ComparePeriod](ref:fdlcompareperiod)",
    "7-2": "None",
    "7-3": "Required only when `CompareTo` is `TIME_PERIOD`. Choose one of the following: `ComparePeriod.ONE_DAY `  \n`ComparePeriod.SEVEN_DAYS` `ComparePeriod.ONE_MONTH`  \n`ComparePeriod.THREE_MONTHS`",
    "8-0": "priority",
    "8-1": "[fdl.Priority](ref:fdlpriority)",
    "8-2": "None",
    "8-3": "`Priority.LOW`  \n`Priority.MEDIUM`  \n`Priority.HIGH`",
    "9-0": "warning_threshold",
    "9-1": "float",
    "9-2": "None",
    "9-3": "[Optional] Threshold value to crossing which a warning level severity alert will be triggered.  This should be a decimal which represents a percentage (e.g. 0.45).",
    "10-0": "critical_threshold",
    "10-1": "float ",
    "10-2": "None",
    "10-3": "Threshold value to crossing which a critical level severity alert will be triggered.  This should be a decimal which represents a percentage (e.g. 0.45).",
    "11-0": "condition",
    "11-1": "[fdl.AlertCondition](ref:fdlalertcondition)",
    "11-2": "None",
    "11-3": "Specifies if the rule should trigger if the metric is greater than or less than the thresholds. `AlertCondition.LESSER `  \n`AlertCondition.GREATER`",
    "12-0": "notifications_config",
    "12-1": "Dict\\[str, Dict[str, Any]]",
    "12-2": "None",
    "12-3": "[Optional] notifications config object created using helper method [build_notifications_config()](ref:clientbuild_notifications_config)",
    "13-0": "columns",
    "13-1": "List[str]",
    "13-2": "None",
    "13-3": "Column names on which alert rule is to be created.  \nApplicable only when alert_type is AlertType.DATA_INTEGRITY or AlertType.DRIFT. When alert type is AlertType.DATA_INTEGRITY, it can take \\*[**\\*ANY\\*\\**]\\* to check for all columns.",
    "14-0": "baseline_id",
    "14-1": "str",
    "14-2": "None",
    "14-3": "Name of the baseline whose histogram is compared against the same derived from current data. When no baseline_id is specified then the [default baseline](doc:fiddler-baselines) is used.  \n  \nUsed only when alert type is `AlertType.DATA_DRIFT`."
  },
  "cols": 4,
  "rows": 15,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]


> 📘 Info
> 
> The Fiddler client can be used to create a variety of alert rules. Rules can be of **Data Drift**, **Performance**, **Data Integrity**, and **Service Metrics ** types and they can be compared to absolute (compare_to = RAW_VALUE) or to relative values (compare_to = TIME_PERIOD).

```python Usage - time_period
# To add a Performance type alert rule which triggers an email notification 
# when precision metric is 5% higher than that from 1 hr bin one day ago.

import fiddler as fdl

notifications_config = client.build_notifications_config(
    emails = "user_1@abc.com, user_2@abc.com",
)
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
```python Usage - raw_value

# To add Data Integrity alert rule which triggers an email notification when 
# published events have more than 5 null values in any 1 hour bin for the _age_ column. 
# Notice compare_to = fdl.CompareTo.RAW_VALUE.

import fiddler as fdl

client.add_alert_rule(
    name = "age-null-1hr",
    project_id = 'project-a',
    model_id = 'model-a',
    alert_type = fdl.AlertType.DATA_INTEGRITY,
    metric = fdl.Metric.MISSING_VALUE,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.RAW_VALUE,
    priority = fdl.Priority.HIGH,
    warning_threshold = 5,
    critical_threshold = 10,
    condition = fdl.AlertCondition.GREATER,
    column = "age",
    notifications_config = notifications_config
)
```
```python Usage - baseline
# To add a Data Drift type alert rule which triggers an email notification 
# when PSI metric for 'age' column from an hr is 5% higher than that from 'baseline_name' dataset.

import fiddler as fdl

client.add_baseline(project_id='project-a', 
                    model_id='model-a', 
                    baseline_name='baseline_name', 
                    type=fdl.BaselineType.PRE_PRODUCTION, 
                    dataset_id='dataset-a')

notifications_config = client.build_notifications_config(
    emails = "user_1@abc.com, user_2@abc.com",
)

client.add_alert_rule(
    name = "psi-gt-5prec-age-baseline_name",
    project_id = 'project-a',
    model_id = 'model-a',
    alert_type = fdl.AlertType.DATA_DRIFT,
    metric = fdl.Metric.PSI,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.RAW_VALUE,
    warning_threshold = 0.05,
    critical_threshold = 0.1,
    condition = fdl.AlertCondition.GREATER,
    priority = fdl.Priority.HIGH,
    notifications_config = notifications_config,
    columns = ["age"],
    baseline_id = 'baseline_name'
)
```
```python Usage - multiple columns
# To add Drift type alert rule which triggers an email notification when 
# value of JSD metric is more than 0.5 for one hour bin for  _age_ or _gender_ columns. 
# Notice compare_to = fdl.CompareTo.RAW_VALUE.

import fiddler as fdl
notifications_config = client.build_notifications_config(
    emails = "user_1@abc.com, user_2@abc.com",
)

client.add_alert_rule(
    name = "jsd_multi_col_1hr",
    project_id = 'project-a',
    model_id = 'model-a',
    alert_type = fdl.AlertType.DATA_DRIFT,
    metric = fdl.Metric.JSD,
    bin_size = fdl.BinSize.ONE_HOUR, 
    compare_to = fdl.CompareTo.RAW_VALUE,
    warning_threshold = 0.4,
    critical_threshold = 0.5,
    condition = fdl.AlertCondition.GREATER,
    priority = fdl.Priority.HIGH,
    notifications_config = notifications_config,
    columns = ["age", "gender"],
)
```

| Return Type | Description               |
| :---------- | :------------------------ |
| Alert Rule  | Created Alert Rule object |

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
```python Response for raw_value rule
AlertRule(alert_rule_uuid='e1aefdd5-ef22-4e81-b869-3964eff8b5cd', 
organization_name='some_org_name', 
project_id='project-a', 
model_id='model-a', 
name='age-null-1hr', 
alert_type=AlertType.DATA_INTEGRITY, 
metric=Metric.MISSING_VALUE, 
column='age', 
priority=Priority.HIGH, 
compare_to=CompareTo.RAW_VALUE, 
compare_period=None, 
warning_threshold=5, 
critical_threshold=10, 
condition=AlertCondition.GREATER,
bin_size=BinSize.ONE_HOUR)

```
```python Response for baseline rule
AlertRule(alert_rule_uuid='e1aefdd5-ef22-4e81-b869-3964eff8b5cd', 
organization_name='some_org_name', 
project_id='project-a', 
model_id='model-a', 
name='psi-gt-5prec-age-baseline_name', 
alert_type=AlertType.DATA_DRIFT, 
metric=Metric.PSI, 
priority=Priority.HIGH, 
compare_to=CompareTo.RAW_VALUE, 
compare_period=None, 
warning_threshold=5, 
critical_threshold=10, 
condition=AlertCondition.GREATER,
bin_size=BinSize.ONE_HOUR,
columns=['age'],
baseline_id='baseline_name')
```
```python Response for multiple column rule
[AlertRule(alert_rule_uuid='9b8711fa-735e-4a72-977c-c4c8b16543ae',
           organization_name='some_org_name',
           project_id='project-a',
           model_id='model-a',
           name='perf-gt-5prec-1hr-1d-ago',
           alert_type=AlertType.DRIFT,
           metric=Metric.JSD,
           priority=Priority.HIGH,
           compare_to='CompareTo.RAW_VALUE,
           compare_period=ComparePeriod.ONE_HOUR,
           compare_threshold=None,
           raw_threshold=None,
           warning_threshold=0.4,
           critical_threshold=0.5,
           condition=AlertCondition.GREATER,
           bin_size=BinSize.ONE_HOUR,
           columns=['age', 'gender'])]
```