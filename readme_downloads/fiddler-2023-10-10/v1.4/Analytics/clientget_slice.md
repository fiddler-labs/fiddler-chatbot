---
title: "client.get_slice"
slug: "clientget_slice"
excerpt: "Retrieve a slice of data as a pandas DataFrame."
hidden: false
createdAt: "2022-05-25T15:10:30.006Z"
updatedAt: "2022-06-21T17:25:05.581Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Parameter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "sql_query",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The SQL query used to retrieve the slice.",
    "1-0": "project_id",
    "1-1": "str",
    "1-2": "None",
    "1-3": "The unique identifier for the project.  The model and/or the dataset to be queried within the project are designated in the *sql_query* itself.",
    "2-0": "columns_override",
    "2-1": "Optional [list]",
    "2-2": "None",
    "2-3": "A list of columns to include in the slice, even if they aren't specified in the query."
  },
  "cols": 4,
  "rows": 3
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "import pandas as pd\n\nPROJECT_ID = 'example_project'\nDATASET_ID = 'example_dataset'\nMODEL_ID = 'example_model'\n\nquery = f\"\"\" SELECT * FROM \"{DATASET_ID}.{MODEL_ID}\" \"\"\"\n\nslice_df = client.get_slice(\n    sql_query=query,\n    project_id=PROJECT_ID\n)",
      "language": "python",
      "name": "Usage - Query a dataset"
    },
    {
      "code": "import pandas as pd\n\nPROJECT_ID = 'example_project'\nMODEL_ID = 'example_model'\n\nquery = f\"\"\" SELECT * FROM \"production.{MODEL_ID}\" \"\"\"\n\nslice_df = client.get_slice(\n    sql_query=query,\n    project_id=PROJECT_ID\n)",
      "language": "python",
      "name": "Usage - Query published events"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "pd.DataFrame",
    "0-1": "A pandas DataFrame containing the slice returned by the query."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:callout]
{
  "type": "info",
  "title": "Info",
  "body": "Only read-only SQL operations are supported. Certain SQL operations like aggregations and joins might not result in a valid slice."
}
[/block]