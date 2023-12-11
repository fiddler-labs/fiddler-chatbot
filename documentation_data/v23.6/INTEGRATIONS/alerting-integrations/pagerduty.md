---
title: "PagerDuty Integration"
slug: "pagerduty"
excerpt: ""
hidden: false
metadata: 
image: []
robots: "index"
createdAt: "Tue Apr 19 2022 20:19:10 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Oct 19 2023 20:59:24 GMT+0000 (Coordinated Universal Time)"
---
Fiddler offers powerful alerting tools for monitoring models. By integrating with  
PagerDuty services, you gain the ability to trigger PagerDuty events within your monitoring  
workflow.

> 📘 
> 
> If your organization has already integrated with PagerDuty, then you may skip to the [Setup: In Fiddler](#setup-in-fiddler) section to learn more about setting up PagerDuty within Fiddler.

## Setup: In PagerDuty

1. Within your PagerDuty Team, navigate to **Services** → **Service Directory**.

![](https://files.readme.io/0ae47bb-pagerduty_1.png "pagerduty_1.png")



2. Within the Service Directory:
   - If you are creating a new service for integration, select **+New Service** and follow the prompts to create your service.
   - Click the **name of the service** you want to integrate with.

![](https://files.readme.io/956dbdf-pagerduty_2.png "pagerduty_2.png")



3. Navigate to **Integrations** within your service, and select **Add a new integration to this service**.

![](https://files.readme.io/ca2e4c2-pagerduty_3.png "pagerduty_3.png")



4. Enter an **Integration Name**, and under **Integration Type** select the option **Use our API directly**. Then, select the **Add Integration** button to save your new integration. You will be redirected to the Integrations page for your service.

![](https://files.readme.io/0f5d5ae-pagerduty_4.png "pagerduty_4.png")



5. Copy the **Integration Key** for your new integration.

![](https://files.readme.io/e144e08-pagerduty_5.png "pagerduty_5.png")



## Setup: In Fiddler

1. Within **Fiddler**, navigate to the **Settings** page, and then to the **PagerDuty Integration** menu. If your organization **already has a PagerDuty service integrated with Fiddler**, you will be able to find it in the list of services.

![](https://files.readme.io/8de1a6b-pagerduty_setup_f_1.png "pagerduty_setup_f_1.png")



2. If you are looking to integrate with a new service, select the **`+`** box on the top right. Then, enter the name of your service, as well as the Integration Key copied from the end of the [Setup: In PagerDuty](#setup-in-pagerduty) section above. After creation, confirm that your new entry is now in the list of available services.

![](https://files.readme.io/9febb10-pagerduty_setup_f_2.png "pagerduty_setup_f_2.png")



> 🚧 
> 
> Creating, editing, and deleting these services is an **ADMINSTRATOR**-only privilege. Please contact an **ADMINSTRATOR** within your organization to setup any new PagerDuty services

## PagerDuty Alerts in Fiddler

1. Within the **Projects** page, select the model you wish to use with PagerDuty.

![](https://files.readme.io/d9ad82e-pagerduty_fiddler_1.png "pagerduty_fiddler_1.png")



2. Select **Monitor** → **Alerts** → **Add Alert**.

![](https://files.readme.io/b7118f0-pagerduty_fiddler_2.png "pagerduty_fiddler_2.png")



3. Enter the condition you would like to alert on, and under **PagerDuty Services**, select all services you would like the alert to trigger for. Additionally, select the **Severity** of this alert, and hit **Save**.

![](https://files.readme.io/8fbffde-pagerduty_fiddler_3.png "pagerduty_fiddler_3.png")



4. After creation, the alert will now trigger for the specified PagerDuty services.

> 📘 Info
> 
> Check out the [alerts documentation](doc:alerts-platform) for more information on setting up alerts.

## FAQ

**Can Fiddler integrate with multiple PagerDuty services?**

- Yes. So long as the service is present within **Settings** → **PagerDuty Services**, anyone within your organization can select that service to be a recipient for an alert.