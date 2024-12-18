---
title: Updating model artifacts
slug: updating-model-artifacts
excerpt: >-
  This document explains how to update a model artifact or surrogate in Fiddler
  using the `Model.update_artifact` or `Model.update_surrogate` functions,
  allowing you to replace a surrogate model or your own uploaded model.
metadata:
  description: >-
    This document explains how to update a model artifact or surrogate in
    Fiddler using the `Model.update_artifact` or `Model.update_surrogate`
    functions, allowing you to replace a surrogate model or your own uploaded
    model.
  image: []
  robots: index
createdAt: Fri Apr 05 2024 12:34:08 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 13:34:58 GMT+0000 (Coordinated Universal Time)
---

# Updating Model Artifacts

If you need to update an existing model artifact or model surrogate in Fiddler, you can use the [update\_artifact()](../Python\_Client\_3-x/api-methods-30.md#update\_artifact) or [update\_surrogate()](../Python\_Client\_3-x/api-methods-30.md#update\_surrogate) functions. These functions allow you to replace existing model surrogates or your own uploaded model artifacts as needed.

#### Update an existing model artifact

Once you have prepared the [model artifacts directory](../product-guide/explainability/artifacts-and-surrogates.md), you can update your model.

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'

project_id = fdl.Project.from_name(PROJECT_NAME).id
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project_id)

job = model.update_artifact(
    model_dir=MODEL_DIR,
)
job.wait()
```

#### Update an existing model surrogate

One reason to update an existing surrogate is if you wish to use an updated baseline dataset from the one used originally. Fiddler will use this updated dataset when creating the model surrogate

```python
PROJECT_NAME = 'YOUR_PROJECT_NAME'
MODEL_NAME = 'YOUR_MODEL_NAME'
DATASET_NAME = 'YOUR_UPDATED_DATASET_NAME'

project_id = fdl.Project.from_name(PROJECT_NAME).id
model = fdl.Model.from_name(name=MODEL_NAME, project_id=project_id)
dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

model.update_surrogate(
  dataset_id=dataset.id
)
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

