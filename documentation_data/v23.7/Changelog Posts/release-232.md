---
title: "Release 23.2 Notes"
slug: "release-232"
type: ""
createdAt: {}
hidden: false
---
This page enumerates the new features and updates in Release 23.2 of the Fiddler platform.

## Release of Fiddler platform version 23.2:

- Support for uploading multiple baselines to a model

- Alert context overlay on the chart editor

- Ability to customize scale and range of y-axis on the chart editor

## What's New and Improved:

- **Support for uploading multiple baselines**
  - Flexibility to add baseline datasets or use production data as the baseline.
  - Perform comparisons amongst multiple baselines to understand how different baselines — data shifts due seasonality or geography for example — may influence model drift and model behavior.
  - Learn more on the [Baselines Platform Guide](doc:fiddler-baselines).

- **Alert context overlay on the chart editor**
  - For absolute alerts, alert context is an overlay on the chart area to easily identify critical and warning thresholds.
  - For relative alerts, Fiddler will automatically plot historic comparison data for additional context on why the alert fired.

- **Customization in the chart editor**
  - Further customize charts by toggling between logarithmic and linear scale, and manually setting the min and max values of the y-axis.
  - Learn more on the [Monitoring Charts](doc:monitoring-charts-ui) page.

### Client Version

Client version 1.8 is required for the updates and features mentioned in this release.