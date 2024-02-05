---
title: "Monitoring with Statistics"
slug: "statistics"
excerpt: ""
hidden: false
createdAt: "Thu Oct 05 2023 13:28:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Wed Dec 20 2023 17:18:45 GMT+0000 (Coordinated Universal Time)"
---
Fiddler supports some simple statistic metrics which can be used to monitor basic aggregations over Columns.

These can be particularly useful when you have a custom metadata field which you would like to monitor over time in addition to Fiddler's other out-of-the-box metrics.

Specifically, we support

- Average (takes the arithmetic mean of a numeric column)
- Sum (calculates the sum of a numeric column)
- Frequency (shows the count of occurrences for each value in a categorical or boolean column)

These metrics can be accessed in Charts and Alerts by selecting the Statistic Metric Type.

**Monitoring a Statistic Metric in Charts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/453a99d-Screen_Shot_2023-10-26_at_1.37.08_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


**Creating an Alert on a Statistic Metric:**

Alert rules can be established based on statistics too.  Like an alert rule, these can be setup using the Fiddler UI, the Fiddler python client or using Fiddler's REST-ful API.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/2b19cf0-Screen_Shot_2023-12-19_at_2.31.43_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]
