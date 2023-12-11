---
title: "client.get_slice (COPY)"
slug: "clientget_slice-new"
excerpt: "Retrieve a slice of data as a pandas DataFrame."
hidden: true
metadata: 
image: []
robots: "index"
createdAt: "Wed May 25 2022 15:10:30 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project. ",
    "1-0": "query",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The SQL query used to retrieve the slice.",
    "2-0": "columns",
    "2-1": "Optional [list]",
    "2-2": "None",
    "2-3": "The list of data columns to return. If None, all columns specified in the slice will be returned.",
    "3-0": "sample",
    "3-1": "Optional[bool]",
    "3-2": "False",
    "3-3": "Whether rows should be sample or not from the database.",
    "4-0": "max_rows",
    "4-1": "Optional[int]",
    "4-2": "10000",
    "4-3": "Number of maximum rows to fetch.  \nNote: Today, Fiddler only allows 10000 max rows to be fetched."
  },
  "cols": 4,
  "rows": 5,
  "align": [
    "left",
    "left",
    "left",
    "left"
  ]
}
[/block]

```python Usage - Query a dataset
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

query = f""" SELECT * FROM "{DATASET_ID}.{MODEL_ID}" """

slice_df = client.get_slice(
    project_id=PROJECT_ID,
  	query=query,
  	columns=['feature_1', 'output', 'target'],
  	sample=True,
  	max_rows=300,
)
```
```python Usage - Query published events
import pandas as pd

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

query = f""" SELECT * FROM "production.{MODEL_ID}" """

slice_df = client.get_slice(
    sql_query=query,
    project_id=PROJECT_ID
)
```

| Return Type  | Description                                                    |
| :----------- | :------------------------------------------------------------- |
| pd.DataFrame | A pandas DataFrame containing the slice returned by the query. |

> 📘 Info
> 
> Only read-only SQL operations are supported. Certain SQL operations like aggregations and joins might not result in a valid slice.