---
title: Publishing Ranking Events
slug: ranking-events
excerpt: ''
createdAt: Thu Jun 30 2022 22:05:47 GMT+0000 (Coordinated Universal Time)
updatedAt: Thu Apr 25 2024 15:03:06 GMT+0000 (Coordinated Universal Time)
---

# Ranking Events

### Publish ranking events

#### The grouped format

Before publishing ranking model events into Fiddler, we need to make sure they are in **grouped format** (i.e. the listing returned within the same **query id**—which is usually the `group_by` argument passed as a part of [TaskParams](../../Python\_Client\_3-x/api-methods-30.md#modeltaskparams) to the [Model](../../Python\_Client\_3-x/api-methods-30.md#model)object—is in the same row with other cells as lists). The first row in the example below indicates there are 3 items returned by **query id**(`srch_id'` in the table) 1.

Below is an example of what this might look like.

| srch\_id | price\_usd                 | review\_score      | ...    | prediction               | target     |
| -------- | -------------------------- | ------------------ | ------ | ------------------------ | ---------- |
| 101      | \[134.77,180.74,159.80]    | \[5.0,2.5,4.5]     | \[...] | \[1.97, 0.84,-0.69]      | \[1,0,0]   |
| ...      | ...                        |                    | ...    | ...                      | ...        |
| 112      | \[26.00,51.00,205.11,73.2] | \[3.0,4.5,2.0,1.0] | \[...] | \[10.75,8.41,-0.23,-3.2] | \[0,1,0,0] |

In the above example, `srch_id` is the name of our `group_by` column, and the other columns all contain lists corresponding to the given group.

#### How can I convert a flat CSV file into this format?

If you're storing your data in a flat CSV file (i.e. each row contains a single item), Fiddler provides a utility function that can be used to convert the flat CSV file into the grouped format specified above.

```python
from fiddler.utils.helpers import group_by
import pandas as pd

df = pd.read_csv('path/to/ranking_events.csv')
df_grouped = group_by(df=df, group_by_col='srch_id')
```

#### Call `model.publish()`

```python

model.publish(df_grouped)

```

In the above example, the `group_by_col` argument should refer to the same column that was specified in the `group_by` argument passed to the [Model Object](../../Python\_Client\_3-x/api-methods-30.md#model).

### Update ranking events

#### Prepare the updating dataframe

We also support updating events for ranking model. You can use `model.publish` method call with `update` flag to `True` and keep the grouped format unchanged.

For example, you might want to alter the exisiting `target` after events are published. You can create a dataframe in the format below where you add the required updates to the desired column. You can then use `model.publish` to send us the updated dataframe. Fiddler will recognise the updates to be made and make the changes in the updated columns, while keeping the rest the same.

#### Call `model.publish()` with `update` flag set to True

```python
model.publish(source=modified_df_grouped, update=True)
```

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

