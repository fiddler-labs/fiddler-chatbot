---
title: Uploading model artifacts
slug: uploading-model-artifacts
excerpt: >-
  This document provides instructions on how to upload a model artifact into
  Fiddler by creating the model and updating the artifact.
metadata:
  description: >-
    This document provides instructions on how to upload a model artifact into
    Fiddler by creating the model and updating the artifact.
  image: []
  robots: index
createdAt: Fri Apr 05 2024 12:04:04 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 13:25:53 GMT+0000 (Coordinated Universal Time)
---

# Uploading Model Artifacts

Before uploading your model artifact into Fiddler, you need to add the model using [model.create](create-a-project-and-model.md) function as well as [create a baseline for it](creating-a-baseline-dataset.md).

Once you have prepared the [model artifact directory](../product-guide/explainability/artifacts-and-surrogates.md), you can upload your model.

#### Upload the artifact

```python

job = model.add_artifact(
    model_dir=MODEL_ARTIFACTS_DIR,
)
job.wait()
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

