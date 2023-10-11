---
title: "fdl.CustomFeature.from_columns"
slug: "fdlcustomfeaturefrom_columns"
hidden: false
createdAt: "2022-11-04T17:35:53.326Z"
updatedAt: "2023-04-17T20:02:57.953Z"
---
This function creates a custom feature from multiple numerical columns.  

| Input Parameters | Type      | Default | Description                                                                                            |
| :--------------- | :-------- | :------ | :----------------------------------------------------------------------------------------------------- |
| cols             | List[str] |         | A list of column names that define this custom feature.                                                |
| custom_name      | str       |         | The name of this custom feature as it will appear in the monitoring tab.                               |
| n_clusters       | int       | 10      | Number of clusters used for clustering-based drift monitoring.                                         |
| monitor          | bool      | True    | A boolean that specifies whether this custom feature will be monitored using clustering-based binning. |

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



| Return Type       | Description                                                                           |
| :---------------- | :------------------------------------------------------------------------------------ |
| fdl.CustomFeature | A [fdl.CustomFeature](ref:fdlcustomfeature) object which can be passed to model info. |