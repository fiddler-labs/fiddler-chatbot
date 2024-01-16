---
title: "Specifying Custom Features"
slug: "vector-monitoring-copy"
excerpt: "\"Patented Fiddler Technology\""
hidden: false
createdAt: "Thu Oct 19 2023 19:24:35 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
# Vector Monitoring for Unstructured Data

```python pyth
CF1 = fdl.CustomFeature.from_columns(['f1','f2','f3'], custom_name = 'vector1')
CF2 = fdl.CustomFeature.from_columns(['f1','f2','f3'], n_clusters=5, custom_name = 'vector2')
CF3 = fdl.TextEmbedding(name='text_embedding',column='embedding',source_column='text')
CF4 = fdl.ImageEmbedding(name='image_embedding',column='embedding',source_column='image_url')
```

### Passing Custom Features List to Model Info

```python
model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    dataset_id = DATASET_ID,
    features = data_cols,
    target='target',
    outputs='predicted_score',
    custom_features = [CF1,CF2,CF3,CF4]
)
```

> 📘 Quick Start for NLP Monitoring
> 
> Check out our [Quick Start guide for NLP monitoring](doc:simple-nlp-monitoring-quick-start) for a fully functional notebook example.
