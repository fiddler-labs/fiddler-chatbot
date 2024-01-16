---
title: "Single Sign On with Okta"
slug: "okta-integration"
excerpt: ""
hidden: false
createdAt: "Mon Aug 01 2022 15:14:37 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
## Overview

These instructions will help administrators configure Fiddler to be used with an existing Okta single sign on application.

## Okta Setup:

First, you must create an OIDC based application within Okta. Your application will require a callback URL during setup time. This URL will be provided to you by a Fiddler administrator. Your application should grant "Authorization Code" permissions to a client acting on behalf of a user. See the image below for how your setup might look like:

![](https://files.readme.io/b7b67fe-Screen_Shot_2022-08-07_at_10.22.36_PM.png)

This is the stage where you can allow certain users of your organization access to Fiddler through Okta. You can use the "Group Assignments" field to choose unique sets of organization members to grant access to. This setup stage will also allow for Role Based Access Control (i.e. RBAC) based on specific groups using your application.

Once your application has been set up, a Fiddler administrator will need to receive the following information and credentials:

- Okta domain
- Client ID
- Client Secret
- Okta Account Type (default or custom)

All of the above can be obtained from your Okta application dashboard, as shown in the pictures below:

![](https://files.readme.io/6442827-Screen_Shot_2022-08-07_at_10.30.03_PM.png)

![](https://files.readme.io/f1dbcf6-Screen_Shot_2022-08-07_at_10.30.15_PM.png)

You can also pass the above information to your Fiddler administrator via your okta.yml file. 

## Logging into Fiddler:

Once a Fiddler administrator has successfully set up a deployment for your organization using your given Okta credentials, you should see the “Sign in with SSO” button enabled. When this button is clicked, you should be navigated to an Okta login screen. Once successfully authenticated, and assuming you have been granted access to Fiddler through Okta, you should be able to login to Fiddler.

![](https://files.readme.io/c96a709-Screen_Shot_2022-08-07_at_10.36.40_PM.png)

NOTES:

1. To be able to login with SSO, it is initially required for the user to register with Fiddler Application. Upon successful registration, the users will be able to login using SSO.
2. The only information Fiddler stores from Okta based logins is a user’s first name, last name, email address, and OIDC token.
3. Fiddler does not currently support using Okta based login through its API (see fiddler-client). In order to use an Okta based account through Fiddler's API, use a valid access token which can be created and copied on the “Credentials” tab on Fiddler’s “Settings” page.
