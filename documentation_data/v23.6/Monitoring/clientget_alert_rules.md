---
title: "client.get_alert_rules"
slug: "clientget_alert_rules"
excerpt: "To get a list of all alert rules for project, model, and other filtering parameters"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Nov 01 2022 06:38:59 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameters",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "Optional [str]",
    "0-2": "None",
    "0-3": "A unique identifier for the project.",
    "1-0": "model_id",
    "1-1": "Optional [str]",
    "1-2": "None",
    "1-3": "A unique identifier for the model.",
    "2-0": "alert_type",
    "2-1": "Optional\\[[fdl.AlertType](ref:fdlalerttype)]",
    "2-2": "None",
    "2-3": "Alert type. One of:  `AlertType.PERFORMANCE`, `AlertType.DATA_DRIFT`, `AlertType.DATA_INTEGRITY`, or `AlertType.SERVICE_METRICS`",
    "3-0": "metric",
    "3-1": "Optional\\[[fdl.Metric](ref:fdlmetric)]",
    "3-2": "None",
    "3-3": "When alert_type is SERVICE_METRICS:  `Metric.TRAFFIC`.  \n  \nWhen alert_type is PERFORMANCE, choose one of the following based on the machine learning model.  \n1)  For binary_classfication: One of  \n`Metric.ACCURACY`, `Metric.TPR`, `Metric.FPR`, `Metric.PRECISION`, `Metric.RECALL`, `Metric.F1_SCORE`, `Metric.ECE`, `Metric.AUC`  \n2) For Regression: One of  \n `Metric.R2`, `Metric.MSE`, `Metric.MAE`, `Metric.MAPE`, `Metric.WMAPE`  \n3)  For Multi-class:  \n`Metric.ACCURACY`, `Metric.LOG_LOSS`  \n4) For Ranking:  \n`Metric.MAP`, `Metric.MEAN_NDCG`  \n  \nWhen alert_type is DRIFT:  \n`Metric.PSI` or `Metric.JSD`  \n  \nWhen alert_type is DATA_INTEGRITY:  \nOne of  \n`Metric.RANGE_VIOLATION`,  \n`Metric.MISSING_VALUE`,  \n`Metric.TYPE_VIOLATION`",
    "4-0": "columns",
    "4-1": "Optional\\[List[str]]",
    "4-2": "None",
    "4-3": " [Optional] List of column names on which alert rule was created. Please note, Alert Rule matching any columns from this list will be returned. ",
    "5-0": "offset",
    "5-1": "Optional[int]",
    "5-2": "None",
    "5-3": "Pointer to the starting of the page index",
    "6-0": "limit",
    "6-1": "Optional[int]",
    "6-2": "None",
    "6-3": "Number of records to be retrieved per page, also referred as page_size",
    "7-0": "ordering",
    "7-1": "Optional\\[List[str]]",
    "7-2": "None",
    "7-3": "List of Alert Rule fields to order by. Eg. [‘critical_threshold’] or [‘- critical_threshold’] for descending order."
  },
  "cols": 4,
  "rows": 8,
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
> The Fiddler client can be used to get a list of alert rules with respect to the filtering parameters.

```python Usage

import fiddler as fdl

alert_rules = client.get_alert_rules(
    project_id = 'project-a',
    model_id = 'model-a', 
    alert_type = fdl.AlertType.DATA_INTEGRITY, 
    metric = fdl.Metric.MISSING_VALUE,
    columns = ["age", "gender"], 
    ordering = ['critical_threshold'], #['-critical_threshold'] for descending
    limit= 4, ## to set number of rules to show in one go
    offset = 0, # page offset (multiple of limit)
)
```

| Return Type     | Description                                                |
| :-------------- | :--------------------------------------------------------- |
| List[AlertRule] | A List containing AlertRule objects returned by the query. |