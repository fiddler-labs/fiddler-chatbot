---
title: "Segments"
slug: "segments"
excerpt: ""
hidden: false
createdAt: "Thu Jan 04 2024 20:06:12 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Jan 11 2024 21:59:28 GMT+0000 (Coordinated Universal Time)"
---
# Overview

Fiddler offers the ability to segment your data based on a custom condition.

# How do I construct a Segment?

Fiddler Segments are constructed using the [Fiddler Query Language (FQL)](doc:fiddler-query-language). 

You can use any of the constants, operators, and functions mentioned in the page linked above in a Segment definition.

However, every Segment definition must return **a boolean row-level expression**.

That can look like

- A condition on some column (e.g. `age > 50`)
- A condition on some combination of columns (e.g. `(age / max_age) < 1.0`)

For details on all supported functions, see the FQL page linked above.

# Adding a Segment

**Note:** To add a Segment using the Python client, see [client.add_segment](ref:clientadd_segment)

From the Model page, you can access Segments by clicking the **Segments** tab at the top of the page.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/477ef0b-Screen_Shot_2024-01-11_at_4.46.06_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Then click **Add Segment** to add a new Segment.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/76cbef9-Screen_Shot_2024-01-11_at_4.47.49_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


Finally, enter the Name, Description, and Definition for your Segment and click **Save**.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f2c930c-Screen_Shot_2024-01-11_at_4.49.07_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Accessing Segments in Charts and Alerts

After your Segment is saved, it can be selected from Charts and Alerts.

**Charts:**

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/738eafc-Screen_Shot_2024-01-11_at_4.56.13_PM.png",
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
        "https://files.readme.io/de253bd-Screen_Shot_2024-01-11_at_4.57.13_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


# Modifying Segments

Since alerts can be set on Segments, making modifications to a Segment may introduce inconsistencies in alerts.

Therefore, **Segments cannot be modified once they are created**.

If you'd like to try out a new Segment, you can create a new one with a different Definition.

# Deleting Segments

**Note:** To delete a Segment using the Python client, see [client.delete_segment](ref:clientdelete_segment)

From the Segments tab, you can delete a Segment by clicking the trash icon next to the Segment of interest.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/c8a2a35-Screen_Shot_2024-01-11_at_4.58.47_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]
