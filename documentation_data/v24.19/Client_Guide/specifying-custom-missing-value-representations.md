---
title: Specifying Custom Missing Value Representations
slug: specifying-custom-missing-value-representations
excerpt: ''
createdAt: Tue Aug 30 2022 18:19:30 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 22 2024 18:41:20 GMT+0000 (Coordinated Universal Time)
---

# Specifying Custom Missing Value Representations

There may be cases where your data contains missing values, but they are represented in a nonstandard way (other than `null` or `NaN`). As an example, suppose an upstream system uses "-1.0" or "-999" in place of `null` for a particular Float column. Fiddler offers a method to specify **your own missing value representations for each column** when defining your model schema. See below for an example.

***

You can modify your `fdl.ModelSchema` object just before onboarding your model to include details about which values should be replaced with nulls when publishing data to Fiddler.

```python
model.schema['my_column'].replace_with_nulls = [
  '-1.0',
  '-999'
]
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

