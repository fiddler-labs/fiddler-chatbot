---
title: "Updating model artifacts"
slug: "updating-model-artifacts"
excerpt: "Update a model already in Fiddler (surrogate or user artifact model)"
hidden: false
createdAt: "2023-02-01T15:55:08.912Z"
updatedAt: "2023-03-08T21:10:47.961Z"
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