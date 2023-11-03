---
title: "Release 23.3 Notes"
slug: "release-233"
createdAt: "2023-08-15T18:03:45.797Z"
hidden: false
---
This page enumerates the new features and updates in Release 23.3 of the Fiddler platform.

> 📘 Platform Release Version 23.3 & Doc v1.8 compatability note
> 
> Note that the documentation version remains v1.8 with this release. The new and improved functionalities are added to their respective pages with the note regarding platform version 23.3 as a requirement.

## Release of Fiddler platform version 23.3:

- Support for added charting up to 6 metrics for one or multiple models 

- Ability to assign metrics to the left or right y-axis in monitoring charts

- Addition of automatically created model monitoring dashboards

- New Root Cause Analysis tab with data drift and data integrity information in monitoring charts 

## What's New and Improved:

- **Multiple metric queries in monitoring charts**
  - Flexibility to add up to 6 metrics queries to visualize multiple metrics or models in one chart.
  - Enables model-to-model comparison in a single chart.
  - Learn more on the [Monitoring Charts Platform Guide](doc:monitoring-charts-platform).

- **Y-axis assignment in monitoring charts**
  - Further, customize charts by assigning metric queries to a left or right y-axis in the customize tab.
  - Learn more on the [Monitoring Charts UI Guide](doc:monitoring-charts-ui).

- **Automatically generated model dashboards**
  - Fiddler will automatically create a model dashboard for all models added to the platform, consisting of charts that display data drift, performance, data integrity, and traffic information.
  - Learn more on the[Dashboards Platform Guide](doc:dashboards-platform).

- **Root cause analysis in monitoring charts**
  - Examine specific timestamps within a monitoring time series chart to reveal the underlying reasons for model underperformance, using visualizations of data drift and data integrity insights.
  - Learn more on the page  [Monitoring Charts UI Guide](doc:monitoring-charts-ui).

### Client Version

Client version 1.8 is required for the updates and features mentioned in this release.