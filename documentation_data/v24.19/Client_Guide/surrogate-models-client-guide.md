---
title: Adding a Surrogate Model
slug: surrogate-models-client-guide
excerpt: ''
createdAt: Tue Dec 13 2022 22:22:39 GMT+0000 (Coordinated Universal Time)
updatedAt: Fri Apr 19 2024 13:23:06 GMT+0000 (Coordinated Universal Time)
---

# Adding a Surrogate Model

Fiddler’s explainability features require a model on the backend that can generate explanations for you.

> 📘 If you don't want to or cannot upload your actual model file, Surrogate Models serve as a way for Fiddler to generate approximate explanations.

A surrogate model **is built automatically** when you call [`add_surrogate`](../Python\_Client\_3-x/api-methods-30.md#add\_surrogate) on an existing model that has a [baseline dataset](creating-a-baseline-dataset.md) defined. You just need to provide a few key details on how your model operates during onboarding.

### Surrogate Model prerequisites:

* An onboarded model with:
  * A defined model task (regression, binary classification, etc.)
  * A target column (ground truth labels)
  * An output column (model predictions)
  * Model feature columns
  * A baseline dataset

#### Update the artifact

```python
DATASET_NAME = 'YOUR_DATASET_NAME'

dataset = fdl.Dataset.from_name(name=DATASET_NAME, model_id=model.id)

job = model.add_surrogate(
    dataset_id=dataset.id
)
job.wait()
```

{% include "../.gitbook/includes/main-doc-dev-footer.md" %}

