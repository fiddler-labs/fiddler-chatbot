---
title: "fdl.TextEmbedding"
slug: "fdltextembedding"
excerpt: "Represents custom features derived from text embeddings."
hidden: false
createdAt: "2023-10-24T04:09:57.121Z"
updatedAt: "2023-10-27T00:10:24.153Z"
---
| Input Parameter | Type                                      | Default                                                                                    | Description                                                                                                          |
| :-------------- | :---------------------------------------- | :----------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| type            | [CustomFeatureType](fdlcustomfeaturetype) | CustomFeatureType.FROM_TEXT_EMBEDDING                                                      | Indicates this feature is derived from a text embedding.                                                             |
| source_column   | str                                       | Required                                                                                   | Specifies the column name where text data (e.g. LLM prompts) is stored                                               |
| column          | str                                       | Required                                                                                   | Specifies the column name where the embeddings corresponding to source_col are stored                                |
| n_tags          | Optional[int]                             | 5                                                                                          | How many tags(tokens) the text embedding are used in each cluster as the `tfidf` summarization in drift computation. |
| n_clusters      | Optional[int]                             | 5                                                                                          | The number of clusters.                                                                                              |
| centroids       | Optional[List]                            | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters`                           |

```python Usage
text_embedding_feature = TextEmbedding(
    name='text_custom_feature',
    source_column='text_column',
    column='text_embedding',
    n_tags=10
)
```