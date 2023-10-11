---
title: "Authorization and Access Control"
slug: "authorization-and-access-control"
hidden: false
createdAt: "2022-04-19T20:26:44.914Z"
updatedAt: "2022-11-14T23:37:42.920Z"
---
## Organization Roles

Fiddler access control comes with some preset roles. There are two global roles at the organizational level 

- **_ADMINISTRATOR_** — Has complete access to every aspect of the organization.
- **_MEMBER_** — Access is assigned at the project and model level.

![](https://files.readme.io/0fbfca7-roles.png "roles.png")

## Project Roles

Each project supports its own set of permissions for its users.

There are three roles that can be assigned:

- **_OWNER_** — Assigns super-user permissions to the user.
- **_WRITE_** — Allows a user to perform write operations (e.g. uploading datasets and/or models, using slice and explain, sending events to Fiddler for monitoring, etc).
- **_READ_** — Allows a user to perform read operations (e.g. getting project/dataset/model metadata, accessing pre-existing charts, etc.).

![](https://files.readme.io/3b07b46-project_roles.png "project_roles.png")

**Some notes about these roles:**

- A user who creates a project is assigned the **OWNER** role by default.
- A project **OWNER** or an organization **ADMINISTRATOR** can share/unshare projects with other users or teams.
- Only the **OWNER** only and an organization **ADMINISTRATOR** have access to a project until that project is explicitly shared with others.
- Project roles can be assigned to individual users or teams by the project  
  **OWNER** or by an organization **ADMINISTRATOR**.

![](https://files.readme.io/caf2bc9-project_settings.png "project_settings.png")

![](https://files.readme.io/97b71c4-project_settings_add.png "project_settings_add.png")

## Teams

A team is a group of users.

- Each user can be a member of zero or more teams.
- Team roles are associated with project roles (i.e. teams can be granted  
  **READ**, **WRITE**, and/or **OWNER** permissions for a project).

Click [here](doc:settings#teams) for more information on teams.

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_