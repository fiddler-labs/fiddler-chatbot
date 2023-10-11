---
title: "Alerts"
slug: "alerts"
hidden: false
createdAt: "2022-04-19T20:25:34.901Z"
updatedAt: "2022-06-13T19:55:31.123Z"
---
Fiddler allows you to set up alerts for your model. View your alerts by clicking Alerts on the Monitor page.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/dacb859-Monitor_Alert_Dashboard_0709.png",
        "Monitor_Alert_Dashboard_0709.png",
        3208,
        1294,
        "#fafafb"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "What kinds of alerts are supported?"
}
[/block]
You can get alerts for the following metrics:

* [Data Drift](doc:data-drift)  — Predictions and all features
* [Performance](doc:performance) 
* [Data Integrity](doc:data-integrity)  — All features
* [Service Metrics](doc:service-metrics) 

You have two options for deciding when to be alerted:

1. Compare the metric to an absolute value (e.g. if traffic for a given hour is less than 1000, then alert).
2. Compare the metric to a previous time period (e.g. if traffic is down 10% or more than it was at the same time one week ago, then alert).

You can set the alert threshold in either case.
[block:api-header]
{
  "title": "Why do we need alerts?"
}
[/block]
* It’s not possible to manually track all metrics 24/7.
* Sensible alerts are your first line of defense, and they are meant to warn about issues in production.
[block:api-header]
{
  "title": "What should I do when I receive an alert?"
}
[/block]
* Click on the link in the email to go to the tab where the alert originated (e.g. Data Drift). 
* Under the Monitoring tab, more information can be obtained from the drill down below the main chart.
* You can also examine the data in the Analyze tab. You can use SQL to slice and dice the data, and use custom visualization tools and operators to make sense of the model’s behavior within the time range under consideration.
[block:api-header]
{
  "title": "Setting up Alerts"
}
[/block]
Create a new alert by clicking the **Add Alert** button on the top-right corner of the Monitor page. Configure the alert, and click **Save** when you're done.

![Create_New_Alert](../../../../assets/page-content/png/Monitor_Alert_New_0709.png "Create New Alert")
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/5dea9bf-Monitor_Alert_New_0709.png",
        "Monitor_Alert_New_0709.png",
        756,
        1093,
        "#f7f8fa"
      ]
    }
  ]
}
[/block]
Once an alert is set, it can be viewed under the **Alerts** tab of the Monitor page.

Delete an existing alert by clicking on the three dots under the Actions column. You can only edit the email for an alert; to make any other changes, you need to delete the alert and create a new one.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/3d0595f-Monitor_Alert_Edit_Delete_0710.png",
        "Monitor_Alert_Edit_Delete_0710.png",
        288,
        209,
        "#f5f7fb"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Sample Alert Email"
}
[/block]
Here's a sample of an email that's sent if an alert is triggered:

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/9dfc566-Monitor_Alert_Email_0710.png",
        "Monitor_Alert_Email_0710.png",
        796,
        1354,
        "#d1d5e6"
      ]
    }
  ]
}
[/block]
**Reference**

* See our article on [_The Rise of MLOps Monitoring_](https://blog.fiddler.ai/2020/09/the-rise-of-mlops-monitoring/)

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*