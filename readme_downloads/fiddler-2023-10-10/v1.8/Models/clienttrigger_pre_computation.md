---
title: "client.trigger_pre_computation"
slug: "clienttrigger_pre_computation"
excerpt: "Runs a variety of precomputation steps for a model."
hidden: false
createdAt: "2022-05-23T19:36:35.716Z"
updatedAt: "2023-06-13T19:09:53.188Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  This method is called automatically now when calling _client.add_model_surrogate()_ or _client.add_model_artifact()_.

> 📘 Note
> 
> This method should be called after _client.upload_model_package()_.  It is not necessary after calling _client.register_model()_ as this step happens automatically when onboarding a model.

| Input Parameter                | Type            | Default | Description                                                                                                               |
| :----------------------------- | :-------------- | :------ | :------------------------------------------------------------------------------------------------------------------------ |
| project_id                     | str             | None    | The unique identifier for the project.                                                                                    |
| model_id                       | str             | None    | A unique identifier for the model.                                                                                        |
| dataset_id                     | str             | None    | The unique identifier for the dataset.                                                                                    |
| overwrite_cache                | Optional [bool] | True    | If True, will overwrite existing cached information.                                                                      |
| batch_size                     | Optional [int]  | 10      | The batch size used for global PDP calculations.                                                                          |
| calculate_predictions          | Optional [bool] | True    | If True, will precompute and store model predictions.                                                                     |
| cache_global_impact_importance | Optional [bool] | True    | If True, global feature impact and global feature importance will be precomputed and cached when the model is registered. |
| cache_global_pdps              | Optional [bool] | True    | If True, global partial dependence plots will be precomputed and cached when the model is registered.                     |
| cache_dataset                  | Optional [bool] | False   | If True, histogram information for the baseline dataset will be precomputed and cached when the model is registered.      |

```python Usage
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

client.trigger_pre_computation(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID
)
```