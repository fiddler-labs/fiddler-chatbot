---
title: "Release 23.4 Notes"
slug: "release-234-notes"
type: ""
createdAt: {}
hidden: false
---
> 📘 **Version Numbering Update**
> 
> As of version 23.4, the documentation versioning will mirror the **platform release version numbers**, rather than the** client version numbers**.
> 
> Please refer to the bottom of the release notes for information on which client version is recommended for a given platform release.

## Release of Fiddler platform version 23.4:

- Support for custom features in Charts, Alerts, and Root Cause Analysis
- Ability to set alerts on multiple columns at once
- Support for webhook alert notifications
- Two new monitoring metrics for analyzing numeric columns (Average and Sum)
- Improved Python client usability

## What’s New and Improved:

- **Custom Features**
  - Custom features can plotted on Charts
  - Alerts can be set on Custom features
- **Alert Rules on Multiple Columns**
  - Streamlined the workflow by enabling users to designate alert rules for up to 20 specified columns
- **Webhook Alert Integration**
  - Webhook is available as a new destination for alert notifications. 
- **Statistic Metrics**
  - Adds a new Metric Type to Charts and Alerts, enabling two new Metrics:
    - Average (takes the average of a numeric Column)
    - Sum (takes the sum of a numeric Column)
  - Learn more on the page [Statistics](doc:statistics)
- **Python client 2.0**
  - Refactors the client structure for improved usability (see API documentation for detailed information)
  - Removed methods:
    - run_feature_importance
    - run_explanation
    - run_fairness
    - run_model
  - New methods:
    - [get_feature_importance](doc:clientget_feature_importance) 
    - [get_feature_impact](doc:clientget_feature_impact) 
    - [get_explanation](doc:clientget_explanation) 
    - [get_fairness](doc:clientget_fairness) 
    - [get_predictions](doc:clientget_predictions) 
  - Updated methods:
    - [get_mutual_information](doc:clientget_mutual_information) 
    - [add_alert_rule](doc:clientget_alert_rule) 
    - [get_alert_rules](doc:clientget_alert_rules) 

### Client Version

Client version 2.0 or above is required for the updates and features mentioned in the 23.4 release.