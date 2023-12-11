---
title: "Statistics"
slug: "statistics"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Thu Oct 05 2023 13:28:07 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 26 2023 17:37:44 GMT+0000 (Coordinated Universal Time)"
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

> 🚧 Frequency Metric Alerting
> 
> Currently, alerts cannot be set on the Frequency Metric. Support for this will be added in a future release.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b4a284a-Screen_Shot_2023-10-05_at_9.36.51_AM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]