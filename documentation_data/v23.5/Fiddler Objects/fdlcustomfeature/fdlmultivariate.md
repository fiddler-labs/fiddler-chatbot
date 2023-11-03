---
title: "fdl.Multivariate"
slug: "fdlmultivariate"
excerpt: "Represents custom features derived from multiple columns."
hidden: false
createdAt: "2023-10-24T04:05:45.942Z"
updatedAt: "2023-10-25T00:37:50.270Z"
---
| Input Parameter    | Type                                      | Default                                                                                    | Description                                                                                                                                |
| :----------------- | :---------------------------------------- | :----------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| type               | [CustomFeatureType](fdlcustomfeaturetype) | CustomFeatureType.FROM_COLUMNS                                                             | Indicates this feature is derived from multiple columns.                                                                                   |
| columns            | List[str]                                 | None                                                                                       | List of original columns from which this feature is derived.                                                                               |
| n_clusters         | Optional[int]                             | 5                                                                                          | The number of clusters.                                                                                                                    |
| centroids          | Optional[List]                            | Centroids of the clusters in the embedded space. Number of centroids equal to `n_clusters` | Centroids of the clusters in the embedded space. Number of centroids equal to \`n_clusters                                                 |
| monitor_components | bool                                      | False                                                                                      | Whether to monitor each column in `columns` as individual feature. If set to `True`, components are monitored and drift will be available. |

```python Usage
multivariate_feature = fdl.Multivariate(
    name='multi_feature',
    columns=['column_1', 'column_2']
)
```