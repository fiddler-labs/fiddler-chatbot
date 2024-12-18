---
title: "Specifying Custom Features"
slug: "vector-monitoring"
excerpt: "\"Patented Fiddler Technology\""
hidden: false
createdAt: "Thu Oct 19 2023 19:24:35 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Fri Apr 19 2024 13:33:04 GMT+0000 (Coordinated Universal Time)"
---
# Vector Monitoring for Unstructured Data

```python
CF1 = fdl.CustomFeature.from_columns(['f1','f2','f3'], custom_name = 'vector1')
CF2 = fdl.CustomFeature.from_columns(['f1','f2','f3'], n_clusters=5, custom_name = 'vector2')
CF3 = fdl.TextEmbedding(name='text_embedding',column='embedding',source_column='text')
CF4 = fdl.ImageEmbedding(name='image_embedding',column='embedding',source_column='image_url')
```

### Passing Custom Features List to Model Spec

```python
model_spec = fdl.ModelSpec(
    inputs=['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance'],
    outputs=['probability_churned'],
    targets=['Churned'],
    decisions=[],
    metadata=[],
    custom_features=[CF1,CF2,CF3,CF4],
)
```

> 📘 Quick Start for NLP Monitoring
> 
> Check out our [Quick Start guide for NLP monitoring](../QuickStart_Notebooks/simple-nlp-monitoring-quick-start.md) for a fully functional notebook example.
