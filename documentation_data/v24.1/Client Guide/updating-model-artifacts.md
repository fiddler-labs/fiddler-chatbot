---
title: "Updating model artifacts"
slug: "updating-model-artifacts"
excerpt: "Update a model already in Fiddler (surrogate or user artifact model)"
hidden: false
createdAt: "Wed Feb 01 2023 15:55:08 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
If you need to update a model artifact already uploaded in Fiddler, you can use the `client.update_model_artifact` function. This allows you to replace a surrogate model or your own uploaded model.

Once you have prepared the [model artifacts directory](doc:artifacts-and-surrogates), you can update your model using [client.update_model_artifact](ref:clientupdate_model_artifact)

```python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
MODEL_ARTIFACTS_DIR = Path('model/')

client.update_model_artifact(
    artifact_dir=MODEL_ARTIFACTS_DIR,
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```
