---
title: Statistics
slug: statistics
excerpt: ''
createdAt: Thu Oct 05 2023 13:28:07 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 21:10:50 GMT+0000 (Coordinated Universal Time)
---

# Statistics

### Overview

Fiddler supports some simple statistic metrics which can be used to monitor basic aggregations over columns. These can be particularly useful when you have a custom metadata field which you would like to monitor over time in addition to Fiddler's other out-of-the-box metrics.

### What is being tracked?

Specifically, we support:

* **Average**: Takes the arithmetic mean of a numeric column
* **Sum**: Calculates the sum of a numeric column
* **Frequency**: Shows the count of occurrences for each value in a categorical or boolean column

### Monitoring Statistic Metrics

#### Charting Statistic Metrics

These metrics can be accessed in Charts and Alerts by selecting the Statistic Metric Type.

![](../../.gitbook/assets/453a99d-Screen\_Shot\_2023-10-26\_at\_1.37.08\_PM.png)

#### Alerting on Statistic Metrics

Alert rules can be established based on statistics too. Like an alert rule, these can be setup using the Fiddler UI, the Fiddler python client or using Fiddler's RESTful API.

![](../../.gitbook/assets/2b19cf0-Screen\_Shot\_2023-12-19\_at\_2.31.43\_PM.png)

{% include "../../.gitbook/includes/main-doc-footer.md" %}

