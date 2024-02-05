---
title: "Custom Metrics"
slug: "custom-metrics"
excerpt: ""
hidden: false
createdAt: "Thu Oct 26 2023 16:21:43 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Jan 10 2024 17:57:09 GMT+0000 (Coordinated Universal Time)"
---
# Overview

Fiddler offers the ability to customize metrics for your specific use case.

# How do I construct a Custom Metric?

Fiddler Custom Metrics are constructed using the [Fiddler Query Language (FQL)](doc:fiddler-query-language). 

You can use any of the constants, operators, and functions mentioned in the page linked above in a Custom Metric definition.

However, every metric must return either

1. an aggregate (produced by aggregate functions and built-in metric functions) or
2. a combination of aggregates

To clarify, you may not define a metric using purely row-level functions.

For details on all these function types, see the FQL page linked above.

# Examples

## Simple Example

Let’s say you wanted to create a Custom Metric for the following metric definition:

- If an event is a false negative, assign a value of -40. If the event is a false positive, assign a value of -400.  If the event is a true positive or true negative, then assign a value of 250.

We can formulate this metric using FQL with the following code:

`average(if(Prediction < 0.5 and Target == 1, -40, if(Prediction >= 0.5 and Target == 0, -400, 250)))`

(Here, we assume `Prediction` is the name of the output column for a binary classifier and `Target` is the name of our label column.)

## Null Violation Flag

This metric returns `1` if a given time bin has at least one null value in the `column1` column. Otherwise, it returns `0`.

`if(null_violation_count(column1) > 0, 1, 0)`

## Tweedie Loss

An implementation of the Tweedie Loss Function. Here, `Target` is the name of the target column and `Prediction` is the name of the prediction/output column.

`average((Target * Prediction ^ (1 - 0.5)) / (1 - 0.5) + Prediction ^ (2 - 0.5) / (2 - 0.5))`

# Adding a Custom Metric

**Note:** To add a Custom Metric using the Python client, see [client.add_custom_metric](ref:clientadd_custom_metric)

From the Model page, you can access Custom Metrics by clicking the **Custom Metrics** tab at the top of the page.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e0b5069-Screen_Shot_2023-11-20_at_1.49.03_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Then click **Add Custom Metric** to add a new Custom Metric.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f91ffdb-Screen_Shot_2023-11-20_at_1.51.09_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Finally, enter the Name, Description, and Definition for your Custom Metric and click **Save**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d1cc8f7-Screen_Shot_2023-11-20_at_1.52.40_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Accessing Custom Metrics in Charts and Alerts

After your Custom Metric is saved, it can be selected from Charts and Alerts.

**Charts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0563507-Screen_Shot_2023-12-18_at_1.23.49_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


**Alerts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8ae37f9-Screen_Shot_2023-12-18_at_1.26.27_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Modifying Custom Metrics

Since alerts can be set on Custom Metrics, making modifications to a metric may introduce inconsistencies in alerts.

Therefore, **Custom Metrics cannot be modified once they are created**.

If you'd like to try out a new metric, you can create a new one with a different Definition.

# Deleting Custom Metrics

**Note:** To delete a Custom Metric using the Python client, see [client.delete_custom_metric](ref:clientdelete_custom_metric)

From the Custom Metrics tab, you can delete a metric by clicking the trash icon next to the metric of interest.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f646c51-Screen_Shot_2023-11-21_at_12.16.34_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]
