---
title: "Settings"
slug: "settings"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:26:28 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Nov 02 2023 16:32:09 GMT+0000 (Coordinated Universal Time)"
---
![](https://files.readme.io/d937de2-Home_Page.png "Home_Page.png")

The Settings section captures team setup, permissions, and credentials. You can access the **Settings** page from the left menu of the Fiddler UI at all times.

These are the key tabs in **Settings**.

## General

The **General** tab shows your organization name, ID, email, and a few other details. The organization ID is needed when accessing Fiddler from the Fiddler Python API client.

![](https://files.readme.io/3f2e734-general.png "general.png")

## Access

The **Access** tab shows the users, teams, and invitations for everyone in the organization.

### Users

The **Users** tab shows all the users that are part of this organization.

![](https://files.readme.io/c8c5bf1-access_user.png "access_user.png")

### Teams

The **Teams** tab shows all the teams that are part of this organization.

![](https://files.readme.io/8cba270-access_team.png "access_team.png")

You can create a team by clicking on the plus (**`+`**) icon on the top-right.

> 🚧 Note
> 
> Only Administrators can create teams. The plus (**`+`**) icon will not be visible unless you have Administrator permissions.

![](https://files.readme.io/b0c4c53-access_create_team.png "access_create_team.png")

### Invitations

The **Invitations** tab shows all pending user invitations.

![](https://files.readme.io/5cb4046-access_invitation.png "access_invitation.png")

You can invite a user by clicking on the plus (**`+`**) icon on the top-right.

> 🚧 Note
> 
> Only Administrators can invite users. The plus (**`+`**) icon will not be visible unless you have Administrator permissions.

![](https://files.readme.io/abb030c-access_invite_user.png "access_invite_user.png")

## Credentials

The **Credentials** tab displays user access keys. These access keys are used by Fiddler Python client for authentication. Each Administrator or Member can create a unique key by clicking on **Create Key**.

![](https://files.readme.io/fce7911-credentials.png "credentials.png")



## Webhook Integrations

Webhook integrations allow you to configure Slack or other common webhook-based solutions to get notified by Fiddler. The "Webhook Integration" tab allows for managing the integrations.![](https://files.readme.io/69ad0d9-Screenshot_2023-10-09_at_4.41.55_PM.png "credentials.png")

### Configure a new Webhook integration

From the "Webhook Integrations" tab, use the + icon on the "Wehbook integrations" tab to configure a new webhook.

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/a0b33c4-Screenshot_2023-10-10_at_12.46.31_PM.png",
        null,
        ""
      ],
      "align": "center",
      "sizing": "50% "
    }
  ]
}
[/block]


You will need to specify the following. 

1. A unique webhook name in the "Service name" option. E.g: Fiddler_webhook 
2. Select your webhook service provider e.g: Slack
3. URL for the service provider where you want to read the messages from Fiddler in your webhook-enabled service. A valid URL : <https://hooks.slack.com/services/xxxxxxxxxx>
4. You can test the webhook service using the "Test" button after you have specified all the details.

### Edit or Delete a Webhook

[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/f7be111-Screenshot_2023-10-09_at_4.58.02_PM.png",
        "",
        ""
      ],
      "align": "center"
    }
  ]
}
[/block]


You can manage your webhook from the "Webhook Integrations" tab. 

1. Select the webhook that you want to edit/delete using the "..." icon towards the right of a webhook integration row.
2. Select the "Delete Webhook" option to delete the webhook

> 🚧 Deleting a Webhook
> 
> You will not be able to delete a webhook that is already linked to alerts. To delete the webhook, you will need to modify the alert and then delete the webhook

3. Select the Edit option to edit the webhook. You will be prompted with the pre-filled details of the webhook service configured.

[^1]\: _Join our [community Slack](https://www.fiddler.ai/slackinvite) to ask any questions_