---
Title: Events Table Examples in RCA
slug: events-table-in-rca
excerpt: ''
hidden: false
---

# Events Table in RCA

Allow visualizing events corresponding to a certain bin in a monitoring chart. Note that this view is to provide example rows used for the computation. The maximum number of rows that can viewed is 1000.

## Analyzing a sample of events

* Navigate to the `Charts` tab in your Fiddler AI instance
* Click on the `Add Chart` button on the top right
* In the modal, select a project
* Select **Monitoring**
* Create a Monitoring chart and click on a time range
* This will display the RCA (Root Cause Analysis) tab
* In RCA, select the `Events Table` tab

## Support

This visualization is supported for any model and data type.

## Represented data

The displayed events are production events coming from the selected model and bin, and segment if it was selected in the monitoring chart.

![Monitoring Chart Configuration](../../.gitbook/assets/monitoring-chart-selection.png) ![Event Table Example](../../.gitbook/assets/data-table-rca-example.png)

## Available Controls

* **Column selection**: On the top right side of the table, select the columns to be displayed. By default all non-vector columns are displayed.

![Event Table Column Selection](../../.gitbook/assets/data-table-column-selection.png)

* **Vector columns**: By default the vector columns are not fetched for latency reasons. Toggle on if vectors need to be fetched.

![Event Table Vectors displayed](../../.gitbook/assets/data-table-vectors.png)

* **Download**: Download the sample events to `CSV` or `PARQUET` format.

![Event Table Vectors Download](../../.gitbook/assets/data-table-download.png)

{% include "../../.gitbook/includes/main-doc-footer.md" %}

