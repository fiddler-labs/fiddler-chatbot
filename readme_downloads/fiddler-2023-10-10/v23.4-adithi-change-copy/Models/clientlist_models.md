---
title: "client.list_models"
slug: "clientlist_models"
excerpt: "Retrieves the model IDs of all models accessible within a project."
hidden: false
createdAt: "2022-05-23T19:06:21.547Z"
updatedAt: "2023-08-01T12:06:28.989Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Use _client.model_names()_ instead.  
> Reference: [client.get_model_names](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_model_names)

| Input Parameter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = 'example_project'

client.list_models(
    project_id=PROJECT_ID
)
```

| Return Type | Description                                    |
| :---------- | :--------------------------------------------- |
| list        | A list containing the string ID of each model. |

```python Response
[
    'model_a',
    'model_b',
    'model_c'
]
```