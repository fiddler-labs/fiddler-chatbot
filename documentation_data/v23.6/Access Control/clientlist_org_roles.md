---
title: "client.list_org_roles"
slug: "clientlist_org_roles"
excerpt: "Retrieves the names of all users and their permissions roles."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed May 25 2022 15:21:21 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
---
[block:callout]
{
  "type": "warning",
  "title": "Warning",
  "body": "Only administrators can use *client.list_org_roles()* ."
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "client.list_org_roles()",
      "language": "python",
      "name": "Usage"
    }
  ]
}
[/block]

[block:parameters]
{
  "data": {
    "h-0": "Return Type",
    "h-1": "Description",
    "0-0": "dict",
    "0-1": "A dictionary of users and their roles in the organization."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n    'members': [\n        {\n            'id': 1,\n            'user': 'admin@example.com',\n            'email': 'admin@example.com',\n            'isLoggedIn': True,\n            'firstName': 'Example',\n            'lastName': 'Administrator',\n            'imageUrl': None,\n            'settings': {'notifyNews': True,\n                'notifyAccount': True,\n                'sliceTutorialCompleted': True},\n            'role': 'ADMINISTRATOR'\n        },\n        {\n            'id': 2,\n            'user': 'user@example.com',\n            'email': 'user@example.com',\n            'isLoggedIn': True,\n            'firstName': 'Example',\n            'lastName': 'User',\n            'imageUrl': None,\n            'settings': {'notifyNews': True,\n                'notifyAccount': True,\n                'sliceTutorialCompleted': True},\n            'role': 'MEMBER'\n        }\n    ],\n    'invitations': [\n        {\n            'id': 3,\n            'user': 'newuser@example.com',\n            'role': 'MEMBER',\n            'invited': True,\n            'link': 'http://app.fiddler.ai/signup/vSQWZkt3FP--pgzmuYe_-3-NNVuR58OLZalZOlvR0GY'\n        }\n    ]\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]