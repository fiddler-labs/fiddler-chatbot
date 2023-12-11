---
title: "Retrieving Events"
slug: "retrieving-events"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed Jul 06 2022 16:22:23 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
After publishing events to Fiddler, you may want to retrieve them for further analysis.
[block:api-header]
{
  "title": "Querying production data"
}
[/block]
You can query production data from the **Analyze** tab by issuing the following SQL query to Fiddler.

```sql
SELECT
    *
FROM
    "production.MODEL_ID"
```

The above query will return the entire production table (all published events) for a model with a model ID of `MODEL_ID`.

[block:api-header]
{
  "title": "Querying a baseline dataset"
}
[/block]
You can query a baseline dataset that has been uploaded to Fiddler with the following SQL query.

```sql
SELECT
    *
FROM
    "DATASET_ID.MODEL_ID"
```

Here, this will return the entire baseline dataset that has been uploaded with an ID of `DATASET_ID` to a model with an ID of `MODEL_ID`.