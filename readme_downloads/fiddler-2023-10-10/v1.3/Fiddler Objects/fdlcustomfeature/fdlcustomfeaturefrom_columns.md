---
title: "fdl.CustomFeature.from_columns"
slug: "fdlcustomfeaturefrom_columns"
hidden: false
createdAt: "2022-08-19T18:44:01.210Z"
updatedAt: "2022-11-03T20:02:50.303Z"
---
This function creates a custom feature from multiple numerical columns.  

| Input Parameters | Type      | Default | Description                                                                                                         |
| :--------------- | :-------- | :------ | :------------------------------------------------------------------------------------------------------------------ |
| cols             | List[str] |         | A list of column names that define this custom feature.                                                             |
| custom_name      | str       |         | The name of this custom feature as it will appear in the monitoring tab.                                            |
| transformation   | str       | None    | An optional transformation step. Currently no transformation is available.                                          |
| n_clusters       | int       | 10      | Number of clusters used for clustering-based drift monitoring.                                                      |
| monitor          | bool      | True    | A boolean variable that specifies whether this custom feature will be monitored using the clustering-based binning. |

```python Usage
CF1 = fdl.CustomFeature.from_columns(['f1','f2','f3'], 
                                     custom_name = 'vector1',
                                     n_clusters=5)

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id = DATASET_ID,
    features = data_cols,
    target='target',
    outputs='predicted_score',
    custom_features = [CF1]
)
```



| Return Type       | Description                                                                                                                         |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| fdl.CustomFeature | A [fdl.CustomFeature](https://dash.readme.com/project/fiddler/v1.3/refs/fdlcustomfeature) object which can be passed to model info. |