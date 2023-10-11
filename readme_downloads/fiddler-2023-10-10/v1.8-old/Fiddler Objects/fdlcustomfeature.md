---
title: "fdl.CustomFeature"
slug: "fdlcustomfeature"
hidden: false
createdAt: "2022-11-04T17:35:03.202Z"
updatedAt: "2023-05-01T20:13:52.837Z"
---
This Fiddler object is used to define custom features based on the columns of a dataset. Custom features are mainly used for monitoring multi-dimensional vectors in NLP and CV use cases. This object holds information about which data columns constitute a custom feature, and information that specifies the settings for monitoring this custom feature.

| Attribute  | Type                                          | Default | Description                                                                                            |
| :--------- | :-------------------------------------------- | :------ | :----------------------------------------------------------------------------------------------------- |
| name       | str                                           | None    | The name of the custom feature                                                                         |
| columns    | List[str]                                     | None    | A list of column name in the dataset which define this custom feature.                                 |
| type       | [CustomFeatureType](ref:fdlcustomfeaturetype) |         | The type of the custom feature based on its origin.                                                    |
| n_clusters | int                                           | 10      | Number of clusters used for clustering-based drift monitoring.                                         |
| monitor    | bool                                          | True    | A boolean that specifies whether this custom feature will be monitored using clustering-based binning. |

In order to initiate a custom feature whose elements are stored across columns of the baseline DataFrame, use the [fdl.CustomFeature.from_columns()](ref:fdlcustomfeaturefrom_columns) constructor function.