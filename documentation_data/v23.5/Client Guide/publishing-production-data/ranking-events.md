---
title: "Publishing Ranking Events"
slug: "ranking-events"
hidden: false
createdAt: "2022-06-30T22:05:47.259Z"
updatedAt: "2023-10-25T17:06:31.348Z"
---
## Publish ranking events

### The grouped format

Before publishing ranking model events into Fiddler, we need to make sure they are in **grouped format** (i.e. the listing returned within the same **query id**—which is usually the `group_by` argument passed to [`fdl.ModelInfo`](/reference/fdlmodelinfo)—is in the same row with other cells as lists). The first row in the example below indicates there are 3 items returned by **query id**(`srch_id'` in the table) 1. 

Below is an example of what this might look like.

| srch_id | price_usd                 | review_score      | ...   | prediction              | target    |
| :------ | :------------------------ | :---------------- | :---- | :---------------------- | --------- |
| 101     | [134.77,180.74,159.80]    | [5.0,2.5,4.5]     | [...] | [1.97, 0.84,-0.69]      | [1,0,0]   |
| ...     | ...                       |                   | ...   | ...                     | ...       |
| 112     | [26.00,51.00,205.11,73.2] | [3.0,4.5,2.0,1.0] | [...] | [10.75,8.41,-0.23,-3.2] | [0,1,0,0] |

In the above example, `srch_id` is the name of our `group_by` column, and the other columns all contain lists corresponding to the given group.

### How can I convert a flat CSV file into this format?

If you're storing your data in a flat CSV file (i.e. each row contains a single item), Fiddler provides a utility function that can be used to convert the flat CSV file into the grouped format specified above. 

```python
from fiddler.utils.pandas_helper import convert_flat_csv_data_to_grouped
import pandas as pd

grouped_df = convert_flat_csv_data_to_grouped(input_data=pd.read_csv('path/to/ranking_events.csv'), group_by_col='srch_id')
```

### Call `publish_events_batch`

```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source=grouped_df,
  	id_field='event_id',
)
```

In the above example, the `group_by_col` argument should refer to the same column that was specified in the `group_by` argument passed to [`fdl.ModelInfo`](/reference/fdlmodelinfo).

## Update ranking events

### Prepare the updating dataframe

We also support updating events for ranking model. You can use `publish_events_batch` and `publish_event` APIs with `update_event` flag to `True` and keep the grouped format unchanged.

For example, you might want to alter the exisiting `target` after events are published. You can create a dataframe in the format below where `group_by_col`,`id_col` and `target_col` are required fields. You can either upload the complete group of events within one `query_id` or the subset contains the changed events.

`Complete format`

| srch_id | event_id                  | target    |
| :------ | :------------------------ | :-------- |
| 101     | ['001','002','003']       | [0,1,0]   |
| ...     | ...                       | ...       |
| 112     | ['367','368','369','370'] | [0,0,0,1] |

`Partial format`

| srch_id | event_id      | target |
| :------ | :------------ | :----- |
| 101     | ['001','002'] | [0,1]  |
| ...     | ...           | ...    |
| 112     | ['367','370'] | [0,1]  |

### Call `publish_events_batch` with `update_event` flag set to True

```python Python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source=grouped_df_update,
  	id_field='event_id',
  	update_event=True,
)
```

### Or call `publish_event` with `update_event` flag

```python Python
events_dict = grouped_df_graded.to_dict('index')
for i, group_id in enumerate(events_dict):
    e= events_dict[group_id]
    '''
    first event:
    {'srch_id':101,'event_id':['001','002'],'target':[0,1]}
    '''
    client_v2.publish_event(project_id=project_id, model_id=model_id, event=e, update_event=True, event_id=str(e['event_id']))
```