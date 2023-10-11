---
title: "client.get_slice"
slug: "clientget_slice"
excerpt: "Retrieve a slice of data as a pandas DataFrame."
hidden: false
createdAt: "2022-05-25T15:10:30.006Z"
updatedAt: "2023-08-01T13:28:05.798Z"
---
| Input Parameter  | Type                 | Default | Description                                                                                                                                     |
| :--------------- | :------------------- | :------ | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| sql_query        | str                  | None    | The SQL query used to retrieve the slice.                                                                                                       |
| project_id       | str                  | None    | The unique identifier for the project.  The model and/or the dataset to be queried within the project are designated in the _sql_query_ itself. |
| columns_override | Optional [list]      | None    | A list of columns to include in the slice, even if they aren't specified in the query.                                                          |
| project_name     | str                  | None    | The unique identifier for the project.  The model and/or the dataset to be queried within the project are designated in the _sql_query_ itself. |
| query            | str                  | None    | The SQL query used to retrieve the slice.                                                                                                       |
| columns          | Optional\[List[str]] | None    | A list of columns to include in the slice, even if they aren't specified in the query.                                                          |
| sample           | Optional[bool]       | None    | Boolean value indicating if the rows should be sample from the database or not.                                                                 |
| max_rows         | Optional[bool]       | None    | Number of maximum rows to fetch                                                                                                                 |

```python Usage - Query a dataset
import pandas as pd

PROJECT_NAME = 'example_project'
DATASET_NAME = 'example_dataset'
MODEL_NAME = 'example_model'

query = f""" SELECT * FROM "{DATASET_NAME}.{MODEL_NAME}" """

slice_df = client.get_slice(
    query=query,
    project_name=PROJECT_NAME
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