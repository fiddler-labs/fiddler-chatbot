---
title: "fdl.EventIdDataSource"
slug: "fdleventiddatasource"
excerpt: "Indicates the single row to use for point explanation given the Event ID."
hidden: false
createdAt: "Wed Aug 30 2023 14:41:28 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Parameter | Type | Default | Description                                                                                                                |
| :-------------- | :--- | :------ | :------------------------------------------------------------------------------------------------------------------------- |
| event_id        | str  | None    | Single event id corresponding to the row to explain.                                                                       |
| dataset_name    | str  | None    | The dataset name if the event is located in the dataset table or 'production' if the event if part of the production data. |

```python Usage
DATASET_ID = 'example_dataset'

# In Dataset table
data_source = fdl.EventIdDataSource(
    event_id='xGhys7-83HgdtsoiuYTa872',
  	dataset_name=DATASET_ID,
)

# In Production table
data_source = fdl.EventIdDataSource(
    event_id='xGhys7-83HgdtsoiuYTa872',
  	dataset_name='production',
)
```
