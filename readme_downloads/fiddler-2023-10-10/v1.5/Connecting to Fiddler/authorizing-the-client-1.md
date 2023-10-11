---
title: "Authorizing the Client"
slug: "authorizing-the-client-1"
hidden: false
createdAt: "2022-04-19T17:18:59.729Z"
updatedAt: "2022-06-21T20:25:56.106Z"
---
In order to use the client, you’ll need to provide some **authorization details**.

Specifically, there are three pieces of information that are required:

* The [URL](#finding-your-url) you are connecting to
* Your [organization ID](#finding-your-organization-id)
* An [authorization token](#finding-your-authorization-token) for your user



This information can be provided in **two ways**:

1. As arguments to the client when it's instantiated (see [`fdl.FiddlerApi`](https://api.fiddler.ai/#fdl-fiddlerapi))
2. In a configuration file (see [`fiddler.ini`](#authorizing-via-configuration-file))
[block:api-header]
{
  "title": "Finding your URL"
}
[/block]
The URL should point to **wherever Fiddler has been deployed** for your organization.

If using Fiddler’s managed cloud service, it should be of the form  

```
https://app.fiddler.ai
```
[block:api-header]
{
  "title": "Finding your organization ID"
}
[/block]
To find your organization ID, navigate to the **Settings** page. Your organization ID will be immediately available on the **General** tab.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/2c7de6e-finding_your_org_id.png",
        "finding_your_org_id.png",
        1260,
        860,
        "#eef0f5"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Finding your authorization token"
}
[/block]
To find your authorization token, first navigate to the **Settings** page. Then click **Credentials** and **Create Key**.
[block:image]
{
  "images": [
    {
      "image": [
        "https://files.readme.io/ea51e6a-finding_your_auth_token.png",
        "finding_your_auth_token.png",
        1260,
        860,
        "#eff0f6"
      ]
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Connecting the Client"
}
[/block]
Once you've located the URL, the org_id and the authorization token, you can connect the Fiddler client to your environment.
[block:code]
{
  "codes": [
    {
      "code": "URL = 'https://app.fiddler.ai'\nORG_ID = 'my_org'\nAUTH_TOKEN = '9AYWiqwxe2hnCAePxg-uEWJUDYRZIZKBSBpx0TvItnw' # not a valid token\n\n# Connect to the Fiddler client\nclient = fdl.FiddlerApi(\n    url=URL,\n    org_id=ORG_ID,\n    auth_token=AUTH_TOKEN\n)",
      "language": "python",
      "name": "Connect the Client"
    }
  ]
}
[/block]

[block:api-header]
{
  "title": "Authorizing via configuration file"
}
[/block]
If you would prefer not to send authorization details as arguments to [`fdl.FiddlerApi`](https://api.fiddler.ai/#fdl-fiddlerapi), you can specify them in a **configuration file** called `fiddler.ini`.

The file should be **located in the same directory as the script or notebook** that initializes the [`fdl.FiddlerApi`](https://api.fiddler.ai/#fdl-fiddlerapi) object.

***

The syntax should follow the below example:
[block:code]
{
  "codes": [
    {
      "code": "[FIDDLER]\nurl = https://app.fiddler.ai\norg_id = my_org\nauth_token = xtu4g_lReHyEisNg23xJ8IEex0YZEZeeEbTwAsupT0U",
      "language": "python",
      "name": "fiddler.ini"
    }
  ]
}
[/block]
Then you can initialize the [`fdl.FiddlerApi`](https://api.fiddler.ai/#fdl-fiddlerapi) object without any arguments, and Fiddler will automatically detect the `fiddler.ini` file:
[block:code]
{
  "codes": [
    {
      "code": "client = fdl.FiddlerApi()",
      "language": "python",
      "name": "Instantiate with fiddler.ini"
    }
  ]
}
[/block]