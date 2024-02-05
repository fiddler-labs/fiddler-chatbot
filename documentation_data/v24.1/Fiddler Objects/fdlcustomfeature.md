---
title: "fdl.CustomFeature"
slug: "fdlcustomfeature"
excerpt: "This is the base class that all other custom features inherit from.  It's flexible enough to accommodate different types of derived features.  Note: All of the derived feature classes (e.g., Multivariate, VectorFeature, etc.) inherit from CustomFeature and thus have its properties, in addition to their specific ones."
hidden: false
createdAt: "Tue Oct 24 2023 03:47:43 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type                                      | Default | Description                                                                                                                       |
| :-------------- | :---------------------------------------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| name            | str                                       | None    | The name of the custom feature.                                                                                                   |
| type            | [CustomFeatureType](fdlcustomfeaturetype) | None    | The type of custom feature. Must be one of the `CustomFeatureType` enum values.                                                   |
| n_clusters      | Optional[int]                             | 5       | The number of clusters.                                                                                                           |
| centroids       | Optional[List]                            | None    | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters`.                                       |
| columns         | Optional\[List[str]]                      | None    | For `FROM_COLUMNS` type, represents the original columns from which the feature is derived.                                       |
| column          | Optional[str]                             | None    | Used for vector-derived features, the original vector column name.                                                                |
| source_column   | Optional[str]                             | None    | Specifies the original column name for embedding-derived features.                                                                |
| n_tags          | Optional[int]                             | 5       | For `FROM_TEXT_EMBEDDING` type, represents the number of tags for each cluster in the `tfidf` summarization in drift computation. |

```python Usage
# use from_columns helper function to generate a custom feature combining multiple numeric columns

feature = fdl.CustomFeature.from_columns(
    name='my_feature',
    columns=['column_1', 'column_2'],
    n_clusters=5
)
```
