---
title: "Release 23.7 Notes"
slug: "release-237-notes"
type: ""
createdAt: {}
hidden: false
---
This page enumerates the new features and updates in Release 23.7 of the Fiddler platform.

## Release of Fiddler platform version 23.7:

- Support for multi-target models

- Support for alert rule creation on the statistics frequency metric

## What's New and Improved:

- **Custom Target Support in Custom Metrics**
  - Custom Metrics now supports the ability to specify which column to use as the target for all built-in performance metrics
  - Custom Metrics now support functions for identifying True Positives, True Negatives, False Positives, and False Negatives for both binary classification and multi-class classification model tasks.
  - See [Custom Metrics](doc:custom-metrics) for more information
- **Alert Rules on Frequency**
  - Support for alert rules on `Frequency` statistics metrics
  - See [Statistics Guide](doc:statistics) for more information

### Client Version

Client version 2.3+ is required for the updates and features mentioned in this release.