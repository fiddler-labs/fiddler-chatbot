---
title: Alerts with Fiddler UI
slug: alerts-with-fiddler-ui
excerpt: ''
createdAt: Wed Feb 07 2024 18:08:16 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 23:12:39 GMT+0000 (Coordinated Universal Time)
---

# Alerts With Fiddler UI

### Overview

Fiddler enables you to set up [alerts](../../product-guide/monitoring-platform/alerts-platform.md) for your model, accessible via the Alerts tab in the navigation bar. The Alerts tab provides views for Triggered Alerts, Alert Rules, and Integrations. You can configure alerts using the Fiddler UI or the [API Client](../../Client_Guide/alerts-with-fiddler-client.md). This page outlines available alert types and provides instructions for setting up and viewing alerts in the Fiddler UI.

![](../../.gitbook/assets/bd02ee8-image.png)

### Setting up Alert Rules

To create a new alert in the Fiddler UI, click Add Alert on the Alerts tab.

1. Fill in the Alert Rule form with basic details like alert name, project, and model.
2. Choose an Alert Type (Traffic, Data Drift, Data Integrity, Performance, Statistic, or Custom Metric) and set up specific metrics, bin size, and columns.
3. Define comparison methods, thresholds, and notification preferences. Click Add Alert Rule to finish.
   1. Learn more about Alert comparisons on the [Alerts Platform Guide](../../product-guide/monitoring-platform/alerts-platform.md).

![](../../.gitbook/assets/52064e5-image.png)

In order to create and configure alerts using the Fiddler API client see [Alert Configuration with Fiddler Client](../../Client_Guide/alerts-with-fiddler-client.md).

### Alert Notification options

You can select the following types of notifications for your alert.

![](../../.gitbook/assets/ee80b90-Screenshot_2023-10-09_at_5.18.21_PM.png)

### Delete an Alert Rule

Delete an existing alert by clicking on the overflow button (⋮) on the right-hand side of any Alert Rule record and clicking `Delete`. To make any other changes to an Alert Rule, you will need to delete the alert and create a new one with the desired specifications.

![](../../.gitbook/assets/eddf05e-image.png)

### Triggered Alert Revisions

Say goodbye to stale alerts! Triggered Alert Revisions mark a leap forward in alert intelligence, giving you the confidence to act decisively and optimize your operations.

Alerts now adapt to changing data. If new information emerges that alters an alert's severity or value, the alert automatically updates you with highlights in the user interface and revised notifications. This approach empowers you to:

* Make informed decisions based on real-time data: No more relying on outdated or inaccurate alerts.
* Focus on critical issues: Updated alerts prioritize the most relevant information.

![Inspect Alert experience](../../.gitbook/assets/5921286-Screenshot_2024-03-07_at_5.21.04_PM.png)

Inspect Alert experience

![Triggered Alert revision experience](../../.gitbook/assets/7f0aa27-Screenshot_2024-03-07_at_5.21.13_PM.png)

Triggered Alert revision experience

### Sample Alert Email

Here's a sample of an email that's sent if an alert is triggered:

![](../../.gitbook/assets/alert-email-perf-example.png)

### Integrations

The Integrations tab is a read-only view of all the integrations your Admin has enabled for use. As of today, users can configure their Alert Rules to notify them via email or Pager Duty services.

![](../../.gitbook/assets/7462149-image.png)

Admins can add new integrations by clicking on the setting cog icon in the main navigation bar and selecting the integration tab of interest.

![](../../.gitbook/assets/6ee3027-Screen_Shot_2022-10-03_at_4.16.00_PM.png)



### Pause alert notification

This feature allows users to temporarily pause and resume notifications for specific alerts without affecting their evaluation and triggering mechanisms. It enhances user experience by providing efficient notification management.\


#### How to Use

**Using the Fiddler User Interface (UI)**

* Locate the Alert Tool:\
  Navigate to the alert rule table and identify the desired alert.
* Toggle Notifications:
  * Click the notification bell icon.
  * The icon updates to indicate the new state (paused or resumed).
* Confirm Action:
  * A loading indicator and a toast notification confirm the action.

**Using the Fiddler Client API**

For programmatic control, use the Fiddler client API's alert-rules method with the enable\_notification argument.

* Details:\
  Refer to the [Fiddler documentation](../../API_Guidelines/alert-rules.md) for a complete explanation of API functionalities.

#### Note

* No Impact on Evaluation:\
  Pausing notifications does not affect the evaluation of alert conditions. The alert tool will continue assessing conditions and triggering alerts as usual.

{% include "../../.gitbook/includes/main-doc-footer.md" %}
