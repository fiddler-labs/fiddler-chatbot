---
title: "Custom Metrics"
slug: "custom-metrics"
excerpt: ""
hidden: false
createdAt: "Thu Oct 26 2023 16:21:43 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Nov 21 2023 17:18:12 GMT+0000 (Coordinated Universal Time)"
---
# Overview

Fiddler offers the ability to customize metrics for your specific use case.

# Language

Fiddler Custom Metrics are constructed using the [Fiddler Query Language (FQL)](doc:fiddler-query-language). 

# Adding a Custom Metric

**Note:** To add a Custom Metric using the Python client, see [client.add_custom_metric](ref:clientadd_custom_metric)

From the Model page, you can access Custom Metrics by clicking the **Custom Metrics** tab at the top of the page.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e0b5069-Screen_Shot_2023-11-20_at_1.49.03_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Then click **Add Custom Metric** to add a new Custom Metric.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f91ffdb-Screen_Shot_2023-11-20_at_1.51.09_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Finally, enter the Name, Description, and Definition for your Custom Metric and click **Save**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d1cc8f7-Screen_Shot_2023-11-20_at_1.52.40_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]




# Accessing Custom Metrics in Charts and Alerts

After your Custom Metric is saved, it can be selected from Charts and Alerts.

**Charts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8e3eade-Screen_Shot_2023-11-20_at_1.56.41_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


**Alerts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/1fae05c-Screen_Shot_2023-11-20_at_1.58.37_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]




# Modifying Custom Metrics

Since alerts can be set on Custom Metrics, making modifications to a metric may introduce inconsistencies in alerts.

Therefore, **Custom Metrics cannot be modified once they are created**.

If you'd like to try out a new metric, you can create a new one with a different Definition.



# Deleting Custom Metrics

**Note:** To delete a Custom Metric using the Python client, see [client.delete_custom_metric](ref:clientdelete_custom_metric)

From the Custom Metrics tab, you can delete a metric by clicking the trash icon next to the metric of interest.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f646c51-Screen_Shot_2023-11-21_at_12.16.34_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]