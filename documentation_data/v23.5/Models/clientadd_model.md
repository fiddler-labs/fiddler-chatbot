---
title: "client.add_model"
slug: "clientadd_model"
excerpt: "Adds a model to Fiddler without uploading an artifact. Requires a** fdl.ModelInfo** object containing information about the model. Requires dataset to have an **output** column."
hidden: false
createdAt: "2022-08-01T01:48:09.567Z"
updatedAt: "2023-10-24T04:14:06.843Z"
---
| Input Parameter | Type          | Default | Description                                                                                                                                                                                              |
| :-------------- | :------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_id      | str           | None    | The unique identifier for the project.                                                                                                                                                                   |
| model_id        | str           | None    | A unique identifier for the model. Must be a lowercase string between 2-30 characters containing only alphanumeric characters and underscores. Additionally, it must not start with a numeric character. |
| dataset_id      | str           | None    | The unique identifier for the dataset.                                                                                                                                                                   |
| model_info      | fdl.ModelInfo | None    | A [fdl.ModelInfo()](ref:fdlmodelinfo) object containing information about the model.                                                                                                                     |

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

client.add_model(
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    model_id=MODEL_ID,
    model_info=model_info
)
```



| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| str         | A message confirming that the model was added. |