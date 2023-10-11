---
title: "client.register_model"
slug: "clientregister_model"
excerpt: "Registers a model without uploading an artifact. Requires a** fdl.ModelInfo** object containing information about the model."
hidden: false
createdAt: "2022-05-23T19:14:26.437Z"
updatedAt: "2022-12-12T19:55:31.652Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Please use _client.add_model()_ going forward.

For more information, see [Registering a Model](doc:registering-a-model).

| Input Parameter                | Type                                          | Default | Description                                                                                                                                                                                              |
| :----------------------------- | :-------------------------------------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id                     | str                                           | None    | The unique identifier for the project.                                                                                                                                                                   |
| model_id                       | str                                           | None    | A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| dataset_id                     | str                                           | None    | The unique identifier for the dataset.                                                                                                                                                                   |
| model_info                     | fdl.ModelInfo                                 | None    | A [fdl.ModelInfo()](ref:fdlmodelinfo) object containing information about the model.                                                                                                                     |
| deployment                     | Optional [fdl.core_objects.DeploymentOptions] | None    | A **DeploymentOptions** object containing information about the model deployment.                                                                                                                        |
| cache_global_impact_importance | Optional [bool]                               | True    | If True, global feature impact and global feature importance will be precomputed and cached when the model is registered.                                                                                |
| cache_global_pdps              | Optional [bool]                               | False   | If True, global partial dependence plots will be precomputed and cached when the model is registered.                                                                                                    |
| cache_dataset                  | Optional [bool]                               | True    | If True, histogram information for the baseline dataset will be precomputed and cached when the model is registered.                                                                                     |

```python Usage
PROJECT_ID = 'example_project'
DATASET_ID = 'example_dataset'
MODEL_ID = 'example_model'

dataset_info = client.get_dataset_info(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID
)

model_task = fdl.ModelTask.BINARY_CLASSIFICATION
model_target = 'target_column'
model_output = 'output_column'
model_features = [
    'feature_1',
    'feature_2',
    'feature_3'
]

model_info = fdl.ModelInfo.from_dataset_info(
    dataset_info=dataset_info,
    target=model_target,
    outputs=[model_output],
    model_task=model_task
)

client.register_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```



| Return Type | Description                                         |
| :---------- | :-------------------------------------------------- |
| str         | A message confirming that the model was registered. |

```python Response
'Model successfully registered on Fiddler. \n Visit https://app.fiddler.ai/projects/example_project'
```