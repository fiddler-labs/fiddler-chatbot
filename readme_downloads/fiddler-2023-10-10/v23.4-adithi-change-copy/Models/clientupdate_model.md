---
title: "client.update_model"
slug: "clientupdate_model"
excerpt: "Replaces the model artifact for a model."
hidden: false
createdAt: "2022-05-23T19:26:42.714Z"
updatedAt: "2023-08-01T13:45:51.369Z"
---
For more information, see [Uploading a Model Artifact](doc:uploading-model-artifacts).

> 🚧 Deprecated
> 
> This client method is deprecated and will not be supported.  This method is is split into  _client.update_model_artifact()_ and _client.update_model()_.

> 🚧 Warning
> 
> This function does not allow for changes in a model's schema. The inputs and outputs to the model must remain the same.

| Input Parameter   | Type                             | Default | Description                                                                                                                       |
| :---------------- | :------------------------------- | :------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| project_name      | str                              | None    | The unique identifier for the project.                                                                                            |
| model_name        | str                              | None    | A unique identifier for the model.                                                                                                |
| info              | Optional[ModelInfo]              | None    | Model related information passed as dictionary from user.                                                                         |
| file_list         | Optional\[List\[Dict[str, Any]]] | None    | A list containing a dictionary of artifact files and their names.                                                                 |
| framework         | Optional[str]                    | None    | Model framework name.                                                                                                             |
| requirements      | Optional[str]                    | None    | Requirements of the model.                                                                                                        |
| project_id        | str                              | None    | `Deprecated` The unique identifier for the project.                                                                               |
| model_id          | str                              | None    | `Deprecated` A unique identifier for the model.                                                                                   |
| model_dir         | pathlib.Path                     | None    | `Deprecated` A path to the directory containing all of the model files needed to run the model.                                   |
| force_pre_compute | bool                             | True    | If True, re-run precomputation steps for the model. This can also be done manually by calling **client.trigger_pre_computation**. |

```python Usage
import pathlib

PROJECT_ID = 'example_project'
MODEL_ID = 'example_model'

model_dir = pathlib.Path('model_dir')

client.update_model(
    project_name=PROJECT_NAME,
    model_name=MODEL_NAME
)
```

| Return Type | Description                                           |
| :---------- | :---------------------------------------------------- |
| bool        | A boolean denoting whether the update was successful. |

```python Response
True
```