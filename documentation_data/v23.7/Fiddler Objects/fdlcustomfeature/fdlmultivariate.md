---
title: "fdl.Multivariate"
slug: "fdlmultivariate"
excerpt: "Represents custom features derived from multiple columns."
hidden: false
createdAt: "Tue Oct 24 2023 04:05:45 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
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
