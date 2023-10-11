---
title: "Monitoring Charts"
slug: "monitoring-charts-platform"
hidden: false
createdAt: "2023-02-23T22:56:27.756Z"
updatedAt: "2023-05-24T17:27:31.121Z"
---
Fiddler AI’s monitoring charts allow you to easily track your models and ensure that they are performing optimally. For any of your models, monitoring charts for data drift, performance, data integrity, or traffic metrics can be displayed using Fiddler Dashboards.

## Supported Metric Types

Monitoring charts enable you to plot one of the following metric types for a given model:

- [**Data Drift**](doc:data-drift-platform#what-is-being-tracked)
  - Plot drift for up to 20 columns at once and track it using your choice of Jensen–Shannon distance (JSD) or Population Stability Index (PSI).
- [**Performance**](doc:performance-tracking-platform#what-is-being-tracked)
  - Available metrics are model dependent.
- [**Data Integrity Violations**](doc:data-integrity-platform#what-is-being-tracked)
  - Plot data integrity violations for up to 20 columns and track one of the three violations at once.
- [**Traffic **](doc:traffic-platform#what-is-being-tracked)

## Key Features:

### Multiple Charting Options

You can [plot up to 20 columns](doc:monitoring-charts-ui#chart-metric-queries--filters) for a model when charting data drift or data integrity metrics, allowing you to compare them side by side.

### Downloadable CSV Data

You can [easily download a CSV of the raw chart data](doc:monitoring-charts-ui#breakdown-summary). This feature allows you to analyze your data further.

### Advanced Chart Functionality

The monitoring charts feature offers [advanced chart functionalities ](doc:monitoring-charts-ui#chart-metric-queries--filters)such as zoom, dragging of time ranges, toggling between bar and line chart types, and more. These features provide you with the flexibility to customize your charts and view your data in a way that is most useful to you.

![](https://files.readme.io/0a8fdbb-image.png)