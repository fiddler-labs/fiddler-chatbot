---
title: "Statistics"
slug: "statistics"
hidden: false
createdAt: "2023-10-05T13:28:07.850Z"
updatedAt: "2023-10-06T19:23:39.976Z"
---
Fiddler supports some simple statistic metrics which can be used to monitor basic aggregations over Columns.

These can be particularly useful when you have a custom metadata field which you would like to monitor over time in addition to Fiddler's other out-of-the-box metrics.

Specifically, we support

- Average (takes the arithmetic mean of a numeric column)
- Sum (calculates the sum of a numeric column)

These metrics can be accessed in Charts and Alerts by selecting the Statistic Metric Type.

**Monitoring a Statistic Metric in Charts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/abb7ca4-Screen_Shot_2023-10-05_at_9.35.39_AM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]




**Creating an Alert on a Statistic Metric:**

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