---
title: Publishing Batches of Events
slug: publishing-batches-of-events
excerpt: ''
createdAt: Tue Apr 19 2022 20:15:35 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 22 2024 18:48:57 GMT+0000 (Coordinated Universal Time)
---

# Publishing Batches Of Events

Fiddler has a flexible ETL framework for retrieving and publishing batches of production data, either from local storage or from the cloud. This provides maximum flexibility in how you are required to store your data when publishing events to Fiddler.

***

**The following data formats are currently supported:**

* pandas DataFrame objects (`pd.DataFrame`)
* CSV files (`.csv`),
* Parquet files (`.pq`)

***

**The following data locations are supported:**

* In memory (for DataFrames)
* Local disk
* AWS S3

***

Once you have a batch of events stored somewhere, all you need to do to publish the batch to Fiddler is call the Fiddler client's `fdl.Model.publish` function.

```python
model.publish("my_batch.csv")
```

_After calling the function, please allow 3-5 minutes for events to populate the_ _**Monitor**_ _page._

{% include "../../.gitbook/includes/main-doc-dev-footer.md" %}

