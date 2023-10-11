---
title: "Alerts with Fiddler UI"
slug: "alerts-ui"
hidden: false
createdAt: "2022-04-19T20:25:34.901Z"
updatedAt: "2023-10-06T17:36:36.545Z"
---
Fiddler allows you to set up [alerts](https://docs.fiddler.ai/v1.6/docs/alerts-platform) for your model. View your alerts by clicking on the Alerts tab in the navigation bar. The Alerts tab presents three views: Triggered Alerts, Alert Rules, and Integrations. Users can set up alerts using both the Fiddler UI and the Fiddler API Client. This page introduces the available alert types, and how to set up and view alerts in the Fiddler UI. For instructions about how to use the Fiddler API client for alert configuration see [Alert Configuration with Fiddler Client](doc:alerts-client).

![](https://files.readme.io/1730387-image.png)

## Setting up Alert Rules

To create a new alert using the Fiddler UI, click the **Add Alert** button on the top-right corner of any screen on the Alerts tab. 

![](https://files.readme.io/78537d3-image.png)

In the Alert Rule form, provide the basic information such as the desired alert name, and the project and model of interest. 

![](https://files.readme.io/8418e4f-image.png)

Next, select the Alert Type you would like to monitor. Users can select from Performance, Data Drift, Data Integrity, or Traffic monitors. For this example, we'll set up a Data Drift alert to measure distribution drift.

![](https://files.readme.io/d51ca30-image.png)

Once an Alert Type is selected, users can choose a metric corresponding to the Alert Type for which to set the alert on. For our Data Drift alert, we will use JSD (Jensen–Shannon distance) as our metric. The next consideration are the bin size, which is the duration for which fiddler monitoring calculates the metric values, and the column to apply this monitor on. Users can select up to 20 columns from the following column categories; Inputs, Outputs, Targets, Metadata, Decisions, and Custom Features. Let's choose a 1 hour bin and the CreditScore column for this example. 

![](https://files.readme.io/033e061-image.png)

Next, users can focus on the alerts comparison method. Learn more about Alert comparisons on the [Alerts Platform Guide](https://docs.fiddler.ai/v1.6/docs/alerts-platform). For our example we will select the Relative comparison option, and compare to the same time 7 days back. Users can select the alert condition as well as a Warning and Critical threshold. We will ask for an alert when the production data is greater than 10%.

![](https://files.readme.io/cb3f4b0-image.png)

Finally user can set the alert rules priority- how important this alert is to a customers work streams, along with how to get notified of triggered alerts. 

![](https://files.readme.io/0e75a9e-image.png)

 Last, click **Add Alert Rule** when you're done. In order to create and configure alerts using the Fiddler API client see [Alert Configuration with Fiddler Client](https://docs.fiddler.ai/v1.5/docs/fiddler-ui).

![](https://files.readme.io/72a1e8b-image.png)

### Alert Rules Tab

Once an alert rule is created it can be viewed in the **Alert Rules** tab. This view enables you to view all alert rules across any projects and model at a glance.

![](https://files.readme.io/ec2fde7-image.png)

A few high level details from the alert rule definition are displayed in the table, but users can select to view the full alert definition by selecting the overflow button (⋮) on the right-hand side of any Alert Rule record and clicking `View All Details`. 

![](https://files.readme.io/0e1dbdc-image.png)

Delete an existing alert by clicking on the overflow button (⋮) on the right-hand side of any Alert Rule record and clicking `Delete`. To make any other changes to an Alert Rule, you will need to delete the alert and create a new one with the desired specifications. 

![](https://files.readme.io/eddf05e-image.png)

## Visualizations

Throughout the Alert Rules, Triggered Alerts, and Home pages users will see references to the monitors they set up. These visualizations include Alert Rule priority, threshold severities, and more.

### Alert Rule Priority

Alert rule priority allows users to specify how important an alert rule is to their workflows, learn more on the [Alerts Platform Guide](https://docs.fiddler.ai/v1.6/docs/alerts-platform).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/4f87100-image.png",
        null,
        ""
      ],
      "align": "center",
      "sizing": "300px"
    }
  ]
}
[/block]


### Threshold Severity

Users can specify Warning and Critical thresholds as additional customization on their monitors, learn more on the [Alerts Platform Guide](https://docs.fiddler.ai/v1.6/docs/alerts-platform).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/664e72e-image.png",
        null,
        ""
      ],
      "align": "center",
      "sizing": "300px"
    }
  ]
}
[/block]


### Alert Summary

On the Fiddler home page, users can get a summary glance of their triggered alerts, categorized by Alert Type. This view allows users to easily navigate to their degraded models.

![](https://files.readme.io/3f76938-image.png)

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

[block:html]
{
  "html": "<div class=\"fiddler-cta\">\n<a class=\"fiddler-cta-link\" href=\"https://www.fiddler.ai/trial?utm_source=fiddler_docs&utm_medium=referral\"><img src=\"https://files.readme.io/af83f1a-fiddler-docs-cta-trial.png\" alt=\"Fiddler Free Trial\"></a>\n</div>"
}
[/block]