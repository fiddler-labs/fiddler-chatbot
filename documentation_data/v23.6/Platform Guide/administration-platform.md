---
title: "Administration"
slug: "administration-platform"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Nov 15 2022 18:09:04 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
## Organization Roles

Fiddler access control comes with some preset roles. There are two global roles at the organizational level 

- **_ADMINISTRATOR_** — Has complete access to every aspect of the organization.
  - As an administrator, you can [invite users](doc:inviting-users) to the platform.
- **_MEMBER_** — Access is assigned at the project and model level.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0fbfca7-roles.png",
        "roles.png",
        ""
      ],
      "align": "center",
      "sizing": "550px"
    }
  ]
}
[/block]



## Project Roles

Each project supports its own set of permissions for its users.

There are three roles that can be assigned:

- **_OWNER_** — Assigns super-user permissions to the user.
- **_WRITE_** — Allows a user to perform write operations (e.g. uploading datasets and/or models, using slice and explain, sending events to Fiddler for monitoring, etc).
- **_READ_** — Allows a user to perform read operations (e.g. getting project/dataset/model metadata, accessing pre-existing charts, etc.).

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/3b07b46-project_roles.png",
        "project_roles.png",
        ""
      ],
      "align": "center",
      "sizing": "550px"
    }
  ]
}
[/block]



**Some notes about these roles:**

- A user who creates a project is assigned the **OWNER** role by default.
- A project **OWNER** or an organization **ADMINISTRATOR** can share/unshare projects with other users or teams.
- Only the **OWNER** only and an organization **ADMINISTRATOR** have access to a project until that project is explicitly shared with others.
- Project roles can be assigned to individual users or teams by the project  
  **OWNER** or by an organization **ADMINISTRATOR**.

## Teams

A team is a group of users.

- Each user can be a member of zero or more teams.
- Team roles are associated with project roles (i.e. teams can be granted  
  **READ**, **WRITE**, and/or **OWNER** permissions for a project).

Click [here](doc:settings#teams) for more information on teams.

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_