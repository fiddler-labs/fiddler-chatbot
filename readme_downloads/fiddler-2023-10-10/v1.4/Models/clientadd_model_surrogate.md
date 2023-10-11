---
title: "client.add_model_surrogate"
slug: "clientadd_model_surrogate"
excerpt: "Adds a surrogate model to an existing a model without uploading an artifact."
hidden: false
createdAt: "2022-08-01T03:05:32.641Z"
updatedAt: "2022-12-14T19:14:32.326Z"
---
> 📘 Note
> 
> Before calling this function, you must have already added a model using [`add_model`](/reference/clientadd_model).

| Input Parameter                | Type                                          | Default | Description                                                                                                                                                                                              |
| :----------------------------- | :-------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id                     | str                                           | None    | The unique identifier for the project.                                                                                                                                                                   |
| model_id                       | str                                           | None    | A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| deployment                     | Optional [fdl.core_objects.DeploymentOptions] | None    | A **DeploymentOptions** object containing information about the model deployment.                                                                                                                        |
| cache_global_impact_importance | Optional [bool]                               | True    | If True, global feature impact and global feature importance will be precomputed and cached when the model is registered.                                                                                |
| cache_global_pdps              | Optional [bool]                               | False   | If True, global partial dependence plots will be precomputed and cached when the model is registered.                                                                                                    |
| cache_dataset                  | Optional [bool]                               | True    | If True, histogram information for the baseline dataset will be precomputed and cached when the model is registered.                                                                                     |

```python Usage
PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

client.add_model_surrogate(
    project_id=PROJECT_ID,
    model_id=MODEL_ID
)
```



| Return Type | Description                                                |
| :---------- | :--------------------------------------------------------- |
| str         | A message confirming that a surrogate model was generated. |