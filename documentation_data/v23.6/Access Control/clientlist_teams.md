---
title: "client.list_teams"
slug: "clientlist_teams"
excerpt: "Retrieves the names of all teams and the users and roles within each team."
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Wed May 25 2022 15:25:05 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Tue Oct 24 2023 04:14:06 GMT+0000 (Coordinated Universal Time)"
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