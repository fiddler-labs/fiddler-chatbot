---
title: "client.list_project_roles"
slug: "clientlist_project_roles"
excerpt: "Retrieves the names of users and their permissions roles for a given project."
hidden: false
createdAt: "Wed May 25 2022 15:23:56 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
| Input Paraemter | Type | Default | Description                            |
| :-------------- | :--- | :------ | :------------------------------------- |
| project_id      | str  | None    | The unique identifier for the project. |

```python Usage
PROJECT_ID = 'example_project'

client.list_project_roles(
    project_id=PROJECT_ID
)
```

| Return Type | Description                                                      |
| :---------- | :--------------------------------------------------------------- |
| dict        | A dictionary of users and their roles for the specified project. |

```python Response
{
    'roles': [
        {
            'user': {
                'email': 'admin@example.com'
            },
            'team': None,
            'role': {
                'name': 'OWNER'
            }
        },
        {
            'user': {
                'email': 'user@example.com'
            },
            'team': None,
            'role': {
                'name': 'READ'
            }
        }
    ]
}
```
