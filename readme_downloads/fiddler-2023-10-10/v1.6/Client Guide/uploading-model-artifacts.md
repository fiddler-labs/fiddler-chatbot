---
title: "Uploading model artifacts"
slug: "uploading-model-artifacts"
excerpt: "Upload a model artifact in Fiddler"
hidden: false
createdAt: "2023-02-01T16:04:40.181Z"
updatedAt: "2023-03-08T20:59:25.056Z"
---
Before uploading your model artifact into Fiddler, you need to add the model with [client.add_model](ref:clientadd_model).

Once you have prepared the [model artifacts directory](doc:artifacts-and-surrogates), you can upload your model using [client.add_model_artifact](ref:clientadd_model_artifact)

```python
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'
MODEL_ARTIFACTS_DIR = Path('model/')

client.add_model_artifact(
    model_dir=MODEL_ARTIFACTS_DIR,
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```