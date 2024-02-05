---
title: "client.list_org_roles"
slug: "clientlist_org_roles"
excerpt: "Retrieves the names of all users and their permissions roles."
hidden: false
createdAt: "Wed May 25 2022 15:21:21 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
> 🚧 Warning
> 
> Only administrators can use _client.list_org_roles()_ .

```python Usage
client.list_org_roles()
```

| Return Type | Description                                                |
| :---------- | :--------------------------------------------------------- |
| dict        | A dictionary of users and their roles in the organization. |

```python Response
{
    'members': [
        {
            'id': 1,
            'user': 'admin@example.com',
            'email': 'admin@example.com',
            'isLoggedIn': True,
            'firstName': 'Example',
            'lastName': 'Administrator',
            'imageUrl': None,
            'settings': {'notifyNews': True,
                'notifyAccount': True,
                'sliceTutorialCompleted': True},
            'role': 'ADMINISTRATOR'
        },
        {
            'id': 2,
            'user': 'user@example.com',
            'email': 'user@example.com',
            'isLoggedIn': True,
            'firstName': 'Example',
            'lastName': 'User',
            'imageUrl': None,
            'settings': {'notifyNews': True,
                'notifyAccount': True,
                'sliceTutorialCompleted': True},
            'role': 'MEMBER'
        }
    ],
    'invitations': [
        {
            'id': 3,
            'user': 'newuser@example.com',
            'role': 'MEMBER',
            'invited': True,
            'link': 'http://app.fiddler.ai/signup/vSQWZkt3FP--pgzmuYe_-3-NNVuR58OLZalZOlvR0GY'
        }
    ]
}
```
