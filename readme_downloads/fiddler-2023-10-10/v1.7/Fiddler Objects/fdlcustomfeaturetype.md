---
title: "fdl.CustomFeatureType"
slug: "fdlcustomfeaturetype"
excerpt: "The type of a custom feature based on how it is created."
hidden: false
createdAt: "2023-05-01T17:44:15.497Z"
updatedAt: "2023-05-01T20:14:44.115Z"
---
| Enum Value   | Description                                                               |
| :----------- | :------------------------------------------------------------------------ |
| FROM_COLUMNS | A custom feature whose elements are stored across columns of a DataFrame. |

The CustomFeatureType is used internally in Fiddler to specify the type of custom features based on their origin. For creating custom features we recommend using the constructor helper functions such as [fdl.CustomFeature.from_columns()](ref:fdlcustomfeaturefrom_columns) which specify the CustomFeatureType automatically.