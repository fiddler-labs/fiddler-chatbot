---
title: "client.list_datasets"
slug: "clientlist_datasets"
excerpt: "Retrieves the dataset IDs of all datasets accessible within a project."
hidden: false
createdAt: "2022-05-23T16:42:07.246Z"
updatedAt: "2023-08-01T11:55:23.941Z"
---
> 🚧 Deprecated
> 
> This client method is being deprecated and will not be supported in future versions of the client.  Use _client.get_dataset_names()_ instead.  
> Reference: [client.get_dataset_names](https://dash.readme.com/project/fiddler/v23.4/refs/clientget_dataset_names)

| Input Parameters | Type | Default | Description                            |
| :--------------- | :--- | :------ | :------------------------------------- |
| project_id       | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = "example_project"

client.list_datasets(
    project_id=PROJECT_ID
)
```

| Return Type | Description                                                 |
| :---------- | :---------------------------------------------------------- |
| list        | A list containing the project name string for each project. |

```python Response
[
    'dataset_a',
    'dataset_b',
    'dataset_c'
]
```