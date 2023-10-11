---
title: "Authorization and Access Control"
slug: "authorization-and-access-control"
hidden: false
createdAt: "2022-04-19T20:26:44.914Z"
updatedAt: "2022-05-10T17:07:57.095Z"
---
[block:api-header]
{
  "title": "Organization Roles"
}
[/block]
Fiddler access control comes with some preset roles. There are two global roles at the organization level 

* ***ADMINISTRATOR*** — Has complete access over every aspect of the organization.
* ***MEMBER*** — Access is assigned at the project and model level.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0fbfca7-roles.png",
        "roles.png",
        1264,
        1318,
        "#e8eaed"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Project Roles"
}
[/block]
Each project supports its own set of permissions for its users.

There are three roles that can be assigned:

* ***OWNER*** — Assigns super-user permissions to the user.
* ***WRITE*** — Allows a user to perform write operations (e.g. uploading datasets and/or models, using slice and explain, sending events to Fiddler for monitoring, etc).
* ***READ*** — Allows a user to perform read operations (e.g. getting project/dataset/model metadata, accessing pre-existing charts, etc.).
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/3b07b46-project_roles.png",
        "project_roles.png",
        1262,
        684,
        "#d9dee3"
      ]
    }
  ]
}
[/block]
**Some notes about these roles:**

* A user who creates a project is assigned the **OWNER** role by default.
* A project **OWNER** or an organization **ADMINISTRATOR** can share/unshare projects with other users or teams.
* Only the **OWNER** only and an organization **ADMINISTRATOR** have access to a project until that project is explicitly shared with others.
* Project roles can be assigned to individual users or teams by the project
**OWNER** or by an organization **ADMINISTRATOR**.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/caf2bc9-project_settings.png",
        "project_settings.png",
        3178,
        712,
        "#fbfbfc"
      ]
    }
  ]
}
[/block]

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/97b71c4-project_settings_add.png",
        "project_settings_add.png",
        3172,
        790,
        "#83879a"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Teams"
}
[/block]
A team is a group of users.

* Each user can be a member of zero or more teams.
* Team roles are associated with project roles (i.e. teams can be granted
**READ**, **WRITE**, and/or **OWNER** permissions for a project).

Click [here](doc:settings#teams) for more information on teams.

[^1]: *Join our [community Slack](http://fiddler-community.slack.com/) to ask any questions*