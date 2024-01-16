---
title: "fdl.Metric"
slug: "fdlmetric"
excerpt: "Supported Metric for different Alert Types in Alert Rules"
hidden: false
createdAt: "Tue Jan 31 2023 07:32:12 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Dec 19 2023 21:20:06 GMT+0000 (Coordinated Universal Time)"
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
    "2-0": "fdl.Metric.FREQUENCY",
    "2-1": "fdl.AlertType.STATISTIC",
    "2-2": "Frequency count of a specific value in a categorical column",
    "3-0": "fdl.Metric.PSI",
    "3-1": "fdl.AlertType.DATA_DRIFT",
    "3-2": "Population Stability Index",
    "4-0": "fdl.Metric.JSD",
    "4-1": "fdl.AlertType.DATA_DRIFT",
    "4-2": "Jensen–Shannon divergence",
    "5-0": "fdl.Metric.MISSING_VALUE",
    "5-1": "fdl.AlertType.DATA_INTEGRITY",
    "5-2": "Missing Value",
    "6-0": "fdl.Metric.TYPE_VIOLATION",
    "6-1": "fdl.AlertType.DATA_INTEGRITY",
    "6-2": "Type Violation",
    "7-0": "fdl.Metric.RANGE_VIOLATION",
    "7-1": "fdl.AlertType.DATA_INTEGRITY",
    "7-2": "Range violation",
    "8-0": "fdl.Metric.TRAFFIC",
    "8-1": "fdl.AlertType.SERVICE_METRICS",
    "8-2": "Traffic Count",
    "9-0": "fdl.Metric.ACCURACY",
    "9-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION,  \nfdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "9-2": "Accuracy",
    "10-0": "fdl.Metric.RECALL",
    "10-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "10-2": "Recall",
    "11-0": "fdl.Metric.FPR",
    "11-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "11-2": "False Positive Rate",
    "12-0": " fdl.Metric.PRECISION",
    "12-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "12-2": "Precision",
    "13-0": "fdl.Metric.TPR",
    "13-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "13-2": "True Positive Rate",
    "14-0": "fdl.Metric.AUC",
    "14-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "14-2": "Area under the ROC Curve",
    "15-0": "fdl.Metric.F1_SCORE",
    "15-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "15-2": "F1 score",
    "16-0": "fdl.Metric.ECE",
    "16-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "16-2": "Expected Calibration Error",
    "17-0": "fdl.Metric.R2",
    "17-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "17-2": "R Squared",
    "18-0": "fdl.Metric.MSE",
    "18-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "18-2": "Mean squared error",
    "19-0": "fdl.Metric.MAPE",
    "19-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "19-2": "Mean Absolute Percentage Error",
    "20-0": "fdl.Metric.WMAPE",
    "20-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "20-2": "Weighted Mean Absolute Percentage Error",
    "21-0": "fdl.Metric.MAE",
    "21-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "21-2": "Mean Absolute Error",
    "22-0": "fdl.Metric.LOG_LOSS",
    "22-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "22-2": "Log Loss",
    "23-0": "fdl.Metric.MAP",
    "23-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "23-2": "Mean Average Precision",
    "24-0": "fdl.Metric.MEAN_NDCG",
    "24-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "24-2": "Normalized Discounted Cumulative Gain"
  },
  "cols": 3,
  "rows": 25,
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
