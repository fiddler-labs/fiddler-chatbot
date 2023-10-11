---
title: "Specifying Custom Missing Value Encodings"
slug: "specifying-custom-missing-value-encodings"
hidden: false
createdAt: "2022-08-30T18:19:30.145Z"
updatedAt: "2022-10-28T22:07:08.374Z"
---
There may be cases in which you have missing values in your data, but you encode these values in a special way (other than the standard `NaN`).

In such cases, Fiddler offers a way to specify **your own missing value encodings for each column**.

***



You can create a "missing_value_encodings" dictionary, which holds the values you would like to have treated as missing for each column. Then just pass that dictionary into your [`fdl.ModelInfo`](/reference/fdlmodelinfo)  object before registering your model.

```python
missing_value_encodings = {
  'column_1': [-999, 'missing'],
  'column_2': [-1, '?', 'na']
}

model_info = fdl.ModelInfo.from_dataset_info(
  ...
  missing_value_encodings=missing_value_encodings
)
```

After you publish events, values in the corresponding `column` will be replaced with `NaN` when you query them on Analyze page as well as on Monitor page. 


[block:callout]
{
  "type": "warning",
  "title": "Note:",
  "body": "Since specified values are converted into `NaN` in Fiddler, please make sure the `column` in `missing_value_encodings` is created with `is_nullbale=True`.\n\n`missing_value_encodings` is also known as `fall_back` before client version `1.4.5`. It's recommended to upgrade to `1.4.5` or later to support `missing_value_encodings`."
}
[/block]