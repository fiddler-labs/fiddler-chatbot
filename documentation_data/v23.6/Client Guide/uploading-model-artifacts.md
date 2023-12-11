---
title: "Uploading model artifacts"
slug: "uploading-model-artifacts"
excerpt: "Upload a model artifact in Fiddler"
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed Feb 01 2023 16:04:40 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
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