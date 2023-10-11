---
title: "fdl.Metric"
slug: "fdlmetric"
excerpt: "Supported Metric for different Alert Types in Alert Rules"
hidden: false
createdAt: "2023-01-31T07:32:12.906Z"
updatedAt: "2023-02-03T03:25:53.558Z"
---
**Following is the list of metrics, with corresponding alert type and model task, for which an alert rule can be created.**

[block:parameters]
{
  "data": {
    "h-0": "Enum Values",
    "h-1": "Supported for [Alert Types](https://docs.fiddler.ai/v1.5/reference/fdlalerttype)  \n([ModelTask ](https://docs.fiddler.ai/v1.5/reference/fdlmodeltask)restriction if any)",
    "h-2": "Description",
    "0-0": "fdl.Metric.PSI",
    "0-1": "fdl.AlertType.DATA_DRIFT",
    "0-2": "Population Stability Index",
    "1-0": "fdl.Metric.JSD",
    "1-1": "fdl.AlertType.DATA_DRIFT",
    "1-2": "Jensen–Shannon divergence",
    "2-0": "fdl.Metric.MISSING_VALUE",
    "2-1": "fdl.AlertType.DATA_INTEGRITY",
    "2-2": "Missing Value",
    "3-0": "fdl.Metric.TYPE_VIOLATION",
    "3-1": "fdl.AlertType.DATA_INTEGRITY",
    "3-2": "Type Violation",
    "4-0": "fdl.Metric.RANGE_VIOLATION",
    "4-1": "fdl.AlertType.DATA_INTEGRITY",
    "4-2": "Range violation",
    "5-0": "fdl.Metric.TRAFFIC",
    "5-1": "fdl.AlertType.SERVICE_METRICS",
    "5-2": "Traffic Count",
    "6-0": "fdl.Metric.ACCURACY",
    "6-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION,  \nfdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "6-2": "Accuracy",
    "7-0": "fdl.Metric.RECALL",
    "7-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "7-2": "Recall",
    "8-0": "fdl.Metric.FPR",
    "8-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "8-2": "False Positive Rate",
    "9-0": " fdl.Metric.PRECISION",
    "9-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "9-2": "Precision",
    "10-0": "fdl.Metric.TPR",
    "10-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "10-2": "True Positive Rate",
    "11-0": "fdl.Metric.AUC",
    "11-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "11-2": "Area under the ROC Curve",
    "12-0": "fdl.Metric.F1_SCORE",
    "12-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "12-2": "F1 score",
    "13-0": "fdl.Metric.ECE",
    "13-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.BINARY_CLASSIFICATION)",
    "13-2": "Expected Calibration Error",
    "14-0": "fdl.Metric.R2",
    "14-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "14-2": "R Squared",
    "15-0": "fdl.Metric.MSE",
    "15-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "15-2": "Mean squared error",
    "16-0": "fdl.Metric.MAPE",
    "16-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "16-2": "Mean Absolute Percentage Error",
    "17-0": "fdl.Metric.WMAPE",
    "17-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "17-2": "Weighted Mean Absolute Percentage Error",
    "18-0": "fdl.Metric.MAE",
    "18-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.REGRESSION)",
    "18-2": "Mean Absolute Error",
    "19-0": "fdl.Metric.LOG_LOSS",
    "19-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.MULTICLASS_CLASSIFICATION)",
    "19-2": "Log Loss",
    "20-0": "fdl.Metric.MAP",
    "20-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "20-2": "Mean Average Precision",
    "21-0": "fdl.Metric.MEAN_NDCG",
    "21-1": "fdl.AlertType.PERFORMANCE  \n(fdl.ModelTask.RANKING)",
    "21-2": "Normalized Discounted Cumulative Gain"
  },
  "cols": 3,
  "rows": 22,
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