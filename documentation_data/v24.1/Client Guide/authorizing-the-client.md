---
title: "Authorizing the Client"
slug: "authorizing-the-client"
excerpt: ""
hidden: false
createdAt: "Tue Apr 19 2022 17:18:59 GMT+0000 (Coordinated Universal Time)"
updatedAt: "Thu Dec 07 2023 22:32:06 GMT+0000 (Coordinated Universal Time)"
---
In order to use the client, you’ll need to provide some **authorization details**.

Specifically, there are three pieces of information that are required:

- The [URL](#finding-your-url) you are connecting to
- Your [organization ID](#finding-your-organization-id)
- An [authorization token](#finding-your-authorization-token) for your user

This information can be provided in **two ways**:

1. As arguments to the client when it's instantiated (see [`fdl.FiddlerApi`](ref:client-setup))
2. In a configuration file (see [`fiddler.ini`](#authorizing-via-configuration-file))

## Finding your URL

The URL should point to **wherever Fiddler has been deployed** for your organization.

If using Fiddler’s managed cloud service, it should be of the form  

```
https://app.fiddler.ai
```

## Finding your organization ID

To find your organization ID, navigate to the **Settings** page. Your organization ID will be immediately available on the **General** tab.

![](https://files.readme.io/2c7de6e-finding_your_org_id.png "finding_your_org_id.png")

## Finding your authorization token

To find your authorization token, first navigate to the **Settings** page. Then click **Credentials** and **Create Key**.

![](https://files.readme.io/ea51e6a-finding_your_auth_token.png "finding_your_auth_token.png")

## Connecting the Client

Once you've located the URL, the org_id and the authorization token, you can connect the Fiddler client to your environment.

```python Connect the Client
URL = 'https://app.fiddler.ai'
ORG_ID = 'my_org'
AUTH_TOKEN = '9AYWiqwxe2hnCAePxg-uEWJUDYRZIZKBSBpx0TvItnw' # not a valid token

# Connect to the Fiddler client
client = fdl.FiddlerApi(
    url=URL,
    org_id=ORG_ID,
    auth_token=AUTH_TOKEN
)
```

## Authorizing via configuration file

If you would prefer not to send authorization details as arguments to [`fdl.FiddlerApi`](ref:client-setup), you can specify them in a **configuration file** called `fiddler.ini`.

The file should be **located in the same directory as the script or notebook** that initializes the [`fdl.FiddlerApi`](ref:client-setup) object.

***

The syntax should follow the below example:

```python fiddler.ini
[FIDDLER]
url = https://app.fiddler.ai
org_id = my_org
auth_token = xtu4g_lReHyEisNg23xJ8IEex0YZEZeeEbTwAsupT0U
```

Then you can initialize the [`fdl.FiddlerApi`](ref:client-setup)object without any arguments, and Fiddler will automatically detect the `fiddler.ini` file:

```python Instantiate with fiddler.ini
client = fdl.FiddlerApi()
```
