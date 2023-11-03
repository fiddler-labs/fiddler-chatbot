---
title: "fdl.EventIdDataSource"
slug: "fdleventiddatasource"
excerpt: "Indicates the single row to use for point explanation given the Event ID."
hidden: false
createdAt: "2023-08-30T14:41:28.432Z"
updatedAt: "2023-10-24T04:14:06.864Z"
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