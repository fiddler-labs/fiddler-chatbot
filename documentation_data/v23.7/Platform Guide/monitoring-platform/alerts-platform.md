---
title: "Alerts"
slug: "alerts-platform"
excerpt: ""
hidden: false
createdAt: "Fri Jan 27 2023 19:53:56 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Dec 08 2023 22:15:43 GMT+0000 (Coordinated Universal Time)"
---
Fiddler enables users to set up alert rules to track a model's health and performance over time. Fiddler alerts also enable users to dig into triggered alerts and perform root cause analysis to discover what is causing a model to degrade. Users can set up alerts using both the [Fiddler UI](doc:alerts-ui) and the [Fiddler API Client](doc:alerts-client).

## Supported Metric Types

You can get alerts for the following metrics:

- [**Data Drift**](doc:data-drift)  — Predictions and all features
  - Model performance can be poor if models trained on a specific dataset encounter different data in production.
- [**Performance**](doc:performance) 
  - Model performance tells us how well a model is doing on its task. A poorly performing model can have significant business implications.
- [**Data Integrity**](doc:data-integrity)  — All features
  - There are three types of violations that can occur at model inference: missing feature values, type mismatches (e.g. sending a float input for a categorical feature type) or range mismatches (e.g. sending an unknown US State for a State categorical feature).
- [**Service Metrics**](doc:traffic-platform) 
  - The volume of traffic received by the model over time that informs us of the overall system health.

## Supported Comparison Types

You have two options for deciding when to be alerted:

1. **Absolute** — Compare the metric to an absolute value
   1. e.g. if traffic for a given hour is less than 1000, then alert.
2. **Relative** — Compare the metric to a previous time period
   1. e.g. if traffic is down 10% or more than it was at the same time one week ago, then alert.

You can set the alert threshold in either case.

## Alert Rule Priority

Whether you're setting up an alert rule to keep tabs on a model in a test environment, or data for production scenarios, Fiddler has you covered. Easily set the Alert Rule Priority to indicate the importance of any given Alert Rule. Users can select from Low, Medium, and High priorities. 

## Alert Rule Severity

For additional flexibility, users can now specify up to two threshold values, **Critical** and **Warning** severities. Critical severity is always required when setting up an Alert Rule, but Warning can be optionally set as well.

## Why do we need alerts?

- It’s not possible to manually track all metrics 24/7.
- Sensible alerts are your first line of defense, and they are meant to warn about issues in production.

## What should I do when I receive an alert?

- Click on the link in the email to go to the tab where the alert originated (e.g. Data Drift). 
- Under the Monitoring tab, more information can be obtained from the drill down below the main chart.
- You can also examine the data in the Analyze tab. You can use SQL to slice and dice the data, and use custom visualization tools and operators to make sense of the model’s behavior within the time range under consideration.

## Sample Alert Email

Here's a sample of an email that's sent if an alert is triggered:

![](https://files.readme.io/9dfc566-Monitor_Alert_Email_0710.png "Monitor_Alert_Email_0710.png")

## Integrations

Fiddler supports the following alert notification integrations:

- Email
- Slack
- PagerDuty
