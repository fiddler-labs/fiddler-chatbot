---
title: "fdl.ImageEmbedding"
slug: "fdlimageembedding"
excerpt: "Represents custom features derived from image embeddings."
hidden: false
createdAt: "2023-10-24T04:11:24.486Z"
updatedAt: "2023-10-25T18:55:39.576Z"
---
| Input Parameter | Type                                      | Default                                                                                    | Description                                                                                |
| :-------------- | :---------------------------------------- | :----------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------- |
| type            | [CustomFeatureType](fdlcustomfeaturetype) | CustomFeatureType.FROM_IMAGE_EMBEDDING                                                     | Indicates this feature is derived from an image embedding.                                 |
| source_column   | str                                       | Required                                                                                   | URL where image data is stored                                                             |
| column          | str                                       | Required                                                                                   | Specifies the column name where embeddings corresponding to source_col are stored.         |
| n_clusters      | Optional[int]                             | 5                                                                                          | The number of clusters                                                                     |
| centroids       | Optional[List]                            | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` |

```python Usage
image_embedding_feature = fdl.ImageEmbedding(
    name='image_feature',
    source_column='image_url',
    column='image_embedding',
)
```