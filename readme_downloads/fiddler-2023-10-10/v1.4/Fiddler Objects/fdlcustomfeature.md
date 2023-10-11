---
title: "fdl.CustomFeature"
slug: "fdlcustomfeature"
hidden: false
createdAt: "2022-11-04T17:02:27.888Z"
updatedAt: "2022-11-04T17:08:25.013Z"
---
This Fiddler object is used to define custom features based on the columns of a dataset. Custom features are mainly used for monitoring multi-dimensional vectors in NLP and CV use cases. This object holds information about which data columns constitute a custom feature, and information that specifies the settings for monitoring this custom feature.

| Attribute      | Type  | Default | Description                                                            |
| :------------- | :---- | :------ | :--------------------------------------------------------------------- |
| name           | str   | None    | The name of the custom feature                                         |
| columns        | [srt] | None    | A list of column name in the dataset which define this custom feature. |
| type           |       | None    |                                                                        |
| transformation | str   | None    |                                                                        |
| n_clusters     | int   | 10      |                                                                        |
| monitor        | bool  | True    |                                                                        |

In order to initiate a custom feature whose elements are stored across columns of the baseline DataFrame, use the [fdl.CustomFeature.from_columns()](ref:fdlcustomfeaturefrom_columns) constructor function.