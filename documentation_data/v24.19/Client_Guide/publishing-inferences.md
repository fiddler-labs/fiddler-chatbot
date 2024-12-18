---
title: Publishing Inferences
slug: publishing-inferences
excerpt: >-
  This document explains how to publish pre-production and production data to a
  Fiddler model for inference data analysis. It provides code examples for batch
  publishing pre-production data and streaming production data.
metadata:
  description: >-
    This document explains how to publish pre-production and production data to
    a Fiddler model for inference data analysis. It provides code examples for
    batch publishing pre-production data and streaming production data.
  image: []
  robots: index
createdAt: Thu Mar 28 2024 11:36:51 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 11:54:04 GMT+0000 (Coordinated Universal Time)
---

# Publishing Inferences

Once a model's schema has been onboarded, you can publish events, also known as inferences, so that Fiddler can analyze that data to ensure expected performance. Event data can be sent as either pre-production or production data. Pre-production data refers to static datasets, such as model training or testing data, while production data consists of the model's time series data that is actively being monitored.

### Publish Pre-production Data to a Model

Fiddler allows only batch publication of pre-production data as it is typically available in its entirety. You can publish multiple pre-production datasets to a model. You may use a dataframe, parquet file, or CSV file for uploading a dataset.

```python
job = model.publish(
    source=DATASET_FILE_PATH,
    environment=fdl.EnvType.PRE_PRODUCTION,
    dataset_name=DATASET_NAME,
)
# The publish() method is asynchronous. Use the publish job's wait() method 
# if sychronous behavior is desired.
# job.wait() 
```

### Publish Production Data to a Model

#### Publish Events as a Stream

Fiddler supports event streams to be published to a model.

```python
model.event_ts_col = 'timestamp_col'
model.event_id_col = 'event_id_col'
DATASET_FILE_PATH = "dataset.csv"

df = pd.read_csv(DATASET_FILE_PATH)

# Generate event_id which is later needed for label updates
df[model.event_id_col] = [str(uuid4()) for _ in range(len(df))]
_add_timestamp(df=df, event_ts_col=model.event_ts_col)

event_ids = model.publish(source=df)

print(f'{len(event_ids)} events published')
```

#### Publish Production Events - Batch

The Fiddler client supports publishing micro batch streams (up to 1K events, configurable)

```python
events = df.sample(10).to_dict(orient='records') # this will give list of event dictionaries

events_ids = model.publish(source=events)

print(f'{len(events_ids)} events published')
```

#### Publish Production Label Updates - Stream

Fiddler supports updates of existing events for provided event ids.

```python
updated_events = [
        {
            model.event_id_col: event_id,
            model.spec.targets[0]: model.task_params.target_class_order[0],
        }
        for event_id in df.sample(100)[model.event_id_col]
]

events_ids = model.publish(source=updated_events, update=True)

print(f'{len(events_ids)} events updated')
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

