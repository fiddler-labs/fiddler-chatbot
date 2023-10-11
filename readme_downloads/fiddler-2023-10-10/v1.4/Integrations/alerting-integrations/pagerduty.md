---
title: "PagerDuty Integration"
slug: "pagerduty"
hidden: false
createdAt: "2022-04-19T20:19:10.407Z"
updatedAt: "2022-06-08T15:51:32.444Z"
---
Fiddler offers powerful alerting tools for monitoring models. By integrating with
PagerDuty services, you gain the ability to trigger PagerDuty events within your monitoring
workflow.
[block:callout]
{
  "type": "info",
  "body": "If your organization has already integrated with PagerDuty, then you may skip to the [Setup: In Fiddler](#setup-in-fiddler) section to learn more about setting up PagerDuty within Fiddler."
}
[/block]

[block:api-header]
{
  "title": "Setup: In PagerDuty"
}
[/block]
1. Within your PagerDuty Team, navigate to **Services** → **Service Directory**.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0ae47bb-pagerduty_1.png",
        "pagerduty_1.png",
        747,
        327,
        "#f2f2f2"
      ]
    }
  ]
}
[/block]
2. Within the Service Directory:
    * If you are creating a new service for integration, select **+New Service** and follow the prompts to create your service.
    * Click the **name of the service** you want to integrate with.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/956dbdf-pagerduty_2.png",
        "pagerduty_2.png",
        1048,
        755,
        "#f3f3f4"
      ]
    }
  ]
}
[/block]
3. Navigate to **Integrations** within your service, and select **Add a new integration to this service**.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ca2e4c2-pagerduty_3.png",
        "pagerduty_3.png",
        1016,
        624,
        "#f2f6f3"
      ]
    }
  ]
}
[/block]
4. Enter an **Integration Name**, and under **Integration Type** select the option **Use our API directly**. Then, select the **Add Integration** button to save your new integration. You will be redirected to the Integrations page for your service.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/0f5d5ae-pagerduty_4.png",
        "pagerduty_4.png",
        574,
        471,
        "#ececeb"
      ]
    }
  ]
}
[/block]
5. Copy the **Integration Key** for your new integration.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/e144e08-pagerduty_5.png",
        "pagerduty_5.png",
        1132,
        571,
        "#f1f6f2"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Setup: In Fiddler"
}
[/block]
1. Within **Fiddler**, navigate to the **Settings** page, and then to the **PagerDuty Integration** menu. If your organization **already has a PagerDuty service integrated with Fiddler**, you will be able to find it in the list of services.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8de1a6b-pagerduty_setup_f_1.png",
        "pagerduty_setup_f_1.png",
        2880,
        888,
        "#f1f3f7"
      ]
    }
  ]
}
[/block]
2. If you are looking to integrate with a new service, select the **`+`** box on the top right. Then, enter the name of your service, as well as the Integration Key copied from the end of the [Setup: In PagerDuty](#setup-in-pagerduty) section above. After creation, confirm that your new entry is now in the list of available services.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/9febb10-pagerduty_setup_f_2.png",
        "pagerduty_setup_f_2.png",
        2880,
        1524,
        "#71768d"
      ]
    }
  ]
}
[/block]

[block:callout]
{
  "type": "warning",
  "body": "Creating, editing, and deleting these services is an **ADMINSTRATOR**-only privilege. Please contact an **ADMINSTRATOR** within your organization to setup any new PagerDuty services"
}
[/block]

[block:api-header]
{
  "title": "PagerDuty Alerts in Fiddler"
}
[/block]
1. Within the **Projects** page, select the model you wish to use with PagerDuty.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/d9ad82e-pagerduty_fiddler_1.png",
        "pagerduty_fiddler_1.png",
        2854,
        1328,
        "#f1f2f7"
      ]
    }
  ]
}
[/block]
2. Select **Monitor** → **Alerts** → **Add Alert**.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/b7118f0-pagerduty_fiddler_2.png",
        "pagerduty_fiddler_2.png",
        2740,
        880,
        "#fafafb"
      ]
    }
  ]
}
[/block]
3. Enter the condition you would like to alert on, and under **PagerDuty Services**, select all services you would like the alert to trigger for. Additionally, select the **Severity** of this alert, and hit **Save**.


[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/8fbffde-pagerduty_fiddler_3.png",
        "pagerduty_fiddler_3.png",
        1152,
        1478,
        "#f9fafb"
      ]
    }
  ]
}
[/block]
4. After creation, the alert will now trigger for the specified PagerDuty services.
[block:callout]
{
  "type": "info",
  "body": "Check out the [alerts documentation](doc:alerts) for more information on setting up alerts.",
  "title": "Info"
}
[/block]

[block:api-header]
{
  "title": "FAQ"
}
[/block]
**Can Fiddler integrate with multiple PagerDuty services?**

* Yes. So long as the service is present within **Settings** → **PagerDuty Services**, anyone within your organization can select that service to be a recipient for an alert.