---
title: "fdl.Metric"
slug: "fdlmetric"
excerpt: "Supported Metric for different Alert Types in Alert Rules"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Jan 31 2023 07:32:12 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
**Following is the list of metrics, with corresponding alert type and model task, for which an alert rule can be created.**

[block:parameters]
{
  "data": {
    "h-0": "Enum Values",
    "h-1": "Supported for [Alert Types](ref:fdlalerttype)  \n([ModelTask ](ref:fdlmodeltask)restriction if any)",
    "h-2": "Description",
    "0-0": "fdl.Metric.SUM",
    "0-1": "fdl.AlertType.STATISTIC",
    "0-2": "Sum of all values of a column across all events",
    "1-0": "fdl.Metric.AVERAGE",
    "1-1": "fdl.AlertType.STATISTIC",
    "1-2": "Average value of a column across all events",
    "2-0": "fdl.Metric.PSI",
    "2-1": "fdl.AlertType.DATA_DRIFT",
    "2-2": "Population Stability Index",
    "3-0": "fdl.Metric.JSD",
    "3-1": "fdl.AlertType.DATA_DRIFT",
    "3-2": "Jensen–Shannon divergence",
    "4-0": "fdl.Metric.MISSING_VALUE",
    "4-1": "fdl.AlertType.DATA_INTEGRITY",
    "4-2": "Missing Value",
    "5-0": "fdl.Metric.TYPE_VIOLATION",
    "5-1": "fdl.AlertType.DATA_INTEGRITY",
    "5-2": "Type Violation",
    "6-0": "fdl.Metric.RANGE_VIOLATION",
    "6-1": "fdl.AlertType.DATA_INTEGRITY",
    "6-2": "Range violation",
    "7-0": "fdl.Metric.TRAFFIC",
    "7-1": "fdl.AlertType.SERVICE_METRICS",
    "7-2": "Traffic Count",
    "8-0": "fdl.Metric.ACCURACY",
    "8-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION,  \nfdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "8-2": "Accuracy",
    "9-0": "fdl.Metric.RECALL",
    "9-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "9-2": "Recall",
    "10-0": "fdl.Metric.FPR",
    "10-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "10-2": "False Positive Rate",
    "11-0": " fdl.Metric.PRECISION",
    "11-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "11-2": "Precision",
    "12-0": "fdl.Metric.TPR",
    "12-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "12-2": "True Positive Rate",
    "13-0": "fdl.Metric.AUC",
    "13-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "13-2": "Area under the ROC Curve",
    "14-0": "fdl.Metric.F1_SCORE",
    "14-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "14-2": "F1 score",
    "15-0": "fdl.Metric.ECE",
    "15-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "15-2": "Expected Calibration Error",
    "16-0": "fdl.Metric.R2",
    "16-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "16-2": "R Squared",
    "17-0": "fdl.Metric.MSE",
    "17-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "17-2": "Mean squared error",
    "18-0": "fdl.Metric.MAPE",
    "18-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "18-2": "Mean Absolute Percentage Error",
    "19-0": "fdl.Metric.WMAPE",
    "19-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "19-2": "Weighted Mean Absolute Percentage Error",
    "20-0": "fdl.Metric.MAE",
    "20-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "20-2": "Mean Absolute Error",
    "21-0": "fdl.Metric.LOG_LOSS",
    "21-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "21-2": "Log Loss",
    "22-0": "fdl.Metric.MAP",
    "22-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "22-2": "Mean Average Precision",
    "23-0": "fdl.Metric.MEAN_NDCG",
    "23-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "23-2": "Normalized Discounted Cumulative Gain"
  },
  "cols": 3,
  "rows": 24,
  "align": [
    "left",
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
    metric = fdl.Metric.PRECISION, <----
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
```coffeescript Outputs
[AlertRule(alert_rule_uuid='9b8711fa-735e-4a72-977c-c4c8b16543ae',
           organization_name='some_org_name',
           project_id='project-a',
           model_id='binary_classification_model-a',
           name='perf-gt-5prec-1hr-1d-ago',
           alert_type=AlertType.PERFORMANCE,
           metric=Metric.PRECISION, <---
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