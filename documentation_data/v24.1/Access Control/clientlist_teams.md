---
title: "client.list_teams"
slug: "clientlist_teams"
excerpt: "Retrieves the names of all teams and the users and roles within each team."
hidden: false
createdAt: "Wed May 25 2022 15:25:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
```python Usage
client.list_teams()
```

| Return Type | Description                                                |
| :---------- | :--------------------------------------------------------- |
| dict        | A dictionary containing information about teams and users. |

```python Response
{
    'example_team': {
        'members': [
            {
                'user': 'admin@example.com',
                'role': 'MEMBER'
            },
            {
                'user': 'user@example.com',
                'role': 'MEMBER'
            }
        ]
    }
}
```
