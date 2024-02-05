---
title: "Specifying Custom Missing Value Encodings"
slug: "specifying-custom-missing-value-encodings"
excerpt: ""
hidden: false
createdAt: "Tue Aug 30 2022 18:19:30 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
There may be cases in which you have missing values in your data, but you encode these values in a special way (other than the standard `NaN`).

In such cases, Fiddler offers a way to specify **your own missing value encodings for each column**.

***

You can create a "fall back" dictionary, which holds the values you would like to have treated as missing for each column. Then just pass that dictionary into your [`fdl.ModelInfo`](/reference/fdlmodelinfo)  object before onboarding your model.

```python
fall_back = {
  'column_1': [-999, 'missing'],
  'column_2': [-1, '?', 'na']
}

model_info = fdl.ModelInfo.from_dataset_info(
  ...
  fall_back=fall_back
)
```
