---
title: "Specifying Custom Missing Value Encodings"
slug: "specifying-custom-missing-value-encodings"
hidden: false
createdAt: "2022-08-30T18:19:30.145Z"
updatedAt: "2022-12-13T22:47:08.171Z"
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