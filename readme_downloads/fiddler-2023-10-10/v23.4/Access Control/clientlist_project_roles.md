---
title: "client.list_project_roles"
slug: "clientlist_project_roles"
excerpt: "Retrieves the names of users and their permissions roles for a given project."
hidden: false
createdAt: "2022-05-25T15:23:56.444Z"
updatedAt: "2022-06-21T17:25:22.253Z"
---
[block:parameters]
{
  "data": {
    "h-0": "Input Paraemter",
    "h-1": "Type",
    "h-2": "Default",
    "h-3": "Description",
    "0-0": "project_id",
    "0-1": "str",
    "0-2": "None",
    "0-3": "The unique identifier for the project."
  },
  "cols": 4,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "PROJECT_ID = 'example_project'\n\nclient.list_project_roles(\n    project_id=PROJECT_ID\n)",
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
    "0-1": "A dictionary of users and their roles for the specified project."
  },
  "cols": 2,
  "rows": 1
}
[/block]

[block:code]
{
  "codes": [
    {
      "code": "{\n    'roles': [\n        {\n            'user': {\n                'email': 'admin@example.com'\n            },\n            'team': None,\n            'role': {\n                'name': 'OWNER'\n            }\n        },\n        {\n            'user': {\n                'email': 'user@example.com'\n            },\n            'team': None,\n            'role': {\n                'name': 'READ'\n            }\n        }\n    ]\n}",
      "language": "python",
      "name": "Response"
    }
  ]
}
[/block]