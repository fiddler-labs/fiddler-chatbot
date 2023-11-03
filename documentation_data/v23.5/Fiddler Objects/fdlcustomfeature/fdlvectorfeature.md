---
title: "fdl.VectorFeature"
slug: "fdlvectorfeature"
excerpt: "Represents custom features derived from a single vector column."
hidden: false
createdAt: "2023-10-24T04:08:01.137Z"
updatedAt: "2023-10-25T00:38:11.186Z"
---
| Input Parameter | Type                                      | Default                                                                                    | Description                                                                                |
| :-------------- | :---------------------------------------- | :----------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| type            | [CustomFeatureType](fdlcustomfeaturetype) | CustomFeatureType.FROM_VECTOR                                                              | Indicates this feature is derived from a single vector column.                             |
| source_column   | Optional[str]                             | None                                                                                       | Specifies the original column if this feature is derived from an embedding.                |
| column          | str                                       | None                                                                                       | The vector column name.                                                                    |
| n_clusters      | Optional[int]                             | 5                                                                                          | The number of clusters.                                                                    |
| centroids       | Optional[List]                            | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` |

```python Usage
vector_feature = fdl.VectorFeature(
    name='vector_feature',
    column='vector_column'
)
```