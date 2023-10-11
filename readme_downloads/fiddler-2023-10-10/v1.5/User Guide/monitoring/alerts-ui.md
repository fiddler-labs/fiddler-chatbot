---
title: "Alerts with Fiddler UI"
slug: "alerts-ui"
hidden: false
createdAt: "2022-04-19T20:25:34.901Z"
updatedAt: "2022-10-26T17:07:10.204Z"
---
Fiddler allows you to set up alerts for your model. View your alerts by clicking on the Alerts tab in the navigation bar. The Alerts tab presents three different views, Triggered Alerts, Alert Rules, and Integrations. Users can set up alerts using both the Fiddler UI and the Fiddler API Client. This page introduces the available alert types, and how to set up and view alerts in the Fiddler UI. For instructions about how to use the Fiddler API client for alert configuration see [Alert Configuration with Fiddler Client](https://docs.fiddler.ai/v1.5/docs/fiddler-ui).

![](https://files.readme.io/1730387-image.png)

## Alert Rule Overview

### Supported Metric Types

You can get alerts for the following metrics:

- [**Data Drift**](doc:data-drift)  — Predictions and all features
  - Model performance can be poor if models trained on a specific dataset encounter different data in production.
- [**Performance**](doc:performance) 
  - Model performance tells us how well a model is doing on its task. A poorly performing model can have significant business implications.
- [**Data Integrity**](doc:data-integrity)  — All features
  - There are three types of violations that can occur at model inference: missing feature values, type mismatches (e.g. sending a float input for a categorical feature type) or range mismatches (e.g. sending an unknown US State for a State categorical feature).
- [**Service Metrics**](doc:service-metrics) 
  - The volume of traffic received by the model over time that informs us of the overall system health.

### Supported Comparison Types

You have two options for deciding when to be alerted:

1. **Absolute** — Compare the metric to an absolute value
   1. e.g. if traffic for a given hour is less than 1000, then alert.
2. **Relative** — Compare the metric to a previous time period
   1. e.g. if traffic is down 10% or more than it was at the same time one week ago, then alert.

You can set the alert threshold in either case.

### Alert Rule Priority

Whether you're setting up an alert rule to keep tabs on a model in a test environment, or data for production scenarios, Fiddler has you covered. Easily set the Alert Rule Priority to indicate the importance of any given Alert Rule. Users can select from the following priority options:

![](https://files.readme.io/8bfe6b3-image.png)

### Severity

For additional flexibility, users can now specify up to two threshold values, **Critical** and **Warning** severities. Critical severity is always required when setting up an Alert Rule, but Warning can be optionally set as well. 

![](https://files.readme.io/7cc863a-image.png)

The different severities will dictate the icon shown in the Triggered Alerts tab as well as the alert donut charts on the Homepage.

![](https://files.readme.io/7034940-image.png)

## Why do we need alerts?

- It’s not possible to manually track all metrics 24/7.
- Sensible alerts are your first line of defense, and they are meant to warn about issues in production.

## What should I do when I receive an alert?

- Click on the link in the email to go to the tab where the alert originated (e.g. Data Drift). 
- Under the Monitoring tab, more information can be obtained from the drill down below the main chart.
- You can also examine the data in the Analyze tab. You can use SQL to slice and dice the data, and use custom visualization tools and operators to make sense of the model’s behavior within the time range under consideration.

## Setting up Alert Rules

Alerts can be created both in the Fiddler UI and using the Fiddler client. To create a new alert using the Fiddler UI, click the **Add Alert** button on the top-right corner of any screen on the Alerts tab. Then fill out the Alert Rule form, and click **Add Alert Rule** when you're done. In order to create and configure alerts using the Fiddler API client see [Alert Configuration with Fiddler Client](https://docs.fiddler.ai/v1.5/docs/fiddler-ui).

![](https://files.readme.io/72a1e8b-image.png)

### Alert Rules

Once an alert rule is created it can be viewed in the **Alert Rules** tab. This view enables you to view all alert rules across any projects and model at a glance.

![](https://files.readme.io/ec2fde7-image.png)

A few high level details from the alert rule definition are displayed in the table, but users can select to view the full alert definition by selecting the overflow button (⋮) on the right-hand side of any Alert Rule record and clicking `View All Details`. 

![](https://files.readme.io/0e1dbdc-image.png)

Delete an existing alert by clicking on the overflow button (⋮) on the right-hand side of any Alert Rule record and clicking `Delete`. To make any other changes to an Alert Rule, you will need to delete the alert and create a new one with the desired specifications. 

![](https://files.readme.io/eddf05e-image.png)

## View Triggered Alerts on Fiddler

The Triggered Alerts view gives a single pane of glass experience where you can view all triggered alerts across any Project and Model. Easily apply time filters to see alerts that fired in a desired range, or customize the table to only show columns that matter the most to you. This view aggregates all triggered alerts by alert rule, where the number of times a given alert rule has been triggered is called out by the `Count` column. Explore the triggered alerts further by clicking on the `Monitor` button to further diagnose your model and data.

![](https://files.readme.io/30a5ab5-Screen_Shot_2022-10-03_at_3.39.32_PM.png)

## Sample Alert Email

Here's a sample of an email that's sent if an alert is triggered:

![](https://files.readme.io/9dfc566-Monitor_Alert_Email_0710.png "Monitor_Alert_Email_0710.png")

## Integrations

The Integrations tab is a read-only view of all the integrations your Admin has enabled for use. As of today, users can configure their Alert Rules to notify them via email or Pager Duty services.

![](https://files.readme.io/7462149-image.png)

Admins can add new integrations by clicking on the setting cog icon in the main navigation bar and selecting the integration tab of interest.

![](https://files.readme.io/6ee3027-Screen_Shot_2022-10-03_at_4.16.00_PM.png)

**Reference**

- See our article on [_The Rise of MLOps Monitoring_](https://www.fiddler.ai/blog/the-rise-of-mlops-monitoring)
- Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions