---
title: Custom Metrics
slug: custom-metrics
excerpt: Define ML monitoring metrics tailored to meet your needs
---

# Custom Metrics

### Overview

Custom metrics offer the capability to define metrics that align precisely with your machine learning requirements. Whether it's tracking business KPIs, crafting specialized performance assessments, or computing weighted averages, custom metrics empower you to tailor measurements to your specific needs. Seamlessly integrate these custom metrics throughout Fiddler, leveraging them in dashboards, alerting, and performance tracking.

Create user-defined metrics by employing a simple query language we call [Fiddler Query Language (FQL)](fiddler-query-language.md). FQL enables you to leverage your model's features, metadata, predictions, and outcomes for new data fields using a rich array of aggregations, operators, and metric functions, thereby expanding the depth of your analytical insights.

### How to Define a Custom Metric

Build custom metrics effortlessly with Fiddler's intuitive Excel-formula-like syntax. 
Once a custom metric is defined, Fiddler distinguishes itself by seamlessly managing time granularity and ranges within the charting, dashboarding, and analytics experience. 
This empowers you to effortlessly adjust time range and granularity without the need to modify your query, ensuring a smooth and efficient analytical experience.

Fiddler Custom Metrics are constructed using the [Fiddler Query Language (FQL)](fiddler-query-language.md).

> 📘 Custom metrics must return either:
>
> * an aggregate (produced by aggregate functions or built-in metric functions)
> * a combination of aggregates

### Examples

#### Simple Metric

Given this example use case:

> If an event is a false negative, assign a value of -40. If the event is a false positive, assign a value of -400. If the event is a true positive or true negative, then assign a value of 250.

Create a new Custom Metric with the following FQL formula:

```python
average(if(fn(), -40, if(fp(), -400, 250)))
```

Fiddler offers many convenience functions such as `fp()` and `fn()`.\
Alternatively, we could also identify false positives and false negatives the old fashioned way.

```python
average(if(Prediction < 0.5 and Target == 1, -40, if(Prediction >= 0.5 and Target == 0, -400, 250)))
```

Here, we assume `Prediction` is the name of the output column for a binary classifier and `Target` is the name of our label column

#### Tweedie Loss

In our next example, we provide an example implementation of the Tweedie Loss Function. Here, `Target` is the name of the target column and `Prediction` is the name of the prediction/output column.

```python
average((Target \* Prediction ^ (1 - 0.5)) / (1 - 0.5) + Prediction ^ (2 - 0.5) / (2 - 0.5))
```

### Adding a Custom Metric

To learn more about adding a Custom Metric using the Python client, see [fdl.CustomMetric](../../Python\_Client\_3-x/api-methods-30.md#custommetric):

```python
METRIC_NAME = 'YOUR_CUSTOM_METRIC_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

PROJECT = fdl.Project.from_name(name=PROJECT_NAME)
MODEL = fdl.Model.from_name(name=MODEL_NAME, project_id=PROJECT.id)

METRIC = fdl.CustomMetric(
        name=METRIC_NAME,
        model_id=MODEL.id,
        definition="average(if(\"spend_amount\">1000, \"spend_amount\", 0))", #Use Fiddler Query Language (FQL) to define your custom metrics
        description='Get average spend for users spending over $1000',
    ).create()
```

### Modifying Custom Metrics

Since alerts can be set on Custom Metrics, making modifications to a metric may introduce inconsistencies in alerts.

> 🚧 Therefore, custom metrics cannot be modified once they are created.

If you'd like to try out a new metric, you can create a new one with a different name and definition.

{% include "../../.gitbook/includes/main-doc-footer.md" %}

