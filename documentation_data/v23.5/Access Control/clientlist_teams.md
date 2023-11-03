---
title: "client.list_teams"
slug: "clientlist_teams"
excerpt: "Retrieves the names of all teams and the users and roles within each team."
hidden: false
createdAt: "2022-05-25T15:25:05.212Z"
updatedAt: "2023-10-24T04:14:06.865Z"
---
[block:code]
{
  "codes": [
    {
      "code": "client.list_teams()",
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
    "0-1": "A dictionary containing information about teams and users."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n    'example_team': {\n        'members': [\n            {\n                'user': 'admin@example.com',\n                'role': 'MEMBER'\n            },\n            {\n                'user': 'user@example.com',\n                'role': 'MEMBER'\n            }\n        ]\n    }\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]