---
title: Segments
slug: segments
excerpt: Define ML segments to focus on problematic model cohorts
createdAt: Thu Jan 04 2024 20:06:12 GMT+0000 (Coordinated Universal Time)
updatedAt: Tue May 07 2024 20:18:58 GMT+0000 (Coordinated Universal Time)
---

# Segments

### Overview

A segment, sometimes referred to as a cohort or slice, represents a distinct subset of model values crucial for performance analysis and troubleshooting. Model segments can be defined using various model dimensions, such as specific time periods or sets of features. Analyzing segments proves invaluable for understanding or troubleshooting specific cohorts of interest, particularly in tasks like bias detection, where overarching datasets might obscure statistical intricacies.

### How to Define a Segment

Fiddler makes it easy to define custom segments using either the Fiddler UI or the Fiddler Python client. Instructions for both approaches are covered in more detail below. In either case, Fiddler Segments are constructed using the [Fiddler Query Language (FQL)](fiddler-query-language.md).

You can use any of the constants, operators, and functions mentioned in the page linked above in a Segment definition.

However, every Segment definition must return **a boolean row-level expression**. In other words, each inference will either satisfy the segment expression and thus belong to the segment or it will not.

### Examples

Let us illustrate further by providing a few examples. A segment can be defined by:

* A condition on some column (e.g. `age > 50`)
* A condition on some combination of columns (e.g. `(age / max_age) < 1.0`)

For details on all supported functions, see the [Fiddler Query Language (FQL)](fiddler-query-language.md) page.

### Adding a Segment

To learn more about adding a Segment using the Python client, see [fdl.Segment.create()](../../Python\_Client\_3-x/api-methods-30.md#create-5)

```python
SEGMENT_NAME = 'YOUR_SEGMENT_NAME'
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

PROJECT = fdl.Project.from_name(name=PROJECT_NAME)
MODEL = fdl.Model.from_name(name=MODEL_NAME, project_id=PROJECT.id)

segment = fdl.Segment(
        name=SEGMENT_NAME,
        model_id=MODEL.id,
        definition="Age < 60", #Use Fiddler Query Language (FQL) to define your custom segments
        description='Users with Age under 60',
    ).create()
```

### Applied Segments

When using segments in the UI for Analytics or Monitoring Charts, applied segments offer a flexible way to define segments on the fly for exploratory analysis. These segments are not saved to the model by default but will persist locally if the chart they are applied to is saved.

At any time, an applied segment can be saved to the model. However, once a segment is saved to the model, it cannot be altered.

### Modifying Saved Segments

Since alerts can be set on Segments, making modifications to a Segment may introduce inconsistencies in alerts.

> 🚧 Therefore, **Saved segments cannot be modified once they are created**.

If you'd like to experiment with a new segment, you can create one with a different definition or use applied segments within charts.

{% include "../../.gitbook/includes/main-doc-footer.md" %}

