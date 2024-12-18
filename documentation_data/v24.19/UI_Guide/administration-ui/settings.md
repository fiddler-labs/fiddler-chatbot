---
title: Settings
slug: settings
excerpt: ''
createdAt: Tue Apr 19 2022 20:26:28 GMT+0000 (Coordinated Universal Time)
updatedAt: Mon Apr 29 2024 22:25:47 GMT+0000 (Coordinated Universal Time)
---

# Application Settings

### Overview

The Settings section captures team setup, permissions, and credentials. You can access the **Settings** page from the user settings on the left navigation bar of the Fiddler UI.

![Fiddler home page showing the user menu open and highlighting the Settings link.](../../.gitbook/assets/728d8bf-Screen\_Shot\_2024-04-29\_at\_6.21.41\_PM.png)

### Key Tabs within Settings

#### General

The **General** tab shows your organization name, your email, and a few other details.

![General tab of the Settings page.](../../.gitbook/assets/3f2e734-general.png)

#### Access

The **Access** tab shows the users, teams, and invitations for everyone in the organization.

**Users**

The **Users** sub-tab shows all the users that are members of this organization.

![Users sub-tab of the Access tab on the Settings page showing a list of users.](../../.gitbook/assets/c8c5bf1-access\_user.png)

**Teams**

The **Teams** tab shows all the teams that have been defined for this organization.

![Teams  sub-tab of the Access tab on the Settings page showing a list of teams](../../.gitbook/assets/settings-access-teams-dir.png)

You can create a team by clicking on the plus (**`+`**) icon on the top-right.

> 🚧 Note
>
> Only Org Admins can create teams. The plus (**`+`**) icon will not be visible unless you have the Org Admin role.

![](../../.gitbook/assets/b0c4c53-access\_create\_team.png)

**Invitations**

The **Invitations** tab shows all pending user invitations. Invitations that have been accepted no longer appear.

![Invitations sub-tab of the Access tab on the Settings page with a list of user invitations.](../../.gitbook/assets/5cb4046-access\_invitation.png)

You can invite a user by clicking on the plus (**`+`**) icon on the top-right.

> 🚧 Note
>
> Only Org Admins can invite users. The plus (**`+`**) icon will not be visible unless you have the Org Admin role.

![](../../.gitbook/assets/abb030c-access\_invite\_user.png)

### Credentials

The **Credentials** tab displays user access keys. These access keys are used by Fiddler Python client for authentication. Each Org Admin or Org Member can create a unique key by clicking on **Create Key**.

![Credentials sub-tab of the Access tab on the Settings page with a list of keys and highlighting the create key button.](../../.gitbook/assets/fce7911-credentials.png)

### Webhooks

Webhooks enable you to link Fiddler to your own notification and communication services and have them receive Fiddler alerts as they are triggered. We support Slack webhook integration directly as well as a custom webhook that can be used with any webhook-consuming platform.\
You can manage these webhooks in the 'Webhook Integration' tab.

**Configure a New Slack Webhook**

From the "Webhook Integrations" tab, use the + icon on the "Webhook Integration" tab to configure a new webhook.

![Create Webhook Service modal dialog](../../.gitbook/assets/a0b33c4-Screenshot\_2023-10-10\_at\_12.46.31\_PM.png)

Follow these steps:

1. Enter a unique webhook name in the **Service Name** textbox
2. Select Slack in the **Provider** dropdown
3. Enter the Slack webhook URL provided by your Slack administrator which will appear similar to this example: [https://hooks.slack.com/services/xxxxxxxxxx](https://hooks.slack.com/services/xxxxxxxxxx)
4. Test the webhook service using the **Test** button
5. Click the **Create** button once the test is successful

Slack documentation on creating webhooks can be reviewed [here](https://api.slack.com/messaging/webhooks).

**Configure a New Custom Webhook**

To configure a webhook for any other platform, follow the same steps listed for the Slack webhook, but instead select **Other** for Provider type and enter the webhook URL provided by the platform's administrator.

1. Enter a unique webhook name in the **Service Name** textbox
2. Select Other in the **Provider** dropdown
3. Enter the webhook URL provided by your platform administrator
4. Test the webhook service using the **Test** button
5. Click the **Create** button once the test is successful

> 🚧 Custom Webhooks
>
> Note that many platforms will require some amount of configuration in order to properly receive and act on the notifications sent by third party software like Fiddler.

#### Edit or Delete a Webhook

![Webhooks list on the Webhook Integration tab with Delete Webhook and Edit Webhook actions](../../.gitbook/assets/f7be111-Screenshot\_2023-10-09\_at\_4.58.02\_PM.png)

You can manage your webhook from the **Webhook Integrations** tab.

1. Select the webhook that you want to edit/delete using the "..." icon towards the right of a webhook integration row.
2. Select the **Delete Webhook** option to delete the webhook

> 🚧 Deleting a Webhook
>
> You will not be able to delete a webhook that is already linked to alerts. To delete the webhook, you will need to modify the alert and then delete the webhook

3. Select the **Edit Webhook** option to edit the webhook
4. Click the **Test** button to test your changes
5. Click the **Save** button once the test is successful

{% include "../../.gitbook/includes/main-doc-footer.md" %}

