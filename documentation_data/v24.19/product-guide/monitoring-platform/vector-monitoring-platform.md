---
title: Vector Monitoring
slug: vector-monitoring-platform
excerpt: '"Patented Fiddler Technology"'
createdAt: Mon Dec 19 2022 19:22:52 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 21:17:39 GMT+0000 (Coordinated Universal Time)
---

# Vector Monitoring

Many modern machine learning systems use input features that cannot be represented as a single number (e.g., text or image data). Such complex features are usually rather represented by high-dimensional vectors which are obtained by applying a vectorization method (e.g., text embeddings generated by NLP models). Furthermore, Fiddler users might be interested in monitoring a group of univariate features together and detecting data drift in multi-dimensional feature spaces.

In order to address the above needs, Fiddler provides a vector monitoring capability which involves enabling users to define "custom features", and a novel method for monitoring data drift in multi-dimensional spaces.

Custom features can be defined by grouping columns together in the baseline and inference data. Or, in the case of NLP or image data, custom features can be defined using columns containing embedding vectors.

## Defining Custom Features

Users can use the Fiddler client to define one or more custom features. Custom features can be specified by:

1. a group of dataset columns that need to be monitored together as a vector. (CF1, CF2)
2. a column containing an existing embedding vector along with the source column (CF3, CF4)
3. defining an enrichment that will instruct Fiddler to generate the embedding vector within the product itself (CF5, CF6).

Once a list of custom features is defined and passed to Fiddler (the details of how to use the Fiddler client to define custom features are provided below), Fiddler runs a clustering-based data drift detection algorithm for each custom feature and calculates a corresponding drift value between the baseline and the published events at the selected time period.

```python
CF1 = fdl.CustomFeature.from_columns(['f1','f2','f3'], custom_name = 'vector1')
CF2 = fdl.CustomFeature.from_columns(['f1','f2','f3'], n_clusters=5, custom_name = 'vector2')
CF3 = fdl.TextEmbedding(name='text_embedding',column='embedding_col',source_column='text')
CF4 = fdl.ImageEmbedding(name='image_embedding',column='embedding_col2',source_column='image_url')

CF5 = fdl.Enrichment(
        name='Enrichment Unstructured Embedding',
        enrichment='embedding',
        columns=['doc_col'],
    )
CF6 = fdl.TextEmbedding(
        name='Document TextEmbedding',
        source_column='doc_col',
        column='Enrichment Unstructured Embedding',
        n_tags=10
    )
```

## Passing Custom Features List to ModelSpec

Once the custom features are defined for vector monitoring, they are then defined as a part of the [`fdl.ModelSpec`](../../Python\_Client\_3-x/api-methods-30.md#modelspec) and onboarded to Fiddler.

```python
model_spec = fdl.ModelSpec(
    inputs=[
        'creditscore',
        'geography',
        'gender',
        'age',
        'tenure',
        'balance',
        'numofproducts',
        'hascrcard',
        'isactivemember',
        'estimatedsalary',
        'doc_col'
    ],
    outputs=['predicted_churn'],
    targets=['churn'],
    metadata=['customer_id', 'timestamp']
    custom_features = [CF1,CF2,CF3,CF4,C5,C6]
)

MODEL_NAME = 'my_model'

model = fdl.Model.from_data(
    name=MODEL_NAME,
    project_id=fdl.Project.from_name(PROJECT_NAME).id,
    source=sample_df,
    spec=model_spec,
    task=model_task,
    task_params=task_params,
    event_id_col=id_column,
    event_ts_col=timestamp_column
)

model.create()
```

> 📘 Quick Start for NLP Monitoring
>
> Check out our [Quick Start guide for NLP monitoring](../../QuickStart\_Notebooks/simple-nlp-monitoring-quick-start.md) for a fully functional notebook example where we instruct Fiddler to generate the embeddings for unstructured inputs.

{% include "../../.gitbook/includes/main-doc-footer.md" %}
