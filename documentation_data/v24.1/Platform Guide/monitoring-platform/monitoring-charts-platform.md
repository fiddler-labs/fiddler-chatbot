---
title: "Monitoring Charts"
slug: "monitoring-charts-platform"
excerpt: ""
hidden: false
createdAt: "Thu Feb 23 2023 22:56:27 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
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

You can [plot up to 20 columns](doc:monitoring-charts-ui#chart-metric-queries--filters) and 6 metric queries for a model enabling you to easily perform model-to-model comparisons and plot multiple metrics in a single chart view.

### Downloadable CSV Data

You can [easily download a CSV of the raw chart data](doc:monitoring-charts-ui#breakdown-summary). This feature allows you to analyze your data further.

### Advanced Chart Functionality

The monitoring charts feature offers [advanced chart functionalities ](doc:monitoring-charts-ui#chart-metric-queries--filters)  to provide you with the flexibility to customize your charts and view your data in a way that is most useful to you. Features include:

- Zoom
- Dragging of time ranges
- Toggling between bar and line chart types
- Adjusting the scale between linear and log options
- Adjusting the range of the y-axis

![](https://files.readme.io/9ad4867-image.png)

Check out more on the [Monitoring Charts UI Guide](doc:monitoring-charts-ui).
