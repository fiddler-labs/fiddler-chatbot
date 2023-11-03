---
title: "Publishing Batches of Events"
slug: "publishing-batches-of-events"
hidden: false
createdAt: "2022-04-19T20:15:35.016Z"
updatedAt: "2023-10-19T20:59:24.698Z"
---
> 📘 Info
> 
> See [client.publish_events_batch()](ref:clientpublish_events_batch) for detailed information on function usage.

Fiddler has a flexible ETL framework for retrieving and publishing batches of production data, either from local storage or from the cloud. This provides maximum flexibility in how you are required to store your data when publishing events to Fiddler.  

***



**The following data formats are currently supported:**

- pandas DataFrame objects (`pd.DataFrame`)
- CSV files (`.csv`),
- Parquet files (`.pq`)
- Pickled pandas DataFrame objects (`.pkl`),
- gzipped CSV files (`.csv.gz`),

***



**The following data locations are supported:**

- In memory (for DataFrames)
- Local disk
- AWS S3

***



Once you have a batch of events stored somewhere, all you need to do to publish the batch to Fiddler is call the Fiddler client's `publish_events_batch` function.

```python
client.publish_events_batch(
    project_id=PROJECT_ID,
    model_id=MODEL_ID,
    batch_source="my_batch.csv"
)
```



_After calling the function, please allow 3-5 minutes for events to populate the_ **_Monitor_** _page._